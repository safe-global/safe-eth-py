from django.test import TestCase

from eth_account import Account

from ..serializers import SafeMultisigEstimateTxSerializer


class TestSerializers(TestCase):
    def test_safe_multisig_tx_estimate_serializer(self):
        safe_address = Account.create().address
        eth_address = Account.create().address
        data = {
            "safe": safe_address,
            "to": None,
            "data": None,
            "value": 1,
            "operation": 0,
        }
        serializer = SafeMultisigEstimateTxSerializer(data=data)

        # To and data cannot be empty
        self.assertFalse(serializer.is_valid())

        data = {
            "safe": safe_address,
            "to": eth_address,
            "data": "0x00",
            "value": 1,
            "operation": 2,
        }
        serializer = SafeMultisigEstimateTxSerializer(data=data)
        # Operation cannot be contract creation and to set
        self.assertFalse(serializer.is_valid())

        # Create Operation has been disabled
        data = {
            "safe": safe_address,
            "to": None,
            "data": "0x00",
            "value": 1,
            "operation": 2,
        }
        serializer = SafeMultisigEstimateTxSerializer(data=data)
        # Operation is not contract creation and to is not empty
        self.assertFalse(serializer.is_valid())
