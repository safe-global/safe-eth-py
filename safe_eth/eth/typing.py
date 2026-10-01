from typing import Any, TypedDict

from eth_typing import ChecksumAddress, Hash32, HexStr
from hexbytes import HexBytes
from web3.types import LogReceipt

EthereumHash = Hash32 | HexBytes | HexStr
EthereumData = bytes | HexStr


class BalanceDict(TypedDict):
    token_address: ChecksumAddress | None
    balance: int


class LogReceiptDecoded(LogReceipt):
    args: dict[str, Any]
