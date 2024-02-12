from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

import requests

from ..bundler_client import BundlerClient
from .mocks.mock_bundler import (
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
        user_operation_hash = (
            "0x5ca9bed4befc5ffa1c5e42fff0348b5013a6ccdd6887a5d0b0409080fe87edcc"
        )
        self.assertIsNone(self.bundler.get_user_operation_by_hash(user_operation_hash))
        mock_session.return_value.json = MagicMock(return_value=user_operation_mock)
        self.assertEqual(
            self.bundler.get_user_operation_by_hash(user_operation_hash),
            user_operation_mock["result"],
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
        self.assertIsNone(self.bundler.get_user_operation_by_hash(user_operation_hash))

    @mock.patch.object(requests.Session, "post")
    def test_get_user_operation_receipt(self, mock_session: MagicMock):
        mock_session.return_value.ok = True
        mock_session.return_value.json = MagicMock(
            return_value={"jsonrpc": "2.0", "id": 1, "result": None}
        )
        user_operation_hash = (
            "0x5ca9bed4befc5ffa1c5e42fff0348b5013a6ccdd6887a5d0b0409080fe87edcc"
        )
        self.assertIsNone(self.bundler.get_user_operation_receipt(user_operation_hash))
        mock_session.return_value.json = MagicMock(
            return_value=user_operation_receipt_mock
        )
        self.assertEqual(
            self.bundler.get_user_operation_receipt(user_operation_hash),
            user_operation_receipt_mock["result"],
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
        self.assertIsNone(self.bundler.get_user_operation_receipt(user_operation_hash))

    @mock.patch.object(requests.Session, "post")
    def test_supported_entry_points(self, mock_session: MagicMock):
        mock_session.return_value.ok = True
        mock_session.return_value.json = MagicMock(
            return_value=supported_entrypoint_mock
        )

        self.assertEqual(
            self.bundler.supported_entry_points(), supported_entrypoint_mock["result"]
        )
