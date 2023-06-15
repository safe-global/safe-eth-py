from enum import Enum, unique


class EthereumNetworkNotSupported(Exception):
    pass


@unique
class EthereumNetwork(Enum):
    """
    Use https://chainlist.org/ as a reference
    """

    UNKNOWN = -1
    GANACHE = 1337
    MAINNET = 1
    GOERLI = 5
    PULSECHAIN_MAINNET = 369
    PULSECHAIN_TESTNET = 943

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
