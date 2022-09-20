from django.test import TestCase

from eth_account import Account

from ... import EthereumClient
from ...oracles import CannotGetPriceFromOracle, KyberOracle
from ..ethereum_test_case import EthereumTestCaseMixin
from ..test_oracles import (
    dai_token_mainnet_address,
    gno_token_mainnet_address,
    usdt_token_mainnet_address,
    weth_token_mainnet_address,
)
from ..utils import just_test_if_mainnet_node


class TestKyberOracle(EthereumTestCaseMixin, TestCase):
    def test_kyber_oracle(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)

        self.assertTrue(KyberOracle.is_available(ethereum_client))
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
            CannotGetPriceFromOracle,
            f"Cannot get decimals for token={random_token_address}",
        ):
            kyber_oracle.get_price(random_token_address)
