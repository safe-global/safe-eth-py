from django.test import TestCase

from eth_account import Account

from ... import EthereumClient
from ...oracles import CannotGetPriceFromOracle, SuperfluidOracle, SushiswapOracle
from ..ethereum_test_case import EthereumTestCaseMixin
from ..test_oracles import gno_token_mainnet_address
from ..utils import just_test_if_polygon_node


class TestSuperfluidOracle(EthereumTestCaseMixin, TestCase):
    def test_get_price(self):
        polygon_node = just_test_if_polygon_node()

        self.assertFalse(SuperfluidOracle.is_available(self.ethereum_client))

        ethereum_client_polygon = EthereumClient(polygon_node)

        self.assertTrue(SuperfluidOracle.is_available(ethereum_client_polygon))

        sushi_oracle_polygon = SushiswapOracle(ethereum_client_polygon)
        superfluid_oracle_polygon = SuperfluidOracle(
            ethereum_client_polygon, sushi_oracle_polygon
        )
        uscdcx_address_polygon = "0xCAa7349CEA390F89641fe306D93591f87595dc1F"
        price = superfluid_oracle_polygon.get_price(uscdcx_address_polygon)
        self.assertGreater(price, 0.0)

        error_message = "It is not a wrapper Super Token"
        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            superfluid_oracle_polygon.get_price(gno_token_mainnet_address)

        with self.assertRaisesMessage(CannotGetPriceFromOracle, error_message):
            superfluid_oracle_polygon.get_price(Account.create().address)
