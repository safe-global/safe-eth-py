import json
import os
import time
from typing import Any, Dict, List, MutableMapping, Optional, Union
from urllib.parse import urljoin

from ...util.http import prepare_http_session
from .. import EthereumNetwork
from .contract_metadata import ContractMetadata


class EtherscanClientException(Exception):
    pass


class EtherscanClientConfigurationProblem(Exception):
    pass


class EtherscanRateLimitError(EtherscanClientException):
    pass


class EtherscanClient:
    NETWORK_WITH_URL = {
        EthereumNetwork.MAINNET: "https://etherscan.io",
        EthereumNetwork.RINKEBY: "https://rinkeby.etherscan.io",
        EthereumNetwork.ROPSTEN: "https://ropsten.etherscan.io",
        EthereumNetwork.GOERLI: "https://goerli.etherscan.io",
        EthereumNetwork.BNB_SMART_CHAIN_MAINNET: "https://bscscan.com",
        EthereumNetwork.POLYGON: "https://polygonscan.com",
        EthereumNetwork.POLYGON_ZKEVM: "https://zkevm.polygonscan.com",
        EthereumNetwork.OPTIMISM: "https://optimistic.etherscan.io",
        EthereumNetwork.ARBITRUM_ONE: "https://arbiscan.io",
        EthereumNetwork.ARBITRUM_NOVA: "https://nova.arbiscan.io",
        EthereumNetwork.ARBITRUM_GOERLI: "https://goerli.arbiscan.io",
        EthereumNetwork.AVALANCHE_C_CHAIN: "https://snowtrace.io",
        EthereumNetwork.GNOSIS: "https://gnosisscan.io",
        EthereumNetwork.MOONBEAM: "https://moonscan.io",
        EthereumNetwork.MOONRIVER: "https://moonriver.moonscan.io",
        EthereumNetwork.MOONBASE_ALPHA: "https://moonbase.moonscan.io",
        EthereumNetwork.CRONOS_MAINNET: "https://cronoscan.com",
        EthereumNetwork.CRONOS_TESTNET: "https://testnet.cronoscan.com",
        EthereumNetwork.CELO_MAINNET: "https://celoscan.io",
        EthereumNetwork.BASE_GOERLI_TESTNET: "https://goerli.basescan.org",
        EthereumNetwork.NEON_EVM_DEVNET: "https://devnet.neonscan.org",
        EthereumNetwork.NEON_EVM_MAINNET: "https://neonscan.org",
        EthereumNetwork.SEPOLIA: "https://sepolia.etherscan.io",
        EthereumNetwork.ZKSYNC_MAINNET: "https://era.zksync.network/",
        EthereumNetwork.FANTOM_OPERA: "https://ftmscan.com",
        EthereumNetwork.FANTOM_TESTNET: "https://testnet.ftmscan.com/",
        EthereumNetwork.LINEA: "https://lineascan.build",
        EthereumNetwork.LINEA_GOERLI: "https://goerli.lineascan.build",
        EthereumNetwork.MANTLE: "https://mantlescan.xyz/",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "https://sepolia.scrollscan.com",
        EthereumNetwork.SCROLL: "https://scrollscan.com",
        EthereumNetwork.KROMA: "https://blockscout.kroma.network",
        EthereumNetwork.KROMA_SEPOLIA: "https://blockscout.sepolia.kroma.network",
        EthereumNetwork.BLAST_SEPOLIA_TESTNET: "https://sepolia.blastscan.io",
        EthereumNetwork.FRAXTAL: "https://fraxscan.com",
        EthereumNetwork.BASE: "https://api.basescan.org/",
        EthereumNetwork.BLAST: "https://blastscan.io",
        EthereumNetwork.TAIKO_MAINNET: "https://taikoscan.io",
        EthereumNetwork.BASE_SEPOLIA_TESTNET: "https://sepolia.basescan.org",
        EthereumNetwork.HOLESKY: "https://holesky.etherscan.io",
        EthereumNetwork.LINEA_SEPOLIA: "https://sepolia.lineascan.build",
        EthereumNetwork.METIS_ANDROMEDA_MAINNET: "https://explorer.metis.io",
        EthereumNetwork.DOGECHAIN_MAINNET: "https://explorer.dogechain.dog",
        EthereumNetwork.FUSE_SPARKNET: "https://explorer.fusespark.io",
        EthereumNetwork.PLUME_TESTNET: "https://testnet-explorer.plumenetwork.xyz",
        EthereumNetwork.CHILIZ_CHAIN_MAINNET: "https://scan.chiliz.com",
        EthereumNetwork.GNOSIS_CHIADO_TESTNET: "https://blockscout.chiadochain.net",
        EthereumNetwork.AMOY: "https://amoy.polygonscan.com",
        EthereumNetwork.PGN_PUBLIC_GOODS_NETWORK: "https://explorer.publicgoods.network",
        EthereumNetwork.EDGEWARE_EDGEEVM_MAINNET: "https://edgscan.live",
        EthereumNetwork.BEAR_NETWORK_CHAIN_MAINNET: "https://brnkscan.bearnetwork.net",
        EthereumNetwork.THAICHAIN: "https://exp.thaichain.org",
        EthereumNetwork.FUSE_MAINNET: "https://explorer.fuse.io",
        EthereumNetwork.FLUENCE_TESTNET: "https://blockscout.testnet.fluence.dev",
        EthereumNetwork.PULSECHAIN: "https://scan.pulsechain.com",
        EthereumNetwork.IMMUTABLE_ZKEVM: "https://explorer.immutable.com",
        EthereumNetwork.BAHAMUT: "https://www.ftnscan.com",
        EthereumNetwork.ASSET_CHAIN_TESTNET: "https://scan-testnet.assetchain.org",
        EthereumNetwork.LISK: "https://blockscout.lisk.com",
        EthereumNetwork.NEXI_MAINNET: "https://www.nexiscan.com",
        EthereumNetwork.MINATO: "https://explorer-testnet.soneium.org",
        EthereumNetwork.EOS_EVM_NETWORK_TESTNET: "https://explorer.testnet.evm.eosnetwork.com",
        EthereumNetwork.BITTORRENT_CHAIN_MAINNET: "https://bttcscan.com",
        EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: "https://scan.testnet.rss3.io",
        EthereumNetwork.BITKUB_CHAIN: "https://www.bkcscan.com",
        EthereumNetwork.METAL_L2: "https://explorer.metall2.com",
        EthereumNetwork.SHIMMEREVM: "https://explorer.evm.shimmer.network",
        EthereumNetwork.HAQQ_CHAIN_TESTNET: "https://explorer.testedge2.haqq.network",
        EthereumNetwork.OASYS_MAINNET: "https://scan.oasys.games",
        EthereumNetwork.MANTA_PACIFIC_MAINNET: "https://pacific-explorer.manta.network",
        EthereumNetwork.FRAXTAL_TESTNET: "https://holesky.fraxscan.com",
        EthereumNetwork.ACALA_NETWORK: "https://blockscout.acala.network",
        EthereumNetwork.ANCIENT8_TESTNET: "https://scanv2-testnet.ancient8.gg",
        EthereumNetwork.FLARE_TESTNET_COSTON2: "https://coston2-explorer.flare.network",
        EthereumNetwork.PUPPYNET: "https://puppyscan.shib.io",
        EthereumNetwork.ROLLUX_MAINNET: "https://explorer.rollux.com",
        EthereumNetwork.ZKSYNC_SEPOLIA_TESTNET: "https://sepolia-era.zksync.network/",
        EthereumNetwork.ATLETA_OLYMPIA: "https://blockscout.atleta.network",
        EthereumNetwork.CELO_ALFAJORES_TESTNET: "https://celo-alfajores.blockscout.com",
        EthereumNetwork.GRAVITY_ALPHA_MAINNET: "https://explorer.gravity.xyz",
        EthereumNetwork.ANCIENT8: "https://scan.ancient8.gg",
        EthereumNetwork.DCHAIN_TESTNET: "https://dchaintestnet-2713017997578000-1.testnet.sagaexplorer.io",
        EthereumNetwork.SYSCOIN_MAINNET: "https://explorer.syscoin.org",
        EthereumNetwork.TENET: "https://tenetscan.io",
        EthereumNetwork.JIBCHAIN_L1: "https://exp-l1.jibchain.net",
        EthereumNetwork.IOTA_EVM_TESTNET: "https://explorer.evm.testnet.iotaledger.net",
        EthereumNetwork.IOTA_EVM: "https://explorer.evm.iota.org",
        EthereumNetwork.BITKUB_CHAIN_TESTNET: "https://testnet.bkcscan.com",
        EthereumNetwork.ROLLUX_TESTNET: "https://rollux.tanenbaum.io",
        EthereumNetwork.MANTA_PACIFIC_TESTNET: "https://pacific-explorer.testnet.manta.network",
        EthereumNetwork.HAQQ_NETWORK: "https://explorer.haqq.network",
        EthereumNetwork.ACALA_MANDALA_TESTNET_TC9: "https://blockscout.mandala.aca-staging.network",
        EthereumNetwork.BERESHEET_BEREEVM_TESTNET: "https://testnet.edgscan.live",
        EthereumNetwork.SEPOLIA_PGN_PUBLIC_GOODS_NETWORK: "https://explorer.sepolia.publicgoods.network",
        EthereumNetwork.LISK_SEPOLIA_TESTNET: "https://sepolia-blockscout.lisk.com",
        EthereumNetwork.ZORA: "https://explorer.zora.energy",
        EthereumNetwork.SATOSHIVM_ALPHA_MAINNET: "https://svmscan.io",
        EthereumNetwork.MANTLE_SEPOLIA_TESTNET: "https://explorer.sepolia.mantle.xyz/",
        EthereumNetwork.SHIMMEREVM_TESTNET: "https://explorer.evm.testnet.shimmer.network",
        EthereumNetwork.BEVM_MAINNET: "https://scan-mainnet.bevm.io",
        EthereumNetwork.CHILIZ_SPICY_TESTNET: "http://spicy-explorer.chiliz.com",
        EthereumNetwork.DCHAIN: "https://dchain-2716446429837000-1.sagaexplorer.io",
        EthereumNetwork.ZORA_SEPOLIA_TESTNET: "https://sepolia.explorer.zora.energy/",
        EthereumNetwork.BLACKFORT_EXCHANGE_NETWORK_TESTNET: "https://testnet-explorer.blackfort.network",
        EthereumNetwork.OP_SEPOLIA_TESTNET: "https://optimism-sepolia.blockscout.com",
        EthereumNetwork.SATOSHIVM_TESTNET: "https://testnet.svmscan.io",
        EthereumNetwork.LUKSO_TESTNET: "https://explorer.execution.testnet.lukso.network",
        EthereumNetwork.CROSSBELL: "https://scan.crossbell.io",
        EthereumNetwork.LUKSO_MAINNET: "https://explorer.execution.mainnet.lukso.network",
        EthereumNetwork.FLUENCE: "https://blockscout.mainnet.fluence.dev",
        EthereumNetwork.SONGBIRD_CANARY_NETWORK: "https://songbird-explorer.flare.network",
        EthereumNetwork.BLACKFORT_EXCHANGE_NETWORK: "https://explorer.blackfort.network",
        EthereumNetwork.RSS3_VSL_MAINNET: "https://scan.rss3.io",
        EthereumNetwork.MANTA_PACIFIC_SEPOLIA_TESTNET: "https://pacific-explorer.sepolia-testnet.manta.network",
        EthereumNetwork.KARURA_NETWORK: "https://blockscout.karura.network",
        EthereumNetwork.APEX_TESTNET: "https://exp-testnet.apexlayer.xyz",
        EthereumNetwork.MODE_TESTNET: "https://sepolia.explorer.mode.network",
        EthereumNetwork.ARBITRUM_SEPOLIA: "https://sepolia.arbiscan.io",
        EthereumNetwork.SONGBIRD_TESTNET_COSTON: "https://coston-explorer.flare.network",
        EthereumNetwork.FLARE_MAINNET: "https://flare-explorer.flare.network",
        EthereumNetwork.FLUENCE_STAGE: "https://blockscout.stage.fluence.dev",
        EthereumNetwork.Q_TESTNET: "https://explorer.qtestnet.org",
        EthereumNetwork.ARTELA_TESTNET: "https://betanet-scan.artela.network",
        EthereumNetwork.EOS_EVM_NETWORK: "https://explorer.evm.eosnetwork.com",
        EthereumNetwork.SHAPE_SEPOLIA_TESTNET: "https://explorer-sepolia.shape.network",
        EthereumNetwork.SHAPE: "https://shapescan.xyz",
        EthereumNetwork.FASTEX_CHAIN_BAHAMUT_OASIS_TESTNET: "https://oasis.ftnscan.com",
        EthereumNetwork.ASSET_CHAIN_MAINNET: "https://scan.assetchain.org",
        EthereumNetwork.PHOENIX_MAINNET: "https://phoenixplorer.com",
        EthereumNetwork.SNAXCHAIN: "https://explorer.snaxchain.io",
        EthereumNetwork.ZKFAIR_MAINNET: "https://scan.zkfair.io",
        EthereumNetwork.SONIC_MAINNET: "https://sonicscan.org",
    }

    NETWORK_WITH_API_URL = {
        EthereumNetwork.MAINNET: "https://api.etherscan.io",
        EthereumNetwork.RINKEBY: "https://api-rinkeby.etherscan.io",
        EthereumNetwork.ROPSTEN: "https://api-ropsten.etherscan.io",
        EthereumNetwork.GOERLI: "https://api-goerli.etherscan.io",
        EthereumNetwork.BNB_SMART_CHAIN_MAINNET: "https://api.bscscan.com",
        EthereumNetwork.POLYGON: "https://api.polygonscan.com",
        EthereumNetwork.POLYGON_ZKEVM: "https://api-zkevm.polygonscan.com",
        EthereumNetwork.OPTIMISM: "https://api-optimistic.etherscan.io",
        EthereumNetwork.ARBITRUM_ONE: "https://api.arbiscan.io",
        EthereumNetwork.ARBITRUM_NOVA: "https://api-nova.arbiscan.io",
        EthereumNetwork.ARBITRUM_GOERLI: "https://api-goerli.arbiscan.io",
        EthereumNetwork.ARBITRUM_SEPOLIA: "https://api-sepolia.arbiscan.io",
        EthereumNetwork.AVALANCHE_C_CHAIN: "https://api.snowtrace.io",
        EthereumNetwork.GNOSIS: "https://api.gnosisscan.io",
        EthereumNetwork.MOONBEAM: "https://api-moonbeam.moonscan.io",
        EthereumNetwork.MOONRIVER: "https://api-moonriver.moonscan.io",
        EthereumNetwork.MOONBASE_ALPHA: "https://api-moonbase.moonscan.io",
        EthereumNetwork.CRONOS_MAINNET: "https://api.cronoscan.com",
        EthereumNetwork.CRONOS_TESTNET: "https://api-testnet.cronoscan.com",
        EthereumNetwork.CELO_MAINNET: "https://api.celoscan.io",
        EthereumNetwork.BASE_GOERLI_TESTNET: "https://api-goerli.basescan.org",
        EthereumNetwork.NEON_EVM_DEVNET: "https://devnet-api.neonscan.org",
        EthereumNetwork.NEON_EVM_MAINNET: "https://api.neonscan.org",
        EthereumNetwork.SEPOLIA: "https://api-sepolia.etherscan.io",
        EthereumNetwork.ZKSYNC_MAINNET: "https://api-era.zksync.network",
        EthereumNetwork.FANTOM_OPERA: "https://api.ftmscan.com",
        EthereumNetwork.FANTOM_TESTNET: "https://api-testnet.ftmscan.com",
        EthereumNetwork.LINEA: "https://api.lineascan.build",
        EthereumNetwork.LINEA_GOERLI: "https://api-testnet.lineascan.build",
        EthereumNetwork.MANTLE: "https://api.mantlescan.xyz",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org/api",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org/api",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "https://api-sepolia.scrollscan.com",
        EthereumNetwork.SCROLL: "https://api.scrollscan.com",
        EthereumNetwork.KROMA: "https://blockscout.kroma.network",
        EthereumNetwork.KROMA_SEPOLIA: "https://blockscout.sepolia.kroma.network",
        EthereumNetwork.BLAST_SEPOLIA_TESTNET: "https://api-sepolia.blastscan.io",
        EthereumNetwork.FRAXTAL: "https://api.fraxscan.com",
        EthereumNetwork.BASE: "https://api.basescan.org",
        EthereumNetwork.BLAST: "https://api.blastscan.io",
        EthereumNetwork.TAIKO_MAINNET: "https://api.taikoscan.io",
        EthereumNetwork.BASE_SEPOLIA_TESTNET: "https://api-sepolia.basescan.org",
        EthereumNetwork.HOLESKY: "https://api-holesky.etherscan.io",
        EthereumNetwork.LINEA_SEPOLIA: "https://api-sepolia.lineascan.build",
        EthereumNetwork.METIS_ANDROMEDA_MAINNET: "https://api.routescan.io/v2/network/mainnet/evm/1088/etherscan",
        EthereumNetwork.DOGECHAIN_MAINNET: "https://explorer.dogechain.dog",
        EthereumNetwork.FUSE_SPARKNET: "https://explorer.fusespark.io",
        EthereumNetwork.PLUME_TESTNET: "https://testnet-explorer.plumenetwork.xyz",
        EthereumNetwork.CHILIZ_CHAIN_MAINNET: "https://scan.chiliz.com",
        EthereumNetwork.GNOSIS_CHIADO_TESTNET: "https://blockscout.chiadochain.net",
        EthereumNetwork.AMOY: "https://api-amoy.polygonscan.com",
        EthereumNetwork.PGN_PUBLIC_GOODS_NETWORK: "https://explorer.publicgoods.network",
        EthereumNetwork.EDGEWARE_EDGEEVM_MAINNET: "https://edgscan.live",
        EthereumNetwork.BEAR_NETWORK_CHAIN_MAINNET: "https://brnkscan.bearnetwork.net",
        EthereumNetwork.THAICHAIN: "https://exp.thaichain.org",
        EthereumNetwork.FUSE_MAINNET: "https://explorer.fuse.io",
        EthereumNetwork.FLUENCE_TESTNET: "https://blockscout.testnet.fluence.dev",
        EthereumNetwork.PULSECHAIN: "https://api.scan.pulsechain.com",
        EthereumNetwork.IMMUTABLE_ZKEVM: "https://explorer.immutable.com",
        EthereumNetwork.BAHAMUT: "https://www.ftnscan.com",
        EthereumNetwork.ASSET_CHAIN_TESTNET: "https://scan-testnet.assetchain.org",
        EthereumNetwork.LISK: "https://blockscout.lisk.com",
        EthereumNetwork.NEXI_MAINNET: "https://www.nexiscan.com",
        EthereumNetwork.MINATO: "https://explorer-testnet.soneium.org",
        EthereumNetwork.EOS_EVM_NETWORK_TESTNET: "https://explorer.testnet.evm.eosnetwork.com",
        EthereumNetwork.BITTORRENT_CHAIN_MAINNET: "https://api.bttcscan.com",
        EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: "https://scan.testnet.rss3.io",
        EthereumNetwork.BITKUB_CHAIN: "https://www.bkcscan.com",
        EthereumNetwork.METAL_L2: "https://explorer.metall2.com",
        EthereumNetwork.SHIMMEREVM: "https://explorer.evm.shimmer.network",
        EthereumNetwork.HAQQ_CHAIN_TESTNET: "https://explorer.testedge2.haqq.network",
        EthereumNetwork.OASYS_MAINNET: "https://scan.oasys.games",
        EthereumNetwork.MANTA_PACIFIC_MAINNET: "https://pacific-explorer.manta.network",
        EthereumNetwork.FRAXTAL_TESTNET: "https://api-holesky.fraxscan.com",
        EthereumNetwork.ACALA_NETWORK: "https://blockscout.acala.network",
        EthereumNetwork.ANCIENT8_TESTNET: "https://scanv2-testnet.ancient8.gg",
        EthereumNetwork.FLARE_TESTNET_COSTON2: "https://coston2-explorer.flare.network",
        EthereumNetwork.PUPPYNET: "https://puppyscan.shib.io",
        EthereumNetwork.ROLLUX_MAINNET: "https://explorer.rollux.com",
        EthereumNetwork.ZKSYNC_SEPOLIA_TESTNET: "https://api-sepolia-era.zksync.network",
        EthereumNetwork.ATLETA_OLYMPIA: "https://blockscout.atleta.network",
        EthereumNetwork.CELO_ALFAJORES_TESTNET: "https://celo-alfajores.blockscout.com",
        EthereumNetwork.GRAVITY_ALPHA_MAINNET: "https://explorer.gravity.xyz",
        EthereumNetwork.ANCIENT8: "https://scan.ancient8.gg",
        EthereumNetwork.DCHAIN_TESTNET: "https://api-dchaintestnet-2713017997578000-1.testnet.sagaexplorer.io",
        EthereumNetwork.SYSCOIN_MAINNET: "https://explorer.syscoin.org",
        EthereumNetwork.TENET: "https://tenetscan.io",
        EthereumNetwork.JIBCHAIN_L1: "https://exp-l1.jibchain.net",
        EthereumNetwork.IOTA_EVM_TESTNET: "https://explorer.evm.testnet.iotaledger.net",
        EthereumNetwork.IOTA_EVM: "https://explorer.evm.iota.org",
        EthereumNetwork.BITKUB_CHAIN_TESTNET: "https://testnet.bkcscan.com",
        EthereumNetwork.ROLLUX_TESTNET: "https://rollux.tanenbaum.io",
        EthereumNetwork.MANTA_PACIFIC_TESTNET: "https://pacific-explorer.testnet.manta.network",
        EthereumNetwork.HAQQ_NETWORK: "https://explorer.haqq.network",
        EthereumNetwork.ACALA_MANDALA_TESTNET_TC9: "https://blockscout.mandala.aca-staging.network",
        EthereumNetwork.BERESHEET_BEREEVM_TESTNET: "https://testnet.edgscan.live",
        EthereumNetwork.SEPOLIA_PGN_PUBLIC_GOODS_NETWORK: "https://explorer.sepolia.publicgoods.network",
        EthereumNetwork.LISK_SEPOLIA_TESTNET: "https://sepolia-blockscout.lisk.com",
        EthereumNetwork.ZORA: "https://explorer.zora.energy",
        EthereumNetwork.SATOSHIVM_ALPHA_MAINNET: "https://svmscan.io",
        EthereumNetwork.MANTLE_SEPOLIA_TESTNET: "https://explorer.sepolia.mantle.xyz",
        EthereumNetwork.SHIMMEREVM_TESTNET: "https://explorer.evm.testnet.shimmer.network",
        EthereumNetwork.BEVM_MAINNET: "https://scan-mainnet-api.bevm.io",
        EthereumNetwork.CHILIZ_SPICY_TESTNET: "http://spicy-explorer.chiliz.com",
        EthereumNetwork.DCHAIN: "https://api-dchain-2716446429837000-1.sagaexplorer.io",
        EthereumNetwork.ZORA_SEPOLIA_TESTNET: "https://sepolia.explorer.zora.energy",
        EthereumNetwork.BLACKFORT_EXCHANGE_NETWORK_TESTNET: "https://testnet-explorer.blackfort.network",
        EthereumNetwork.OP_SEPOLIA_TESTNET: "https://optimism-sepolia.blockscout.com",
        EthereumNetwork.SATOSHIVM_TESTNET: "https://testnet.svmscan.io",
        EthereumNetwork.LUKSO_TESTNET: "https://api.explorer.execution.testnet.lukso.network",
        EthereumNetwork.CROSSBELL: "https://scan.crossbell.io",
        EthereumNetwork.LUKSO_MAINNET: "https://api.explorer.execution.mainnet.lukso.network",
        EthereumNetwork.FLUENCE: "https://blockscout.mainnet.fluence.dev",
        EthereumNetwork.SONGBIRD_CANARY_NETWORK: "https://songbird-explorer.flare.network",
        EthereumNetwork.BLACKFORT_EXCHANGE_NETWORK: "https://explorer.blackfort.network",
        EthereumNetwork.RSS3_VSL_MAINNET: "https://scan.rss3.io",
        EthereumNetwork.MANTA_PACIFIC_SEPOLIA_TESTNET: "https://pacific-explorer.sepolia-testnet.manta.network",
        EthereumNetwork.KARURA_NETWORK: "https://blockscout.karura.network",
        EthereumNetwork.APEX_TESTNET: "https://exp-testnet.apexlayer.xyz",
        EthereumNetwork.MODE_TESTNET: "https://sepolia.explorer.mode.network",
        EthereumNetwork.SONGBIRD_TESTNET_COSTON: "https://coston-explorer.flare.network",
        EthereumNetwork.FLARE_MAINNET: "https://flare-explorer.flare.network",
        EthereumNetwork.FLUENCE_STAGE: "https://blockscout.stage.fluence.dev",
        EthereumNetwork.Q_TESTNET: "https://explorer.qtestnet.org",
        EthereumNetwork.ARTELA_TESTNET: "https://betanet-scan.artela.network",
        EthereumNetwork.EOS_EVM_NETWORK: "https://explorer.evm.eosnetwork.com",
        EthereumNetwork.SHAPE_SEPOLIA_TESTNET: "https://explorer-sepolia.shape.network",
        EthereumNetwork.SHAPE: "https://shapescan.xyz",
        EthereumNetwork.FASTEX_CHAIN_BAHAMUT_OASIS_TESTNET: "https://oasis.ftnscan.com",
        EthereumNetwork.ASSET_CHAIN_MAINNET: "https://scan.assetchain.org",
        EthereumNetwork.PHOENIX_MAINNET: "https://phoenixplorer.com",
        EthereumNetwork.SNAXCHAIN: "https://explorer.snaxchain.io",
        EthereumNetwork.ZKFAIR_MAINNET: "https://scan.zkfair.io",
        EthereumNetwork.SONIC_MAINNET: "https://api.sonicscan.org",
    }
    HTTP_HEADERS: MutableMapping[str, Union[str, bytes]] = {
        "User-Agent": "curl/7.77.0",
    }

    def __init__(
        self,
        network: EthereumNetwork,
        api_key: Optional[str] = None,
        request_timeout: int = int(
            os.environ.get("ETHERSCAN_CLIENT_REQUEST_TIMEOUT", 10)
        ),
    ):
        self.network = network
        self.api_key = api_key
        self.base_url = self.NETWORK_WITH_URL.get(network, "")
        self.base_api_url = self.NETWORK_WITH_API_URL.get(network, "")
        if not self.base_api_url:
            raise EtherscanClientConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )
        self.http_session = prepare_http_session(10, 100)
        self.http_session.headers = self.HTTP_HEADERS
        self.request_timeout = request_timeout

    def build_url(self, query: str):
        url = urljoin(self.base_api_url, f"api?{query}")
        if self.api_key:
            url += f"&apikey={self.api_key}"
        return url

    def _do_request(self, url: str) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        response = self.http_session.get(url, timeout=self.request_timeout)

        if response.ok:
            response_json = response.json()
            result = response_json["result"]
            if "Max rate limit reached" in result:
                # Max rate limit reached, please use API Key for higher rate limit
                raise EtherscanRateLimitError
            if response_json["status"] == "1":
                return result
        return None

    def _retry_request(
        self, url: str, retry: bool = True
    ) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        for _ in range(3):
            try:
                return self._do_request(url)
            except EtherscanRateLimitError as exc:
                if not retry:
                    raise exc
                else:
                    time.sleep(5)
        return None

    @staticmethod
    def _process_contract_metadata(
        contract_data: Dict[str, Any]
    ) -> Optional[ContractMetadata]:
        contract_name = contract_data["ContractName"]
        contract_abi = contract_data["ABI"]
        contract_proxy_implementation_address = (
            contract_data.get("Implementation") or None
        )
        if contract_abi:
            return ContractMetadata(
                contract_name,
                contract_abi,
                False,
                contract_proxy_implementation_address,
            )
        return None

    def get_contract_metadata(
        self, contract_address: str, retry: bool = True
    ) -> Optional[ContractMetadata]:
        contract_source_code = self.get_contract_source_code(
            contract_address, retry=retry
        )
        if contract_source_code:
            return self._process_contract_metadata(contract_source_code)
        return None

    @staticmethod
    def _process_get_contract_source_code_response(response):
        if response and isinstance(response, list):
            result = response[0]
            abi_str = result.get("ABI")

            if isinstance(abi_str, str) and abi_str.startswith("["):
                try:
                    result["ABI"] = json.loads(abi_str)
                except json.JSONDecodeError:
                    result["ABI"] = None  # Handle the case where JSON decoding fails
            else:
                result["ABI"] = None

            return result

    def get_contract_source_code(self, contract_address: str, retry: bool = True):
        """
        Get source code for a contract. Source code query also returns:

            - ContractName: "",
            - CompilerVersion: "",
            - OptimizationUsed: "",
            - Runs: "",
            - ConstructorArguments: ""
            - EVMVersion: "Default",
            - Library: "",
            - LicenseType: "",
            - Proxy: "0",
            - Implementation: "",
            - SwarmSource: ""

        :param contract_address:
        :param retry: if ``True``, try again if there's Rate Limit Error
        :return:
        """
        url = self.build_url(
            f"module=contract&action=getsourcecode&address={contract_address}"
        )
        response = self._retry_request(url, retry=retry)  # Returns a list
        return self._process_get_contract_source_code_response(response)

    def get_contract_abi(self, contract_address: str, retry: bool = True):
        url = self.build_url(
            f"module=contract&action=getabi&address={contract_address}"
        )
        result = self._retry_request(url, retry=retry)
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                pass
        return None
