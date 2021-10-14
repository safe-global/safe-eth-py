import math
import os
from logging import getLogger
from typing import Any, Dict, List, Optional, Tuple

import rlp
from ethereum.exceptions import InvalidTransaction
from ethereum.transactions import Transaction, secpk1n
from ethereum.utils import checksum_encode, mk_contract_address
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import ContractConstructor

from gnosis.eth.constants import GAS_CALL_DATA_BYTE, NULL_ADDRESS
from gnosis.eth.contracts import (
    get_erc20_contract,
    get_paying_proxy_contract,
    get_safe_V0_0_1_contract,
)

logger = getLogger(__name__)


class InvalidERC20Token(Exception):
    pass


class SafeCreationTx:
    def __init__(
        self,
        w3: Web3,
        owners: List[str],
        threshold: int,
        signature_s: int,
        master_copy: str,
        gas_price: int,
        funder: Optional[str],
        payment_token: Optional[str] = None,
        payment_token_eth_value: float = 1.0,
        fixed_creation_cost: Optional[int] = None,
    ):
        """
        Prepare Safe creation
        :param w3: Web3 instance
        :param owners: Owners of the Safe
        :param threshold: Minimum number of users required to operate the Safe
        :param signature_s: Random s value for ecdsa signature
        :param master_copy: Safe master copy address
        :param gas_price: Gas Price
        :param funder: Address to refund when the Safe is created. Address(0) if no need to refund
        :param payment_token: Payment token instead of paying the funder with ether. If None Ether will be used
        :param payment_token_eth_value: Value of payment token per 1 Ether
        :param fixed_creation_cost: Fixed creation cost of Safe (Wei)
        """

        assert 0 < threshold <= len(owners)
        funder = funder or NULL_ADDRESS
        payment_token = payment_token or NULL_ADDRESS
        assert Web3.isChecksumAddress(master_copy)
        assert Web3.isChecksumAddress(funder)
        assert Web3.isChecksumAddress(payment_token)

        self.w3 = w3
        self.owners = owners
        self.threshold = threshold
        self.s = signature_s
        self.master_copy = master_copy
        self.gas_price = gas_price
        self.funder = funder
        self.payment_token = payment_token
        self.payment_token_eth_value = payment_token_eth_value
        self.fixed_creation_cost = fixed_creation_cost

        # Get bytes for `setup(address[] calldata _owners, uint256 _threshold, address to, bytes calldata data)`
        # This initializer will be passed to the proxy and will be called right after proxy is deployed
        safe_setup_data: bytes = self._get_initial_setup_safe_data(owners, threshold)

        # Calculate gas based on experience of previous deployments of the safe
        calculated_gas: int = self._calculate_gas(
            owners, safe_setup_data, payment_token
        )
        # Estimate gas using web3
        estimated_gas: int = self._estimate_gas(
            master_copy, safe_setup_data, funder, payment_token
        )
        self.gas = max(calculated_gas, estimated_gas)

        # Payment will be safe deploy cost + transfer fees for sending ether to the deployer
        self.payment = self._calculate_refund_payment(
            self.gas, gas_price, fixed_creation_cost, payment_token_eth_value
        )

        self.tx_dict: Dict[str, Any] = self._build_proxy_contract_creation_tx(
            master_copy=master_copy,
            initializer=safe_setup_data,
            funder=funder,
            payment_token=payment_token,
            payment=self.payment,
            gas=self.gas,
            gas_price=gas_price,
        )

        self.tx_pyethereum: Transaction = (
            self._build_contract_creation_tx_with_valid_signature(self.tx_dict, self.s)
        )
        self.tx_raw = rlp.encode(self.tx_pyethereum)
        self.tx_hash = self.tx_pyethereum.hash
        self.deployer_address = checksum_encode(self.tx_pyethereum.sender)
        self.safe_address = checksum_encode(self.tx_pyethereum.creates)

        self.v = self.tx_pyethereum.v
        self.r = self.tx_pyethereum.r
        self.safe_setup_data = safe_setup_data

        assert (
            checksum_encode(mk_contract_address(self.deployer_address, nonce=0))
            == self.safe_address
        )

    @property
    def payment_ether(self):
        return self.gas * self.gas_price

    @staticmethod
    def find_valid_random_signature(s: int) -> Tuple[int, int]:
        """
        Find v and r valid values for a given s
        :param s: random value
        :return: v, r
        """
        for _ in range(10000):
            r = int(os.urandom(31).hex(), 16)
            v = (r % 2) + 27
            if r < secpk1n:
                tx = Transaction(0, 1, 21000, b"", 0, b"", v=v, r=r, s=s)
                try:
                    tx.sender
                    return v, r
                except (InvalidTransaction, ValueError):
                    logger.debug("Cannot find signature with v=%d r=%d s=%d", v, r, s)

        raise ValueError("Valid signature not found with s=%d", s)

    @staticmethod
    def _calculate_gas(
        owners: List[str], safe_setup_data: bytes, payment_token: str
    ) -> int:
        """
        Calculate gas manually, based on tests of previosly deployed safes
        :param owners: Safe owners
        :param safe_setup_data: Data for proxy setup
        :param payment_token: If payment token, we will need more gas to transfer and maybe storage if first time
        :return: total gas needed for deployment
        """
        # TODO Do gas calculation estimating the call instead this magic

        base_gas = 60580  # Transaction standard gas

        # If we already have the token, we don't have to pay for storage, so it will be just 5K instead of 20K.
        # The other 1K is for overhead of making the call
        if payment_token != NULL_ADDRESS:
            payment_token_gas = 55000
        else:
            payment_token_gas = 0

        data_gas = GAS_CALL_DATA_BYTE * len(safe_setup_data)  # Data gas
        gas_per_owner = 18020  # Magic number calculated by testing and averaging owners
        return (
            base_gas
            + data_gas
            + payment_token_gas
            + 270000
            + len(owners) * gas_per_owner
        )

    @staticmethod
    def _calculate_refund_payment(
        gas: int,
        gas_price: int,
        fixed_creation_cost: Optional[int],
        payment_token_eth_value: float,
    ) -> int:
        if fixed_creation_cost is None:
            # Payment will be safe deploy cost + transfer fees for sending ether to the deployer
            base_payment: int = (gas + 23000) * gas_price
            # Calculate payment for tokens using the conversion (if used)
            return math.ceil(base_payment / payment_token_eth_value)
        else:
            return fixed_creation_cost

    def _build_proxy_contract_creation_constructor(
        self,
        master_copy: str,
        initializer: bytes,
        funder: str,
        payment_token: str,
        payment: int,
    ) -> ContractConstructor:
        """
        :param master_copy: Master Copy of Gnosis Safe already deployed
        :param initializer: Data initializer to send to GnosisSafe setup method
        :param funder: Address that should get the payment (if payment set)
        :param payment_token: Address if a token is used. If not set, 0x0 will be ether
        :param payment: Payment
        :return: Transaction dictionary
        """
        if not funder or funder == NULL_ADDRESS:
            funder = NULL_ADDRESS
            payment = 0

        return get_paying_proxy_contract(self.w3).constructor(
            master_copy, initializer, funder, payment_token, payment
        )

    def _build_proxy_contract_creation_tx(
        self,
        master_copy: str,
        initializer: bytes,
        funder: str,
        payment_token: str,
        payment: int,
        gas: int,
        gas_price: int,
        nonce: int = 0,
    ):
        """
        :param master_copy: Master Copy of Gnosis Safe already deployed
        :param initializer: Data initializer to send to GnosisSafe setup method
        :param funder: Address that should get the payment (if payment set)
        :param payment_token: Address if a token is used. If not set, 0x0 will be ether
        :param payment: Payment
        :return: Transaction dictionary
        """
        return self._build_proxy_contract_creation_constructor(
            master_copy, initializer, funder, payment_token, payment
        ).buildTransaction(
            {
                "gas": gas,
                "gasPrice": gas_price,
                "nonce": nonce,
            }
        )

    def _build_contract_creation_tx_with_valid_signature(
        self, tx_dict: Dict[str, Any], s: int
    ) -> Transaction:
        """
        Use pyethereum `Transaction` to generate valid tx using a random signature
        :param tx_dict: Web3 tx dictionary
        :param s: Signature s value
        :return: PyEthereum creation tx for the proxy contract
        """
        zero_address = HexBytes("0x" + "0" * 40)
        f_address = HexBytes("0x" + "f" * 40)
        nonce = tx_dict["nonce"]
        gas_price = tx_dict["gasPrice"]
        gas = tx_dict["gas"]
        to = tx_dict.get("to", b"")  # Contract creation should always have `to` empty
        value = tx_dict["value"]
        data = tx_dict["data"]
        for _ in range(100):
            try:
                v, r = self.find_valid_random_signature(s)
                contract_creation_tx = Transaction(
                    nonce, gas_price, gas, to, value, HexBytes(data), v=v, r=r, s=s
                )
                sender_address = contract_creation_tx.sender
                contract_address = contract_creation_tx.creates
                if sender_address in (zero_address, f_address) or contract_address in (
                    zero_address,
                    f_address,
                ):
                    raise InvalidTransaction
                return contract_creation_tx
            except InvalidTransaction:
                pass
        raise ValueError("Valid signature not found with s=%d", s)

    def _estimate_gas(
        self, master_copy: str, initializer: bytes, funder: str, payment_token: str
    ) -> int:
        """
        Gas estimation done using web3 and calling the node
        Payment cannot be estimated, as no ether is in the address. So we add some gas later.
        :param master_copy: Master Copy of Gnosis Safe already deployed
        :param initializer: Data initializer to send to GnosisSafe setup method
        :param funder: Address that should get the payment (if payment set)
        :param payment_token: Address if a token is used. If not set, 0x0 will be ether
        :return: Total gas estimation
        """

        # Estimate the contract deployment. We cannot estimate the refunding, as the safe address has not any fund
        gas: int = self._build_proxy_contract_creation_constructor(
            master_copy, initializer, funder, payment_token, 0
        ).estimateGas()

        # We estimate the refund as a new tx
        if payment_token == NULL_ADDRESS:
            # Same cost to send 1 ether than 1000
            gas += self.w3.eth.estimate_gas({"to": funder, "value": 1})
        else:
            # Top should be around 52000 when storage is needed (funder no previous owner of token),
            # we use value 1 as we are simulating an internal call, and in that calls you don't pay for the data.
            # If it was a new tx sending 5000 tokens would be more expensive than sending 1 because of data costs
            try:
                gas += (
                    get_erc20_contract(self.w3, payment_token)
                    .functions.transfer(funder, 1)
                    .estimateGas({"from": payment_token})
                )
            except ValueError as exc:
                if "transfer amount exceeds balance" in str(exc):
                    return 70000
                raise InvalidERC20Token from exc

        return gas

    def _get_initial_setup_safe_data(self, owners: List[str], threshold: int) -> bytes:
        return (
            get_safe_V0_0_1_contract(self.w3, self.master_copy)
            .functions.setup(
                owners,
                threshold,
                NULL_ADDRESS,  # Contract address for optional delegate call
                b"",  # Data payload for optional delegate call
            )
            .buildTransaction(
                {
                    "gas": 1,
                    "gasPrice": 1,
                }
            )["data"]
        )
