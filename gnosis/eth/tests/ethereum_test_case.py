import logging

from django.conf import settings

from eth_account import Account
from eth_account.signers.local import LocalAccount

from ..ethereum_client import EthereumClientProvider
from .utils import deploy_example_erc20, send_tx

logger = logging.getLogger(__name__)


class EthereumTestCaseMixin:
    @classmethod
    def prepare_tests(cls):
        cls.ethereum_client = EthereumClientProvider()
        cls.w3 = cls.ethereum_client.w3
        cls.ethereum_test_account: LocalAccount = Account.privateKeyToAccount(settings.ETHEREUM_TEST_PRIVATE_KEY)

    @property
    def gas_price(self):
        return self.w3.eth.gasPrice

    def send_tx(self, tx, account: LocalAccount) -> bytes:
        return send_tx(self.w3, tx, account)

    def send_ether(self, to, value):
        return send_tx(self.w3, {'to': to, 'value': value}, self.ethereum_test_account)

    def create_account(self, initial_ether: float = 0, initial_wei: int = 0) -> LocalAccount:
        account = Account.create()
        if initial_ether > .0 or initial_wei > 0:
            self.send_tx({'to': account.address,
                          'value': self.w3.toWei(initial_ether, 'ether') + initial_wei
                          }, self.ethereum_test_account)
        return account

    def deploy_example_erc20(self, amount: int, owner: str):
        return deploy_example_erc20(self.w3, amount, owner, account=self.ethereum_test_account)
