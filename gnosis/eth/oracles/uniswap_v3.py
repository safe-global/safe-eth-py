import functools
import logging
from typing import Optional

from eth_abi.exceptions import DecodingError
from eth_typing import ChecksumAddress
from web3.contract import Contract
from web3.exceptions import BadFunctionCallOutput

from gnosis.util import cached_property

from .. import EthereumClient
from ..constants import NULL_ADDRESS
from ..contracts import get_erc20_contract
from .abis.uniswap_v3 import (
    uniswap_v3_factory_abi,
    uniswap_v3_pool_abi,
    uniswap_v3_router_abi,
)
from .exceptions import CannotGetPriceFromOracle
from .oracles import PriceOracle
from .utils import get_decimals

logger = logging.getLogger(__name__)


class UniswapV3Oracle(PriceOracle):
    # https://docs.uniswap.org/protocol/reference/deployments
    UNISWAP_V3_ROUTER = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"

    # Cache to optimize calculation: https://docs.uniswap.org/sdk/guides/fetching-prices#understanding-sqrtprice
    PRICE_CONVERSION_CONSTANT = 2**192

    def __init__(
        self,
        ethereum_client: EthereumClient,
        uniswap_v3_router_address: Optional[ChecksumAddress] = None,
    ):
        """
        :param ethereum_client:
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

        self.router_address = uniswap_v3_router_address or self.UNISWAP_V3_ROUTER
        self.factory = self.get_factory()

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
        uniswap_v3_router_address: Optional[ChecksumAddress] = None,
    ) -> bool:
        """
        :param ethereum_client:
        :param uniswap_v3_router_address:
        :return: `True` if Uniswap V3 is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.is_contract(
            uniswap_v3_router_address or cls.UNISWAP_V3_ROUTER
        )

    def get_factory(self) -> Contract:
        """
        Factory contract creates the pools for token pairs

        :return: Uniswap V3 Factory Contract
        """
        try:
            factory_address = self.router.functions.factory().call()
        except BadFunctionCallOutput:
            raise ValueError(
                f"Uniswap V3 Router Contract {self.router_address} does not exist"
            )
        return self.w3.eth.contract(factory_address, abi=uniswap_v3_factory_abi)

    @cached_property
    def router(self) -> Contract:
        """
        Router knows about the `Uniswap Factory` and `Wrapped Eth` addresses for the network

        :return: Uniswap V3 Router Contract
        """
        return self.w3.eth.contract(self.router_address, abi=uniswap_v3_router_abi)

    @cached_property
    def weth_address(self) -> ChecksumAddress:
        """
        :return: Wrapped ether checksummed address
        """
        return self.router.functions.WETH9().call()

    @functools.lru_cache(maxsize=512)
    def get_pool_address(
        self, token_address: str, token_address_2: str, fee: Optional[int] = 3000
    ) -> Optional[ChecksumAddress]:
        """
        Get pool address for tokens with a given fee (by default, 0.3)

        :param token_address:
        :param token_address_2:
        :param fee: Uniswap V3 uses 0.3 as the default fee
        :return: Pool address
        """

        pool_address = self.factory.functions.getPool(
            token_address, token_address_2, fee
        ).call()
        if pool_address == NULL_ADDRESS:
            return None

        return pool_address

    def get_price(
        self, token_address: str, token_address_2: Optional[str] = None
    ) -> float:
        """
        :param token_address:
        :param token_address_2:
        :return: price for `token_address` related to `token_address_2`. If `token_address_2` is not
            provided, `Wrapped Eth` address will be used
        """
        token_address_2 = token_address_2 or self.weth_address
        if token_address == token_address_2:
            return 1.0

        reversed = token_address.lower() > token_address_2.lower()

        # Make it cache friendly as order does not matter
        args = (
            (token_address_2, token_address)
            if reversed
            else (token_address, token_address_2)
        )
        pool_address = self.get_pool_address(*args)

        if not pool_address:
            raise CannotGetPriceFromOracle(
                f"Uniswap V3 pool does not exist for {token_address} and {token_address_2}"
            )

        # Decimals needs to be adjusted
        token_decimals = get_decimals(token_address, self.ethereum_client)
        token_2_decimals = get_decimals(token_address_2, self.ethereum_client)

        pool_contract = self.w3.eth.contract(pool_address, abi=uniswap_v3_pool_abi)
        try:
            (
                token_balance,
                token_2_balance,
                (sqrt_price_x96, _, _, _, _, _, _),
            ) = self.ethereum_client.batch_call(
                [
                    get_erc20_contract(
                        self.ethereum_client.w3, token_address
                    ).functions.balanceOf(pool_address),
                    get_erc20_contract(
                        self.ethereum_client.w3, token_address_2
                    ).functions.balanceOf(pool_address),
                    pool_contract.functions.slot0(),
                ]
            )
            if (token_balance / 10**token_decimals) < 2 or (
                token_2_balance / 10**token_2_decimals
            ) < 2:
                error_message = (
                    f"Not enough liquidity on uniswap v3 for pair token_1={token_address} "
                    f"token_2={token_address_2}, at least 2 units of each token are required"
                )
                logger.warning(error_message)
                raise CannotGetPriceFromOracle(error_message)
        except (
            ValueError,
            BadFunctionCallOutput,
            DecodingError,
        ) as e:
            error_message = (
                f"Cannot get uniswap v3 price for pair token_1={token_address} "
                f"token_2={token_address_2}"
            )
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e

        # https://docs.uniswap.org/sdk/guides/fetching-prices
        if not reversed:
            # Multiplying by itself is way faster than exponential
            price = (sqrt_price_x96 * sqrt_price_x96) / self.PRICE_CONVERSION_CONSTANT
        else:
            price = self.PRICE_CONVERSION_CONSTANT / (sqrt_price_x96 * sqrt_price_x96)

        return price * 10 ** (token_decimals - token_2_decimals)
