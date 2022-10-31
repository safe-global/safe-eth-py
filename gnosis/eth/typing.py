from typing import Optional, TypedDict, Union

from eth_typing import Hash32, HexStr
from hexbytes import HexBytes

EthereumHash = Union[Hash32, HexBytes, HexStr]
EthereumData = Union[bytes, HexStr]


class BalanceDict(TypedDict):
    token_address: Optional[str]
    balance: int
