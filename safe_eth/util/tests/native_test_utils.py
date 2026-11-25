from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any
from unittest import TestCase, mock

from Crypto.Hash import keccak as pycryptodome_keccak
from eth_hash.auto import keccak as eth_hash_keccak

from safe_eth.util import native


@contextmanager
def eth_hash_backend() -> Iterator[None]:
    """
    Make eth-hash (so web3, eth-utils and eth-keys) use its own backend instead of the
    native keccak256
    """
    with (
        mock.patch.object(eth_hash_keccak, "hasher", native.eth_hash_backend_hasher),
        mock.patch.object(
            eth_hash_keccak, "preimage", native.eth_hash_backend_preimage
        ),
    ):
        yield


def reference_keccak256(data: bytes) -> bytes:
    """keccak256 of the raw bytes of ``data``, with pycryptodome"""
    return pycryptodome_keccak.new(
        digest_bits=256, data=memoryview(data).tobytes()
    ).digest()


def call_outcome(function: Callable[..., Any], *args: Any) -> tuple[Any, ...]:
    """
    :return: ``("result", <result>, <result type>)`` or
        ``("error", <exception type>, <exception message>)``
    """
    try:
        result = function(*args)
    except Exception as error:
        return ("error", type(error), str(error))
    return ("result", result, type(result))


def assert_same_outcome_as_reference(
    test_case: TestCase,
    function: Callable[..., Any],
    reference_function: Callable[..., Any],
    *args: Any,
) -> None:
    """
    Check ``function(*args)`` returns the same value, or raises the same error with the
    same message, as ``reference_function(*args)``, which runs with the eth-hash backend
    instead of the native keccak256
    """
    outcome = call_outcome(function, *args)
    with eth_hash_backend():
        reference_outcome = call_outcome(reference_function, *args)
    test_case.assertEqual(outcome, reference_outcome, (function.__name__, args))
