from typing import Any, TypedDict

from eth_typing import Address, ChecksumAddress, HexAddress, HexStr

AnyAddressType = Address | HexAddress | ChecksumAddress


class ParameterDecoded(TypedDict):
    name: str
    type: str
    value: Any


class DataDecoded(TypedDict):
    method: str
    parameters: list[ParameterDecoded]


class Erc20Info(TypedDict):
    name: str
    symbol: str
    decimals: int
    logo_uri: str


class Balance(TypedDict):
    token_address: AnyAddressType | None
    token: Erc20Info | None
    balance: int


class DelegateUser(TypedDict):
    safe: AnyAddressType | None
    delegate: AnyAddressType
    delegator: AnyAddressType
    label: str


class MessageConfirmation(TypedDict):
    created: str
    modified: str
    owner: AnyAddressType
    signature: HexStr
    signatureType: str


class Message(TypedDict):
    created: str
    modified: str
    safe: AnyAddressType
    messageHash: HexStr
    message: Any
    proposedBy: AnyAddressType
    safeAppId: int
    confirmations: list[MessageConfirmation] | None
    preparedSignature: HexStr | None


class TransactionConfirmation(TypedDict):
    owner: AnyAddressType
    submissionDate: str
    transactionHash: HexStr
    signature: HexStr
    signatureType: str


class Transaction(TypedDict):
    safe: AnyAddressType
    to: AnyAddressType
    value: str
    data: HexStr | None
    operation: int
    gasToken: AnyAddressType | None
    safeTxGas: str
    baseGas: str
    gasPrice: str
    refundReceiver: AnyAddressType | None
    nonce: str
    execution_date: str
    submission_date: str
    modified: str
    blockNumber: int | None
    transactionHash: HexStr
    safeTxHash: HexStr
    proposer: AnyAddressType
    executor: AnyAddressType | None
    isExecuted: bool
    isSuccessful: bool | None
    ethGasPrice: str | None
    maxFeePerGas: str | None
    maxPriorityFeePerGas: str | None
    gasUsed: int | None
    fee: int | None
    origin: str | None
    dataDecoded: list[DataDecoded] | None
    confirmationsRequired: int
    confirmations: list[TransactionConfirmation] | None
    trusted: bool
    signatures: HexStr | None
