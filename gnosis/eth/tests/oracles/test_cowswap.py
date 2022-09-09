from unittest import mock

from django.test import TestCase

from eth_account import Account
from requests import Session

from ... import EthereumClient
from ...oracles import CannotGetPriceFromOracle, CowswapOracle
from ..ethereum_test_case import EthereumTestCaseMixin
from ..test_oracles import (
    dai_token_mainnet_address,
    usdc_token_mainnet_address,
    usdt_token_mainnet_address,
    weth_token_mainnet_address,
)
from ..utils import just_test_if_mainnet_node


class TestCowswapOracle(EthereumTestCaseMixin, TestCase):
    def test_get_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)

        self.assertTrue(CowswapOracle.is_available(ethereum_client))

        cowswap_oracle = CowswapOracle(ethereum_client)

        price = cowswap_oracle.get_price(weth_token_mainnet_address)
        self.assertEqual(price, 1.0)

        price = cowswap_oracle.get_price(dai_token_mainnet_address)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        price = cowswap_oracle.get_price(
            weth_token_mainnet_address, dai_token_mainnet_address
        )
        self.assertGreater(price, 1)

        # Test with 2 stablecoins with same decimals
        price = cowswap_oracle.get_price(
            usdt_token_mainnet_address, usdc_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)

        # Test with 2 stablecoins with different decimals
        price = cowswap_oracle.get_price(
            dai_token_mainnet_address, usdc_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)

        price = cowswap_oracle.get_price(
            usdc_token_mainnet_address, dai_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)

        with mock.patch.object(Session, "get", side_effect=IOError("Connection Error")):
            with self.assertRaisesMessage(
                CannotGetPriceFromOracle,
                f"Cannot get price from CowSwap "
                f"{{}} "
                f"for token-1={usdc_token_mainnet_address} to token-2={dai_token_mainnet_address}",
            ):
                cowswap_oracle.get_price(
                    usdc_token_mainnet_address, dai_token_mainnet_address
                )

        random_token = Account.create().address
        with self.assertRaisesMessage(
            CannotGetPriceFromOracle,
            f"Cannot get decimals for token={random_token}",
        ):
            cowswap_oracle.get_price(random_token)

        with mock.patch(
            "gnosis.eth.oracles.cowswap.get_decimals", autospec=True, return_value=18
        ):
            with self.assertRaisesMessage(
                CannotGetPriceFromOracle,
                f"Cannot get price from CowSwap "
                f"{{'errorType': 'UnsupportedToken', 'description': 'Token address {random_token.lower()}'}} "
                f"for token-1={random_token} to token-2={weth_token_mainnet_address}",
            ):
                cowswap_oracle.get_price(random_token)
