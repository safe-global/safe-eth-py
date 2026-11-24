import functools
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar
from unittest import TestCase, mock

from eth_hash.auto import keccak as eth_hash_keccak

from safe_eth.util import native

TestCaseType = TypeVar("TestCaseType", bound=TestCase)


@contextmanager
def without_native() -> Iterator[None]:
    """
    Make the helpers and eth-hash (so web3, eth-utils and eth-keys) use their Python
    implementation
    """
    with (
        mock.patch.object(native, "safe_eth_native", None),
        mock.patch.object(eth_hash_keccak, "hasher", native.eth_hash_backend_hasher),
    ):
        yield


def with_and_without_native(
    test_method: Callable[[TestCaseType], Any],
) -> Callable[[TestCaseType], None]:
    """
    Run the test with the native extension and with the Python implementation
    """

    @functools.wraps(test_method)
    def run_test(test_case: TestCaseType) -> None:
        with test_case.subTest(native=True):
            test_method(test_case)
        with test_case.subTest(native=False), without_native():
            test_method(test_case)

    return run_test


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


def assert_same_outcome_with_and_without_native(
    test_case: TestCase, function: Callable[..., Any], *args: Any
) -> None:
    """
    Check ``function(*args)`` returns the same value, or raises the same error with the
    same message, with the native extension and with the Python implementation
    """
    native_outcome = call_outcome(function, *args)
    with without_native():
        python_outcome = call_outcome(function, *args)
    test_case.assertEqual(native_outcome, python_outcome, (function.__name__, args))
