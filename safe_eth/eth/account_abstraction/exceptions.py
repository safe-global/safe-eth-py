class BundlerClientException(ValueError):
    pass


class BundlerClientConnectionException(BundlerClientException, IOError):
    pass


class BundlerClientResponseException(BundlerClientException):
    pass
