import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict

from typing import Union, Optional

from eth_typing import Hash32, HexStr

EthereumHash = Union[Hash32, HexStr]
EthereumData = Union[bytes, HexStr]


class BalanceDict(TypedDict):
    token_address: Optional[str]
    balance: int
