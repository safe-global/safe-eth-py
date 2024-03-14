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

    https://github.com/eth-infinitism/account-abstraction/blob/v0.6.0
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
    ) -> "UserOperation":
        return cls(
            HexBytes(user_operation_hash),
            ChecksumAddress(user_operation_response["userOperation"]["sender"]),
            int(user_operation_response["userOperation"]["nonce"], 16),
            HexBytes(user_operation_response["userOperation"]["initCode"]),
            HexBytes(user_operation_response["userOperation"]["callData"]),
            int(user_operation_response["userOperation"]["callGasLimit"], 16),
            int(user_operation_response["userOperation"]["verificationGasLimit"], 16),
            int(user_operation_response["userOperation"]["preVerificationGas"], 16),
            int(user_operation_response["userOperation"]["maxFeePerGas"], 16),
            int(user_operation_response["userOperation"]["maxPriorityFeePerGas"], 16),
            HexBytes(user_operation_response["userOperation"]["paymasterAndData"]),
            HexBytes(user_operation_response["userOperation"]["signature"]),
            ChecksumAddress(user_operation_response["entryPoint"]),
            metadata=UserOperationMetadata(
                HexBytes(user_operation_response["transactionHash"]),
                HexBytes(user_operation_response["blockHash"]),
                int(user_operation_response["blockNumber"], 16),
            ),
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
        result = self.paymaster_and_data[:20]
        return result if result else None

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
