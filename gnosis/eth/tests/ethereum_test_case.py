import logging
import os

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.contract import Contract
from web3.types import TxParams

from ..ethereum_client import EthereumClient, EthereumClientProvider
from ..multicall import Multicall
from .utils import deploy_erc20, send_tx

logger = logging.getLogger(__name__)


_cached_data = {
    "ethereum_client": None,  # Prevents initializing again
}


class EthereumTestCaseMixin:
    ethereum_client: EthereumClient
    ethereum_node_url: str
    w3: Web3
    ethereum_test_account: LocalAccount
    multicall: Multicall

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ethereum_test_account = cls.get_ethereum_test_account(cls)
        # Caching ethereum_client to prevent initializing again
        cls.ethereum_client = _cached_data["ethereum_client"]

        if not cls.ethereum_client:
            cls.ethereum_client = EthereumClientProvider()
            Multicall.deploy_contract(cls.ethereum_client, cls.ethereum_test_account)
            _cached_data["ethereum_client"] = cls.ethereum_client

        cls.ethereum_node_url = cls.ethereum_client.ethereum_node_url

        cls.w3 = cls.ethereum_client.w3
        cls.multicall = cls.ethereum_client.multicall
        assert cls.multicall, "Multicall must be defined"

    def get_ethereum_test_account(self) -> LocalAccount:
        try:
            from django.conf import settings

            key = settings.ETHEREUM_TEST_PRIVATE_KEY
        except ModuleNotFoundError:
            key = os.environ.get(
                "ETHEREUM_TEST_PRIVATE_KEY",
                "b0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773",  # Ganache account 9
            )
        return Account.from_key(key)

    @property
    def gas_price(self):
        return self.w3.eth.gas_price

    def send_tx(self, tx: TxParams, account: LocalAccount) -> bytes:
        return send_tx(self.w3, tx, account)

    def send_ether(self, to: str, value: int) -> bytes:
        return send_tx(self.w3, {"to": to, "value": value}, self.ethereum_test_account)

    def create_and_fund_account(
        self, initial_ether: float = 0, initial_wei: int = 0
    ) -> LocalAccount:
        account = Account.create()
        if initial_ether > 0.0 or initial_wei > 0:
            self.send_tx(
                {
                    "to": account.address,
                    "value": self.w3.to_wei(initial_ether, "ether") + initial_wei,
                },
                self.ethereum_test_account,
            )
        return account

    def deploy_erc20(
        self,
        name: str,
        symbol: str,
        owner: str,
        amount: int,
        decimals: int = 18,
    ) -> Contract:
        return deploy_erc20(
            self.w3,
            self.ethereum_test_account,
            name,
            symbol,
            owner,
            amount,
            decimals=decimals,
        )

    def deploy_example_erc20(self, amount: int, owner: str) -> Contract:
        return deploy_erc20(
            self.w3, self.ethereum_test_account, "Uxio", "UXI", owner, amount
        )
