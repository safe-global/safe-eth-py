import hashlib
import os
import unittest
from concurrent.futures import ThreadPoolExecutor

import safe_eth_native
from Crypto.PublicKey import ECC
from native_test_helpers import (
    build_p256_signatures,
    load_wycheproof_ecdsa_tests,
    sign_p256_digest,
)

P256_P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
P256_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
P256_GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
P256_GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

# RFC 6979 appendix A.2.5 (P-256, SHA-256)
RFC_6979_PUBLIC_KEY_X = (
    0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6
)
RFC_6979_PUBLIC_KEY_Y = (
    0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299
)
RFC_6979_SIGNATURES = [
    (
        b"sample",
        0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716,
        0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8,
    ),
    (
        b"test",
        0xF1ABB023518351CD71D881567B1EA663ED3EFCF6C5132B354F28D3B0B7D38367,
        0x019F4113742A2B14BD25926B49C649155F267E60D3814B4C0CC84250E46F0083,
    ),
]


class TestP256Verify(unittest.TestCase):
    def test_rfc_6979_vectors(self):
        """RFC 6979 signatures verify, also in high `s` form, and only for their own message"""
        for message, r, s in RFC_6979_SIGNATURES:
            with self.subTest(message=message):
                message_hash = int.from_bytes(hashlib.sha256(message).digest(), "big")
                self.assertTrue(
                    safe_eth_native.p256_verify(
                        message_hash, r, s, RFC_6979_PUBLIC_KEY_X, RFC_6979_PUBLIC_KEY_Y
                    )
                )
                # The high `s` form is accepted, the precompile has no low `s` rule
                self.assertTrue(
                    safe_eth_native.p256_verify(
                        message_hash,
                        r,
                        P256_N - s,
                        RFC_6979_PUBLIC_KEY_X,
                        RFC_6979_PUBLIC_KEY_Y,
                    )
                )
        # One message with the signature of the other one
        message_hash = int.from_bytes(hashlib.sha256(b"test").digest(), "big")
        _, r, s = RFC_6979_SIGNATURES[0]
        self.assertFalse(
            safe_eth_native.p256_verify(
                message_hash, r, s, RFC_6979_PUBLIC_KEY_X, RFC_6979_PUBLIC_KEY_Y
            )
        )

    def test_wycheproof_vectors(self):
        """Wycheproof ECDSA verification vectors, with SHA-256 and SHA-512"""
        tested_signature_count = 0
        for file_name in (
            "ecdsa_secp256r1_sha256_p1363_test.json",
            "ecdsa_secp256r1_sha512_p1363_test.json",
        ):
            for test in load_wycheproof_ecdsa_tests(file_name):
                # IEEE P1363 signatures of another size cannot be split into `r` and `s`
                if len(test.signature) != 64:
                    continue
                tested_signature_count += 1
                with self.subTest(file=file_name, test_id=test.test_id):
                    self.assertEqual(
                        safe_eth_native.p256_verify(
                            int.from_bytes(test.message_digest, "big"),
                            int.from_bytes(test.signature[:32], "big"),
                            int.from_bytes(test.signature[32:], "big"),
                            test.public_key_x,
                            test.public_key_y,
                        ),
                        test.is_valid,
                    )
        self.assertGreater(tested_signature_count, 500)

    def test_random_signatures(self):
        """pycryptodome signatures verify, in low and high `s` form, and any change breaks them"""
        for message_hash, r, s, public_key_x, public_key_y in build_p256_signatures(
            100
        ):
            self.assertTrue(
                safe_eth_native.p256_verify(
                    message_hash, r, s, public_key_x, public_key_y
                )
            )
            self.assertTrue(
                safe_eth_native.p256_verify(
                    message_hash, r, P256_N - s, public_key_x, public_key_y
                )
            )
            for changed_values in (
                (message_hash ^ 1, r, s, public_key_x, public_key_y),
                (message_hash, r ^ 1, s, public_key_x, public_key_y),
                (message_hash, r, s ^ 1, public_key_x, public_key_y),
                (message_hash, s, r, public_key_x, public_key_y),
                # The negated public key is on the curve, but it is another key
                (message_hash, r, s, public_key_x, P256_P - public_key_y),
            ):
                self.assertFalse(safe_eth_native.p256_verify(*changed_values))

    def test_message_hash_above_curve_order(self):
        """
        The hash is used as an integer modulo n, so a hash above n verifies the
        signature of the hash minus n, like the precompile
        """
        private_key = ECC.generate(curve="P-256")
        public_key_x, public_key_y = (
            int(private_key.pointQ.x),
            int(private_key.pointQ.y),
        )
        for message_hash in (P256_N, P256_N + 1, 2**256 - 1, P256_N + 12345):
            with self.subTest(message_hash=message_hash):
                r, s = sign_p256_digest(
                    private_key, (message_hash - P256_N).to_bytes(32, "big")
                )
                self.assertTrue(
                    safe_eth_native.p256_verify(
                        message_hash, r, s, public_key_x, public_key_y
                    )
                )
                self.assertTrue(
                    safe_eth_native.p256_verify(
                        message_hash - P256_N, r, s, public_key_x, public_key_y
                    )
                )

    def test_message_hash_zero(self):
        """A hash of zero is a valid input"""
        private_key = ECC.generate(curve="P-256")
        r, s = sign_p256_digest(private_key, bytes(32))
        self.assertTrue(
            safe_eth_native.p256_verify(
                0, r, s, int(private_key.pointQ.x), int(private_key.pointQ.y)
            )
        )

    def test_generator_as_public_key(self):
        """The generator is the public key of the private key 1"""
        private_key = ECC.construct(curve="P-256", d=1)
        digest = os.urandom(32)
        r, s = sign_p256_digest(private_key, digest)
        self.assertTrue(
            safe_eth_native.p256_verify(
                int.from_bytes(digest, "big"), r, s, P256_GX, P256_GY
            )
        )

    def test_invalid_public_keys(self):
        """Public keys that are not a point on the curve never verify"""
        message_hash, r, s, public_key_x, public_key_y = build_p256_signatures(1)[0]
        for invalid_x, invalid_y in (
            (0, 0),
            (public_key_x, public_key_y + 1),
            (public_key_x + 1, public_key_y),
            (public_key_x + P256_P, public_key_y),
            (public_key_x, public_key_y + P256_P),
            (P256_P, public_key_y),
            (public_key_x, P256_P),
            (2**256 - 1, 2**256 - 1),
            (2**256 + public_key_x, public_key_y),
            (-public_key_x, public_key_y),
            (public_key_x, -1),
        ):
            with self.subTest(public_key_x=invalid_x, public_key_y=invalid_y):
                self.assertFalse(
                    safe_eth_native.p256_verify(
                        message_hash, r, s, invalid_x, invalid_y
                    )
                )

    def test_signature_values_out_of_range(self):
        """`r` and `s` must be in [1, n - 1]"""
        message_hash, r, s, public_key_x, public_key_y = build_p256_signatures(1)[0]
        for invalid_r, invalid_s in (
            (0, s),
            (r, 0),
            (0, 0),
            (P256_N, s),
            (r, P256_N),
            (r + P256_N, s),
            (r, s + P256_N),
            (2**256 - 1, s),
            (r, 2**256 - 1),
            (2**256, s),
            (r, 2**256),
            (-r, s),
            (r, -s),
        ):
            with self.subTest(r=invalid_r, s=invalid_s):
                self.assertFalse(
                    safe_eth_native.p256_verify(
                        message_hash, invalid_r, invalid_s, public_key_x, public_key_y
                    )
                )

    def test_message_hash_out_of_range(self):
        """The precompile takes a 32 bytes hash: negative values or values of more bits never verify"""
        message_hash, r, s, public_key_x, public_key_y = build_p256_signatures(1)[0]
        for invalid_message_hash in (-message_hash, -1, message_hash + 2**256, 2**512):
            with self.subTest(message_hash=invalid_message_hash):
                self.assertFalse(
                    safe_eth_native.p256_verify(
                        invalid_message_hash, r, s, public_key_x, public_key_y
                    )
                )

    def test_other_types(self):
        """Values that are not `int` raise `TypeError`"""
        message_hash, r, s, public_key_x, public_key_y = build_p256_signatures(1)[0]
        values = [message_hash, r, s, public_key_x, public_key_y]
        for position in range(len(values)):
            for invalid_value in (
                float(values[position]),
                values[position].to_bytes(32, "big"),
                str(values[position]),
                None,
            ):
                invalid_values = list(values)
                invalid_values[position] = invalid_value
                with self.subTest(position=position, value=invalid_value):
                    with self.assertRaises(TypeError):
                        safe_eth_native.p256_verify(*invalid_values)

    def test_threads(self):
        """Verifying from several threads at once, as the GIL is released while verifying"""
        signatures = build_p256_signatures(50) * 4
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(
                executor.map(
                    lambda signature: safe_eth_native.p256_verify(*signature),
                    signatures,
                )
            )
        self.assertEqual(results, [True] * len(signatures))
