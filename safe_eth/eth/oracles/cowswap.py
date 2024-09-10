import logging
from typing import Optional, Union, cast

from eth_typing import ChecksumAddress, HexAddress, HexStr

from safe_eth.eth.clients.cowswap import CowSwapAPI, OrderKind
from safe_eth.eth.clients.cowswap.cow_swap_api import AmountResponse, ErrorResponse

from .. import EthereumClient, EthereumNetworkNotSupported
from .exceptions import CannotGetPriceFromOracle
from .oracles import PriceOracle
from .utils import get_decimals

logger = logging.getLogger(__name__)


class CowswapOracle(PriceOracle):
    """
    CowSwap Oracle implementation

    https://docs.cow.fi/off-chain-services/api
    """

    def __init__(
        self,
        ethereum_client: EthereumClient,
    ):
        """
        :param ethereum_client:
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.api = CowSwapAPI(ethereum_client.get_network())

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if CowSwap is available for the EthereumClient provided, `False` otherwise
        """
        try:
            CowSwapAPI(ethereum_client.get_network())
            return True
        except EthereumNetworkNotSupported:
            return False

    def get_price(
        self, token_address_1: str, token_address_2: Optional[str] = None
    ) -> float:
        token_address_2 = token_address_2 or self.api.weth_address
        if token_address_1 == token_address_2:
            return 1.0
        token_address_1_checksum = ChecksumAddress(HexAddress(HexStr(token_address_1)))
        token_address_2_checksum = ChecksumAddress(HexAddress(HexStr(token_address_2)))
        token_1_decimals = get_decimals(token_address_1_checksum, self.ethereum_client)
        try:
            result: Union[
                AmountResponse, ErrorResponse
            ] = self.api.get_estimated_amount(
                token_address_1_checksum,
                token_address_2_checksum,
                OrderKind.SELL,
                10**token_1_decimals,
            )
            if "buyAmount" in result and "sellAmount" in result:
                result = cast(AmountResponse, result)
                # Decimals needs to be adjusted
                token_2_decimals = get_decimals(
                    token_address_2_checksum, self.ethereum_client
                )
                return (
                    float(result["buyAmount"])
                    / result["sellAmount"]
                    * 10 ** (token_1_decimals - token_2_decimals)
                )

            exception = None
        except IOError as exc:
            exception = exc

        message = (
            f"Cannot get price from CowSwap {{}} "
            f"for token-1={token_address_1} to token-2={token_address_2}"
        )
        logger.debug(message)
        raise CannotGetPriceFromOracle(message) from exception
