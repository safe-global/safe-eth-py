class SafeServiceException(Exception):
    pass


class CannotEstimateGas(SafeServiceException):
    pass


class CannotRetrieveSafeInfoException(SafeServiceException):
    pass


class InvalidChecksumAddress(SafeServiceException):
    pass


class InvalidPaymentToken(SafeServiceException):
    pass


class InvalidMultisigTx(SafeServiceException):
    pass


class InvalidInternalTx(InvalidMultisigTx):
    pass


class SignatureNotProvidedByOwner(InvalidMultisigTx):
    pass


class SignaturesDataTooShort(InvalidMultisigTx):
    pass


class InvalidOwnerProvided(InvalidMultisigTx):
    pass


class InvalidSignaturesProvided(InvalidMultisigTx):
    pass


class CouldNotPayGasWithEther(InvalidMultisigTx):
    pass


class CouldNotPayGasWithToken(InvalidMultisigTx):
    pass


class HashHasNotBeenApproved(InvalidMultisigTx):
    pass


class NotEnoughSafeTransactionGas(InvalidMultisigTx):
    pass


class InvalidContractSignatureLocation(InvalidMultisigTx):
    pass


class OnlyOwnersCanApproveAHash(InvalidMultisigTx):
    pass


class OwnerManagerException(InvalidMultisigTx):
    pass


class ModuleManagerException(InvalidMultisigTx):
    pass
