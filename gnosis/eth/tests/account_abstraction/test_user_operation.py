from unittest import TestCase

from ...account_abstraction import UserOperation
from ...account_abstraction.user_operation import UserOperationV07
from ..mocks.mock_bundler import (
    safe_4337_chain_id_mock,
    safe_4337_user_operation_hash_mock,
    user_operation_mock,
    user_operation_v07_hash,
    user_operation_v07_mock,
)


class TestUserOperation(TestCase):
    def test_calculate_user_operation_hash_V06(self):
        user_operation_hash = safe_4337_user_operation_hash_mock
        user_operation = UserOperation.from_bundler_response(
            user_operation_hash.hex(), user_operation_mock["result"]
        )
        self.assertIsInstance(user_operation, UserOperation)
        self.assertEqual(
            user_operation.calculate_user_operation_hash(safe_4337_chain_id_mock),
            user_operation_hash,
        )

    def test_calculate_user_operation_hash_V07(self):
        user_operation_hash = user_operation_v07_hash
        user_operation = UserOperation.from_bundler_response(
            user_operation_hash.hex(), user_operation_v07_mock["result"]
        )
        self.assertIsInstance(user_operation, UserOperationV07)
        self.assertEqual(
            user_operation.calculate_user_operation_hash(safe_4337_chain_id_mock),
            user_operation_hash,
        )
