from typing import Any, List, Optional, TypedDict, Union

from eth_typing import Address, ChecksumAddress, HexAddress, HexStr

AnyAddressType = Union[Address, HexAddress, ChecksumAddress]


class ParameterDecoded(TypedDict):
    name: str
    type: str
    value: Any


class DataDecoded(TypedDict):
    method: str
    parameters: List[ParameterDecoded]


class Erc20Info(TypedDict):
    name: str
    symbol: str
    decimals: int
    logo_uri: str


class Balance(TypedDict):
    token_address: Optional[AnyAddressType]
    token: Optional[Erc20Info]
    balance: int


class DelegateUser(TypedDict):
    safe: Optional[AnyAddressType]
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
    confirmations: Optional[List[MessageConfirmation]]
    preparedSignature: Optional[HexStr]


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
    data: Optional[HexStr]
    operation: int
    gasToken: Optional[AnyAddressType]
    safeTxGas: int
    baseGas: int
    gasPrice: str
    refundReceiver: Optional[AnyAddressType]
    nonce: int
    execution_date: str
    submission_date: str
    modified: str
    blockNumber: Optional[int]
    transactionHash: HexStr
    safeTxHash: HexStr
    proposer: AnyAddressType
    executor: Optional[AnyAddressType]
    isExecuted: bool
    isSuccessful: Optional[bool]
    ethGasPrice: Optional[str]
    maxFeePerGas: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    gasUsed: Optional[int]
    fee: Optional[int]
    origin: Optional[str]
    dataDecoded: Optional[List[DataDecoded]]
    confirmationsRequired: int
    confirmations: Optional[List[TransactionConfirmation]]
    trusted: bool
    signatures: Optional[HexStr]
