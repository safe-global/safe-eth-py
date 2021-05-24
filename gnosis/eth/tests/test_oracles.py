from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from eth_account import Account

from .. import EthereumClient
from ..oracles import (BalancerOracle, CannotGetPriceFromOracle, CurveOracle,
                       KyberOracle, MooniswapOracle, SushiswapOracle,
                       UniswapOracle, UniswapV2Oracle, YearnOracle)
from .ethereum_test_case import EthereumTestCaseMixin
from .utils import just_test_if_mainnet_node

gno_token_mainnet_address = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
weth_token_mainnet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

dai_token_mainnet_address = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
usdt_token_mainnet_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7'


class TestOracles(EthereumTestCaseMixin, TestCase):
    def test_kyber_oracle(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        kyber_oracle = KyberOracle(ethereum_client)
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
        uniswap_oracle = UniswapOracle(ethereum_client)
        token_address = dai_token_mainnet_address
        price = uniswap_oracle.get_price(token_address)
        self.assertEqual(uniswap_oracle.get_uniswap_exchange.cache_info().hits, 0)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'Not enough liquidity'):
            token_address = gno_token_mainnet_address
            uniswap_oracle.get_price(token_address)

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
                                      f'Cannot get uniswap v2 price for pair token_1={random_token_address}'):
            uniswap_v2_oracle.get_price(random_token_address)

    @mock.patch.object(UniswapV2Oracle, 'factory_address', return_value='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                       new_callable=mock.PropertyMock)
    @mock.patch.object(UniswapV2Oracle, 'get_decimals', return_value=(18, 3),
                       autospec=True)
    @mock.patch.object(UniswapV2Oracle, 'get_reserves', return_value=(int(1e20), 600),
                       autospec=True)
    def test_get_price_liquidity(self, get_reserves_mock: MagicMock, get_decimals_mock: MagicMock,
                                 factory_address_mock: MagicMock):
        uniswap_v2_oracle = UniswapV2Oracle(self.ethereum_client)
        token_1, token_2 = '0xA14F6F8867DB84a45BCD148bfaf4e4f54B4B9b12', '0xC426A8F4C79EF274Ed93faC9e1A09bFC5659B06B'

        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'Not enough liquidity'):
            uniswap_v2_oracle.get_price(token_1, token_2)

        get_reserves_mock.return_value = (int(1e20), 6000)
        self.assertEqual(uniswap_v2_oracle.get_price(token_1, token_2), 0.06)

        get_reserves_mock.return_value = reversed(get_reserves_mock.return_value)
        self.assertEqual(uniswap_v2_oracle.get_price(token_2, token_1), 0.06)  # Reserves were inverted

    def test_get_pool_token_price(self):
        dai_eth_pool_address = '0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11'
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_v2_oracle = UniswapV2Oracle(ethereum_client)

        price = uniswap_v2_oracle.get_pool_token_price(dai_eth_pool_address)
        self.assertGreater(price, 0.)


class TestSushiSwapOracle(EthereumTestCaseMixin, TestCase):
    def test_get_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        sushiswap_oracle = SushiswapOracle(ethereum_client)

        price = sushiswap_oracle.get_price(gno_token_mainnet_address, weth_token_mainnet_address)
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Test with 2 stablecoins
        price = sushiswap_oracle.get_price(dai_token_mainnet_address, usdt_token_mainnet_address)
        self.assertAlmostEqual(price, 1., delta=0.5)
        self.assertEqual(sushiswap_oracle._decimals_cache[dai_token_mainnet_address], 18)
        self.assertEqual(sushiswap_oracle._decimals_cache[usdt_token_mainnet_address], 6)

        price = sushiswap_oracle.get_price(usdt_token_mainnet_address, dai_token_mainnet_address)
        self.assertAlmostEqual(price, 1., delta=0.5)


class TestCurveOracle(EthereumTestCaseMixin, TestCase):
    def test_get_pool_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        curve_oracle = CurveOracle(ethereum_client)
        curve_token_address = '0xC25a3A3b969415c80451098fa907EC722572917F'  # Curve.fi DAI/USDC/USDT/sUSD

        price = curve_oracle.get_pool_usd_token_price(curve_token_address)
        self.assertAlmostEqual(price, 1., delta=0.5)

        error_message = 'It is not a curve pool token'
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            curve_oracle.get_pool_usd_token_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            curve_oracle.get_pool_usd_token_price(Account.create().address)


class TestYearnOracle(EthereumTestCaseMixin, TestCase):
    def test_get_pool_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        yearn_oracle = YearnOracle(ethereum_client)
        yearn_token_address = '0x5533ed0a3b83F70c3c4a1f69Ef5546D3D4713E44'  # Yearn Curve.fi DAI/USDC/USDT/sUSD
        iearn_token_address = '0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01'  # iearn DAI

        price = yearn_oracle.get_pool_usd_token_price(yearn_token_address)
        self.assertAlmostEqual(price, 1., delta=0.5)

        price = yearn_oracle.get_pool_usd_token_price(iearn_token_address)
        self.assertAlmostEqual(price, 1., delta=0.5)

        error_message = 'It is not a Yearn yVault'
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            yearn_oracle.get_pool_usd_token_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            yearn_oracle.get_pool_usd_token_price(Account.create().address)


class TestBalancerOracle(EthereumTestCaseMixin, TestCase):
    def test_get_pool_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_oracle = UniswapV2Oracle(ethereum_client)
        balancer_oracle = BalancerOracle(ethereum_client, uniswap_oracle)
        balancer_token_address = '0x59A19D8c652FA0284f44113D0ff9aBa70bd46fB4'  # Balancer 80% BAL + 20% WETH

        price = balancer_oracle.get_pool_token_price(balancer_token_address)
        self.assertAlmostEqual(price, 1., delta=0.9)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'It is not a balancer pool token'):
            balancer_oracle.get_pool_token_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'It is not a balancer pool token'):
            balancer_oracle.get_pool_token_price(Account.create().address)


class TestMooniswapOracle(EthereumTestCaseMixin, TestCase):
    def test_get_pool_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_oracle = UniswapV2Oracle(ethereum_client)
        mooniswap_oracle = MooniswapOracle(ethereum_client, uniswap_oracle)
        mooniswap_pool_address = '0x6a11F3E5a01D129e566d783A7b6E8862bFD66CcA'  # 1inch Liquidity Pool (ETH-WBTC)
        other_version_mooniswap_pool_address = '0x8a2f2F8637deb4Ee7C9400A240d27E3A32147dA4'  # Mooniswap V1 (OWL-GNO)

        price = mooniswap_oracle.get_pool_token_price(mooniswap_pool_address)
        self.assertGreater(price, 0)

        price = mooniswap_oracle.get_pool_token_price(other_version_mooniswap_pool_address)
        self.assertGreater(price, 0)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'It is not a mooniswap pool token'):
            mooniswap_oracle.get_pool_token_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, 'It is not a mooniswap pool token'):
            mooniswap_oracle.get_pool_token_price(Account.create().address)
