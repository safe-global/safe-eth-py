import logging

from django.test import TestCase

from eth_account import Account

from gnosis.eth import EthereumClient
from gnosis.eth.tests.utils import just_test_if_mainnet_node
from gnosis.safe import Safe

from ..proxy_factory import ProxyFactory
from .safe_test_case import SafeTestCaseMixin
from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)


class TestProxyFactory(SafeTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.proxy_factory = ProxyFactory(
            cls.proxy_factory_contract_address, cls.ethereum_client
        )

    def test_check_proxy_code(self):
        proxy_contract_address = self.deploy_test_safe().address
        self.assertTrue(self.proxy_factory.check_proxy_code(proxy_contract_address))

        self.assertFalse(
            self.proxy_factory.check_proxy_code(self.safe_contract_address)
        )

        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract(
            self.ethereum_test_account, self.safe_contract_address
        )
        self.assertTrue(
            self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address)
        )

        # Test proxy factory v1.1.1
        ethereum_tx_sent = ProxyFactory.deploy_proxy_factory_contract_v1_1_1(
            self.ethereum_client, self.ethereum_test_account
        )
        proxy_factory_V1_1_1 = ProxyFactory(
            ethereum_tx_sent.contract_address, self.ethereum_client
        )
        ethereum_tx_sent = proxy_factory_V1_1_1.deploy_proxy_contract(
            self.ethereum_test_account, self.safe_contract_address
        )
        self.assertTrue(
            self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address)
        )

        # Test proxy factory v1.0.0
        ethereum_tx_sent = ProxyFactory.deploy_proxy_factory_contract_v1_0_0(
            self.ethereum_client, self.ethereum_test_account
        )
        proxy_factory_V1_0_0 = ProxyFactory(
            ethereum_tx_sent.contract_address, self.ethereum_client
        )
        ethereum_tx_sent = proxy_factory_V1_0_0.deploy_proxy_contract(
            self.ethereum_test_account, self.safe_contract_address
        )
        self.assertTrue(
            self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address)
        )

    def test_check_proxy_code_mainnet(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        last_proxy_factory_address = "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2"
        proxy_factory = ProxyFactory(last_proxy_factory_address, ethereum_client)

        # Random Safes deployed by the proxy_factory
        safes = [
            "0x7f2722741F997c63133e656a70aE5Ae0614aD7f5",  # v1.0.0
            "0x655A9e6b044d6B62F393f9990ec3eA877e966e18",  # v1.1.1
            # '',  # v1.2.0
            "0xDaB5dc22350f9a6Aff03Cf3D9341aAD0ba42d2a6",  # v1.3.0
        ]

        for safe in safes:
            with self.subTest(safe=safe):
                self.assertTrue(proxy_factory.check_proxy_code(safe))

    def test_deploy_proxy_contract(self):
        s = 15
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        payment_token = None
        safe_creation_tx = Safe.build_safe_creation_tx(
            self.ethereum_client,
            self.safe_contract_V0_0_1_address,
            s,
            owners,
            threshold,
            self.gas_price,
            payment_token,
            payment_receiver=self.ethereum_test_account.address,
        )
        # Send ether for safe deploying costs
        self.send_tx(
            {"to": safe_creation_tx.safe_address, "value": safe_creation_tx.payment},
            self.ethereum_test_account,
        )

        proxy_factory = ProxyFactory(
            self.proxy_factory_contract_address, self.ethereum_client
        )
        ethereum_tx_sent = proxy_factory.deploy_proxy_contract(
            self.ethereum_test_account,
            safe_creation_tx.master_copy,
            safe_creation_tx.safe_setup_data,
            safe_creation_tx.gas,
            gas_price=self.gas_price,
        )
        receipt = self.ethereum_client.get_transaction_receipt(
            ethereum_tx_sent.tx_hash, timeout=20
        )
        self.assertEqual(receipt.status, 1)
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(
            safe.retrieve_master_copy_address(), safe_creation_tx.master_copy
        )
        self.assertEqual(set(safe.retrieve_owners()), set(owners))

    def test_deploy_proxy_contract_with_nonce(self):
        salt_nonce = generate_salt_nonce()
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        payment_token = None
        safe_create2_tx = Safe.build_safe_create2_tx(
            self.ethereum_client,
            self.safe_contract_address,
            self.proxy_factory_contract_address,
            salt_nonce,
            owners,
            threshold,
            self.gas_price,
            payment_token,
        )
        # Send ether for safe deploying costs
        self.send_tx(
            {"to": safe_create2_tx.safe_address, "value": safe_create2_tx.payment},
            self.ethereum_test_account,
        )

        proxy_factory = ProxyFactory(
            self.proxy_factory_contract_address, self.ethereum_client
        )
        ethereum_tx_sent = proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            safe_create2_tx.master_copy_address,
            safe_create2_tx.safe_setup_data,
            salt_nonce,
            safe_create2_tx.gas,
            gas_price=self.gas_price,
        )
        receipt = self.ethereum_client.get_transaction_receipt(
            ethereum_tx_sent.tx_hash, timeout=20
        )
        self.assertEqual(receipt.status, 1)
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(
            ethereum_tx_sent.contract_address, safe_create2_tx.safe_address
        )
        self.assertEqual(set(safe.retrieve_owners()), set(owners))
        self.assertEqual(
            safe.retrieve_master_copy_address(), safe_create2_tx.master_copy_address
        )

    def test_get_proxy_runtime_code(self):
        self.assertGreater(len(self.proxy_factory.get_proxy_runtime_code()), 4)
