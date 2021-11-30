from django.db import models

from ..models import (
    EthereumAddressField,
    EthereumAddressV2Field,
    Keccak256Field,
    Sha3HashField,
    Uint256Field,
)


class EthereumAddress(models.Model):
    value = EthereumAddressField(null=True)


class EthereumAddressV2(models.Model):
    value = EthereumAddressV2Field(null=True)


class Uint256(models.Model):
    value = Uint256Field(null=True)


class Sha3Hash(models.Model):
    value = Sha3HashField(null=True)


class Keccak256Hash(models.Model):
    value = Keccak256Field(null=True)
