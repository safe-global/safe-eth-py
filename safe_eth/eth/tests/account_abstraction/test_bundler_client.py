import copy
from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

import requests
from eth_typing import HexStr

from ...account_abstraction import (
    BundlerClient,
    BundlerClientConnectionException,
    BundlerClientResponseException,
    UserOperation,
    UserOperationReceipt,
)
from ..mocks.mock_bundler import (
    safe_4337_user_operation_hash_mock,
    supported_entrypoint_mock,
    user_operation_mock,
    user_operation_receipt_mock,
)


class TestBundlerClient(TestCase):
    def setUp(self):
        self.bundler = BundlerClient("https://localhost")

    @mock.patch.object(requests.Session, "post")
    def test_get_user_operation_by_hash(self, mock_session: MagicMock):
        mock_session.return_value.ok = True
        mock_session.return_value.json = MagicMock(
            return_value={"jsonrpc": "2.0", "id": 1, "result": None}
        )
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()

        self.assertIsNone(self.bundler.get_user_operation_by_hash(user_operation_hash))
        mock_session.return_value.json = MagicMock(return_value=user_operation_mock)
        self.bundler.get_user_operation_by_hash.cache_clear()
        expected_user_operation = UserOperation.from_bundler_response(
            HexStr(user_operation_hash), user_operation_mock["result"]
        )
        self.assertEqual(
            self.bundler.get_user_operation_by_hash(user_operation_hash),
            expected_user_operation,
        )

        mock_session.return_value.json = MagicMock(
            return_value={
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32600,
                    "message": "Unspecified origin not on whitelist.",
                },
            }
        )
        self.bundler.get_user_operation_by_hash.cache_clear()
        with self.assertRaises(BundlerClientResponseException):
            self.assertIsNone(
                self.bundler.get_user_operation_by_hash(user_operation_hash)
            )
        mock_session.side_effect = IOError
        with self.assertRaises(BundlerClientConnectionException):
            self.assertIsNone(
                self.bundler.get_user_operation_by_hash(user_operation_hash)
            )

    @mock.patch.object(requests.Session, "post")
    def test_get_user_operation_receipt(self, mock_session: MagicMock):
        mock_session.return_value.ok = True
        mock_session.return_value.json = MagicMock(
            return_value={"jsonrpc": "2.0", "id": 1, "result": None}
        )
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()
        self.assertIsNone(self.bundler.get_user_operation_receipt(user_operation_hash))
        mock_session.return_value.json = MagicMock(
            return_value=copy.deepcopy(user_operation_receipt_mock)
        )
        self.bundler.get_user_operation_receipt.cache_clear()

        expected_user_operation_receipt = UserOperationReceipt.from_bundler_response(
            user_operation_receipt_mock["result"]
        )
        self.assertEqual(
            self.bundler.get_user_operation_receipt(user_operation_hash),
            expected_user_operation_receipt,
        )
        mock_session.return_value.json = MagicMock(
            return_value={
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32600,
                    "message": "Unspecified origin not on whitelist.",
                },
            }
        )
        self.bundler.get_user_operation_receipt.cache_clear()
        with self.assertRaises(BundlerClientResponseException):
            self.assertIsNone(
                self.bundler.get_user_operation_receipt(user_operation_hash)
            )
        mock_session.side_effect = IOError
        with self.assertRaises(BundlerClientConnectionException):
            self.assertIsNone(
                self.bundler.get_user_operation_receipt(user_operation_hash)
            )

    @mock.patch.object(requests.Session, "post")
    def test_get_user_operation_and_receipt(self, mock_session: MagicMock):
        mock_session.return_value.ok = True
        mock_session.return_value.json = MagicMock(
            return_value=[
                {"jsonrpc": "2.0", "id": 1, "result": None},
                {"jsonrpc": "2.0", "id": 2, "result": None},
            ]
        )
        user_operation_hash = safe_4337_user_operation_hash_mock.hex()
        self.assertIsNone(
            self.bundler.get_user_operation_and_receipt(user_operation_hash)
        )
        mock_session.return_value.json = MagicMock(
            return_value=[
                user_operation_mock,
                copy.deepcopy(user_operation_receipt_mock),
            ]
        )
        self.bundler.get_user_operation_and_receipt.cache_clear()
        expected_user_operation = UserOperation.from_bundler_response(
            HexStr(user_operation_hash), user_operation_mock["result"]
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
        self.assertEqual(user_operation_receipt, expected_user_operation_receipt)
        mock_session.return_value.json = MagicMock(
            return_value={
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32600,
                    "message": "Unspecified origin not on whitelist.",
                },
            }
        )
        self.bundler.get_user_operation_and_receipt.cache_clear()
        with self.assertRaises(BundlerClientResponseException):
            self.assertIsNone(
                self.bundler.get_user_operation_and_receipt(user_operation_hash)
            )
        mock_session.side_effect = IOError
        with self.assertRaises(BundlerClientConnectionException):
            self.assertIsNone(
                self.bundler.get_user_operation_and_receipt(user_operation_hash)
            )

    @mock.patch.object(requests.Session, "post")
    def test_supported_entry_points(self, mock_session: MagicMock):
        mock_session.return_value.ok = True
        mock_session.return_value.json = MagicMock(
            return_value=supported_entrypoint_mock
        )

        self.assertEqual(
            self.bundler.supported_entry_points(), supported_entrypoint_mock["result"]
        )
