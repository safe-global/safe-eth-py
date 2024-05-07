import os

from django.test import TestCase

import pytest

from ...account_abstraction import BundlerClient, UserOperation, UserOperationReceipt
from ...account_abstraction.user_operation import UserOperationV07
from ..mocks.mock_bundler import (
    safe_4337_chain_id_mock,
    safe_4337_user_operation_hash_mock,
    user_operation_mock,
    user_operation_receipt_mock,
    user_operation_v07_chain_id,
    user_operation_v07_hash,
)


class TestE2EBundlerClient(TestCase):
    def setUp(self):
        bundler_client_variable_name = "ETHEREUM_4337_BUNDLER_URL"
        bundler_client_url = os.environ.get(bundler_client_variable_name)
        if not bundler_client_url:
            pytest.skip(f"{bundler_client_variable_name} needs to be defined")

        self.bundler = BundlerClient(bundler_client_url)

    def test_get_chain_id(self):
        self.assertGreater(self.bundler.get_chain_id(), 0)

    def test_get_user_operation_by_hash(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()

        expected_user_operation = UserOperation.from_bundler_response(
            user_operation_hash, user_operation_mock["result"]
        )
        user_operation = self.bundler.get_user_operation_by_hash(user_operation_hash)
        self.assertEqual(
            user_operation,
            expected_user_operation,
        )
        self.assertEqual(
            user_operation.calculate_user_operation_hash(safe_4337_chain_id_mock).hex(),
            user_operation_hash,
        )

    def test_get_user_operation_V07_by_hash(self):
        """
        Test UserOperation v0.7
        """
        user_operation_hash = user_operation_v07_hash.hex()
        user_operation = self.bundler.get_user_operation_by_hash(user_operation_hash)
        self.assertIsInstance(user_operation, UserOperationV07)
        self.assertEqual(
            user_operation.calculate_user_operation_hash(
                user_operation_v07_chain_id
            ).hex(),
            user_operation_hash,
        )

    def test_get_user_operation_receipt(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()
        expected_user_operation_receipt = UserOperationReceipt.from_bundler_response(
            user_operation_receipt_mock["result"]
        )

        self.assertEqual(
            self.bundler.get_user_operation_receipt(user_operation_hash),
            expected_user_operation_receipt,
        )

    @pytest.mark.xfail(reason="Some bundlers don't support batch requests")
    def test_get_user_operation_and_receipt(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()

        expected_user_operation = UserOperation.from_bundler_response(
            user_operation_hash, user_operation_mock["result"]
        )
        expected_user_operation_receipt = UserOperationReceipt.from_bundler_response(
            user_operation_receipt_mock["result"]
        )
        (
            user_operation,
            user_operation_receipt,
        ) = self.bundler.get_user_operation_and_receipt(user_operation_hash)
        self.assertEqual(
            user_operation,
            expected_user_operation,
        )
        self.assertEqual(
            user_operation_receipt,
            expected_user_operation_receipt,
        )

    def test_supported_entry_points(self):
        supported_entry_points = self.bundler.supported_entry_points()
        self.assertIn(len(supported_entry_points), (1, 2))
        self.assertIn(
            "0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789", supported_entry_points
        )
