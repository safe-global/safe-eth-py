import dataclasses
from typing import Any, Dict, Union

from eth_abi import encode as abi_encode
from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes

from gnosis.eth.utils import fast_keccak


@dataclasses.dataclass
class UserOperation:
    """
    EIP4337 UserOperation for Entrypoint v0.6

    https://github.com/eth-infinitism/account-abstraction/blob/v0.6.0
    """

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
    transaction_hash: bytes
    block_hash: bytes
    block_number: int
    user_operation_hash: bytes

    def __init__(
        self,
        user_operation_hash: Union[HexStr, bytes],
        user_operation_response: Dict[str, Any],
    ):
        self.sender = ChecksumAddress(
            user_operation_response["userOperation"]["sender"]
        )
        self.nonce = int(user_operation_response["userOperation"]["nonce"], 16)
        self.init_code = HexBytes(user_operation_response["userOperation"]["initCode"])
        self.call_data = HexBytes(user_operation_response["userOperation"]["callData"])
        self.call_gas_limit = int(
            user_operation_response["userOperation"]["callGasLimit"], 16
        )
        self.verification_gas_limit = int(
            user_operation_response["userOperation"]["verificationGasLimit"], 16
        )
        self.pre_verification_gas = int(
            user_operation_response["userOperation"]["preVerificationGas"], 16
        )
        self.max_fee_per_gas = int(
            user_operation_response["userOperation"]["maxFeePerGas"], 16
        )
        self.max_priority_fee_per_gas = int(
            user_operation_response["userOperation"]["maxPriorityFeePerGas"], 16
        )
        self.paymaster_and_data = HexBytes(
            user_operation_response["userOperation"]["paymasterAndData"]
        )
        self.signature = HexBytes(user_operation_response["userOperation"]["signature"])
        self.entry_point = ChecksumAddress(user_operation_response["entryPoint"])
        self.transaction_hash = HexBytes(user_operation_response["transactionHash"])
        self.block_hash = HexBytes(user_operation_response["blockHash"])
        self.block_number = int(user_operation_response["blockNumber"], 16)
        self.user_operation_hash = HexBytes(user_operation_hash)

    def __str__(self):
        return f"User Operation sender={self.sender} nonce={self.nonce} hash={self.user_operation_hash.hex()}"

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
