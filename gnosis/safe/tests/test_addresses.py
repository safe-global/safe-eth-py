from unittest import TestCase

from packaging.version import Version

from gnosis.eth import EthereumNetwork
from gnosis.eth.utils import fast_is_checksum_address
from gnosis.safe.addresses import MASTER_COPIES, PROXY_FACTORIES


class TestAddresses(TestCase):
    def test_master_copies(self):
        for ethereum_network, master_copies in MASTER_COPIES.items():
            self.assertIsInstance(ethereum_network, EthereumNetwork)
            self.assertIsInstance(master_copies, list)
            for master_copy in master_copies:
                self.assertIsInstance(master_copy, tuple)
                self.assertEqual(len(master_copy), 3)
                self.assertTrue(fast_is_checksum_address(master_copy[0]))
                self.assertGreaterEqual(master_copy[1], 0)
                self.assertGreater(Version(master_copy[2]), Version("0.0.0"))

    def test_proxy_factories(self):
        for ethereum_network, proxy_factories in PROXY_FACTORIES.items():
            self.assertIsInstance(ethereum_network, EthereumNetwork)
            self.assertIsInstance(proxy_factories, list)
            for proxy_factory in proxy_factories:
                self.assertIsInstance(proxy_factory, tuple)
                self.assertEqual(len(proxy_factory), 2)
                self.assertTrue(fast_is_checksum_address(proxy_factory[0]))
                self.assertGreaterEqual(proxy_factory[1], 0)
