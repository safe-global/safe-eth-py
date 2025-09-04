import math
from logging import getLogger
from typing import List, NamedTuple, Optional, Sequence

from eth_abi.packed import encode_packed
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.types import TxParams, Wei

from safe_eth.eth.constants import GAS_CALL_DATA_BYTE, NULL_ADDRESS
from safe_eth.eth.contracts import (
    get_proxy_factory_contract,
    get_safe_contract,
    get_safe_V1_0_0_contract,
    get_safe_V1_1_1_contract,
    get_safe_V1_3_0_contract,
    get_safe_V1_4_1_contract,
    get_safe_V1_5_0_contract,
)
from safe_eth.eth.utils import (
    fast_is_checksum_address,
    get_empty_tx_params,
    mk_contract_address_2,
)

from .constants import TOKEN_TRANSFER_GAS

logger = getLogger(__name__)


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
    """
    Helper to create Safes using Safe's Proxy Factory with CREATE2
    """

    MASTER_COPY_VERSION_WITH_CONTRACT = {
        "1.5.0": get_safe_V1_5_0_contract,
        "1.4.1": get_safe_V1_4_1_contract,
        "1.3.0": get_safe_V1_3_0_contract,
        "1.1.1": get_safe_V1_1_1_contract,
        "1.0.0": get_safe_V1_0_0_contract,
    }

    def __init__(
        self,
        w3: Web3,
        master_copy_address: ChecksumAddress,
        proxy_factory_address: ChecksumAddress,
    ):
        """
        :param w3: Web3 instance
        :param master_copy_address: `Safe` master copy address
        :param proxy_factory_address: `Safe Proxy Factory` address
        """
        assert fast_is_checksum_address(master_copy_address)
        assert fast_is_checksum_address(proxy_factory_address)

        self.w3 = w3
        self.master_copy_address = master_copy_address
        self.proxy_factory_address = proxy_factory_address

        # Check Safe master copy version
        self.safe_version = (
            get_safe_contract(w3, master_copy_address).functions.VERSION().call()
        )
        master_copy_contract_fn = self.MASTER_COPY_VERSION_WITH_CONTRACT.get(
            self.safe_version
        )
        if not master_copy_contract_fn:
            raise ValueError("Safe version must be 1.5.0, 1.4.1, 1.3.0, 1.1.1 or 1.0.0")

        self.master_copy_contract = master_copy_contract_fn(w3, master_copy_address)

        self.proxy_factory_contract = get_proxy_factory_contract(
            w3, proxy_factory_address
        )

    def build(
        self,
        owners: Sequence[ChecksumAddress],
        threshold: int,
        salt_nonce: int,
        gas_price: int,
        fallback_handler: Optional[ChecksumAddress] = None,
        payment_receiver: Optional[ChecksumAddress] = None,
        payment_token: Optional[ChecksumAddress] = None,
        payment_token_eth_value: float = 1.0,
        fixed_creation_cost: Optional[int] = None,
    ) -> SafeCreate2Tx:
        """
        :param owners: Owners of the Safe
        :param threshold: Minimum number of users required to operate the Safe
        :param fallback_handler: Handler for fallback calls to the Safe
        :param salt_nonce: Web3 instance
        :param gas_price: Gas Price
        :param payment_receiver: Address to refund when the Safe is created. Address(0) if no need to refund
        :param payment_token: Payment token instead of paying the funder with ether. If None Ether will be used
        :param payment_token_eth_value: Value of payment token per 1 Ether
        :param fixed_creation_cost: Fixed creation cost of Safe (Wei)
        :return: SafeCreate2Tx with all the data for execution
        """

        assert 0 < threshold <= len(owners)
        fallback_handler = fallback_handler or NULL_ADDRESS
        payment_receiver = payment_receiver or NULL_ADDRESS
        payment_token = payment_token or NULL_ADDRESS
        assert fast_is_checksum_address(payment_receiver)
        assert fast_is_checksum_address(payment_token)
        owners_list = list(map(str, owners))

        # Get bytes for `setup(address[] calldata _owners, uint256 _threshold, address to, bytes calldata data,
        # address paymentToken, uint256 payment, address payable paymentReceiver)`
        # This initializer will be passed to the ProxyFactory to be called right after proxy is deployed
        # We use `payment=0` as safe has no ether yet and estimation will fail
        safe_setup_data: bytes = self._get_initial_setup_safe_data(
            owners_list,
            threshold,
            fallback_handler=fallback_handler,
            payment_token=payment_token,
            payment_receiver=payment_receiver,
        )

        calculated_gas: int = self._calculate_gas(
            owners_list, safe_setup_data, payment_token
        )
        estimated_gas: int = self._estimate_gas(
            safe_setup_data, salt_nonce, payment_token, payment_receiver
        )
        logger.debug("Magic gas %d - Estimated gas %d", calculated_gas, estimated_gas)
        gas = max(calculated_gas, estimated_gas)

        # Payment will be safe deploy cost
        payment = self._calculate_refund_payment(
            gas, gas_price, fixed_creation_cost, payment_token_eth_value
        )

        # Now we have a estimate for `payment` so we get initialization data again
        final_safe_setup_data: bytes = self._get_initial_setup_safe_data(
            owners_list,
            threshold,
            fallback_handler=fallback_handler,
            payment_token=payment_token,
            payment=payment,
            payment_receiver=payment_receiver,
        )

        safe_address = self.calculate_create2_address(final_safe_setup_data, salt_nonce)
        assert int(
            safe_address, 16
        ), "Calculated Safe address cannot be the NULL ADDRESS"

        return SafeCreate2Tx(
            salt_nonce,
            owners_list,
            threshold,
            fallback_handler,
            self.master_copy_address,
            self.proxy_factory_address,
            payment_receiver,
            payment_token,
            payment,
            gas,
            gas_price,
            payment_token_eth_value,
            fixed_creation_cost,
            safe_address,
            final_safe_setup_data,
        )

    @staticmethod
    def _calculate_gas(
        owners: List[str], safe_setup_data: bytes, payment_token: str
    ) -> int:
        """
        Calculate gas manually, based on tests of previously deployed Safes

        :param owners: Safe owners
        :param safe_setup_data: Data for proxy setup
        :param payment_token: If payment token, we will need more gas to transfer and maybe storage if first time
        :return: total gas needed for deployment
        """
        base_gas = 250_000  # Transaction base gas

        # If we already have the token, we don't have to pay for storage, so it will be just 5K instead of 60K.
        if payment_token != NULL_ADDRESS:
            payment_token_gas = TOKEN_TRANSFER_GAS
        else:
            payment_token_gas = 0

        data_gas = GAS_CALL_DATA_BYTE * len(safe_setup_data)  # Data gas
        gas_per_owner = (
            25_000  # Magic number calculated by testing and averaging owners
        )
        return base_gas + data_gas + payment_token_gas + len(owners) * gas_per_owner

    @staticmethod
    def _calculate_refund_payment(
        gas: int,
        gas_price: int,
        fixed_creation_cost: Optional[int],
        payment_token_eth_value: float,
    ) -> int:
        if fixed_creation_cost is None:
            # Payment will be safe deploy cost + transfer fees for sending ether to the deployer
            base_payment: int = gas * gas_price
            # Calculate payment for tokens using the conversion (if used)
            return math.ceil(base_payment / payment_token_eth_value)
        else:
            return fixed_creation_cost

    def calculate_create2_address(self, safe_setup_data: bytes, salt_nonce: int):
        proxy_creation_code = (
            self.proxy_factory_contract.functions.proxyCreationCode().call()
        )
        salt = self.w3.keccak(
            encode_packed(
                ["bytes", "uint256"], [self.w3.keccak(safe_setup_data), salt_nonce]
            )
        )
        deployment_data = encode_packed(
            ["bytes", "uint256"],
            [proxy_creation_code, int(self.master_copy_address, 16)],
        )
        return mk_contract_address_2(
            self.proxy_factory_contract.address, salt, deployment_data
        )

    def _estimate_gas(
        self,
        initializer: bytes,
        salt_nonce: int,
        payment_token: str,
        payment_receiver: str,
    ) -> int:
        """
        Estimate gas via `eth_estimateGas`.
        Payment cannot be estimated, as ether/tokens don't have to be in the calculated Safe address,
        so we add some gas later.

        :param initializer: Data initializer to send to Safe setup method
        :param salt_nonce: Nonce that will be used to generate the salt to calculate
        the address of the new proxy contract.
        :return: Total gas estimation
        """

        # Estimate the contract deployment. We cannot estimate the refunding, as the safe address has not any funds
        gas: int = self.proxy_factory_contract.functions.createProxyWithNonce(
            self.master_copy_address, initializer, salt_nonce
        ).estimate_gas()

        # We estimate the refund as a new tx
        if payment_token == NULL_ADDRESS:
            # Same cost to send 1 ether than 1000
            gas += self.w3.eth.estimate_gas({"to": payment_receiver, "value": Wei(1)})
        else:
            # Assume the worst scenario with a regular token transfer without storage
            # initialized (payment_receiver no previous owner of token)
            gas += 60_000

        # Add a little more for overhead
        gas += 20_000

        return gas

    def _get_initial_setup_safe_data(
        self,
        owners: List[str],
        threshold: int,
        fallback_handler: str = NULL_ADDRESS,
        payment_token: str = NULL_ADDRESS,
        payment: int = 0,
        payment_receiver: str = NULL_ADDRESS,
    ) -> bytes:
        empty_params: TxParams = get_empty_tx_params()

        if self.safe_version in ("1.5.0", "1.4.1", "1.3.0", "1.1.1"):
            return HexBytes(
                self.master_copy_contract.functions.setup(
                    owners,
                    threshold,
                    NULL_ADDRESS,  # Contract address for optional delegate call
                    b"",  # Data payload for optional delegate call
                    fallback_handler,  # Handler for fallback calls to this contract
                    payment_token,
                    payment,
                    payment_receiver,
                ).build_transaction(empty_params)["data"]
            )
        elif self.safe_version == "1.0.0":
            return HexBytes(
                self.master_copy_contract.functions.setup(
                    owners,
                    threshold,
                    NULL_ADDRESS,  # Contract address for optional delegate call
                    b"",  # Data payload for optional delegate call
                    payment_token,
                    payment,
                    payment_receiver,
                ).build_transaction(empty_params)["data"]
            )
        else:
            raise ValueError("Safe version must be 1.5.0, 1.4.1, 1.3.0, 1.1.1 or 1.0.0")
