from django.test import TestCase

from ethereum.utils import sha3
from hexbytes import HexBytes
from rest_framework import serializers

from ...constants import NULL_ADDRESS, SENTINEL_ADDRESS
from ...utils import (get_eth_address_with_invalid_checksum,
                      get_eth_address_with_key)
from ..serializers import EthereumAddressField, HexadecimalField, Sha3HashField


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


class TestSerializers(TestCase):
    def test_ethereum_address_field(self):
        valid_address, _ = get_eth_address_with_key()
        for value in ['0x674647242239941B2D35368E66A4EDc39b161Da1',
                      '0x40f3F89639Bffc7B23Ca5d9FCb9ed9a9c579664A',
                      valid_address,
                      None]:
            serializer = EthereumAddressSerializerTest(data={'value': value})
            self.assertTrue(serializer.is_valid())
            self.assertEqual(value, serializer.data['value'])

        invalid_address = get_eth_address_with_invalid_checksum()
        for not_valid_value in ['0x674647242239941B2D35368E66A4EDc39b161DA1',
                                invalid_address,
                                '0x0000000000000000000000000000000000000000',
                                '0x0000000000000000000000000000000000000001',
                                '0xABC',
                                '0xJK']:
            serializer = EthereumAddressSerializerTest(data={'value': not_valid_value})
            self.assertFalse(serializer.is_valid())

    def test_ethereum_zero_address_field(self):
        valid_address, _ = get_eth_address_with_key()
        S = EthereumZeroAddressSerializerTest
        self.assertTrue(S(data={'value': valid_address}).is_valid())
        self.assertTrue(S(data={'value': NULL_ADDRESS}).is_valid())
        self.assertFalse(S(data={'value': SENTINEL_ADDRESS}).is_valid())

    def test_ethereum_sentinel_address_field(self):
        valid_address, _ = get_eth_address_with_key()
        S = EthereumSentinelAddressSerializerTest
        self.assertTrue(S(data={'value': valid_address}).is_valid())
        self.assertTrue(S(data={'value': SENTINEL_ADDRESS}).is_valid())
        self.assertFalse(S(data={'value': NULL_ADDRESS}).is_valid())

    def test_hexadecimal_field(self):
        serializer = HexadecimalBlankSerializerTest(data={'value': '0x'})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['value'])
        self.assertIsNone(serializer.data['value'])

        serializer = HexadecimalBlankSerializerTest(data={'value': None})
        self.assertFalse(serializer.is_valid())

        serializer = HexadecimalNullSerializerTest(data={'value': None})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['value'])

        value = '0xabcd'
        serializer = HexadecimalSerializerTest(data={'value': value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))
        self.assertEqual(value, serializer.data['value'])

        value = '0xabcd'
        serializer = HexadecimalSerializerTest(data={'value': HexBytes(value)})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))
        self.assertEqual(value, serializer.data['value'])

        value = '0xabcd'
        bytes_value = bytes.fromhex(value.replace('0x', ''))
        serializer = HexadecimalSerializerTest(data={'value': bytes_value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))
        self.assertEqual(value, serializer.data['value'])

        value = 'abc'
        serializer = HexadecimalSerializerTest(data={'value': value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))

    def test_hexadecimal_class_field(self):
        class A:
            pass

        a = A()
        for value in ['abc', '0xabc', b'23', memoryview(b'23')]:
            hex_value = value if isinstance(value, str) else value.hex()
            a.value = value
            serializer = HexadecimalSerializerTest(a)
            self.assertEqual(serializer.data['value'], HexBytes(hex_value).hex())

    def test_hash_serializer_field(self):
        value = sha3('test').hex()
        serializer = Sha3HashSerializerTest(data={'value': value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))

        # Hash with one more character - Must be 32 bytes
        serializer = Sha3HashSerializerTest(data={'value': value + 'a'})
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())

        # Hash with one less character - Must be 32 bytes
        serializer = Sha3HashSerializerTest(data={'value': value[:-1]})
        self.assertFalse(serializer.is_valid())
