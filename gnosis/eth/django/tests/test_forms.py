from django.forms import forms
from django.test import TestCase

from hexbytes import HexBytes
from web3 import Web3

from ..forms import EthereumAddressFieldForm, HexFieldForm, Keccak256FieldForm


class EthereumAddressForm(forms.Form):
    value = EthereumAddressFieldForm()


class HexForm(forms.Form):
    value = HexFieldForm(required=False)


class Keccak256Form(forms.Form):
    value = Keccak256FieldForm(required=False)


class TestForms(TestCase):
    def test_ethereum_address_field_form(self):
        form = EthereumAddressForm(data={"value": "not an ethereum address"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ["Enter a valid checksummed Ethereum Address."]
        )

        form = EthereumAddressForm(
            data={"value": "0xbaa7df320f385318fe3409cc95db48de60dfa033"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ["Enter a valid checksummed Ethereum Address."]
        )

        form = EthereumAddressForm(
            data={"value": "0xbaa7df320f385318fE3409CC95Db48DE60dfA033"}
        )
        self.assertTrue(form.is_valid())

    def test_hex_field_form(self):
        form = HexForm(data={"value": "not a hexadecimal"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["value"], ["Enter a valid hexadecimal."])

        form = HexForm(data={"value": "0xabcd"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["value"], HexBytes("0xabcd"))

        form = HexForm(initial={"value": memoryview(bytes.fromhex("cdef"))})
        self.assertIn('value="0xcdef"', form.as_p())

        form = HexForm(data={"value": 1})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["value"], HexBytes(1))

        form = HexForm(data={"value": ""})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data["value"])

        form = HexForm(data={"value": None})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data["value"])

    def test_keccak256_field_form(self):
        form = Keccak256Form(data={"value": "not a hash"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ['"not a hash" is not a valid keccak256 hash.']
        )

        form = Keccak256Form(data={"value": "0x1234"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ['"0x1234" keccak256 hash should be 32 bytes.']
        )

        form = Keccak256Form(data={"value": Web3.keccak(text="testing").hex()})
        self.assertTrue(form.is_valid())

        form = Keccak256Form(data={"value": ""})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data["value"])

        form = HexForm(data={"value": None})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data["value"])
