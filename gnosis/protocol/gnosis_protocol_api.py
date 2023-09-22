from functools import cached_property
from typing import Any, Dict, List, Optional, TypedDict, Union, cast

import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_typing import AnyAddress, ChecksumAddress, HexStr
from hexbytes import HexBytes

from gnosis.eth import EthereumNetwork, EthereumNetworkNotSupported
from gnosis.eth.eip712 import eip712_encode_hash

from ..eth.constants import NULL_ADDRESS
from .order import Order, OrderKind


class TradeResponse(TypedDict):
    blockNumber: int
    logIndex: int
    orderUid: HexStr
    buyAmount: str  # Stringified int
    sellAmount: str  # Stringified int
    sellAmountBeforeFees: str  # Stringified int
    owner: AnyAddress  # Not checksummed
    buyToken: AnyAddress
    sellToken: AnyAddress
    txHash: HexStr


class AmountResponse(TypedDict):
    sellAmount: int
    buyAmount: int


class ErrorResponse(TypedDict):
    errorType: str
    description: str


class GnosisProtocolAPI:
    """
    Client for GnosisProtocol API. More info: https://docs.cowswap.exchange/
    """

    SETTLEMENT_CONTRACT_ADDRESSES = {
        EthereumNetwork.MAINNET: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
        EthereumNetwork.GOERLI: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
        EthereumNetwork.GNOSIS: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    }

    API_BASE_URLS = {
        EthereumNetwork.MAINNET: "https://api.cow.fi/mainnet/api/v1/",
        EthereumNetwork.GOERLI: "https://api.cow.fi/goerli/api/v1/",
        EthereumNetwork.GNOSIS: "https://api.cow.fi/xdai/api/v1/",
    }

    def __init__(self, ethereum_network: EthereumNetwork, request_timeout: int = 10):
        self.network = ethereum_network
        if self.network not in self.API_BASE_URLS:
            raise EthereumNetworkNotSupported(
                f"{self.network.name} network not supported by Gnosis Protocol"
            )
        self.settlement_contract_address = self.SETTLEMENT_CONTRACT_ADDRESSES[
            self.network
        ]
        self.base_url = self.API_BASE_URLS[self.network]
        self.http_session = self._prepare_http_session()
        self.request_timeout = request_timeout

    def _prepare_http_session(self) -> requests.Session:
        """
        Prepare http session with custom pooling. See:
        https://urllib3.readthedocs.io/en/stable/advanced-usage.html
        https://docs.python-requests.org/en/v1.2.3/api/#requests.adapters.HTTPAdapter
        https://web3py.readthedocs.io/en/stable/providers.html#httpprovider
        """
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=100,
            pool_block=False,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @cached_property
    def weth_address(self) -> ChecksumAddress:
        """
        :return: Wrapped ether checksummed address
        """
        if self.network == EthereumNetwork.GNOSIS:  # WXDAI
            return ChecksumAddress("0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d")
        if self.network == EthereumNetwork.GOERLI:  # Goerli WETH9
            return ChecksumAddress("0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6")

        # Mainnet WETH9
        return ChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")

    def get_quote(
        self, order: Order, from_address: ChecksumAddress
    ) -> Union[Dict[str, Any], ErrorResponse]:
        url = self.base_url + "quote"
        data_json = {
            "sellToken": order.sellToken.lower(),
            "buyToken": order.buyToken.lower(),
            "sellAmountAfterFee": str(order.sellAmount),
            # "validTo": order.validTo,
            "appData": HexBytes(order.appData).hex()
            if isinstance(order.appData, bytes)
            else order.appData,
            "feeAmount": str(order.feeAmount),
            "kind": order.kind,
            "partiallyFillable": order.partiallyFillable,
            "signingScheme": "ethsign",
            "from": from_address,
            "priceQuality": "fast",
        }
        r = self.http_session.post(url, json=data_json, timeout=self.request_timeout)
        if r.ok:
            return r.json()
        else:
            return ErrorResponse(r.json())

    def get_fee(
        self, order: Order, from_address: ChecksumAddress
    ) -> Union[int, ErrorResponse]:
        quote = self.get_quote(order, from_address)

        if "quote" in quote:
            return int(quote["quote"]["feeAmount"])
        else:
            return quote

    def place_order(
        self, order: Order, private_key: HexStr
    ) -> Union[HexStr, ErrorResponse]:
        """
        Place order. If `feeAmount=0` in Order it will be calculated calling `get_fee(order, from_address)`

        :return: UUID for the order as a hex hash
        """
        assert (
            order.buyAmount and order.sellAmount
        ), "Order buyAmount and sellAmount cannot be empty"

        url = self.base_url + "orders/"
        from_address = Account.from_key(private_key).address
        if not order.feeAmount:
            fee_amount = self.get_fee(order, from_address)
            if isinstance(fee_amount, int):
                order.feeAmount = fee_amount
            elif "errorType" in fee_amount:  # ErrorResponse
                return fee_amount

        signable_hash = eip712_encode_hash(
            order.get_eip712_structured_data(
                self.network.value, self.settlement_contract_address
            )
        )
        message = encode_defunct(primitive=signable_hash)
        signed_message = Account.from_key(private_key).sign_message(message)

        data_json = {
            "sellToken": order.sellToken.lower(),
            "buyToken": order.buyToken.lower(),
            "sellAmount": str(order.sellAmount),
            "buyAmount": str(order.buyAmount),
            "validTo": order.validTo,
            "appData": HexBytes(order.appData).hex()
            if isinstance(order.appData, bytes)
            else order.appData,
            "feeAmount": str(order.feeAmount),
            "kind": order.kind,
            "partiallyFillable": order.partiallyFillable,
            "signature": signed_message.signature.hex(),
            "signingScheme": "ethsign",
            "from": from_address,
        }
        r = self.http_session.post(url, json=data_json, timeout=self.request_timeout)
        if r.ok:
            return HexStr(r.json())
        else:
            return ErrorResponse(r.json())

    def get_orders(
        self, owner: ChecksumAddress, offset: int = 0, limit=10
    ) -> List[Dict[str, Any]]:
        """
        :param owner:
        :param offset: Defaults to 0
        :param limit: Defaults to 10. Maximum is 1000, minimum is 1
        :return: Orders of one user paginated. The orders are ordered by their creation
            date descending (newest orders first).
            To enumerate all orders start with offset 0 and keep increasing the offset by the
            total number of returned results. When a response contains less than the limit
            the last page has been reached.
        """
        url = self.base_url + f"account/{owner}/orders"
        r = self.http_session.get(url, timeout=self.request_timeout)
        if r.ok:
            return cast(List[Dict[str, Any]], r.json())
        else:
            return ErrorResponse(r.json())

    def get_trades(
        self, order_ui: Optional[HexStr] = None, owner: Optional[ChecksumAddress] = None
    ) -> List[TradeResponse]:
        assert bool(order_ui) ^ bool(
            owner
        ), "order_ui or owner must be provided, but not both"
        url = self.base_url + "trades/?"
        if order_ui:
            url += f"orderUid={order_ui}"
        elif owner:
            url += f"owner={owner}"

        r = self.http_session.get(url, timeout=self.request_timeout)
        if r.ok:
            return cast(List[TradeResponse], r.json())
        else:
            return ErrorResponse(r.json())

    def get_estimated_amount(
        self,
        base_token: ChecksumAddress,
        quote_token: ChecksumAddress,
        kind: OrderKind,
        amount_wei: int,
    ) -> Union[AmountResponse, ErrorResponse]:
        """

        :param base_token:
        :param quote_token:
        :param kind:
        :param amount_wei:
        :return: Both `sellAmount` and `buyAmount` as they can be adjusted by CowSwap API
        """
        order = Order(
            sellToken=base_token,
            buyToken=quote_token,
            receiver=NULL_ADDRESS,
            sellAmount=amount_wei * 10 if kind == OrderKind.SELL else 0,
            buyAmount=amount_wei * 10 if kind == OrderKind.BUY else 0,
            validTo=0,  # Valid for 1 hour
            appData="0x0000000000000000000000000000000000000000000000000000000000000000",
            feeAmount=0,
            kind=kind.name.lower(),  # `sell` or `buy`
            partiallyFillable=False,
            sellTokenBalance="erc20",  # `erc20`, `external` or `internal`
            buyTokenBalance="erc20",  # `erc20` or `internal`
        )

        quote = self.get_quote(order, NULL_ADDRESS)
        if "quote" in quote:
            return {
                "buyAmount": int(quote["quote"]["buyAmount"]),
                "sellAmount": int(quote["quote"]["sellAmount"]),
            }
        else:
            return quote
