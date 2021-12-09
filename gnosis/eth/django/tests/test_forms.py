from django.forms import forms
from django.test import TestCase

from web3 import Web3

from ..filters import EthereumAddressFieldForm, Keccak256FieldForm


class EthereumAddressForm(forms.Form):
    value = EthereumAddressFieldForm()


class Keccak256Form(forms.Form):
    value = Keccak256FieldForm()


class TestForms(TestCase):
    def test_ethereum_address_field_form(self):
        form = EthereumAddressForm(data={"value": "not a ethereum address"})
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
