import dataclasses
from typing import Any, Dict, List, Optional

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.types import LogReceipt

from gnosis.eth.account_abstraction.constants import (
    ACCOUNT_DEPLOYED_TOPIC,
    DEPOSIT_EVENT_TOPIC,
    EXECUTION_FROM_MODULE_FAILURE_TOPIC,
    EXECUTION_FROM_MODULE_SUCCESS_TOPIC,
)
from gnosis.eth.utils import fast_to_checksum_address


@dataclasses.dataclass(eq=True, frozen=True)
class UserOperationReceipt:
    user_operation_hash: bytes
    entry_point: ChecksumAddress
    sender: ChecksumAddress
    nonce: int
    paymaster: Optional[ChecksumAddress]
    actual_gas_cost: int
    actual_gas_used: int
    success: bool
    reason: Optional[str]
    logs: List[LogReceipt]

    @classmethod
    def from_bundler_response(
        cls,
        user_operation_receipt_response: Dict[str, Any],
    ) -> "UserOperationReceipt":
        return cls(
            HexBytes(user_operation_receipt_response["userOpHash"]),
            user_operation_receipt_response["entryPoint"],
            user_operation_receipt_response["sender"],
            int(user_operation_receipt_response["nonce"], 16),
            user_operation_receipt_response.get("paymaster"),
            int(user_operation_receipt_response["actualGasCost"], 16),
            int(user_operation_receipt_response["actualGasUsed"], 16),
            user_operation_receipt_response["success"],
            user_operation_receipt_response.get("reason"),
            user_operation_receipt_response["logs"],
        )

    def get_deployed_account(self) -> Optional[ChecksumAddress]:
        """
        :return: Deployed account in case a new account was deployed
        """
        for log in self.logs:
            if (
                len(log["topics"]) == 3
                and HexBytes(log["topics"][0]) == ACCOUNT_DEPLOYED_TOPIC
            ):
                # Address is stored at the 40 last chars of the 3rd topic
                return fast_to_checksum_address(log["topics"][2][-40:])
        return None

    def get_deposit(self) -> int:
        """
        :return: Deposited value on the entrypoint for running the UserOperationReceipt
        """
        deposited = 0
        for log in self.logs:
            if (
                len(log["topics"]) == 2
                and HexBytes(log["topics"][0]) == DEPOSIT_EVENT_TOPIC
                and fast_to_checksum_address(log["address"]) == self.entry_point
                and fast_to_checksum_address(log["topics"][1][-40:]) == self.sender
            ):
                deposited += int(log["data"], 16)
        return deposited

    def get_module_address(self) -> Optional[ChecksumAddress]:
        """
        Use Safe's `ExecutionFromModuleSuccess` event to get the 4337 module address

        :return: If using a ``Safe``, the ``4337 module address`` used, ``None`` otherwise
        """
        for log in reversed(self.logs):
            if (
                len(log["topics"]) == 2
                and HexBytes(log["topics"][0])
                in (
                    EXECUTION_FROM_MODULE_SUCCESS_TOPIC,
                    EXECUTION_FROM_MODULE_FAILURE_TOPIC,
                )
                and fast_to_checksum_address(log["address"]) == self.sender
            ):
                return fast_to_checksum_address(log["topics"][1][-40:])
        return None
