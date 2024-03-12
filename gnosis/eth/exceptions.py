from eth_typing import ChecksumAddress


class EthereumClientException(ValueError):
    pass


class ChainIdIsRequired(EthereumClientException):
    pass


class TransactionAlreadyImported(EthereumClientException):
    pass


class ReplacementTransactionUnderpriced(EthereumClientException):
    pass


class TransactionQueueLimitReached(EthereumClientException):
    pass


class FromAddressNotFound(EthereumClientException):
    pass


class InvalidNonce(EthereumClientException):
    pass


class NonceTooLow(InvalidNonce):
    pass


class NonceTooHigh(InvalidNonce):
    pass


class InsufficientFunds(EthereumClientException):
    pass


class SenderAccountNotFoundInNode(EthereumClientException):
    pass


class UnknownAccount(EthereumClientException):
    pass


class GasLimitExceeded(EthereumClientException):
    pass


class TransactionGasPriceTooLow(EthereumClientException):
    pass


class ContractAlreadyDeployed(EthereumClientException):
    def __init__(self, message: str, address: ChecksumAddress):
        super().__init__(message)
        self.address = address


class InvalidERC20Info(EthereumClientException):
    pass


class InvalidERC721Info(EthereumClientException):
    pass


class BatchCallException(EthereumClientException):
    pass


class BatchCallFunctionFailed(BatchCallException):
    pass
