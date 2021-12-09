import binascii

from django.core.exceptions import ValidationError
from django.forms import CharField as CharFieldForm
from django.utils.translation import gettext_lazy as _

import django_filters
from hexbytes import HexBytes
from web3 import Web3


class EthereumAddressFieldForm(CharFieldForm):
    default_error_messages = {
        "invalid": _("Enter a valid checksummed Ethereum Address."),
    }

    def prepare_value(self, value):
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        elif not Web3.isChecksumAddress(value):
            raise ValidationError(self.error_messages["invalid"], code="invalid")
        return value


class EthereumAddressFilter(django_filters.Filter):
    field_class = EthereumAddressFieldForm


class Keccak256FieldForm(CharFieldForm):
    default_error_messages = {
        "invalid": _('"%(value)s" is not a valid keccak256 hash.'),
        "length": _('"%(value)s" keccak256 hash should be 32 bytes.'),
    }

    def prepare_value(self, value):
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        else:
            try:
                bytes_value = HexBytes(value)
                if len(bytes_value) != 32:
                    raise ValidationError(
                        self.error_messages["length"],
                        code="length",
                        params={"value": value},
                    )
            except (binascii.Error, ValueError):
                raise ValidationError(
                    self.error_messages["invalid"],
                    code="invalid",
                    params={"value": value},
                )
        return value


class Keccak256Filter(django_filters.Filter):
    field_class = Keccak256FieldForm
