from django.core.exceptions import ValidationError

from ..utils import fast_is_checksum_address


def validate_checksumed_address(address):
    if not fast_is_checksum_address(address):
        raise ValidationError(
            "%(address)s has an invalid checksum",
            params={"address": address},
        )
