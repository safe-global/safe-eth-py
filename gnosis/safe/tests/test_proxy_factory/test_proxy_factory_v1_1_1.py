import logging

from django.test import TestCase

from gnosis.safe import ProxyFactory

from ..safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestProxyFactoryV1_1_1(SafeTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_check_proxy_code(self):
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
