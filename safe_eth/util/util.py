import os
from logging import getLogger
from typing import Any, Iterable, Sequence

from eth_typing import HexStr

logger = getLogger(__name__)

TRUTHY_ENV_VALUES = ("1", "true", "yes", "on")
FALSY_ENV_VALUES = ("0", "false", "no", "off")


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


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Read a boolean environment variable

    :param name: Environment variable name
    :param default: Value returned when the variable is not set, or set to a value that
        is neither truthy nor falsy
    :return: `True` for `1`, `true`, `yes` and `on`, `False` for `0`, `false`, `no` and
        `off` (both case insensitive), `default` otherwise
    """
    value = os.environ.get(name)
    if value is None:
        return default
    normalized_value = value.strip().lower()
    if normalized_value in TRUTHY_ENV_VALUES:
        return True
    if normalized_value in FALSY_ENV_VALUES:
        return False
    logger.warning(
        "Environment variable %s=%s is not a boolean, using %s",
        name,
        value,
        default,
    )
    return default
