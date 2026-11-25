import os
import random
import unittest

import eth_utils
import safe_eth_native
from native_test_helpers import BytesSubclass, StrSubclass, reference_checksum_address

# https://eips.ethereum.org/EIPS/eip-55#test-cases
EIP_55_CHECKSUM_ADDRESSES = [
    # All caps
    "0x52908400098527886E0F7030069857D2E4169EE7",
    "0x8617E340B3D01FA5F11F306F4090FD50E238070D",
    # All lower
    "0xde709f2102306220921060314715629080e2fb77",
    "0x27b1fdb04752bbc536007a920d24acb045561c26",
    # Normal
    "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed",
    "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359",
    "0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB",
    "0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb",
]

# `is_checksum_address` table of the eth-utils test suite
ETH_UTILS_IS_CHECKSUM_ADDRESS_CASES = [
    ("0x52908400098527886E0F7030069857D2E4169EE7", True),
    ("0x8617E340B3D01FA5F11F306F4090FD50E238070D", True),
    ("0xde709f2102306220921060314715629080e2fb77", True),
    ("0x27b1fdb04752bbc536007a920d24acb045561c26", True),
    ("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed", True),
    ("0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359", True),
    ("0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB", True),
    ("0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb", True),
    ("0xd3cda913deb6f67967b99d67acdfa1712c293601", False),
    ("0xD3CDA913DEB6F67967B99D67ACDFA1712C293601", False),
    ("0XD1220A0CF47C7B9BE7A2E6BA89F429762E7B9ADB", False),
    ("0xd1220a0cf47c7b9be7a2e6ba89f429762e7b9adb", False),
    (b"0x52908400098527886E0F7030069857D2E4169EE7", False),
    (b"0xd1220a0cf47c7b9be7a2e6ba89f429762e7b9adb", False),
]

# `to_checksum_address` table of the eth-utils test suite
ETH_UTILS_TO_CHECKSUM_ADDRESS_CASES = [
    (
        "0xd3cda913deb6f67967b99d67acdfa1712c293601",
        "0xd3CdA913deB6f67967B99D67aCDFa1712C293601",
    ),
    (
        "0xD3CDA913DEB6F67967B99D67ACDFA1712C293601",
        "0xd3CdA913deB6f67967B99D67aCDFa1712C293601",
    ),
    (
        "0xd3CdA913deB6f67967B99D67aCDFa1712C293601",
        "0xd3CdA913deB6f67967B99D67aCDFa1712C293601",
    ),
    (
        b"\xd3\xcd\xa9\x13\xde\xb6\xf6yg\xb9\x9dg\xac\xdf\xa1q,)6\x01",
        "0xd3CdA913deB6f67967B99D67aCDFa1712C293601",
    ),
    (
        "0xc6d9d2cd449a754c494264e1809c50e34d64562b",
        "0xc6d9d2cD449A754c494264e1809c50e34D64562b",
    ),
    (
        "c6d9d2cd449a754c494264e1809c50e34d64562b",
        "0xc6d9d2cD449A754c494264e1809c50e34D64562b",
    ),
    (
        b"\xc6\xd9\xd2\xcdD\x9auLIBd\xe1\x80\x9cP\xe3MdV+",
        "0xc6d9d2cD449A754c494264e1809c50e34D64562b",
    ),
]

# Characters that look like hex digits but are not ASCII hex digits
NOT_HEX_CHARACTERS = ["g", "G", "x", " ", "\n", "é", "١", "０", "ａ", "\x00", "\ud800"]


def build_address_forms(address_bytes: bytes) -> list[str | bytes]:
    """Every form of the same address `to_checksum_address` accepts"""
    lowercase_hex = address_bytes.hex()
    checksum_address = reference_checksum_address(address_bytes)
    return [
        address_bytes,
        BytesSubclass(address_bytes),
        "0x" + lowercase_hex,
        "0X" + lowercase_hex,
        "0x" + lowercase_hex.upper(),
        "0X" + lowercase_hex.upper(),
        lowercase_hex,
        lowercase_hex.upper(),
        checksum_address,
        checksum_address[2:],
        "0x" + checksum_address[2:].swapcase(),
        StrSubclass("0x" + lowercase_hex),
    ]


def build_invalid_addresses(address_bytes: bytes) -> list[str | bytes]:
    lowercase_hex = address_bytes.hex()
    invalid_addresses: list[str | bytes] = [
        b"",
        address_bytes[:19],
        address_bytes + b"\x00",
        ("0x" + lowercase_hex).encode(),
        lowercase_hex.encode(),
        "",
        "0x",
        "0X",
        "0x" + lowercase_hex[:39],
        "0x" + lowercase_hex + "0",
        lowercase_hex[:39],
        lowercase_hex + "0",
        "0x0x" + lowercase_hex[:38],
        "x0" + lowercase_hex,
        "00" + lowercase_hex,
        " 0x" + lowercase_hex,
        "0x" + lowercase_hex + " ",
        "0x" + lowercase_hex + "\n",
        "0x " + lowercase_hex[:39],
    ]
    for not_hex_character in NOT_HEX_CHARACTERS:
        position = random.randrange(40)
        invalid_addresses.append(
            "0x"
            + lowercase_hex[:position]
            + not_hex_character
            + lowercase_hex[position + 1 :]
        )
    return invalid_addresses


class TestToChecksumAddress(unittest.TestCase):
    def test_eip_55_vectors(self):
        """EIP-55 test cases, from the lowercase, uppercase and checksummed forms"""
        for checksum_address in EIP_55_CHECKSUM_ADDRESSES:
            for value in (
                checksum_address,
                checksum_address.lower(),
                "0x" + checksum_address[2:].upper(),
                bytes.fromhex(checksum_address[2:]),
            ):
                with self.subTest(value=value):
                    self.assertEqual(
                        safe_eth_native.to_checksum_address(value), checksum_address
                    )

    def test_eth_utils_vectors(self):
        """`to_checksum_address` table of the eth-utils test suite"""
        for value, expected_checksum_address in ETH_UTILS_TO_CHECKSUM_ADDRESS_CASES:
            with self.subTest(value=value):
                self.assertEqual(
                    safe_eth_native.to_checksum_address(value),
                    expected_checksum_address,
                )

    def test_every_form_matches_eth_utils(self):
        """Random addresses in every accepted form give the same result as eth-utils"""
        for address_bytes in [bytes(20), b"\xff" * 20] + [
            os.urandom(20) for _ in range(2000)
        ]:
            expected_checksum_address = reference_checksum_address(address_bytes)
            for value in build_address_forms(address_bytes):
                self.assertEqual(
                    eth_utils.to_checksum_address(value), expected_checksum_address
                )
                checksum_address = safe_eth_native.to_checksum_address(value)
                self.assertEqual(checksum_address, expected_checksum_address, value)
                self.assertIs(type(checksum_address), str)

    def test_rejects_invalid_addresses(self):
        """Values eth-utils rejects raise `ValueError`"""
        for _ in range(50):
            for value in build_invalid_addresses(os.urandom(20)):
                with self.subTest(value=value):
                    with self.assertRaises(ValueError):
                        eth_utils.to_checksum_address(value)
                    with self.assertRaises(ValueError):
                        safe_eth_native.to_checksum_address(value)

    def test_rejects_other_types(self):
        """Values that are not `bytes` or `str` raise `TypeError`"""
        for value in (
            None,
            1,
            int.from_bytes(os.urandom(20), "big"),
            1.0,
            bytearray(20),
            memoryview(bytes(20)),
            [0] * 20,
        ):
            with self.subTest(value=value), self.assertRaises(TypeError):
                safe_eth_native.to_checksum_address(value)


class TestIsChecksumAddress(unittest.TestCase):
    def test_eth_utils_vectors(self):
        """`is_checksum_address` table of the eth-utils test suite"""
        for value, expected in ETH_UTILS_IS_CHECKSUM_ADDRESS_CASES:
            with self.subTest(value=value):
                self.assertIs(safe_eth_native.is_checksum_address(value), expected)

    def test_matches_eth_utils(self):
        """Valid and invalid values give the same result as eth-utils"""
        for _ in range(2000):
            address_bytes = os.urandom(20)
            checksum_address = reference_checksum_address(address_bytes)
            self.assertTrue(safe_eth_native.is_checksum_address(checksum_address))
            self.assertTrue(
                safe_eth_native.is_checksum_address(StrSubclass(checksum_address))
            )
            values = build_address_forms(address_bytes) + build_invalid_addresses(
                address_bytes
            )
            # Flip the case of one letter
            letter_positions = [
                position
                for position, character in enumerate(checksum_address)
                if position > 1 and character.isalpha()
            ]
            if letter_positions:
                position = random.choice(letter_positions)
                values.append(
                    checksum_address[:position]
                    + checksum_address[position].swapcase()
                    + checksum_address[position + 1 :]
                )
            for value in values:
                self.assertIs(
                    safe_eth_native.is_checksum_address(value),
                    eth_utils.is_checksum_address(value),
                    value,
                )

    def test_other_types_are_not_checksum_addresses(self):
        """Only `str` can be a checksum address, the encoded address included"""
        checksum_address = reference_checksum_address(os.urandom(20))
        for value in (
            None,
            1,
            1.0,
            checksum_address.encode(),
            bytearray(checksum_address.encode()),
            [checksum_address],
            object(),
        ):
            with self.subTest(value=value):
                self.assertFalse(safe_eth_native.is_checksum_address(value))
