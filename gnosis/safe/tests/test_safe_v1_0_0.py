from eth_account import Account
from packaging.version import Version

from ...eth.constants import NULL_ADDRESS
from .. import Safe
from .test_safe import TestSafe as BaseTestSafe


class TestSafeV100(BaseTestSafe):
    @property
    def safe_contract(self):
        """
        :return: Last Safe Contract available
        """
        return self.safe_contract_V1_0_0

    def deploy_test_safe(self, *args, **kwargs):
        if "fallback_handler" in kwargs:
            kwargs.pop("fallback_handler")  # It's not supported
        return self.deploy_test_safe_v1_0_0(*args, **kwargs)

    def test_create(self):
        # Create test is creating new version of the Safe
        pass

    def test_send_multisig_tx(self):
        # TODO Check this test
        pass

    def test_retrieve_fallback_handler(self):
        # Fallback handler must be empty in Safes < v1.1.0
        safe = self.deploy_test_safe()
        self.assertEqual(safe.retrieve_fallback_handler(), NULL_ADDRESS)

    def test_retrieve_guard(self):
        # Test guard must be empty in Safes < v1.2.0
        safe = self.deploy_test_safe()
        self.assertEqual(safe.retrieve_guard(), NULL_ADDRESS)
        self.assertLess(Version(safe.retrieve_version()), Version("1.3.0"))

    def test_retrieve_modules(self):
        safe = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        safe_contract = safe.contract
        module_address = Account.create().address
        self.assertEqual(safe.retrieve_modules(), [])

        tx = safe_contract.functions.enableModule(module_address).build_transaction(
            {"from": self.ethereum_test_account.address, "gas": 0, "gasPrice": 0}
        )
        safe_tx = safe.build_multisig_tx(safe.address, 0, tx["data"])
        safe_tx.sign(self.ethereum_test_account.key)
        safe_tx.execute(
            tx_sender_private_key=self.ethereum_test_account.key,
            tx_gas_price=self.gas_price,
        )
        self.assertEqual(safe.retrieve_modules(), [module_address])
        self.assertEqual(safe.retrieve_all_info().modules, [module_address])

    def test_retrieve_modules_unitialized_safe(self):
        """
        Unitialized Safes from V1.4.1 will revert
        """

        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract.address,
            initializer=b"",
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_modules(), [])
