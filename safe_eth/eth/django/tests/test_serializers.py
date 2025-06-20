import base64

from django.core.serializers import serialize
from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes
from rest_framework import serializers

from safe_eth.util.util import to_0x_hex_str

from ...constants import NULL_ADDRESS, SENTINEL_ADDRESS
from ...utils import fast_keccak_text, get_eth_address_with_invalid_checksum
from ..serializers import (
    EthereumAddressField,
    HexadecimalField,
    Sha3HashField,
    Uint32Field,
    Uint96Field,
)
from .models import HexV2Hash


class EthereumAddressSerializerTest(serializers.Serializer):
    value = EthereumAddressField(allow_null=True)


class EthereumSentinelAddressSerializerTest(serializers.Serializer):
    value = EthereumAddressField(allow_null=True, allow_sentinel_address=True)


class EthereumZeroAddressSerializerTest(serializers.Serializer):
    value = EthereumAddressField(allow_null=True, allow_zero_address=True)


class HexadecimalSerializerTest(serializers.Serializer):
    value = HexadecimalField()


class HexadecimalBlankSerializerTest(serializers.Serializer):
    value = HexadecimalField(allow_blank=True)


class HexadecimalNullSerializerTest(serializers.Serializer):
    value = HexadecimalField(allow_null=True)


class Sha3HashSerializerTest(serializers.Serializer):
    value = Sha3HashField()


class Uint96SerializerTest(serializers.Serializer):
    value = Uint96Field()


class Uint32SerializerTest(serializers.Serializer):
    value = Uint32Field()


class TestSerializers(TestCase):
    def test_ethereum_address_field(self):
        valid_address = Account.create().address
        for value in [
            "0x674647242239941B2D35368E66A4EDc39b161Da1",
            "0x40f3F89639Bffc7B23Ca5d9FCb9ed9a9c579664A",
            valid_address,
            None,
        ]:
            serializer = EthereumAddressSerializerTest(data={"value": value})
            self.assertTrue(serializer.is_valid())
            self.assertEqual(value, serializer.data["value"])

        invalid_address = get_eth_address_with_invalid_checksum()
        for not_valid_value in [
            "0x674647242239941B2D35368E66A4EDc39b161DA1",
            invalid_address,
            "0x0000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000001",
            "0xABC",
            "0xJK",
        ]:
            serializer = EthereumAddressSerializerTest(data={"value": not_valid_value})
            self.assertFalse(serializer.is_valid())

        serializer = EthereumAddressSerializerTest(data={"value": NULL_ADDRESS})
        self.assertFalse(serializer.is_valid())
        self.assertIn("0x0 address is not allowed", serializer.errors["value"])

    def test_ethereum_zero_address_field(self):
        valid_address = Account.create().address
        S = EthereumZeroAddressSerializerTest
        self.assertTrue(S(data={"value": valid_address}).is_valid())
        self.assertTrue(S(data={"value": NULL_ADDRESS}).is_valid())
        self.assertFalse(S(data={"value": SENTINEL_ADDRESS}).is_valid())

    def test_ethereum_sentinel_address_field(self):
        valid_address = Account.create().address
        S = EthereumSentinelAddressSerializerTest
        self.assertTrue(S(data={"value": valid_address}).is_valid())
        self.assertTrue(S(data={"value": SENTINEL_ADDRESS}).is_valid())
        self.assertFalse(S(data={"value": NULL_ADDRESS}).is_valid())

    def test_hexadecimal_field(self):
        serializer = HexadecimalBlankSerializerTest(data={"value": "0x"})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data["value"])
        self.assertIsNone(serializer.data["value"])

        serializer = HexadecimalBlankSerializerTest(data={"value": None})
        self.assertFalse(serializer.is_valid())

        serializer = HexadecimalNullSerializerTest(data={"value": None})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data["value"])

        value = "0xabcd"
        serializer = HexadecimalSerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["value"], HexBytes(value))
        self.assertEqual(value, serializer.data["value"])

        value = "0xabcd"
        serializer = HexadecimalSerializerTest(data={"value": HexBytes(value)})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["value"], HexBytes(value))
        self.assertEqual(value, serializer.data["value"])

        value = "0xabcd"
        bytes_value = bytes.fromhex(value.replace("0x", ""))
        serializer = HexadecimalSerializerTest(data={"value": bytes_value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["value"], HexBytes(value))
        self.assertEqual(value, serializer.data["value"])

        value = "abc"
        serializer = HexadecimalSerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["value"], HexBytes(value))

        value = "abc"
        serializer = HexadecimalSerializerTest(data={"value": [value]})
        self.assertFalse(serializer.is_valid())

    def test_hexadecimal_class_field(self):
        class A:
            pass

        a = A()
        for value in ["abc", "0xabc", b"23", memoryview(b"23")]:
            hex_value = value if isinstance(value, str) else value.hex()
            a.value = value
            serializer = HexadecimalSerializerTest(a)
            self.assertEqual(
                serializer.data["value"], to_0x_hex_str(HexBytes(hex_value))
            )

    def test_hash_serializer_field(self):
        value = fast_keccak_text("test").hex()
        serializer = Sha3HashSerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["value"], HexBytes(value))

        # Hash with one more character - Must be 32 bytes
        serializer = Sha3HashSerializerTest(data={"value": value + "a"})
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())

        # Hash with 1 less character - Should still be 32 bytes
        serializer = Sha3HashSerializerTest(data={"value": value[:-1]})
        self.assertTrue(serializer.is_valid())

        # Hash with 2 less character - Less than 32 bytes
        serializer = Sha3HashSerializerTest(data={"value": value[:-2]})
        self.assertFalse(serializer.is_valid())

    def test_uint96_field(self):
        value = None
        serializer = Uint96SerializerTest(data={"value": value})
        self.assertFalse(serializer.is_valid())

        value = -1
        serializer = Uint96SerializerTest(data={"value": value})
        self.assertFalse(serializer.is_valid())

        value = 1000
        serializer = Uint96SerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())

        value = 2**96
        serializer = Uint96SerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())

        value = 2**97
        serializer = Uint96SerializerTest(data={"value": value})
        self.assertFalse(serializer.is_valid())

    def test_uint32_field(self):
        value = None
        serializer = Uint32SerializerTest(data={"value": value})
        self.assertFalse(serializer.is_valid())

        value = -1
        serializer = Uint32SerializerTest(data={"value": value})
        self.assertFalse(serializer.is_valid())

        value = 1000
        serializer = Uint32SerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())

        value = 2**32
        serializer = Uint32SerializerTest(data={"value": value})
        self.assertTrue(serializer.is_valid())

        # 2**33 still have the same number of digits than 2**32
        value = 2**34
        serializer = Uint32SerializerTest(data={"value": value})
        self.assertFalse(serializer.is_valid())

    def test_hexv2field(self):
        hex_value = HexBytes("0x1234abcd")
        alt_inputs = [hex_value, b"\x12\x34\xab\xcd"]

        for v in alt_inputs:
            with self.subTest(v=v):
                obj = HexV2Hash.objects.create(value=v)
                obj.refresh_from_db()
                self.assertIsInstance(obj.value, bytes)
                self.assertEqual(obj.value, bytes(v))

    def test_serialize_hexv2field_to_json(self):
        hexvalue = HexBytes("0x1234abcd")
        expected_base64 = base64.b64encode(bytes(hexvalue)).decode()

        HexV2Hash.objects.create(value=hexvalue)
        serialized = serialize("json", HexV2Hash.objects.all())

        self.assertIn(expected_base64, serialized)
