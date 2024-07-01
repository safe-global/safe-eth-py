from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.db import transaction
from django.test import TestCase

from eth_account import Account
from faker import Faker

from ...constants import NULL_ADDRESS, SENTINEL_ADDRESS
from ...utils import fast_is_checksum_address, fast_keccak_text
from .models import EthereumAddressV2, Keccak256Hash, Uint32, Uint96, Uint256

faker = Faker()


class TestModels(TestCase):
    def test_ethereum_address_field(self):
        address = Account.create().address
        self.assertTrue(fast_is_checksum_address(address))
        ethereum_address = EthereumAddressV2.objects.create(value=address)
        ethereum_address.refresh_from_db()
        self.assertTrue(fast_is_checksum_address(ethereum_address.value))
        self.assertEqual(address, ethereum_address.value)

        # Test addresses
        for addresss in (
            None,
            NULL_ADDRESS,
            SENTINEL_ADDRESS,
            Account.create().address,
        ):
            with self.subTest(special_address=addresss):
                EthereumAddressV2.objects.create(value=addresss)
                self.assertEqual(
                    EthereumAddressV2.objects.get(value=addresss).value,
                    addresss,
                )

        with self.assertRaisesMessage(
            ValidationError,
            '"0x23" value must be an EIP55 checksummed address.',
        ):
            with transaction.atomic():
                EthereumAddressV2.objects.create(value="0x23")

        ethereum_address = EthereumAddressV2(value=Account.create().address)
        self.assertIsNone(ethereum_address.full_clean())

    def test_uint256_field(self):
        for value in [
            2,
            2**256,
            25572735541615049941137326092682691158109824779649981270427004917341670006487,
            None,
        ]:
            uint256 = Uint256.objects.create(value=value)
            uint256.refresh_from_db()
            self.assertEqual(uint256.value, value)

        # Overflow
        with self.assertRaises(Exception):
            value = 2**263
            Uint256.objects.create(value=value)

        # Signed
        with self.assertRaises(ValidationError):
            Uint256.objects.create(value=-2)

    def test_uint96_field(self):
        for value in [
            2,
            2**96,
            79228162514264337593543950336,
            None,
        ]:
            uint96 = Uint96.objects.create(value=value)
            uint96.refresh_from_db()
            self.assertEqual(uint96.value, value)

        # Overflow
        with self.assertRaises(Exception):
            value = 2**97
            Uint96.objects.create(value=value)

        # Signed
        with self.assertRaises(ValidationError):
            Uint96.objects.create(value=-2)

    def test_uint32_field(self):
        for value in [
            2,
            2**32,
            4294967296,
            None,
        ]:
            uint32 = Uint32.objects.create(value=value)
            uint32.refresh_from_db()
            self.assertEqual(uint32.value, value)
        # Overflow
        with self.assertRaises(Exception):
            value = 2**34
            Uint32.objects.create(value=value)

        # Signed
        with self.assertRaises(ValidationError):
            Uint32.objects.create(value=-2)

    def test_keccak256_field(self):
        value_hexbytes = fast_keccak_text(faker.name())
        value_hex_with_0x: str = value_hexbytes.hex()
        value_hex_without_0x: str = value_hex_with_0x[2:]
        value: bytes = bytes(value_hexbytes)

        values = [value, value_hex_without_0x, value_hex_with_0x, value_hexbytes]

        for v in values:
            with self.subTest(v=v):
                keccak256_hash = Keccak256Hash(value=v)
                self.assertIsNone(keccak256_hash.full_clean())
                keccak256_hash.save()
                keccak256_hash.refresh_from_db()
                self.assertEqual(keccak256_hash.value, value_hex_with_0x)

        for v in values:
            with self.subTest(v=v):
                self.assertEqual(
                    Keccak256Hash.objects.filter(value=v).count(), len(values)
                )

        # Hash null
        keccak256_hash = Keccak256Hash.objects.create(value=None)
        keccak256_hash.refresh_from_db()
        self.assertIsNone(keccak256_hash.value)

        # Hash too big
        value_hex_invalid: str = "0x" + value_hex_without_0x + "a"
        with self.assertRaisesMessage(
            ValidationError, f'"{value_hex_invalid}" hash must have exactly 32 bytes.'
        ):
            with transaction.atomic():
                Keccak256Hash.objects.create(value=value_hex_invalid)

        # Hash too small
        value_hex_invalid: str = "0x" + "a1"
        with self.assertRaisesMessage(
            ValidationError, f'"{value_hex_invalid}" hash must have exactly 32 bytes.'
        ):
            with transaction.atomic():
                Keccak256Hash.objects.create(value=value_hex_invalid)

        # Invalid hash
        value_hex_invalid: str = "UX/IO"
        with self.assertRaisesMessage(
            ValidationError,
            f'"{value_hex_invalid}" hash must be a 32 bytes hexadecimal.',
        ):
            with transaction.atomic():
                Keccak256Hash.objects.create(value=value_hex_invalid)

    def test_serialize_keccak256_field_to_json(self):
        hexvalue: str = (
            "0xdb5b7c6d3b0cc538a5859afc4674a785d9d111c3835390295f3d3173d41ca8ea"
        )
        Keccak256Hash.objects.create(value=hexvalue)
        serialized = serialize("json", Keccak256Hash.objects.all())
        # hexvalue should be in serialized data
        self.assertIn(hexvalue, serialized)

    def test_serialize_ethereum_address_v2_field_to_json(self):
        address: str = "0x5aFE3855358E112B5647B952709E6165e1c1eEEe"
        EthereumAddressV2.objects.create(value=address)
        serialized = serialize("json", EthereumAddressV2.objects.all())
        # address should be in serialized data
        self.assertIn(address, serialized)

    def test_serialize_uint256_field_to_json(self):
        value = 2**256
        Uint256.objects.create(value=value)
        serialized = serialize("json", Uint256.objects.all())
        # value should be in serialized data
        self.assertIn(str(value), serialized)
