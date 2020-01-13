import logging
from abc import ABC, abstractmethod

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

from .. import EthereumClient
from ..constants import NULL_ADDRESS
from ..contracts import (get_kyber_network_proxy_contract,
                         get_uniswap_exchange_contract,
                         get_uniswap_factory_contract)

logger = logging.getLogger(__name__)


class OracleException(Exception):
    pass


class InvalidPriceFromOracle(OracleException):
    pass


class CannotGetPriceFromOracle(OracleException):
    pass


class PriceOracle(ABC):
    @abstractmethod
    def get_price(self, *args) -> float:
        pass


class KyberOracle(PriceOracle):
    ETH_TOKEN_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

    def __init__(self, ethereum_client: EthereumClient, kyber_network_proxy_address: str):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.kyber_network_proxy_address = kyber_network_proxy_address

    def get_price(self, token_address_1: str, token_address_2: str = ETH_TOKEN_ADDRESS) -> float:
        kyber_network_proxy_contract = get_kyber_network_proxy_contract(self.w3,
                                                                        self.kyber_network_proxy_address)
        try:
            expected_rate, _ = kyber_network_proxy_contract.functions.getExpectedRate(token_address_1,
                                                                                      token_address_2,
                                                                                      int(1e18)).call()
            price = expected_rate / 1e18

            if price <= 0.:
                # Try again the opposite
                expected_rate, _ = kyber_network_proxy_contract.functions.getExpectedRate(token_address_2,
                                                                                          token_address_1,
                                                                                          int(1e18)).call()
                price = (1e18 / expected_rate) if expected_rate else 0

            if price <= 0.:
                error_message = f'price={price} <= 0 from kyber-network-proxy={self.kyber_network_proxy_address} ' \
                                f'for token-1={token_address_1} to token-2={token_address_2}'
                logger.warning(error_message)
                raise InvalidPriceFromOracle(error_message)
            return price
        except ValueError as e:
            error_message = f'Cannot get price from kyber-network-proxy={self.kyber_network_proxy_address} ' \
                            f'for token-1={token_address_1} to token-2={token_address_2}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e


class UniswapOracle(PriceOracle):
    def __init__(self, ethereum_client: EthereumClient, uniswap_factory_address: str):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.uniswap_factory_address = uniswap_factory_address
        self.uniswap_exchanges = {}

    def get_price(self, token_address: str) -> float:
        if token_address not in self.uniswap_exchanges:
            uniswap_factory = get_uniswap_factory_contract(self.w3, self.uniswap_factory_address)
            self.uniswap_exchanges[token_address] = uniswap_factory.functions.getExchange(token_address).call()
        uniswap_exchange_address = self.uniswap_exchanges[token_address]

        if uniswap_exchange_address == NULL_ADDRESS:
            error_message = f'Non existing uniswap exchange for token={token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message)

        try:
            token_decimals = self.ethereum_client.erc20.get_decimals(token_address)
            token_balance = self.ethereum_client.erc20.get_balance(uniswap_exchange_address, token_address)
            balance = self.ethereum_client.get_balance(uniswap_exchange_address)
            price = balance / token_balance / 10**(18 - token_decimals)
            if price <= 0.:
                error_message = f'price={price} <= 0 from uniswap-factory={uniswap_exchange_address} ' \
                                f'for token={token_address}'
                logger.warning(error_message)
                raise InvalidPriceFromOracle(error_message)
            return price
        except (BadFunctionCallOutput, ZeroDivisionError) as e:
            error_message = f'Cannot get token balance for token={token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e
