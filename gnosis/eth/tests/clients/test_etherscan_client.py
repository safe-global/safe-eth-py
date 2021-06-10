from django.test import TestCase

from ... import EthereumNetwork
from ...clients import EtherscanClient, EtherscanRateLimitError
from .mocks import sourcify_safe_metadata


class TestEtherscanClient(TestCase):
    def test_etherscan_get_abi(self):
        try:
            etherscan_api = EtherscanClient(EthereumNetwork.MAINNET)
            safe_master_copy_abi = sourcify_safe_metadata['output']['abi']
            self.assertEqual(etherscan_api.get_contract_abi('0x6851D6fDFAfD08c0295C392436245E5bc78B0185'),
                             safe_master_copy_abi)

            self.assertIsNone(etherscan_api.get_contract_abi('0xaE32496491b53841efb51829d6f886387708F99a'))
        except EtherscanRateLimitError:
            self.skipTest('Etherscan rate limit reached')
