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
    }
