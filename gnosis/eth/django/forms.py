import binascii
from typing import Any, Optional

from django import forms
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from hexbytes import HexBytes

from gnosis.eth.utils import fast_is_checksum_address


class EthereumAddressFieldForm(forms.CharField):
    default_error_messages = {
        "invalid": _("Enter a valid checksummed Ethereum Address."),
    }

    def prepare_value(self, value):
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        elif not fast_is_checksum_address(value):
            raise ValidationError(self.error_messages["invalid"], code="invalid")
        return value


class HexFieldForm(forms.CharField):
    default_error_messages = {
        "invalid": _("Enter a valid hexadecimal."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_value = None

    def prepare_value(self, value: memoryview) -> str:
        if value:
            return "0x" + bytes(value).hex()
        else:
            return ""

    def to_python(self, value: Optional[Any]) -> Optional[HexBytes]:
        if value in self.empty_values:
            return self.empty_value
        try:
            if isinstance(value, str):
                value = value.strip()
            return HexBytes(value)
        except (binascii.Error, TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )


class Keccak256FieldForm(HexFieldForm):
    default_error_messages = {
        "invalid": _('"%(value)s" is not a valid keccak256 hash.'),
        "length": _('"%(value)s" keccak256 hash should be 32 bytes.'),
    }

    def prepare_value(self, value: str) -> str:
        # Keccak field already returns a hex str
        return value

    def to_python(self, value: Optional[Any]) -> HexBytes:
        value: Optional[HexBytes] = super().to_python(value)
        if value and len(value) != 32:
            raise ValidationError(
                self.error_messages["length"],
                code="length",
                params={"value": value.hex()},
            )
        return value
