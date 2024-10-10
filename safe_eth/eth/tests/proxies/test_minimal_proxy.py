from unittest import TestCase

from eth_account import Account

from safe_eth.eth.proxies import MinimalProxy
from safe_eth.eth.tests.ethereum_test_case import EthereumTestCaseMixin


class TestMinimalProxy(EthereumTestCaseMixin, TestCase):
    def test_get_implementation_address(self):
        account = self.ethereum_test_account
        contract_address = Account.create().address
        deployment_data = MinimalProxy.get_deployment_data(contract_address)
        expected_code = MinimalProxy.get_expected_code(contract_address)

        tx = {"data": deployment_data}

        tx_hash = self.send_tx(tx, account)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        proxy_address = tx_receipt["contractAddress"]
        code = self.w3.eth.get_code(proxy_address)
        self.assertEqual(code, expected_code)

        minimal_proxy = MinimalProxy(proxy_address, self.ethereum_client)
        self.assertEqual(minimal_proxy.get_implementation_address(), contract_address)
