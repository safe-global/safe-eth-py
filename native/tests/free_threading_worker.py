"""
Calls every function of ``safe_eth_native`` from many threads at the same time.

It runs in its own process and imports only ``safe_eth_native`` and the standard library,
as importing a module that does not support free-threading (pysha3, for example) enables the
GIL again. Reads the cases and their expected results as JSON from stdin, and prints the
GIL state and the wrong results as JSON.
"""

import json
import sys
import threading
from typing import Any

import safe_eth_native

THREAD_COUNT = 16
ROUNDS = 10


def find_wrong_results(cases: dict[str, Any]) -> list[str]:
    wrong_results = []
    for message_hex, expected_digest_hex in cases["keccak256"]:
        digest = safe_eth_native.keccak256(bytes.fromhex(message_hex))
        if digest.hex() != expected_digest_hex:
            wrong_results.append(f"keccak256 of {len(message_hex) // 2} bytes")
    for message_hash_hex, v, r, s, expected_signer_hex in cases["ecrecover"]:
        signer = safe_eth_native.ecrecover(bytes.fromhex(message_hash_hex), v, r, s)
        if (signer.hex() if signer else None) != expected_signer_hex:
            wrong_results.append(f"ecrecover {message_hash_hex}")
    for signature_values, expected_is_valid in cases["p256_verify"]:
        if safe_eth_native.p256_verify(*signature_values) != expected_is_valid:
            wrong_results.append(f"p256_verify {signature_values}")
    for address_hex, expected_checksum_address in cases["to_checksum_address"]:
        if (
            safe_eth_native.to_checksum_address(address_hex)
            != expected_checksum_address
        ):
            wrong_results.append(f"to_checksum_address {address_hex}")
        if not safe_eth_native.is_checksum_address(expected_checksum_address):
            wrong_results.append(f"is_checksum_address {expected_checksum_address}")
    return wrong_results


def is_gil_enabled() -> bool:
    # Free-threaded builds exist since Python 3.13
    if sys.version_info >= (3, 13):
        return sys._is_gil_enabled()
    return True


def main() -> None:
    cases = json.load(sys.stdin)
    wrong_results_by_thread: list[list[str]] = [[] for _ in range(THREAD_COUNT)]
    start_barrier = threading.Barrier(THREAD_COUNT)

    def run_thread(thread_index: int) -> None:
        start_barrier.wait()
        for _ in range(ROUNDS):
            wrong_results_by_thread[thread_index] += find_wrong_results(cases)

    threads = [
        threading.Thread(target=run_thread, args=(thread_index,))
        for thread_index in range(THREAD_COUNT)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(
        json.dumps(
            {
                "is_gil_enabled": is_gil_enabled(),
                "wrong_results": [
                    wrong_result
                    for wrong_results in wrong_results_by_thread
                    for wrong_result in wrong_results
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
