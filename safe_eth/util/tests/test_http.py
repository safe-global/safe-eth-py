from unittest import TestCase

from safe_eth.util.http import build_full_url


class TestHttpUtils(TestCase):
    def test_build_full_url(self):
        result = build_full_url(
            "localhost:8000/txs", "/api/v1/multisig-transactions/12345/"
        )
        self.assertEqual(
            result, "http://localhost:8000/txs/api/v1/multisig-transactions/12345/"
        )

        result = build_full_url(
            "http://localhost:8000/txs", "api/v1/multisig-transactions/12345/"
        )
        self.assertEqual(
            result, "http://localhost:8000/txs/api/v1/multisig-transactions/12345/"
        )

        result = build_full_url(
            "localhost:8000", "/txs/api/v1/multisig-transactions/12345/"
        )
        self.assertEqual(
            result, "http://localhost:8000/txs/api/v1/multisig-transactions/12345/"
        )

        result = build_full_url(
            "http://localhost:8000", "txs/api/v1/multisig-transactions/12345/"
        )
        self.assertEqual(
            result, "http://localhost:8000/txs/api/v1/multisig-transactions/12345/"
        )

        result = build_full_url(
            "https://safe-transaction-sepolia.safe.global",
            "/api/v1/multisig-transactions/12345/",
        )
        self.assertEqual(
            result,
            "https://safe-transaction-sepolia.safe.global/api/v1/multisig-transactions/12345/",
        )

        result = build_full_url(
            "https://safe-transaction-sepolia.safe.global/",
            "api/v1/multisig-transactions/12345/",
        )
        self.assertEqual(
            result,
            "https://safe-transaction-sepolia.safe.global/api/v1/multisig-transactions/12345/",
        )
