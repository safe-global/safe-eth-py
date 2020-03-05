import functools
import logging
from abc import ABC, abstractmethod

import requests
from hexbytes import HexBytes
from web3.exceptions import BadFunctionCallOutput

from .. import EthereumClient
from ..constants import NULL_ADDRESS
from ..contracts import (get_erc20_contract, get_kyber_network_proxy_contract,
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
    # This is the `tokenAddress` they use for ETH ¯\_(ツ)_/¯
    ETH_TOKEN_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

    def __init__(self, ethereum_client: EthereumClient, kyber_network_proxy_address: str):
        """
        :param ethereum_client:
        :param kyber_network_proxy_address: https://developer.kyber.network/docs/MainnetEnvGuide/#contract-addresses
        """
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
        """
        :param ethereum_client:
        :param uniswap_factory_address: https://docs.uniswap.io/frontend-integration/connect-to-uniswap#factory-contract
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.uniswap_factory_address = uniswap_factory_address

    @functools.lru_cache(maxsize=None)
    def get_uniswap_exchange(self, token_address: str) -> str:
        uniswap_factory = get_uniswap_factory_contract(self.w3, self.uniswap_factory_address)
        return uniswap_factory.functions.getExchange(token_address).call()

    def _get_balances_without_batching(self, uniswap_exchange_address: str, token_address: str):
        balance = self.ethereum_client.get_balance(uniswap_exchange_address)
        token_decimals = self.ethereum_client.erc20.get_decimals(token_address)
        token_balance = self.ethereum_client.erc20.get_balance(uniswap_exchange_address, token_address)
        return balance, token_decimals, token_balance

    def _get_balances_using_batching(self, uniswap_exchange_address: str, token_address: str):
        # Use batching instead
        payload_balance = {'jsonrpc': '2.0',
                           'method': 'eth_getBalance',
                           'params': [uniswap_exchange_address, 'latest'],
                           'id': 0}
        erc20 = get_erc20_contract(self.w3, token_address)
        params = {'gas': 0, 'gasPrice': 0}
        decimals_data = erc20.functions.decimals().buildTransaction(params)['data']
        token_balance_data = erc20.functions.balanceOf(uniswap_exchange_address).buildTransaction(params)['data']
        datas = [decimals_data, token_balance_data]
        payload_calls = [{'id': i + 1, 'jsonrpc': '2.0', 'method': 'eth_call',
                          'params': [{'to': token_address, 'data': data}, 'latest']}
                         for i, data in enumerate(datas)]
        payloads = [payload_balance] + payload_calls
        r = requests.post(self.ethereum_client.ethereum_node_url, json=payloads)
        if not r.ok:
            raise CannotGetPriceFromOracle(f'Error from node with url={self.ethereum_client.ethereum_node_url}')
        results = [HexBytes(result['result']) for result in r.json()]

        balance = int(results[0].hex(), 16)
        token_decimals = self.ethereum_client.w3.codec.decode_single('uint8', results[1])
        token_balance = self.ethereum_client.w3.codec.decode_single('uint256', results[2])
        return balance, token_decimals, token_balance

    def get_price(self, token_address: str) -> float:
        uniswap_exchange_address = self.get_uniswap_exchange(token_address)

        if uniswap_exchange_address == NULL_ADDRESS:
            error_message = f'Non existing uniswap exchange for token={token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message)

        try:
            balance, token_decimals, token_balance = self._get_balances_using_batching(uniswap_exchange_address,
                                                                                       token_address)
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
