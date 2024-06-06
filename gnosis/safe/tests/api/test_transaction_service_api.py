import copy
from unittest import mock
from unittest.mock import MagicMock, PropertyMock, patch

from django.test import TestCase

from eth_account import Account
from eth_typing import HexStr
from hexbytes import HexBytes

from gnosis.eth import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin
from gnosis.safe import SafeTx
from gnosis.safe.api.transaction_service_api import (
    ApiSafeTxHashNotMatchingException,
    TransactionServiceApi,
)

from ...api import SafeAPIException
from ..mocks.mock_transactions import (
    transaction_data_decoded_mock,
    transaction_data_mock,
    transaction_mock,
)


class TestTransactionServiceAPI(EthereumTestCaseMixin, TestCase):
    def setUp(self) -> None:
        self.transaction_service_api = TransactionServiceApi(
            EthereumNetwork.GNOSIS, ethereum_client=self.ethereum_client
        )
        self.safe_address = "0xAedF684C1c41B51CbD228116e11484425d2FACB9"

    def test_constructor(self):
        ethereum_network = EthereumNetwork.GOERLI
        base_url = "https://safe.global"
        transaction_service_api = TransactionServiceApi(
            ethereum_network, ethereum_client=None, base_url=base_url
        )
        self.assertEqual(transaction_service_api.network, ethereum_network)
        self.assertIsNone(transaction_service_api.ethereum_client)
        self.assertEqual(transaction_service_api.base_url, base_url)

    def test_from_ethereum_client(self):
        with self.assertRaisesMessage(EthereumNetworkNotSupported, "GANACHE"):
            TransactionServiceApi.from_ethereum_client(self.ethereum_client)

        with mock.patch.object(
            EthereumClient, "get_network", return_value=EthereumNetwork.GOERLI
        ):
            transaction_service_api = TransactionServiceApi.from_ethereum_client(
                self.ethereum_client
            )
            self.assertEqual(
                transaction_service_api.ethereum_client, self.ethereum_client
            )
            self.assertEqual(transaction_service_api.network, EthereumNetwork.GOERLI)

    def test_data_decoded_to_text(self):
        decoded_data_text = self.transaction_service_api.data_decoded_to_text(
            transaction_data_mock
        )
        self.assertIn(
            "- changeMasterCopy: 0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F",
            decoded_data_text,
        )
        self.assertIn(
            "- setFallbackHandler: 0xd5D82B6aDDc9027B22dCA772Aa68D5d74cdBdF44",
            decoded_data_text,
        )

    def test_get_balances(self):
        balances = self.transaction_service_api.get_balances(self.safe_address)
        self.assertIsInstance(balances, list)
        self.assertGreaterEqual(len(balances), 1)

    def test_get_transactions(self):
        transactions = self.transaction_service_api.get_transactions(self.safe_address)
        self.assertIsInstance(transactions, list)
        self.assertEqual(len(transactions), 6)

        # Test arguments
        with patch.object(TransactionServiceApi, "_get_request") as mock_get_request:
            self.transaction_service_api.get_transactions(
                self.safe_address, limit=2, nonce__lt=30, failed=False
            )

        expected_url = f"/api/v1/safes/{self.safe_address}/multisig-transactions/?limit=2&nonce__lt=30&failed=False"
        mock_get_request.assert_called_once_with(expected_url)

        # Test valid safe tx has
        with patch.object(
            SafeTx, "safe_version", new_callable=PropertyMock
        ) as mock_safe_version:
            mock_safe_version.return_value = "1.4.1"
            safe_tx_hash = (
                "0x06c88df42a8ab64b2b2c5e2b5c8c4df384c267b39929a8416d1518db23f91783"
            )
            transactions = self.transaction_service_api.get_transactions(
                self.safe_address, safe_tx_hash=safe_tx_hash
            )
            self.assertIsInstance(transactions, list)
            self.assertEqual(len(transactions), 1)

        # Test invalid safe tx hash
        with (
            patch.object(TransactionServiceApi, "_get_request") as mock_get_request,
            patch.object(
                SafeTx, "safe_version", new_callable=PropertyMock
            ) as mock_safe_version,
        ):
            mock_safe_version.return_value = "1.4.1"
            mock_get_request.return_value.ok = True
            mock_get_request.return_value.json = MagicMock(
                return_value={"results": [transaction_mock]}
            )

            safe_tx_invalid_hash = (
                "0x06c88df42a8ab64b2b2c5e2b5c8c4df384c267b39929a8416d1518db23f90000"
            )
            with self.assertRaises(ApiSafeTxHashNotMatchingException) as context:
                self.transaction_service_api.get_transactions(
                    self.safe_address, safe_tx_hash=safe_tx_invalid_hash
                )
            safe_tx_hash_expected = transaction_mock.get("safeTxHash")
            self.assertIn(
                f"API safe-tx-hash: {safe_tx_invalid_hash} doesn't match the calculated safe-tx-hash: {safe_tx_hash_expected}",
                str(context.exception),
            )

    def test_get_safes_for_owner(self):
        owner_address = "0x3066786706Ff0B6e71044e55074dBAE7D01573cB"
        safes = self.transaction_service_api.get_safes_for_owner(owner_address)
        self.assertListEqual(safes, [self.safe_address])

    def test_get_safe_transaction(self):
        safe_tx_hash = HexBytes(
            "0x06c88df42a8ab64b2b2c5e2b5c8c4df384c267b39929a8416d1518db23f91783"
        )
        with (
            patch.object(TransactionServiceApi, "_get_request") as mock_get_request,
            patch.object(
                SafeTx, "safe_version", new_callable=PropertyMock
            ) as mock_safe_version,
        ):
            mock_safe_version.return_value = "1.4.1"
            mock_get_request.return_value.ok = True
            mock_get_request.return_value.json = MagicMock(
                return_value=transaction_mock
            )

            safe_tx, tx_hash = self.transaction_service_api.get_safe_transaction(
                safe_tx_hash
            )
            self.assertEqual(safe_tx.tx_hash, tx_hash)
            self.assertEqual(safe_tx.safe_version, "1.4.1")
            self.assertEqual(safe_tx.safe_tx_hash, safe_tx_hash)

            # Test not executed tx
            not_executed_transaction_mock = copy.deepcopy(transaction_mock)
            not_executed_transaction_mock["transactionHash"] = None
            mock_get_request.return_value.json = MagicMock(
                return_value=not_executed_transaction_mock
            )
            safe_tx, tx_hash = self.transaction_service_api.get_safe_transaction(
                safe_tx_hash
            )
            self.assertIsNone(tx_hash)
            self.assertIsNone(safe_tx.tx_hash)

            # Test invalid safe tx hash
            safe_tx_invalid_hash = HexBytes(
                "0x06c88df42a8ab64b2b2c5e2b5c8c4df384c267b39929a8416d1518db23f90000"
            )
            with self.assertRaises(ApiSafeTxHashNotMatchingException) as context:
                self.transaction_service_api.get_safe_transaction(safe_tx_invalid_hash)

            safe_tx_hash_expected = transaction_mock.get("safeTxHash")
            self.assertIn(
                f"API safe-tx-hash: {safe_tx_invalid_hash.hex()} doesn't match the calculated safe-tx-hash: {safe_tx_hash_expected}",
                str(context.exception),
            )

            # Test response not ok
            mock_get_request.return_value.ok = False
            with self.assertRaises(SafeAPIException) as context:
                self.transaction_service_api.get_safe_transaction(safe_tx_hash)
            self.assertIn(
                f"Cannot get transaction with safe-tx-hash={safe_tx_hash.hex()}:",
                str(context.exception),
            )

    def test_remove_delegate(self):
        with patch.object(
            TransactionServiceApi, "_delete_request"
        ) as mock_delete_request:
            delegate_address = Account().create().address
            delegator_account = Account().create()
            message_hash = self.transaction_service_api.create_delegate_message_hash(
                delegate_address
            )
            signature = delegator_account.signHash(message_hash).signature.hex()
            self.transaction_service_api.remove_delegate(
                delegate_address, delegator_account.address, signature
            )

            expected_url = f"/api/v2/delegates/{delegate_address}/"
            expected_payload = {
                "delegator": delegator_account.address,
                "signature": signature,
            }
            mock_delete_request.assert_called_once_with(expected_url, expected_payload)

            self.transaction_service_api.remove_delegate(
                delegate_address,
                delegator_account.address,
                signature,
                self.safe_address,
            )

            expected_payload = {
                "safe": self.safe_address,
                "delegator": delegator_account.address,
                "signature": signature,
            }
            mock_delete_request.assert_called_with(expected_url, expected_payload)

    def test_add_delegate(self):
        with patch.object(TransactionServiceApi, "_post_request") as mock_post_request:
            delegate_address = Account().create().address
            delegator_account = Account().create()
            message_hash = self.transaction_service_api.create_delegate_message_hash(
                delegate_address
            )
            signature = delegator_account.signHash(message_hash).signature.hex()
            label = "test label"
            self.transaction_service_api.add_delegate(
                delegate_address, delegator_account.address, label, signature
            )

            expected_url = "/api/v2/delegates/"
            expected_payload = {
                "delegate": delegate_address,
                "delegator": delegator_account.address,
                "signature": signature,
                "label": label,
            }
            mock_post_request.assert_called_once_with(expected_url, expected_payload)

            self.transaction_service_api.add_delegate(
                delegate_address,
                delegator_account.address,
                label,
                signature,
                self.safe_address,
            )

            expected_payload = {
                "safe": self.safe_address,
                "delegate": delegate_address,
                "delegator": delegator_account.address,
                "signature": signature,
                "label": label,
            }
            mock_post_request.assert_called_with(expected_url, expected_payload)

    def test_decode_data(self):
        with patch.object(TransactionServiceApi, "_post_request") as mock_post_request:
            mock_post_request.return_value.ok = True
            mock_post_request.return_value.json = MagicMock(
                return_value=transaction_data_decoded_mock
            )
            data = HexStr(
                "0x095ea7b3000000000000000000000000e6fc577e87f7c977c4393300417dcc592d90acf8ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            )
            to_address = "0x4127839cdf4F73d9fC9a2C2861d8d1799e9DF40C"
            decoded_data = self.transaction_service_api.decode_data(data, to_address)
            expected_url = "/api/v1/data-decoder/"
            expected_payload = {"data": HexBytes(data).hex(), "to": to_address}
            mock_post_request.assert_called_once_with(expected_url, expected_payload)
            self.assertEqual(decoded_data.get("method"), "approve")
            self.assertEqual(decoded_data.get("parameters")[0].get("name"), "spender")
            self.assertEqual(decoded_data.get("parameters")[1].get("name"), "value")

            # Test response not ok
            mock_post_request.return_value.ok = False
            with self.assertRaises(SafeAPIException) as context:
                self.transaction_service_api.decode_data(data, to_address)
            self.assertIn(
                "Cannot decode tx data:",
                str(context.exception),
            )
