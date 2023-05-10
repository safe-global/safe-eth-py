import json
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from eth_typing import ChecksumAddress

from .. import EthereumNetwork
from .contract_metadata import ContractMetadata


class BlockscoutClientException(Exception):
    pass


class BlockScoutConfigurationProblem(BlockscoutClientException):
    pass


class BlockscoutClient:
    NETWORK_WITH_URL = {
        EthereumNetwork.GNOSIS: "https://blockscout.com/poa/xdai/",
        EthereumNetwork.POLYGON: "https://polygon-explorer-mainnet.chainstacklabs.com/",
        EthereumNetwork.MUMBAI: "https://polygon-explorer-mumbai.chainstacklabs.com/",
        EthereumNetwork.ENERGY_WEB_CHAIN: "https://explorer.energyweb.org/",
        EthereumNetwork.ENERGY_WEB_VOLTA_TESTNET: "https://volta-explorer.energyweb.org/",
        EthereumNetwork.POLIS_MAINNET: "https://explorer.polis.tech",
        EthereumNetwork.BOBABEAM: "https://blockexplorer.bobabeam.boba.network/",
        EthereumNetwork.BOBA_NETWORK_RINKEBY_TESTNET: "https://blockexplorer.rinkeby.boba.network/",
        EthereumNetwork.BOBA_NETWORK: "https://blockexplorer.boba.network/",
        EthereumNetwork.GATHER_DEVNET_NETWORK: "https://devnet-explorer.gather.network/",
        EthereumNetwork.GATHER_TESTNET_NETWORK: "https://testnet-explorer.gather.network/",
        EthereumNetwork.GATHER_MAINNET_NETWORK: "https://explorer.gather.network/",
        EthereumNetwork.METIS_STARDUST_TESTNET: "https://stardust-explorer.metis.io/",
        EthereumNetwork.METIS_GOERLI_TESTNET: "https://goerli.explorer.metisdevops.link/",
        EthereumNetwork.METIS_ANDROMEDA_MAINNET: "https://andromeda-explorer.metis.io/",
        EthereumNetwork.FUSE_MAINNET: "https://explorer.fuse.io/",
        EthereumNetwork.VELAS_EVM_MAINNET: "https://evmexplorer.velas.com/",
        EthereumNetwork.REI_NETWORK: "https://scan.rei.network/",
        EthereumNetwork.REI_CHAIN_TESTNET: "https://scan-test.rei.network/",
        EthereumNetwork.METER_MAINNET: "https://scan.meter.io/",
        EthereumNetwork.METER_TESTNET: "https://scan-warringstakes.meter.io/",
        EthereumNetwork.GODWOKEN_TESTNET_V1: "https://v1.betanet.gwscan.com/",
        EthereumNetwork.GODWOKEN_MAINNET: "https://v1.gwscan.com/",
        EthereumNetwork.VENIDIUM_TESTNET: "https://evm-testnet.venidiumexplorer.com/",
        EthereumNetwork.VENIDIUM_MAINNET: "https://evm.venidiumexplorer.com/",
        EthereumNetwork.KLAYTN_TESTNET_BAOBAB: "https://baobab.scope.klaytn.com/",
        EthereumNetwork.KLAYTN_MAINNET_CYPRESS: "https://scope.klaytn.com/",
        EthereumNetwork.ACALA_NETWORK: "https://blockscout.acala.network/",
        EthereumNetwork.KARURA_NETWORK_TESTNET: "https://blockscout.karura.network/",
        EthereumNetwork.ACALA_NETWORK_TESTNET: "https://blockscout.mandala.acala.network/",
        EthereumNetwork.ASTAR: "https://blockscout.com/astar/",
        EthereumNetwork.EVMOS: "https://evm.evmos.org",
        EthereumNetwork.EVMOS_TESTNET: "https://evm.evmos.dev",
        EthereumNetwork.RABBIT_ANALOG_TESTNET_CHAIN: "https://rabbit.analogscan.com",
        EthereumNetwork.KCC_MAINNET: "https://scan.kcc.io/",
        EthereumNetwork.KCC_TESTNET: "https://scan-testnet.kcc.network/",
        EthereumNetwork.ARBITRUM_ONE: "https://explorer.arbitrum.io",
        EthereumNetwork.ARBITRUM_NOVA: "https://nova-explorer.arbitrum.io",
        EthereumNetwork.ARBITRUM_GOERLI: "https://goerli-rollup-explorer.arbitrum.io",
        EthereumNetwork.CROSSBELL: "https://scan.crossbell.io",
        EthereumNetwork.ETHEREUM_CLASSIC_MAINNET: "https://blockscout.com/etc/mainnet/",
        EthereumNetwork.ETHEREUM_CLASSIC_TESTNET_MORDOR: "https://blockscout.com/etc/mordor/",
    }

    def __init__(self, network: EthereumNetwork):
        self.network = network
        self.base_url = self.NETWORK_WITH_URL.get(network)
        if self.base_url is None:
            raise BlockScoutConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )
        self.grahpql_url = self.base_url + "/graphiql"
        self.http_session = requests.Session()

    def build_url(self, path: str):
        return urljoin(self.base_url, path)

    def _do_request(self, url: str, query: str) -> Optional[Dict[str, Any]]:
        response = self.http_session.post(url, json={"query": query}, timeout=10)
        if not response.ok:
            return None

        return response.json()

    def get_contract_metadata(
        self, address: ChecksumAddress
    ) -> Optional[ContractMetadata]:
        query = '{address(hash: "%s") { hash, smartContract {name, abi} }}' % address
        result = self._do_request(self.grahpql_url, query)
        if (
            result
            and "error" not in result
            and result.get("data", {}).get("address", {})
            and result["data"]["address"]["smartContract"]
        ):
            smart_contract = result["data"]["address"]["smartContract"]
            return ContractMetadata(
                smart_contract["name"], json.loads(smart_contract["abi"]), False
            )
