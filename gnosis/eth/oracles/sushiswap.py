import logging

from hexbytes import HexBytes

from .. import EthereumNetwork
from .oracles import UniswapV2Oracle

logger = logging.getLogger(__name__)


class SushiswapOracle(UniswapV2Oracle):
    PAIR_INIT_CODE = HexBytes(
        "0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303"
    )
    ROUTER_ADDRESSES = {
        EthereumNetwork.MAINNET: "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
        EthereumNetwork.MATIC: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.ARBITRUM: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.AVALANCHE: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.MOON_MOONRIVER: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.FANTOM: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.BINANCE: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.XDAI: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.CELO: "0x1421bDe4B10e8dd459b3BCb598810B1337D56842",
        EthereumNetwork.FUSE_MAINNET: "0xF4d73326C13a4Fc5FD7A064217e12780e9Bd62c3",
        EthereumNetwork.OKEXCHAIN: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.PALM: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.MOON_MOONBEAM: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
        EthereumNetwork.HECO: "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
    }
