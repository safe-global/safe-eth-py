"""
Support for MakerDAO MultiCall contract
"""
from dataclasses import dataclass
from typing import Any, List, Sequence, Tuple

from eth_abi.exceptions import DecodingError
from eth_typing import BlockNumber, ChecksumAddress
from hexbytes import HexBytes
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import ContractFunction
from web3.exceptions import ContractLogicError

from . import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from .oracles.abis.makerdao import multicall_v2_abi

MULTICALL_V2_ADDRESSES = {
    EthereumNetwork.MAINNET: '0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696',
    EthereumNetwork.KOVAN: '0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696',
    EthereumNetwork.RINKEBY: '0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696',
    EthereumNetwork.GOERLI: '0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696',
    EthereumNetwork.ROPSTEN: '0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696',
    EthereumNetwork.BINANCE: '0xed386Fe855C1EFf2f843B910923Dd8846E45C5A4',
    EthereumNetwork.MATIC: '0xed386Fe855C1EFf2f843B910923Dd8846E45C5A4',
    EthereumNetwork.MUMBAI: '0xed386Fe855C1EFf2f843B910923Dd8846E45C5A4',
}


@dataclass
class MulticallResult:
    success: bool
    return_data: bytes


@dataclass
class MulticallDecodedResult:
    success: bool
    return_data_decoded: Any


class MulticallException(Exception):
    pass


class MulticallFunctionFailed(MulticallException):
    pass


class Multicall:
    def __init__(self, ethereum_client: EthereumClient):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        ethereum_network = ethereum_client.get_network()
        address = MULTICALL_V2_ADDRESSES.get(ethereum_network)
        if not address:
            raise EthereumNetworkNotSupported('Multicall contract not available for %s', ethereum_network.name)
        self.contract = self.w3.eth.contract(address, abi=multicall_v2_abi)

    def _build_payload(self, contract_functions: Sequence[ContractFunction]
                       ) -> Tuple[List[Tuple[ChecksumAddress, bytes]], List[List[Any]]]:
        targets_with_data = []
        output_types = []
        for contract_function in contract_functions:
            targets_with_data.append((contract_function.address,
                                      HexBytes(contract_function._encode_transaction_data())))
            output_types.append([output['type'] for output in contract_function.abi['outputs']])

        return targets_with_data, output_types

    def _decode_data(self, output_type: Sequence[str], data: bytes) -> Any:
        """

        :param output_type:
        :param data:
        :return:
        :raises: DecodingError
        :raises: OverflowError
        """
        try:
            decoded_values = self.w3.codec.decode_abi(output_type, data)
            normalized_data = map_abi_data(BASE_RETURN_NORMALIZERS, output_type, decoded_values)
            if len(normalized_data) == 1:
                return normalized_data[0]
            else:
                return normalized_data
        except DecodingError:
            return b''

    def _aggregate(self, targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]]) -> Tuple[BlockNumber, List[Any]]:
        """

        :param targets_with_data: List of target `addresses` and `data` to be called in each Contract
        :return:
        :raises: MulticallFunctionFailed
        """
        aggregate_parameter = [{'target': target, 'callData': data} for target, data in targets_with_data]
        try:
            return self.contract.functions.aggregate(aggregate_parameter).call()
        except ContractLogicError:
            raise MulticallFunctionFailed

    def aggregate(self, contract_functions: Sequence[ContractFunction]) -> Tuple[BlockNumber, List[Any]]:
        """
        Calls ``aggregate`` on MakerDAO's Multicall contract. If a function called raises an error execution is stopped

        :param contract_functions:
        :return: A tuple with the ``blockNumber`` and a list with the decoded return values
        :raises: MulticallFunctionFailed
        """
        targets_with_data, output_types = self._build_payload(contract_functions)
        block_number, results = self._aggregate(targets_with_data)
        decoded_results = [self._decode_data(output_type, data) for output_type, data in zip(output_types, results)]
        return block_number, decoded_results

    def _try_aggregate(self,
                       targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]],
                       require_success: bool = False
                       ) -> List[MulticallResult]:
        aggregate_parameter = [{'target': target, 'callData': data} for target, data in targets_with_data]
        try:
            result = self.contract.functions.tryAggregate(require_success, aggregate_parameter).call()
            return [MulticallResult(success, data) for success, data in result]
        except ContractLogicError:
            raise MulticallFunctionFailed

    def try_aggregate(self,
                      contract_functions: Sequence[ContractFunction],
                      require_success: bool = False
                      ) -> List[MulticallDecodedResult]:
        """
        Calls ``try_aggregate`` on MakerDAO's Multicall contract.

        :param contract_functions:
        :param require_success: If ``True``, an exception in any of the functions will stop the execution
        :return: A list with the decoded return values
        """
        targets_with_data, output_types = self._build_payload(contract_functions)
        results = self._try_aggregate(targets_with_data, require_success=require_success)
        return [
            MulticallDecodedResult(
                multicall_result.success,
                self._decode_data(
                    output_type,
                    multicall_result.return_data
                ) if multicall_result.success else multicall_result.return_data
            ) for output_type, multicall_result in zip(output_types, results)
        ]
