import dataclasses
from functools import cached_property
from typing import Any, Dict, Optional, Union

from eth_abi import encode as abi_encode
from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes

from gnosis.eth.utils import fast_keccak, fast_to_checksum_address


@dataclasses.dataclass(eq=True, frozen=True)
class UserOperationMetadata:
    transaction_hash: bytes
    block_hash: bytes
    block_number: int


@dataclasses.dataclass(eq=True, frozen=True)
class UserOperation:
    """
    EIP4337 UserOperation for Entrypoint v0.6

    https://github.com/eth-infinitism/account-abstraction/blob/v0.6.0/contracts/interfaces/UserOperation.sol
    """

    user_operation_hash: bytes
    sender: ChecksumAddress
    nonce: int
    init_code: bytes
    call_data: bytes
    call_gas_limit: int
    verification_gas_limit: int
    pre_verification_gas: int
    max_fee_per_gas: int
    max_priority_fee_per_gas: int
    paymaster_and_data: bytes
    signature: bytes
    entry_point: ChecksumAddress
    metadata: Optional[UserOperationMetadata] = None

    @classmethod
    def from_bundler_response(
        cls,
        user_operation_hash: Union[HexStr, bytes],
        user_operation_response: Dict[str, Any],
    ) -> Union["UserOperation", "UserOperationV07"]:
        user_operation = user_operation_response["userOperation"]
        metadata = UserOperationMetadata(
            HexBytes(user_operation_response["transactionHash"]),
            HexBytes(user_operation_response["blockHash"]),
            int(user_operation_response["blockNumber"], 16),
        )
        if "initCode" in user_operation:
            return cls(
                HexBytes(user_operation_hash),
                ChecksumAddress(user_operation["sender"]),
                int(user_operation["nonce"], 16),
                HexBytes(user_operation["initCode"]),
                HexBytes(user_operation["callData"]),
                int(user_operation["callGasLimit"], 16),
                int(user_operation["verificationGasLimit"], 16),
                int(user_operation["preVerificationGas"], 16),
                int(user_operation["maxFeePerGas"], 16),
                int(user_operation["maxPriorityFeePerGas"], 16),
                HexBytes(user_operation["paymasterAndData"]),
                HexBytes(user_operation["signature"]),
                ChecksumAddress(user_operation_response["entryPoint"]),
                metadata=metadata,
            )
        else:
            if paymaster := user_operation.get("paymaster"):
                # Paymaster parameters are optional
                paymaster_verification_gas_limit = int(
                    user_operation["paymasterVerificationGasLimit"], 16
                )
                paymaster_post_op_gas_limit = int(
                    user_operation["paymasterPostOpGasLimit"], 16
                )
                paymaster_data = HexBytes(user_operation["paymasterData"])
            else:
                paymaster_verification_gas_limit = None
                paymaster_post_op_gas_limit = None
                paymaster_data = None

            return UserOperationV07(
                HexBytes(user_operation_hash),
                ChecksumAddress(user_operation["sender"]),
                int(user_operation["nonce"], 16),
                ChecksumAddress(user_operation["factory"]),
                HexBytes(user_operation["factoryData"]),
                HexBytes(user_operation["callData"]),
                int(user_operation["callGasLimit"], 16),
                int(user_operation["verificationGasLimit"], 16),
                int(user_operation["preVerificationGas"], 16),
                int(user_operation["maxPriorityFeePerGas"], 16),
                int(user_operation["maxFeePerGas"], 16),
                HexBytes(user_operation["signature"]),
                ChecksumAddress(user_operation_response["entryPoint"]),
                paymaster_verification_gas_limit,
                paymaster_post_op_gas_limit,
                paymaster,
                paymaster_data,
                metadata=metadata,
            )

    def __str__(self):
        return f"User Operation sender={self.sender} nonce={self.nonce} hash={self.user_operation_hash.hex()}"

    @cached_property
    def paymaster(self) -> Optional[ChecksumAddress]:
        if self.paymaster_and_data and len(self.paymaster_and_data) >= 20:
            return fast_to_checksum_address(self.paymaster_and_data[:20])
        return None

    @cached_property
    def paymaster_data(self) -> Optional[bytes]:
        if self.paymaster_and_data:
            return self.paymaster_and_data[20:]
        return None

    def calculate_user_operation_hash(self, chain_id: int) -> bytes:
        hash_init_code = fast_keccak(self.init_code)
        hash_call_data = fast_keccak(self.call_data)
        hash_paymaster_and_data = fast_keccak(self.paymaster_and_data)
        user_operation_encoded = abi_encode(
            [
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
            ],
            [
                self.sender,
                self.nonce,
                hash_init_code,
                hash_call_data,
                self.call_gas_limit,
                self.verification_gas_limit,
                self.pre_verification_gas,
                self.max_fee_per_gas,
                self.max_priority_fee_per_gas,
                hash_paymaster_and_data,
            ],
        )
        return fast_keccak(
            abi_encode(
                ["bytes32", "address", "uint256"],
                [fast_keccak(user_operation_encoded), self.entry_point, chain_id],
            )
        )


@dataclasses.dataclass(eq=True, frozen=True)
class UserOperationV07:
    """
    EIP4337 UserOperation for Entrypoint v0.7

    https://github.com/eth-infinitism/account-abstraction/blob/v0.7.0/contracts/interfaces/PackedUserOperation.sol
    """

    user_operation_hash: bytes
    sender: ChecksumAddress
    nonce: int
    factory: ChecksumAddress
    factory_data: bytes
    call_data: bytes
    call_gas_limit: int
    verification_gas_limit: int
    pre_verification_gas: int
    max_priority_fee_per_gas: int
    max_fee_per_gas: int
    signature: bytes
    entry_point: ChecksumAddress
    paymaster_verification_gas_limit: Optional[int] = None
    paymaster_post_op_gas_limit: Optional[int] = None
    paymaster: Optional[bytes] = None
    paymaster_data: Optional[bytes] = None
    metadata: Optional[UserOperationMetadata] = None

    @property
    def account_gas_limits(self) -> bytes:
        """
        :return:Account Gas Limits is a `bytes32` in Solidity, first `bytes16` `verification_gas_limit` and then `call_gas_limit`
        """
        return HexBytes(self.verification_gas_limit).rjust(16, b"\x00") + HexBytes(
            self.call_gas_limit
        ).rjust(16, b"\x00")

    @property
    def gas_fees(self) -> bytes:
        """
        :return: Gas Fees is a `bytes32` in Solidity, first `bytes16` `verification_gas_limit` and then `call_gas_limit`
        """
        return HexBytes(self.max_priority_fee_per_gas).rjust(16, b"\x00") + HexBytes(
            self.max_fee_per_gas
        ).rjust(16, b"\x00")

    @property
    def paymaster_and_data(self) -> bytes:
        if not self.paymaster:
            return b""
        return (
            HexBytes(self.paymaster).rjust(20, b"\x00")
            + HexBytes(self.paymaster_verification_gas_limit).rjust(16, b"\x00")
            + HexBytes(self.paymaster_post_op_gas_limit).rjust(16, b"\x00")
            + HexBytes(self.paymaster_data)
        )

    def calculate_user_operation_hash(self, chain_id: int) -> bytes:
        hash_init_code = fast_keccak(HexBytes(self.factory) + self.factory_data)
        hash_call_data = fast_keccak(self.call_data)
        hash_paymaster_and_data = fast_keccak(self.paymaster_and_data)
        user_operation_encoded = abi_encode(
            [
                "address",
                "uint256",
                "bytes32",
                "bytes32",
                "bytes32",
                "uint256",
                "bytes32",
                "bytes32",
            ],
            [
                self.sender,
                self.nonce,
                hash_init_code,
                hash_call_data,
                self.account_gas_limits,
                self.pre_verification_gas,
                self.gas_fees,
                hash_paymaster_and_data,
            ],
        )
        return fast_keccak(
            abi_encode(
                ["bytes32", "address", "uint256"],
                [fast_keccak(user_operation_encoded), self.entry_point, chain_id],
            )
        )
