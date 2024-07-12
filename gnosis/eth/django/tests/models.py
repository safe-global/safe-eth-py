from django.db import models

from ..models import (
    EthereumAddressBinaryField,
    EthereumAddressFastBinaryField,
    Keccak256Field,
    Uint32Field,
    Uint96Field,
    Uint256Field,
)


class EthereumAddressBinary(models.Model):
    value = EthereumAddressBinaryField(null=True)


class EthereumAddressFastBinary(models.Model):
    value = EthereumAddressFastBinaryField(null=True)


class Uint256(models.Model):
    value = Uint256Field(null=True)


class Uint96(models.Model):
    value = Uint96Field(null=True)


class Uint32(models.Model):
    value = Uint32Field(null=True)


class Keccak256Hash(models.Model):
    value = Keccak256Field(null=True)
