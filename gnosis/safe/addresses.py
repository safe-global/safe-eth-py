"""
Contains information about Safe contract addresses deployed in every chain

Every entry contains a tuple with address, deployment block number and version
"""
from typing import Dict, List, Tuple

from gnosis.eth import EthereumNetwork

MASTER_COPIES: Dict[EthereumNetwork, List[Tuple[str, int, str]]] = {
    EthereumNetwork.MAINNET: [
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
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10329734, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 9084503, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 8915728, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 7457553, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 6766257, "0.1.0"),
        ("0xAC6072986E985aaBE7804695EC2d8970Cf7541A2", 6569433, "0.0.2"),
    ],
    EthereumNetwork.GOERLI: [
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
    EthereumNetwork.PULSECHAIN_MAINNET: [
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
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10329734, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 9084503, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 8915728, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 7457553, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 6766257, "0.1.0"),
        ("0xAC6072986E985aaBE7804695EC2d8970Cf7541A2", 6569433, "0.0.2"),
    ],
    EthereumNetwork.PULSECHAIN_TESTNET: [
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
        ("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552", 12504268, "1.3.0"),
        ("0x6851D6fDFAfD08c0295C392436245E5bc78B0185", 10329734, "1.2.0"),
        ("0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F", 9084503, "1.1.1"),
        ("0xaE32496491b53841efb51829d6f886387708F99B", 8915728, "1.1.0"),
        ("0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A", 7457553, "1.0.0"),
        ("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af", 6766257, "0.1.0"),
        ("0xAC6072986E985aaBE7804695EC2d8970Cf7541A2", 6569433, "0.0.2"),
    ],
}

PROXY_FACTORIES: Dict[EthereumNetwork, List[Tuple[str, int]]] = {
    EthereumNetwork.MAINNET: [
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
    EthereumNetwork.GOERLI: [
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
    EthereumNetwork.PULSECHAIN_MAINNET: [
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
    EthereumNetwork.PULSECHAIN_TESTNET: [
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
}
