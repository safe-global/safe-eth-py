from typing import List

from django.test import TestCase

from ... import EthereumNetwork
from ...clients import Sourcify


class TestSourcify(TestCase):
    def test_sourcify_get_contract_metadata(self):
        sourcify = Sourcify()
        safe_contract_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
        try:
            contract_metadata = sourcify.get_contract_metadata(safe_contract_address)
        except IOError:
            self.skipTest("Cannot connect to Sourcify")
        self.assertEqual(contract_metadata.name, "GnosisSafe")
        self.assertIsInstance(contract_metadata.abi, List)
        self.assertTrue(contract_metadata.abi)
        self.assertFalse(contract_metadata.partial_match)
        contract_metadata_rinkeby = Sourcify(
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
