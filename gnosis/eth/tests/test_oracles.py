import os

from django.test import TestCase

import pytest
import requests

from .. import EthereumClient
from ..oracles import KyberOracle, UniswapOracle

MAINNET_NODE = os.environ.get('ETHEREUM_MAINNET_NODE')


if not MAINNET_NODE:
    pytest.skip("Mainnet node not defined, cannot test oracles", allow_module_level=True)
elif requests.get(MAINNET_NODE).status_code == 404:
    pytest.skip("Cannot connect to mainnet node", allow_module_level=True)


class TestOracles(TestCase):
    gno_token_mainnet_address = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
    weth_token_mainnet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

    kyber_proxy_mainnet_address = '0x818E6FECD516Ecc3849DAf6845e3EC868087B755'
    uniswap_proxy_mainnet_address = '0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95'

    def test_kyber_oracle(self):
        ethereum_client = EthereumClient(MAINNET_NODE)
        kyber_oracle = KyberOracle(ethereum_client, self.kyber_proxy_mainnet_address)
        price = kyber_oracle.get_price(self.gno_token_mainnet_address, self.weth_token_mainnet_address)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

    def test_uniswap_oracle(self):
        ethereum_client = EthereumClient(MAINNET_NODE)
        uniswap_oracle = UniswapOracle(ethereum_client, self.uniswap_proxy_mainnet_address)
        token_address = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
        price = uniswap_oracle.get_price(token_address)
        self.assertEqual(uniswap_oracle.get_uniswap_exchange.cache_info().hits, 0)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Check batching is working
        uniswap_exchange = uniswap_oracle.get_uniswap_exchange(token_address)
        self.assertEqual(uniswap_oracle.get_uniswap_exchange.cache_info().hits, 1)
        self.assertEqual(uniswap_oracle._get_balances_using_batching(uniswap_exchange, token_address),
                         uniswap_oracle._get_balances_without_batching(uniswap_exchange, token_address))
