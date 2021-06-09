import functools
import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple

import requests
from eth_abi.exceptions import DecodingError
from eth_abi.packed import encode_abi_packed
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

from .. import EthereumClient
from ..constants import NULL_ADDRESS
from ..contracts import (get_erc20_contract, get_kyber_network_proxy_contract,
                         get_uniswap_factory_contract,
                         get_uniswap_v2_factory_contract,
                         get_uniswap_v2_pair_contract,
                         get_uniswap_v2_router_contract)
from ..ethereum_client import EthereumNetwork
from .abis.balancer_abis import balancer_pool_abi
from .abis.curve_abis import curve_address_provider_abi, curve_registry_abi
from .abis.mooniswap_abis import mooniswap_abi
from .abis.yearn_abis import YVAULT_ABI

try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property


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


class PricePoolOracle(ABC):
    @abstractmethod
    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        pass


class UsdPricePoolOracle(ABC):
    @abstractmethod
    def get_pool_usd_token_price(self, pool_token_address: ChecksumAddress) -> float:
        pass


class KyberOracle(PriceOracle):
    # This is the `tokenAddress` they use for ETH ¯\_(ツ)_/¯
    ETH_TOKEN_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    ADDRESSES = {
        EthereumNetwork.MAINNET: '0x9AAb3f75489902f3a48495025729a0AF77d4b11e',
        EthereumNetwork.RINKEBY: '0x0d5371e5EE23dec7DF251A8957279629aa79E9C5',
        EthereumNetwork.ROPSTEN: '0xd719c34261e099Fdb33030ac8909d5788D3039C4',
        EthereumNetwork.KOVAN: '0xc153eeAD19e0DBbDb3462Dcc2B703cC6D738A37c',
    }

    def __init__(self, ethereum_client: EthereumClient,
                 kyber_network_proxy_address: Optional[str] = None):
        """
        :param ethereum_client:
        :param kyber_network_proxy_address: https://developer.kyber.network/docs/MainnetEnvGuide/#contract-addresses
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self._kyber_network_proxy_address = kyber_network_proxy_address

    @cached_property
    def kyber_network_proxy_address(self):
        if self._kyber_network_proxy_address:
            return self._kyber_network_proxy_address
        return self.ADDRESSES.get(self.ethereum_client.get_network(),
                                  self.ADDRESSES.get(EthereumNetwork.MAINNET))  # By default return Mainnet address

    @cached_property
    def kyber_network_proxy_contract(self):
        return get_kyber_network_proxy_contract(self.w3, self.kyber_network_proxy_address)

    def get_price(self, token_address_1: str, token_address_2: str = ETH_TOKEN_ADDRESS) -> float:
        try:
            # Get decimals for token, estimation will be more accurate
            decimals = self.ethereum_client.erc20.get_decimals(token_address_1)
            token_unit = int(10 ** decimals)
            expected_rate, _ = self.kyber_network_proxy_contract.functions.getExpectedRate(token_address_1,
                                                                                           token_address_2,
                                                                                           int(token_unit)).call()

            price = expected_rate / 1e18

            if price <= 0.:
                # Try again the opposite
                expected_rate, _ = self.kyber_network_proxy_contract.functions.getExpectedRate(token_address_2,
                                                                                               token_address_1,
                                                                                               int(token_unit)).call()
                price = (token_unit / expected_rate) if expected_rate else 0

            if price <= 0.:
                error_message = f'price={price} <= 0 from kyber-network-proxy={self.kyber_network_proxy_address} ' \
                                f'for token-1={token_address_1} to token-2={token_address_2}'
                logger.warning(error_message)
                raise InvalidPriceFromOracle(error_message)
            return price
        except (ValueError, BadFunctionCallOutput, DecodingError) as e:
            error_message = f'Cannot get price from kyber-network-proxy={self.kyber_network_proxy_address} ' \
                            f'for token-1={token_address_1} to token-2={token_address_2}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e


class UniswapOracle(PriceOracle):
    ADDRESSES = {
        EthereumNetwork.MAINNET: '0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95',
        EthereumNetwork.RINKEBY: '0xf5D915570BC477f9B8D6C0E980aA81757A3AaC36',
        EthereumNetwork.ROPSTEN: '0x9c83dCE8CA20E9aAF9D3efc003b2ea62aBC08351',
        EthereumNetwork.KOVAN: '0xD3E51Ef092B2845f10401a0159B2B96e8B6c3D30',
        EthereumNetwork.GOERLI: '0x6Ce570d02D73d4c384b46135E87f8C592A8c86dA',
    }

    def __init__(self, ethereum_client: EthereumClient, uniswap_factory_address: Optional[str] = None):
        """
        :param ethereum_client:
        :param uniswap_factory_address: https://docs.uniswap.io/frontend-integration/connect-to-uniswap#factory-contract
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self._uniswap_factory_address = uniswap_factory_address

    @cached_property
    def uniswap_factory_address(self):
        if self._uniswap_factory_address:
            return self._uniswap_factory_address
        return self.ADDRESSES.get(self.ethereum_client.get_network(),
                                  self.ADDRESSES.get(EthereumNetwork.MAINNET))

    @cached_property
    def uniswap_factory(self):
        return get_uniswap_factory_contract(self.w3, self.uniswap_factory_address)

    @functools.lru_cache(maxsize=None)
    def get_uniswap_exchange(self, token_address: str) -> str:
        return self.uniswap_factory.functions.getExchange(token_address).call()

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

        results = []
        for result in r.json():
            if 'result' not in result:
                raise CannotGetPriceFromOracle(result['error'])
            else:
                results.append(HexBytes(result['result']))

        balance = int(results[0].hex(), 16)
        token_decimals = self.ethereum_client.w3.codec.decode_single('uint8', results[1])
        token_balance = self.ethereum_client.w3.codec.decode_single('uint256', results[2])
        return balance, token_decimals, token_balance

    def get_price(self, token_address: str) -> float:
        try:
            uniswap_exchange_address = self.get_uniswap_exchange(token_address)
            if uniswap_exchange_address == NULL_ADDRESS:
                raise ValueError
        except (ValueError, BadFunctionCallOutput, DecodingError) as e:
            error_message = f'Non existing uniswap exchange for token={token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e

        try:
            balance, token_decimals, token_balance = self._get_balances_using_batching(uniswap_exchange_address,
                                                                                       token_address)
            # Check liquidity. Require at least 2 ether to be on the pool
            if balance / 1e18 < 2:
                raise CannotGetPriceFromOracle(f'Not enough liquidity for token={token_address}')

            price = balance / token_balance / 10**(18 - token_decimals)
            if price <= 0.:
                error_message = f'price={price} <= 0 from uniswap-factory={uniswap_exchange_address} ' \
                                f'for token={token_address}'
                logger.warning(error_message)
                raise InvalidPriceFromOracle(error_message)
            return price
        except (ValueError, ZeroDivisionError, BadFunctionCallOutput, DecodingError) as e:
            error_message = f'Cannot get token balance for token={token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e


class UniswapV2Oracle(PricePoolOracle, PriceOracle):
    # Pair init code is keccak(getCode(UniswapV2Pair))
    pair_init_code = HexBytes('0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f')
    router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'  # Same address on every network

    def __init__(self, ethereum_client: EthereumClient,
                 router_address: Optional[str] = None):
        """
        :param ethereum_client:
        :param router_address: https://uniswap.org/docs/v2/smart-contracts/router02/
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.router_address: str = router_address or self.router_address
        self.router = get_uniswap_v2_router_contract(ethereum_client.w3, self.router_address)
        self._decimals_cache: Dict[str, int] = {}

    @cached_property
    def factory(self):
        return get_uniswap_v2_factory_contract(self.ethereum_client.w3, self.factory_address)

    @cached_property
    def factory_address(self) -> str:
        """
        :return: Uniswap factory checksummed address
        :raises: BadFunctionCallOutput: If router contract is not deployed
        """
        return self.router.functions.factory().call()

    @cached_property
    def weth_address(self) -> str:
        """
        :return: Wrapped ether checksummed address
        :raises: BadFunctionCallOutput: If router contract is not deployed
        """
        return self.router.functions.WETH().call()

    @functools.lru_cache(maxsize=None)
    def get_pair_address(self, token_address: str, token_address_2: str) -> Optional[str]:
        """
        Get uniswap pair address. `token_address` and `token_address_2` are interchangeable.
        https://uniswap.org/docs/v2/smart-contracts/factory/
        :param token_address:
        :param token_address_2:
        :return: Address of the pair for `token_address` and `token_address_2`, if it has been created, else `None`.
        """
        # Token order does not matter for getting pair, just for creating or querying PairCreated event
        pair_address = self.factory.functions.getPair(token_address, token_address_2).call()
        if pair_address == NULL_ADDRESS:
            return None
        return pair_address

    def calculate_pair_address(self, token_address: str, token_address_2: str):
        """
        Calculate pair address without querying blockchain.
        https://uniswap.org/docs/v2/smart-contract-integration/getting-pair-addresses/#docs-header
        :param token_address:
        :param token_address_2:
        :return: Checksummed address for token pair. It could be not created yet
        """
        if token_address.lower() > token_address_2.lower():
            token_address, token_address_2 = token_address_2, token_address
        salt = Web3.keccak(encode_abi_packed(['address', 'address'],
                                             [token_address, token_address_2]))
        address = Web3.keccak(
            encode_abi_packed(['bytes', 'address', 'bytes', 'bytes'],
                              [HexBytes('ff'), self.factory_address, salt, self.pair_init_code]
                              ))[-20:]
        return Web3.toChecksumAddress(address)

    def get_decimals(self, token_address: str, token_address_2: str) -> Tuple[int, int]:
        if not (token_address in self._decimals_cache and token_address_2 in self._decimals_cache):
            decimals_1, decimals_2 = self.ethereum_client.batch_call(
                [
                    get_erc20_contract(self.w3, token_address).functions.decimals(),
                    get_erc20_contract(self.w3, token_address_2).functions.decimals(),
                ])
            self._decimals_cache[token_address] = decimals_1
            self._decimals_cache[token_address_2] = decimals_2
        return self._decimals_cache[token_address], self._decimals_cache[token_address_2]

    def get_reserves(self, pair_address: str) -> Tuple[int, int]:
        """
        Returns the
        Also returns the block.timestamp (mod 2**32) of the last block during which an interaction occured for the pair.
        https://uniswap.org/docs/v2/smart-contracts/pair/
        :return: Reserves of `token_address` and `token_address_2` used to price trades and distribute liquidity.
        """
        pair_contract = get_uniswap_v2_pair_contract(self.ethereum_client.w3, pair_address)
        # Reserves return token_1 reserves, token_2 reserves and block timestamp (mod 2**32) of last interaction
        reserves_1, reserves_2, _ = pair_contract.functions.getReserves().call()
        return reserves_1, reserves_2

    def get_price(self, token_address: str, token_address_2: Optional[str] = None) -> float:
        # These lines only make sense when `get_pair_address` is used. `calculate_pair_address` will always return
        # an address, even it that exchange is not deployed

        # pair_address = self.get_pair_address(token_address, token_address_2)
        # if not pair_address:
        #    error_message = f'Non existing uniswap V2 exchange for token={token_address}'
        #    logger.warning(error_message)
        #    raise CannotGetPriceFromOracle(error_message)
        try:
            token_address_2 = token_address_2 if token_address_2 else self.weth_address
            if token_address == token_address_2:
                return 1.
            pair_address = self.calculate_pair_address(token_address, token_address_2)
            # Tokens are sorted, so token_1 < token_2
            reserves_1, reserves_2 = self.get_reserves(pair_address)
            decimals_1, decimals_2 = self.get_decimals(token_address, token_address_2)
            if token_address.lower() > token_address_2.lower():
                reserves_2, reserves_1 = reserves_1, reserves_2

            # Check liquidity. Require at least 2 units of every token to be on the pool
            if reserves_1 / 10 ** decimals_1 < 2 or reserves_2 / 10 ** decimals_2 < 2:
                raise CannotGetPriceFromOracle(f'Not enough liquidity for pair token_1={token_address} '
                                               f'token_2={token_address_2}')
            decimals_normalized_reserves_1 = reserves_1 * 10 ** decimals_2
            decimals_normalized_reserves_2 = reserves_2 * 10 ** decimals_1

            return decimals_normalized_reserves_2 / decimals_normalized_reserves_1
        except (ValueError, ZeroDivisionError, BadFunctionCallOutput, DecodingError) as e:
            error_message = f'Cannot get uniswap v2 price for pair token_1={token_address} ' \
                            f'token_2={token_address_2}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e

    def get_price_without_exception(self, token_address: str, token_address_2: Optional[str] = None) -> float:
        """
        :param token_address:
        :param token_address_2:
        :return: Call `get_price`, return 0. instead on an exception if there's any issue
        """
        try:
            return self.get_price(token_address, token_address_2=token_address_2)
        except CannotGetPriceFromOracle:
            return 0.

    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        Estimate pool token price based on its components
        :param pool_token_address:
        :return: Pool token eth price per unit (total pool token supply / 1e18)
        :raises: CannotGetPriceFromOracle
        """
        try:
            pair_contract = get_uniswap_v2_pair_contract(self.ethereum_client.w3, pool_token_address)
            ((reserves_1, reserves_2, _),
             token_address_1, token_address_2, total_supply) = self.ethereum_client.batch_call(
                [
                    pair_contract.functions.getReserves(),
                    pair_contract.functions.token0(),
                    pair_contract.functions.token1(),
                    pair_contract.functions.totalSupply(),
                ])
            decimals_1, decimals_2 = self.get_decimals(token_address_1, token_address_2)

            # Total value for one token should be the same than total value for the other token
            # if pool is under active arbitrage. We use the price for the first token we find
            for token_address, decimals, reserves in zip((token_address_1, token_address_2),
                                                         (decimals_1, decimals_2),
                                                         (reserves_1, reserves_2)):
                try:
                    price = self.get_price(token_address)
                    total_value = (reserves / 10 ** decimals_1) * price
                    return (total_value * 2) / (total_supply / 1e18)
                except CannotGetPriceFromOracle:
                    continue
        except (ValueError, ZeroDivisionError, BadFunctionCallOutput, DecodingError) as e:
            error_message = f'Cannot get uniswap v2 price for pool token={pool_token_address}'
            logger.warning(error_message)
            raise CannotGetPriceFromOracle(error_message) from e


class SushiswapOracle(UniswapV2Oracle):
    pair_init_code = HexBytes('0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303')
    router_address = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'


class CurveOracle(UsdPricePoolOracle):
    """
    Curve pool Oracle. More info on https://curve.fi/
    """
    def __init__(self, ethereum_client: EthereumClient,
                 address_provider: str = '0x0000000022D53366457F9d5E68Ec105046FC4383'):
        """
        :param ethereum_client:
        :param address_provider: https://curve.readthedocs.io/registry-address-provider.html
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.address_provider_contract = self.w3.eth.contract(address_provider, abi=curve_address_provider_abi)

    @cached_property
    def registry_contract(self):
        """
        :return: https://curve.readthedocs.io/registry-registry.html
        """
        return self.w3.eth.contract(self.address_provider_contract.functions.get_registry().call(),
                                    abi=curve_registry_abi)

    def get_pool_usd_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        :param pool_token_address: Curve pool token address
        :return: Usd price for token
        :raises: CannotGetPriceFromOracle
        """
        try:
            return self.registry_contract.functions.get_virtual_price_from_lp_token(pool_token_address).call() / 1e18
        except (ValueError, BadFunctionCallOutput, DecodingError):
            raise CannotGetPriceFromOracle(f'Cannot get price for {pool_token_address}. It is not a curve pool token')


class YearnOracle(UsdPricePoolOracle):
    """
    Yearn oracle. More info on https://docs.yearn.finance
    """
    def __init__(self, ethereum_client: EthereumClient):
        """
        :param ethereum_client:
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    def get_pool_usd_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        :param pool_token_address: Yearn yVault pool token address
        :return: Usd price for token
        :raises: CannotGetPriceFromOracle
        """
        contract = self.w3.eth.contract(pool_token_address, abi=YVAULT_ABI)
        try:
            return contract.functions.getPricePerFullShare().call() / 1e18
        except (ValueError, BadFunctionCallOutput, DecodingError):
            raise CannotGetPriceFromOracle(f'Cannot get price for {pool_token_address}. It is not a Yearn yVault')


class BalancerOracle(PricePoolOracle):
    """
    Oracle for Balancer. More info on https://balancer.exchange
    """
    def __init__(self, ethereum_client: EthereumClient, price_oracle: PriceOracle):
        """
        :param ethereum_client:
        :param price_oracle: Price oracle to get the price for the components of the Balancer Pool, UniswapV2 is
        recommended
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.price_oracle = price_oracle

    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        Estimate balancer pool token price based on its components
        :param pool_token_address: Balancer pool token address
        :return: Eth price for pool token
        :raises: CannotGetPriceFromOracle
        """
        try:
            balancer_pool_contract = self.w3.eth.contract(pool_token_address, abi=balancer_pool_abi)
            current_tokens, total_supply = self.ethereum_client.batch_call([
                balancer_pool_contract.functions.getCurrentTokens(),
                balancer_pool_contract.functions.totalSupply(),
            ])
            number_tokens = len(current_tokens)
            # denormalized_weight = self.ethereum_client.batch_call([
            #    balancer_pool_contract.functions.getReserves(current_token)
            #    for current_token in current_tokens
            # ])
            token_balances_and_decimals = self.ethereum_client.batch_call([
                balancer_pool_contract.functions.getBalance(token_address)
                for token_address in current_tokens
            ] + [
                get_erc20_contract(self.w3, token_address).functions.decimals()
                for token_address in current_tokens
            ])
            token_balances = token_balances_and_decimals[:number_tokens]
            token_decimals = token_balances_and_decimals[number_tokens:]
            token_prices = [self.price_oracle.get_price(token_address) for token_address in current_tokens]
            total_eth_value = 0
            for token_balance, token_decimal, token_price in zip(token_balances, token_decimals, token_prices):
                total_eth_value += (token_balance / 10**token_decimal) * token_price
            return total_eth_value / (total_supply / 1e18)
        except (ValueError, BadFunctionCallOutput, DecodingError):
            raise CannotGetPriceFromOracle(f'Cannot get price for {pool_token_address}. '
                                           f'It is not a balancer pool token')


class MooniswapOracle(BalancerOracle):
    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        Estimate balancer pool token price based on its components
        :param pool_token_address: Moniswap pool token address
        :return: Eth price for pool token
        :raises: CannotGetPriceFromOracle
        """
        try:
            balancer_pool_contract = self.w3.eth.contract(pool_token_address, abi=mooniswap_abi)
            tokens, total_supply = self.ethereum_client.batch_call([
                balancer_pool_contract.functions.getTokens(),
                balancer_pool_contract.functions.totalSupply(),
            ])
            if len(tokens) == 1 or any([token == NULL_ADDRESS for token in tokens]):  # One of the tokens is ether
                ethereum_amount = self.ethereum_client.get_balance(pool_token_address)
                return ethereum_amount * 2 / total_supply
            else:
                for token in tokens:
                    try:
                        price = self.price_oracle.get_price(token)
                        token_contract = get_erc20_contract(self.w3, token)
                        token_balance, token_decimals = self.ethereum_client.batch_call([
                            token_contract.functions.balanceOf(pool_token_address),
                            token_contract.functions.decimals(),
                        ])
                        total_value = (token_balance / 10 ** token_decimals) * price
                        return (total_value * 2) / (total_supply / 1e18)
                    except CannotGetPriceFromOracle:
                        continue

                raise CannotGetPriceFromOracle(f'Cannot get price for {pool_token_address}. '
                                               f'It is not a mooniswap pool token')

        except (ValueError, BadFunctionCallOutput, DecodingError):
            raise CannotGetPriceFromOracle(f'Cannot get price for {pool_token_address}. '
                                           f'It is not a mooniswap pool token')
