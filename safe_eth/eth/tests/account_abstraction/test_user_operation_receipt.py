from unittest import TestCase

from ...account_abstraction import UserOperationReceipt
from ..mocks.mock_bundler import user_operation_receipt_mock


class TestUserOperation(TestCase):
    def setUp(self):
        super().setUp()
        self.user_operation_receipt = UserOperationReceipt.from_bundler_response(
            user_operation_receipt_mock["result"]
        )

    def test_get_deployed_account(self):
        self.assertEqual(
            self.user_operation_receipt.get_deployed_account(),
            self.user_operation_receipt.sender,
        )

    def test_get_deposit(self):
        expected_value = 759_940_285_250_436
        self.assertEqual(self.user_operation_receipt.get_deposit(), expected_value)

    def test_get_module_address(self):
        expected_value = "0xa581c4A4DB7175302464fF3C06380BC3270b4037"
        self.assertEqual(
            self.user_operation_receipt.get_module_address(), expected_value
        )
