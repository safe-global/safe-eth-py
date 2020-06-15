from typing import Union, TypedDict, Optional

from eth_typing import Hash32, HexStr
from hexbytes import HexBytes

EthereumHash = Union[Hash32, HexStr]
EthereumData = Union[bytes, HexStr]


class BalanceDict(TypedDict):
    token_address: Optional[str]
    balance: int
