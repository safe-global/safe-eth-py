from typing import Union

from eth_typing import Hash32, HexStr
from hexbytes import HexBytes

EthereumHash = Union[Hash32, HexBytes, HexStr]
EthereumData = Union[bytes, HexBytes, HexStr]
