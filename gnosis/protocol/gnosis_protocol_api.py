from typing import Any, Dict, List, Optional, Union, cast

import requests
from eip712_structs import make_domain
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_typing import AnyAddress, ChecksumAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth import EthereumNetwork, EthereumNetworkNotSupported
from gnosis.util import cached_property

from .order import Order, OrderKind

try:
    from typing import TypedDict  # pylint: disable=no-name-in-module
except ImportError:
    from typing_extensions import TypedDict


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
    amount: str
    token: AnyAddress


class ErrorResponse(TypedDict):
    errorType: str
    description: str


class GnosisProtocolAPI:
    """
    Client for GnosisProtocol API. More info: https://docs.cowswap.exchange/
    """

    settlement_contract_addresses = {
        EthereumNetwork.MAINNET: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
        EthereumNetwork.GOERLI: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
        EthereumNetwork.XDAI: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    }

    api_base_urls = {
        EthereumNetwork.MAINNET: "https://api.cow.fi/mainnet/api/v1/",
        EthereumNetwork.GOERLI: "https://api.cow.fi/goerli/api/v1/",
        EthereumNetwork.XDAI: "https://api.cow.fi/xdai/api/v1/",
    }

    def __init__(self, ethereum_network: EthereumNetwork):
        self.network = ethereum_network
        if self.network not in self.api_base_urls:
            raise EthereumNetworkNotSupported(
                f"{self.network.name} network not supported by Gnosis Protocol"
            )
        self.domain_separator = self.build_domain_separator(self.network)
        self.base_url = self.api_base_urls[self.network]
        self.http_session = requests.Session()

    @cached_property
    def weth_address(self) -> ChecksumAddress:
        """
        :return: Wrapped ether checksummed address
        """
        if self.network == EthereumNetwork.MAINNET:
            return ChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
        elif self.network == EthereumNetwork.RINKEBY:
            return ChecksumAddress("0xc778417E063141139Fce010982780140Aa0cD5Ab")
        else:  # XDAI
            return ChecksumAddress("0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1")

    @classmethod
    def build_domain_separator(cls, ethereum_network: EthereumNetwork):
        return make_domain(
            name="Gnosis Protocol",
            version="v2",
            chainId=str(ethereum_network.value),
            verifyingContract=cls.settlement_contract_addresses[ethereum_network],
        )

    def get_fee(self, order: Order) -> int:
        if order["kind"] == "sell":
            amount = order["sellAmount"]
        else:
            amount = order["buyAmount"]
        url = (
            self.base_url
            + f'fee/?sellToken={order["sellToken"]}&buyToken={order["buyToken"]}'
            f'&amount={amount}&kind={order["kind"]}'
        )
        result = self.http_session.get(url).json()
        if "amount" in result:
            return int(result["amount"])
        else:
            return 0

    def place_order(
        self, order: Order, private_key: HexStr
    ) -> Union[HexStr, ErrorResponse]:
        """
        Place order. If `feeAmount=0` in Order it will be calculated calling `get_fee(order)`

        :return: UUID for the order as an hex hash
        """
        assert (
            order["buyAmount"] and order["sellAmount"]
        ), "Order buyAmount and sellAmount cannot be empty"

        url = self.base_url + "orders/"
        order["feeAmount"] = order["feeAmount"] or self.get_fee(order)
        signable_bytes = order.signable_bytes(domain=self.domain_separator)
        signable_hash = Web3.keccak(signable_bytes)
        message = encode_defunct(primitive=signable_hash)
        signed_message = Account.from_key(private_key).sign_message(message)

        data_json = {
            "sellToken": order["sellToken"].lower(),
            "buyToken": order["buyToken"].lower(),
            "sellAmount": str(order["sellAmount"]),
            "buyAmount": str(order["buyAmount"]),
            "validTo": order["validTo"],
            "appData": HexBytes(order["appData"]).hex()
            if isinstance(order["appData"], bytes)
            else order["appData"],
            "feeAmount": str(order["feeAmount"]),
            "kind": order["kind"],
            "partiallyFillable": order["partiallyFillable"],
            "signature": signed_message.signature.hex(),
            "signingScheme": "ethsign",
            "from": Account.from_key(private_key).address,
        }
        r = self.http_session.post(url, json=data_json)
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
        r = self.http_session.get(url)
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

        r = self.http_session.get(url)
        if r.ok:
            return cast(List[TradeResponse], r.json())
        else:
            return ErrorResponse(r.json())

    def get_estimated_amount(
        self,
        base_token: ChecksumAddress,
        quote_token: ChecksumAddress,
        kind: OrderKind,
        amount: int,
    ) -> Union[AmountResponse, ErrorResponse]:
        """
        The estimated amount in quote token for either buying or selling amount of baseToken.
        """
        url = self.base_url + f"markets/{base_token}-{quote_token}/{kind.name}/{amount}"
        r = self.http_session.get(url)
        if r.ok:
            return AmountResponse(r.json())
        else:
            return ErrorResponse(r.json())
