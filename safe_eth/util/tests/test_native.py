import os
from unittest import TestCase, mock

import eth_utils
from eth_hash.auto import keccak as eth_hash_keccak
from sha3 import keccak_256

from safe_eth.util import native


class TestNative(TestCase):
    def test_native_extension_is_installed(self):
        """
        The tests run with the ``native`` extra installed, so both the native and the
        Python implementations are always tested
        """
        self.assertIsNotNone(native.safe_eth_native)


class TestNativeKeccakInEthHash(TestCase):
    def test_eth_hash_uses_native_keccak(self):
        """Importing safe-eth-py makes the native keccak256 the eth-hash one, `new()` included"""
        self.assertIs(eth_hash_keccak.hasher, native.safe_eth_native.keccak256)
        self.assertIs(eth_hash_keccak.preimage, native.NativeKeccakPreimage)
        self.assertIsInstance(eth_hash_keccak.new(b""), native.NativeKeccakPreimage)

    def test_eth_hash_new_same_digests_as_pysha3(self):
        """
        `keccak.new()` gives the pysha3 digests after each update, for every input type
        pysha3 takes, and its copies are independent
        """
        first_part, second_part, third_part = (
            os.urandom(length) for length in (0, 137, 3000)
        )
        preimage = eth_hash_keccak.new(bytearray(first_part))
        expected_hash = keccak_256(first_part)
        self.assertEqual(preimage.digest(), expected_hash.digest())
        for part in (second_part, bytearray(third_part), memoryview(second_part)):
            preimage.update(part)
            expected_hash.update(part)
            self.assertEqual(preimage.digest(), expected_hash.digest())
        preimage_copy = preimage.copy()
        preimage_copy.update(b"only in the copy")
        self.assertEqual(preimage.digest(), expected_hash.digest())
        expected_hash.update(b"only in the copy")
        self.assertEqual(preimage_copy.digest(), expected_hash.digest())
        with self.assertRaises(TypeError):
            preimage.update("text")
        with self.assertRaisesRegex(
            TypeError, "Can only compute the hash of `bytes` or `bytearray`"
        ):
            eth_hash_keccak.new("text")

    def test_eth_hash_calls_hasher(self):
        """
        `hasher` is not a documented eth-hash API: check eth-utils still goes through it,
        so an eth-hash upgrade cannot drop the native keccak256 without failing here
        """
        with mock.patch.object(
            eth_hash_keccak, "hasher", wraps=native.safe_eth_native.keccak256
        ) as hasher:
            eth_utils.keccak(b"data")
            eth_utils.to_checksum_address(os.urandom(20))
        self.assertEqual(hasher.call_count, 2)

    def test_same_digests_as_pysha3(self):
        """eth-hash and eth-utils give the pysha3 digests for `bytes`, `bytearray` and hex input"""
        for length in (0, 1, 32, 136, 1000, 5000):
            data = os.urandom(length)
            expected_digest = keccak_256(data).digest()
            with self.subTest(length=length):
                self.assertEqual(eth_hash_keccak(data), expected_digest)
                self.assertEqual(eth_hash_keccak(bytearray(data)), expected_digest)
                self.assertEqual(eth_utils.keccak(data), expected_digest)
                self.assertEqual(eth_utils.keccak(hexstr=data.hex()), expected_digest)

    def test_eth_hash_still_validates_the_input_type(self):
        """eth-hash rejects the input before calling `hasher`, with its own error"""
        for value in ("text", memoryview(b"data"), None, 1):
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    TypeError, "Can only compute the hash of `bytes` or `bytearray`"
                ):
                    eth_hash_keccak(value)

    def test_eth_hash_backend_env_is_respected(self):
        """
        `ETH_HASH_BACKEND`, a missing extension, or a native keccak256 that gives a wrong
        digest for the empty input leave the eth-hash backend as it is
        """
        broken_native_extension = mock.Mock()
        broken_native_extension.keccak256.return_value = bytes(32)
        for patch in (
            mock.patch.dict(os.environ, {"ETH_HASH_BACKEND": "pysha3"}),
            mock.patch.object(native, "safe_eth_native", None),
            mock.patch.object(native, "safe_eth_native", broken_native_extension),
        ):
            with (
                self.subTest(patch=patch),
                mock.patch.object(eth_hash_keccak, "hasher") as hasher,
                mock.patch.object(eth_hash_keccak, "preimage") as preimage,
                patch,
            ):
                native.use_native_keccak_in_eth_hash()
                self.assertIs(eth_hash_keccak.hasher, hasher)
                self.assertIs(eth_hash_keccak.preimage, preimage)
        # Without patches they are replaced, so the checks above can fail
        with (
            mock.patch.object(eth_hash_keccak, "hasher"),
            mock.patch.object(eth_hash_keccak, "preimage"),
        ):
            native.use_native_keccak_in_eth_hash()
            self.assertIs(eth_hash_keccak.hasher, native.safe_eth_native.keccak256)
            self.assertIs(eth_hash_keccak.preimage, native.NativeKeccakPreimage)

    def test_restore_eth_hash_backend(self):
        """eth-hash goes back to its own backend, with the same digests, and can use native again"""
        data = os.urandom(100)
        try:
            native.restore_eth_hash_backend()
            self.assertIs(eth_hash_keccak.hasher, native.eth_hash_backend_hasher)
            self.assertIs(eth_hash_keccak.preimage, native.eth_hash_backend_preimage)
            self.assertEqual(eth_utils.keccak(data), keccak_256(data).digest())
            self.assertNotIsInstance(
                eth_hash_keccak.new(data), native.NativeKeccakPreimage
            )
            self.assertEqual(
                eth_hash_keccak.new(data).digest(), keccak_256(data).digest()
            )
        finally:
            native.use_native_keccak_in_eth_hash()
        self.assertIs(eth_hash_keccak.hasher, native.safe_eth_native.keccak256)
        self.assertIs(eth_hash_keccak.preimage, native.NativeKeccakPreimage)
