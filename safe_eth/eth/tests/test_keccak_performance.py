import os

import pytest
from eth_utils import keccak
from web3 import Web3

from safe_eth.eth.utils import fast_keccak

# Define the message sizes (parameters)
TEST_SIZES = [16, 1024, 64 * 1024, 1024 * 1024]


# --- 1. Data Fixture (Forces Cache Miss) ---
@pytest.fixture(scope="function", params=TEST_SIZES)
def random_data(request):
    """
    Fixture that yields a new, random byte string for each test parameter.
    This guarantees a cache miss for fast_keccak on every run.
    """
    size = request.param
    name = f"{size // 1024}KB" if size >= 1024 else f"{size}B"
    # Yield the name and the fresh random data
    return name, os.urandom(size)


# --- 2. Benchmark Tests ---
#
def test_keccak_web3_py(benchmark, random_data):
    name, data = random_data
    # Group results by the input size name
    benchmark.group = f"Keccak-{name}"
    # The benchmark fixture runs the function multiple times
    benchmark(Web3.keccak, data)


def test_keccak_eth_utils(benchmark, random_data):
    name, data = random_data
    # Group results by the input size name
    benchmark.group = f"Keccak-{name}"
    # The benchmark fixture runs the function multiple times
    benchmark(keccak, data)


def test_keccak_safe_eth(benchmark, random_data):
    name, data = random_data
    # Use the same group name to align the results
    benchmark.group = f"Keccak-{name}"
    # The benchmark fixture runs the function multiple times
    benchmark(fast_keccak, data)
