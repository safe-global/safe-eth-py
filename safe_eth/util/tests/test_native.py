import os
import subprocess
import sys
from unittest import TestCase, mock

import eth_utils
from eth_hash.auto import keccak as eth_hash_keccak

from safe_eth.util import native

from .native_test_utils import eth_hash_backend, reference_keccak256


class TestNativeKeccakInEthHash(TestCase):
    def test_eth_hash_uses_native_keccak(self):
        """Importing safe-eth-py makes the native keccak256 the eth-hash one, `new()` included"""
        self.assertIs(eth_hash_keccak.hasher, native.safe_eth_native.keccak256)
        self.assertIs(eth_hash_keccak.preimage, native.NativeKeccakPreimage)
        self.assertIsInstance(eth_hash_keccak.new(b""), native.NativeKeccakPreimage)

    def test_import_safe_eth_uses_native_keccak(self):
        """A bare `import safe_eth`, with no submodule, makes the native keccak256 the eth-hash one"""
        check_code = (
            "import safe_eth, safe_eth_native\n"
            "from eth_hash.auto import keccak\n"
            "assert keccak.hasher is safe_eth_native.keccak256\n"
            "assert keccak.preimage.__name__ == 'NativeKeccakPreimage'\n"
        )
        environment = {
            key: value for key, value in os.environ.items() if key != "ETH_HASH_BACKEND"
        }
        subprocess.run([sys.executable, "-c", check_code], check=True, env=environment)

    def test_import_safe_eth_with_eth_hash_backend_env(self):
        """
        `import safe_eth` fails if the backend in `ETH_HASH_BACKEND` is not installed,
        instead of the first hash, and works with one that is installed
        """
        environment = dict(os.environ)
        for eth_hash_backend_name, check_code in (
            ("pysha3", "import safe_eth"),
            (
                "pycryptodome",
                "import safe_eth, safe_eth_native\n"
                "from eth_hash.auto import keccak\n"
                "assert keccak.hasher is not safe_eth_native.keccak256\n",
            ),
        ):
            environment["ETH_HASH_BACKEND"] = eth_hash_backend_name
            with self.subTest(eth_hash_backend_name=eth_hash_backend_name):
                process = subprocess.run(
                    [sys.executable, "-c", check_code],
                    env=environment,
                    capture_output=True,
                    text=True,
                )
                if eth_hash_backend_name == "pysha3":
                    self.assertNotEqual(process.returncode, 0)
                    self.assertIn(
                        "ImportError: The backend specified in ETH_HASH_BACKEND, "
                        "'pysha3', is not installed",
                        process.stderr,
                    )
                else:
                    self.assertEqual(process.returncode, 0, process.stderr)

    def test_wrong_native_keccak256_fails(self):
        """A native keccak256 with wrong digests raises, so `import safe_eth` fails"""
        native.check_native_keccak256()
        with mock.patch.object(
            native.safe_eth_native, "keccak256", return_value=bytes(32)
        ):
            with self.assertRaisesRegex(
                ImportError, "safe-eth-native keccak256 returns wrong digests"
            ):
                native.check_native_keccak256()

    def test_eth_hash_new_same_digests_as_pycryptodome(self):
        """
        `keccak.new()` gives the pycryptodome digests after each update, for `bytes`,
        `bytearray` and `memoryview`, and its copies are independent
        """
        first_part, second_part, third_part = (
            os.urandom(length) for length in (0, 137, 3000)
        )
        preimage = eth_hash_keccak.new(bytearray(first_part))
        hashed_data = first_part
        self.assertEqual(preimage.digest(), reference_keccak256(hashed_data))
        for part in (second_part, bytearray(third_part), memoryview(second_part)):
            preimage.update(part)
            hashed_data += part
            self.assertEqual(preimage.digest(), reference_keccak256(hashed_data))
        preimage_copy = preimage.copy()
        preimage_copy.update(b"only in the copy")
        self.assertEqual(preimage.digest(), reference_keccak256(hashed_data))
        self.assertEqual(
            preimage_copy.digest(),
            reference_keccak256(hashed_data + b"only in the copy"),
        )
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

    def test_same_digests_as_pycryptodome(self):
        """eth-hash and eth-utils give the pycryptodome digests for `bytes`, `bytearray` and hex input"""
        for length in (0, 1, 32, 136, 1000, 5000):
            data = os.urandom(length)
            expected_digest = reference_keccak256(data)
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
        `ETH_HASH_BACKEND` leaves the eth-hash backend as it is, and it hashes once so
        eth-hash loads its backend
        """
        with (
            mock.patch.object(eth_hash_keccak, "hasher") as hasher,
            mock.patch.object(eth_hash_keccak, "preimage") as preimage,
            mock.patch.dict(os.environ, {"ETH_HASH_BACKEND": "pycryptodome"}),
        ):
            native.use_native_keccak_in_eth_hash()
            self.assertIs(eth_hash_keccak.hasher, hasher)
            self.assertIs(eth_hash_keccak.preimage, preimage)
            hasher.assert_called_once_with(b"")
        # Without `ETH_HASH_BACKEND` they are replaced, so the check above can fail
        with (
            mock.patch.object(eth_hash_keccak, "hasher"),
            mock.patch.object(eth_hash_keccak, "preimage"),
        ):
            native.use_native_keccak_in_eth_hash()
            self.assertIs(eth_hash_keccak.hasher, native.safe_eth_native.keccak256)
            self.assertIs(eth_hash_keccak.preimage, native.NativeKeccakPreimage)

    def test_eth_hash_backend(self):
        """
        `eth_hash_backend()`, used to run the test references without the native
        extension, makes eth-hash use its own backend, with the same digests
        """
        data = os.urandom(100)
        with eth_hash_backend():
            self.assertIs(eth_hash_keccak.hasher, native.eth_hash_backend_hasher)
            self.assertIs(eth_hash_keccak.preimage, native.eth_hash_backend_preimage)
            self.assertEqual(eth_utils.keccak(data), reference_keccak256(data))
            self.assertNotIsInstance(
                eth_hash_keccak.new(data), native.NativeKeccakPreimage
            )
            self.assertEqual(
                eth_hash_keccak.new(data).digest(), reference_keccak256(data)
            )
        self.assertIs(eth_hash_keccak.hasher, native.safe_eth_native.keccak256)
        self.assertIs(eth_hash_keccak.preimage, native.NativeKeccakPreimage)
