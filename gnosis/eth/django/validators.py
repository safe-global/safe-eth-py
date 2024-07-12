from django.core.exceptions import ValidationError

from hexbytes import HexBytes

from ..utils import fast_is_checksum_address


def validate_address(address: str):
    try:
        address_bytes = HexBytes(address)
        if len(address_bytes) != 20:
            raise ValueError
    except ValueError:
        raise ValidationError(
            "%(address)s is not a valid EthereumAddress",
            params={"address": address},
        )


def validate_checksumed_address(address: str):
    if not fast_is_checksum_address(address):
        raise ValidationError(
            "%(address)s has an invalid checksum",
            params={"address": address},
        )
