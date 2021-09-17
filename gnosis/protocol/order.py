from enum import Enum

from eip712_structs import Address, Boolean, Bytes, EIP712Struct, String, Uint


class Order(EIP712Struct):
    sellToken = Address()
    buyToken = Address()
    receiver = Address()
    sellAmount = Uint(256)
    buyAmount = Uint(256)
    validTo = Uint(32)
    appData = Bytes(32)
    feeAmount = Uint(256)
    kind = String()  # `sell` or `buy`
    partiallyFillable = Boolean()
    sellTokenBalance = String()  # `erc20`, `external` or `internal`
    buyTokenBalance = String()  # `erc20` or `internal`


class OrderKind(Enum):
    BUY = 0
    SELL = 1
