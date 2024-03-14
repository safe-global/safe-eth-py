from unittest import TestCase

from ...account_abstraction import UserOperation
from ..mocks.mock_bundler import (
    safe_4337_chain_id_mock,
    safe_4337_user_operation_hash_mock,
    user_operation_mock,
)


class TestUserOperation(TestCase):
    def test_calculate_user_operation_hash(self):
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()
        user_operation = UserOperation.from_bundler_response(
            user_operation_hash, user_operation_mock["result"]
        )
        self.assertEqual(
            user_operation.calculate_user_operation_hash(safe_4337_chain_id_mock),
            safe_4337_user_operation_hash_mock,
        )
