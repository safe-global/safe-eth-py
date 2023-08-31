from django.test import TestCase

import pytest

from ... import EthereumNetwork
from ...clients import EtherscanClient, EtherscanRateLimitError
from .mocks import etherscan_multisend_abi, sourcify_safe_metadata


class TestEtherscanClient(TestCase):
    def test_etherscan_get_abi(self):
        try:
            etherscan_api = EtherscanClient(EthereumNetwork.MAINNET)
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

            random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
            self.assertIsNone(etherscan_api.get_contract_abi(random_address))
            self.assertIsNone(etherscan_api.get_contract_metadata(random_address))
        except EtherscanRateLimitError:
            self.skipTest("Etherscan rate limit reached")

    @pytest.mark.xfail(reason="Test might fail due to third-party service issues")
    def test_etherscan_get_abi_zksync(self):
        multisend_address = "0x0dFcccB95225ffB03c6FBB2559B530C2B7C8A912"
        etherscan_api = EtherscanClient(EthereumNetwork(324))
        self.assertEqual(
            etherscan_api.get_contract_abi(multisend_address),
            etherscan_multisend_abi,
        )
