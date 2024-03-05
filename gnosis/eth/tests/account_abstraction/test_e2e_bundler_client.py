import os

from django.test import TestCase

import pytest

from ...account_abstraction import BundlerClient, UserOperation
from ..mocks.mock_bundler import (
    safe_4337_user_operation_hash_mock,
    supported_entrypoint_mock,
    user_operation_mock,
    user_operation_receipt_mock,
    user_operation_receipt_parsed_mock,
)


class TestE2EBundlerClient(TestCase):
    def setUp(self):
        bundler_client_variable_name = "BUNDLER_CLIENT_URL"
        bundler_client_url = os.environ.get(bundler_client_variable_name)
        if not bundler_client_url:
            pytest.skip(f"{bundler_client_variable_name} needs to be defined")

        self.bundler = BundlerClient(bundler_client_url)

    def test_get_user_operation_by_hash(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()

        expected_user_operation = UserOperation.from_bundler_response(
            user_operation_hash, user_operation_mock["result"]
        )
        self.assertEqual(
            self.bundler.get_user_operation_by_hash(user_operation_hash),
            expected_user_operation,
        )

    def test_get_user_operation_receipt(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()

        self.assertEqual(
            self.bundler.get_user_operation_receipt(user_operation_hash),
            user_operation_receipt_mock["result"],
        )

    @pytest.mark.xfail(reason="Some bundlers don't support batch requests")
    def test_get_user_operation_and_receipt(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()

        expected_user_operation = UserOperation.from_bundler_response(
            user_operation_hash, user_operation_mock["result"]
        )
        (
            user_operation,
            user_operation_receipt,
        ) = self.bundler.get_user_operation_and_receipt(user_operation_hash)
        self.assertEqual(
            user_operation,
            expected_user_operation,
        )
        self.assertDictEqual(
            user_operation_receipt,
            user_operation_receipt_parsed_mock["result"],
        )

    def test_supported_entry_points(self):
        self.assertEqual(
            self.bundler.supported_entry_points(), supported_entrypoint_mock["result"]
        )
