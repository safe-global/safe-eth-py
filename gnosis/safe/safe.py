import dataclasses
import math
import os
from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import cached_property
from logging import getLogger
from typing import Callable, Dict, List, Optional, Union

import eth_abi
from eth_abi.exceptions import DecodingError
from eth_abi.packed import encode_packed
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress, Hash32, HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import Web3Exception
from web3.types import BlockIdentifier, TxParams

from gnosis.eth import EthereumClient, EthereumTxSent
from gnosis.eth.constants import GAS_CALL_DATA_BYTE, NULL_ADDRESS, SENTINEL_ADDRESS
from gnosis.eth.contracts import (
    ContractBase,
    get_compatibility_fallback_handler_contract,
    get_safe_contract,
    get_safe_V0_0_1_contract,
    get_safe_V1_0_0_contract,
    get_safe_V1_1_1_contract,
    get_safe_V1_3_0_contract,
    get_safe_V1_4_1_contract,
    get_simulate_tx_accessor_V1_4_1_contract,
)
from gnosis.eth.utils import (
    fast_bytes_to_checksum_address,
    fast_is_checksum_address,
    fast_keccak,
    get_empty_tx_params,
)

from ..eth.typing import EthereumData
from .addresses import SAFE_SIMULATE_TX_ACCESSOR_ADDRESS
from .exceptions import CannotEstimateGas, CannotRetrieveSafeInfoException
from .safe_creator import SafeCreator
from .safe_tx import SafeTx

logger = getLogger(__name__)


class SafeOperation(Enum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2


@dataclasses.dataclass
class SafeInfo:
    address: ChecksumAddress
    fallback_handler: ChecksumAddress
    guard: ChecksumAddress
    master_copy: ChecksumAddress
    modules: List[ChecksumAddress]
    nonce: int
    owners: List[ChecksumAddress]
    threshold: int
    version: str


class Safe(SafeCreator, ContractBase, metaclass=ABCMeta):
    """
    Collection of methods and utilies to handle a Safe
    """

    # keccak256("fallback_manager.handler.address")
    FALLBACK_HANDLER_STORAGE_SLOT = (
        0x6C9A6C4A39284E37ED1CF53D337577D14212A4870FB976A4366C693B939918D5
    )
    # keccak256("guard_manager.guard.address")
    GUARD_STORAGE_SLOT = (
        0x4A204F620C8C5CCDCA3FD54D003BADD85BA500436A431F0CBDA4F558C93C34C8
    )

    # keccak256("SafeMessage(bytes message)");
    SAFE_MESSAGE_TYPEHASH = bytes.fromhex(
        "60b3cbf8b4a223d68d641b3b6ddf9a298e7f33710cf3d3a9d1146b5a6150fbca"
    )

    def __new__(
        cls, address: ChecksumAddress, ethereum_client: EthereumClient, *args, **kwargs
    ) -> "Safe":
        """
        Hacky factory for Safe

        :param address:
        :param ethereum_client:
        :param kwargs:
        """
        assert fast_is_checksum_address(address), "%s is not a valid address" % address
        if cls is not Safe:
            return super().__new__(cls, address, ethereum_client, *args, **kwargs)

        versions: Dict[str, Safe] = {
            "0.0.1": SafeV001,
            "1.0.0": SafeV100,
            "1.1.1": SafeV111,
            "1.2.0": SafeV120,
            "1.3.0": SafeV130,
            "1.4.1": SafeV141,
        }
        default_version = SafeV141

        version: Optional[str]
        try:
            contract = get_safe_contract(ethereum_client.w3, address=address)
            version = contract.functions.VERSION().call(block_identifier="latest")
        except (Web3Exception, ValueError):
            version = None  # Cannot detect the version

        instance_class = versions.get(version, default_version)
        instance = super().__new__(instance_class)
        return instance

    def __init__(
        self,
        address: ChecksumAddress,
        ethereum_client: EthereumClient,
        simulate_tx_accessor_address: Optional[ChecksumAddress] = None,
    ):
        self._simulate_tx_accessor_address = simulate_tx_accessor_address
        super().__init__(address, ethereum_client)

    def __str__(self):
        return f"Safe={self.address}"

    @abstractmethod
    def get_version(self) -> str:
        """
        :return: String with Safe Master Copy semantic version, must match `retrieve_version()`
        """
        raise NotImplementedError

    @cached_property
    def chain_id(self) -> int:
        return self.ethereum_client.get_chain_id()

    @property
    def simulate_tx_accessor_address(self) -> ChecksumAddress:
        if self._simulate_tx_accessor_address:
            return self._simulate_tx_accessor_address
        return os.environ.get(
            "SAFE_SIMULATE_TX_ACCESSOR_ADDRESS", SAFE_SIMULATE_TX_ACCESSOR_ADDRESS
        )

    @simulate_tx_accessor_address.setter
    def simulate_tx_accessor_address(self, value: ChecksumAddress):
        self._simulate_tx_accessor_address = value

    def retrieve_version(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> str:
        return self.contract.functions.VERSION().call(block_identifier=block_identifier)

    @cached_property
    def domain_separator(self) -> Optional[bytes]:
        """
        :return: EIP721 DomainSeparator for the Safe. Returns `None` if not supported (for Safes < 1.0.0)
        """
        try:
            return self.retrieve_domain_separator()
        except (Web3Exception, DecodingError, ValueError):
            logger.warning("Safe %s does not support domainSeparator", self.address)
            return None

    @classmethod
    def deploy_contract(
        cls,
        ethereum_client: EthereumClient,
        deployer_account: LocalAccount,
    ) -> EthereumTxSent:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        Safe with version > v1.1.1 doesn't need to be initialized as it already has a constructor

        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: ``EthereumTxSent`` with the deployed contract address
        """
        contract_fn = cls.get_contract_fn(cls)
        safe_contract = contract_fn(ethereum_client.w3)
        constructor_data = safe_contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]
        ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data
        )
        deployed_version = (
            contract_fn(ethereum_client.w3, ethereum_tx_sent.contract_address)
            .functions.VERSION()
            .call()
        )
        assert deployed_version == cls.get_version(
            cls
        ), f"Deployed version {deployed_version} is not matching expected {cls.get_version(cls)} version"

        logger.info(
            "Deployed and initialized Safe Master Contract version=%s on address %s by %s",
            deployed_version,
            ethereum_tx_sent.contract_address,
            deployer_account.address,
        )
        return ethereum_tx_sent

    def check_funds_for_tx_gas(
        self, safe_tx_gas: int, base_gas: int, gas_price: int, gas_token: str
    ) -> bool:
        """
        Check safe has enough funds to pay for a tx

        :param safe_tx_gas: Safe tx gas
        :param base_gas: Data gas
        :param gas_price: Gas Price
        :param gas_token: Gas Token, to use token instead of ether for the gas
        :return: `True` if enough funds, `False` otherwise
        """
        if gas_token == NULL_ADDRESS:
            balance = self.ethereum_client.get_balance(self.address)
        else:
            balance = self.ethereum_client.erc20.get_balance(self.address, gas_token)
        return balance >= (safe_tx_gas + base_gas) * gas_price

    def estimate_tx_base_gas(
        self,
        to: ChecksumAddress,
        value: int,
        data: bytes,
        operation: int,
        gas_token: ChecksumAddress,
        estimated_tx_gas: int,
    ) -> int:
        """
        Calculate gas costs that are independent of the transaction execution(e.g. base transaction fee,
        signature check, payment of the refund...)

        :param to:
        :param value:
        :param data:
        :param operation:
        :param gas_token:
        :param estimated_tx_gas: gas calculated with `estimate_tx_gas`
        :return:
        """
        data = data or b""
        safe_contract = self.contract
        threshold = self.retrieve_threshold()
        nonce = self.retrieve_nonce()

        # Every byte == 0 -> 4  Gas
        # Every byte != 0 -> 16 Gas (68 before Istanbul)
        # numbers < 256 (0x00(31*2)..ff) are 192 -> 31 * 4 + 1 * GAS_CALL_DATA_BYTE
        # numbers < 65535 (0x(30*2)..ffff) are 256 -> 30 * 4 + 2 * GAS_CALL_DATA_BYTE

        # Calculate gas for signatures
        # (array count (3 -> r, s, v) + ecrecover costs) * signature count
        # ecrecover for ecdsa ~= 4K gas, we use 6K
        ecrecover_gas = 6000
        signature_gas = threshold * (
            1 * GAS_CALL_DATA_BYTE + 2 * 32 * GAS_CALL_DATA_BYTE + ecrecover_gas
        )

        safe_tx_gas = estimated_tx_gas
        base_gas = 0
        gas_price = 1
        gas_token = gas_token or NULL_ADDRESS
        signatures = b""
        refund_receiver = NULL_ADDRESS
        data = HexBytes(
            safe_contract.functions.execTransaction(
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                base_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signatures,
            ).build_transaction(get_empty_tx_params())["data"]
        )

        # If nonce == 0, nonce storage has to be initialized
        if nonce == 0:
            nonce_gas = 20000
        else:
            nonce_gas = 5000

        # Keccak costs for the hash of the safe tx
        hash_generation_gas = 1500

        base_gas = (
            signature_gas
            + self.ethereum_client.estimate_data_gas(data)
            + nonce_gas
            + hash_generation_gas
        )

        # Add additional gas costs
        if base_gas > 65536:
            base_gas += 64
        else:
            base_gas += 128

        base_gas += 32000  # Base tx costs, transfer costs...
        return base_gas

    def estimate_tx_gas_with_safe(
        self,
        to: ChecksumAddress,
        value: int,
        data: bytes,
        operation: int,
        gas_limit: Optional[int] = None,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> int:
        """
        Estimate tx gas using safe `requiredTxGas` method

        :return: int: Estimated gas
        :raises: CannotEstimateGas: If gas cannot be estimated
        :raises: ValueError: Cannot decode received data
        """

        safe_address = self.address
        data = data or b""

        def parse_revert_data(result: bytes) -> int:
            # 4 bytes - error method id
            # 32 bytes - position
            # 32 bytes - length
            # Last 32 bytes - value of revert (if everything went right)
            gas_estimation_offset = 4 + 32 + 32
            gas_estimation = result[gas_estimation_offset:]

            # Estimated gas must be 32 bytes
            if len(gas_estimation) != 32:
                gas_limit_text = (
                    f"with gas limit={gas_limit} "
                    if gas_limit is not None
                    else "without gas limit set "
                )
                logger.warning(
                    "Safe=%s Problem estimating gas, returned value %sis %s for tx=%s",
                    safe_address,
                    gas_limit_text,
                    result.hex(),
                    tx,
                )
                raise CannotEstimateGas("Received %s for tx=%s" % (result.hex(), tx))

            return int(gas_estimation.hex(), 16)

        tx = self.contract.functions.requiredTxGas(
            to, value, data, operation
        ).build_transaction(
            {
                "from": safe_address,
                "gas": 0,  # Don't call estimate
                "gasPrice": 0,  # Don't get gas price
            }
        )

        tx_params = {
            "from": safe_address,
            "to": safe_address,
            "data": tx["data"],
        }

        if gas_limit:
            tx_params["gas"] = hex(gas_limit)

        query = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [tx_params, block_identifier],
            "id": 1,
        }

        response = self.ethereum_client.http_session.post(
            self.ethereum_client.ethereum_node_url, json=query, timeout=30
        )
        if response.ok:
            response_data = response.json()
            error_data: Optional[str] = None
            if "error" in response_data and "data" in response_data["error"]:
                error_data = response_data["error"]["data"]
            elif "result" in response_data:  # Ganache-cli
                error_data = response_data["result"]

            if error_data:
                if "0x" in error_data:
                    return parse_revert_data(
                        HexBytes(error_data[error_data.find("0x") :])
                    )

        raise CannotEstimateGas(
            f"Received {response.status_code} - {response.content} from ethereum node"
        )

    def estimate_tx_gas_with_web3(
        self, to: ChecksumAddress, value: int, data: EthereumData
    ) -> int:
        """
        :param to:
        :param value:
        :param data:
        :return: Estimation using web3 `estimate_gas`
        """
        try:
            return self.ethereum_client.estimate_gas(
                to, from_=self.address, value=value, data=data
            )
        except (Web3Exception, ValueError) as exc:
            raise CannotEstimateGas(
                f"Cannot estimate gas with `eth_estimateGas`: {exc}"
            ) from exc

    def estimate_tx_gas_by_trying(
        self, to: ChecksumAddress, value: int, data: Union[bytes, str], operation: int
    ):
        """
        Try to get an estimation with Safe's `requiredTxGas`. If estimation is successful, try to set a gas limit and
        estimate again. If gas estimation is ok, same gas estimation should be returned, if it's less than required
        estimation will not be completed, so estimation was not accurate and gas limit needs to be increased.

        :param to:
        :param value:
        :param data:
        :param operation:
        :return: Estimated gas calling `requiredTxGas` setting a gas limit and checking if `eth_call` is successful
        :raises: CannotEstimateGas
        """
        if not data:
            data = b""
        elif isinstance(data, str):
            data = HexBytes(data)

        gas_estimated = self.estimate_tx_gas_with_safe(to, value, data, operation)
        block_gas_limit: Optional[int] = None
        base_gas: Optional[int] = self.ethereum_client.estimate_data_gas(data)

        for i in range(
            1, 30
        ):  # Make sure tx can be executed, fixing for example 63/64th problem
            try:
                self.estimate_tx_gas_with_safe(
                    to,
                    value,
                    data,
                    operation,
                    gas_limit=gas_estimated + base_gas + 32000,
                )
                return gas_estimated
            except CannotEstimateGas:
                logger.warning(
                    "Safe=%s - Found 63/64 problem gas-estimated=%d to=%s data=%s",
                    self.address,
                    gas_estimated,
                    to,
                    data.hex(),
                )
                block_gas_limit = (
                    block_gas_limit
                    or self.w3.eth.get_block("latest", full_transactions=False)[
                        "gasLimit"
                    ]
                )
                gas_estimated = math.floor((1 + i * 0.03) * gas_estimated)
                if gas_estimated >= block_gas_limit:
                    return block_gas_limit
        return gas_estimated

    def estimate_tx_gas(
        self, to: ChecksumAddress, value: int, data: bytes, operation: int
    ) -> int:
        """
        Estimate tx gas. Use `requiredTxGas` on the Safe contract and fallbacks to `eth_estimateGas` if that method
        fails. Note: `eth_estimateGas` cannot estimate delegate calls

        :param to:
        :param value:
        :param data:
        :param operation:
        :return: Estimated gas for Safe inner tx
        :raises: CannotEstimateGas
        """
        # Costs to route through the proxy and nested calls
        PROXY_GAS = 1000
        # https://github.com/ethereum/solidity/blob/dfe3193c7382c80f1814247a162663a97c3f5e67/libsolidity/codegen/ExpressionCompiler.cpp#L1764
        # This was `false` before solc 0.4.21 -> `m_context.evmVersion().canOverchargeGasForCall()`
        # So gas needed by caller will be around 35k
        OLD_CALL_GAS = 35000
        # Web3 `estimate_gas` estimates less gas
        WEB3_ESTIMATION_OFFSET = 23000
        ADDITIONAL_GAS = PROXY_GAS + OLD_CALL_GAS

        try:
            return (
                self.estimate_tx_gas_by_trying(to, value, data, operation)
                + ADDITIONAL_GAS
            )
        except CannotEstimateGas:
            return (
                self.estimate_tx_gas_with_web3(to, value, data)
                + ADDITIONAL_GAS
                + WEB3_ESTIMATION_OFFSET
            )

    def get_message_hash(self, message: Union[str, Hash32]) -> Hash32:
        """
        Return hash of a message that can be signed by owners.

        :param message: Message that should be hashed. A ``Hash32`` must be provided for EIP191 or EIP712 messages
        :return: Message hash
        """

        if isinstance(message, str):
            message = message.encode()
        message_hash = fast_keccak(message)

        safe_message_hash = Web3.keccak(
            eth_abi.encode(
                ["bytes32", "bytes32"], [self.SAFE_MESSAGE_TYPEHASH, message_hash]
            )
        )
        return Web3.keccak(
            encode_packed(
                ["bytes1", "bytes1", "bytes32", "bytes32"],
                [
                    bytes.fromhex("19"),
                    bytes.fromhex("01"),
                    self.domain_separator,
                    safe_message_hash,
                ],
            )
        )

    def retrieve_all_info(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> SafeInfo:
        """
        Get all Safe info in the same batch call.

        :param block_identifier:
        :return:
        :raises: CannotRetrieveSafeInfoException
        """

        # FIXME for not initialized Safes `getModules` get into an infinite loop on the RPC
        try:
            contract = self.contract
            master_copy = self.retrieve_master_copy_address()
            if master_copy == NULL_ADDRESS:
                raise CannotRetrieveSafeInfoException(self.address)

            fallback_handler = self.retrieve_fallback_handler()
            guard = self.retrieve_guard()  # Guard was implemented in v1.1.1

            # From v1.1.1:
            # - `getModulesPaginated` is available
            # - `getModules` returns only 10 modules
            modules_fn = (
                contract.functions.getModulesPaginated(SENTINEL_ADDRESS, 20)
                if hasattr(contract.functions, "getModulesPaginated")
                else contract.functions.getModules()
            )

            results = self.ethereum_client.batch_call(
                [
                    modules_fn,
                    contract.functions.nonce(),
                    contract.functions.getOwners(),
                    contract.functions.getThreshold(),
                    contract.functions.VERSION(),
                ],
                from_address=self.address,
                block_identifier=block_identifier,
                raise_exception=False,
            )
            modules_response, nonce, owners, threshold, version = results
            if (
                modules_response
                and len(modules_response) == 2
                and isinstance(modules_response[0], (tuple, list))
            ):
                # Must be a Tuple[List[ChecksumAddress], ChecksumAddress]
                # >= v1.1.1
                modules, next_module = modules_response
                if modules and next_module != SENTINEL_ADDRESS:
                    # Still more elements in the list
                    modules = self.retrieve_modules()
            else:
                # < v1.1.1
                modules = modules_response

            return SafeInfo(
                self.address,
                fallback_handler,
                guard,
                master_copy,
                modules if modules else [],
                nonce,
                owners,
                threshold,
                version,
            )
        except (Web3Exception, ValueError) as e:
            raise CannotRetrieveSafeInfoException(self.address) from e

    def retrieve_domain_separator(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> str:
        return self.contract.functions.domainSeparator().call(
            block_identifier=block_identifier
        )

    def retrieve_code(self) -> HexBytes:
        return self.w3.eth.get_code(self.address)

    def retrieve_fallback_handler(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        address = self.ethereum_client.w3.eth.get_storage_at(
            self.address,
            self.FALLBACK_HANDLER_STORAGE_SLOT,
            block_identifier=block_identifier,
        )[-20:].rjust(20, b"\0")
        if len(address) == 20:
            return fast_bytes_to_checksum_address(address)
        else:
            return NULL_ADDRESS

    def retrieve_guard(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        address = self.ethereum_client.w3.eth.get_storage_at(
            self.address, self.GUARD_STORAGE_SLOT, block_identifier=block_identifier
        )[-20:].rjust(20, b"\0")
        if len(address) == 20:
            return fast_bytes_to_checksum_address(address)
        else:
            return NULL_ADDRESS

    def retrieve_master_copy_address(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        address = self.w3.eth.get_storage_at(
            self.address, "0x00", block_identifier=block_identifier
        )[-20:].rjust(20, b"\0")
        return fast_bytes_to_checksum_address(address)

    def retrieve_modules(
        self,
        pagination: Optional[int] = 50,
        max_modules_to_retrieve: Optional[int] = 500,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[ChecksumAddress]:
        """
        Get modules enabled on the Safe
        From v1.1.1:
          - ``getModulesPaginated`` is available
          - ``getModules`` returns only 10 modules

        :param pagination: Number of modules to get per request
        :param max_modules_to_retrieve: Maximum number of modules to retrieve
        :param block_identifier:
        :return: List of module addresses
        """
        if not hasattr(self.contract.functions, "getModulesPaginated"):
            # Custom code for Safes < v1.3.0
            # Safe V1_0_0 can get into an infinite loop if it's not initialized
            if self.retrieve_threshold() == 0:
                return []
            return self.contract.functions.getModules().call(
                block_identifier=block_identifier
            )

        # We need to iterate the module paginator
        contract = self.contract
        next_module = SENTINEL_ADDRESS
        all_modules: List[ChecksumAddress] = []

        for _ in range(max_modules_to_retrieve // pagination):
            # If we use a `while True` loop a custom coded Safe could get us into an infinite loop
            (modules, next_module) = contract.functions.getModulesPaginated(
                next_module, pagination
            ).call(block_identifier=block_identifier)

            # Safes with version < 1.4.0 don't include the `starter address` used as pagination in the module list
            # From 1.4.0 onwards it is included, so we check for duplicated addresses before inserting
            for module in modules + [next_module]:
                if module not in all_modules + [NULL_ADDRESS, SENTINEL_ADDRESS]:
                    all_modules.append(module)

            if not modules or next_module in (NULL_ADDRESS, SENTINEL_ADDRESS):
                # `NULL_ADDRESS` is only seen in uninitialized Safes
                break
        return all_modules

    def retrieve_is_hash_approved(
        self,
        owner: str,
        safe_hash: bytes,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> bool:
        return (
            self.contract.functions.approvedHashes(owner, safe_hash).call(
                block_identifier=block_identifier
            )
            == 1
        )

    def retrieve_is_message_signed(
        self,
        message_hash: Hash32,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> bool:
        return self.contract.functions.signedMessages(message_hash).call(
            block_identifier=block_identifier
        )

    def retrieve_is_owner(
        self, owner: str, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> bool:
        return self.contract.functions.isOwner(owner).call(
            block_identifier=block_identifier
        )

    def retrieve_nonce(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> int:
        return self.contract.functions.nonce().call(block_identifier=block_identifier)

    def retrieve_owners(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> List[str]:
        return self.contract.functions.getOwners().call(
            block_identifier=block_identifier
        )

    def retrieve_threshold(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> int:
        return self.contract.functions.getThreshold().call(
            block_identifier=block_identifier
        )

    def build_multisig_tx(
        self,
        to: ChecksumAddress,
        value: int,
        data: bytes,
        operation: int = SafeOperation.CALL.value,
        safe_tx_gas: int = 0,
        base_gas: int = 0,
        gas_price: int = 0,
        gas_token: ChecksumAddress = NULL_ADDRESS,
        refund_receiver: ChecksumAddress = NULL_ADDRESS,
        signatures: bytes = b"",
        safe_nonce: Optional[int] = None,
    ) -> SafeTx:
        """
        Allows to execute a Safe transaction confirmed by required number of owners and then pays the account
        that submitted the transaction. The fees are always transfered, even if the user transaction fails

        :param to: Destination address of Safe transaction
        :param value: Ether value of Safe transaction
        :param data: Data payload of Safe transaction
        :param operation: Operation type of Safe transaction
        :param safe_tx_gas: Gas that should be used for the Safe transaction
        :param base_gas: Gas costs for that are independent of the transaction execution
            (e.g. base transaction fee, signature check, payment of the refund)
        :param gas_price: Gas price that should be used for the payment calculation
        :param gas_token: Token address (or `0x000..000` if ETH) that is used for the payment
        :param refund_receiver: Address of receiver of gas payment (or `0x000..000` if tx.origin).
        :param signatures: Packed signature data ({bytes32 r}{bytes32 s}{uint8 v})
        :param safe_nonce: Nonce of the safe (to calculate hash)
        :param safe_version: Safe version (to calculate hash)
        :return: SafeTx
        """

        if safe_nonce is None:
            safe_nonce = self.retrieve_nonce()
        return SafeTx(
            self.ethereum_client,
            self.address,
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures=signatures,
            safe_nonce=safe_nonce,
            safe_version=self.get_version(),
            chain_id=self.chain_id,
        )

    def send_multisig_tx(
        self,
        to: ChecksumAddress,
        value: int,
        data: bytes,
        operation: int,
        safe_tx_gas: int,
        base_gas: int,
        gas_price: int,
        gas_token: ChecksumAddress,
        refund_receiver: ChecksumAddress,
        signatures: bytes,
        tx_sender_private_key: HexStr,
        tx_gas=None,
        tx_gas_price=None,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> EthereumTxSent:
        """
        Build and send Safe tx

        :param to:
        :param value:
        :param data:
        :param operation:
        :param safe_tx_gas:
        :param base_gas:
        :param gas_price:
        :param gas_token:
        :param refund_receiver:
        :param signatures:
        :param tx_sender_private_key:
        :param tx_gas: Gas for the external tx. If not, `(safe_tx_gas + data_gas) * 2` will be used
        :param tx_gas_price: Gas price of the external tx. If not, `gas_price` will be used
        :param block_identifier:
        :return: Tuple(tx_hash, tx)
        :raises: InvalidMultisigTx: If user tx cannot go through the Safe
        """

        safe_tx = self.build_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
        )

        tx_sender_address = Account.from_key(tx_sender_private_key).address
        safe_tx.call(
            tx_sender_address=tx_sender_address, block_identifier=block_identifier
        )

        tx_hash, tx = safe_tx.execute(
            tx_sender_private_key=tx_sender_private_key,
            tx_gas=tx_gas,
            tx_gas_price=tx_gas_price,
            block_identifier=block_identifier,
        )

        return EthereumTxSent(tx_hash, tx, None)


class SafeV001(Safe):
    def get_version(self):
        return "0.0.1"

    def get_contract_fn(self) -> Callable[[Web3, ChecksumAddress], Contract]:
        return get_safe_V0_0_1_contract

    @staticmethod
    def deploy_contract(
        ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key

        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: ``EthereumTxSent`` with the deployed contract address
        """

        safe_contract = get_safe_V0_0_1_contract(ethereum_client.w3)
        constructor_data = safe_contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]
        initializer_data = safe_contract.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            [
                "0x0000000000000000000000000000000000000002",
                "0x0000000000000000000000000000000000000003",
            ],
            2,  # Threshold. Maximum security
            NULL_ADDRESS,  # Address for optional DELEGATE CALL
            b"",  # Data for optional DELEGATE CALL
        ).build_transaction({"to": NULL_ADDRESS, "gas": 0, "gasPrice": 0})["data"]

        ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data, HexBytes(initializer_data)
        )
        logger.info(
            "Deployed and initialized Old Safe Master Contract=%s by %s",
            ethereum_tx_sent.contract_address,
            deployer_account.address,
        )
        return ethereum_tx_sent


class SafeV100(Safe):
    def get_version(self):
        return "1.0.0"

    def get_contract_fn(self) -> Contract:
        return get_safe_V1_0_0_contract

    @staticmethod
    def deploy_contract(
        ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key

        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: ``EthereumTxSent`` with the deployed contract address
        """

        safe_contract = get_safe_V1_0_0_contract(ethereum_client.w3)
        constructor_data = safe_contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]
        initializer_data = safe_contract.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            [
                "0x0000000000000000000000000000000000000002",
                "0x0000000000000000000000000000000000000003",
            ],
            2,  # Threshold. Maximum security
            NULL_ADDRESS,  # Address for optional DELEGATE CALL
            b"",  # Data for optional DELEGATE CALL
            NULL_ADDRESS,  # Payment token
            0,  # Payment
            NULL_ADDRESS,  # Refund receiver
        ).build_transaction({"to": NULL_ADDRESS, "gas": 0, "gasPrice": 0})["data"]

        ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data, HexBytes(initializer_data)
        )
        logger.info(
            "Deployed and initialized Safe Master Contract=%s by %s",
            ethereum_tx_sent.contract_address,
            deployer_account.address,
        )
        return ethereum_tx_sent


class SafeV111(Safe):
    def get_version(self):
        return "1.1.1"

    def get_contract_fn(self) -> Contract:
        return get_safe_V1_1_1_contract


class SafeV120(Safe):
    def get_version(self):
        return "1.2.0"

    def get_contract_fn(self) -> Contract:
        return get_safe_V1_1_1_contract


class SafeV130(Safe):
    def get_version(self):
        return "1.3.0"

    def get_contract_fn(self) -> Contract:
        return get_safe_V1_3_0_contract


class SafeV141(Safe):
    def get_version(self):
        return "1.4.1"

    def get_contract_fn(self) -> Contract:
        return get_safe_V1_4_1_contract

    def estimate_tx_gas_with_safe(
        self,
        to: ChecksumAddress,
        value: int,
        data: bytes,
        operation: int,
        gas_limit: Optional[int] = None,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> int:
        """
        Estimate tx gas. Use `SimulateTxAccesor` and `simulate` on the `CompatibilityFallHandler`

        :param to:
        :param value:
        :param data:
        :param operation:
        :param gas_limit:
        :param block_identifier:
        :return:
        """
        accessor = get_simulate_tx_accessor_V1_4_1_contract(
            self.w3, address=self.simulate_tx_accessor_address
        )
        simulator = get_compatibility_fallback_handler_contract(
            self.w3, address=self.address
        )
        simulation_data = accessor.functions.simulate(
            to, value, data, operation
        ).build_transaction(get_empty_tx_params())["data"]
        params: TxParams = {"gas": gas_limit} if gas_limit else {}
        # params = {'gas': 2_045_741}
        try:
            accessible_data = simulator.functions.simulate(
                accessor.address, simulation_data
            ).call(params)
        except ValueError as e:
            raise CannotEstimateGas(f"Reverted call using SimulateTxAccessor {e}")
        try:
            # Simulate returns (uint256 estimate, bool success, bytes memory returnData)
            (estimate, success, return_data) = eth_abi.decode(
                ["uint256", "bool", "bytes"], accessible_data
            )
            if not success:
                raise CannotEstimateGas(
                    "Cannot estimate gas using SimulateTxAccessor - Execution not successful"
                )
            return estimate
        except DecodingError as e:
            try:
                decoded_revert = eth_abi.decode(["string"], accessible_data)
            except DecodingError:
                decoded_revert = "No revert message"
            raise CannotEstimateGas(
                f"Cannot estimate gas using SimulateTxAccessor {e} - {decoded_revert}"
            )
