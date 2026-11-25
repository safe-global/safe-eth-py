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
    so web3, eth-utils and eth-account use it, unless ``ETH_HASH_BACKEND`` selects an
    eth-hash backend. eth-hash cannot register a new backend, so its ``hasher`` and
    ``preimage`` attributes are replaced.
    """
    if not os.getenv("ETH_HASH_BACKEND"):
        eth_hash_keccak.hasher = safe_eth_native.keccak256  # type: ignore[assignment]
        eth_hash_keccak.preimage = NativeKeccakPreimage  # type: ignore[assignment]


use_native_keccak_in_eth_hash()
