from typing import Any, Iterable, Sequence, Union

from hexbytes import HexBytes


def chunks(elements: Sequence[Any], n: int) -> Iterable[Any]:
    """
    :param elements: List
    :param n: Number of elements per chunk
    :return: Yield successive n-sized chunks from l
    """
    for i in range(0, len(elements), n):
        yield elements[i : i + n]


def to_0x_hex_str(value: Union[bytes, HexBytes]) -> str:
    """
    Convert bytes or HexBytes to a 0x-prefixed hex string
    :param value: bytes or HexBytes value
    :return: 0x-prefixed hex string
    """
    if isinstance(value, HexBytes):
        return value.to_0x_hex()
    return "0x" + value.hex()
