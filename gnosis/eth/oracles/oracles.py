import logging
from abc import ABC, abstractmethod

from web3 import Web3

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


class Kyber(PriceOracle):
    def __init__(self, w3: Web3, kyber_network_proxy_address: str):
        self.w3 = w3
        self.kyber_network_proxy_address = kyber_network_proxy_address

    def get_price(self, token_address_1: str, token_address_2: str) -> float:
        kyber_network_proxy_contract = get_kyber_network_proxy_contract(self.w3,
                                                                        self.kyber_network_proxy_address)
        try:
            expected_rate, _ = kyber_network_proxy_contract.functions.getExpectedRate(token_address_1,
                                                                                      token_address_2,
                                                                                      int(1e18)).call()
            price = expected_rate / 1e18
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


class Uniswap(PriceOracle):
    def __init__(self, w3: Web3, uniswap_exchange_address: str):
        self.w3 = w3
        self.uniswap_exchange_address = uniswap_exchange_address

    def get_price(self, token_address: str) -> float:
        uniswap_factory = get_uniswap_factory_contract(self.w3, self.uniswap_exchange_address)
        uniswap_exchange_address = uniswap_factory.functions.getExchange(token_address).call()
        if uniswap_exchange_address == NULL_ADDRESS:
            error_message = f'Cannot get price from uniswap-factory={uniswap_exchange_address} ' \
                            f'for token={token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message)

        uniswap_exchange = get_uniswap_exchange_contract(self.w3, uniswap_exchange_address)
        value = int(1e18)
        price = uniswap_exchange.functions.getTokenToEthInputPrice(value).call() / value
        if price <= 0.:
            error_message = f'price={price} <= 0 from uniswap-factory={uniswap_exchange_address} ' \
                            f'for token={token_address}'
            logger.warning(error_message)
            raise InvalidPriceFromOracle(error_message)
        return price


