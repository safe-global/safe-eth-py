from django.test import TestCase

from ... import EthereumClient
from ...oracles import SushiswapOracle
from ...oracles.utils import get_decimals as oracles_get_decimals
from ..ethereum_test_case import EthereumTestCaseMixin
from ..test_oracles import (
    dai_token_mainnet_address,
    usdt_token_mainnet_address,
    wbtc_token_mainnet_address,
    weth_token_mainnet_address,
)
from ..utils import just_test_if_mainnet_node


class TestSushiSwapOracle(EthereumTestCaseMixin, TestCase):
    def test_get_price(self):
        oracles_get_decimals.cache_clear()
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)

        self.assertTrue(SushiswapOracle.is_available(ethereum_client))
        sushiswap_oracle = SushiswapOracle(ethereum_client)

        price = sushiswap_oracle.get_price(
            wbtc_token_mainnet_address, weth_token_mainnet_address
        )
        self.assertGreater(price, 0)
        self.assertEqual(oracles_get_decimals.cache_info().currsize, 2)

        # Test with 2 stablecoins
        price = sushiswap_oracle.get_price(
            dai_token_mainnet_address, usdt_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)
        self.assertEqual(oracles_get_decimals.cache_info().currsize, 4)

        self.assertEqual(oracles_get_decimals.cache_info().hits, 0)
        self.assertEqual(
            oracles_get_decimals(dai_token_mainnet_address, ethereum_client), 18
        )
        self.assertEqual(
            oracles_get_decimals(usdt_token_mainnet_address, ethereum_client), 6
        )
        self.assertEqual(oracles_get_decimals.cache_info().hits, 2)

        price = sushiswap_oracle.get_price(
            usdt_token_mainnet_address, dai_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)
        self.assertEqual(oracles_get_decimals.cache_info().currsize, 4)
        self.assertEqual(oracles_get_decimals.cache_info().hits, 4)
        oracles_get_decimals.cache_clear()
