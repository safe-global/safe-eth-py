from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from eth_account import Account

from .. import EthereumClient
from ..oracles import (CannotGetPriceFromOracle, KyberOracle, UniswapOracle,
                       UniswapV2Oracle)
from .ethereum_test_case import EthereumTestCaseMixin
from .utils import just_test_if_mainnet_node

gno_token_mainnet_address = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
weth_token_mainnet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

kyber_proxy_mainnet_address = '0x818E6FECD516Ecc3849DAf6845e3EC868087B755'
uniswap_proxy_mainnet_address = '0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95'

dai_token_mainnet_address = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
usdt_token_mainnet_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7'


class TestOracles(EthereumTestCaseMixin, TestCase):
    def test_kyber_oracle(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        kyber_oracle = KyberOracle(ethereum_client, kyber_proxy_mainnet_address)
        price = kyber_oracle.get_price(gno_token_mainnet_address, weth_token_mainnet_address)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Test with 2 stablecoins
        price = kyber_oracle.get_price(dai_token_mainnet_address, usdt_token_mainnet_address)
        self.assertAlmostEqual(price, 1., delta=0.5)

        price = kyber_oracle.get_price(usdt_token_mainnet_address, dai_token_mainnet_address)
        self.assertAlmostEqual(price, 1., delta=0.5)

    def test_kyber_oracle_not_deployed(self):
        kyber_oracle = KyberOracle(self.ethereum_client, Account.create().address)
        random_token_address = Account.create().address
        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'Cannot get price from kyber-network-proxy'):
            kyber_oracle.get_price(random_token_address)

    def test_uniswap_oracle(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_oracle = UniswapOracle(ethereum_client, uniswap_proxy_mainnet_address)
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

    def test_uniswap_oracle_not_deployed(self):
        uniswap_oracle = UniswapOracle(self.ethereum_client, Account.create().address)
        random_token_address = Account.create().address
        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'Non existing uniswap exchange'):
            uniswap_oracle.get_price(random_token_address)


class TestUniswapV2Oracle(EthereumTestCaseMixin, TestCase):
    @mock.patch.object(UniswapV2Oracle, 'factory_address', return_value='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                       new_callable=mock.PropertyMock)
    def test_calculate_pair_address(self, factory_address_mock: MagicMock):
        uniswap_v2_oracle = UniswapV2Oracle(self.ethereum_client)
        expected_address = '0x3e8468f66d30Fc99F745481d4B383f89861702C6'

        self.assertEqual(uniswap_v2_oracle.calculate_pair_address(gno_token_mainnet_address,
                                                                  weth_token_mainnet_address), expected_address)
        self.assertEqual(uniswap_v2_oracle.calculate_pair_address(weth_token_mainnet_address,
                                                                  gno_token_mainnet_address), expected_address)

    def test_get_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_v2_oracle = UniswapV2Oracle(ethereum_client)

        price = uniswap_v2_oracle.get_price(gno_token_mainnet_address, weth_token_mainnet_address)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Test with 2 stablecoins
        price = uniswap_v2_oracle.get_price(dai_token_mainnet_address, usdt_token_mainnet_address)
        self.assertAlmostEqual(price, 1., delta=0.5)
        self.assertEqual(uniswap_v2_oracle._decimals_cache[dai_token_mainnet_address], 18)
        self.assertEqual(uniswap_v2_oracle._decimals_cache[usdt_token_mainnet_address], 6)

        price = uniswap_v2_oracle.get_price(usdt_token_mainnet_address, dai_token_mainnet_address)
        self.assertAlmostEqual(price, 1., delta=0.5)

    def test_get_price_contract_not_deployed(self):
        uniswap_v2_oracle = UniswapV2Oracle(self.ethereum_client)
        random_token_address = Account.create().address
        with self.assertRaisesMessage(CannotGetPriceFromOracle,
                                      f'Cannot get uniswap v2 token balance for token={random_token_address}'):
            uniswap_v2_oracle.get_price(random_token_address)
