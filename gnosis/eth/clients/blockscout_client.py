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
        EthereumNetwork.ETHEREUM_CLASSIC: "https://blockscout.com/etc/mainnet/graphiql",
        EthereumNetwork.MORDOR_TESTNET: "https://blockscout.com/etc/mordor/graphiql",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "https://sepolia-blockscout.scroll.io/graphiql",
        EthereumNetwork.MANTLE: "https://explorer.mantle.xyz/api/v1/graphql",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz/graphiql",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org/graphiql",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org/graphiql",
        EthereumNetwork.ZETACHAIN_ATHENS_3_TESTNET: "https://zetachain-athens-3.blockscout.com/graphiql",
        EthereumNetwork.SCROLL: "https://blockscout.scroll.io/graphiql",
        EthereumNetwork.ROOTSTOCK_MAINNET: "https://rootstock.blockscout.com/graphiql",
        EthereumNetwork.ROOTSTOCK_TESTNET: "https://rootstock-testnet.blockscout.com/graphiql",
        EthereumNetwork.LINEA: "https://explorer.linea.build/graphiql",
        EthereumNetwork.LINEA_GOERLI: "https://explorer.goerli.linea.build/graphiql",
        EthereumNetwork.NEON_EVM_MAINNET: "https://neon.blockscout.com/graphiql",
        EthereumNetwork.NEON_EVM_DEVNET: "https://neon-devnet.blockscout.com/graphiql",
        EthereumNetwork.OASIS_SAPPHIRE: "https://explorer.sapphire.oasis.io/graphiql",
        EthereumNetwork.OASIS_SAPPHIRE_TESTNET: "https://testnet.explorer.sapphire.oasis.dev/graphiql",
        EthereumNetwork.CASCADIA_TESTNET: "https://explorer.cascadia.foundation/graphiql",
        EthereumNetwork.TENET: "https://tenetscan.io/graphiql",
        EthereumNetwork.TENET_TESTNET: "https://testnet.tenetscan.io/graphiql",
        EthereumNetwork.CRONOS_MAINNET: "https://cronos.org/explorer/graphiql",
        EthereumNetwork.CRONOS_TESTNET: "https://cronos.org/explorer/testnet3/graphiql",
        EthereumNetwork.THUNDERCORE_MAINNET: "https://explorer-mainnet.thundercore.com/graphiql",
        EthereumNetwork.THUNDERCORE_TESTNET: "https://explorer-testnet.thundercore.com/graphiql",
        EthereumNetwork.PGN_PUBLIC_GOODS_NETWORK: "https://explorer.publicgoods.network/graphiql",
        EthereumNetwork.SEPOLIA_PGN_PUBLIC_GOODS_NETWORK: "https://explorer.sepolia.publicgoods.network/graphiql",
        EthereumNetwork.ARTHERA_MAINNET: "https://explorer.arthera.net/graphiql",
        EthereumNetwork.ARTHERA_TESTNET: "https://explorer-test.arthera.net/graphiql",
        EthereumNetwork.MANTA_PACIFIC_MAINNET: "https://pacific-explorer.manta.network/graphiql",
        EthereumNetwork.KROMA: "https://blockscout.kroma.network/graphiql",
        EthereumNetwork.KROMA_SEPOLIA: "https://blockscout.sepolia.kroma.network/graphiql",
        EthereumNetwork.ZORA: "https://explorer.zora.energy/graphiql",
        EthereumNetwork.ZORA_SEPOLIA_TESTNET: "https://sepolia.explorer.zora.energy/graphiql",
        EthereumNetwork.HAQQ_NETWORK: "https://explorer.haqq.network/graphiql",
        EthereumNetwork.HAQQ_CHAIN_TESTNET: "https://explorer.testedge2.haqq.network/graphiql",
        EthereumNetwork.MODE: "https://explorer.mode.network/graphiql",
        EthereumNetwork.MODE_TESTNET: "https://sepolia.explorer.mode.network/graphiql",
        EthereumNetwork.MANTLE_SEPOLIA_TESTNET: "https://explorer.sepolia.mantle.xyz/api/v1/graphql",
        EthereumNetwork.OP_SEPOLIA_TESTNET: "https://optimism-sepolia.blockscout.com/graphiql",
        EthereumNetwork.UNREAL_TESTNET: "https://unreal.blockscout.com/graphiql",
        EthereumNetwork.TAIKO_KATLA_L2: "https://explorer.katla.taiko.xyz/graphiql",
        EthereumNetwork.SEI_DEVNET: "https://seitrace.com/graphiql",
        EthereumNetwork.LISK_SEPOLIA_TESTNET: "https://sepolia-blockscout.lisk.com/api/v1/graphql",
        EthereumNetwork.BOTANIX_TESTNET: "https://blockscout.botanixlabs.dev/graphiql",
        EthereumNetwork.REYA_NETWORK: "https://explorer.reya.network/graphiql",
        EthereumNetwork.AURORIA_TESTNET: "https://auroria.explorer.stratisevm.com/graphiql",
        EthereumNetwork.STRATIS_MAINNET: "https://explorer.stratisevm.com/graphiql",
        EthereumNetwork.SHIMMEREVM: "https://explorer.evm.shimmer.network/graphiql",
        EthereumNetwork.IOTA_EVM: "https://iota-evm.blockscout.com/graphiql",
        EthereumNetwork.BITROCK_MAINNET: "https://explorer.bit-rock.io/api/v1/graphql",
        EthereumNetwork.BITROCK_TESTNET: "https://testnetscan.bit-rock.io/api/v1/graphql",
        EthereumNetwork.OP_CELESTIA_RASPBERRY: "https://opcelestia-raspberry.gelatoscout.com/api/v1/graphql",
        EthereumNetwork.POLYGON_BLACKBERRY: "https://polygon-blackberry.gelatoscout.com/api/v1/graphql",
        EthereumNetwork.ARBITRUM_BLUEBERRY: "https://arb-blueberry.gelatoscout.com/api/v1/graphql",
        EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: "https://scan.testnet.rss3.io/api/v1/graphql",
        EthereumNetwork.RSS3_VSL_MAINNET: "https://scan.rss3.io/api/v1/graphql",
        EthereumNetwork.CROSSFI_TESTNET: "https://scan.testnet.ms/graphiql",
        EthereumNetwork.ASTAR_ZKYOTO: "https://astar-zkyoto.blockscout.com/api/v1/graphql",
        EthereumNetwork.SAAKURU_MAINNET: "https://explorer.saakuru.network/graphiql",
        EthereumNetwork.REDSTONE: "https://explorer.redstone.xyz/api/v1/graphql",
        EthereumNetwork.GARNET_HOLESKY: "https://api.explorer.garnet.qry.live/api/v1/graphql",
        EthereumNetwork.TAIKO_HEKLA_L2: "https://blockscoutapi.hekla.taiko.xyz/graphiql",
        EthereumNetwork.ASTAR_ZKEVM: "https://astar-zkevm.explorer.startale.com/api/v1/graphql",
        EthereumNetwork.RE_AL: "https://explorer.re.al/api/v1/graphql",
        EthereumNetwork.UNREAL: "https://unreal.blockscout.com/api/v1/graphql",
        EthereumNetwork.LISK: "https://blockscout.lisk.com/api/v1/graphql",
        EthereumNetwork.OPEN_CAMPUS_CODEX: "https://opencampus-codex.blockscout.com/api/v1/graphql",
        EthereumNetwork.LORENZO: "https://scan.lorenzo-protocol.xyz/api/v1/graphql",
        EthereumNetwork.DODOCHAIN_TESTNET: "https://testnet-scan.dodochain.com/api/v1/graphql",
        EthereumNetwork.ETHERLINK_MAINNET: "https://explorer.etherlink.com/api/v1/graphql",
        EthereumNetwork.ETHERLINK_TESTNET: "https://testnet-explorer.etherlink.com/api/v1/graphql",
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
