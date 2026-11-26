import hashlib
import unittest
from decimal import Decimal

from .. import p256

# These tests check what `p256.verify` adds to the native function: the integer conversion and
# the message hash modulo n

P256_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

# Known-answer vector from RFC 6979 Appendix A.2.5 (NIST P-256, SHA-256), message "sample"
# https://datatracker.ietf.org/doc/html/rfc6979#appendix-A.2.5
PUBLIC_KEY_X = 0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6
PUBLIC_KEY_Y = 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299
SAMPLE_HASH = int.from_bytes(hashlib.sha256(b"sample").digest(), "big")
SAMPLE_R = 0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716
SAMPLE_S = 0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8
SAMPLE_VALUES = (SAMPLE_HASH, SAMPLE_R, SAMPLE_S, PUBLIC_KEY_X, PUBLIC_KEY_Y)


class TestP256(unittest.TestCase):
    def test_verify(self):
        """The RFC 6979 signature verifies, and not with a changed `s`"""
        self.assertTrue(p256.verify(*SAMPLE_VALUES))
        self.assertFalse(
            p256.verify(SAMPLE_HASH, SAMPLE_R, SAMPLE_S + 1, PUBLIC_KEY_X, PUBLIC_KEY_Y)
        )

    def test_verify_message_hash_modulo_n(self):
        """Only the message hash modulo n is used, as by the precompile"""
        for message_hash, is_valid in (
            (SAMPLE_HASH + P256_N, True),
            (SAMPLE_HASH - P256_N, True),
            (SAMPLE_HASH - 5 * P256_N, True),
            (SAMPLE_HASH + 2**256, False),
            (-SAMPLE_HASH, False),
        ):
            with self.subTest(message_hash=message_hash):
                self.assertEqual(
                    p256.verify(message_hash, *SAMPLE_VALUES[1:]), is_valid
                )

    def test_verify_integer_like_values(self):
        """
        `int` subclasses and objects with `__index__` are used as their integer value. An
        overridden `__mod__` is not used for the message hash
        """

        class IntWithModulo(int):
            def __mod__(self, other):
                return 0

        class IndexOnly:
            def __init__(self, value: int):
                self.value = value

            def __index__(self) -> int:
                return self.value

        self.assertTrue(p256.verify(IntWithModulo(SAMPLE_HASH), *SAMPLE_VALUES[1:]))
        self.assertTrue(p256.verify(*(IndexOnly(value) for value in SAMPLE_VALUES)))

    def test_verify_values_that_are_not_integers(self):
        """Values that are not integers raise `TypeError`, in any position"""
        for position, value in enumerate(SAMPLE_VALUES):
            for not_integer_value in (float(value), Decimal(value), str(value)):
                values = list(SAMPLE_VALUES)
                values[position] = not_integer_value
                with self.subTest(position=position, value=not_integer_value):
                    with self.assertRaises(TypeError):
                        p256.verify(*values)


if __name__ == "__main__":
    unittest.main()
