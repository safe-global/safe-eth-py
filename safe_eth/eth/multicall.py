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
from eth_typing import BlockIdentifier, BlockNumber, ChecksumAddress, HexAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract.contract import Contract, ContractFunction
from web3.exceptions import ContractLogicError

from . import EthereumClient, EthereumNetwork, EthereumNetworkNotSupported
from .contracts import ContractBase, get_multicall_v3_contract
from .ethereum_client import EthereumTxSent
from .exceptions import BatchCallFunctionFailed, ContractAlreadyDeployed
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
        EthereumNetwork.BNB_SMART_CHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BNB_SMART_CHAIN_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.RINKEBY: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.KCC_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.KCC_TESTNET: "0x665683D9bd41C09cF38c3956c926D9924F1ADa97",
        EthereumNetwork.ROPSTEN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CELO_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CELO_ALFAJORES_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.AURORA_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BASE_GOERLI_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.METIS_ANDROMEDA_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.DOGECHAIN_MAINNET: "0x68a8609a60a008EFA633dfdec592c03B030cC508",
        EthereumNetwork.ZKSYNC_MAINNET: "0xF9cda624FBC7e059355ce98a31693d299FACd963",
        EthereumNetwork.IMMUTABLE_ZKEVM_TESTNET: "0x2CC787Ed364600B0222361C4188308Fa8E68bA60",
        EthereumNetwork.PLINGA_MAINNET: "0x0989576160f2e7092908BB9479631b901060b6e4",
        EthereumNetwork.ABSTRACT_TESTNET: "0xF9cda624FBC7e059355ce98a31693d299FACd963",
        EthereumNetwork.MEVERSE_CHAIN_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.DFK_CHAIN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CRONOS_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.GNOSIS_CHIADO_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.AMOY: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SEI_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.HARMONY_MAINNET_SHARD_0: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BASE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BLAST_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.PGN_PUBLIC_GOODS_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.EDGEWARE_EDGEEVM_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.THAICHAIN: "0x0DaD6130e832c21719C5CE3bae93454E16A84826",
        EthereumNetwork.FUSE_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OKXCHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.PULSECHAIN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.PULSECHAIN_TESTNET_V4: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.IMMUTABLE_ZKEVM: "0x236bdA4589e44e6850f5aC6a74BfCa398a86c6c0",
        EthereumNetwork.IOTEX_NETWORK_TESTNET: "0xb5cecD6894c6f473Ec726A176f1512399A2e355d",
        EthereumNetwork.PALM_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.UNREAL: "0x8b6B0e60D8CD84898Ea8b981065A12F876eA5677",
        EthereumNetwork.ASSET_CHAIN_TESTNET: "0x989F832D35988cb5e3eB001Fa2Fe789469EC31Ea",
        EthereumNetwork.KAIA_KAIROS_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CANTO: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LISK: "0xA9d71E1dd7ca26F26e656E66d6AA81ed7f745bf0",
        EthereumNetwork.PHOENIX_MAINNET: "0x498cF757a575cFF2c2Ed9f532f56Efa797f86442",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.NEXI_MAINNET: "0x0277A46Cc69A57eE3A6C8c158bA874832F718B8E",
        EthereumNetwork.BEAM: "0x4956F15eFdc3dC16645e90Cc356eAFA65fFC65Ec",
        EthereumNetwork.TAIKO_MAINNET: "0xcb2436774C3e191c85056d248EF4260ce5f27A9D",
        EthereumNetwork.MINATO: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.EOS_EVM_NETWORK_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.KAVA_TESTNET: "0xDf1D724A7166261eEB015418fe8c7679BBEa7fd6",
        EthereumNetwork.IOTEX_NETWORK_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FILECOIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LINEA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CONFLUX_ESPACE_TESTNET: "0xEFf0078910f638cd81996cc117bccD3eDf2B072F",
        EthereumNetwork.BITTORRENT_CHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.WANCHAIN_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.THE_ROOT_NETWORK_MAINNET: "0xc9C2E2429AeC354916c476B30d729deDdC94988d",
        EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BOB: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.PREVIEWNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BLAST: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FORMA: "0xd53C6FFB123F7349A32980F87faeD8FfDc9ef079",
        EthereumNetwork.XDC_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.METAL_L2: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BOB_SEPOLIA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.X_LAYER_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZKFAIR_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OASIS_SAPPHIRE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LINEA_GOERLI: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MANTA_PACIFIC_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.XAI_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.NEON_EVM_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ASTAR: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.WANCHAIN: "0xcDF6A1566e78EB4594c86Fe73Fcdc82429e97fbB",
        EthereumNetwork.FRAXTAL_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.X_LAYER_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FUNKI_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BERACHAIN_BARTIO: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BASE_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CRONOS_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.GARNET_HOLESKY: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.PUPPYNET: "0xA4029b74FBA366c926eDFA7Dd10B21C621170a4c",
        EthereumNetwork.ROLLUX_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZIRCUIT_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZKSYNC_SEPOLIA_TESTNET: "0xF9cda624FBC7e059355ce98a31693d299FACd963",
        EthereumNetwork.ATLETA_OLYMPIA: "0x1472ec6392180fb84F345d2455bCC75B26577115",
        EthereumNetwork.KAIA_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SHIBARIUM: "0x864Bf681ADD6052395188A89101A1B37d3B4C961",
        EthereumNetwork.ASTAR_ZKEVM: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.INEVM_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.GRAVITY_ALPHA_MAINNET: "0xf8ac4BEB2F75d2cFFb588c63251347fdD629B92c",
        EthereumNetwork.SYSCOIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.JIBCHAIN_L1: "0xc0C8C486D1466C57Efe13C2bf000d4c56F47CBdC",
        EthereumNetwork.MODE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ROOTSTOCK_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.METACHAIN_MAINNET: "0x0000000000000000000000000000000000003001",
        EthereumNetwork.CYBER_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MEVERSE_CHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.DEFICHAIN_EVM_NETWORK_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.POLYGON_ZKEVM_CARDONA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ROLLUX_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SHAPE_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MANTA_PACIFIC_TESTNET: "0x211B1643b95Fe76f11eD8880EE810ABD9A4cf56C",
        EthereumNetwork.RE_AL: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.TELOS_EVM_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SEPOLIA_PGN_PUBLIC_GOODS_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LISK_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OPBNB_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZORA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MANTLE_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CYBER_TESTNET: "0xffc391F0018269d4758AEA1a144772E8FB99545E",
        EthereumNetwork.KAVA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZORA_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OP_SEPOLIA_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MOONBASE_ALPHA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LUKSO_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SCROLL: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.OPBNB_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FRAXTAL: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CROSSBELL: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.REDSTONE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LUKSO_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.TAIKO_JOLNIR_L2: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.DARWINIA_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SOPHON_TESTNET: "0x83c04d112adedA2C6D9037bb6ecb42E7f0b108Af",
        EthereumNetwork.XDC_APOTHEM_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MOONBEAM: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.RSS3_VSL_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.METIS_GOERLI_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SYSCOIN_TANENBAUM_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LYRA_CHAIN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.METACHAIN_ISTANBUL: "0x0000000000000000000000000000000000003001",
        EthereumNetwork.PLAYFI_ALBIREO_TESTNET: "0xF9cda624FBC7e059355ce98a31693d299FACd963",
        EthereumNetwork.NEON_EVM_DEVNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CONFLUX_ESPACE: "0xEFf0078910f638cd81996cc117bccD3eDf2B072F",
        EthereumNetwork.BEAM_TESTNET: "0x9BF49b704EE2A095b95c1f2D4EB9010510c41C9E",
        EthereumNetwork.PUBLICMINT_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MOONRIVER: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MANTA_PACIFIC_SEPOLIA_TESTNET: "0xca54918f7B525C8df894668846506767412b53E3",
        EthereumNetwork.CRAB_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.PALM: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MANTLE_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZETACHAIN_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.APEX_TESTNET: "0xf7642be33a6b18D16a995657adb5a68CD0438aE2",
        EthereumNetwork.ASTAR_ZKYOTO: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MODE_TESTNET: "0xBAba8373113Fb7a68f195deF18732e01aF8eDfCF",
        EthereumNetwork.ARBITRUM_SEPOLIA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.CORE_BLOCKCHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.MANTLE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.HOLESKY: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ETHERLINK_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZETACHAIN_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.DEFICHAIN_EVM_NETWORK_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.LINEA_SEPOLIA: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.BOBA_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.DARWINIA_KOI_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.THE_ROOT_NETWORK_PORCINI_TESTNET: "0xc9C2E2429AeC354916c476B30d729deDdC94988d",
        EthereumNetwork.ARTELA_TESTNET: "0xd07c8635f76e8745Ee7092fbb6e8fbc5FeF09DD7",
        EthereumNetwork.EOS_EVM_NETWORK: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_NEBULA_HUB: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_CALYPSO_HUB: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_TITAN_HUB: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_EUROPA_HUB_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_EUROPA_HUB: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_CALYPSO_HUB_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_NEBULA_HUB_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SKALE_TITAN_HUB_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZENCHAIN_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SNAXCHAIN: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.SHAPE: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FUSION_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.VICTION_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.ZIRCUIT_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FUSION_TESTNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.AREON_NETWORK_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
        EthereumNetwork.FLARE_MAINNET: "0xcA11bde05977b3631167028862bE2a173976CA11",
    }

    def __init__(
        self,
        ethereum_client: EthereumClient,
        multicall_contract_address: Optional[ChecksumAddress] = None,
    ):
        ethereum_network = ethereum_client.get_network()
        address = multicall_contract_address or self.ADDRESSES.get(ethereum_network)
        mainnet_address = self.ADDRESSES.get(EthereumNetwork.MAINNET)
        if not address and mainnet_address:
            # Try with Multicall V3 deterministic address
            address = ChecksumAddress(HexAddress(HexStr(mainnet_address)))
            if not ethereum_client.is_contract(address):
                raise EthereumNetworkNotSupported(
                    "Multicall contract not available for %s", ethereum_network.name
                )

        if not address:
            raise ValueError("Contract address cannot be none")

        super().__init__(ChecksumAddress(HexAddress(HexStr(address))), ethereum_client)

    def get_contract_fn(self) -> Callable[[Web3, Optional[ChecksumAddress]], Contract]:
        return get_multicall_v3_contract

    @classmethod
    def deploy_contract(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> Optional[EthereumTxSent]:
        """
        Deploy contract

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: ``EthereumTxSent`` with the deployed contract address, ``None`` if already deployed
        """
        contract_fn = cls.get_contract_fn(cls)  # type: ignore[arg-type]
        contract = contract_fn(ethereum_client.w3, None)
        constructor_data = contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]

        try:
            ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
                deployer_account, constructor_data
            )
            assert ethereum_tx_sent.contract_address is not None
            contract_address = ethereum_tx_sent.contract_address
            logger.info(
                "Deployed Multicall V2 Contract %s by %s",
                contract_address,
                deployer_account.address,
            )
            # Add address to addresses dictionary
            cls.ADDRESSES[ethereum_client.get_network()] = contract_address
            return ethereum_tx_sent
        except ContractAlreadyDeployed as e:
            cls.ADDRESSES[ethereum_client.get_network()] = e.address
            return None

    @staticmethod
    def _build_payload(
        contract_functions: Sequence[ContractFunction],
    ) -> Tuple[List[Tuple[ChecksumAddress, HexBytes]], List[List[Any]]]:
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
    ) -> Tuple[List[Tuple[ChecksumAddress, HexBytes]], List[List[Any]]]:
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
        return None

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
                block_identifier=block_identifier or "latest"
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
            self._decode_data(output_type, data) if data is not None else None
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
            ).call(block_identifier=block_identifier or "latest")

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
                if multicall_result.success and multicall_result.return_data is not None
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
                if multicall_result.success and multicall_result.return_data is not None
                else multicall_result.return_data,
            )
            for output_type, multicall_result in zip(output_types, results)
        ]
