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
from ...account_abstraction.safe_operation import _domain_separator_cache


class TestSafeOperation(TestCase):
    def setUp(self):
        _domain_separator_cache.clear()

    def tearDown(self):
        _domain_separator_cache.clear()

    def test_safe_operation(self):
        safe_operation = SafeOperation.from_user_operation(
            UserOperation.from_bundler_response(
                safe_4337_user_operation_hash_mock, user_operation_mock["result"]
            )
        )

        self.assertDictEqual(_domain_separator_cache, {})

        self.assertEqual(
            safe_operation.get_domain_separator(
                safe_4337_chain_id_mock, safe_4337_module_address_mock
            ),
            safe_4337_module_domain_separator_mock,
        )
        self.assertDictEqual(
            _domain_separator_cache,
            {
                (
                    safe_4337_chain_id_mock,
                    safe_4337_module_address_mock,
                ): safe_4337_module_domain_separator_mock
            },
        )

        self.assertEqual(
            safe_operation.get_safe_operation_hash(
                safe_4337_chain_id_mock, safe_4337_module_address_mock
            ),
            safe_4337_safe_operation_hash_mock,
        )
        self.assertDictEqual(
            _domain_separator_cache,
            {
                (
                    safe_4337_chain_id_mock,
                    safe_4337_module_address_mock,
                ): safe_4337_module_domain_separator_mock
            },
        )
