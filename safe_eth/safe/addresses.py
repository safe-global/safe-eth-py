"""
Contains information about Safe contract addresses deployed in every chain

Every entry contains a tuple with address, deployment block number and version
"""
from typing import Dict, List, Tuple, Union

from eth_typing import ChecksumAddress, HexAddress, HexStr

from safe_eth.eth import EthereumNetwork
from safe_eth.eth.utils import fast_to_checksum_address
from safe_eth.safe.safe_deployments import default_safe_deployments

SAFE_SIMULATE_TX_ACCESSOR_ADDRESS: ChecksumAddress = ChecksumAddress(
    HexAddress(HexStr("0x3d4BA2E0884aa488718476ca2FB8Efc291A46199"))
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
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            34516629,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 63352908, "1.3.0"),  # v1.3.0
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6702420, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            8792328,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            88610931,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 266489799, "1.3.0"),  # v1.3.0
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 144832221, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            163904906,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            8944350,
            "1.3.0+L2",
        ),  # 1.3.0+L2 safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            23700081,
            "1.3.0+L2",
        ),  # 1.3.0+L2 default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            8944351,
            "1.3.0",
        ),  # 1.3.0 safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            23700082,
            "1.3.0",
        ),  # 1.3.0 default singleton address
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 23116909, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            23116907,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 37031334, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            43431152,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.MOONBEAM: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 172_092, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 172_094, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6277734, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6277732,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.MOONRIVER: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 707_738, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 707_741, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6876735, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6876733,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.MOONBASE_ALPHA: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 939_244, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 939_246, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7269447, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7269444,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 111449608, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            113995630,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 22304927, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 22304923, "1.3.0+L2"),  # v1.3.0+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 121013988, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            121013976,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
    EthereumNetwork.KAIA_KAIROS_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 93821635, "1.3.0+L2"),
    ],
    EthereumNetwork.KAIA_MAINNET: [
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 22052462, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            22052454,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.CRONOS_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 3002268, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 3002760, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14208726, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14208724,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5854670, "1.4.1"),  # v1.4.1
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5172602, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5172599,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.KAVA: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2116303, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2116307, "1.3.0"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 10266347, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            10266344,
            "1.3.0+L2",
        ),  # v1.3.0+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 58258063, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            58258060,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.HARMONY_TESTNET_SHARD_0: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 4824474, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4824480, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 27807657, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            27807654,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.VELAS_EVM_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 27572492, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 27572642, "1.3.0"),
    ],
    EthereumNetwork.WEMIX3_0_MAINNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 12651754, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 12651757, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 51018381, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            51018375,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.WEMIX3_0_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 20834033, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 20834039, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 59201415, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            59201405,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.EVMOS_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 70652, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 70654, "1.3.0"),
    ],
    EthereumNetwork.EVMOS: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 158463, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 158486, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 21226508, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            21226507,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.MAP_PROTOCOL: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 5190553, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 5190556, "1.3.0"),
    ],
    EthereumNetwork.MAPO_MAKALU: [
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 9527798, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            9527796,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.TENET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 727470, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 727472, "1.3.0"),
    ],
    EthereumNetwork.LINEA_GOERLI: [
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2807831, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2807830,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ASTAR: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1106426, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1106429, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6524141, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6524130,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.SHIDEN: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1634935, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1634935, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6642417, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6642415,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 13511109, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            15254528,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ZKSYNC_MAINNET: [
        (
            "0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910",
            7259230,
            "1.3.0",
        ),  # v1.3.0 zksync
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            60386563,
            "1.3.0",
        ),  # v1.3.0 canonical
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            60386404,
            "1.3.0",
        ),  # v1.3.0 eip155
        (
            "0x1727c2c531cf966f902E5927b98490fDFb3b2b70",
            7259224,
            "1.3.0+L2",
        ),  # v1.3.0+L2 zksync
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            60386561,
            "1.3.0+L2",
        ),  # v1.3.0+L2 canonical
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            60386402,
            "1.3.0+L2",
        ),  # v1.3.0+L2 eip155
        (
            "0xC35F063962328aC65cED5D4c3fC5dEf8dec68dFa",
            57957670,
            "1.4.1",
        ),  # v1.4.1 zksync
        (
            "0x41675C099F32341bf84BFc5382aF534df5C7461a",
            60385701,
            "1.4.1",
        ),  # v1.4.1 canonical
        (
            "0x610fcA2e0279Fa1F8C00c8c2F71dF522AD469380",
            57957674,
            "1.4.1+L2",
        ),  # v1.4.1+L2 zksync
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            60385703,
            "1.4.1+L2",
        ),  # v1.4.1+L2 canonical
    ],
    EthereumNetwork.MANTLE_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 4404246, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4404284, "1.3.0"),
    ],
    EthereumNetwork.MANTLE: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1511,
            "1.3.0+L2",
        ),  # 1.3.0+L2 safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            5292901,
            "1.3.0+L2",
        ),  # 1.3.0+L2 default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            1512,
            "1.3.0",
        ),  # 1.3.0 safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            5292915,
            "1.3.0",
        ),  # 1.3.0 default singleton address
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 57306677, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            57306670,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.CASCADIA_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1408599, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1408613, "1.3.0"),
    ],
    EthereumNetwork.OASIS_SAPPHIRE: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 325640, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 325643, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3960886, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            3960884,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 9390428, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            9390426,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.OASIS_SAPPHIRE_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1378154, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1378155, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6538875, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6538873,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12222616, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12222613,
            "1.3.0+L2",
        ),  # v1.3.0+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1583051, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1583049,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3925363, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            4422667,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7733239, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6394544,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ROOTSTOCK_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 2362236, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2362238, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5178634, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5178632,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 13877078, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            13877076,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1315570, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1315572, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7483164, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7483162,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ZETACHAIN_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1962980, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1962981, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5221017, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5221016,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5007158, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6500570,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.TELOS_EVM_MAINNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 237435759, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 237435774, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 344576238, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            344576227,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.TELOS_EVM_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 194005796, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 194005824, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 301047807, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            301047793,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2303585, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2303584,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.KROMA: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 5281960, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5281965, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 11658189, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            11658184,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.KROMA_SEPOLIA: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 7992402, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 7992408, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14243945, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14243941,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6524841, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6524836,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 7457757, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            7457753,
            "1.3.0+L2",
        ),  # v1.3.0+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 12924063, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14667422,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6688248, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6688128,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.MANTLE_SEPOLIA_TESTNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 1927686, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1927692, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7826403, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7826399,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
    EthereumNetwork.UNREAL_OLD: [
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1560002, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1559997,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.SEI_DEVNET: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 4552451, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4552489, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 24838672, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            24838667,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.LISK_SEPOLIA_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 657757, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 657761, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5944845, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5944842,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BOTANIX_TESTNET: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 165429, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 165430, "1.4.1"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1368811, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1368813,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1368719, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1368717,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.BLAST_SEPOLIA_TESTNET: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1087958, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1087964, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 4514678, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6253521,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.REYA_NETWORK: [
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 84, "1.3.0+L2"),
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 85, "1.3.0"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2172963, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2172961,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.FRAXTAL: [
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3452673, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5195803,
            "1.4.1+L2",
        ),  # v1.4.1+L2
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
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 92581199, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            92581197,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 87195101, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            92581726,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.OP_CELESTIA_RASPBERRY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1028180, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1028176,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 6038449, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            6038440,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7101215, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7101212,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.POLYGON_BLACKBERRY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 765162, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 765158, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1194318, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1194313,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1725506, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1725503,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ARBITRUM_BLUEBERRY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 19373, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 19372, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 42035, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 42034, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 281865, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 281864, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.X_LAYER_MAINNET: [
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            359517,
            "1.3.0",
        ),  # v1.3.0 safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            71844,
            "1.3.0",
        ),  # v1.3.0 default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            359442,
            "1.3.0+L2",
        ),  # v1.3.0+L2 safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            100691,
            "1.3.0+L2",
        ),  # v1.3.0+L2 default singleton address
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3752736, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            3752752,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.PULSECHAIN: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 18804226, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            18804223,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12504423,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10329734, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 9084503, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 8915728, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 7457553, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 6766257, "0.1.0"),
        ("0xAC6072986E985aaBE7804695EC2d8970Cf7541A2", 6569433, "0.0.2"),
    ],
    EthereumNetwork.PULSECHAIN_TESTNET_V4: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12504423,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10329734, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 9084503, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 8915728, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 7457553, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 6766257, "0.1.0"),
        ("0xAC6072986E985aaBE7804695EC2d8970Cf7541A2", 6569433, "0.0.2"),
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
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3481865, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            3481851,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BLAST: [
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 377556, "1.4.1+L2"),
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 377716, "1.4.1"),
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            257369,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            132449,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            257372,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            132456,
            "1.3.0",
        ),  # default singleton address
    ],
    EthereumNetwork.ASTAR_ZKYOTO: [
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            914726,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1026758,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            914732,
            "1.3.0",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            1026763,
            "1.3.0",
        ),  # safe singleton address
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2841029, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2841024,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.SAAKURU_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 26744133, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            26744132,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 30517766, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            30517763,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.REDSTONE: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 930078, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 930071, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2533129, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2533126,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.GARNET_HOLESKY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 937241, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 937238, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2540794, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2540791,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ENDURANCE_SMART_CHAIN_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 462220, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 462219, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 461979, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 461978, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.MORPH_HOLESKY: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 260126, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 260124, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1171434, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1171430,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12482468, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            12482460,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.CYBER_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1098959, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1098954,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1886363, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1886361,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.CYBER_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 515925, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 515924, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 324597, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 673157, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.LISK: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 139956, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 139953, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1236905, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1236895,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.TAIKO_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 10710, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 10708, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 7377, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 7376, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 19221, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 19220, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.TAIKO_HEKLA_L2: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 158860, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 158815, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 253322, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 253199, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 276588, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 276587, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.AMOY: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6006133, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6006129,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ASTAR_ZKEVM: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2802306, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2802301,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.HOLESKY: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 100429, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 100427, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.RE_AL: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 81988, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 81987, "1.4.1+L2"),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 22, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 21, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.UNREAL: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 61547, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 61546, "1.4.1+L2"),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1777, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1776, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.SEI_NETWORK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 80547079, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            80547067,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ZETACHAIN_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3315631, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            3315630,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.LINEA_SEPOLIA: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1305454, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1305452,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ZILLIQA_EVM: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3831182, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            3831180,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ZILLIQA_EVM_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6965149, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6965147,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ZIRCUIT_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 9199719, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            9199713,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 22760836, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            22760831,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 16922951, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            16922955,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.LORENZO: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 303716, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 303709, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.F_XCORE_TESTNET_NETWORK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14854853, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14854852,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.F_XCORE_MAINNET_NETWORK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 16088827, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            16088826,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.DODOCHAIN_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1649, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 1648, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.ETHERLINK_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 994183, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 994181, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.ETHERLINK_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 3826171, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            3826169,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.KAVA_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 11835211, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            11835209,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14909879, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14909880,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BERACHAIN_BARTIO: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 100431, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 100426, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.WORLD_CHAIN: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 257924, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 257920, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 257516, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 257513, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.ABEY_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 20551597, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            20551593,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.FLARE_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 27375871, "1.3.0"),  # v1.3.0
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 27619321, "1.4.1"),  # v1.4.1
    ],
    EthereumNetwork.GNOSIS_CHIADO_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 117845, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 117838, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.SONGBIRD_CANARY_NETWORK: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 36564936, "1.3.0"),  # v1.3.0
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 66811156, "1.4.1"),  # v1.4.1
    ],
    EthereumNetwork.SONGBIRD_TESTNET_COSTON: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 9254177, "1.3.0"),  # v1.3.0
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 19263461, "1.4.1"),  # v1.4.1
    ],
    EthereumNetwork.FLARE_TESTNET_COSTON2: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 3541, "1.3.0"),  # v1.3.0
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 10423623, "1.4.1"),  # v1.4.1
    ],
    EthereumNetwork.NAL_SEPOLIA_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2074612, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            2074608,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.ALEPH_ZERO_EVM: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 130, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 129, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 943007, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 942991, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 944503, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 944478, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.IRISHUB: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 25909146, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            25909145,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.NAL_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1777700, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1777694,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.CRONOS_ZKEVM_TESTNET: [
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 163814, "1.3.0"),  # v1.3.0
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 163812, "1.3.0+L2"),  # v1.3.0+L2
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 19013, "1.3.0"),  # v1.3.0
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 19012, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.CRONOS_ZKEVM_MAINNET: [
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 6105, "1.3.0"),  # v1.3.0
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 6104, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.SKOPJE_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2845182, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2845179,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2972545, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            2972541,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.GPT_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1358329, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1358326,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1448591, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1448589,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.BEVM_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1651910, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1651908,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BEVM_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1571646, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1571644,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.NAHMII_3_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 724, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 723, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.ZIRCUIT_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1498633, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1498628,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 12993066, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            12994083,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BOB_SEPOLIA: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.SNAXCHAIN: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 388477, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 388470, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 388643, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 388638, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.Q_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 15479491, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            15479490,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 15650874, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            15650873,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.Q_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14783676, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14783675,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 14907815, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            14907814,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.SHAPE_SEPOLIA_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 15845870, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            15845866,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7703644, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7703648,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.SHAPE: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 14353553, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            14353548,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6299328, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6299333,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.VANA_MOKSHA_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 49109, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 49107, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 652256, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 652259, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.CONNEXT_SEPOLIA: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 6526, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 6525, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.EVERCLEAR_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 13152, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 13151, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.BAHAMUT: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 3007545, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            3007543,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.OORT_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 29277886, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            29277936,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.GAME7_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 154980, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 154977, "1.4.1+L2"),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 216550, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 216546, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 154906, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 154905, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.GAME7: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 76, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 75, "1.4.1+L2"),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 56, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 55, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 66, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 65, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.MORPH: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 177483, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 177481, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 177679, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 177708, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.OORT_MAINNETDEV: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 304563, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 304588, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.INK_SEPOLIA: [
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),
    ],
    EthereumNetwork.STORY_ODYSSEY_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 340803, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 340800, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 340907, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 340904, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.SWELLCHAIN_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 836957, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 836953, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 836417, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 836412, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.FILECOIN_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 4155380, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            4155378,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4541183, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            4541180,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.FILECOIN_CALIBRATION_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1854685, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1839902,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2241199, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2241195,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.NAHMII_3_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 13895, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 13894, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.PLUME_DEVNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5167643, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5167648,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.PLUME_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 52581, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 52582, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.SWELLCHAIN: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 261408, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 261401, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 261807, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 261813, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.HASHKEY_CHAIN_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4795480, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4795470,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 4795005, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            4794997,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.SONIC_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 107741, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 107743, "1.4.1+L2"),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 95, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 93, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5780860, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            5728153,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.WATERFALL_9_TEST_NETWORK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7329851, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7329879,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.WATERFALL_NETWORK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2517926, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2517940,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.INK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 455060, "1.4.1"),
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 455065, "1.4.1+L2"),
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 454704, "1.3.0"),  # 1.3.0 eip155
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            454704,
            "1.3.0",
        ),  # 1.3.0 canonical
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            454704,
            "1.3.0+L2",
        ),  # 1.3.0+L2 eip155
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            454704,
            "1.3.0+L2",
        ),  # 1.3.0+L2 canonical
    ],
    EthereumNetwork.SONIC_BLAZE_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 7541, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 7535, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 12484041, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            11777878,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.EXSAT_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7691657, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7691662,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.HASHKEY_CHAIN: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 127779, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 127784, "1.4.1+L2"),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 128075, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 128069, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.EXSAT_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7687809, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7687815,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.UNICHAIN: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7393772, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7393779,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            7394646,
            "1.3.0",
        ),  # v1.3.0 canonical
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            7394633,
            "1.3.0+L2",
        ),  # v1.3.0+L2 canonical
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 7394633, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            7394633,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.BERACHAIN: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 40883, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            40887,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            41420,
            "1.3.0",
        ),  # v1.3.0 canonical
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            41416,
            "1.3.0+L2",
        ),  # v1.3.0+L2 canonical
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 45842, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            45838,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.EVM_ON_FLOW: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 3042677, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            3042653,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 10722596, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            10722613,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.EVM_ON_FLOW_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2346918, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2346892,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 20813606, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            20813625,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BIRDLAYER: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 242, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 241, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.ABSTRACT: [
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 57876, "1.3.0"),  # v1.3.0
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 57875, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.ABSTRACT_SEPOLIA_TESTNET: [
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 2207773, "1.3.0"),  # v1.3.0
        (
            "0x1727c2c531cf966f902E5927b98490fDFb3b2b70",
            2207769,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.OKTO_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5693701, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5693713,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.STORY: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 542735, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 542731, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 621448, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 621444, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 621109, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 621114, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.NIBIRU_CATACLYSM_1: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 21722399, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            21722389,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 19868217, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            19868594,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 19869113, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            19869158,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.NIBIRU_TESTNET_2: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1126361, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1126358,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 675154, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 675137, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 674987, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 674995, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.TAC_TURIN: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2491842, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2491840,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2231705, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2231707,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ALEPH_ZERO: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 204, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 203, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 676, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 675, "1.4.1+L2"),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5639039, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            5639037,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.ETHEREUM_HOODI: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 20182, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 20175, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 20136, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 20134, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 20211, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 20212, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.KATANA_MAINNET: [
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            318968,
            "1.3.0+L2",
        ),  # safe singleton address
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            318968,
            "1.3.0+L2",
        ),  # default singleton address
        (
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            318968,
            "1.3.0",
        ),  # safe singleton address
        (
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            318968,
            "1.3.0",
        ),  # default singleton address
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 318968, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            318968,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.AUTONOMYS_TAURUS_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1196806, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1196805,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 416926, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 416924, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.STORY_AENEID_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 973663, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 974369, "1.4.1+L2"),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2462519, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2462515,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4945905, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4945901,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.AUTONITY_PICCADILLY_TIBER_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14677654, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14677658,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BOBA_SEPOLIA: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 8927245, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            8926694,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 21674916, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            21674910,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 14069986, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            14069990,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BERACHAIN_BEPOLIA: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2068001, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2068009,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2070087, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2070069,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1440054, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1440051,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.SONEIUM_TESTNET_MINATO: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1835127, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1835122,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 3900870, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            3900875,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.IMMUTABLE_ZKEVM: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 1602100, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            1602095,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 23354731, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            23354725,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 18849270, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            18849274,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.IMMUTABLE_ZKEVM_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 3244337, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            3244331,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 19363850, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            19363854,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 24995980, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            24995976,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.PYROPE_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 382699, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 629391, "1.4.1+L2"),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 3752652, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            3752648,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.PLATON_DEV_TESTNET2: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 85388213, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            85388217,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.PLATON_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 121386519, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            121386523,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ARENA_Z: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1528719, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            8199827,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 8196632, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            8196628,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            0,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.PEAQ: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 1365390, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            1365388,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 5688273, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            5688273,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1315238, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1315236,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.BOTANIX_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 235980, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 235983, "1.4.1+L2"),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 235718, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 235717, "1.3.0+L2"),  # v1.3.0+L2
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 529880, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 529882, "1.3.0"),  # v1.3.0
    ],
    EthereumNetwork.TAC_SAINT_PETERSBURG: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 2049675, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            2049670,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 2049549, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            2049545,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2049465, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2049467,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.TAC_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 18286, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 18283, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 18477, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 18474, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 18001, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 18003, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.SOPHON: [
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 114, "1.3.0"),  # v1.3.0
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 113, "1.3.0+L2"),  # v1.3.0+L2
        ("0xC35F063962328aC65cED5D4c3fC5dEf8dec68dFa", 128, "1.4.1"),  # v1.4.1
        ("0x610fcA2e0279Fa1F8C00c8c2F71dF522AD469380", 129, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.SOPHON_TESTNET: [
        ("0xC35F063962328aC65cED5D4c3fC5dEf8dec68dFa", 75651, "1.4.1"),  # v1.4.1
        ("0x610fcA2e0279Fa1F8C00c8c2F71dF522AD469380", 75652, "1.4.1+L2"),  # v1.4.1+L2
        ("0xB00ce5CCcdEf57e539ddcEd01DF43a13855d9910", 13509, "1.3.0"),  # v1.3.0
        ("0x1727c2c531cf966f902E5927b98490fDFb3b2b70", 13508, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.PLASMA_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 517714, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 517707, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 519224, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 519218, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 521786, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 521790, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.CODEX_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 11533343, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            11533339,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 11535157, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            11535159,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.METAL_L2: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 20205345, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            20205342,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.MONAD_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 11644083, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            11644096,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 11644969, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            11644962,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 11648273, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            11648260,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.ETHEREAL_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 224358, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 224357, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 225459, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 225457, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 225492, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 225493, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.OPBNB_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4641098, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4641092,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 13660300, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            13660289,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 21962333, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            24176116,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.POLYNOMIAL: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 18563390, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            18563394,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.ENI_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 6360950, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            6360954,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.VANA: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4515256, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4515254,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 625365, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 625361, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 625823, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 625825, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.ZIRCUIT_GARFIELD_TESTNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 6165739, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            6165735,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 5814318, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            5814325,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            0,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.PHAROS_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 18710950, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            18710892,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 18712474, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            18712497,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.PLASMA_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 64431, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 64428, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 63827, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 63824, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 0, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 0, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.LENS: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 4250424, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            4250422,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4250534, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            4250530,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1724225, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1724229,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.PAIX_DEVELOPMENT_NETWORK: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 179038, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 179037, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork._0G_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 4923822, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            4923855,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 3649778, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            3649629,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 4899977, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            4899944,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.INCENTIV_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 375424, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 375423, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 381980, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 381983, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.AUTONOMYS_CHRONOS_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 119160, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 119158, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 119202, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 119200, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 119222, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 119224, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.BOB: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 200509, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 200503, "1.3.0+L2"),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 427036, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            13768019,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.CROSSFI_MAINNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 680500, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 680498, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 680898, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 680900, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.CITREA_TESTNET: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 665299, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 665297, "1.3.0+L2"),  # v1.3.0+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 665116, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 665112, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 1793093, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            1793096,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.MINT_MAINNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 7688631, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            7688635,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 0, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 0, "1.3.0+L2"),  # v1.3.0+L2
    ],
    EthereumNetwork.SEI_TESTNET: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 188493719, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            188493725,
            "1.4.1+L2",
        ),  # v1.4.1+L2
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 188493237, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            188493226,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 188492836, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            188492825,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.INCENTIV: [
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 223237, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 223236, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 223817, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 223819, "1.4.1+L2"),  # v1.4.1+L2
    ],
    EthereumNetwork.SAGA: [
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 2031967, "1.4.1"),  # v1.4.1
        (
            "0x29fcB43b46531BcA003ddC8FCB67FFE91900C762",
            2031969,
            "1.4.1+L2",
        ),  # v1.4.1+L2
    ],
    EthereumNetwork.GRAVITY_ALPHA_MAINNET: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 98991875, "1.3.0"),  # v1.3.0
        (
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            98991862,
            "1.3.0+L2",
        ),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 96, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 95, "1.4.1+L2"),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 66231348, "1.3.0"),  # v1.3.0
        (
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
            66231340,
            "1.3.0+L2",
        ),  # v1.3.0+L2
    ],
    EthereumNetwork.GRAVITY_ALPHA_TESTNET_SEPOLIA: [
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 10827, "1.3.0"),  # v1.3.0
        ("0x3E5c63644E683549055b9Be8653de26E0B4CD36E", 10826, "1.3.0+L2"),  # v1.3.0+L2
        ("0x41675C099F32341bf84BFc5382aF534df5C7461a", 433, "1.4.1"),  # v1.4.1
        ("0x29fcB43b46531BcA003ddC8FCB67FFE91900C762", 434, "1.4.1+L2"),  # v1.4.1+L2
        ("0x69f4D1788e39c87893C980c06EdF4b7f686e2938", 510, "1.3.0"),  # v1.3.0
        ("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA", 509, "1.3.0+L2"),  # v1.3.0+L2
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6702792),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 99258141),  # v1.4.1
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
        ),  # v1.3.0 safe proxy factory address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            8485873,
        ),  # v1.3.0 default proxy factory address
    ],
    EthereumNetwork.CELO_MAINNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            8944342,
        ),  # v1.3.0 safe proxy factory address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            23700074,
        ),  # v1.3.0 default proxy factory address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 23116898),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 37031436),  # v1.4.1
    ],
    EthereumNetwork.MOONBEAM: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 172078),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6277718),  # v1.4.1
    ],
    EthereumNetwork.MOONRIVER: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 707_721),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6876719),  # v1.4.1
    ],
    EthereumNetwork.MOONBASE_ALPHA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 939_239),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7269421),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 105342078),  # v1.4.1
    ],
    EthereumNetwork.BOBA_BNB_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 22831),  # v1.3.0
    ],
    EthereumNetwork.BOBA_AVAX: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 55739),  # v1.3.0
    ],
    EthereumNetwork.BOBA_NETWORK: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 170895),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 22304897), # v1.3.0
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 121013905),  # v1.4.1
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
    EthereumNetwork.KAIA_KAIROS_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 93821613),  # v1.3.0
    ],
    EthereumNetwork.KAIA_MAINNET: [
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 22049385),  # v1.4.1
    ],
    EthereumNetwork.CRONOS_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2958469),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14208753),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5172579),  # v1.4.1
    ],
    EthereumNetwork.KAVA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2116356),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 10266328),  # v1.3.0
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 58258043),  # v1.4.1
    ],
    EthereumNetwork.HARMONY_TESTNET_SHARD_0: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4824437),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 27807637),  # v1.4.1
    ],
    EthereumNetwork.VELAS_EVM_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 27571962),  # v1.3.0
    ],
    EthereumNetwork.WEMIX3_0_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 12651730),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 51018344),  # v1.4.1
    ],
    EthereumNetwork.WEMIX3_0_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 20833988),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 20758876),  # v1.4.1
    ],
    EthereumNetwork.EVMOS_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 70637),  # v1.3.0
    ],
    EthereumNetwork.EVMOS: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 146858),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 21226499),  # v1.4.1
    ],
    EthereumNetwork.MAP_PROTOCOL: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 5190546),  # v1.3.0
    ],
    EthereumNetwork.MAPO_MAKALU: [
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 9527674),  # v1.4.1
    ],
    EthereumNetwork.TENET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 727457),  # v1.3.0
    ],
    EthereumNetwork.LINEA_GOERLI: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            3279584,
        ),  # v1.3.0  Safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            363118,
        ),  # v1.3.0  Default singleton address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2807823),  # v1.4.1
    ],
    EthereumNetwork.ASTAR: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1106417),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6308759),  # v1.4.1
    ],
    EthereumNetwork.SHIDEN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1634935),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6642401),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 13511105),  # v1.4.1
    ],
    EthereumNetwork.ZKSYNC_MAINNET: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 7259190),  # v1.3.0 zksync
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 60386545),  # v1.3.0 canonical
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 60386388),  # v1.3.0 eip155
        ("0xc329D02fd8CB2fc13aa919005aF46320794a8629", 57957636),  # v1.4.1 zksync
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 60385637),  # v1.4.1 canonical
    ],
    EthereumNetwork.MANTLE_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4404053),  # v1.3.0
    ],
    EthereumNetwork.MANTLE: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            1504,
        ),  # v1.3.0 safe proxy factory address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            5292797,
        ),  # v1.3.0 default proxy factory address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 57306582),  # v1.4.1
    ],
    EthereumNetwork.CASCADIA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1408580),  # v1.3.0
    ],
    EthereumNetwork.OASIS_SAPPHIRE_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1378137),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6538856),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12222596),  # v1.3.0
    ],
    EthereumNetwork.OASIS_SAPPHIRE: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 325632),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3960870),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 9390409),  # v1.3.0
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1582959),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3925361),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6394526),  # v1.4.1
    ],
    EthereumNetwork.ROOTSTOCK_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2362232),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5178608),  # v1.4.1
    ],
    EthereumNetwork.BEAM: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 27621),  # v1.3.0
    ],
    EthereumNetwork.BEAM_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 85318),  # v1.3.0
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 7709119),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 13877066),  # v1.4.1
    ],
    EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1315556),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7483149),  # v1.4.1
    ],
    EthereumNetwork.ZETACHAIN_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1962972),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5221009),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5007155),  # v1.4.1
    ],
    EthereumNetwork.TELOS_EVM_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 237435678),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 344576179),  # v1.4.1
    ],
    EthereumNetwork.TELOS_EVM_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 194005709),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 301047704),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2303577),  # v1.4.1
    ],
    EthereumNetwork.KROMA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5281925),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 11658156),  # v1.4.1
    ],
    EthereumNetwork.KROMA_SEPOLIA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 7867188),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14243918),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6524805),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 7457728),  # v1.3.0
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 12924059),  # v1.4.1
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
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6688269),  # v1.4.1
    ],
    EthereumNetwork.MANTLE_SEPOLIA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1927649),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7826372),  # v1.4.1
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
    EthereumNetwork.UNREAL_OLD: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 735),  # v1.3.0
    ],
    EthereumNetwork.TAIKO_KATLA_L2: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 44820),  # v1.3.0
    ],
    EthereumNetwork.BERACHAIN_ARTIO: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 379659),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1559673),  # v1.4.1
    ],
    EthereumNetwork.SEI_DEVNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4552166),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 24838616),  # v1.4.1
    ],
    EthereumNetwork.LISK_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 657735),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5944825),  # v1.4.1
    ],
    EthereumNetwork.BOTANIX_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 165422),  # v1.4.1
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1368795),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1368703),  # v1.3.0
    ],
    EthereumNetwork.BLAST_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1087898),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 4514675),  # v1.4.1
    ],
    EthereumNetwork.REYA_NETWORK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 77),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2172952),  # v1.4.1
    ],
    EthereumNetwork.FRAXTAL: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            0,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            1675084,
        ),  # v1.3.0 default singleton address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3452668),  # v1.4.1
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
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 92581183),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 92581713),  # v1.4.1
    ],
    EthereumNetwork.OP_CELESTIA_RASPBERRY: [
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            1028156,
        ),  # v1.3.0 default proxy factory address
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            6038388,
        ),  # v1.3.0 safe proxy factory address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7101196),  # v1.4.1
    ],
    EthereumNetwork.POLYGON_BLACKBERRY: [
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            765141,
        ),  # v1.3.0 default proxy factory address
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            1194297,
        ),  # v1.3.0 safe proxy factory address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1725488),  # v1.4.1
    ],
    EthereumNetwork.ARBITRUM_BLUEBERRY: [
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            19364,
        ),  # v1.3.0 default proxy factory address
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            42024,
        ),  # v1.3.0 safe proxy factory address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 281856),  # v1.4.1
    ],
    EthereumNetwork.X_LAYER_MAINNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            359536,
        ),  # v1.3.0 safe proxy factory address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            71695,
        ),  # v1.3.0 default proxy factory address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3752781),  # v1.4.1
    ],
    EthereumNetwork.PULSECHAIN: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 18804210),  # 1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12504126),  # v1.3.0
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 9084508),  # v1.1.1
        ("0x50e55Af101C777bA7A1d560a774A82eF002ced9F", 8915731),  # v1.1.0
        ("0x12302fE9c02ff50939BaAaaf415fc226C078613C", 7450116),  # v1.0.0
    ],
    EthereumNetwork.PULSECHAIN_TESTNET_V4: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 12504126),  # v1.3.0
        ("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 9084508),  # v1.1.1
        ("0x50e55Af101C777bA7A1d560a774A82eF002ced9F", 8915731),  # v1.1.0
        ("0x12302fE9c02ff50939BaAaaf415fc226C078613C", 7450116),  # v1.0.0
    ],
    EthereumNetwork.RSS3_VSL_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2297578),  # v1.3.0
    ],
    EthereumNetwork.RSS3_VSL_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1699348),  # v1.3.0
    ],
    EthereumNetwork.CROSSFI_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2322620),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3481834),  # v1.4.1
    ],
    EthereumNetwork.BLAST: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 377537),  # v1.4.1
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            257344,
        ),  # v1.3.0  Safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            132405,
        ),  # v1.3.0  Default singleton address
    ],
    EthereumNetwork.ASTAR_ZKYOTO: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            1026735,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            914700,
        ),  # v1.3.0 default singleton address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2840996),  # v1.4.1
    ],
    EthereumNetwork.SAAKURU_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 26744116),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 30517726),  # v1.4.1
    ],
    EthereumNetwork.REDSTONE: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 930025),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 929904),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2533109),  # v1.4.1
    ],
    EthereumNetwork.GARNET_HOLESKY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 937080),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 936805),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2540773),  # v1.4.1
    ],
    EthereumNetwork.ENDURANCE_SMART_CHAIN_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 462212),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 461971),  # v1.4.1
    ],
    EthereumNetwork.MORPH_HOLESKY: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 260112),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1171388),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 11020464),  # v1.3.0
    ],
    EthereumNetwork.CYBER_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1098904),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1886341),  # v1.4.1
    ],
    EthereumNetwork.CYBER_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 515914),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 324595),  # v1.4.1
    ],
    EthereumNetwork.LISK: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 139932),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1236816),  # v1.4.1
    ],
    EthereumNetwork.TAIKO_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 10700),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 7366),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 19211),  # v1.4.1
    ],
    EthereumNetwork.TAIKO_HEKLA_L2: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 158794),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 253167),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 276578),  # v1.4.1
    ],
    EthereumNetwork.AMOY: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6005942),  # v1.4.1
    ],
    EthereumNetwork.ASTAR_ZKEVM: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2802278),  # v1.4.1
    ],
    EthereumNetwork.HOLESKY: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 100413),  # v1.4.1
    ],
    EthereumNetwork.RE_AL: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 81980),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 14),  # v1.3.0
    ],
    EthereumNetwork.UNREAL: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 61539),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1769),  # v1.3.0
    ],
    EthereumNetwork.SEI_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 80546985),  # v1.4.1
    ],
    EthereumNetwork.ZETACHAIN_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3315623),  # v1.4.1
    ],
    EthereumNetwork.LINEA_SEPOLIA: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1305441),  # v1.4.1
    ],
    EthereumNetwork.ZILLIQA_EVM: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3831166),  # v1.4.1
    ],
    EthereumNetwork.ZILLIQA_EVM_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6965133),  # v1.4.1
    ],
    EthereumNetwork.ZIRCUIT_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 9199668),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 22760793),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 16922921),  # v1.4.1
    ],
    EthereumNetwork.LORENZO: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 303664),  # v1.3.0
    ],
    EthereumNetwork.F_XCORE_TESTNET_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14854843),  # v1.4.1
    ],
    EthereumNetwork.F_XCORE_MAINNET_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 16088791),  # v1.4.1
    ],
    EthereumNetwork.DODOCHAIN_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1641),  # v1.3.0
    ],
    EthereumNetwork.ETHERLINK_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 994172),  # v1.3.0
    ],
    EthereumNetwork.ETHERLINK_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 3826151),  # v1.3.0
    ],
    EthereumNetwork.KAVA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 11835195),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14909866),  # v1.4.1
    ],
    EthereumNetwork.BERACHAIN_BARTIO: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 100399),  # v1.3.0
    ],
    EthereumNetwork.WORLD_CHAIN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 257893),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5134071),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 257488),  # v1.4.1
    ],
    EthereumNetwork.ABEY_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 20551566),  # v1.3.0
    ],
    EthereumNetwork.FLARE_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 27375848),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 27619301),  # v1.4.1
    ],
    EthereumNetwork.GNOSIS_CHIADO_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 117835),  # v1.3.0
    ],
    EthereumNetwork.SONGBIRD_CANARY_NETWORK: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 36564904),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 66811110),  # v1.4.1
    ],
    EthereumNetwork.SONGBIRD_TESTNET_COSTON: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 9254173),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 19263417),  # v1.4.1
    ],
    EthereumNetwork.FLARE_TESTNET_COSTON2: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 3526),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 10423552),  # v1.4.1
    ],
    EthereumNetwork.NAL_SEPOLIA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2074580),  # v1.3.0
    ],
    EthereumNetwork.ALEPH_ZERO_EVM: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 122),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 942339),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 944370),  # v1.4.1
    ],
    EthereumNetwork.IRISHUB: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 25909136),  # v1.4.1
    ],
    EthereumNetwork.NAL_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1777652),  # v1.3.0
    ],
    EthereumNetwork.CRONOS_ZKEVM_TESTNET: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 163805),  # v1.3.0
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 18997),  # v1.3.0
    ],
    EthereumNetwork.CRONOS_ZKEVM_MAINNET: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 6097),  # v1.3.0
    ],
    EthereumNetwork.SKOPJE_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2845163),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2972526),  # v1.3.0
    ],
    EthereumNetwork.GPT_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1358312),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1448576),  # v1.3.0
    ],
    EthereumNetwork.BEVM_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1651896),  # v1.4.1
    ],
    EthereumNetwork.BEVM_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1571637),  # v1.4.1
    ],
    EthereumNetwork.NAHMII_3_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 716),  # v1.4.1
    ],
    EthereumNetwork.ZIRCUIT_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 131958),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 8246),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 12993033),  # v1.4.1
    ],
    EthereumNetwork.BOB_SEPOLIA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1298122),  # v1.3.0
    ],
    EthereumNetwork.SNAXCHAIN: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 378233),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 388424),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 388607),  # v1.4.1
    ],
    EthereumNetwork.Q_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 15479481),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 15650865),  # v1.3.0
    ],
    EthereumNetwork.Q_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14783667),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 14907808),  # v1.3.0
    ],
    EthereumNetwork.SHAPE_SEPOLIA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2572133),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 15845840),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7703611),  # v1.4.1
    ],
    EthereumNetwork.SHAPE: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1174902),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 14353521),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5878646),  # v1.4.1
    ],
    EthereumNetwork.VANA_MOKSHA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 48927),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 652216),  # v1.4.1
    ],
    EthereumNetwork.CONNEXT_SEPOLIA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 6518),  # v1.3.0
    ],
    EthereumNetwork.EVERCLEAR_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 13144),  # v1.3.0
    ],
    EthereumNetwork.BAHAMUT: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 3007535),  # v1.3.0
    ],
    EthereumNetwork.OORT_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 29277576),  # v1.4.1
    ],
    EthereumNetwork.GAME7_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 154954),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 216522),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 154896),  # v1.3.0
    ],
    EthereumNetwork.GAME7: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 68),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 48),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 58),  # v1.3.0
    ],
    EthereumNetwork.MORPH: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 177467),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 177663),  # v1.4.1
    ],
    EthereumNetwork.OORT_MAINNETDEV: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 304339),  # v1.4.1
    ],
    EthereumNetwork.INK_SEPOLIA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 681679),  # v1.3.0
    ],
    EthereumNetwork.STORY_ODYSSEY_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 340781),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 340886),  # v1.4.1
    ],
    EthereumNetwork.SWELLCHAIN_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 836921),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 836381),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 836863),  # v1.3.0
    ],
    EthereumNetwork.FILECOIN_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 4155364),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4541142),  # v1.3.0
    ],
    EthereumNetwork.FILECOIN_CALIBRATION_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1839904),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2240773),  # v1.3.0
    ],
    EthereumNetwork.NAHMII_3_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 13887),  # v1.4.1
    ],
    EthereumNetwork.PLUME_DEVNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5167616),  # v1.4.1
    ],
    EthereumNetwork.PLUME_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 52573),  # v1.4.1
    ],
    EthereumNetwork.SWELLCHAIN: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 261351),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 261536),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 261762),  # v1.4.1
    ],
    EthereumNetwork.HASHKEY_CHAIN_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4795410),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 4794946),  # v1.4.1
    ],
    EthereumNetwork.SONIC_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 107724),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 79),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5714149),  # v1.3.0
    ],
    EthereumNetwork.WATERFALL_9_TEST_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7329623),  # v1.4.1
    ],
    EthereumNetwork.WATERFALL_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2517833),  # v1.4.1
    ],
    EthereumNetwork.INK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 454711),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 454704),  # v1.3.0 eip155
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 454704),  # v1.3.0 canonical
    ],
    EthereumNetwork.SONIC_BLAZE_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 7483),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 11777889),  # v1.4.1
    ],
    EthereumNetwork.EXSAT_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7691605),  # v1.4.1
    ],
    EthereumNetwork.HASHKEY_CHAIN: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 127743),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 128028),  # v1.3.0
    ],
    EthereumNetwork.EXSAT_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7687767),  # v1.4.1
    ],
    EthereumNetwork.UNICHAIN: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7393713),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 7393985),  # v1.3.0 eip155
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 7394571),  # v1.3.0 canonical
    ],
    EthereumNetwork.BERACHAIN: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 40852),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 45810),  # v1.3.0 eip155
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 41386),  # v1.3.0 canonical
    ],
    EthereumNetwork.EVM_ON_FLOW: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 3041363),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 10722466),  # v1.4.1
    ],
    EthereumNetwork.EVM_ON_FLOW_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2344624),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 20813455),  # v1.4.1
    ],
    EthereumNetwork.BIRDLAYER: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 234),  # v1.3.0
    ],
    EthereumNetwork.ABSTRACT: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 57868),  # v1.3.0
    ],
    EthereumNetwork.ABSTRACT_SEPOLIA_TESTNET: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 2207746),  # v1.3.0
    ],
    EthereumNetwork.OKTO_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5693633),  # v1.4.1
    ],
    EthereumNetwork.STORY: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 542710),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 621416),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 621073),  # v1.4.1
    ],
    EthereumNetwork.NIBIRU_CATACLYSM_1: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 21722329),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 19868328),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 19858911),  # v1.4.1
    ],
    EthereumNetwork.NIBIRU_TESTNET_2: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1126337),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 675078),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 674772),  # v1.4.1
    ],
    EthereumNetwork.TAC_TURIN: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2491820),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2231663),  # v1.4.1
    ],
    EthereumNetwork.ALEPH_ZERO: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 196),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 668),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5639028),  # v1.3.0
    ],
    EthereumNetwork.ETHEREUM_HOODI: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 20156),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 20124),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 20198),  # v1.4.1
    ],
    EthereumNetwork.KATANA_MAINNET: [
        (
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
            318968,
        ),  # v1.3.0 safe singleton address
        (
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            318968,
        ),  # v1.3.0 default singleton address
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 13511105),  # v1.4.1
    ],
    EthereumNetwork.AUTONOMYS_TAURUS_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1196789),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 416910),  # v1.4.1
    ],
    EthereumNetwork.STORY_AENEID_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 973637),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2462491),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4945880),  # v1.3.0
    ],
    EthereumNetwork.AUTONITY_PICCADILLY_TIBER_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14677602),  # v1.4.1
    ],
    EthereumNetwork.BOBA_SEPOLIA: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 8926647),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 21674875),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 14069955),  # v1.4.1
    ],
    EthereumNetwork.BERACHAIN_BEPOLIA: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2067958),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2069978),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1440031),  # v1.3.0
    ],
    EthereumNetwork.SONEIUM_TESTNET_MINATO: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1835098),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2337245),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 3900839),  # v1.4.1
    ],
    EthereumNetwork.IMMUTABLE_ZKEVM: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 1602061),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 23354694),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 18849241),  # v1.4.1
    ],
    EthereumNetwork.IMMUTABLE_ZKEVM_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 3244297),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 19363822),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 24995946),  # v1.3.0
    ],
    EthereumNetwork.PYROPE_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 382695),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 3752626),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 629498),  # v1.3.0
    ],
    EthereumNetwork.PLATON_DEV_TESTNET2: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 85388183),  # v1.4.1
    ],
    EthereumNetwork.PLATON_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 121386465),  # v1.4.1
    ],
    EthereumNetwork.ARENA_Z: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1528714),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 8196583),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 9395369),  # v1.3.0
    ],
    EthereumNetwork.PEAQ: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1365374),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5688263),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1315222),  # v1.4.1
    ],
    EthereumNetwork.BOTANIX_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 235940),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 235706),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 529867),  # v1.3.0
    ],
    EthereumNetwork.TAC_SAINT_PETERSBURG: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2049644),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 2049523),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2049440),  # v1.4.1
    ],
    EthereumNetwork.TAC_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 18262),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 18453),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 17977),  # v1.4.1
    ],
    EthereumNetwork.SOPHON: [
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 106),  # v1.3.0
        ("0xc329D02fd8CB2fc13aa919005aF46320794a8629", 120),  # v1.4.1
    ],
    EthereumNetwork.SOPHON_TESTNET: [
        ("0xc329D02fd8CB2fc13aa919005aF46320794a8629", 75634),  # v1.4.1
        ("0xDAec33641865E4651fB43181C6DB6f7232Ee91c2", 13501),  # v1.3.0
    ],
    EthereumNetwork.PLASMA_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 517662),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 519172),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 521732),  # v1.4.1
    ],
    EthereumNetwork.CODEX_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 11533321),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 11531800),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 11535137),  # v1.4.1
    ],
    EthereumNetwork.METAL_L2: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1252050),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 20204890),  # v1.3.0
    ],
    EthereumNetwork.MONAD_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 11641791),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 11644889),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 11648187),  # v1.3.0
    ],
    EthereumNetwork.ETHEREAL_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 224350),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 225445),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 225484),  # v1.4.1
    ],
    EthereumNetwork.OPBNB_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4640861),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 13660224),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 21962323),  # v1.4.1
    ],
    EthereumNetwork.POLYNOMIAL: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 18563369),  # v1.4.1
    ],
    EthereumNetwork.ENI_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 6360916),  # v1.4.1
    ],
    EthereumNetwork.VANA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4515240),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 625278),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 625808),  # v1.4.1
    ],
    EthereumNetwork.ZIRCUIT_GARFIELD_TESTNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 1928120),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 5814274),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 5815409),  # v1.3.0
    ],
    EthereumNetwork.PHAROS_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 18709976),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 18712208),  # v1.4.1
    ],
    EthereumNetwork.PLASMA_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 64075),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 63796),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 0),  # v1.4.1
    ],
    EthereumNetwork.LENS: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 4250411),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4250519),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1724224),  # v1.4.1
    ],
    EthereumNetwork.PAIX_DEVELOPMENT_NETWORK: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 179030),  # v1.4.1
    ],
    EthereumNetwork._0G_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 4923560),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 3648926),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 4899749),  # v1.3.0
    ],
    EthereumNetwork.INCENTIV_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 375409),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 381960),  # v1.4.1
    ],
    EthereumNetwork.AUTONOMYS_CHRONOS_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 119145),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 119191),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 119206),  # v1.4.1
    ],
    EthereumNetwork.BOB: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 200468),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 199948),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 427032),  # v1.4.1
    ],
    EthereumNetwork.CROSSFI_MAINNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 680488),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 680790),  # v1.4.1
    ],
    EthereumNetwork.CITREA_TESTNET: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 665279),  # v1.3.0
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 665089),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 1792647),  # v1.4.1
    ],
    EthereumNetwork.MINT_MAINNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 7688600),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 2888224),  # v1.3.0
    ],
    EthereumNetwork.SEI_TESTNET: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 188493669),  # v1.4.1
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 188493154),  # v1.3.0
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 188492754),  # v1.3.0
    ],
    EthereumNetwork.INCENTIV: [
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 223220),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 223803),  # v1.4.1
    ],
    EthereumNetwork.SAGA: [
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 2031957),  # v1.4.1
    ],
    EthereumNetwork.GRAVITY_ALPHA_MAINNET: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 98990719),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 88),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 66229672),  # v1.3.0
    ],
    EthereumNetwork.GRAVITY_ALPHA_TESTNET_SEPOLIA: [
        ("0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2", 10817),  # v1.3.0
        ("0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67", 425),  # v1.4.1
        ("0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC", 502),  # v1.3.0
    ],
}


safe_singleton_contract_names = ["GnosisSafe", "GnosisSafeL2", "Safe", "SafeL2"]
safe_proxy_factory_contract_names = [
    "ProxyFactory",
    "GnosisSafeProxyFactory",
    "SafeProxyFactory",
]


def get_default_addresses_with_version(
    filter_contract_names: Union[List, None] = None
) -> List[Tuple[ChecksumAddress, str]]:
    """
    Get the default addresses and versions from contract names.
    The version is the extended one with L2 in case of L2 contract.

    :return: list of Safe deployment contract addresses with version
    """
    default_addresses: List[Tuple[ChecksumAddress, str]] = []
    for version, contracts in default_safe_deployments.items():
        for contract_name, addresses in contracts.items():
            if not filter_contract_names or contract_name in filter_contract_names:
                for address in addresses:
                    extended_version = (
                        version + "+L2" if "L2" in contract_name else version
                    )
                    default_addresses.append(
                        (fast_to_checksum_address(address), extended_version)
                    )

    return default_addresses
