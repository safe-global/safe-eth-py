from ...eth.constants import NULL_ADDRESS
from .test_safe import TestSafe as BaseTestSafe  # So it's not run twice by pytest


class TestSafeV141(BaseTestSafe):
    @property
    def safe_contract(self):
        """
        :return: Safe Contract v1.4.1
        """
        return self.safe_contract_V1_4_1

    def deploy_test_safe(self, *args, **kwargs):
        return self.deploy_test_safe_v1_4_1(*args, **kwargs)

    def test_retrieve_module_guard(self):
        # Module guard (setModuleGuard) was introduced in v1.5.0, must be empty in v1.4.1
        safe = self.deploy_test_safe()
        self.assertEqual(safe.retrieve_module_guard(), NULL_ADDRESS)
