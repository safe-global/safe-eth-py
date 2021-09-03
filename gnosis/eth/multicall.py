"""
Support for MakerDAO MultiCall contract
"""
from dataclasses import dataclass
from typing import Any, List, Sequence, Tuple

from eth_typing import BlockNumber, ChecksumAddress

from . import EthereumClient, EthereumNetwork
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


class Multicall:
    def __init__(self, ethereum_client: EthereumClient):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        ethereum_network = ethereum_client.get_network()
        address = MULTICALL_V2_ADDRESSES.get(ethereum_network)
        self.contract = self.w3.eth.contract(address, abi=multicall_v2_abi)

    def aggregate(self, targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]]) -> Tuple[BlockNumber, List[Any]]:
        """

        :param targets_with_data: List of target `addresses` and `data` to be called in each Contract
        :return:
        """
        aggregate_parameter = [{'target': target, 'callData': data} for target, data in targets_with_data]
        return self.contract.functions.aggregate(aggregate_parameter).call()

    def try_aggregate(self,
                      targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]],
                      require_success: bool = False
                      ) -> List[MulticallResult]:
        aggregate_parameter = [{'target': target, 'callData': data} for target, data in targets_with_data]
        result = self.contract.functions.tryAggregate(require_success, aggregate_parameter).call()
        return [MulticallResult(success, data) for success, data in result]
