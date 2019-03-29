import logging

from django.test import TestCase

from eth_account import Account

from ..exceptions import NotEnoughSafeTransactionGas, SignaturesDataTooShort
from ..safe_tx import SafeTx
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestSafeTx(TestCase, SafeTestCaseMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_send_safe_tx(self):
        owners = [Account.create() for _ in range(2)]
        owner_addresses = [owner.address for owner in owners]
        threshold = 1
        safe_creation = self.deploy_test_safe(owners=owner_addresses, threshold=threshold,
                                              initial_funding_wei=self.w3.toWei(0.1, 'ether'))
        safe_address = safe_creation.safe_address
        to = Account().create().address
        value = self.w3.toWei(0.01, 'ether')
        safe_tx_gas = 200000
        data_gas = 100000

        safe_tx = SafeTx(self.ethereum_client, safe_address, to, value, b'', 0, safe_tx_gas, data_gas, self.gas_price,
                         None, None, safe_nonce=0)

        with self.assertRaises(SignaturesDataTooShort):
            safe_tx.call(tx_sender_address=self.ethereum_test_account.address)

        # Check signing
        self.assertFalse(safe_tx.signers)
        safe_tx.sign(owners[0].privateKey)
        self.assertIn(owners[0].address, safe_tx.signers)

        with self.assertRaises(NotEnoughSafeTransactionGas):
            safe_tx.call(tx_sender_address=self.ethereum_test_account.address, tx_gas=safe_tx_gas // 2)

        self.assertEqual(safe_tx.call(tx_sender_address=self.ethereum_test_account.address), 1)
        tx_hash, _ = safe_tx.execute(tx_sender_private_key=self.ethereum_test_account.privateKey)
        self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        self.assertEqual(self.ethereum_client.get_balance(to), value)

        safe_tx.unsign(owners[0].address)
        self.assertFalse(safe_tx.signers)

    def test_sign_safe_tx(self):
        owners = [Account.create() for _ in range(3)]
        owners_unsorted = sorted(owners, key=lambda x: x.address.lower(), reverse=True)
        owner_addresses = [owner.address for owner in owners_unsorted]
        threshold = 1
        safe_creation = self.deploy_test_safe(owners=owner_addresses, threshold=threshold,
                                              initial_funding_wei=self.w3.toWei(0.1, 'ether'))
        safe_address = safe_creation.safe_address
        to = Account().create().address
        value = self.w3.toWei(0.01, 'ether')

        safe_tx = SafeTx(self.ethereum_client, safe_address, to, value, b'', 0, 200000, 100000, self.gas_price,
                         None, None, safe_nonce=0)

        safe_tx.sign(owners_unsorted[0].privateKey)
        safe_tx.sign(owners_unsorted[2].privateKey)
        signers = [owner_addresses[0], owner_addresses[2]]

        self.assertEqual(safe_tx.signers, safe_tx.sorted_signers)
        self.assertNotEqual(signers, safe_tx.signers)
        self.assertEqual(set(signers), set(safe_tx.signers))
        self.assertEqual(len(safe_tx.signers), 2)

        safe_tx.sign(owners_unsorted[1].privateKey)
        signers = owner_addresses
        self.assertEqual(safe_tx.signers, safe_tx.sorted_signers)
        self.assertNotEqual(signers, safe_tx.signers)
        self.assertEqual(set(signers), set(safe_tx.signers))
        self.assertEqual(len(safe_tx.signers), 3)

        # Sign again
        safe_tx.sign(owners_unsorted[0].privateKey)
        self.assertEqual(len(safe_tx.signers), 3)

        # Sign again
        safe_tx.unsign(owners_unsorted[1].address)
        signers = [owner_addresses[0], owner_addresses[2]]
        self.assertEqual(set(signers), set(safe_tx.signers))
        self.assertEqual(len(safe_tx.signers), 2)
