"""
MultiCall Smart Contract API
https://github.com/mds1/multicall
"""
import logging
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, Tuple

import eth_abi
from eth_abi.exceptions import DecodingError
from eth_account.signers.local import LocalAccount
from eth_typing import BlockIdentifier, BlockNumber, ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract.contract import Contract, ContractFunction
from web3.exceptions import ContractLogicError

from . import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from .contracts import ContractBase, get_multicall_v3_contract
from .ethereum_client import EthereumTxSent
from .exceptions import BatchCallFunctionFailed
from .utils import get_empty_tx_params

logger = logging.getLogger(__name__)


@dataclass
class MulticallResult:
    success: bool
    return_data: Optional[bytes]


@dataclass
class MulticallDecodedResult:
    success: bool
    return_data_decoded: Optional[Any]


class Multicall(ContractBase):
    # https://github.com/mds1/multicall#deployments
    ADDRESSES = {
        EthereumNetwork.MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.GOERLI: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SEPOLIA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OPTIMISM: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OPTIMISM_GOERLI_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ARBITRUM_ONE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ARBITRUM_NOVA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ARBITRUM_GOERLI: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.POLYGON: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MUMBAI: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.POLYGON_ZKEVM: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.POLYGON_ZKEVM_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.GNOSIS: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.AVALANCHE_C_CHAIN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.AVALANCHE_FUJI_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FANTOM_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FANTOM_OPERA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BINANCE_SMART_CHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BINANCE_SMART_CHAIN_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.KOVAN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.RINKEBY: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.KCC_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.KCC_TESTNET: "0x665683D9bd41C09cF38c3956c926D9924F1ADa97",
        EthereumNetwork.ROPSTEN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CELO_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CELO_ALFAJORES_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.AURORA_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BASE_GOERLI_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
    }

    def __init__(
        self,
        ethereum_client: EthereumClient,
        multicall_contract_address: Optional[ChecksumAddress] = None,
    ):
        ethereum_network = ethereum_client.get_network()
        address = multicall_contract_address or self.ADDRESSES.get(ethereum_network)
        if not address:
            # Try with Multicall V3 deterministic address
            address = self.ADDRESSES.get(EthereumNetwork.MAINNET)
            if not ethereum_client.is_contract(address):
                raise EthereumNetworkNotSupported(
                    "Multicall contract not available for %s", ethereum_network.name
                )
        super().__init__(address, ethereum_client)

    def get_contract_fn(self) -> Callable[[Web3, Optional[ChecksumAddress]], Contract]:
        return get_multicall_v3_contract

    @classmethod
    def deploy_contract(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy contract

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: ``EthereumTxSent`` with the deployed contract address
        """
        contract_fn = cls.get_contract_fn(cls)
        contract = contract_fn(ethereum_client.w3)
        constructor_data = contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]

        ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data
        )

        contract_address = ethereum_tx_sent.contract_address
        logger.info(
            "Deployed Multicall V2 Contract %s by %s",
            contract_address,
            deployer_account.address,
        )
        # Add address to addresses dictionary
        cls.ADDRESSES[ethereum_client.get_network()] = contract_address
        return ethereum_tx_sent

    @staticmethod
    def _build_payload(
        contract_functions: Sequence[ContractFunction],
    ) -> Tuple[List[Tuple[ChecksumAddress, bytes]], List[List[Any]]]:
        targets_with_data = []
        output_types = []
        for contract_function in contract_functions:
            targets_with_data.append(
                (
                    contract_function.address,
                    HexBytes(contract_function._encode_transaction_data()),
                )
            )
            output_types.append(
                [output["type"] for output in contract_function.abi["outputs"]]
            )

        return targets_with_data, output_types

    def _build_payload_same_function(
        self,
        contract_function: ContractFunction,
        contract_addresses: Sequence[ChecksumAddress],
    ) -> Tuple[List[Tuple[ChecksumAddress, bytes]], List[List[Any]]]:
        targets_with_data = []
        output_types = []
        tx_data = HexBytes(contract_function._encode_transaction_data())
        for contract_address in contract_addresses:
            targets_with_data.append((contract_address, tx_data))
            output_types.append(
                [output["type"] for output in contract_function.abi["outputs"]]
            )

        return targets_with_data, output_types

    def _decode_data(self, output_type: Sequence[str], data: bytes) -> Optional[Any]:
        """

        :param output_type:
        :param data:
        :return:
        :raises: DecodingError
        """
        if data:
            try:
                decoded_values = eth_abi.decode(output_type, data)
                normalized_data = map_abi_data(
                    BASE_RETURN_NORMALIZERS, output_type, decoded_values
                )
                if len(normalized_data) == 1:
                    return normalized_data[0]
                else:
                    return normalized_data
            except DecodingError:
                logger.warning(
                    "Cannot decode %s using output-type %s", data, output_type
                )
                return data

    def _aggregate(
        self,
        targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]],
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> Tuple[BlockNumber, List[Optional[Any]]]:
        """

        :param targets_with_data: List of target `addresses` and `data` to be called in each Contract
        :param block_identifier:
        :return:
        :raises: BatchCallFunctionFailed
        """
        aggregate_parameter = [
            {"target": target, "callData": data} for target, data in targets_with_data
        ]
        try:
            return self.contract.functions.aggregate(aggregate_parameter).call(
                block_identifier=block_identifier
            )
        except (ContractLogicError, OverflowError):
            raise BatchCallFunctionFailed

    def aggregate(
        self,
        contract_functions: Sequence[ContractFunction],
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> Tuple[BlockNumber, List[Optional[Any]]]:
        """
        Calls ``aggregate`` on MakerDAO's Multicall contract. If a function called raises an error execution is stopped

        :param contract_functions:
        :param block_identifier:
        :return: A tuple with the ``blockNumber`` and a list with the decoded return values
        :raises: BatchCallFunctionFailed
        """
        targets_with_data, output_types = self._build_payload(contract_functions)
        block_number, results = self._aggregate(
            targets_with_data, block_identifier=block_identifier
        )
        decoded_results = [
            self._decode_data(output_type, data)
            for output_type, data in zip(output_types, results)
        ]
        return block_number, decoded_results

    def _try_aggregate(
        self,
        targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]],
        require_success: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[MulticallResult]:
        """
        Calls ``try_aggregate`` on MakerDAO's Multicall contract.

        :param targets_with_data:
        :param require_success: If ``True``, an exception in any of the functions will stop the execution. Also, an
            invalid decoded value will stop the execution
        :param block_identifier:
        :return: A list with the decoded return values
        """

        aggregate_parameter = [
            {"target": target, "callData": data} for target, data in targets_with_data
        ]
        try:
            result = self.contract.functions.tryAggregate(
                require_success, aggregate_parameter
            ).call(block_identifier=block_identifier)

            if require_success and b"" in (data for _, data in result):
                # `b''` values are decoding errors/missing contracts/missing functions
                raise BatchCallFunctionFailed

            return [
                MulticallResult(success, data if data else None)
                for success, data in result
            ]
        except (ContractLogicError, OverflowError, ValueError):
            raise BatchCallFunctionFailed

    def try_aggregate(
        self,
        contract_functions: Sequence[ContractFunction],
        require_success: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[MulticallDecodedResult]:
        """
        Calls ``try_aggregate`` on MakerDAO's Multicall contract.

        :param contract_functions:
        :param require_success: If ``True``, an exception in any of the functions will stop the execution
        :param block_identifier:
        :return: A list with the decoded return values
        """
        targets_with_data, output_types = self._build_payload(contract_functions)
        results = self._try_aggregate(
            targets_with_data,
            require_success=require_success,
            block_identifier=block_identifier,
        )
        return [
            MulticallDecodedResult(
                multicall_result.success,
                self._decode_data(output_type, multicall_result.return_data)
                if multicall_result.success
                else multicall_result.return_data,
            )
            for output_type, multicall_result in zip(output_types, results)
        ]

    def try_aggregate_same_function(
        self,
        contract_function: ContractFunction,
        contract_addresses: Sequence[ChecksumAddress],
        require_success: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[MulticallDecodedResult]:
        """
        Calls ``try_aggregate`` on MakerDAO's Multicall contract. Reuse same function with multiple contract addresses.
        It's more optimal due to instantiating ``ContractFunction`` objects is very demanding

        :param contract_function:
        :param contract_addresses:
        :param require_success: If ``True``, an exception in any of the functions will stop the execution
        :param block_identifier:
        :return: A list with the decoded return values
        """

        targets_with_data, output_types = self._build_payload_same_function(
            contract_function, contract_addresses
        )
        results = self._try_aggregate(
            targets_with_data,
            require_success=require_success,
            block_identifier=block_identifier,
        )
        return [
            MulticallDecodedResult(
                multicall_result.success,
                self._decode_data(output_type, multicall_result.return_data)
                if multicall_result.success
                else multicall_result.return_data,
            )
            for output_type, multicall_result in zip(output_types, results)
        ]
