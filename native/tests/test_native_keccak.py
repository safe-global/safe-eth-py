import array
import os
import random
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

import safe_eth_native
from native_test_helpers import (
    BytesSubclass,
    load_keccak_256_known_answers,
    reference_keccak256,
)

# Keccak-256 absorbs the input in blocks of 136 bytes
KECCAK_256_RATE = 136
GIL_RELEASE_MIN_LENGTH = 2048


class TestKeccak256(unittest.TestCase):
    def test_known_answers(self):
        """Keccak team ShortMsgKAT_256 vectors, every byte aligned message length from 0 to 255 bytes"""
        known_answers = list(load_keccak_256_known_answers())
        self.assertEqual(len(known_answers), 256)
        for message, expected_digest in known_answers:
            with self.subTest(message_length=len(message)):
                self.assertEqual(safe_eth_native.keccak256(message), expected_digest)

    def test_ethereum_vectors(self):
        """Digests used across the Ethereum tooling (eth-hash, solidity selectors)"""
        for message, expected_digest_hex in (
            (b"", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
            (
                b"arsttsra",
                "b1f354b28ff28452d6b9d61f41061bbe82beb1fc98f33364a8058d1a5d164d05",
            ),
            (
                b"transfer(address,uint256)",
                "a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b",
            ),
            (
                b"Transfer(address,address,uint256)",
                "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            ),
        ):
            with self.subTest(message=message):
                self.assertEqual(
                    safe_eth_native.keccak256(message).hex(), expected_digest_hex
                )

    def test_every_length_matches_pycryptodome(self):
        """
        Lengths from 0 to several blocks, so every padding position and the block
        boundaries are covered, plus the lengths around the GIL release threshold
        """
        lengths = list(range(0, KECCAK_256_RATE * 5 + 2)) + [
            GIL_RELEASE_MIN_LENGTH - 1,
            GIL_RELEASE_MIN_LENGTH,
            GIL_RELEASE_MIN_LENGTH + 1,
        ]
        for length in lengths:
            message = os.urandom(length)
            expected_digest = reference_keccak256(message)
            self.assertEqual(
                safe_eth_native.keccak256(message), expected_digest, length
            )

    def test_long_messages(self):
        """Messages of several MiB, hashed without the GIL"""
        for message in (
            b"\x00" * (1 << 20),
            bytes(range(256)) * 8192,
            os.urandom(5 << 20),
        ):
            self.assertEqual(
                safe_eth_native.keccak256(message), reference_keccak256(message)
            )

    def test_threads(self):
        """Hashing from several threads at once, under and over the GIL release threshold"""
        messages = [os.urandom(length) for length in (32, 1000, 4096, 100_000) * 50]
        expected_digests = [reference_keccak256(message) for message in messages]
        with ThreadPoolExecutor(max_workers=8) as executor:
            digests = list(executor.map(safe_eth_native.keccak256, messages))
        self.assertEqual(digests, expected_digests)

    def test_bytes_subclass(self):
        """`bytes` subclasses like `HexBytes` are accepted"""
        message = BytesSubclass(b"message")
        self.assertEqual(
            safe_eth_native.keccak256(message), reference_keccak256(b"message")
        )

    def test_return_type(self):
        """The digest is 32 `bytes`"""
        digest = safe_eth_native.keccak256(b"")
        self.assertIs(type(digest), bytes)
        self.assertEqual(len(digest), 32)

    def test_byte_buffers(self):
        """
        Buffers give the digest of their raw bytes, like pysha3 and `hashlib`, whatever
        their item format, also for unaligned views (pysha3 unaligned tests)
        """
        for length in (
            0,
            1,
            32,
            KECCAK_256_RATE,
            1000,
            GIL_RELEASE_MIN_LENGTH,
            100_000,
        ):
            message = os.urandom(length)
            expected_digest = reference_keccak256(message)
            for buffer in (
                bytearray(message),
                memoryview(message),
                memoryview(bytearray(message)),
                array.array("B", message),
                array.array("b", message),
            ):
                with self.subTest(length=length, buffer_type=type(buffer).__name__):
                    self.assertEqual(safe_eth_native.keccak256(buffer), expected_digest)
            if length % 4 == 0:
                for wide_items_buffer in (
                    memoryview(message).cast("I"),
                    array.array("I", message),
                ):
                    self.assertEqual(
                        safe_eth_native.keccak256(wide_items_buffer), expected_digest
                    )
            for offset in range(1, 15):
                unaligned_view = memoryview(offset * b"\x00" + message)[offset:]
                self.assertEqual(
                    safe_eth_native.keccak256(unaligned_view), expected_digest
                )
            if length > 1:
                # Like `hashlib`, only C-contiguous buffers are accepted
                with self.assertRaises(BufferError):
                    safe_eth_native.keccak256(memoryview(message)[::2])

    def test_bytearray_changed_by_other_threads(self):
        """
        Hashing a `bytearray` that other threads write to and try to resize never crashes
        and always returns a digest. A resize fails with `BufferError` while it is hashed
        """
        shared_data = bytearray(os.urandom(GIL_RELEASE_MIN_LENGTH * 50))
        stop_event = threading.Event()

        def change_shared_data() -> None:
            while not stop_event.is_set():
                shared_data[random.randrange(len(shared_data))] = random.randrange(256)
                try:
                    shared_data.extend(b"\x00" * 100)
                    del shared_data[-100:]
                except BufferError:
                    pass

        writer_threads = [threading.Thread(target=change_shared_data) for _ in range(2)]
        for writer_thread in writer_threads:
            writer_thread.start()
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                digests = list(
                    executor.map(
                        lambda _: safe_eth_native.keccak256(shared_data), range(200)
                    )
                )
        finally:
            stop_event.set()
            for writer_thread in writer_threads:
                writer_thread.join()
        self.assertTrue(all(len(digest) == 32 for digest in digests))

    def test_buffer_rewritten_by_other_threads_is_hashed_whole(self):
        """
        Other threads replace the whole content of a `bytearray` while it is hashed, directly
        or through a `memoryview`: each digest is the one of a full content, never of a mix
        of two (the case that matters on free-threaded Python)
        """
        first_content = os.urandom(GIL_RELEASE_MIN_LENGTH * 50)
        second_content = os.urandom(len(first_content))
        expected_digests = {
            reference_keccak256(first_content),
            reference_keccak256(second_content),
        }
        shared_data = bytearray(first_content)
        stop_event = threading.Event()

        def rewrite_shared_data() -> None:
            while not stop_event.is_set():
                shared_data[:] = first_content
                shared_data[:] = second_content

        for buffer in (
            shared_data,
            memoryview(shared_data),
            memoryview(shared_data)[0:],
        ):
            with self.subTest(buffer_type=type(buffer).__name__):
                writer_threads = [
                    threading.Thread(target=rewrite_shared_data) for _ in range(2)
                ]
                stop_event.clear()
                for writer_thread in writer_threads:
                    writer_thread.start()
                try:
                    with ThreadPoolExecutor(max_workers=4) as executor:
                        digests = set(
                            executor.map(
                                lambda _, buffer=buffer: safe_eth_native.keccak256(
                                    buffer
                                ),
                                range(300),
                            )
                        )
                finally:
                    stop_event.set()
                    for writer_thread in writer_threads:
                        writer_thread.join()
                self.assertLessEqual(digests, expected_digests)

    def test_rejects_other_types(self):
        """Text must be encoded first, and other objects without a buffer are rejected"""
        for value in ("text", None, 1, [1, 2], object()):
            with self.subTest(value=value), self.assertRaises(TypeError):
                safe_eth_native.keccak256(value)
