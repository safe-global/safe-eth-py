from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from gnosis.eth.constants import (SIGNATURE_R_MAX_VALUE, SIGNATURE_R_MIN_VALUE,
                                  SIGNATURE_S_MAX_VALUE, SIGNATURE_S_MIN_VALUE,
                                  SIGNATURE_V_MAX_VALUE, SIGNATURE_V_MIN_VALUE)
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
        elif v > 30 and self.check_v(v - 4):  # Support eth_sign
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
    to = EthereumAddressField()
    value = serializers.IntegerField(min_value=0)
    data = HexadecimalField(default=None, allow_null=True, allow_blank=True)
    operation = serializers.IntegerField(min_value=0)
    gas_token = EthereumAddressField(default=None, allow_null=True, allow_zero_address=True)

    def validate_operation(self, value):
        try:
            return SafeOperation(value).value
        except ValueError:
            raise ValidationError('Unknown operation')

    def validate(self, data):
        super().validate(data)

        if not data['to'] and not data['data']:
            raise ValidationError('`data` and `to` cannot both be null')

        if not data['to'] and not data['data']:
            raise ValidationError('`data` and `to` cannot both be null')

        if data['operation'] == SafeOperation.CREATE.value:
            raise ValidationError('Operation CREATE not supported. Please use Gnosis Safe CreateLib')
            #  if data['to']:
            #      raise ValidationError('Operation is Create, but `to` was provided')
            #  elif not data['data']:
            #      raise ValidationError('Operation is Create, but not `data` was provided')

        return data


class SafeMultisigTxSerializer(SafeMultisigEstimateTxSerializer):
    """
    DEPRECATED, use `SafeMultisigTxSerializerV1` instead
    """
    safe_tx_gas = serializers.IntegerField(min_value=0)
    data_gas = serializers.IntegerField(min_value=0)
    gas_price = serializers.IntegerField(min_value=0)
    refund_receiver = EthereumAddressField(default=None, allow_null=True, allow_zero_address=True)
    nonce = serializers.IntegerField(min_value=0)


class SafeMultisigTxSerializerV1(SafeMultisigEstimateTxSerializer):
    """
    Version 1.0.0 of the Safe changes `data_gas` to `base_gas`
    """
    safe_tx_gas = serializers.IntegerField(min_value=0)
    base_gas = serializers.IntegerField(min_value=0)
    gas_price = serializers.IntegerField(min_value=0)
    refund_receiver = EthereumAddressField(default=None, allow_null=True, allow_zero_address=True)
    nonce = serializers.IntegerField(min_value=0)
