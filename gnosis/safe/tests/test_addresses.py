from unittest import TestCase

from gnosis.eth import EthereumNetwork
from gnosis.safe.addresses import MASTER_COPIES, PROXY_FACTORIES


class TestAddresses(TestCase):
    def test_master_copies(self):
        for ethereum_network, master_copies in MASTER_COPIES.items():
            self.assertIsInstance(ethereum_network, EthereumNetwork)
            self.assertIsInstance(master_copies, list)
            for master_copy in master_copies:
                self.assertIsInstance(master_copy, tuple)
                self.assertEqual(len(master_copy), 3)

    def test_proxy_factories(self):
        for ethereum_network, proxy_factories in PROXY_FACTORIES.items():
            self.assertIsInstance(ethereum_network, EthereumNetwork)
            self.assertIsInstance(proxy_factories, list)
            for proxy_factory in proxy_factories:
                self.assertIsInstance(proxy_factory, tuple)
                self.assertEqual(len(proxy_factory), 2)
