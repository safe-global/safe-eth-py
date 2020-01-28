import math
from logging import getLogger
from typing import List, NamedTuple, Optional

from eth_abi.packed import encode_abi_packed
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.constants import GAS_CALL_DATA_BYTE, NULL_ADDRESS
from gnosis.eth.contracts import (get_proxy_factory_contract,
                                  get_safe_contract, get_safe_V1_0_0_contract)
from gnosis.eth.utils import generate_address_2

logger = getLogger(__name__)


class InvalidERC20Token(Exception):
    pass


class SafeCreate2Tx(NamedTuple):
    salt_nonce: int
    owners: List[str]
    threshold: int
    fallback_handler: str
    master_copy_address: str
    proxy_factory_address: str
    payment_receiver: str
    payment_token: str
    payment: int
    gas: int
    gas_price: int
    payment_token_eth_value: float
    fixed_creation_cost: Optional[int]
    safe_address: str
    safe_setup_data: bytes

    @property
    def payment_ether(self):
        return self.gas * self.gas_price


class SafeCreate2TxBuilder:
    def __init__(self, w3: Web3, master_copy_address: str, proxy_factory_address: str):
        """
        Init builder for safe creation using create2
        :param w3: Web3 instance
        :param master_copy_address: `Gnosis Safe` master copy address
        :param proxy_factory_address: `Gnosis Proxy Factory` address
        """
        assert Web3.isChecksumAddress(master_copy_address)
        assert Web3.isChecksumAddress(proxy_factory_address)

        self.w3 = w3
        self.master_copy_address = master_copy_address
        self.proxy_factory_address = proxy_factory_address
        self.safe_version = get_safe_contract(w3, master_copy_address).functions.VERSION().call()
        if self.safe_version == '1.1.1':
            self.master_copy_contract = get_safe_contract(w3, master_copy_address)
        elif self.safe_version == '1.0.0':
            self.master_copy_contract = get_safe_V1_0_0_contract(w3, master_copy_address)
        else:
            raise ValueError('Safe version must be 1.1.1 or 1.0.0')
        self.proxy_factory_contract = get_proxy_factory_contract(w3, proxy_factory_address)

    def build(self, owners: List[str], threshold: int, salt_nonce: int,
              gas_price: int, fallback_handler: Optional[str] = None, payment_receiver: Optional[str] = None,
              payment_token: Optional[str] = None,
              payment_token_eth_value: float = 1.0, fixed_creation_cost: Optional[int] = None):
        """
        Prepare Safe creation
        :param owners: Owners of the Safe
        :param threshold: Minimum number of users required to operate the Safe
        :param fallback_handler: Handler for fallback calls to the Safe
        :param salt_nonce: Web3 instance
        :param gas_price: Gas Price
        :param payment_receiver: Address to refund when the Safe is created. Address(0) if no need to refund
        :param payment_token: Payment token instead of paying the funder with ether. If None Ether will be used
        :param payment_token_eth_value: Value of payment token per 1 Ether
        :param fixed_creation_cost: Fixed creation cost of Safe (Wei)
        """

        assert 0 < threshold <= len(owners)
        fallback_handler = fallback_handler or NULL_ADDRESS
        payment_receiver = payment_receiver or NULL_ADDRESS
        payment_token = payment_token or NULL_ADDRESS
        assert Web3.isChecksumAddress(payment_receiver)
        assert Web3.isChecksumAddress(payment_token)

        # Get bytes for `setup(address[] calldata _owners, uint256 _threshold, address to, bytes calldata data,
        # address paymentToken, uint256 payment, address payable paymentReceiver)`
        # This initializer will be passed to the ProxyFactory to be called right after proxy is deployed
        # We use `payment=0` as safe has no ether yet and estimation will fail
        safe_setup_data: bytes = self._get_initial_setup_safe_data(owners, threshold, fallback_handler=fallback_handler,
                                                                   payment_token=payment_token,
                                                                   payment_receiver=payment_receiver)

        magic_gas: int = self._calculate_gas(owners, safe_setup_data, payment_token)
        estimated_gas: int = self._estimate_gas(safe_setup_data,
                                                salt_nonce, payment_token, payment_receiver)
        logger.debug('Magic gas %d - Estimated gas %d' % (magic_gas, estimated_gas))
        gas = max(magic_gas, estimated_gas)

        # Payment will be safe deploy cost
        payment = self._calculate_refund_payment(gas,
                                                 gas_price,
                                                 fixed_creation_cost,
                                                 payment_token_eth_value)

        # Now we have a estimate for `payment` so we get initialization data again
        final_safe_setup_data: bytes = self._get_initial_setup_safe_data(owners, threshold,
                                                                         fallback_handler=fallback_handler,
                                                                         payment_token=payment_token, payment=payment,
                                                                         payment_receiver=payment_receiver)

        safe_address = self.calculate_create2_address(final_safe_setup_data, salt_nonce)
        assert int(safe_address, 16), 'Calculated Safe address cannot be the NULL ADDRESS'

        return SafeCreate2Tx(salt_nonce, owners, threshold, fallback_handler,
                             self.master_copy_address, self.proxy_factory_address,
                             payment_receiver, payment_token, payment, gas, gas_price, payment_token_eth_value,
                             fixed_creation_cost, safe_address, final_safe_setup_data)

    @staticmethod
    def _calculate_gas(owners: List[str], safe_setup_data: bytes, payment_token: str) -> int:
        """
        Calculate gas manually, based on tests of previosly deployed safes
        :param owners: Safe owners
        :param safe_setup_data: Data for proxy setup
        :param payment_token: If payment token, we will need more gas to transfer and maybe storage if first time
        :return: total gas needed for deployment
        """
        base_gas = 205000  # Transaction base gas

        # If we already have the token, we don't have to pay for storage, so it will be just 5K instead of 20K.
        # The other 1K is for overhead of making the call
        if payment_token != NULL_ADDRESS:
            payment_token_gas = 55000
        else:
            payment_token_gas = 0

        data_gas = GAS_CALL_DATA_BYTE * len(safe_setup_data)  # Data gas
        gas_per_owner = 20000  # Magic number calculated by testing and averaging owners
        return base_gas + data_gas + payment_token_gas + len(owners) * gas_per_owner

    @staticmethod
    def _calculate_refund_payment(gas: int, gas_price: int, fixed_creation_cost: Optional[int],
                                  payment_token_eth_value: float) -> int:
        if fixed_creation_cost is None:
            # Payment will be safe deploy cost + transfer fees for sending ether to the deployer
            base_payment: int = gas * gas_price
            # Calculate payment for tokens using the conversion (if used)
            return math.ceil(base_payment / payment_token_eth_value)
        else:
            return fixed_creation_cost

    def calculate_create2_address(self, safe_setup_data: bytes, salt_nonce: int):
        proxy_creation_code = self.proxy_factory_contract.functions.proxyCreationCode().call()
        salt = self.w3.keccak(encode_abi_packed(['bytes', 'uint256'], [self.w3.keccak(safe_setup_data), salt_nonce]))
        deployment_data = encode_abi_packed(['bytes', 'uint256'], [proxy_creation_code,
                                                                   int(self.master_copy_address, 16)])
        return generate_address_2(self.proxy_factory_contract.address, salt, deployment_data)

    def _estimate_gas(self, initializer: bytes, salt_nonce: int,
                      payment_token: str, payment_receiver: str) -> int:
        """
        Gas estimation done using web3 and calling the node
        Payment cannot be estimated, as no ether is in the address. So we add some gas later.
        :param initializer: Data initializer to send to GnosisSafe setup method
        :param salt_nonce: Nonce that will be used to generate the salt to calculate
        the address of the new proxy contract.
        :return: Total gas estimation
        """

        # Estimate the contract deployment. We cannot estimate the refunding, as the safe address has not any fund
        gas: int = self.proxy_factory_contract.functions.createProxyWithNonce(self.master_copy_address,
                                                                              initializer, salt_nonce).estimateGas()

        # It's not very relevant if is 1 or 9999
        payment: int = 1

        # We estimate the refund as a new tx
        if payment_token == NULL_ADDRESS:
            # Same cost to send 1 ether than 1000
            gas += self.w3.eth.estimateGas({'to': payment_receiver, 'value': payment})
        else:
            # Top should be around 52000 when storage is needed (funder no previous owner of token),
            # we use value 1 as we are simulating an internal call, and in that calls you don't pay for the data.
            # If it was a new tx sending 5000 tokens would be more expensive than sending 1 because of data costs
            gas += 55000
            # try:
            #     gas += get_erc20_contract(self.w3,
            #                               payment_token).functions.transfer(payment_receiver,
            #                                                                 payment).estimateGas({'from':
            #                                                                                      payment_token})
            # except ValueError as exc:
            #     raise InvalidERC20Token from exc

        return gas

    def _get_initial_setup_safe_data(self, owners: List[str], threshold: int,
                                     fallback_handler: str = NULL_ADDRESS,
                                     payment_token: str = NULL_ADDRESS,
                                     payment: int = 0,
                                     payment_receiver: str = NULL_ADDRESS) -> bytes:
        if self.safe_version == '1.1.1':
            return HexBytes(self.master_copy_contract.functions.setup(
                owners,
                threshold,
                NULL_ADDRESS,  # Contract address for optional delegate call
                b'',            # Data payload for optional delegate call
                fallback_handler,  # Handler for fallback calls to this contract
                payment_token,
                payment,
                payment_receiver
            ).buildTransaction({
                'gas': 1,
                'gasPrice': 1,
            })['data'])
        elif self.safe_version == '1.0.0':
            return HexBytes(self.master_copy_contract.functions.setup(
                owners,
                threshold,
                NULL_ADDRESS,  # Contract address for optional delegate call
                b'',  # Data payload for optional delegate call
                payment_token,
                payment,
                payment_receiver
            ).buildTransaction({
                'gas': 1,
                'gasPrice': 1,
            })['data'])
        else:
            raise ValueError('Safe version must be 1.1.1 or 1.0.0')
