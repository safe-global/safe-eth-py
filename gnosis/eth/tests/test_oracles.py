from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from eth_account import Account

from .. import EthereumClient
from ..oracles import (
    AaveOracle,
    BalancerOracle,
    CannotGetPriceFromOracle,
    CreamOracle,
    CurveOracle,
    EnzymeOracle,
    KyberOracle,
    MooniswapOracle,
    PoolTogetherOracle,
    SushiswapOracle,
    UniswapOracle,
    UniswapV2Oracle,
    YearnOracle,
    ZerionComposedOracle,
)
from .ethereum_test_case import EthereumTestCaseMixin
from .utils import just_test_if_mainnet_node

gno_token_mainnet_address = "0x6810e776880C02933D47DB1b9fc05908e5386b96"
weth_token_mainnet_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

dai_token_mainnet_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
usdt_token_mainnet_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"


class TestOracles(EthereumTestCaseMixin, TestCase):
    def test_kyber_oracle(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        kyber_oracle = KyberOracle(ethereum_client)
        price = kyber_oracle.get_price(
            gno_token_mainnet_address, weth_token_mainnet_address
        )
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Test with 2 stablecoins
        price = kyber_oracle.get_price(
            dai_token_mainnet_address, usdt_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)

        price = kyber_oracle.get_price(
            usdt_token_mainnet_address, dai_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)

        self.assertEqual(
            kyber_oracle.get_price("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"), 1.0
        )

    def test_kyber_oracle_not_deployed(self):
        kyber_oracle = KyberOracle(self.ethereum_client, Account.create().address)
        random_token_address = Account.create().address
        with self.assertRaisesMessage(
            CannotGetPriceFromOracle, "Cannot get price from kyber-network-proxy"
        ):
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

        with self.assertRaisesMessage(CannotGetPriceFromOracle, "Not enough liquidity"):
            token_address = gno_token_mainnet_address
            uniswap_oracle.get_price(token_address)

        # Check batching is working
        uniswap_exchange = uniswap_oracle.get_uniswap_exchange(token_address)
        self.assertEqual(uniswap_oracle.get_uniswap_exchange.cache_info().hits, 1)
        self.assertEqual(
            uniswap_oracle._get_balances_using_batching(
                uniswap_exchange, token_address
            ),
            uniswap_oracle._get_balances_without_batching(
                uniswap_exchange, token_address
            ),
        )

    def test_uniswap_oracle_not_deployed(self):
        uniswap_oracle = UniswapOracle(self.ethereum_client, Account.create().address)
        random_token_address = Account.create().address
        with self.assertRaisesMessage(
            CannotGetPriceFromOracle, "Non existing uniswap exchange"
        ):
            uniswap_oracle.get_price(random_token_address)


class TestUniswapV2Oracle(EthereumTestCaseMixin, TestCase):
    @mock.patch.object(
        UniswapV2Oracle,
        "factory_address",
        return_value="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        new_callable=mock.PropertyMock,
    )
    def test_calculate_pair_address(self, factory_address_mock: MagicMock):
        uniswap_v2_oracle = UniswapV2Oracle(self.ethereum_client)
        expected_address = "0x3e8468f66d30Fc99F745481d4B383f89861702C6"

        self.assertEqual(
            uniswap_v2_oracle.calculate_pair_address(
                gno_token_mainnet_address, weth_token_mainnet_address
            ),
            expected_address,
        )
        self.assertEqual(
            uniswap_v2_oracle.calculate_pair_address(
                weth_token_mainnet_address, gno_token_mainnet_address
            ),
            expected_address,
        )

    def test_get_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_v2_oracle = UniswapV2Oracle(ethereum_client)

        price = uniswap_v2_oracle.get_price(
            gno_token_mainnet_address, weth_token_mainnet_address
        )
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Test with 2 stablecoins
        price = uniswap_v2_oracle.get_price(
            dai_token_mainnet_address, usdt_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)
        self.assertEqual(
            uniswap_v2_oracle._decimals_cache[dai_token_mainnet_address], 18
        )
        self.assertEqual(
            uniswap_v2_oracle._decimals_cache[usdt_token_mainnet_address], 6
        )

        price = uniswap_v2_oracle.get_price(
            usdt_token_mainnet_address, dai_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)

    def test_get_price_contract_not_deployed(self):
        uniswap_v2_oracle = UniswapV2Oracle(self.ethereum_client)
        random_token_address = Account.create().address
        with self.assertRaisesMessage(
            CannotGetPriceFromOracle,
            f"Cannot get uniswap v2 price for pair token_1={random_token_address}",
        ):
            uniswap_v2_oracle.get_price(random_token_address)

    @mock.patch.object(
        UniswapV2Oracle,
        "factory_address",
        return_value="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        new_callable=mock.PropertyMock,
    )
    @mock.patch.object(
        UniswapV2Oracle, "get_decimals", return_value=(18, 3), autospec=True
    )
    @mock.patch.object(
        UniswapV2Oracle, "get_reserves", return_value=(int(1e20), 600), autospec=True
    )
    def test_get_price_liquidity(
        self,
        get_reserves_mock: MagicMock,
        get_decimals_mock: MagicMock,
        factory_address_mock: MagicMock,
    ):
        uniswap_v2_oracle = UniswapV2Oracle(self.ethereum_client)
        token_1, token_2 = (
            "0xA14F6F8867DB84a45BCD148bfaf4e4f54B4B9b12",
            "0xC426A8F4C79EF274Ed93faC9e1A09bFC5659B06B",
        )

        with self.assertRaisesMessage(CannotGetPriceFromOracle, "Not enough liquidity"):
            uniswap_v2_oracle.get_price(token_1, token_2)

        get_reserves_mock.return_value = (int(1e20), 6000)
        self.assertEqual(uniswap_v2_oracle.get_price(token_1, token_2), 0.06)

        get_reserves_mock.return_value = reversed(get_reserves_mock.return_value)
        self.assertEqual(
            uniswap_v2_oracle.get_price(token_2, token_1), 0.06
        )  # Reserves were inverted

    def test_get_pool_token_price(self):
        dai_eth_pool_address = "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11"
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_v2_oracle = UniswapV2Oracle(ethereum_client)

        price = uniswap_v2_oracle.get_pool_token_price(dai_eth_pool_address)
        self.assertGreater(price, 0.0)


class TestSushiSwapOracle(EthereumTestCaseMixin, TestCase):
    def test_get_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        sushiswap_oracle = SushiswapOracle(ethereum_client)

        price = sushiswap_oracle.get_price(
            gno_token_mainnet_address, weth_token_mainnet_address
        )
        self.assertLess(price, 1)
        self.assertGreater(price, 0)

        # Test with 2 stablecoins
        price = sushiswap_oracle.get_price(
            dai_token_mainnet_address, usdt_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)
        self.assertEqual(
            sushiswap_oracle._decimals_cache[dai_token_mainnet_address], 18
        )
        self.assertEqual(
            sushiswap_oracle._decimals_cache[usdt_token_mainnet_address], 6
        )

        price = sushiswap_oracle.get_price(
            usdt_token_mainnet_address, dai_token_mainnet_address
        )
        self.assertAlmostEqual(price, 1.0, delta=0.5)


class TestAaveOracle(EthereumTestCaseMixin, TestCase):
    def test_get_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_oracle = UniswapV2Oracle(ethereum_client)
        aave_oracle = AaveOracle(ethereum_client, uniswap_oracle)

        aweth_address = "0x030bA81f1c18d280636F32af80b9AAd02Cf0854e"
        price = aave_oracle.get_price(aweth_address)
        self.assertGreater(price, 0.0)

        stacked_aave_address = "0x4da27a545c0c5B758a6BA100e3a049001de870f5"
        price = aave_oracle.get_price(stacked_aave_address)
        self.assertGreater(price, 0.0)

        error_message = "It is not an Aaave atoken"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            aave_oracle.get_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            aave_oracle.get_price(Account.create().address)


class TestCreamOracle(EthereumTestCaseMixin, TestCase):
    def test_get_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        sushi_oracle = SushiswapOracle(ethereum_client)
        cream_oracle = CreamOracle(ethereum_client, sushi_oracle)

        cyusdc_address = "0x76Eb2FE28b36B3ee97F3Adae0C69606eeDB2A37c"
        price = cream_oracle.get_price(cyusdc_address)
        self.assertGreater(price, 0.0)

        cydai_address = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"
        price = cream_oracle.get_price(cydai_address)
        self.assertGreater(price, 0.0)

        error_message = "It is not a Cream cToken"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            cream_oracle.get_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            cream_oracle.get_price(Account.create().address)


class TestCurveOracle(EthereumTestCaseMixin, TestCase):
    def test_get_underlying_tokens(self):
        curve_token_address = (
            "0xC25a3A3b969415c80451098fa907EC722572917F"  # Curve.fi DAI/USDC/USDT/sUSD
        )
        local_curve_oracle = CurveOracle(self.ethereum_client)
        error_message = "Cannot find Zerion adapter"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            local_curve_oracle.get_underlying_tokens(curve_token_address)

        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        curve_oracle = CurveOracle(ethereum_client)

        # Curve.fi ETH/stETH (steCRV) is working with the updated adapter
        self.assertEqual(
            len(
                curve_oracle.get_underlying_tokens(
                    "0x06325440D014e39736583c165C2963BA99fAf14E"
                )
            ),
            2,
        )

        underlying_tokens = curve_oracle.get_underlying_tokens(curve_token_address)
        self.assertEqual(len(underlying_tokens), 4)

        self.assertCountEqual(
            [underlying_token.address for underlying_token in underlying_tokens],
            [
                "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51",
            ],
        )
        for underlying_token in underlying_tokens:
            self.assertTrue(0.0 < underlying_token.quantity < 1.0)

        error_message = "It is not a Zerion supported pool token"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            curve_oracle.get_underlying_tokens(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            curve_oracle.get_underlying_tokens(Account.create().address)

    def test_get_underlying_tokens_gauges(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        curve_oracle = CurveOracle(ethereum_client)

        # 3crv gauge deposit: dai, usdc, usdt
        gauge_deposit_address = "0xF5194c3325202F456c95c1Cf0cA36f8475C1949F"
        gauge_lp_token_address = "0x5282a4eF67D9C33135340fB3289cc1711c13638C"
        gauge_underlying_tokens = curve_oracle.get_underlying_tokens(
            gauge_deposit_address
        )
        lp_token_underlying_tokens = curve_oracle.get_underlying_tokens(
            gauge_lp_token_address
        )

        self.assertEqual(gauge_underlying_tokens, lp_token_underlying_tokens)


class TestZerionComposedOracle(EthereumTestCaseMixin, TestCase):
    def test_zerion_composed_oracle(self):
        with self.assertRaisesMessage(ValueError, "Expected a Zerion adapter address"):
            ZerionComposedOracle(self.ethereum_client)


class TestPoolTogetherOracle(EthereumTestCaseMixin, TestCase):
    def test_get_underlying_token(self):
        pool_together_token_address = (
            "0xD81b1A8B1AD00Baa2D6609E0BAE28A38713872f7"  # v3 USDC Ticket
        )
        local_pool_together_oracle = CurveOracle(self.ethereum_client)
        error_message = "Cannot find Zerion adapter"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            local_pool_together_oracle.get_underlying_tokens(
                pool_together_token_address
            )

        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        pool_together_oracle = PoolTogetherOracle(ethereum_client)

        underlying_tokens = pool_together_oracle.get_underlying_tokens(
            pool_together_token_address
        )
        self.assertEqual(len(underlying_tokens), 1)
        self.assertEqual(
            [underlying_token.address for underlying_token in underlying_tokens],
            ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"],
        )
        self.assertEqual(underlying_tokens[0].quantity, 1.0)

        error_message = "It is not a Zerion supported pool token"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            pool_together_oracle.get_underlying_tokens(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            pool_together_oracle.get_underlying_tokens(Account.create().address)


class TestYearnOracle(EthereumTestCaseMixin, TestCase):
    def test_get_underlying_tokens(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        yearn_oracle = YearnOracle(ethereum_client)
        yearn_token_address = "0x5533ed0a3b83F70c3c4a1f69Ef5546D3D4713E44"  # Yearn Curve.fi DAI/USDC/USDT/sUSD
        yearn_underlying_token_address = (
            "0xC25a3A3b969415c80451098fa907EC722572917F"  # Curve.fi DAI/USDC/USDT/sUSD
        )
        iearn_token_address = "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01"  # iearn DAI
        iearn_underlying_token_address = (
            "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # DAI
        )
        yvault_token_address = (
            "0xdCD90C7f6324cfa40d7169ef80b12031770B4325"  # steCRV yVault
        )
        yvault_underlying_token_address = (
            "0x06325440D014e39736583c165C2963BA99fAf14E"  # steCRV
        )

        underlying_tokens = yearn_oracle.get_underlying_tokens(yearn_token_address)
        self.assertEqual(len(underlying_tokens), 1)
        underlying_token = underlying_tokens[0]
        self.assertEqual(underlying_token.quantity, 1.0)
        self.assertEqual(underlying_token.address, yearn_underlying_token_address)

        underlying_tokens = yearn_oracle.get_underlying_tokens(iearn_token_address)
        self.assertEqual(len(underlying_tokens), 1)
        underlying_token = underlying_tokens[0]
        self.assertEqual(underlying_token.quantity, 1.0)
        self.assertEqual(underlying_token.address, iearn_underlying_token_address)

        underlying_tokens = yearn_oracle.get_underlying_tokens(yvault_token_address)
        self.assertEqual(len(underlying_tokens), 1)
        underlying_token = underlying_tokens[0]
        self.assertEqual(underlying_token.quantity, 1.0)
        self.assertEqual(underlying_token.address, yvault_underlying_token_address)

        # Test yToken
        y_token = "0x30FCf7c6cDfC46eC237783D94Fc78553E79d4E9C"
        yearn_underlying_token = "0x3a664Ab939FD8482048609f652f9a0B0677337B9"
        underlying_tokens = yearn_oracle.get_underlying_tokens(y_token)
        self.assertEqual(len(underlying_tokens), 1)
        underlying_token = underlying_tokens[0]
        self.assertAlmostEqual(underlying_token.quantity, 1.0, delta=0.5)
        self.assertEqual(underlying_token.address, yearn_underlying_token)

        error_message = "It is not a Yearn yToken/yVault"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            yearn_oracle.get_underlying_tokens(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            yearn_oracle.get_underlying_tokens(Account.create().address)


class TestBalancerOracle(EthereumTestCaseMixin, TestCase):
    def test_get_pool_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_oracle = UniswapV2Oracle(ethereum_client)
        balancer_oracle = BalancerOracle(ethereum_client, uniswap_oracle)
        balancer_token_address = (
            "0x59A19D8c652FA0284f44113D0ff9aBa70bd46fB4"  # Balancer 80% BAL + 20% WETH
        )

        price = balancer_oracle.get_pool_token_price(balancer_token_address)
        self.assertAlmostEqual(price, 1.0, delta=0.9)

        with self.assertRaisesMessage(
            CannotGetPriceFromOracle, "It is not a balancer pool token"
        ):
            balancer_oracle.get_pool_token_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(
            CannotGetPriceFromOracle, "It is not a balancer pool token"
        ):
            balancer_oracle.get_pool_token_price(Account.create().address)


class TestMooniswapOracle(EthereumTestCaseMixin, TestCase):
    def test_get_pool_token_price(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        uniswap_oracle = UniswapV2Oracle(ethereum_client)
        mooniswap_oracle = MooniswapOracle(ethereum_client, uniswap_oracle)
        mooniswap_pool_address = "0x6a11F3E5a01D129e566d783A7b6E8862bFD66CcA"  # 1inch Liquidity Pool (ETH-WBTC)
        other_version_mooniswap_pool_address = (
            "0x8a2f2F8637deb4Ee7C9400A240d27E3A32147dA4"  # Mooniswap V1 (OWL-GNO)
        )

        price = mooniswap_oracle.get_pool_token_price(mooniswap_pool_address)
        self.assertGreater(price, 0)

        price = mooniswap_oracle.get_pool_token_price(
            other_version_mooniswap_pool_address
        )
        self.assertGreater(price, 0)

        with self.assertRaisesMessage(
            CannotGetPriceFromOracle, "It is not a mooniswap pool token"
        ):
            mooniswap_oracle.get_pool_token_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(
            CannotGetPriceFromOracle, "It is not a mooniswap pool token"
        ):
            mooniswap_oracle.get_pool_token_price(Account.create().address)


class TestEnzymeOracle(EthereumTestCaseMixin, TestCase):
    def test_get_underlying_tokens(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        enzyme_oracle = EnzymeOracle(ethereum_client)
        mln_vault_token_address = "0x45c45799Bcf6C7Eb2Df0DA1240BE04cE1D18CC69"
        mln_vault_underlying_token = "0xec67005c4E498Ec7f55E092bd1d35cbC47C91892"
        usf_fund_token_address = "0x86FB84E92c1EEDc245987D28a42E123202bd6701"
        usf_fund_underlying_tokens = [
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "0x182B723a58739a9c974cFDB385ceaDb237453c28",
            "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",
            "0xD533a949740bb3306d119CC777fa900bA034cd52",
        ]

        underlying_tokens = enzyme_oracle.get_underlying_tokens(mln_vault_token_address)
        self.assertEqual(len(underlying_tokens), 1)
        underlying_token = underlying_tokens[0]
        self.assertEqual(underlying_token.quantity, 1.0)
        self.assertEqual(underlying_token.address, mln_vault_underlying_token)

        underlying_tokens = enzyme_oracle.get_underlying_tokens(usf_fund_token_address)
        self.assertEqual(len(underlying_tokens), 4)
        for underlying_token in underlying_tokens:
            self.assertIn(underlying_token.address, usf_fund_underlying_tokens)
            self.assertAlmostEqual(underlying_token.quantity, 0.5, delta=0.5)
