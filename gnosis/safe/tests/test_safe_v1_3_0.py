from .. import Safe
from .test_safe import TestSafe as BaseTestSafe  # So it's not run twice by pytest


class TestSafeV130(BaseTestSafe):
    @property
    def safe_contract(self):
        """
        :return: Last Safe Contract available
        """
        return self.safe_contract_V1_3_0

    def deploy_test_safe(self, *args, **kwargs):
        return self.deploy_test_safe_v1_3_0(*args, **kwargs)

    def test_retrieve_modules_unitialized_safe(self):
        """
         An unitialized V1.3.0 Safe will return `[[], '0x0000000000000000000000000000000000000000']` when calling
        `getModulesPaginated`, as `SENTINEL_ADDRESS` is only set when initialized
        """

        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract.address,
            initializer=b"",
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_modules(), [])
        self.assertEqual(safe.retrieve_all_info().modules, [])
