from django.test import TestCase

from eth_account import Account
from web3 import Web3

from gnosis.eth.constants import NULL_ADDRESS

from ..signatures import get_signing_address


class TestSafeSignature(TestCase):
    def test_get_signing_address(self):
        account = Account.create()
        # Random hash
        random_hash = Web3.keccak(text="tanxugueiras")
        signature = account.signHash(random_hash)
        self.assertEqual(
            get_signing_address(random_hash, signature.v, signature.r, signature.s),
            account.address,
        )

        # Invalid signature will return the `NULL_ADDRESS`
        self.assertEqual(
            get_signing_address(random_hash, signature.v - 8, signature.r, signature.s),
            NULL_ADDRESS,
        )
