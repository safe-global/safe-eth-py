"""
Makes eth-hash, so web3, eth-utils and eth-account, use the keccak256 of the native
(Rust) extension ``safe-eth-native``
"""

import os

import safe_eth_native
from eth_hash.abc import PreImageAPI
from eth_hash.auto import keccak as eth_hash_keccak

# Functions of the eth-hash backend, before they are replaced
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


def check_native_keccak256() -> None:
    """
    :raises ImportError: if the native keccak256 of an empty input is wrong, as all the
        hashes of the process would be wrong too
    """
    if safe_eth_native.keccak256(b"") != EMPTY_INPUT_KECCAK256:
        raise ImportError(
            "safe-eth-native keccak256 returns wrong digests, reinstall safe-eth-native"
        )


def use_native_keccak_in_eth_hash() -> None:
    """
    Make the native keccak256 the one of eth-hash, for ``keccak()`` and ``keccak.new()``,
    so web3, eth-utils and eth-account use it, unless ``ETH_HASH_BACKEND`` selects an
    eth-hash backend. eth-hash cannot register a new backend, so its ``hasher`` and
    ``preimage`` attributes are replaced.

    :raises ImportError: if the backend set in ``ETH_HASH_BACKEND`` is not installed.
        eth-hash loads and checks its backend on the first hash, so it is done here
    """
    if os.getenv("ETH_HASH_BACKEND"):
        eth_hash_keccak(b"")
    else:
        eth_hash_keccak.hasher = safe_eth_native.keccak256  # type: ignore[assignment]
        eth_hash_keccak.preimage = NativeKeccakPreimage  # type: ignore[assignment]


check_native_keccak256()
use_native_keccak_in_eth_hash()
