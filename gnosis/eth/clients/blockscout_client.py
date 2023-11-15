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
        EthereumNetwork.GNOSIS: "https://gnosis.blockscout.com/api/v1/graphql",
        EthereumNetwork.ENERGY_WEB_CHAIN: "https://explorer.energyweb.org/graphiql",
        EthereumNetwork.ENERGY_WEB_VOLTA_TESTNET: "https://volta-explorer.energyweb.org/graphiql",
        EthereumNetwork.POLIS_MAINNET: "https://explorer.polis.tech/graphiql",
        EthereumNetwork.BOBA_NETWORK: "https://blockexplorer.boba.network/graphiql",
        EthereumNetwork.GATHER_DEVNET_NETWORK: "https://devnet-explorer.gather.network/graphiql",
        EthereumNetwork.GATHER_TESTNET_NETWORK: "https://testnet-explorer.gather.network/graphiql",
        EthereumNetwork.GATHER_MAINNET_NETWORK: "https://explorer.gather.network/graphiql",
        EthereumNetwork.METIS_GOERLI_TESTNET: "https://goerli.explorer.metisdevops.link/graphiql",
        EthereumNetwork.METIS_ANDROMEDA_MAINNET: "https://andromeda-explorer.metis.io/graphiql",
        EthereumNetwork.FUSE_MAINNET: "https://explorer.fuse.io/graphiql",
        EthereumNetwork.VELAS_EVM_MAINNET: "https://evmexplorer.velas.com/graphiql",
        EthereumNetwork.REI_NETWORK: "https://scan.rei.network/graphiql",
        EthereumNetwork.REI_CHAIN_TESTNET: "https://scan-test.rei.network/graphiql",
        EthereumNetwork.METER_MAINNET: "https://scan.meter.io/graphiql",
        EthereumNetwork.METER_TESTNET: "https://scan-warringstakes.meter.io/graphiql",
        EthereumNetwork.GODWOKEN_TESTNET_V1: "https://v1.betanet.gwscan.com/graphiql",
        EthereumNetwork.GODWOKEN_MAINNET: "https://v1.gwscan.com/graphiql",
        EthereumNetwork.VENIDIUM_TESTNET: "https://evm-testnet.venidiumexplorer.com/graphiql",
        EthereumNetwork.VENIDIUM_MAINNET: "https://evm.venidiumexplorer.com/graphiql",
        EthereumNetwork.KLAYTN_TESTNET_BAOBAB: "https://baobab.scope.klaytn.com/graphiql",
        EthereumNetwork.KLAYTN_MAINNET_CYPRESS: "https://scope.klaytn.com/graphiql",
        EthereumNetwork.ACALA_NETWORK: "https://blockscout.acala.network/graphiql",
        EthereumNetwork.KARURA_NETWORK_TESTNET: "https://blockscout.karura.network/graphiql",
        EthereumNetwork.ASTAR: "https://blockscout.com/astar/graphiql",
        EthereumNetwork.SHIDEN: "https://blockscout.com/shiden/graphiql",
        EthereumNetwork.EVMOS: "https://evm.evmos.org/graphiql",
        EthereumNetwork.EVMOS_TESTNET: "https://evm.evmos.dev/graphiql",
        EthereumNetwork.KCC_MAINNET: "https://scan.kcc.io/graphiql",
        EthereumNetwork.KCC_TESTNET: "https://scan-testnet.kcc.network/graphiql",
        EthereumNetwork.CROSSBELL: "https://scan.crossbell.io/graphiql",
        EthereumNetwork.ETHEREUM_CLASSIC_MAINNET: "https://blockscout.com/etc/mainnet/graphiql",
        EthereumNetwork.ETHEREUM_CLASSIC_TESTNET_MORDOR: "https://blockscout.com/etc/mordor/graphiql",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "https://sepolia-blockscout.scroll.io/graphiql",
        EthereumNetwork.MANTLE: "https://explorer.mantle.xyz/graphiql",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz/graphiql",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org/graphiql",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org/graphiql",
        EthereumNetwork.ZETACHAIN_ATHENS_TESTNET: "https://zetachain-athens-3.blockscout.com/graphiql",
        EthereumNetwork.SCROLL: "https://blockscout.scroll.io/graphiql",
        EthereumNetwork.RSK_MAINNET: "https://rootstock.blockscout.com/graphiql",
        EthereumNetwork.RSK_TESTNET: "https://rootstock-testnet.blockscout.com/graphiql",
        EthereumNetwork.LINEA: "https://explorer.linea.build/graphiql",
        EthereumNetwork.LINEA_TESTNET: "https://explorer.goerli.linea.build/graphiql",
        EthereumNetwork.NEON_EVM_MAINNET: "https://neon.blockscout.com/graphiql",
        EthereumNetwork.NEON_EVM_DEVNET: "https://neon-devnet.blockscout.com/graphiql",
        EthereumNetwork.OASIS_SAPPHIRE: "https://explorer.sapphire.oasis.io/graphiql",
        EthereumNetwork.OASIS_SAPPHIRE_TESTNET: "https://testnet.explorer.sapphire.oasis.dev/graphiql",
        EthereumNetwork.CASCADIA_TESTNET: "https://explorer.cascadia.foundation/graphiql",
        EthereumNetwork.TENET: "https://tenetscan.io/graphiql",
        EthereumNetwork.TENET_TESTNET: "https://testnet.tenetscan.io/graphiql",
        EthereumNetwork.VELAS_EVM_MAINNET: "https://evmexplorer.velas.com/graphiql",
        EthereumNetwork.CRONOS_MAINNET_BETA: "https://cronos.org/explorer/graphiql",
        EthereumNetwork.CRONOS_TESTNET: "https://cronos.org/explorer/testnet3/graphiql",
        EthereumNetwork.THUNDERCORE_MAINNET: "https://explorer-mainnet.thundercore.com/graphiql",
        EthereumNetwork.THUNDERCORE_TESTNET: "https://explorer-testnet.thundercore.com/graphiql",
    }

    def __init__(self, network: EthereumNetwork):
        self.network = network
        self.grahpql_url = self.NETWORK_WITH_URL.get(network)
        if self.grahpql_url is None:
            raise BlockScoutConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )
        self.http_session = requests.Session()

    def build_url(self, path: str):
        return urljoin(self.grahpql_url, path)

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
