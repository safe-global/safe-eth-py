import hashlib
import unittest

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
    def test_verify_valid_signatures(self):
        self.assertTrue(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertTrue(
            p256.verify(TEST_HASH, TEST_R, TEST_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    def test_verify_wrong_message(self):
        # `sample` signature against `test` digest must not verify
        self.assertFalse(
            p256.verify(TEST_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    def test_verify_tampered_signature(self):
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R + 1, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S + 1, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    def test_verify_wrong_public_key(self):
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X + 1, PUBLIC_KEY_Y)
        )

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

    def test_verify_public_key_not_on_curve(self):
        self.assertFalse(p256._is_on_curve(PUBLIC_KEY_X, PUBLIC_KEY_Y + 1))
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y + 1)
        )

    def test_generator_on_curve(self):
        self.assertTrue(p256._is_on_curve(p256._GX, p256._GY))


if __name__ == "__main__":
    unittest.main()
