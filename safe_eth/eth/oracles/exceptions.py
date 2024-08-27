class OracleException(Exception):
    pass


class InvalidPriceFromOracle(OracleException):
    pass


class CannotGetPriceFromOracle(OracleException):
    pass
