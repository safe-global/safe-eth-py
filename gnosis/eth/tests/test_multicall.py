from django.test import TestCase

from .. import EthereumClient, EthereumNetworkNotSupported
from ..constants import NULL_ADDRESS
from ..contracts import get_erc20_contract
from ..multicall import (Multicall, MulticallDecodedResult,
                         MulticallFunctionFailed)
from .ethereum_test_case import EthereumTestCaseMixin
from .utils import just_test_if_mainnet_node


class TestMulticallNetworkException(EthereumTestCaseMixin, TestCase):
    def test_multicall_network_exception(self):
        with self.assertRaisesMessage(EthereumNetworkNotSupported, 'Multicall contract not available for'):
            Multicall(self.ethereum_client)


class TestMulticall(EthereumTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        mainnet_node = just_test_if_mainnet_node()
        cls.ethereum_client = EthereumClient(mainnet_node)
        cls.gno_contract = get_erc20_contract(cls.ethereum_client.w3, '0x6810e776880C02933D47DB1b9fc05908e5386b96')
        cls.not_existing_contract = get_erc20_contract(cls.ethereum_client.w3, NULL_ADDRESS)
        cls.multicall = Multicall(cls.ethereum_client)

    def test_multicall_aggregate(self):
        block_number, results = self.multicall.aggregate([
            self.gno_contract.functions.name(),
            self.gno_contract.functions.symbol(),
            self.gno_contract.functions.decimals(),
        ])
        expected_results = ['Gnosis Token', 'GNO', 18]
        self.assertEqual(results, expected_results)
        self.assertGreater(block_number, 0)

        expected_results = [b'']
        block_number, results = self.multicall.aggregate([
            self.not_existing_contract.functions.name(),
        ])
        self.assertEqual(results, expected_results)
        self.assertGreater(block_number, 0)

        expected_results = ['Gnosis Token', b'', 'GNO', 18]
        block_number, results = self.multicall.aggregate([
                self.gno_contract.functions.name(),
                self.not_existing_contract.functions.name(),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals(),
            ])
        self.assertEqual(results, expected_results)
        self.assertGreater(block_number, 0)

        with self.assertRaises(MulticallFunctionFailed):
            self.multicall.aggregate([
                self.gno_contract.functions.name(),
                self.gno_contract.functions.transfer(NULL_ADDRESS, 1),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals(),
            ])

    def test_multicall_ty_aggregate(self):
        results = self.multicall.try_aggregate([
            self.gno_contract.functions.name(),
            self.gno_contract.functions.symbol(),
            self.gno_contract.functions.decimals()
        ])
        expected_results = [MulticallDecodedResult(success=True, return_data_decoded='Gnosis Token'),
                            MulticallDecodedResult(success=True, return_data_decoded='GNO'),
                            MulticallDecodedResult(success=True, return_data_decoded=18)]
        self.assertEqual(results, expected_results)

        results = self.multicall.try_aggregate([
            self.gno_contract.functions.name(),
            self.gno_contract.functions.transfer(NULL_ADDRESS, 1),
            self.gno_contract.functions.symbol(),
            self.gno_contract.functions.decimals()
        ])
        expected_results = [MulticallDecodedResult(success=True, return_data_decoded='Gnosis Token'),
                            MulticallDecodedResult(success=False, return_data_decoded=b''),
                            MulticallDecodedResult(success=True, return_data_decoded='GNO'),
                            MulticallDecodedResult(success=True, return_data_decoded=18)]
        self.assertEqual(results, expected_results)

        with self.assertRaises(MulticallFunctionFailed):
            self.multicall.try_aggregate([
                self.gno_contract.functions.name(),
                self.gno_contract.functions.transfer(NULL_ADDRESS, 1),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals()
            ], require_success=True)
