import hashlib
import os
import random
import unittest
from concurrent.futures import ThreadPoolExecutor

import safe_eth_native
from native_test_helpers import (
    NATIVE_KEYS,
    SECP256K1_N,
    BytesSubclass,
    address_from_public_key,
    build_secp256k1_signatures,
    load_wycheproof_ecdsa_tests,
    reference_keccak256,
)

SECP256K1_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP256K1_GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798

# go-ethereum `core/vm/testdata/precompiles/ecRecover.json`, `ValidKey`
GETH_MESSAGE_HASH = bytes.fromhex(
    "18c547e4f7b0f325ad1e56f57e26c745b09a3e503d86e00e5255ff7f715d3d1c"
)
GETH_V = 28
GETH_R = 0x73B1693892219D736CABA55BDB67216E485557EA6B6AF75F37096C9AA6A5A75F
GETH_S = 0xEEB940B1D03B21E36B0E47E79769F095FE2AB855BD91E3A38756B7D75A9C4549
GETH_SIGNER = bytes.fromhex("a94f5374fce5edbc8e2a8697c15331677e6ebf0b")

# eth-keys `tests/backends/conftest.py`: keccak256(b"message") signed by known keys
ETH_KEYS_MESSAGE_HASH = reference_keccak256(b"message")
ETH_KEYS_SIGNATURES = [
    (
        "5eed5fa3a67696c334762bb4823e585e2ee579aba3558d9955296d6c04541b426078dbd48d74af1fd0c72aa1a05147cf17be6b60bdbed6ba19b08ec28445b0ca",
        1,
        80536744857756143861726945576089915884233437828013729338039544043241440681784,
        1902566422691403459035240420865094128779958320521066670269403689808757640701,
    ),
    (
        "347746ccb908e583927285fa4bd202f08e2f82f09c920233d89c47c79e48f937d049130e3d1c14cf7b21afefc057f71da73dec8e8ff74ff47dc6a574ccd5d570",
        1,
        41741612198399299636429810387160790514780876799439767175315078161978521003886,
        47545396818609319588074484786899049290652725314938191835667190243225814114102,
    ),
]

# coincurve `tests/conftest.py`: sha256 of `MESSAGE` signed by `PRIVATE_KEY_BYTES`
COINCURVE_MESSAGE = (
    b"\xdfw\xeb)\t2R8\xda5\x02\xadE\xdd\xce\xd2\xe0\xb4\xf1\x81\xe7\xdf"
    b":\xce\x82m\xcf\x99\xf3o\x9d\xe6\xfb\xe4\x98O\x88\xcfh\xbe\xfd\xc2"
    b"{\xafm\xb3\xff\xb4QR\xffPu$\xfc>A'\x03t\xc5\xf9\xd8\xf3I,\xaa\"*"
    b"\xd7q\xfe\xb7]\x11\xa9uB'd\x89\x03'3\xb8/\x80\xa2#\x00\xa2\xfe"
    b"\xff\xae\xb0\x86\xc1/ o\xc8]?\xa05L\xff8\x8az\x92\xc9\xab\x9fg0|"
    b'\\5\x98\xfaG\x9b#\xec\x1a\xc5\x10\xd6\x08\x9c:\x01"\x0c\x812O/i'
    b'\xc4WI\x0c\r\xd8\x81-m1_\x14]$\xf8\x16\xef\x1e\x1d\xb0"Q\x1a\xcf'
    b'`R\xae\x0c"r2\x9a\xa3\xdb\xc4W}<c\xd8\x0e\xb5\x96\x99\x87\xdeU'
    b"\x84\x1a?No\x10T\xf8\xb8\xd3\x18\xa4\xaf"
)
COINCURVE_RECOVERABLE_SIGNATURE = (
    b"\xee$\x1b\x0e@fa\xd4<\x17)\xa7\n\xd0\xd7\xef\x90\xcd\x13"
    b"\xad`\xc1\x06[\xe0\x821\x96\xe29\x80'\r\x02\x13\xd2\xaf?"
    b"\x92G\x80&8\x1cVz%2\xb0\x8a\xd0l\x0b4\x9c~\x93\x18\xad"
    b"\xe4J\x9c-\n\x00"
)
COINCURVE_PUBLIC_KEY_X = (
    27753912938952041417634381842191885283234814940840273460372041880794577257268
)
COINCURVE_PUBLIC_KEY_Y = (
    53663045980837260634637807506183816949039230809110041985901491152185762425315
)

# libsecp256k1 `src/modules/recovery/tests_impl.h`, `test_ecdsa_recovery_edge_cases`
LIBSECP256K1_MESSAGE_HASH = b"This is a very secret message..."
# Signed with the invalid secret key 0, it only recovers with recovery id 1
LIBSECP256K1_SECRET_ZERO_SIGNATURE = bytes.fromhex(
    "67cb285f9cd194e840d629397af5569662fde44649995963179a7dd17bd23532"
    "4b1b7df34ce1f68e694ff6f11ac751dd7dd73e387ee4fc866e1be8ecc7dd9557"
)


def eth_keys_recover(message_hash: bytes, v: int, r: int, s: int) -> bytes | None:
    """eth-keys pure Python backend, `None` when it rejects the signature"""
    try:
        signature = NATIVE_KEYS.Signature(vrs=(v - 27, r, s))
        public_key = NATIVE_KEYS.ecdsa_recover(message_hash, signature)
    except Exception:
        return None
    return address_from_public_key(public_key.to_bytes())


class TestEcrecover(unittest.TestCase):
    def test_geth_precompile_vectors(self):
        """go-ethereum ecrecover precompile vectors"""
        self.assertEqual(
            safe_eth_native.ecrecover(GETH_MESSAGE_HASH, GETH_V, GETH_R, GETH_S),
            GETH_SIGNER,
        )
        # `CallEcrecoverUnrecoverableKey`: `r` is in range, but there is no valid point
        self.assertIsNone(
            safe_eth_native.ecrecover(
                bytes.fromhex(
                    "a8b53bdf3306a35a7103ab5504a0c9b492295564b6202b1942a84ef300107281"
                ),
                27,
                0x3078356531653033663533636531386237373263636230303933666637316633,
                0x6635336635633735623734646362333161383561613862383839326234653862,
            )
        )
        # `InvalidHighV-bits-*`: `v` is 28 in its lowest bits only
        for invalid_v in (
            (1 << 252) + GETH_V,
            (1 << 100) + GETH_V,
            (1 << 100) + (1 << 8) + GETH_V,
        ):
            self.assertIsNone(
                safe_eth_native.ecrecover(GETH_MESSAGE_HASH, invalid_v, GETH_R, GETH_S)
            )

    def test_eth_keys_vectors(self):
        """eth-keys backend fixtures, signatures of known keys"""
        for public_key_hex, recovery_id, r, s in ETH_KEYS_SIGNATURES:
            expected_signer = address_from_public_key(bytes.fromhex(public_key_hex))
            self.assertEqual(
                safe_eth_native.ecrecover(
                    ETH_KEYS_MESSAGE_HASH, recovery_id + 27, r, s
                ),
                expected_signer,
            )

    def test_eth_keys_point_at_infinity_vectors(self):
        """eth-keys vectors (from ethereum/tests) where the recovered point is the point at infinity"""
        for message_hash, v, r, s in (
            (
                bytes.fromhex(
                    "6b8d2c81b11b2d699528dde488dbdf2f94293d0d33c32e347f255fa4a6c1f0a9"
                ),
                27,
                SECP256K1_GX,
                0x6B8D2C81B11B2D699528DDE488DBDF2F94293D0D33C32E347F255FA4A6C1F0A9,
            ),
            (
                bytes.fromhex(
                    "1476abb745d423bf09273f1afd887d951181d25adc66c4834a70491911b7f750"
                ),
                28,
                29836180350949573232951565573845061551093497675544587026406064656720118638890,
                36811185137926304485684021052401800813557229270017380070056792973957337676018,
            ),
        ):
            with self.subTest(message_hash=message_hash.hex()):
                self.assertIsNone(eth_keys_recover(message_hash, v, r, s))
                self.assertIsNone(safe_eth_native.ecrecover(message_hash, v, r, s))

    def test_coincurve_vector(self):
        """coincurve sample recoverable signature, over the sha256 of the message"""
        r = int.from_bytes(COINCURVE_RECOVERABLE_SIGNATURE[:32], "big")
        s = int.from_bytes(COINCURVE_RECOVERABLE_SIGNATURE[32:64], "big")
        v = COINCURVE_RECOVERABLE_SIGNATURE[64] + 27
        self.assertEqual(
            safe_eth_native.ecrecover(
                hashlib.sha256(COINCURVE_MESSAGE).digest(), v, r, s
            ),
            address_from_public_key(
                COINCURVE_PUBLIC_KEY_X.to_bytes(32, "big")
                + COINCURVE_PUBLIC_KEY_Y.to_bytes(32, "big")
            ),
        )

    def test_libsecp256k1_edge_cases(self):
        """libsecp256k1 recovery edge cases, for the 2 recovery ids Ethereum uses"""
        r = int.from_bytes(LIBSECP256K1_SECRET_ZERO_SIGNATURE[:32], "big")
        s = int.from_bytes(LIBSECP256K1_SECRET_ZERO_SIGNATURE[32:], "big")
        self.assertIsNone(
            safe_eth_native.ecrecover(LIBSECP256K1_MESSAGE_HASH, 27, r, s)
        )
        recovered_signer = safe_eth_native.ecrecover(
            LIBSECP256K1_MESSAGE_HASH, 28, r, s
        )
        self.assertIsNotNone(recovered_signer)
        self.assertEqual(
            recovered_signer, eth_keys_recover(LIBSECP256K1_MESSAGE_HASH, 28, r, s)
        )

        # (r, s) = (4, 4) and (1, 1) recover with every recovery id
        for small_value in (1, 4):
            for v in (27, 28):
                with self.subTest(r=small_value, s=small_value, v=v):
                    recovered_signer = safe_eth_native.ecrecover(
                        LIBSECP256K1_MESSAGE_HASH, v, small_value, small_value
                    )
                    self.assertIsNotNone(recovered_signer)
                    self.assertEqual(
                        recovered_signer,
                        eth_keys_recover(
                            LIBSECP256K1_MESSAGE_HASH, v, small_value, small_value
                        ),
                    )

        # (0, 1) and (1, 0) do not recover
        for r, s in ((0, 1), (1, 0)):
            for v in (27, 28):
                with self.subTest(r=r, s=s, v=v):
                    self.assertIsNone(
                        safe_eth_native.ecrecover(LIBSECP256K1_MESSAGE_HASH, v, r, s)
                    )

    def test_wycheproof_vectors(self):
        """
        Wycheproof ECDSA verification vectors, with SHA-256 and SHA-512. A signature is
        valid for a public key if and only if recovering it with the right `v` gives that
        public key. The only exception are valid signatures with `x(R) = r + n`, which
        need recovery ids 2 or 3, and the EVM `ecrecover` only takes `v` 27 or 28.
        """
        tested_signature_count = 0
        for file_name in (
            "ecdsa_secp256k1_sha256_p1363_test.json",
            "ecdsa_secp256k1_sha512_p1363_test.json",
        ):
            for test in load_wycheproof_ecdsa_tests(file_name):
                # IEEE P1363 signatures of another size cannot be split into `r` and `s`
                if len(test.signature) != 64:
                    continue
                tested_signature_count += 1
                r = int.from_bytes(test.signature[:32], "big")
                s = int.from_bytes(test.signature[32:], "big")
                expected_signer = address_from_public_key(
                    test.public_key_x.to_bytes(32, "big")
                    + test.public_key_y.to_bytes(32, "big")
                )
                recovered_signers = {
                    safe_eth_native.ecrecover(test.message_digest, v, r, s)
                    for v in (27, 28)
                }
                with self.subTest(file=file_name, test_id=test.test_id):
                    if not (1 <= r < SECP256K1_N and 1 <= s < SECP256K1_N):
                        self.assertFalse(test.is_valid)
                        self.assertEqual(recovered_signers, {None})
                    elif test.is_valid and expected_signer not in recovered_signers:
                        self.assertLess(r, SECP256K1_P - SECP256K1_N)
                    else:
                        self.assertEqual(
                            expected_signer in recovered_signers, test.is_valid
                        )
        self.assertGreater(tested_signature_count, 500)

    def test_random_signatures(self):
        """Low `s` and high `s` signatures recover the signer, and the other `v` gives the eth-keys address"""
        for message_hash, v, r, s, signer in build_secp256k1_signatures(50):
            self.assertEqual(safe_eth_native.ecrecover(message_hash, v, r, s), signer)
            # The other `v` gives another address
            other_signer = safe_eth_native.ecrecover(message_hash, 55 - v, r, s)
            self.assertNotEqual(other_signer, signer)
            self.assertEqual(other_signer, eth_keys_recover(message_hash, 55 - v, r, s))
            # Another message gives another address
            self.assertNotEqual(
                safe_eth_native.ecrecover(os.urandom(32), v, r, s), signer
            )

    def test_random_values_match_eth_keys(self):
        """For random `r` and `s` (half of them have no point), both give the same address or no address"""
        for _ in range(300):
            message_hash = os.urandom(32)
            v = random.choice((27, 28))
            r = random.randrange(1, SECP256K1_N)
            s = random.randrange(1, SECP256K1_N)
            self.assertEqual(
                safe_eth_native.ecrecover(message_hash, v, r, s),
                eth_keys_recover(message_hash, v, r, s),
            )

    def test_message_hash_edge_values(self):
        """Hashes of zero, n and above n are reduced modulo n, like eth-keys"""
        _, v, r, s, _ = build_secp256k1_signatures(1)[0]
        for message_hash_int in (
            0,
            1,
            SECP256K1_N - 1,
            SECP256K1_N,
            SECP256K1_N + 1,
            2**256 - 1,
        ):
            message_hash = message_hash_int.to_bytes(32, "big")
            with self.subTest(message_hash=message_hash.hex()):
                self.assertEqual(
                    safe_eth_native.ecrecover(message_hash, v, r, s),
                    eth_keys_recover(message_hash, v, r, s),
                )
        # A hash above n recovers the same address as the hash minus n
        self.assertEqual(
            safe_eth_native.ecrecover((SECP256K1_N + 5).to_bytes(32, "big"), v, r, s),
            safe_eth_native.ecrecover((5).to_bytes(32, "big"), v, r, s),
        )

    def test_invalid_values_return_none(self):
        """Values the EVM precompile rejects return `None` instead of raising"""
        message_hash, v, r, s, _ = build_secp256k1_signatures(1)[0]
        # x = 5 has no point on secp256k1 (5**3 + 7 = 132 is not a square mod p)
        r_without_point = 5
        for invalid_v, invalid_r, invalid_s in [
            (0, r, s),
            (1, r, s),
            (2, r, s),
            (3, r, s),
            (26, r, s),
            (29, r, s),
            (30, r, s),
            (31, r, s),
            (35, r, s),
            (36, r, s),
            (-27, r, s),
            (-1, r, s),
            (2**64 + 27, r, s),
            (2**256 + 27, r, s),
            (v, 0, s),
            (v, r, 0),
            (v, 0, 0),
            (v, SECP256K1_N, s),
            (v, r, SECP256K1_N),
            (v, SECP256K1_N + r, s),
            (v, r, SECP256K1_N + s),
            (v, 2**256 - 1, s),
            (v, r, 2**256 - 1),
            (v, 2**256, s),
            (v, r, 2**256),
            (v, 2**256 + r, s),
            (v, -1, s),
            (v, r, -1),
            (v, -r, s),
            (v, r_without_point, s),
        ]:
            with self.subTest(v=invalid_v, r=invalid_r, s=invalid_s):
                self.assertIsNone(
                    safe_eth_native.ecrecover(
                        message_hash, invalid_v, invalid_r, invalid_s
                    )
                )
                self.assertIsNone(
                    eth_keys_recover(message_hash, invalid_v, invalid_r, invalid_s)
                )

    def test_message_hash_must_be_32_bytes(self):
        """A hash of another length raises `ValueError`, and a value that is not `bytes` raises `TypeError`"""
        message_hash, v, r, s, _ = build_secp256k1_signatures(1)[0]
        for invalid_message_hash in (b"", message_hash[:31], message_hash + b"\x00"):
            with self.subTest(length=len(invalid_message_hash)):
                with self.assertRaises(ValueError):
                    safe_eth_native.ecrecover(invalid_message_hash, v, r, s)
        for invalid_message_hash in (
            message_hash.hex(),
            bytearray(message_hash),
            memoryview(message_hash),
            int.from_bytes(message_hash, "big"),
            None,
        ):
            with self.subTest(message_hash=invalid_message_hash):
                with self.assertRaises(TypeError):
                    safe_eth_native.ecrecover(invalid_message_hash, v, r, s)

    def test_other_types(self):
        """`bytes` subclasses like `HexBytes` are accepted, `v`, `r` and `s` must be `int`"""
        message_hash, v, r, s, signer = build_secp256k1_signatures(1)[0]
        self.assertEqual(
            safe_eth_native.ecrecover(BytesSubclass(message_hash), v, r, s), signer
        )
        for invalid_v, invalid_r, invalid_s in (
            (float(v), r, s),
            (str(v), r, s),
            (None, r, s),
            (v, float(r), s),
            (v, r.to_bytes(32, "big"), s),
            (v, r, None),
        ):
            with self.subTest(v=invalid_v, r=invalid_r, s=invalid_s):
                with self.assertRaises(TypeError):
                    safe_eth_native.ecrecover(
                        message_hash, invalid_v, invalid_r, invalid_s
                    )

    def test_int_subclass_cannot_change_the_conversion(self):
        """`r` and `s` are read as `int`, even when a subclass overrides `to_bytes`"""

        class ZeroBytesInt(int):
            def to_bytes(self, *args, **kwargs):
                return bytes(32)

        message_hash, v, r, s, signer = build_secp256k1_signatures(1)[0]
        self.assertEqual(
            safe_eth_native.ecrecover(
                message_hash, v, ZeroBytesInt(r), ZeroBytesInt(s)
            ),
            signer,
        )

    def test_return_type(self):
        """The signer is 20 `bytes`"""
        message_hash, v, r, s, _ = build_secp256k1_signatures(1)[0]
        signer = safe_eth_native.ecrecover(message_hash, v, r, s)
        self.assertIs(type(signer), bytes)
        self.assertEqual(len(signer), 20)

    def test_threads(self):
        """Recovering from several threads at once, as the GIL is released while recovering"""
        signatures = build_secp256k1_signatures(25)
        with ThreadPoolExecutor(max_workers=8) as executor:
            recovered_signers = list(
                executor.map(
                    lambda signature: safe_eth_native.ecrecover(*signature[:4]),
                    signatures * 4,
                )
            )
        self.assertEqual(
            recovered_signers, [signature[4] for signature in signatures * 4]
        )
