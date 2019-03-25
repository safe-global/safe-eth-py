class SafeServiceException(Exception):
    pass


class GasPriceTooLow(SafeServiceException):
    pass


class CannotEstimateGas(SafeServiceException):
    pass


class InvalidChecksumAddress(SafeServiceException):
    pass


class InvalidPaymentToken(SafeServiceException):
    pass


class InvalidMultisigTx(SafeServiceException):
    pass


class InvalidInternalTx(InvalidMultisigTx):
    pass


class InvalidGasEstimation(InvalidMultisigTx):
    pass


class SignatureNotProvidedByOwner(InvalidMultisigTx):
    pass


class SignaturesDataTooShort(InvalidMultisigTx):
    pass


class InvalidSignaturesProvided(InvalidMultisigTx):
    pass


class CouldNotPayGasWithEther(InvalidMultisigTx):
    pass


class CouldNotPayGasWithToken(InvalidMultisigTx):
    pass


class HashHasNotBeenApproved(InvalidMultisigTx):
    pass
