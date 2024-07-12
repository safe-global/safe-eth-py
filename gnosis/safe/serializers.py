from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from gnosis.eth.django.serializers import EthereumAddressField, HexadecimalField

from .enums import SafeOperationEnum


class SafeMultisigEstimateTxSerializer(serializers.Serializer):
    safe = EthereumAddressField()
    to = EthereumAddressField()
    value = serializers.IntegerField(min_value=0)
    data = HexadecimalField(default=None, allow_null=True, allow_blank=True)
    operation = serializers.IntegerField(min_value=0)
    gas_token = EthereumAddressField(
        default=None, allow_null=True, allow_zero_address=True
    )

    def validate_operation(self, value):
        try:
            return SafeOperationEnum(value).value
        except ValueError:
            raise ValidationError("Unknown operation")

    def validate(self, data):
        super().validate(data)

        if not data["to"] and not data["data"]:
            raise ValidationError("`data` and `to` cannot both be null")

        if not data["to"] and not data["data"]:
            raise ValidationError("`data` and `to` cannot both be null")

        if data["operation"] == SafeOperationEnum.CREATE.value:
            raise ValidationError(
                "Operation CREATE not supported. Please use Gnosis Safe CreateLib"
            )
            #  if data['to']:
            #      raise ValidationError('Operation is Create, but `to` was provided')
            #  elif not data['data']:
            #      raise ValidationError('Operation is Create, but not `data` was provided')

        return data


class SafeMultisigTxSerializer(SafeMultisigEstimateTxSerializer):
    safe_tx_gas = serializers.IntegerField(min_value=0)
    base_gas = serializers.IntegerField(min_value=0)
    gas_price = serializers.IntegerField(min_value=0)
    refund_receiver = EthereumAddressField(
        default=None, allow_null=True, allow_zero_address=True
    )
    nonce = serializers.IntegerField(min_value=0)
