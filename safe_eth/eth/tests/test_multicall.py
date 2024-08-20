from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from .. import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from ..constants import NULL_ADDRESS
from ..contracts import get_erc20_contract
from ..exceptions import BatchCallFunctionFailed
from ..multicall import Multicall, MulticallDecodedResult
from .ethereum_test_case import EthereumTestCaseMixin
from .utils import just_test_if_mainnet_node


class TestMulticallGanache(EthereumTestCaseMixin, TestCase):
    """
    Test Multicall using ganache
    """

    @mock.patch.object(
        EthereumClient, "get_network", return_value=EthereumNetwork.UNKNOWN
    )
    def test_multicall_network_exception(self, ethereum_network_mock: MagicMock):
        with self.assertRaisesMessage(
            EthereumNetworkNotSupported, "Multicall contract not available for"
        ):
            Multicall(self.ethereum_client)

    def test_multicall_try_aggregate(self):
        erc20_contract = self.deploy_example_erc20(
            1, self.ethereum_test_account.address
        )

        results = self.multicall.try_aggregate(
            [
                erc20_contract.functions.name(),
                erc20_contract.functions.transfer(NULL_ADDRESS, 1),
                erc20_contract.functions.symbol(),
                erc20_contract.functions.decimals(),
            ]
        )
        expected_results = [
            MulticallDecodedResult(success=True, return_data_decoded="Uxio"),
            MulticallDecodedResult(
                success=False,
                return_data_decoded=b"\x08\xc3y\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00#ERC20: transfer to the zero address\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            ),  # noqa
            MulticallDecodedResult(success=True, return_data_decoded="UXI"),
            MulticallDecodedResult(success=True, return_data_decoded=18),
        ]

        self.assertEqual(results, expected_results)

    def test_try_aggregate_same_function(self):
        account = "0x44425Eff435c3B1C38Cbc1139f248CA2918ACccA"
        erc20_contracts = [self.deploy_example_erc20(i, account) for i in range(3)]
        token_addresses = [erc20_contract.address for erc20_contract in erc20_contracts]

        erc20_contract = get_erc20_contract(self.ethereum_client.w3)

        results = self.multicall.try_aggregate_same_function(
            erc20_contract.functions.balanceOf(account), token_addresses
        )
        expected_results = [
            MulticallDecodedResult(success=True, return_data_decoded=0),
            MulticallDecodedResult(success=True, return_data_decoded=1),
            MulticallDecodedResult(success=True, return_data_decoded=2),
        ]

        self.assertEqual(results, expected_results)


class TestMulticallNode(EthereumTestCaseMixin, TestCase):
    """
    Test Multicall using a production node
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        mainnet_node = just_test_if_mainnet_node()
        cls.ethereum_client = EthereumClient(mainnet_node)
        cls.gno_contract = get_erc20_contract(
            cls.ethereum_client.w3, "0x6810e776880C02933D47DB1b9fc05908e5386b96"
        )
        cls.not_existing_contract = get_erc20_contract(
            cls.ethereum_client.w3, NULL_ADDRESS
        )
        cls.multicall = Multicall(cls.ethereum_client)

    def test_multicall_aggregate(self):
        block_number, results = self.multicall.aggregate(
            [
                self.gno_contract.functions.name(),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals(),
            ]
        )
        expected_results = ["Gnosis Token", "GNO", 18]
        self.assertEqual(results, expected_results)
        self.assertGreater(block_number, 0)

        expected_results = [None]
        block_number, results = self.multicall.aggregate(
            [
                self.not_existing_contract.functions.name(),
            ]
        )
        self.assertEqual(results, expected_results)
        self.assertGreater(block_number, 0)

        expected_results = ["Gnosis Token", None, "GNO", 18]
        block_number, results = self.multicall.aggregate(
            [
                self.gno_contract.functions.name(),
                self.not_existing_contract.functions.name(),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals(),
            ]
        )
        self.assertEqual(results, expected_results)
        self.assertGreater(block_number, 0)

        with self.assertRaises(BatchCallFunctionFailed):
            self.multicall.aggregate(
                [
                    self.gno_contract.functions.name(),
                    self.gno_contract.functions.transfer(NULL_ADDRESS, 1),
                    self.gno_contract.functions.symbol(),
                    self.gno_contract.functions.decimals(),
                ]
            )

    def test_multicall_ty_aggregate(self):
        results = self.multicall.try_aggregate(
            [
                self.gno_contract.functions.name(),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals(),
            ]
        )
        expected_results = [
            MulticallDecodedResult(success=True, return_data_decoded="Gnosis Token"),
            MulticallDecodedResult(success=True, return_data_decoded="GNO"),
            MulticallDecodedResult(success=True, return_data_decoded=18),
        ]
        self.assertEqual(results, expected_results)

        results = self.multicall.try_aggregate(
            [
                self.gno_contract.functions.name(),
                self.gno_contract.functions.transfer(NULL_ADDRESS, 1),
                self.gno_contract.functions.symbol(),
                self.gno_contract.functions.decimals(),
            ]
        )
        expected_results = [
            MulticallDecodedResult(success=True, return_data_decoded="Gnosis Token"),
            MulticallDecodedResult(success=False, return_data_decoded=None),
            MulticallDecodedResult(success=True, return_data_decoded="GNO"),
            MulticallDecodedResult(success=True, return_data_decoded=18),
        ]
        self.assertEqual(results, expected_results)

        with self.assertRaises(BatchCallFunctionFailed):
            self.multicall.try_aggregate(
                [
                    self.gno_contract.functions.name(),
                    self.gno_contract.functions.transfer(NULL_ADDRESS, 1),
                    self.gno_contract.functions.symbol(),
                    self.gno_contract.functions.decimals(),
                ],
                require_success=True,
            )
