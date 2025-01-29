import unittest

from django.test import TestCase

import pytest

from ... import EthereumNetwork
from ...clients import BlockscoutClient, BlockScoutConfigurationProblem
from ...clients.blockscout_client import AsyncBlockscoutClient
from .mocks import safe_proxy_abi_mock, sourcify_safe_metadata


class TestBlockscoutClient(TestCase):
    @pytest.mark.flaky(reruns=5)
    def test_blockscout_client(self):
        with self.assertRaises(BlockScoutConfigurationProblem):
            BlockscoutClient(EthereumNetwork.MAINNET)

        blockscout_client = BlockscoutClient(EthereumNetwork.GNOSIS)
        safe_master_copy_abi = sourcify_safe_metadata["output"]["abi"]
        safe_master_copy_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
        contract_metadata = blockscout_client.get_contract_metadata(
            safe_master_copy_address
        )
        self.assertEqual(contract_metadata.name, "GnosisSafe")
        self.assertEqual(contract_metadata.abi, safe_master_copy_abi)
        self.assertEqual(contract_metadata.implementation, None)

        proxy_address = "0xfca7Da0a0290D7BcBEcD93bE124756fC9B6F8E6A"
        implementation_address = "0x3E5c63644E683549055b9Be8653de26E0B4CD36E"
        contract_metadata = blockscout_client.get_contract_metadata(proxy_address)
        self.assertEqual(contract_metadata.name, "GnosisSafeProxy")
        self.assertEqual(contract_metadata.implementation, implementation_address)
        self.assertEqual(contract_metadata.abi, safe_proxy_abi_mock)

        random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
        self.assertIsNone(blockscout_client.get_contract_metadata(random_address))


class TestAsyncBlockscoutClient(unittest.IsolatedAsyncioTestCase):
    async def test_async_blockscout_client(self):
        blockscout_client = AsyncBlockscoutClient(EthereumNetwork.GNOSIS)
        safe_master_copy_abi = sourcify_safe_metadata["output"]["abi"]
        safe_master_copy_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
        contract_metadata = await blockscout_client.async_get_contract_metadata(
            safe_master_copy_address
        )
        self.assertEqual(contract_metadata.name, "GnosisSafe")
        self.assertEqual(contract_metadata.abi, safe_master_copy_abi)

        self.assertEqual(contract_metadata.implementation, None)

        proxy_address = "0xfca7Da0a0290D7BcBEcD93bE124756fC9B6F8E6A"
        implementation_address = "0x3E5c63644E683549055b9Be8653de26E0B4CD36E"
        contract_metadata = blockscout_client.get_contract_metadata(proxy_address)
        self.assertEqual(contract_metadata.name, "GnosisSafeProxy")
        self.assertEqual(contract_metadata.implementation, implementation_address)
        self.assertEqual(contract_metadata.abi, safe_proxy_abi_mock)

        random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
        self.assertIsNone(
            await blockscout_client.async_get_contract_metadata(random_address)
        )
