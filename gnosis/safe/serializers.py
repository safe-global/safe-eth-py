from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from gnosis.eth.constants import *
from gnosis.eth.django.serializers import (EthereumAddressField,
                                           HexadecimalField)

from .safe import SafeOperation


class SafeSignatureSerializer(serializers.Serializer):
    """
    When using safe signatures `v` can have more values
    """
    v = serializers.IntegerField(min_value=0)
    r = serializers.IntegerField(min_value=0)
    s = serializers.IntegerField(min_value=0)

    def validate_v(self, v):
        if v == 0:  # Contract signature
            return v
        elif v == 1:  # Approved hash
            return v
        elif self.check_v(v):
            return v
        else:
            raise serializers.ValidationError("v should be 0, 1 or be in %d-%d" % (SIGNATURE_V_MIN_VALUE,
                                                                                   SIGNATURE_V_MAX_VALUE))

    def validate(self, data):
        super().validate(data)

        v = data['v']
        r = data['r']
        s = data['s']

        if v not in [0, 1]:  # Disable checks for `r` and `s` if v is 0 or 1
            if not self.check_r(r):
                raise serializers.ValidationError("r not valid")
            elif not self.check_s(s):
                raise serializers.ValidationError("s not valid")
        return data

    def check_v(self, v):
        return SIGNATURE_V_MIN_VALUE <= v <= SIGNATURE_V_MAX_VALUE

    def check_r(self, r):
        return SIGNATURE_R_MIN_VALUE <= r <= SIGNATURE_R_MAX_VALUE

    def check_s(self, s):
        return SIGNATURE_S_MIN_VALUE <= s <= SIGNATURE_S_MAX_VALUE


class SafeMultisigEstimateTxSerializer(serializers.Serializer):
    safe = EthereumAddressField()
    to = EthereumAddressField(default=None, allow_null=True)
    value = serializers.IntegerField(min_value=0)
    data = HexadecimalField(default=None, allow_null=True, allow_blank=True)
    operation = serializers.IntegerField(min_value=0)
    gas_token = EthereumAddressField(default=None, allow_null=True, allow_zero_address=True)

    def validate_operation(self, value):
        try:
            SafeOperation(value)
            return value
        except ValueError:
            raise ValidationError('Unknown operation')

    def validate(self, data):
        super().validate(data)

        if not data['to'] and not data['data']:
            raise ValidationError('`data` and `to` cannot both be null')

        if not data['to'] and not data['data']:
            raise ValidationError('`data` and `to` cannot both be null')

        if data['operation'] == SafeOperation.CREATE.value:
            if data['to']:
                raise ValidationError('Operation is Create, but `to` was provided')
            elif not data['data']:
                raise ValidationError('Operation is Create, but not `data` was provided')
        elif not data['to']:
            raise ValidationError('Operation is not Create, but `to` was not provided')

        return data


class SafeMultisigTxSerializer(SafeMultisigEstimateTxSerializer):
    safe_tx_gas = serializers.IntegerField(min_value=0)
    data_gas = serializers.IntegerField(min_value=0)
    gas_price = serializers.IntegerField(min_value=0)
    refund_receiver = EthereumAddressField(default=None, allow_null=True, allow_zero_address=True)
    nonce = serializers.IntegerField(min_value=0)
