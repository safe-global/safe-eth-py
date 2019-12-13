from django.conf import settings
from django.test import TestCase

from eth_account import Account

from gnosis.eth import EthereumClient, InsufficientFunds


class TestRealNodes(TestCase):
    def test_node_exceptions(self):
        node_urls = settings.ETHEREUM_TEST_NODES_URLS
        for node_url in node_urls:
            random_address = Account.create().address
            random_sender_account = Account.create()
            ethereum_service = EthereumClient(node_url)
            with self.assertRaises(InsufficientFunds):
                ethereum_service.send_unsigned_transaction({'to': random_address, 'value': 0, 'data': b'',
                                                            'gas': 25000, 'gasPrice': 1},
                                                           private_key=random_sender_account.key)

    def test_safe_exceptions(self):
        pass
