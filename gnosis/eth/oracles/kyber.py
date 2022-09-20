import logging
from typing import Optional

from eth_abi.exceptions import DecodingError
from web3.exceptions import BadFunctionCallOutput

from gnosis.util import cached_property

from .. import EthereumClient, EthereumNetwork
from ..contracts import get_kyber_network_proxy_contract
from .exceptions import CannotGetPriceFromOracle, InvalidPriceFromOracle
from .oracles import PriceOracle
from .utils import get_decimals

logger = logging.getLogger(__name__)


class KyberOracle(PriceOracle):
    """
    KyberSwap Legacy Oracle

    https://docs.kyberswap.com/Legacy/addresses/addresses-mainnet
    """

    # This is the `tokenAddress` they use for ETH ¯\_(ツ)_/¯
    ETH_TOKEN_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    ADDRESSES = {
        EthereumNetwork.MAINNET: "0x9AAb3f75489902f3a48495025729a0AF77d4b11e",
        EthereumNetwork.RINKEBY: "0x0d5371e5EE23dec7DF251A8957279629aa79E9C5",
        EthereumNetwork.ROPSTEN: "0xd719c34261e099Fdb33030ac8909d5788D3039C4",
        EthereumNetwork.KOVAN: "0xc153eeAD19e0DBbDb3462Dcc2B703cC6D738A37c",
    }

    def __init__(
        self,
        ethereum_client: EthereumClient,
        kyber_network_proxy_address: Optional[str] = None,
    ):
        """
        :param ethereum_client:
        :param kyber_network_proxy_address: https://developer.kyber.network/docs/MainnetEnvGuide/#contract-addresses
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self._kyber_network_proxy_address = kyber_network_proxy_address

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.get_network() in cls.ADDRESSES

    @cached_property
    def kyber_network_proxy_address(self):
        if self._kyber_network_proxy_address:
            return self._kyber_network_proxy_address
        return self.ADDRESSES.get(
            self.ethereum_client.get_network(),
            self.ADDRESSES.get(EthereumNetwork.MAINNET),
        )  # By default return Mainnet address

    @cached_property
    def kyber_network_proxy_contract(self):
        return get_kyber_network_proxy_contract(
            self.w3, self.kyber_network_proxy_address
        )

    def get_price(
        self, token_address_1: str, token_address_2: str = ETH_TOKEN_ADDRESS
    ) -> float:
        if token_address_1 == token_address_2:
            return 1.0
        try:
            # Get decimals for token, estimation will be more accurate
            decimals = get_decimals(token_address_1, self.ethereum_client)
            token_unit = int(10**decimals)
            (
                expected_rate,
                _,
            ) = self.kyber_network_proxy_contract.functions.getExpectedRate(
                token_address_1, token_address_2, int(token_unit)
            ).call()

            price = expected_rate / 1e18

            if price <= 0.0:
                # Try again the opposite
                (
                    expected_rate,
                    _,
                ) = self.kyber_network_proxy_contract.functions.getExpectedRate(
                    token_address_2, token_address_1, int(token_unit)
                ).call()
                price = (token_unit / expected_rate) if expected_rate else 0

            if price <= 0.0:
                error_message = (
                    f"price={price} <= 0 from kyber-network-proxy={self.kyber_network_proxy_address} "
                    f"for token-1={token_address_1} to token-2={token_address_2}"
                )
                logger.warning(error_message)
                raise InvalidPriceFromOracle(error_message)
            return price
        except (ValueError, BadFunctionCallOutput, DecodingError) as e:
            error_message = (
                f"Cannot get price from kyber-network-proxy={self.kyber_network_proxy_address} "
                f"for token-1={token_address_1} to token-2={token_address_2}"
            )
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e
