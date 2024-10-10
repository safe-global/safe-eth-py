from unittest import TestCase

from safe_eth.eth.proxies import SafeProxy
from safe_eth.safe.tests.safe_test_case import SafeTestCaseMixin


class TestSafeProxy(SafeTestCaseMixin, TestCase):
    def test_get_implementation_address(self):
        safe = self.deploy_test_safe_v1_4_1()
        self.assertEqual(
            safe.retrieve_master_copy_address(), self.safe_contract_V1_4_1.address
        )

        safe_proxy = SafeProxy(safe.address, self.ethereum_client)
        self.assertEqual(
            safe_proxy.get_implementation_address(), self.safe_contract_V1_4_1.address
        )
