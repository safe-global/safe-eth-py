import functools
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional, Tuple

import requests
from eth_abi import decode as decode_abi
from eth_abi.exceptions import DecodingError
from eth_abi.packed import encode_packed
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract
from web3.exceptions import Web3Exception

from .. import EthereumClient, EthereumNetwork
from ..constants import NULL_ADDRESS
from ..contracts import (
    get_erc20_contract,
    get_uniswap_factory_contract,
    get_uniswap_v2_factory_contract,
    get_uniswap_v2_pair_contract,
    get_uniswap_v2_router_contract,
)
from ..utils import fast_bytes_to_checksum_address, fast_keccak, get_empty_tx_params
from .abis.aave_abis import AAVE_ATOKEN_ABI
from .abis.balancer_abis import balancer_pool_abi
from .abis.cream_abis import cream_ctoken_abi
from .abis.mooniswap_abis import mooniswap_abi
from .abis.zerion_abis import ZERION_TOKEN_ADAPTER_ABI
from .exceptions import CannotGetPriceFromOracle, InvalidPriceFromOracle
from .helpers.curve_gauge_list import CURVE_GAUGE_TO_LP_TOKEN
from .utils import get_decimals

logger = logging.getLogger(__name__)


@dataclass
class UnderlyingToken:
    address: ChecksumAddress
    quantity: int


class BaseOracle(ABC):
    @classmethod
    @abstractmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        raise NotImplementedError


class PriceOracle(BaseOracle):
    @abstractmethod
    def get_price(self, *args) -> float:
        raise NotImplementedError


class PricePoolOracle(BaseOracle):
    @abstractmethod
    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        raise NotImplementedError


class ComposedPriceOracle(BaseOracle):
    @abstractmethod
    def get_underlying_tokens(self, *args) -> List[Tuple[UnderlyingToken]]:
        raise NotImplementedError


class UniswapOracle(PriceOracle):
    """
    Uniswap V1 Oracle

    https://docs.uniswap.org/protocol/V1/guides/connect-to-uniswap
    """

    ADDRESSES = {
        EthereumNetwork.MAINNET: "0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95",
        EthereumNetwork.RINKEBY: "0xf5D915570BC477f9B8D6C0E980aA81757A3AaC36",
        EthereumNetwork.ROPSTEN: "0x9c83dCE8CA20E9aAF9D3efc003b2ea62aBC08351",
        EthereumNetwork.KOVAN: "0xD3E51Ef092B2845f10401a0159B2B96e8B6c3D30",
        EthereumNetwork.GOERLI: "0x6Ce570d02D73d4c384b46135E87f8C592A8c86dA",
    }

    def __init__(
        self,
        ethereum_client: EthereumClient,
        uniswap_factory_address: Optional[str] = None,
    ):
        """
        :param ethereum_client:
        :param uniswap_factory_address: https://docs.uniswap.io/frontend-integration/connect-to-uniswap#factory-contract
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self._uniswap_factory_address = uniswap_factory_address

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
    def uniswap_factory_address(self):
        if self._uniswap_factory_address:
            return self._uniswap_factory_address
        return self.ADDRESSES.get(
            self.ethereum_client.get_network(),
            self.ADDRESSES.get(EthereumNetwork.MAINNET),
        )

    @cached_property
    def uniswap_factory(self):
        return get_uniswap_factory_contract(self.w3, self.uniswap_factory_address)

    @functools.lru_cache(maxsize=2048)
    def get_uniswap_exchange(self, token_address: str) -> str:
        return self.uniswap_factory.functions.getExchange(token_address).call()

    def _get_balances_without_batching(
        self, uniswap_exchange_address: str, token_address: str
    ):
        balance = self.ethereum_client.get_balance(uniswap_exchange_address)
        token_decimals = self.ethereum_client.erc20.get_decimals(token_address)
        token_balance = self.ethereum_client.erc20.get_balance(
            uniswap_exchange_address, token_address
        )
        return balance, token_decimals, token_balance

    def _get_balances_using_batching(
        self, uniswap_exchange_address: str, token_address: str
    ):
        # Use batching instead
        payload_balance = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [uniswap_exchange_address, "latest"],
            "id": 0,
        }
        erc20 = get_erc20_contract(self.w3, token_address)
        params = get_empty_tx_params()
        decimals_data = erc20.functions.decimals().build_transaction(params)["data"]
        token_balance_data = erc20.functions.balanceOf(
            uniswap_exchange_address
        ).build_transaction(params)["data"]
        datas = [decimals_data, token_balance_data]
        payload_calls = [
            {
                "id": i + 1,
                "jsonrpc": "2.0",
                "method": "eth_call",
                "params": [{"to": token_address, "data": data}, "latest"],
            }
            for i, data in enumerate(datas)
        ]
        payloads = [payload_balance] + payload_calls
        r = requests.post(
            self.ethereum_client.ethereum_node_url,
            json=payloads,
            timeout=self.ethereum_client.timeout,
        )
        if not r.ok:
            raise CannotGetPriceFromOracle(
                f"Error from node with url={self.ethereum_client.ethereum_node_url}"
            )

        results = []
        for result in r.json():
            if "result" not in result:
                raise CannotGetPriceFromOracle(result["error"])
            else:
                results.append(HexBytes(result["result"]))

        balance = int(results[0].hex(), 16)
        token_decimals = decode_abi(["uint8"], results[1])[0]
        token_balance = decode_abi(["uint256"], results[2])[0]
        return balance, token_decimals, token_balance

    def get_price(self, token_address: str) -> float:
        try:
            uniswap_exchange_address = self.get_uniswap_exchange(token_address)
            if uniswap_exchange_address == NULL_ADDRESS:
                raise ValueError
        except (Web3Exception, DecodingError, ValueError) as e:
            message = f"Non existing uniswap exchange for token={token_address}"
            logger.debug(message)
            raise CannotGetPriceFromOracle(message) from e

        try:
            balance, token_decimals, token_balance = self._get_balances_using_batching(
                uniswap_exchange_address, token_address
            )
            # Check liquidity. Require at least 2 ether to be on the pool
            if balance / 1e18 < 2:
                raise CannotGetPriceFromOracle(
                    f"Not enough liquidity for token={token_address}"
                )

            price = balance / token_balance / 10 ** (18 - token_decimals)
            if price <= 0.0:
                message = (
                    f"price={price} <= 0 from uniswap-factory={uniswap_exchange_address} "
                    f"for token={token_address}"
                )
                logger.debug(message)
                raise InvalidPriceFromOracle(message)
            return price
        except (
            Web3Exception,
            DecodingError,
            ValueError,
            ZeroDivisionError,
        ) as e:
            message = f"Cannot get token balance for token={token_address}"
            logger.debug(message)
            raise CannotGetPriceFromOracle(message) from e


class UniswapV2Oracle(PricePoolOracle, PriceOracle):
    ROUTER_ADDRESSES = {
        EthereumNetwork.MAINNET: "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    }

    # Pair init code is keccak(getCode(UniswapV2Pair))
    PAIR_INIT_CODE = HexBytes(
        "0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f"
    )

    def __init__(
        self, ethereum_client: EthereumClient, router_address: Optional[str] = None
    ):
        """
        :param ethereum_client:
        :param router_address: https://uniswap.org/docs/v2/smart-contracts/router02/
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.router_address: str = router_address or self.ROUTER_ADDRESSES.get(
            ethereum_client.get_network(),
            self.ROUTER_ADDRESSES[EthereumNetwork.MAINNET],
        )
        self.router = get_uniswap_v2_router_contract(
            ethereum_client.w3, self.router_address
        )

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.is_contract(
            cls.ROUTER_ADDRESSES.get(
                ethereum_client.get_network(),
                cls.ROUTER_ADDRESSES[EthereumNetwork.MAINNET],
            )
        )

    @cached_property
    def factory(self):
        return get_uniswap_v2_factory_contract(
            self.ethereum_client.w3, self.factory_address
        )

    @cached_property
    def factory_address(self) -> str:
        """
        :return: Uniswap factory checksummed address
        :raises: Web3Exception: If router contract is not deployed
        """
        return self.router.functions.factory().call()

    @cached_property
    def weth_address(self) -> str:
        """
        :return: Wrapped ether checksummed address
        :raises: Web3Exception: If router contract is not deployed
        """
        return self.router.functions.WETH().call()

    @functools.lru_cache(maxsize=2048)
    def get_pair_address(
        self, token_address: str, token_address_2: str
    ) -> Optional[str]:
        """
        Get uniswap pair address. `token_address` and `token_address_2` are interchangeable.
        https://uniswap.org/docs/v2/smart-contracts/factory/

        :param token_address:
        :param token_address_2:
        :return: Address of the pair for `token_address` and `token_address_2`, if it has been created, else `None`.
        """
        # Token order does not matter for getting pair, just for creating or querying PairCreated event
        pair_address = self.factory.functions.getPair(
            token_address, token_address_2
        ).call()
        if pair_address == NULL_ADDRESS:
            return None
        return pair_address

    @functools.lru_cache(maxsize=2048)
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
        salt = fast_keccak(
            encode_packed(["address", "address"], [token_address, token_address_2])
        )
        address = fast_keccak(
            encode_packed(
                ["bytes", "address", "bytes", "bytes"],
                [HexBytes("ff"), self.factory_address, salt, self.PAIR_INIT_CODE],
            )
        )[-20:]
        return fast_bytes_to_checksum_address(address)

    def get_reserves(self, pair_address: str) -> Tuple[int, int]:
        """
        Returns the number of tokens in the pool. `getReserves()` also returns the block.timestamp (mod 2**32) of
        the last block during which an interaction occurred for the pair, but it's ignored.
        https://uniswap.org/docs/v2/smart-contracts/pair/

        :return: Reserves of `token_address` and `token_address_2` used to price trades and distribute liquidity.
        """
        pair_contract = get_uniswap_v2_pair_contract(
            self.ethereum_client.w3, pair_address
        )
        # Reserves return token_1 reserves, token_2 reserves and block timestamp (mod 2**32) of last interaction
        reserves_1, reserves_2, _ = pair_contract.functions.getReserves().call()
        return reserves_1, reserves_2

    def get_price(
        self, token_address: str, token_address_2: Optional[str] = None
    ) -> float:
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
                return 1.0
            pair_address = self.calculate_pair_address(token_address, token_address_2)
            # Tokens are sorted, so token_1 < token_2
            reserves_1, reserves_2 = self.get_reserves(pair_address)
            decimals_1 = get_decimals(token_address, self.ethereum_client)
            decimals_2 = get_decimals(token_address_2, self.ethereum_client)
            if token_address.lower() > token_address_2.lower():
                reserves_2, reserves_1 = reserves_1, reserves_2

            # Check liquidity. Require at least 2 units of every token to be on the pool
            if reserves_1 / 10**decimals_1 < 2 or reserves_2 / 10**decimals_2 < 2:
                raise CannotGetPriceFromOracle(
                    f"Not enough liquidity for pair token_1={token_address} "
                    f"token_2={token_address_2}"
                )
            decimals_normalized_reserves_1 = reserves_1 * 10**decimals_2
            decimals_normalized_reserves_2 = reserves_2 * 10**decimals_1

            return decimals_normalized_reserves_2 / decimals_normalized_reserves_1
        except (
            Web3Exception,
            DecodingError,
            ValueError,
            ZeroDivisionError,
        ) as e:
            message = (
                f"Cannot get uniswap v2 price for pair token_1={token_address} "
                f"token_2={token_address_2}"
            )
            logger.debug(message)
            raise CannotGetPriceFromOracle(message) from e

    def get_price_without_exception(
        self, token_address: str, token_address_2: Optional[str] = None
    ) -> float:
        """
        :param token_address:
        :param token_address_2:
        :return: Call `get_price`, return 0. instead on an exception if there's any issue
        """
        try:
            return self.get_price(token_address, token_address_2=token_address_2)
        except CannotGetPriceFromOracle:
            return 0.0

    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        Estimate pool token price based on its components

        :param pool_token_address:
        :return: Pool token eth price per unit (total pool token supply / 1e18)
        :raises: CannotGetPriceFromOracle
        """
        try:
            pair_contract = get_uniswap_v2_pair_contract(
                self.ethereum_client.w3, pool_token_address
            )
            (
                (reserves_1, reserves_2, _),
                token_address_1,
                token_address_2,
                total_supply,
            ) = self.ethereum_client.batch_call(
                [
                    pair_contract.functions.getReserves(),
                    pair_contract.functions.token0(),
                    pair_contract.functions.token1(),
                    pair_contract.functions.totalSupply(),
                ]
            )
            decimals_1 = get_decimals(token_address_1, self.ethereum_client)
            decimals_2 = get_decimals(token_address_2, self.ethereum_client)

            # Total value for one token should be the same than total value for the other token
            # if pool is under active arbitrage. We use the price for the first token we find
            for token_address, decimals, reserves in zip(
                (token_address_1, token_address_2),
                (decimals_1, decimals_2),
                (reserves_1, reserves_2),
            ):
                try:
                    price = self.get_price(token_address)
                    total_value = (reserves / 10**decimals_1) * price
                    return (total_value * 2) / (total_supply / 1e18)
                except CannotGetPriceFromOracle:
                    continue
        except (
            Web3Exception,
            DecodingError,
            ValueError,
            ZeroDivisionError,
        ) as e:
            message = f"Cannot get uniswap v2 price for pool token={pool_token_address}"
            logger.debug(message)
            raise CannotGetPriceFromOracle(message) from e


class AaveOracle(PriceOracle):
    def __init__(self, ethereum_client: EthereumClient, price_oracle: PriceOracle):
        """
        :param ethereum_client:
        :param price_oracle: Price oracle to get the price for the components of Aave Tokens, UniswapV2 is
        recommended
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.price_oracle = price_oracle

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.get_network() == EthereumNetwork.MAINNET

    def get_price(self, token_address: str) -> float:
        if (
            token_address == "0x4da27a545c0c5B758a6BA100e3a049001de870f5"
        ):  # Stacked Aave
            return self.price_oracle.get_price(
                "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
            )
        try:
            underlying_token = (
                self.w3.eth.contract(token_address, abi=AAVE_ATOKEN_ABI)
                .functions.UNDERLYING_ASSET_ADDRESS()
                .call()
            )
            return self.price_oracle.get_price(underlying_token)
        except (Web3Exception, DecodingError, ValueError):
            raise CannotGetPriceFromOracle(
                f"Cannot get price for {token_address}. It is not an Aaave atoken"
            )


class CreamOracle(PriceOracle):
    def __init__(self, ethereum_client: EthereumClient, price_oracle: PriceOracle):
        """
        :param ethereum_client:
        :param price_oracle: Price oracle to get the price for the components of Cream Tokens, UniswapV2 is
        recommended
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.price_oracle = price_oracle

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.get_network() == EthereumNetwork.MAINNET

    def get_price(self, token_address: str) -> float:
        try:
            underlying_token = (
                self.w3.eth.contract(token_address, abi=cream_ctoken_abi)
                .functions.underlying()
                .call()
            )
            return self.price_oracle.get_price(underlying_token)
        except (Web3Exception, DecodingError, ValueError):
            raise CannotGetPriceFromOracle(
                f"Cannot get price for {token_address}. It is not a Cream cToken"
            )


class ZerionComposedOracle(ComposedPriceOracle):
    ZERION_ADAPTER_ADDRESS = None

    def __init__(
        self,
        ethereum_client: EthereumClient,
        zerion_adapter_address: Optional[str] = None,
    ):
        """
        :param ethereum_client:
        :param zerion_adapter_address: Can be retrieved using the Zerion registry on
            0x06FE76B2f432fdfEcAEf1a7d4f6C3d41B5861672 . https://github.com/zeriontech/defi-sdk/wiki/Addresses is
            outdated
        """

        self.zerion_adapter_address = (
            zerion_adapter_address or self.ZERION_ADAPTER_ADDRESS
        )
        if not self.zerion_adapter_address:
            raise ValueError("Expected a Zerion adapter address")
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.get_network() == EthereumNetwork.MAINNET

    @cached_property
    def zerion_adapter_contract(self) -> Optional[Contract]:
        """
        :return: https://curve.readthedocs.io/registry-registry.html
        """
        if self.ethereum_client.is_contract(self.zerion_adapter_address):
            return self.w3.eth.contract(
                self.zerion_adapter_address, abi=ZERION_TOKEN_ADAPTER_ABI
            )

    def get_underlying_tokens(
        self, token_address: ChecksumAddress
    ) -> List[UnderlyingToken]:
        """
        Use Zerion Token adapter to return underlying components for pool

        :param token_address: Pool token address
        :return: Price per share and underlying token
        :raises: CannotGetPriceFromOracle
        """
        if not self.zerion_adapter_contract:
            raise CannotGetPriceFromOracle(
                f"{self.__class__.__name__}: Cannot get price for {token_address}. Cannot find Zerion adapter"
            )

        try:
            results = self.zerion_adapter_contract.functions.getComponents(
                token_address
            ).call()
            if results:
                underlying_tokens = []
                for token_address, _, quantity in results:
                    # If there's just one component, quantity must be 100%
                    normalized_quantity = (
                        1.0
                        if len(results) == 1
                        else quantity / 10 ** len(str(quantity))
                    )
                    underlying_tokens.append(
                        UnderlyingToken(token_address, normalized_quantity)
                    )
                return underlying_tokens
        except (ValueError, Web3Exception, DecodingError):
            pass

        raise CannotGetPriceFromOracle(
            f"{self.__class__.__name__}: Cannot get price for {token_address}. It is not a Zerion supported pool token"
        )


class CurveOracle(ZerionComposedOracle):
    """
    Curve pool Oracle. More info on https://curve.fi/
    """

    ZERION_ADAPTER_ADDRESS = (
        "0x99b0bEadc3984eab9842AF81f9fad0C2219108cc"  # Mainnet address
    )

    def get_underlying_tokens(
        self, token_address: ChecksumAddress
    ) -> List[UnderlyingToken]:
        """
        Check if passed token address is a Curve gauge deposit token, if it's a gauge we replace the address with
        the corresponding LP token address
        More info on https://resources.curve.fi/base-features/understanding-gauges
        """
        if CURVE_GAUGE_TO_LP_TOKEN.get(token_address):
            return super().get_underlying_tokens(CURVE_GAUGE_TO_LP_TOKEN[token_address])

        return super().get_underlying_tokens(token_address)


class PoolTogetherOracle(ZerionComposedOracle):
    """
    PoolTogether pool Oracle. More info on https://pooltogether.com/
    """

    ZERION_ADAPTER_ADDRESS = (
        "0xb4E0E1672fFd9b128784dB9f3BE9158fac3f1DFc"  # Mainnet address
    )


class EnzymeOracle(ZerionComposedOracle):
    """
    Enzyme pool Oracle. More info on https://enzyme.finance/
    """

    ZERION_ADAPTER_ADDRESS = (
        "0x9e71455D748C23566b19493D09435574097C7D67"  # Mainnet address
    )


class YearnOracle(ComposedPriceOracle):
    """
    Yearn oracle. More info on https://docs.yearn.finance
    """

    def __init__(
        self,
        ethereum_client: EthereumClient,
        yearn_vault_token_adapter: Optional[
            str
        ] = "0xb460FcC1B6c1CBD7D03F47B6BD5F03994d286c75",
        iearn_token_adapter: Optional[
            str
        ] = "0x65B23774daE2a5be02dD275918DDF048d177a5B4",
    ):
        """
        :param ethereum_client:
        :param yearn_vault_token_adapter:
        :param iearn_token_adapter:
        """
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.yearn_vault_token_adapter = ZerionComposedOracle(
            ethereum_client, yearn_vault_token_adapter
        )
        self.iearn_token_adapter = ZerionComposedOracle(
            ethereum_client, iearn_token_adapter
        )

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.get_network() == EthereumNetwork.MAINNET

    def get_underlying_tokens(
        self, token_address: ChecksumAddress
    ) -> List[Tuple[float, ChecksumAddress]]:
        """
        :param token_address:
        :return: Price per share and underlying token
        :raises: CannotGetPriceFromOracle
        """
        for adapter in (self.yearn_vault_token_adapter, self.iearn_token_adapter):
            try:
                # Getting underlying token function is the same for both yVault and yToken
                return adapter.get_underlying_tokens(token_address)
            except CannotGetPriceFromOracle:
                pass

        raise CannotGetPriceFromOracle(
            f"Cannot get price for {token_address}. It is not a Yearn yToken/yVault"
        )


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

    @classmethod
    def is_available(
        cls,
        ethereum_client: EthereumClient,
    ) -> bool:
        """
        :param ethereum_client:
        :return: `True` if Oracle is available for the EthereumClient provided, `False` otherwise
        """
        return ethereum_client.get_network() == EthereumNetwork.MAINNET

    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        Estimate balancer pool token price based on its components

        :param pool_token_address: Balancer pool token address
        :return: Eth price for pool token
        :raises: CannotGetPriceFromOracle
        """
        try:
            balancer_pool_contract = self.w3.eth.contract(
                pool_token_address, abi=balancer_pool_abi
            )
            current_tokens, total_supply = self.ethereum_client.batch_call(
                [
                    balancer_pool_contract.functions.getCurrentTokens(),
                    balancer_pool_contract.functions.totalSupply(),
                ]
            )
            if not current_tokens:
                raise ValueError
            number_tokens = len(current_tokens)
            # denormalized_weight = self.ethereum_client.batch_call([
            #    balancer_pool_contract.functions.getReserves(current_token)
            #    for current_token in current_tokens
            # ])
            token_balances_and_decimals = self.ethereum_client.batch_call(
                [
                    balancer_pool_contract.functions.getBalance(token_address)
                    for token_address in current_tokens
                ]
                + [
                    get_erc20_contract(self.w3, token_address).functions.decimals()
                    for token_address in current_tokens
                ]
            )
            token_balances = token_balances_and_decimals[:number_tokens]
            token_decimals = token_balances_and_decimals[number_tokens:]
            token_prices = [
                self.price_oracle.get_price(token_address)
                for token_address in current_tokens
            ]
            total_eth_value = 0
            for token_balance, token_decimal, token_price in zip(
                token_balances, token_decimals, token_prices
            ):
                total_eth_value += (token_balance / 10**token_decimal) * token_price
            return total_eth_value / (total_supply / 1e18)
        except (Web3Exception, DecodingError, ValueError):
            raise CannotGetPriceFromOracle(
                f"Cannot get price for {pool_token_address}. "
                f"It is not a balancer pool token"
            )


class MooniswapOracle(BalancerOracle):
    def get_pool_token_price(self, pool_token_address: ChecksumAddress) -> float:
        """
        Estimate balancer pool token price based on its components

        :param pool_token_address: Moniswap pool token address
        :return: Eth price for pool token
        :raises: CannotGetPriceFromOracle
        """
        try:
            balancer_pool_contract = self.w3.eth.contract(
                pool_token_address, abi=mooniswap_abi
            )
            tokens, total_supply = self.ethereum_client.batch_call(
                [
                    balancer_pool_contract.functions.getTokens(),
                    balancer_pool_contract.functions.totalSupply(),
                ]
            )
            if not tokens:
                raise ValueError
            if len(tokens) == 1 or any(
                [token == NULL_ADDRESS for token in tokens]
            ):  # One of the tokens is ether
                ethereum_amount = self.ethereum_client.get_balance(pool_token_address)
                return ethereum_amount * 2 / total_supply
            else:
                for token in tokens:
                    try:
                        price = self.price_oracle.get_price(token)
                        token_contract = get_erc20_contract(self.w3, token)
                        token_balance, token_decimals = self.ethereum_client.batch_call(
                            [
                                token_contract.functions.balanceOf(pool_token_address),
                                token_contract.functions.decimals(),
                            ]
                        )
                        total_value = (token_balance / 10**token_decimals) * price
                        return (total_value * 2) / (total_supply / 1e18)
                    except CannotGetPriceFromOracle:
                        continue

                raise CannotGetPriceFromOracle(
                    f"Cannot get price for {pool_token_address}. "
                    f"It is not a mooniswap pool token"
                )

        except (Web3Exception, DecodingError, ValueError):
            raise CannotGetPriceFromOracle(
                f"Cannot get price for {pool_token_address}. "
                f"It is not a mooniswap pool token"
            )
