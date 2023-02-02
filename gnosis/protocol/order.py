from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Literal

from eth_typing import ChecksumAddress, Hash32


@dataclass
class Order:
    sellToken: ChecksumAddress
    buyToken: ChecksumAddress
    receiver: ChecksumAddress
    sellAmount: int
    buyAmount: int
    validTo: int
    appData: Hash32
    feeAmount: int
    kind: Literal["sell", "buy"]
    partiallyFillable: bool
    sellTokenBalance: Literal["erc20", "external", "internal"]
    buyTokenBalance: Literal["erc20", "internal"]

    def is_sell_order(self) -> bool:
        return self.kind == "sell"

    def get_eip712_structured_data(
        self, chain_id: int, verifying_contract: ChecksumAddress
    ) -> Dict[str, Any]:
        types = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Order": [
                {"name": "sellToken", "type": "address"},
                {"name": "buyToken", "type": "address"},
                {"name": "receiver", "type": "address"},
                {"name": "sellAmount", "type": "uint256"},
                {"name": "buyAmount", "type": "uint256"},
                {"name": "validTo", "type": "uint32"},
                {"name": "appData", "type": "bytes32"},
                {"name": "feeAmount", "type": "uint256"},
                {"name": "kind", "type": "string"},
                {"name": "partiallyFillable", "type": "bool"},
                {"name": "sellTokenBalance", "type": "string"},
                {"name": "buyTokenBalance", "type": "string"},
            ],
        }
        message = {
            "sellToken": self.sellToken,
            "buyToken": self.buyToken,
            "receiver": self.receiver,
            "sellAmount": self.sellAmount,
            "buyAmount": self.buyAmount,
            "validTo": self.validTo,
            "appData": self.appData,
            "feeAmount": self.feeAmount,
            "kind": self.kind,
            "partiallyFillable": self.partiallyFillable,
            "sellTokenBalance": self.sellTokenBalance,
            "buyTokenBalance": self.buyTokenBalance,
        }

        return {
            "types": types,
            "primaryType": "Order",
            "domain": {
                "name": "Gnosis Protocol",
                "version": "v2",
                "chainId": chain_id,
                "verifyingContract": verifying_contract,
            },
            "message": message,
        }


class OrderKind(Enum):
    BUY = 0
    SELL = 1
