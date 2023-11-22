from unittest import mock

from django.test import TestCase

from gnosis.eth import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin

from ...api.transaction_service_api import TransactionServiceApi


class TestTransactionServiceAPI(EthereumTestCaseMixin, TestCase):
    def setUp(self) -> None:
        self.transaction_service_api = TransactionServiceApi(
            EthereumNetwork.GOERLI, ethereum_client=self.ethereum_client
        )
        self.safe_address = "0x24833C9c4644a70250BCCBcB5f8529b609eaE6EC"

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
        test_data = {
            "method": "multiSend",
            "parameters": [
                {
                    "name": "transactions",
                    "type": "bytes",
                    "value": "0x00c68877b75c3f9b950a798f9c9df4cde121c432ed000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000247de7edef00000000000000000000000034cfac646f301356faa8b21e94227e3583fe3f5f00c68877b75c3f9b950a798f9c9df4cde121c432ed00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000024f08a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf44",
                    "decodedValue": [
                        {
                            "operation": "CALL",
                            "to": "0xc68877B75c3f9b950a798f9C9dF4cDE121C432eD",
                            "value": 0,
                            "data": "0x7de7edef00000000000000000000000034cfac646f301356faa8b21e94227e3583fe3f5f",
                            "decodedData": {
                                "method": "changeMasterCopy",
                                "parameters": [
                                    {
                                        "name": "_masterCopy",
                                        "type": "address",
                                        "value": "0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F",
                                    }
                                ],
                            },
                        },
                        {
                            "operation": "CALL",
                            "to": "0xc68877B75c3f9b950a798f9C9dF4cDE121C432eD",
                            "value": 0,
                            "data": "0xf08a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf44",
                            "decodedData": {
                                "method": "setFallbackHandler",
                                "parameters": [
                                    {
                                        "name": "handler",
                                        "type": "address",
                                        "value": "0xd5D82B6aDDc9027B22dCA772Aa68D5d74cdBdF44",
                                    }
                                ],
                            },
                        },
                    ],
                }
            ],
        }
        decoded_data_text = self.transaction_service_api.data_decoded_to_text(test_data)
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

    def test_get_transactions(self):
        transactions = self.transaction_service_api.get_transactions(self.safe_address)
        self.assertIsInstance(transactions, list)

    def test_get_safes_for_owner(self):
        owner_address = "0x5aC255889882aCd3da2aA939679E3f3d4cea221e"
        safes = self.transaction_service_api.get_safes_for_owner(owner_address)
        self.assertIn(self.safe_address, safes)
