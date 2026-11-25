"""
Native (Rust) implementations of the hot paths, installed with the ``native`` extra
(``safe-eth-py[native]``). ``safe_eth_native`` is ``None`` when the extra is not
installed, and the callers use their Python implementation.
"""

import os

from eth_hash.auto import keccak as eth_hash_keccak

try:
    import safe_eth_native
except ImportError:
    safe_eth_native = None  # type: ignore[assignment]

# Hash function of the eth-hash backend, to go back to it without the native extension
eth_hash_backend_hasher = eth_hash_keccak.hasher

EMPTY_INPUT_KECCAK256 = bytes.fromhex(
    "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
)


def use_native_keccak_in_eth_hash() -> None:
    """
    Make the native keccak256 the one of eth-hash, so web3, eth-utils and eth-account use
    it, unless the extension is not installed or ``ETH_HASH_BACKEND`` selects an eth-hash
    backend. eth-hash cannot register a new backend, so its ``hasher`` attribute is
    replaced, after the same check of the empty input digest that eth-hash runs on its
    backends. ``keccak.new()`` keeps using the eth-hash backend.
    """
    if (
        safe_eth_native is not None
        and not os.getenv("ETH_HASH_BACKEND")
        and safe_eth_native.keccak256(b"") == EMPTY_INPUT_KECCAK256
    ):
        eth_hash_keccak.hasher = safe_eth_native.keccak256  # type: ignore[assignment]


def restore_eth_hash_backend() -> None:
    """
    Make eth-hash use its own backend again, the pycryptodome or pysha3 keccak256
    """
    eth_hash_keccak.hasher = eth_hash_backend_hasher


use_native_keccak_in_eth_hash()
