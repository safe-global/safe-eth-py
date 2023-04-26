from time import time

from django.test import TestCase

import pytest
from eth_account import Account
from web3 import Web3

from ...eth import EthereumNetwork
from ...eth.constants import NULL_ADDRESS
from .. import GnosisProtocolAPI, Order, OrderKind


@pytest.skip("Having issues often", allow_module_level=True)
class TestGnosisProtocolAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mainnet_gnosis_protocol_api = GnosisProtocolAPI(EthereumNetwork.MAINNET)
        cls.goerli_gnosis_protocol_api = GnosisProtocolAPI(EthereumNetwork.GOERLI)
        cls.mainnet_gno_token_address = "0x6810e776880C02933D47DB1b9fc05908e5386b96"
        cls.goerli_cow_token_address = "0x3430d04E42a722c5Ae52C5Bffbf1F230C2677600"

    def test_api_is_available(self):
        random_owner = Account.create().address
        for ethereum_network in (
            EthereumNetwork.MAINNET,
            EthereumNetwork.GOERLI,
            EthereumNetwork.GNOSIS,
        ):
            with self.subTest(ethereum_network=ethereum_network):
                self.assertEqual(
                    self.goerli_gnosis_protocol_api.get_orders(random_owner), []
                )

    def test_get_estimated_amount(self):
        gnosis_protocol_api = GnosisProtocolAPI(EthereumNetwork.MAINNET)
        response = gnosis_protocol_api.get_estimated_amount(
            self.mainnet_gno_token_address,
            self.mainnet_gno_token_address,
            OrderKind.SELL,
            1,
        )
        self.assertDictEqual(
            response,
            {
                "errorType": "SameBuyAndSellToken",
                "description": "Buy token is the same as the sell token.",
            },
        )

        response = gnosis_protocol_api.get_estimated_amount(
            "0x6820e776880c02933d47db1b9fc05908e5386b96",
            self.mainnet_gno_token_address,
            OrderKind.SELL,
            1,
        )
        self.assertIn("errorType", response)
        self.assertIn("description", response)

        response = gnosis_protocol_api.get_estimated_amount(
            self.mainnet_gno_token_address,
            self.mainnet_gnosis_protocol_api.weth_address,
            OrderKind.SELL,
            int(1e18),
        )
        amount = float(response["buyAmount"]) / response["sellAmount"]
        self.assertGreater(amount, 0)
        self.assertLess(amount, 1)

    def test_get_fee(self):
        order = Order(
            sellToken=self.mainnet_gno_token_address,
            buyToken=self.mainnet_gno_token_address,
            receiver=NULL_ADDRESS,
            sellAmount=int(1e18),
            buyAmount=1,
            validTo=int(time()) + 3600,
            appData=Web3.keccak(text="hola"),
            feeAmount=0,
            kind="sell",
            partiallyFillable=False,
            sellTokenBalance="erc20",
            buyTokenBalance="erc20",
        )
        from_address = Account.create().address
        self.assertEqual(
            self.mainnet_gnosis_protocol_api.get_fee(order, from_address),
            {
                "errorType": "SameBuyAndSellToken",
                "description": "Buy token is the same as the sell token.",
            },
        )
        order.buyToken = self.mainnet_gnosis_protocol_api.weth_address
        self.assertGreaterEqual(
            self.mainnet_gnosis_protocol_api.get_fee(order, from_address), 0
        )

    def test_get_trades(self):
        mainnet_order_ui = "0x65F1206182C77A040ED41D507B59C622FA94AB5E71CCA567202CFF3909F3D5C4DBE338E45276630FD8237149DD47EE027AF26F9C619723D0"
        self.assertEqual(
            self.mainnet_gnosis_protocol_api.get_trades(order_ui=mainnet_order_ui),
            [
                {
                    "blockNumber": 13643462,
                    "logIndex": 0,
                    "orderUid": "0x65f1206182c77a040ed41d507b59c622fa94ab5e71cca567202cff3909f3d5c4dbe338e45276630fd8237149dd47ee027af26f9c619723d0",
                    "buyAmount": "28361861093850079821",
                    "sellAmount": "113521821882",
                    "sellAmountBeforeFees": "113465370931",
                    "owner": "0xdbe338e45276630fd8237149dd47ee027af26f9c",
                    "buyToken": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                    "sellToken": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "txHash": "0x691d1a8ba39c036e841b6e2ed970f9068ac4a27b61955afb852f11019f2ff4d8",
                }
            ],
        )

    def test_place_order(self):
        order = Order(
            sellToken=self.mainnet_gno_token_address,
            buyToken=self.mainnet_gno_token_address,
            receiver=NULL_ADDRESS,
            sellAmount=1,
            buyAmount=1,
            validTo=int(time()) + 3600,
            appData=Web3.keccak(text="hola"),
            feeAmount=0,
            kind="sell",
            partiallyFillable=False,
            sellTokenBalance="erc20",
            buyTokenBalance="erc20",
        )
        result = self.goerli_gnosis_protocol_api.place_order(
            order, Account().create().key
        )
        self.assertEqual(
            order.feeAmount, 0
        )  # Cannot estimate, as buy token is the same as the sell token
        self.assertEqual(
            result,
            {
                "description": "Buy token is the same as the sell token.",
                "errorType": "SameBuyAndSellToken",
            },
        )

        order.sellToken = self.goerli_gnosis_protocol_api.weth_address
        order.buyToken = self.goerli_cow_token_address
        order_id = self.goerli_gnosis_protocol_api.place_order(
            order, Account().create().key
        )

        if type(order_id) is dict:
            pytest.xfail(order_id["errorType"])
        else:
            self.assertEqual(order_id[:2], "0x")
            self.assertEqual(len(order_id), 114)
