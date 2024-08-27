from django.core.exceptions import ValidationError
from django.test import TestCase

from eth_account import Account

from ..validators import validate_checksumed_address


class TestValidators(TestCase):
    def test_checksum_address_validator(self):
        eth_address = Account.create().address

        self.assertIsNone(validate_checksumed_address(eth_address))

        self.assertRaises(
            ValidationError, validate_checksumed_address, eth_address.lower()
        )
