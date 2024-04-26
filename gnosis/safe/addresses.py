"""
Contains information about Safe contract addresses deployed in every chain

Every entry contains a tuple with address, deployment block number and version
"""
from typing import Dict, List, Tuple

from eth_typing import ChecksumAddress

from gnosis.eth import EthereumNetwork

SAFE_SIMULATE_TX_ACCESSOR_ADDRESS: ChecksumAddress = (
    "0x3d4BA2E0884aa488718476ca2FB8Efc291A46199"
)

MASTER_COPIES: Dict[EthereumNetwork, List[Tuple[str, int, str]]] = {
    EthereumNetwork.MAINNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 17486982, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 17487000, "1.4.1"),
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            14981217,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12504423,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            17530813,
            "1.3.0",
        ),  # safe singleton factory
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            12504268,
            "1.3.0",
        ),  # default singleton address
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10329734, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 9084503, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 8915728, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 7457553, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 6766257, "0.1.0"),
        ("0xAC6072986E985aaBE7804695EC2d8970Cf7541A2", 6569433, "0.0.2"),
    ],
    EthereumNetwork.RINKEBY: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 8527380, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 8527381, "1.3.0"),
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 6723632, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 5590754, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 5423491, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 4110083, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 3392692, "0.1.0"),
        ("0x2727D69C0BD14B1dDd28371B8D97e808aDc1C2f7", 3055781, "0.0.2"),
    ],
    EthereumNetwork.GOERLI: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 9134479, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 9134480, "1.4.1"),
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            6900544,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4854168,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            6900547,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            4854169,
            "1.3.0",
        ),  # default singleton address
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 2930373, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 1798663, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 1631488, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 319108, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 34096, "0.1.0"),
    ],
    EthereumNetwork.GNOSIS: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 28204126, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 28204128, "1.4.1"),
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            27679972,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            16236936,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            27679975,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            16236998,
            "1.3.0",
        ),  # default singleton address
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10612049, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 10045292, "1.1.1"),
        ("0x2CB0ebc503dE87CFD8f0eCEED8197bF7850184ae", 12529466, "1.1.1+Circles"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 19560130, "1.0.0"),
    ],
    EthereumNetwork.ENERGY_WEB_CHAIN: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 12028662, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12028664, "1.3.0"),
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 6398655, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 6399212, "1.1.1"),
    ],
    EthereumNetwork.ENERGY_WEB_VOLTA_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 11942450, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 11942451, "1.3.0"),
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 6876086, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 6876642, "1.1.1"),
    ],
    EthereumNetwork.POLYGON: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 44367857, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 44367925, "1.4.1"),
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            34516629,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            14306478,
            "1.3.0+L2",
        ),  # default singleton address
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 14306478, "1.3.0"),
    ],
    EthereumNetwork.POLYGON_ZKEVM: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            4460434,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            79000,
            "1.3.0+L2",
        ),  # default singleton address
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 79000, "1.3.0"),
    ],
    EthereumNetwork.MUMBAI: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 13736914, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 13736914, "1.3.0"),
    ],
    EthereumNetwork.ARBITRUM_ONE: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            88610931,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1146,
            "1.3.0+L2",
        ),  # default singleton address
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1140, "1.3.0"),
    ],
    EthereumNetwork.ARBITRUM_NOVA: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 426, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 427, "1.3.0"),
    ],
    EthereumNetwork.ARBITRUM_RINKEBY: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 57070, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 57070, "1.3.0"),
    ],
    EthereumNetwork.ARBITRUM_GOERLI: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 11545, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 11546, "1.3.0"),
    ],
    EthereumNetwork.ARBITRUM_SEPOLIA: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 154, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 155, "1.3.0"),
    ],
    EthereumNetwork.BNB_SMART_CHAIN_MAINNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 31484712, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 31484715, "1.4.1"),
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            28092011,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            8485899,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            28092014,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            8485903,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.CELO_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 8944350, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 8944351, "1.3.0"),
    ],
    EthereumNetwork.AVALANCHE_C_CHAIN: [
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            22_123_383,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            4_949_507,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            14_747_111,
            "1.3.0",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            4_949_512,
            "1.3.0",
        ),  # safe singleton address
    ],
    EthereumNetwork.MOONBEAM: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 172_092, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 172_094, "1.3.0"),
    ],
    EthereumNetwork.MOONRIVER: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 707_738, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 707_741, "1.3.0"),
    ],
    EthereumNetwork.MOONBASE_ALPHA: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 939_244, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 939_246, "1.3.0"),
    ],
    EthereumNetwork.FUSE_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 12_725_078, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12_725_081, "1.3.0"),
    ],
    EthereumNetwork.FUSE_SPARKNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1_010_518, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1_010_520, "1.3.0"),
    ],
    EthereumNetwork.POLIS_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1227, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1278, "1.3.0"),
    ],
    EthereumNetwork.OPTIMISM: [
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            30813792,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            173749,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            3936972,
            "1.3.0",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            173751,
            "1.3.0",
        ),  # safe singleton address
    ],
    EthereumNetwork.BOBA_BNB_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 22284, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 22285, "1.3.0"),
    ],
    EthereumNetwork.BOBA_AVAX: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 55746, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 55747, "1.3.0"),
    ],
    EthereumNetwork.BOBA_NETWORK: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 170908, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 170910, "1.3.0"),
    ],
    EthereumNetwork.AURORA_MAINNET: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            111687756,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            52494543,
            "1.3.0+L2",
        ),  # default singleton address
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 52494556, "1.3.0"),
    ],
    EthereumNetwork.METIS_STARDUST_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 56124, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 56125, "1.3.0"),
    ],
    EthereumNetwork.METIS_GOERLI_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 131845, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 131846, "1.3.0"),
    ],
    EthereumNetwork.METIS_ANDROMEDA_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 61767, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 61768, "1.3.0"),
    ],
    EthereumNetwork.SHYFT_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1000, "1.3.0+L2"),  # v1.3.0
    ],
    EthereumNetwork.SHYFT_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1984340, "1.3.0+L2"),  # v1.3.0
    ],
    EthereumNetwork.REI_NETWORK: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2388036, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2388042, "1.3.0"),
    ],
    EthereumNetwork.METER_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 23863901, "1.3.0+L2")  # v1.3.0
    ],
    EthereumNetwork.METER_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 15035438, "1.3.0+L2")  # v1.3.0
    ],
    EthereumNetwork.EURUS_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 7127163, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 7127166, "1.3.0"),
    ],
    EthereumNetwork.EURUS_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 12845441, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12845443, "1.3.0"),
    ],
    EthereumNetwork.VENIDIUM_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1127191, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1127192, "1.3.0"),
    ],
    EthereumNetwork.VENIDIUM_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 761243, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 761244, "1.3.0"),
    ],
    EthereumNetwork.GODWOKEN_TESTNET_V1: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 93204, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 93168, "1.3.0"),
    ],
    EthereumNetwork.KLAYTN_TESTNET_BAOBAB: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 93821635, "1.3.0+L2"),
    ],
    EthereumNetwork.KLAYTN_MAINNET_CYPRESS: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 93507490, "1.3.0+L2"),
    ],
    EthereumNetwork.MILKOMEDA_A1_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 796, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 797, "1.3.0"),
    ],
    EthereumNetwork.MILKOMEDA_A1_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 6218, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 6042, "1.3.0"),
    ],
    EthereumNetwork.MILKOMEDA_C1_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 5080339, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 5080357, "1.3.0"),
    ],
    EthereumNetwork.MILKOMEDA_C1_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 4896727, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4896733, "1.3.0"),
    ],
    EthereumNetwork.CRONOS_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 3290833, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 3290835, "1.3.0"),
    ],
    EthereumNetwork.CRONOS_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 3002268, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 3002760, "1.3.0"),
    ],
    EthereumNetwork.RABBIT_ANALOG_TESTNET_CHAIN: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1434229, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1434230, "1.3.0"),
    ],
    EthereumNetwork.CLOUDWALK_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 13743076, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 13743082, "1.3.0"),
    ],
    EthereumNetwork.KCC_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 4860807, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4860810, "1.3.0"),
    ],
    EthereumNetwork.KCC_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 12147586, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12147596, "1.3.0"),
    ],
    EthereumNetwork.PUBLICMINT_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 19974991, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 19974993, "1.3.0"),
    ],
    EthereumNetwork.PUBLICMINT_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 14062206, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 14062208, "1.3.0"),
    ],
    EthereumNetwork.XDC_APOTHEM_NETWORK: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 42293309, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 42293315, "1.3.0"),
    ],
    EthereumNetwork.BASE: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            595207,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            2704166,
            "1.3.0+L2",
        ),  # default singleton address
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 595211, "1.3.0"),
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            8405927,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BASE_GOERLI_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 7330635, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7330643, "1.4.1"),
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 938848, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 939064, "1.3.0"),
    ],
    EthereumNetwork.BASE_SEPOLIA_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 3282054, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 3282056, "1.3.0"),
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 5125249, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5125256, "1.3.0"),
    ],
    EthereumNetwork.KAVA: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2116303, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2116307, "1.3.0"),
    ],
    EthereumNetwork.CROSSBELL: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 28314790, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 28314796, "1.3.0"),
    ],
    EthereumNetwork.IOTEX_NETWORK_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 22172521, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 22172524, "1.3.0"),
    ],
    EthereumNetwork.HARMONY_MAINNET_SHARD_0: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 22502193, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 22502199, "1.3.0"),
        ("0x3736aC8400751bf07c6A2E4db3F4f3D9D422abB2", 11526669, "1.2.0"),
    ],
    EthereumNetwork.HARMONY_TESTNET_SHARD_0: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 4824474, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4824480, "1.3.0"),
    ],
    EthereumNetwork.VELAS_EVM_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 27572492, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 27572642, "1.3.0"),
    ],
    EthereumNetwork.WEMIX3_0_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 12651754, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 12651757, "1.3.0"),
    ],
    EthereumNetwork.WEMIX3_0_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 20834033, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 20834039, "1.3.0"),
    ],
    EthereumNetwork.EVMOS_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 70652, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 70654, "1.3.0"),
    ],
    EthereumNetwork.EVMOS: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 158463, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 158486, "1.3.0"),
    ],
    EthereumNetwork.MAP_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 5190553, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 5190556, "1.3.0"),
    ],
    EthereumNetwork.MAP_MAKALU: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2987582, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2987584, "1.3.0"),
    ],
    EthereumNetwork.ETHEREUM_CLASSIC: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 15904944, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 15904946, "1.3.0"),
    ],
    EthereumNetwork.MORDOR_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 6333171, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 6333172, "1.3.0"),
    ],
    EthereumNetwork.SEPOLIA: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 3921532, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3921533, "1.4.1"),
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            2086878,
            "1.3.0+L2",
        ),  # Default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2087039,
            "1.3.0+L2",
        ),  # Safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            2086880,
            "1.3.0",
        ),  # Default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            2087040,
            "1.3.0",
        ),  # Safe singleton address
    ],
    EthereumNetwork.TENET_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 885391, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 885392, "1.3.0"),
    ],
    EthereumNetwork.TENET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 727470, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 727472, "1.3.0"),
    ],
    EthereumNetwork.LINEA_TESTNET: [
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            363132,
            "1.3.0+L2",
        ),  # Default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            3279607,
            "1.3.0+L2",
        ),  # Safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            363135,
            "1.3.0",
        ),  # Default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            3279611,
            "1.3.0",
        ),  # Safe singleton address
    ],
    EthereumNetwork.ASTAR: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1106426, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1106429, "1.3.0"),
    ],
    EthereumNetwork.SHIDEN: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1634935, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1634935, "1.3.0"),
    ],
    EthereumNetwork.DARWINIA_NETWORK: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            491175,
            "1.3.0+L2",
        )
    ],
    EthereumNetwork.CRAB_NETWORK: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            739900,
            "1.3.0+L2",
        )
    ],
    EthereumNetwork.ZORA: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            9677661,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            11932,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            9677757,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            11934,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.ZKSYNC_MAINNET: [
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 7259224, "1.3.0+L2"),
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 7259230, "1.3.0"),
    ],
    EthereumNetwork.MANTLE_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 4404246, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4404284, "1.3.0"),
    ],
    EthereumNetwork.MANTLE: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1511, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1512, "1.3.0"),
    ],
    EthereumNetwork.CASCADIA_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1408599, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1408613, "1.3.0"),
    ],
    EthereumNetwork.OASIS_SAPPHIRE: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 325640, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 325643, "1.3.0"),
    ],
    EthereumNetwork.OASIS_SAPPHIRE_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1378154, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1378155, "1.3.0"),
    ],
    EthereumNetwork.EDGEWARE_EDGEEVM_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 18176819, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 18176820, "1.3.0"),
    ],
    EthereumNetwork.LINEA: [
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            17,
            "1.3.0+L2",
        ),  # Default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1939925,
            "1.3.0+L2",
        ),  # Safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            18,
            "1.3.0",
        ),  # Default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            1939927,
            "1.3.0",
        ),  # Safe singleton address
    ],
    EthereumNetwork.NEON_EVM_DEVNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 205147021, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 205147000, "1.3.0"),
    ],
    EthereumNetwork.NEON_EVM_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 203994162, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 203994202, "1.3.0"),
    ],
    EthereumNetwork.SCROLL_SEPOLIA_TESTNET: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2913895,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            6261,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            2913898,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            6262,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.FANTOM_OPERA: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 38810826, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 21817262, "1.3.0"),
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 4580000, "1.3.0+L2"),
    ],
    EthereumNetwork.FANTOM_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4627348, "1.3.0"),
        ("0x5696Ae62C36aF747966522C401FbD57492451f19", 4627348, "1.3.0"),
    ],
    EthereumNetwork.ROOTSTOCK_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 3891238, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 3891240, "1.3.0"),
    ],
    EthereumNetwork.ROOTSTOCK_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2362236, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2362238, "1.3.0"),
    ],
    EthereumNetwork.BEAM: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 27629, "1.3.0"),
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 27628, "1.3.0+L2"),
    ],
    EthereumNetwork.BEAM_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 85332, "1.3.0"),
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 85331, "1.3.0+L2"),
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 7709133, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 7709135, "1.3.0"),
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1315570, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1315572, "1.3.0"),
    ],
    EthereumNetwork.ZETACHAIN_ATHENS_3_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1962980, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1962981, "1.3.0"),
    ],
    EthereumNetwork.SCROLL: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2905495,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            187,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            2905498,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            189,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.TELOS_EVM_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 237435759, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 237435774, "1.3.0"),
    ],
    EthereumNetwork.TELOS_EVM_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 194005796, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 194005824, "1.3.0"),
    ],
    EthereumNetwork.PGN_PUBLIC_GOODS_NETWORK: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 344345, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 344348, "1.3.0"),
    ],
    EthereumNetwork.SEPOLIA_PGN_PUBLIC_GOODS_NETWORK: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1774114, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1774116, "1.3.0"),
    ],
    EthereumNetwork.ARTHERA_MAINNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 5559, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5560, "1.4.1"),
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 5549, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5550, "1.3.0"),
    ],
    EthereumNetwork.ARTHERA_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 4186405, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 4186415, "1.4.1"),
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 119967, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 119968, "1.3.0"),
    ],
    EthereumNetwork.MANTA_PACIFIC_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 338471, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 338472, "1.3.0"),
    ],
    EthereumNetwork.KROMA: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 5281960, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5281965, "1.3.0"),
    ],
    EthereumNetwork.KROMA_SEPOLIA: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 7992402, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 7992408, "1.3.0"),
    ],
    EthereumNetwork.HAQQ_NETWORK: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 9054796, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 9054798, "1.4.1"),
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 422246, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 422357, "1.3.0"),
    ],
    EthereumNetwork.HAQQ_CHAIN_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 7031878, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7031879, "1.4.1"),
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1514959, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1514966, "1.3.0"),
    ],
    EthereumNetwork.MODE: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2610515, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2610520, "1.3.0"),
    ],
    EthereumNetwork.MODE_TESTNET: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            9375471,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1948156,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            9375476,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            1948159,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.ZORA_SEPOLIA_TESTNET: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            4265431,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            46719,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            4265435,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            46722,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.MANTLE_SEPOLIA_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1927686, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1927692, "1.3.0"),
    ],
    EthereumNetwork.OP_SEPOLIA_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 7162879, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7162883, "1.4.1"),
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4357288,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            7438249,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            4357293,
            "1.3.0",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            7438259,
            "1.3.0",
        ),  # safe singleton address
    ],
    EthereumNetwork.UNREAL_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 742, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 743, "1.3.0"),
    ],
    EthereumNetwork.TAIKO_KATLA_L2: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 136482, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 136484, "1.3.0"),
    ],
    EthereumNetwork.BERACHAIN_ARTIO: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 379846, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 380093, "1.3.0"),
    ],
    EthereumNetwork.SEI_DEVNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 4552451, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4552489, "1.3.0"),
    ],
    EthereumNetwork.LISK_SEPOLIA_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 657757, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 657761, "1.3.0"),
    ],
    EthereumNetwork.BOTANIX_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 165429, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 165430, "1.4.1"),
    ],
    EthereumNetwork.BLAST_SEPOLIA_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1087958, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1087964, "1.3.0"),
    ],
    EthereumNetwork.REYA_NETWORK: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 84, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 85, "1.3.0"),
    ],
    EthereumNetwork.FRAXTAL_MAINNET: [
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1675112,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            0,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            2353663,
            "1.3.0",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            0,
            "1.3.0",
        ),  # safe singleton address
    ],
    EthereumNetwork.AURORIA_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 186765, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.STRATIS_MAINNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 106947, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.SHIMMEREVM: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 155333, "1.3.0"),  # v1.3.0
    ],
    EthereumNetwork.IOTA_EVM: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 13225, "1.3.0"),  # v1.3.0
    ],
    EthereumNetwork.BITROCK_MAINNET: [
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            12949190,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BITROCK_TESTNET: [
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            13177774,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.XDC_NETWORK: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 53901624, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            53901616,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.OP_CELESTIA_RASPBERRY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1028180, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1028176,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.POLYGON_BLACKBERRY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 765162, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 765158, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.ARBITRUM_BLUEBERRY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 19373, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 19372, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.X_LAYER_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 359517, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 359442, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.PULSECHAIN: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12504423,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.PULSECHAIN_TESTNET_V4: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12504423,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2297637, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            2297627,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.RSS3_VSL_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1699411, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1699402,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.CROSSFI_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2322641, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2322638,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
}

PROXY_FACTORIES: Dict[EthereumNetwork, List[Tuple[str, int]]] = {
    EthereumNetwork.MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 17440707),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            14981216,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            12504126,
        ),  # v1.3.0 default singleton address
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 9084508),  # v1.1.1
        ("0x50e55Af101C777bA7A1d560a774A82eF002ced9F", 8915731),  # v1.1.0
        ("0x12302fE9c02ff50939BaAaaf415fc226C078613C", 7450116),  # v1.0.0
    ],
    EthereumNetwork.RINKEBY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 8493997),  # v1.3.0
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 5590757),
        ("0x50e55Af101C777bA7A1d560a774A82eF002ced9F", 5423494),
        ("0x12302fE9c02ff50939BaAaaf415fc226C078613C", 4110083),
    ],
    EthereumNetwork.GOERLI: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 8681525),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            6900531,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            4695402,
        ),  # v1.3.0 default singleton address
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 1798666),
        ("0x50e55Af101C777bA7A1d560a774A82eF002ced9F", 1631491),
        ("0x12302fE9c02ff50939BaAaaf415fc226C078613C", 312509),
    ],
    EthereumNetwork.GNOSIS: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 27419153),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            27679953,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            16236878,
        ),  # v1.3.0 default singleton address
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 10045327),  # v1.1.1
        ("0x12302fE9c02ff50939BaAaaf415fc226C078613C", 17677119),  # v1.0.0
    ],
    EthereumNetwork.ENERGY_WEB_CHAIN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12028652),  # v1.3.0
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 6399239),
    ],
    EthereumNetwork.ENERGY_WEB_VOLTA_TESTNET: [
        # ('0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2', 0),  # v1.3.0
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 6876681),
    ],
    EthereumNetwork.POLYGON: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 40683009),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            34504003,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            14306478,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.MUMBAI: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 13736914),  # v1.3.0
    ],
    EthereumNetwork.POLYGON_ZKEVM: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            4460053,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            79000,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.ARBITRUM_ONE: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            88610602,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            1140,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.ARBITRUM_NOVA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 419),  # v1.3.0
    ],
    EthereumNetwork.ARBITRUM_RINKEBY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 57070),  # v1.3.0
    ],
    EthereumNetwork.ARBITRUM_GOERLI: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 11538),  # v1.3.0
    ],
    EthereumNetwork.ARBITRUM_SEPOLIA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 147),  # v1.3.0
    ],
    EthereumNetwork.BNB_SMART_CHAIN_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 28092030),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            28059981,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            8485873,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.CELO_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 8944342),  # v1.3.0
    ],
    EthereumNetwork.AVALANCHE_C_CHAIN: [
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            14_747_108,
        ),  # v1.3.0 default singleton address
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            4_949_487,
        ),  # v1.3.0 safe singleton address
    ],
    EthereumNetwork.MOONBEAM: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 172078),  # v1.3.0
    ],
    EthereumNetwork.MOONRIVER: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 707_721),  # v1.3.0
    ],
    EthereumNetwork.MOONBASE_ALPHA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 939_239),  # v1.3.0
    ],
    EthereumNetwork.FUSE_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12_725_072),  # v1.3.0
    ],
    EthereumNetwork.FUSE_SPARKNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1_010_506),  # v1.3.0
    ],
    EthereumNetwork.POLIS_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1266),  # v1.3.0
    ],
    EthereumNetwork.OPTIMISM: [
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            3936933,
        ),  # v1.3.0 default singleton address
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            173709,
        ),  # v1.3.0 safe singleton address
    ],
    EthereumNetwork.BOBA_BNB_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 22831),  # v1.3.0
    ],
    EthereumNetwork.BOBA_AVAX: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 55739),  # v1.3.0
    ],
    EthereumNetwork.BOBA_NETWORK: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 170895),  # v1.3.0
    ],
    EthereumNetwork.AURORA_MAINNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            111687685,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            52494463,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.METIS_STARDUST_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 56117),  # v1.3.0
    ],
    EthereumNetwork.METIS_GOERLI_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 131842),  # v1.3.0
    ],
    EthereumNetwork.METIS_ANDROMEDA_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 61758),  # v1.3.0
    ],
    EthereumNetwork.SHYFT_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2000),  # v1.3.0
    ],
    EthereumNetwork.SHYFT_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1984340),  # v1.3.0
    ],
    EthereumNetwork.REI_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2387999),  # v1.3.0
    ],
    EthereumNetwork.METER_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 23863720),  # v1.3.0
    ],
    EthereumNetwork.METER_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 15035363),  # v1.3.0
    ],
    EthereumNetwork.EURUS_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 7127155),  # v1.3.0
    ],
    EthereumNetwork.EURUS_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12845425),  # v1.3.0
    ],
    EthereumNetwork.VENIDIUM_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1127130),  # v1.3.0
    ],
    EthereumNetwork.VENIDIUM_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 761231),  # v1.3.0
    ],
    EthereumNetwork.GODWOKEN_TESTNET_V1: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 93108),  # v1.3.0
    ],
    EthereumNetwork.KLAYTN_TESTNET_BAOBAB: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 93821613),  # v1.3.0
    ],
    EthereumNetwork.KLAYTN_MAINNET_CYPRESS: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 93506870),  # v1.3.0
    ],
    EthereumNetwork.MILKOMEDA_A1_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 789),  # v1.3.0
    ],
    EthereumNetwork.MILKOMEDA_A1_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 6218),  # v1.3.0
    ],
    EthereumNetwork.MILKOMEDA_C1_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 5080303),  # v1.3.0
    ],
    EthereumNetwork.MILKOMEDA_C1_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4896699),  # v1.3.0
    ],
    EthereumNetwork.CRONOS_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 3290819),  # v1.3.0
    ],
    EthereumNetwork.CRONOS_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2958469),  # v1.3.0
    ],
    EthereumNetwork.RABBIT_ANALOG_TESTNET_CHAIN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1434222),  # v1.3.0
    ],
    EthereumNetwork.CLOUDWALK_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 13743040),  # v1.3.0
    ],
    EthereumNetwork.KCC_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4860798),  # v1.3.0
    ],
    EthereumNetwork.KCC_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12147567),  # v1.3.0
    ],
    EthereumNetwork.PUBLICMINT_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 19974979),  # v1.3.0
    ],
    EthereumNetwork.PUBLICMINT_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 14062193),  # v1.3.0
    ],
    EthereumNetwork.XDC_APOTHEM_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 42293264),  # v1.3.0
    ],
    EthereumNetwork.BASE: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            595181,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            2156359,
        ),  # v1.3.0 default singleton address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3024579),  # v1.4.1
    ],
    EthereumNetwork.BASE_GOERLI_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7330598),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 938696),  # v1.3.0
    ],
    EthereumNetwork.BASE_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 3282032),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5125191),  # v1.3.0
    ],
    EthereumNetwork.KAVA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2116356),  # v1.3.0
    ],
    EthereumNetwork.CROSSBELL: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 28314747),  # v1.3.0
    ],
    EthereumNetwork.IOTEX_NETWORK_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 22172504),  # v1.3.0
    ],
    EthereumNetwork.HARMONY_MAINNET_SHARD_0: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 22502012),  # v1.3.0
        ("0x4f9b1dEf3a0f6747bF8C870a27D3DeCdf029100e", 11526678),
    ],
    EthereumNetwork.HARMONY_TESTNET_SHARD_0: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4824437),  # v1.3.0
    ],
    EthereumNetwork.VELAS_EVM_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 27571962),  # v1.3.0
    ],
    EthereumNetwork.WEMIX3_0_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 12651730),  # v1.3.0
    ],
    EthereumNetwork.WEMIX3_0_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 20833988),  # v1.3.0
    ],
    EthereumNetwork.EVMOS_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 70637),  # v1.3.0
    ],
    EthereumNetwork.EVMOS: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 146858),  # v1.3.0
    ],
    EthereumNetwork.MAP_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 5190546),  # v1.3.0
    ],
    EthereumNetwork.MAP_MAKALU: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2987578),  # v1.3.0
    ],
    EthereumNetwork.ETHEREUM_CLASSIC: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 15904946),  # v1.3.0
    ],
    EthereumNetwork.MORDOR_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 6333172),  # v1.3.0
    ],
    EthereumNetwork.SEPOLIA: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3312223),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            2087031,
        ),  # v1.3.0  Safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            2086864,
        ),  # v1.3.0  Default singleton address
    ],
    EthereumNetwork.TENET_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 885379),  # v1.3.0
    ],
    EthereumNetwork.TENET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 727457),  # v1.3.0
    ],
    EthereumNetwork.LINEA_TESTNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            3279584,
        ),  # v1.3.0  Safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            363118,
        ),  # v1.3.0  Default singleton address
    ],
    EthereumNetwork.ASTAR: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1106417),  # v1.3.0
    ],
    EthereumNetwork.SHIDEN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1634935),  # v1.3.0
    ],
    EthereumNetwork.DARWINIA_NETWORK: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            491157,
        )
    ],
    EthereumNetwork.CRAB_NETWORK: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            739882,
        )
    ],
    EthereumNetwork.ZORA: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            9677950,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            11914,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.ZKSYNC_MAINNET: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 7259190),  # v1.3.0
    ],
    EthereumNetwork.MANTLE_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4404053),  # v1.3.0
    ],
    EthereumNetwork.MANTLE: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1504),  # v1.3.0
    ],
    EthereumNetwork.CASCADIA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1408580),  # v1.3.0
    ],
    EthereumNetwork.OASIS_SAPPHIRE_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1378137),  # v1.3.0
    ],
    EthereumNetwork.OASIS_SAPPHIRE: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 325632),  # v1.3.0
    ],
    EthereumNetwork.EDGEWARE_EDGEEVM_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 18176812),  # v1.3.0
    ],
    EthereumNetwork.LINEA: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            1939855,
        ),  # v1.3.0  Safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            10,
        ),  # v1.3.0  Default singleton address
    ],
    EthereumNetwork.NEON_EVM_DEVNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 205146874),  # v1.3.0
    ],
    EthereumNetwork.NEON_EVM_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 203993869),  # v1.3.0
    ],
    EthereumNetwork.SCROLL_SEPOLIA_TESTNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            2913883,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            6254,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.FANTOM_OPERA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 38810826),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 21817221),  # v1.3.0
    ],
    EthereumNetwork.FANTOM_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4627348),  # v1.3.0
        ("0x63B5caf390e8AF7133DBE6bA92A69167a854Ac91", 4627348),  # v1.3.0
    ],
    EthereumNetwork.ROOTSTOCK_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 3891234),  # v1.3.0
    ],
    EthereumNetwork.ROOTSTOCK_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2362232),  # v1.3.0
    ],
    EthereumNetwork.BEAM: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 27621),  # v1.3.0
    ],
    EthereumNetwork.BEAM_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 85318),  # v1.3.0
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 7709119),  # v1.3.0
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1315556),  # v1.3.0
    ],
    EthereumNetwork.ZETACHAIN_ATHENS_3_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1962972),  # v1.3.0
    ],
    EthereumNetwork.SCROLL: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            2905472,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            179,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.TELOS_EVM_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 237435678),  # v1.3.0
    ],
    EthereumNetwork.TELOS_EVM_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 194005709),  # v1.3.0
    ],
    EthereumNetwork.PGN_PUBLIC_GOODS_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 344314),  # v1.3.0
    ],
    EthereumNetwork.SEPOLIA_PGN_PUBLIC_GOODS_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1774097),  # v1.3.0
    ],
    EthereumNetwork.ARTHERA_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5552),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5542),  # v1.3.0
    ],
    EthereumNetwork.ARTHERA_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 4186337),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 119959),  # v1.3.0
    ],
    EthereumNetwork.MANTA_PACIFIC_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 338464),  # v1.3.0
    ],
    EthereumNetwork.KROMA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5281925),  # v1.3.0
    ],
    EthereumNetwork.KROMA_SEPOLIA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 7867188),  # v1.3.0
    ],
    EthereumNetwork.HAQQ_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 9054785),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 422239),  # v1.3.0
    ],
    EthereumNetwork.HAQQ_CHAIN_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7031865),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1514954),  # v1.3.0
    ],
    EthereumNetwork.MODE: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2610484),  # v1.3.0
    ],
    EthereumNetwork.MODE_TESTNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            9375436,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            1948140,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.ZORA_SEPOLIA_TESTNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            4265398,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            46699,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.MANTLE_SEPOLIA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1927649),  # v1.3.0
    ],
    EthereumNetwork.OP_SEPOLIA_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7162843),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            7438194,
        ),  # v1.3.0  Safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            4357263,
        ),  # v1.3.0  Default singleton address
    ],
    EthereumNetwork.UNREAL_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 735),  # v1.3.0
    ],
    EthereumNetwork.TAIKO_KATLA_L2: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 44820),  # v1.3.0
    ],
    EthereumNetwork.BERACHAIN_ARTIO: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 379659),  # v1.3.0
    ],
    EthereumNetwork.SEI_DEVNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4552166),  # v1.3.0
    ],
    EthereumNetwork.LISK_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 657735),  # v1.3.0
    ],
    EthereumNetwork.BOTANIX_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 165422),  # v1.4.1
    ],
    EthereumNetwork.BLAST_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1087898),  # v1.3.0
    ],
    EthereumNetwork.REYA_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 77),  # v1.3.0
    ],
    EthereumNetwork.FRAXTAL_MAINNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            0,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            1675084,
        ),  # v1.3.0 default singleton address
    ],
    EthereumNetwork.AURORIA_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 186758),  # v1.4.1
    ],
    EthereumNetwork.STRATIS_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 106940),  # v1.4.1
    ],
    EthereumNetwork.SHIMMEREVM: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 155079),  # v1.3.0
    ],
    EthereumNetwork.IOTA_EVM: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 13212),  # v1.3.0
    ],
    EthereumNetwork.BITROCK_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 12949157),  # v1.4.1
    ],
    EthereumNetwork.BITROCK_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 13177748),  # v1.4.1
    ],
    EthereumNetwork.XDC_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 53901564),  # v1.3.0
    ],
    EthereumNetwork.OP_CELESTIA_RASPBERRY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1028156),  # v1.3.0
    ],
    EthereumNetwork.POLYGON_BLACKBERRY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 765141),  # v1.3.0
    ],
    EthereumNetwork.ARBITRUM_BLUEBERRY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 19364),  # v1.3.0
    ],
    EthereumNetwork.X_LAYER_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 359536),  # v1.3.0
    ],
    EthereumNetwork.PULSECHAIN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12504126),  # v1.3.0
    ],
    EthereumNetwork.PULSECHAIN_TESTNET_V4: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12504126),  # v1.3.0
    ],
    EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2297578),  # v1.3.0
    ],
    EthereumNetwork.RSS3_VSL_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1699348),  # v1.3.0
    ],
    EthereumNetwork.CROSSFI_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2322620),  # v1.3.0
    ],
}
