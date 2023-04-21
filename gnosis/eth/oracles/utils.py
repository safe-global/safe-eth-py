import functools
import logging

from eth_abi.exceptions import DecodingError
from eth_typing import ChecksumAddress
from web3.exceptions import Web3Exception

from gnosis.eth import EthereumClient

from .exceptions import CannotGetPriceFromOracle

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=10_000)
def get_decimals(
    token_address: ChecksumAddress, ethereum_client: EthereumClient
) -> int:
    """
    Auxiliary function so RPC call to get `token decimals` is cached and
    can be reused for every Oracle, instead of having a cache per Oracle.

    :param token_address:
    :param ethereum_client:
    :return: Decimals for a token
    :raises CannotGetPriceFromOracle: If there's a problem with the query
    """
    try:
        return ethereum_client.erc20.get_decimals(token_address)
    except (
        Web3Exception,
        DecodingError,
        ValueError,
    ) as e:
        message = f"Cannot get decimals for token={token_address}"
        logger.debug(message)
        raise CannotGetPriceFromOracle(message) from e
