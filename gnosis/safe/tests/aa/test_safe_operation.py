from unittest import TestCase

from gnosis.eth.account_abstraction import UserOperation
from gnosis.eth.tests.mocks.mock_bundler import (
    safe_4337_chain_id_mock,
    safe_4337_module_address_mock,
    safe_4337_module_domain_separator_mock,
    safe_4337_safe_operation_hash_mock,
    safe_4337_user_operation_hash_mock,
    user_operation_mock,
)

from ...account_abstraction import SafeOperation


class TestSafeOperation(TestCase):
    def test_safe_operation(self):
        safe_operation = SafeOperation.from_user_operation(
            UserOperation(
                safe_4337_user_operation_hash_mock, user_operation_mock["result"]
            )
        )

        self.assertEqual(
            safe_operation.get_domain_separator(
                safe_4337_chain_id_mock, safe_4337_module_address_mock
            ),
            safe_4337_module_domain_separator_mock,
        )
        self.assertEqual(
            safe_operation.get_safe_operation_hash(
                safe_4337_chain_id_mock, safe_4337_module_address_mock
            ),
            safe_4337_safe_operation_hash_mock,
        )
