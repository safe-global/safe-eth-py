import dataclasses
import datetime
import logging
from functools import cache, cached_property
from typing import Optional
from zoneinfo import ZoneInfo

from eth_abi import encode as abi_encode
from eth_abi.packed import encode_packed
from eth_typing import ChecksumAddress
from hexbytes import HexBytes

from gnosis.eth.account_abstraction import UserOperation
from gnosis.eth.utils import fast_keccak

logger = logging.getLogger(__name__)

_domain_separator_cache = {}


@dataclasses.dataclass(eq=True, frozen=True)
class SafeOperation:
    """
    Safe EIP4337 operation
    More info: https://github.com/safe-global/safe-modules/blob/main/modules/4337/contracts/Safe4337Module.sol#L55

    TypeHash calculation:

    .. code-block:: python

        keccak256(
            "SafeOp(address safe,uint256 nonce,bytes initCode,bytes callData,uint256 callGasLimit,uint256 verificationGasLimit,uint256 preVerificationGas,uint256 maxFeePerGas,uint256 maxPriorityFeePerGas,bytes paymasterAndData,uint48 validAfter,uint48 validUntil,address entryPoint)"
        )

    Domain separator calculation:

    .. code-block:: python
        keccak256("EIP712Domain(uint256 chainId,address verifyingContract)"

    """

    safe: ChecksumAddress
    nonce: int  # uint256
    init_code_hash: bytes  # bytes32
    call_data_hash: bytes  # bytes32
    call_gas_limit: int  # uint256
    verification_gas_limit: int  # uint256
    pre_verification_gas: int  # uint256
    max_fee_per_gas: int  # uint256
    max_priority_fee_per_gas: int  # uint256
    paymaster_and_data_hash: bytes  # bytes32
    valid_after: int  # uint48
    valid_until: int  # uint48
    entry_point: ChecksumAddress
    signature: bytes
    TYPE_HASH: bytes = HexBytes(
        "0x84aa190356f56b8c87825f54884392a9907c23ee0f8e1ea86336b763faf021bd"
    )  # bytes32
    DOMAIN_SEPARATOR_TYPE_HASH: bytes = HexBytes(
        "0x47e79534a245952e8b16893a336b85a3d9ea9fa8c573f3d803afb92a79469218"
    )  # bytes32
    safe_operation_hash: Optional[bytes] = None

    @classmethod
    def from_user_operation(cls, user_operation: UserOperation):
        return cls(
            user_operation.sender,
            user_operation.nonce,
            fast_keccak(user_operation.init_code),
            fast_keccak(user_operation.call_data),
            user_operation.call_gas_limit,
            user_operation.verification_gas_limit,
            user_operation.pre_verification_gas,
            user_operation.max_fee_per_gas,
            user_operation.max_priority_fee_per_gas,
            fast_keccak(user_operation.paymaster_and_data),
            int.from_bytes(user_operation.signature[:6], byteorder="big"),
            int.from_bytes(user_operation.signature[6:12], byteorder="big"),
            user_operation.entry_point,
            user_operation.signature[12:],
        )

    @staticmethod
    def _parse_epoch(epoch: int) -> Optional[datetime.datetime]:
        if not epoch:
            return None

        try:
            return datetime.datetime.fromtimestamp(epoch, ZoneInfo("UTC"))
        except (OverflowError, ValueError) as exc:
            logger.warning("Invalid epoch %d: %s", epoch, exc)
            return None

    @cached_property
    def valid_after_as_datetime(self) -> Optional[datetime.datetime]:
        return self._parse_epoch(self.valid_after)

    @cached_property
    def valid_until_as_datetime(self) -> Optional[datetime.datetime]:
        return self._parse_epoch(self.valid_until)

    @cached_property
    def safe_operation_hash_preimage(self) -> bytes:
        encoded_safe_op_struct = abi_encode(
            [
                "bytes32",
                "address",
                "uint256",
                "bytes32",
                "bytes32",
                "uint256",
                "uint256",
                "uint256",
                "uint256",
                "uint256",
                "bytes32",
                "uint48",
                "uint48",
                "address",
            ],
            [
                self.TYPE_HASH,
                self.safe,
                self.nonce,
                self.init_code_hash,
                self.call_data_hash,
                self.call_gas_limit,
                self.verification_gas_limit,
                self.pre_verification_gas,
                self.max_fee_per_gas,
                self.max_priority_fee_per_gas,
                self.paymaster_and_data_hash,
                self.valid_after,
                self.valid_until,
                self.entry_point,
            ],
        )
        return fast_keccak(encoded_safe_op_struct)

    def get_domain_separator(
        self, chain_id: int, module_address: ChecksumAddress
    ) -> bytes:
        key = (chain_id, module_address)
        if key not in _domain_separator_cache:
            _domain_separator_cache[key] = fast_keccak(
                abi_encode(
                    ["bytes32", "uint256", "address"],
                    [self.DOMAIN_SEPARATOR_TYPE_HASH, chain_id, module_address],
                )
            )
        return _domain_separator_cache[key]

    @cache
    def get_safe_operation_hash(
        self, chain_id: int, module_address: ChecksumAddress
    ) -> bytes:
        safe_op_struct_hash = self.safe_operation_hash_preimage
        operation_data = encode_packed(
            ["bytes1", "bytes1", "bytes32", "bytes32"],
            [
                bytes.fromhex("19"),
                bytes.fromhex("01"),
                self.get_domain_separator(chain_id, module_address),
                safe_op_struct_hash,
            ],
        )
        return fast_keccak(operation_data)
