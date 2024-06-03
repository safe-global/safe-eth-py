from typing import Any, List, Optional, TypedDict

from eth_typing import AnyAddress, HexStr


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
    token_address: Optional[AnyAddress]
    token: Optional[Erc20Info]
    balance: int


class DelegateUser(TypedDict):
    safe: Optional[AnyAddress]
    delegate: AnyAddress
    delegator: AnyAddress
    label: str


class MessageConfirmation(TypedDict):
    created: str
    modified: str
    owner: AnyAddress
    signature: HexStr
    signatureType: str


class Message(TypedDict):
    created: str
    modified: str
    safe: AnyAddress
    messageHash: HexStr
    message: Any
    proposedBy: AnyAddress
    safeAppId: int
    confirmations: Optional[List[MessageConfirmation]]
    preparedSignature: Optional[HexStr]


class TransactionConfirmation(TypedDict):
    owner: AnyAddress
    submissionDate: str
    transactionHash: HexStr
    signature: HexStr
    signatureType: str


class Transaction(TypedDict):
    safe: AnyAddress
    to: AnyAddress
    value: str
    data: Optional[HexStr]
    operation: int
    gasToken: Optional[AnyAddress]
    safeTxGas: int
    baseGas: int
    gasPrice: str
    refundReceiver: Optional[AnyAddress]
    nonce: int
    execution_date: str
    submission_date: str
    modified: str
    blockNumber: Optional[int]
    transactionHash: HexStr
    safeTxHash: HexStr
    proposer: AnyAddress
    executor: Optional[AnyAddress]
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
