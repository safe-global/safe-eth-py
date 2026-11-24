import json
import os
import subprocess
import sys
import sysconfig
import unittest
from pathlib import Path

from native_test_helpers import (
    build_p256_signatures,
    build_secp256k1_signatures,
    reference_checksum_address,
    reference_keccak256,
)

WORKER_PATH = Path(__file__).parent / "free_threading_worker.py"
IS_FREE_THREADED_BUILD = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


def run_python(
    arguments: list[str], stdin_text: str = ""
) -> subprocess.CompletedProcess:
    """
    Run the Python of the tests without `PYTHON_GIL`, so it starts with the GIL
    disabled, and fail on the warning printed when a module enables the GIL again
    """
    environment = {
        name: value for name, value in os.environ.items() if name != "PYTHON_GIL"
    }
    return subprocess.run(
        [sys.executable, "-W", "error::RuntimeWarning", *arguments],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=environment,
        timeout=300,
    )


def build_cases() -> dict:
    """Inputs for every function, with the results of the reference implementations"""
    keccak256_cases = [
        (message.hex(), reference_keccak256(message).hex())
        for message in (
            os.urandom(length)
            for length in (0, 32, 136, 1000, 2047, 2048, 5000, 100_000) * 3
        )
    ]
    ecrecover_cases: list[tuple[str, int, int, int, str | None]] = []
    for message_hash, v, r, s, signer in build_secp256k1_signatures(15):
        ecrecover_cases.append((message_hash.hex(), v, r, s, signer.hex()))
        # `v` out of range never recovers
        ecrecover_cases.append((message_hash.hex(), 29, r, s, None))
    p256_verify_cases = []
    for p256_message_hash, *signature_values in build_p256_signatures(10):
        p256_verify_cases.append(([p256_message_hash, *signature_values], True))
        p256_verify_cases.append(([p256_message_hash ^ 1, *signature_values], False))
    to_checksum_address_cases = [
        (address.hex(), reference_checksum_address(address))
        for address in (os.urandom(20) for _ in range(200))
    ]
    return {
        "keccak256": keccak256_cases,
        "ecrecover": ecrecover_cases,
        "p256_verify": p256_verify_cases,
        "to_checksum_address": to_checksum_address_cases,
    }


@unittest.skipUnless(IS_FREE_THREADED_BUILD, "Python is not a free-threaded build")
class TestFreeThreading(unittest.TestCase):
    def test_import_keeps_the_gil_disabled(self):
        """The module declares it can run without the GIL, so importing it does not enable the GIL"""
        completed_process = run_python(
            [
                "-c",
                "import sys, safe_eth_native; assert not sys._is_gil_enabled()",
            ]
        )
        self.assertEqual(completed_process.returncode, 0, completed_process.stderr)

    def test_parallel_calls_without_gil(self):
        """Every function called from 16 threads at the same time, without the GIL, gives the right result"""
        completed_process = run_python(
            [str(WORKER_PATH)], stdin_text=json.dumps(build_cases())
        )
        self.assertEqual(completed_process.returncode, 0, completed_process.stderr)
        worker_result = json.loads(completed_process.stdout)
        self.assertFalse(worker_result["is_gil_enabled"])
        self.assertEqual(worker_result["wrong_results"], [])
