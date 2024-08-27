from typing import Any, Dict, Optional, TypedDict, Union

from eth_typing import ChecksumAddress, Hash32, HexStr
from hexbytes import HexBytes
from web3.types import LogReceipt

EthereumHash = Union[Hash32, HexBytes, HexStr]
EthereumData = Union[bytes, HexStr]


class BalanceDict(TypedDict):
    token_address: Optional[ChecksumAddress]
    balance: int


class LogReceiptDecoded(LogReceipt):
    args: Dict[str, Any]
