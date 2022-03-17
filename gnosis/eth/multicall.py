"""
Support for MakerDAO MultiCall contract
"""
import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Tuple

from eth_abi.exceptions import DecodingError
from eth_account.signers.local import LocalAccount
from eth_typing import BlockIdentifier, BlockNumber, ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import ContractFunction
from web3.exceptions import ContractLogicError

from . import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from .ethereum_client import EthereumTxSent
from .exceptions import BatchCallFunctionFailed
from .oracles.abis.makerdao import multicall_v2_abi, multicall_v2_bytecode

logger = logging.getLogger(__name__)


@dataclass
class MulticallResult:
    success: bool
    return_data: Optional[bytes]


@dataclass
class MulticallDecodedResult:
    success: bool
    return_data_decoded: Optional[Any]


class Multicall:
    ADDRESSES = {
        EthereumNetwork.MAINNET: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
        EthereumNetwork.ARBITRUM: "0x021CeAC7e681dBCE9b5039d2535ED97590eB395c",
        EthereumNetwork.BINANCE: "0xed386Fe855C1EFf2f843B910923Dd8846E45C5A4",
        EthereumNetwork.GOERLI: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
        EthereumNetwork.KOVAN: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
        EthereumNetwork.MATIC: "0xed386Fe855C1EFf2f843B910923Dd8846E45C5A4",
        EthereumNetwork.MUMBAI: "0xed386Fe855C1EFf2f843B910923Dd8846E45C5A4",
        EthereumNetwork.RINKEBY: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
        EthereumNetwork.ROPSTEN: "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
        EthereumNetwork.XDAI: "0x08612d3C4A5Dfe2FaaFaFe6a4ff712C2dC675bF7",
        EthereumNetwork.FANTOM: "0xD98e3dBE5950Ca8Ce5a4b59630a5652110403E5c",
        EthereumNetwork.AVALANCHE: "0xAbeC56f92a89eEe33F5194Ca4151DD59785c2C74",
    }

    def __init__(
        self,
        ethereum_client: EthereumClient,
        multicall_contract_address: Optional[ChecksumAddress] = None,
    ):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        ethereum_network = ethereum_client.get_network()
        address = multicall_contract_address or self.ADDRESSES.get(ethereum_network)
        if not address:
            raise EthereumNetworkNotSupported(
                "Multicall contract not available for %s", ethereum_network.name
            )
        self.contract = self.get_contract(self.w3, address)

    def get_contract(self, w3: Web3, address: Optional[ChecksumAddress] = None):
        return w3.eth.contract(
            address, abi=multicall_v2_abi, bytecode=multicall_v2_bytecode
        )

    @classmethod
    def deploy_contract(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy contract

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        contract = cls.get_contract(cls, ethereum_client.w3)
        tx = contract.constructor().buildTransaction({"from": deployer_account.address})

        tx_hash = ethereum_client.send_unsigned_transaction(
            tx, private_key=deployer_account.key
        )
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt and tx_receipt["status"]
        contract_address = tx_receipt["contractAddress"]
        logger.info(
            "Deployed Multicall V2 Contract %s by %s",
            contract_address,
            deployer_account.address,
        )
        # Add address to addresses dictionary
        cls.ADDRESSES[ethereum_client.get_network()] = contract_address
        return EthereumTxSent(tx_hash, tx, contract_address)

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
                decoded_values = self.w3.codec.decode_abi(output_type, data)
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
