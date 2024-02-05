from typing import Any, Dict, Optional, TypedDict, Union

from eth_typing import Hash32, HexStr
from hexbytes import HexBytes
from web3.types import LogReceipt

EthereumHash = Union[Hash32, HexBytes, HexStr]
EthereumData = Union[bytes, HexStr]


class BalanceDict(TypedDict):
    token_address: Optional[str]
    balance: int


class LogReceiptDecoded(LogReceipt):
    args: Dict[str, Any]
