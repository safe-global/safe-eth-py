import logging

from django.test import TestCase

from eth_account import Account

from gnosis.safe import Safe

from ..proxy_factory import ProxyFactory
from .safe_test_case import SafeTestCaseMixin
from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)


class TestProxyFactory(TestCase, SafeTestCaseMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()
        cls.proxy_factory = ProxyFactory(cls.proxy_factory_contract_address, cls.ethereum_client)

    def test_check_proxy_code(self):
        proxy_contract_address = self.deploy_test_safe().safe_address
        self.assertTrue(self.proxy_factory.check_proxy_code(proxy_contract_address))

        ethereum_tx_sent = Safe.deploy_master_contract(self.ethereum_client, self.ethereum_test_account)
        self.assertFalse(self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address))

        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract(self.ethereum_test_account,
                                                                    Account.create().address)
        self.assertTrue(self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address))

    def test_deploy_proxy_contract(self):
        s = 15
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        payment_token = None
        safe_creation_tx = Safe.build_safe_creation_tx(self.ethereum_client, self.safe_old_contract_address,
                                                       s, owners, threshold, self.gas_price, payment_token,
                                                       payment_receiver=self.ethereum_test_account.address)
        # Send ether for safe deploying costs
        self.send_tx({
            'to': safe_creation_tx.safe_address,
            'value': safe_creation_tx.payment
        }, self.ethereum_test_account)

        proxy_factory = ProxyFactory(self.proxy_factory_contract_address, self.ethereum_client)
        ethereum_tx_sent = proxy_factory.deploy_proxy_contract(self.ethereum_test_account,
                                                               safe_creation_tx.master_copy,
                                                               safe_creation_tx.safe_setup_data,
                                                               safe_creation_tx.gas,
                                                               gas_price=self.gas_price)
        receipt = self.ethereum_client.get_transaction_receipt(ethereum_tx_sent.tx_hash, timeout=20)
        self.assertEqual(receipt.status, 1)
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_master_copy_address(), safe_creation_tx.master_copy)
        self.assertEqual(set(safe.retrieve_owners()), set(owners))

    def test_deploy_proxy_contract_with_nonce(self):
        salt_nonce = generate_salt_nonce()
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        payment_token = None
        safe_create2_tx = Safe.build_safe_create2_tx(self.ethereum_client, self.safe_contract_address,
                                                     self.proxy_factory_contract_address, salt_nonce,
                                                     owners, threshold, self.gas_price, payment_token)
        # Send ether for safe deploying costs
        self.send_tx({
            'to': safe_create2_tx.safe_address,
            'value': safe_create2_tx.payment
        }, self.ethereum_test_account)

        proxy_factory = ProxyFactory(self.proxy_factory_contract_address, self.ethereum_client)
        ethereum_tx_sent = proxy_factory.deploy_proxy_contract_with_nonce(self.ethereum_test_account,
                                                                          safe_create2_tx.master_copy_address,
                                                                          safe_create2_tx.safe_setup_data,
                                                                          salt_nonce,
                                                                          safe_create2_tx.gas,
                                                                          gas_price=self.gas_price)
        receipt = self.ethereum_client.get_transaction_receipt(ethereum_tx_sent.tx_hash, timeout=20)
        self.assertEqual(receipt.status, 1)
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(ethereum_tx_sent.contract_address, safe_create2_tx.safe_address)
        self.assertEqual(set(safe.retrieve_owners()), set(owners))
        self.assertEqual(safe.retrieve_master_copy_address(), safe_create2_tx.master_copy_address)

    def test_get_proxy_runtime_code(self):
        self.assertGreater(len(self.proxy_factory.get_proxy_runtime_code()), 4)
