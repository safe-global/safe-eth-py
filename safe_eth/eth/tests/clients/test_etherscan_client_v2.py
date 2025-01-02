import os
import unittest

from django.test import TestCase

import pytest

from ... import EthereumNetwork
from ...clients import EtherscanClientV2, EtherscanRateLimitError
from ...clients.etherscan_client_v2 import AsyncEtherscanClientV2
from .mocks import sourcify_safe_metadata


class TestEtherscanClientV2(TestCase):
    @classmethod
    def get_etherscan_api(cls, network: EthereumNetwork):
        etherscan_api_key_variable_name = "ETHERSCAN_API_KEY"
        etherscan_api_key = os.environ.get(etherscan_api_key_variable_name)
        if not etherscan_api_key:
            pytest.skip(f"{etherscan_api_key_variable_name} needs to be defined")

        return EtherscanClientV2(network, api_key=etherscan_api_key)

    def test_etherscan_get_abi(self):
        try:
            etherscan_api = self.get_etherscan_api(EthereumNetwork.MAINNET)
            safe_master_copy_abi = sourcify_safe_metadata["output"]["abi"]
            safe_master_copy_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
            self.assertEqual(
                etherscan_api.get_contract_abi(safe_master_copy_address),
                safe_master_copy_abi,
            )

            contract_metadata = etherscan_api.get_contract_metadata(
                safe_master_copy_address
            )
            self.assertEqual(contract_metadata.name, "GnosisSafe")
            self.assertEqual(contract_metadata.abi, safe_master_copy_abi)
            self.assertIsNone(contract_metadata.implementation)

            random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
            self.assertIsNone(etherscan_api.get_contract_abi(random_address))
            self.assertIsNone(etherscan_api.get_contract_metadata(random_address))
        except EtherscanRateLimitError:
            self.skipTest("Etherscan rate limit reached")

    def test_etherscan_get_contract_metadata(self):
        try:
            etherscan_api = self.get_etherscan_api(EthereumNetwork.MAINNET)
            proxy_address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

            contract_metadata = etherscan_api.get_contract_metadata(proxy_address)
            self.assertEqual(contract_metadata.name, "FiatTokenProxy")
            self.assertEqual(
                contract_metadata.implementation,
                "0x43506849d7c04f9138d1a2050bbf3a0c054402dd",
            )

        except EtherscanRateLimitError:
            self.skipTest("Etherscan rate limit reached")

    def test_is_supported_network(self):
        try:
            self.assertTrue(
                EtherscanClientV2.is_supported_network(EthereumNetwork.GNOSIS)
            )
            self.assertFalse(
                EtherscanClientV2.is_supported_network(EthereumNetwork.UNKNOWN)
            )
        except EtherscanRateLimitError:
            self.skipTest("Etherscan rate limit reached")


class TestAsyncEtherscanClientV2(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def get_etherscan_api(cls, network: EthereumNetwork):
        etherscan_api_key_variable_name = "ETHERSCAN_API_KEY"
        etherscan_api_key = os.environ.get(etherscan_api_key_variable_name)
        if not etherscan_api_key:
            pytest.skip(f"{etherscan_api_key_variable_name} needs to be defined")

        return AsyncEtherscanClientV2(network, api_key=etherscan_api_key)

    async def test_async_etherscan_get_abi(self):
        try:
            etherscan_api = self.get_etherscan_api(EthereumNetwork.MAINNET)
            safe_master_copy_abi = sourcify_safe_metadata["output"]["abi"]
            safe_master_copy_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
            self.assertEqual(
                await etherscan_api.async_get_contract_abi(safe_master_copy_address),
                safe_master_copy_abi,
            )

            contract_metadata = await etherscan_api.async_get_contract_metadata(
                safe_master_copy_address
            )
            self.assertEqual(contract_metadata.name, "GnosisSafe")
            self.assertEqual(contract_metadata.abi, safe_master_copy_abi)

            random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
            self.assertIsNone(
                await etherscan_api.async_get_contract_abi(random_address)
            )
            self.assertIsNone(
                await etherscan_api.async_get_contract_metadata(random_address)
            )
        except EtherscanRateLimitError:
            self.skipTest("Etherscan rate limit reached")
