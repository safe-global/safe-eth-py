import json
from functools import cached_property
from typing import Any, Dict, List, Optional, TypedDict, Union, cast

from eth_account import Account
from eth_account.messages import encode_defunct
from eth_typing import Address, ChecksumAddress, HexAddress, HexStr

from safe_eth.eth import EthereumNetwork, EthereumNetworkNotSupported
from safe_eth.eth.constants import NULL_ADDRESS
from safe_eth.eth.eip712 import eip712_encode_hash
from safe_eth.util.http import prepare_http_session

from .order import Order, OrderKind

AnyAddressType = Union[Address, HexAddress, ChecksumAddress]


class TradeResponse(TypedDict):
    blockNumber: int
    logIndex: int
    orderUid: HexStr
    buyAmount: str  # Stringified int
    sellAmount: str  # Stringified int
    sellAmountBeforeFees: str  # Stringified int
    owner: AnyAddressType  # Not checksummed
    buyToken: AnyAddressType
    sellToken: AnyAddressType
    txHash: HexStr


class AmountResponse(TypedDict):
    sellAmount: int
    buyAmount: int


class ErrorResponse(TypedDict):
    errorType: str
    description: str


class CowSwapAPI:
    """
    Client for CowSwap API. More info: https://docs.cowswap.exchange/
    """

    SETTLEMENT_CONTRACT_ADDRESSES = {
        EthereumNetwork.MAINNET: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
        EthereumNetwork.GNOSIS: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
        EthereumNetwork.SEPOLIA: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    }

    API_BASE_URLS = {
        EthereumNetwork.MAINNET: "https://api.cow.fi/mainnet",
        EthereumNetwork.GNOSIS: "https://api.cow.fi/xdai",
        EthereumNetwork.SEPOLIA: "https://api.cow.fi/sepolia",
    }

    def __init__(self, ethereum_network: EthereumNetwork, request_timeout: int = 10):
        self.network = ethereum_network
        if self.network not in self.API_BASE_URLS:
            raise EthereumNetworkNotSupported(
                f"{self.network.name} network not supported by CowSwap"
            )
        self.settlement_contract_address = self.SETTLEMENT_CONTRACT_ADDRESSES[
            self.network
        ]
        self.base_url = self.API_BASE_URLS[self.network]
        self.http_session = prepare_http_session(10, 100)
        self.request_timeout = request_timeout

    @cached_property
    def weth_address(self) -> ChecksumAddress:
        """
        :return: Wrapped ether checksummed address
        """
        if self.network == EthereumNetwork.GNOSIS:  # WXDAI
            return ChecksumAddress(
                HexAddress(HexStr("0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"))
            )

        # Mainnet WETH9
        return ChecksumAddress(
            HexAddress(HexStr("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"))
        )

    def get_quote(
        self, order: Order, from_address: ChecksumAddress
    ) -> Union[Dict[str, Any], ErrorResponse]:
        url = self.base_url + "/api/v1/quote"
        data_json = {
            "sellToken": order.sellToken.lower(),
            "buyToken": order.buyToken.lower(),
            "sellAmountAfterFee": str(order.sellAmount),
            # "validTo": order.validTo,
            "appData": json.dumps(order.appData),
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
            response_dict = r.json()
            return ErrorResponse(
                errorType=response_dict.get("errorType", "Error getting quote"),
                description=response_dict.get("description", ""),
            )

    def get_fee(
        self, order: Order, from_address: ChecksumAddress
    ) -> Union[int, ErrorResponse]:
        quote = self.get_quote(order, from_address)

        if "quote" in quote:
            result = cast(Dict[str, Any], quote)
            return int(result["quote"]["feeAmount"])
        else:
            error = cast(ErrorResponse, quote)
            return error

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

        url = self.base_url + "/api/v1/orders"
        from_address = Account.from_key(private_key).address
        if not order.feeAmount:
            fee_amount = self.get_fee(order, from_address)
            if isinstance(fee_amount, int):
                order.feeAmount = fee_amount
            elif "errorType" in fee_amount:  # ErrorResponse
                return fee_amount

        signable_hash = eip712_encode_hash(
            order.get_eip712_structured_data(
                self.network.value,
                ChecksumAddress(HexAddress(HexStr(self.settlement_contract_address))),
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
            "appData": json.dumps(order.appData),
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
            response_dict = r.json()
            return ErrorResponse(
                errorType=response_dict.get("errorType", "Error placing order"),
                description=response_dict.get("description", ""),
            )

    def get_orders(
        self, owner: ChecksumAddress, offset: int = 0, limit=10
    ) -> Union[List[Dict[str, Any]], ErrorResponse]:
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
        url = self.base_url + f"/api/v1/account/{owner}/orders"
        r = self.http_session.get(url, timeout=self.request_timeout)
        if r.ok:
            return cast(List[Dict[str, Any]], r.json())
        else:
            response_dict = r.json()
            return ErrorResponse(
                errorType=response_dict.get("errorType", "Error getting orders"),
                description=response_dict.get("description", ""),
            )

    def get_trades(
        self, order_ui: Optional[HexStr] = None, owner: Optional[ChecksumAddress] = None
    ) -> Union[List[TradeResponse], ErrorResponse]:
        assert bool(order_ui) ^ bool(
            owner
        ), "order_ui or owner must be provided, but not both"
        url = self.base_url + "/api/v1/trades/?"
        if order_ui:
            url += f"orderUid={order_ui}"
        elif owner:
            url += f"owner={owner}"

        r = self.http_session.get(url, timeout=self.request_timeout)
        if r.ok:
            return cast(List[TradeResponse], r.json())
        else:
            response_dict = r.json()
            return ErrorResponse(
                errorType=response_dict.get("errorType", "Error getting trades"),
                description=response_dict.get("description", ""),
            )

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
            appData={},
            feeAmount=0,
            kind="sell" if kind == OrderKind.SELL else "buy",  # `sell` or `buy`
            partiallyFillable=False,
            sellTokenBalance="erc20",  # `erc20`, `external` or `internal`
            buyTokenBalance="erc20",  # `erc20` or `internal`
        )

        quote = self.get_quote(order, NULL_ADDRESS)
        if "quote" in quote:
            result = cast(Dict[str, Any], quote)
            return {
                "buyAmount": int(result["quote"]["buyAmount"]),
                "sellAmount": int(result["quote"]["sellAmount"]),
            }
        else:
            error = cast(ErrorResponse, quote)
            return error
