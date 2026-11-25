import hashlib
import json
import os
import unittest
from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from ...util.tests.native_test_utils import (
    assert_same_outcome_with_and_without_native,
    with_and_without_native,
)
from .. import p256

# Known-answer vectors from RFC 6979 Appendix A.2.5 (NIST P-256, SHA-256).
# https://datatracker.ietf.org/doc/html/rfc6979#appendix-A.2.5
PUBLIC_KEY_X = 0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6
PUBLIC_KEY_Y = 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299

# message "sample"
SAMPLE_HASH = int.from_bytes(hashlib.sha256(b"sample").digest(), "big")
SAMPLE_R = 0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716
SAMPLE_S = 0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8

# message "test"
TEST_HASH = int.from_bytes(hashlib.sha256(b"test").digest(), "big")
TEST_R = 0xF1ABB023518351CD71D881567B1EA663ED3EFCF6C5132B354F28D3B0B7D38367
TEST_S = 0x019F4113742A2B14BD25926B49C649155F267E60D3814B4C0CC84250E46F0083


class TestP256(unittest.TestCase):
    @with_and_without_native
    def test_verify_valid_signatures(self):
        self.assertTrue(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertTrue(
            p256.verify(TEST_HASH, TEST_R, TEST_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    @with_and_without_native
    def test_verify_wrong_message(self):
        # `sample` signature against `test` digest must not verify
        self.assertFalse(
            p256.verify(TEST_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    @with_and_without_native
    def test_verify_tampered_signature(self):
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R + 1, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S + 1, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    @with_and_without_native
    def test_verify_wrong_public_key(self):
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X + 1, PUBLIC_KEY_Y)
        )

    @with_and_without_native
    def test_verify_signature_out_of_range(self):
        # `r` and `s` must be in [1, n-1]
        self.assertFalse(
            p256.verify(SAMPLE_HASH, 0, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, 0, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertFalse(
            p256.verify(SAMPLE_HASH, p256._N, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, p256._N, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    @with_and_without_native
    def test_verify_public_key_not_on_curve(self):
        self.assertFalse(p256._is_on_curve(PUBLIC_KEY_X, PUBLIC_KEY_Y + 1))
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y + 1)
        )

    def test_generator_on_curve(self):
        self.assertTrue(p256._is_on_curve(p256._GX, p256._GY))


# Wycheproof vectors of the native extension tests, not in the safe-eth-py package
WYCHEPROOF_P256_VECTORS = (
    Path(__file__).parents[3]
    / "native"
    / "tests"
    / "vectors"
    / "ecdsa_secp256r1_sha256_p1363_test.json"
)


class TestP256VerifyWithAndWithoutNative(unittest.TestCase):
    """The native extension and the Python implementation give the same result"""

    def test_random_signatures(self):
        """Valid, high `s` and changed signatures, and hashes out of the 32 bytes range"""
        for _ in range(20):
            private_key = ECC.generate(curve="P-256")
            message_digest = SHA256.new(os.urandom(32))
            signature = DSS.new(private_key, "fips-186-3").sign(message_digest)
            message_hash = int.from_bytes(message_digest.digest(), "big")
            r = int.from_bytes(signature[:32], "big")
            s = int.from_bytes(signature[32:], "big")
            public_key_x = int(private_key.pointQ.x)
            public_key_y = int(private_key.pointQ.y)
            self.assertTrue(p256.verify(message_hash, r, s, public_key_x, public_key_y))
            for values in (
                (message_hash, r, s, public_key_x, public_key_y),
                (message_hash, r, p256._N - s, public_key_x, public_key_y),
                (message_hash ^ 1, r, s, public_key_x, public_key_y),
                (message_hash, r ^ 1, s, public_key_x, public_key_y),
                (message_hash, r, s, public_key_x, p256._P - public_key_y),
                (message_hash + p256._N, r, s, public_key_x, public_key_y),
                (message_hash + 2**256, r, s, public_key_x, public_key_y),
                (-message_hash, r, s, public_key_x, public_key_y),
            ):
                assert_same_outcome_with_and_without_native(self, p256.verify, *values)

    def test_invalid_values(self):
        """Values out of range and public keys that are not on the curve"""
        for r, s, public_key_x, public_key_y in (
            (0, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (SAMPLE_R, 0, PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (p256._N, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (SAMPLE_R, p256._N, PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (SAMPLE_R + 2**256, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (-SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (SAMPLE_R, SAMPLE_S, 0, 0),
            (SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X + p256._P, PUBLIC_KEY_Y),
            (SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y + p256._P),
            (SAMPLE_R, SAMPLE_S, -PUBLIC_KEY_X, PUBLIC_KEY_Y),
            (SAMPLE_R, SAMPLE_S, p256._GX, p256._GY),
        ):
            with self.subTest(r=r, s=s, public_key_x=public_key_x):
                assert_same_outcome_with_and_without_native(
                    self, p256.verify, SAMPLE_HASH, r, s, public_key_x, public_key_y
                )

    def test_values_that_are_not_int(self):
        """Values that are not exactly `int` go to the Python implementation"""
        values = [SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y]
        for position in range(len(values)):
            for not_int_value in (float(values[position]), str(values[position]), True):
                not_int_values = list(values)
                not_int_values[position] = not_int_value
                with self.subTest(position=position, value=not_int_value):
                    assert_same_outcome_with_and_without_native(
                        self, p256.verify, *not_int_values
                    )

    def test_wycheproof_vectors(self):
        """Wycheproof P-256 SHA-256 vectors, which the Python implementation also has to pass"""
        if not WYCHEPROOF_P256_VECTORS.exists():
            self.skipTest(
                "The vectors are in the repository, not in the safe-eth-py package"
            )
        test_data = json.loads(WYCHEPROOF_P256_VECTORS.read_text())
        for test_group in test_data["testGroups"]:
            public_key_x = int(test_group["publicKey"]["wx"], 16)
            public_key_y = int(test_group["publicKey"]["wy"], 16)
            for test in test_group["tests"]:
                signature = bytes.fromhex(test["sig"])
                if len(signature) != 64:
                    continue
                message_hash = int.from_bytes(
                    hashlib.sha256(bytes.fromhex(test["msg"])).digest(), "big"
                )
                r = int.from_bytes(signature[:32], "big")
                s = int.from_bytes(signature[32:], "big")
                with self.subTest(test_id=test["tcId"]):
                    self.assertEqual(
                        p256.verify(message_hash, r, s, public_key_x, public_key_y),
                        test["result"] == "valid",
                    )
                    assert_same_outcome_with_and_without_native(
                        self,
                        p256.verify,
                        message_hash,
                        r,
                        s,
                        public_key_x,
                        public_key_y,
                    )


if __name__ == "__main__":
    unittest.main()
