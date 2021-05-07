from typing import Optional, Union

from eth_typing import Hash32, HexStr
from hexbytes import HexBytes

try:
    from typing import TypedDict  # pylint: disable=no-name-in-module
except ImportError:
    from typing_extensions import TypedDict


EthereumHash = Union[Hash32, HexBytes, HexStr]
EthereumData = Union[bytes, HexStr]


class BalanceDict(TypedDict):
    token_address: Optional[str]
    balance: int
