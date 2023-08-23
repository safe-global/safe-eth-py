import logging

from django.test import TestCase

from gnosis.eth.contracts import get_proxy_1_0_0_deployed_bytecode
from gnosis.eth.utils import compare_byte_code
from gnosis.safe import ProxyFactory

from ...proxy_factory import ProxyFactoryV100
from ..safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestProxyFactoryV100(SafeTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_check_proxy_code(self):
        # Test proxy factory v1.0.0
        ethereum_tx_sent = ProxyFactoryV100.deploy_proxy_factory_contract(
            self.ethereum_client, self.ethereum_test_account
        )
        proxy_factory_V1_0_0 = ProxyFactory(
            ethereum_tx_sent.contract_address, self.ethereum_client, version="1.0.0"
        )
        ethereum_tx_sent = proxy_factory_V1_0_0.deploy_proxy_contract(
            self.ethereum_test_account, self.safe_contract_address
        )
        self.assertTrue(
            self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address)
        )
        deployed_code = self.w3.eth.get_code(ethereum_tx_sent.contract_address)
        self.assertTrue(
            compare_byte_code(get_proxy_1_0_0_deployed_bytecode(), deployed_code)
        )
