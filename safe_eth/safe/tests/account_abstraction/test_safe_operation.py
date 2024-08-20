import dataclasses
import datetime
import zoneinfo
from unittest import TestCase

from safe_eth.eth.account_abstraction import UserOperation
from safe_eth.eth.tests.mocks.mock_bundler import (
    safe_4337_chain_id_mock,
    safe_4337_module_address_mock,
    safe_4337_module_domain_separator_mock,
    safe_4337_safe_operation_hash_mock,
    safe_4337_user_operation_hash_mock,
    user_operation_mock,
    user_operation_with_valid_dates_hash_mock,
    user_operation_with_valid_dates_mock,
)

from ...account_abstraction import SafeOperation
from ...account_abstraction.safe_operation import _domain_separator_cache


class TestSafeOperation(TestCase):
    def setUp(self):
        _domain_separator_cache.clear()

    def tearDown(self):
        _domain_separator_cache.clear()

    def test_from_user_operation(self):
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

        self.assertIsNone(safe_operation.valid_after_as_datetime)
        self.assertIsNone(safe_operation.valid_until_as_datetime)

    def test_datetime_parse(self):
        safe_operation = SafeOperation.from_user_operation(
            UserOperation.from_bundler_response(
                user_operation_with_valid_dates_hash_mock,
                user_operation_with_valid_dates_mock["result"],
            )
        )

        self.assertEqual(safe_operation.valid_after, 1710848424)
        self.assertEqual(
            safe_operation.valid_after_as_datetime,
            datetime.datetime(
                2024, 3, 19, 11, 40, 24, tzinfo=zoneinfo.ZoneInfo(key="UTC")
            ),
        )
        self.assertEqual(safe_operation.valid_until, 1710908424)
        self.assertEqual(
            safe_operation.valid_until_as_datetime,
            datetime.datetime(
                2024, 3, 20, 4, 20, 24, tzinfo=zoneinfo.ZoneInfo(key="UTC")
            ),
        )

        # Test invalid value cannot be parsed as datetime
        invalid_safe_operation = dataclasses.replace(
            safe_operation,
            valid_after=5555555555555555555555,
            valid_until=666666666666666666666,
        )
        self.assertIsNone(invalid_safe_operation.valid_after_as_datetime)
        self.assertIsNone(invalid_safe_operation.valid_until_as_datetime)
