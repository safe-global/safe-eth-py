import unittest
from typing import List
from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from ... import EthereumNetwork
from ...clients import SourcifyClient
from ...clients.sourcify_client import (
    AsyncSourcifyClient,
    SourcifyClientConfigurationProblem,
)


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
        sourcify_client_mainnet = SourcifyClient()
        safe_contract_address = "0x41675C099F32341bf84BFc5382aF534df5C7461a"
        try:
            safe_contract_metadata_mainnet = (
                sourcify_client_mainnet.get_contract_metadata(safe_contract_address)
            )
        except IOError:
            self.skipTest("Cannot connect to Sourcify")
        assert safe_contract_metadata_mainnet is not None
        self.assertEqual(safe_contract_metadata_mainnet.name, "Safe")
        self.assertIsInstance(safe_contract_metadata_mainnet.abi, List)
        self.assertTrue(safe_contract_metadata_mainnet.abi)
        self.assertFalse(safe_contract_metadata_mainnet.partial_match)
        sourcify_client_sepolia = SourcifyClient(EthereumNetwork.SEPOLIA)
        contract_metadata_sepolia = sourcify_client_sepolia.get_contract_metadata(
            safe_contract_address
        )
        self.assertEqual(safe_contract_metadata_mainnet, contract_metadata_sepolia)

        # Testing sourcify partial match token
        partial_match_contract_address = "0x000000000000C1CB11D5c062901F32D06248CE48"
        token_contract_metadata_mainnet = sourcify_client_mainnet.get_contract_metadata(
            partial_match_contract_address
        )
        assert token_contract_metadata_mainnet is not None
        self.assertEqual(token_contract_metadata_mainnet.name, "LiquidGasToken")
        self.assertIsInstance(token_contract_metadata_mainnet.abi, List)
        self.assertTrue(token_contract_metadata_mainnet.abi)
        self.assertTrue(token_contract_metadata_mainnet.partial_match)


class TestAsyncSourcifyClient(unittest.IsolatedAsyncioTestCase):
    @mock.patch.object(SourcifyClient, "is_chain_supported", return_value=True)
    async def test_async_get_contract_metadata(
        self, is_chain_supported_mock: MagicMock
    ):
        sourcify_client_mainnet = AsyncSourcifyClient()
        safe_contract_address = "0x41675C099F32341bf84BFc5382aF534df5C7461a"
        try:
            safe_contract_metadata_mainnet = (
                await sourcify_client_mainnet.async_get_contract_metadata(
                    safe_contract_address
                )
            )
        except IOError:
            self.skipTest("Cannot connect to Sourcify")
        assert safe_contract_metadata_mainnet is not None
        self.assertEqual(safe_contract_metadata_mainnet.name, "Safe")
        self.assertIsInstance(safe_contract_metadata_mainnet.abi, List)
        self.assertTrue(safe_contract_metadata_mainnet.abi)
        self.assertFalse(safe_contract_metadata_mainnet.partial_match)
        sourcify_client_sepolia = AsyncSourcifyClient(EthereumNetwork.SEPOLIA)
        contract_metadata_sepolia = (
            await sourcify_client_sepolia.async_get_contract_metadata(
                safe_contract_address
            )
        )
        self.assertEqual(safe_contract_metadata_mainnet, contract_metadata_sepolia)

        # Testing sourcify partial match token
        partial_match_contract_address = "0x000000000000C1CB11D5c062901F32D06248CE48"
        token_contract_metadata_mainnet = (
            await sourcify_client_mainnet.async_get_contract_metadata(
                partial_match_contract_address
            )
        )
        assert token_contract_metadata_mainnet is not None
        self.assertEqual(token_contract_metadata_mainnet.name, "LiquidGasToken")
        self.assertIsInstance(token_contract_metadata_mainnet.abi, List)
        self.assertTrue(token_contract_metadata_mainnet.abi)
        self.assertTrue(token_contract_metadata_mainnet.partial_match)
