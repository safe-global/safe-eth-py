from typing import Any, Iterable, Sequence

from eth_typing import HexStr


def chunks(elements: Sequence[Any], n: int) -> Iterable[Any]:
    """
    :param elements: List
    :param n: Number of elements per chunk
    :return: Yield successive n-sized chunks from l
    """
    for i in range(0, len(elements), n):
        yield elements[i : i + n]


def to_0x_hex_str(value: bytes) -> HexStr:
    """
    Convert bytes to a 0x-prefixed hex string

    :param value: bytes value
    :return: 0x-prefixed hex string
    """
    return HexStr("0x" + value.hex())
