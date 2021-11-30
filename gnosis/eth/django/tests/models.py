from django.db import models

from ..models import (
    EthereumAddressField,
    EthereumAddressV2Field,
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
