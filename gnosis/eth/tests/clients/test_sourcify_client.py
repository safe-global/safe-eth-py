from typing import List
from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from ... import EthereumNetwork
from ...clients import SourcifyClient
from ...clients.sourcify_client import SourcifyClientConfigurationProblem


class TestSourcifyClient(TestCase):
    @mock.patch.object(SourcifyClient, "is_chain_supported")
    def test_init(self, is_chain_supported_mock: MagicMock):
        is_chain_supported_mock.return_value = False
        with self.assertRaises(SourcifyClientConfigurationProblem):
            SourcifyClient(EthereumNetwork.OLYMPIC)

        is_chain_supported_mock.return_value = True
        self.assertIsInstance(SourcifyClient(), SourcifyClient)
        self.assertIsInstance(SourcifyClient(EthereumNetwork.GNOSIS), SourcifyClient)

    def test_is_chain_supported(self):
        try:
            sourcify = SourcifyClient()
        except IOError:
            self.skipTest("Cannot connect to Sourcify")

        self.assertTrue(sourcify.is_chain_supported(EthereumNetwork.MAINNET.value))
        self.assertTrue(sourcify.is_chain_supported(EthereumNetwork.GNOSIS.value))
        self.assertFalse(sourcify.is_chain_supported(2))

    @mock.patch.object(SourcifyClient, "is_chain_supported", return_value=True)
    def test_get_contract_metadata(self, is_chain_supported_mock: MagicMock):
        sourcify = SourcifyClient()
        safe_contract_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
        try:
            contract_metadata = sourcify.get_contract_metadata(safe_contract_address)
        except IOError:
            self.skipTest("Cannot connect to Sourcify")
        self.assertEqual(contract_metadata.name, "GnosisSafe")
        self.assertIsInstance(contract_metadata.abi, List)
        self.assertTrue(contract_metadata.abi)
        self.assertFalse(contract_metadata.partial_match)
        contract_metadata_rinkeby = SourcifyClient(
            EthereumNetwork.RINKEBY
        ).get_contract_metadata(safe_contract_address)
        self.assertEqual(contract_metadata, contract_metadata_rinkeby)

        partial_match_contract_address = "0x000000000000C1CB11D5c062901F32D06248CE48"
        contract_metadata = sourcify.get_contract_metadata(
            partial_match_contract_address
        )
        self.assertEqual(contract_metadata.name, "LiquidGasToken")
        self.assertIsInstance(contract_metadata.abi, List)
        self.assertTrue(contract_metadata.abi)
        self.assertTrue(contract_metadata.partial_match)
