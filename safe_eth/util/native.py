"""
Native (Rust) implementations of the hot paths, installed with the ``native`` extra
(``safe-eth-py[native]``). ``safe_eth_native`` is ``None`` when the extra is not
installed, and the callers use their Python implementation.
"""

import os

from eth_hash.abc import PreImageAPI
from eth_hash.auto import keccak as eth_hash_keccak

try:
    import safe_eth_native
except ImportError:
    safe_eth_native = None  # type: ignore[assignment]

# Functions of the eth-hash backend, to go back to them without the native extension
eth_hash_backend_hasher = eth_hash_keccak.hasher
eth_hash_backend_preimage = eth_hash_keccak.preimage

EMPTY_INPUT_KECCAK256 = bytes.fromhex(
    "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
)


class NativeKeccakPreimage(PreImageAPI):
    """
    ``keccak.new()`` of eth-hash with the native keccak256. The data is kept and hashed
    again on each ``digest()``, as the pycryptodome backend of eth-hash also keeps it to
    be able to copy. So each ``digest()`` costs the size of all the data so far, and many
    ``update()`` and ``digest()`` calls on the same object take quadratic time. Nothing in
    web3, eth-utils or eth-account uses ``keccak.new()``; if something calls it in a loop,
    a native class that keeps the Keccak state is the fix.
    """

    def __init__(self, value: bytes | bytearray) -> None:
        self._data = bytearray(value)

    def update(self, value: bytes) -> None:
        self._data += value

    def digest(self) -> bytes:
        return safe_eth_native.keccak256(self._data)

    def copy(self) -> "NativeKeccakPreimage":
        return NativeKeccakPreimage(self._data)


def use_native_keccak_in_eth_hash() -> None:
    """
    Make the native keccak256 the one of eth-hash, for ``keccak()`` and ``keccak.new()``,
    so web3, eth-utils and eth-account use it, unless the extension is not installed or
    ``ETH_HASH_BACKEND`` selects an eth-hash backend. eth-hash cannot register a new
    backend, so its ``hasher`` and ``preimage`` attributes are replaced, after the same
    check of the empty input digest that eth-hash runs on its backends.
    """
    if (
        safe_eth_native is not None
        and not os.getenv("ETH_HASH_BACKEND")
        and safe_eth_native.keccak256(b"") == EMPTY_INPUT_KECCAK256
    ):
        eth_hash_keccak.hasher = safe_eth_native.keccak256  # type: ignore[assignment]
        eth_hash_keccak.preimage = NativeKeccakPreimage  # type: ignore[assignment]


def restore_eth_hash_backend() -> None:
    """
    Make eth-hash use its own backend again, the pycryptodome or pysha3 keccak256
    """
    eth_hash_keccak.hasher = eth_hash_backend_hasher
    eth_hash_keccak.preimage = eth_hash_backend_preimage


use_native_keccak_in_eth_hash()
