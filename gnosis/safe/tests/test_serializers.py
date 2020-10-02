from django.test import TestCase

from gnosis.eth.constants import (SIGNATURE_R_MAX_VALUE, SIGNATURE_R_MIN_VALUE,
                                  SIGNATURE_S_MAX_VALUE, SIGNATURE_S_MIN_VALUE)
from gnosis.eth.utils import get_eth_address_with_key

from ..serializers import (SafeMultisigEstimateTxSerializer,
                           SafeSignatureSerializer)


class TestSerializers(TestCase):
    def test_safe_signature_serializer(self):
        for v in [0, 1]:
            self.assertFalse(SafeSignatureSerializer(data={'v': v, 'r': -1, 's': 0}).is_valid())
            self.assertTrue(SafeSignatureSerializer(data={'v': v, 'r': 0, 's': 0}).is_valid())
            self.assertTrue(SafeSignatureSerializer(data={'v': v, 'r': SIGNATURE_R_MAX_VALUE + 1, 's': 0}).is_valid())
            self.assertTrue(SafeSignatureSerializer(data={'v': v, 'r': SIGNATURE_R_MAX_VALUE + 1,
                                                          's': SIGNATURE_S_MAX_VALUE + 1}).is_valid())

        for v in [27, 28]:
            self.assertFalse(SafeSignatureSerializer(data={'v': v, 'r': 0, 's': 0}).is_valid())
            self.assertTrue(SafeSignatureSerializer(data={'v': v, 'r': SIGNATURE_R_MIN_VALUE + 1,
                                                          's': SIGNATURE_S_MAX_VALUE - 1}).is_valid())
            self.assertTrue(SafeSignatureSerializer(data={'v': v, 'r': SIGNATURE_R_MAX_VALUE - 1,
                                                          's': SIGNATURE_S_MIN_VALUE + 1}).is_valid())

            self.assertFalse(SafeSignatureSerializer(data={'v': v, 'r': SIGNATURE_R_MAX_VALUE + 1,
                                                           's': SIGNATURE_S_MAX_VALUE - 1}).is_valid())
            self.assertFalse(SafeSignatureSerializer(data={'v': v, 'r': SIGNATURE_R_MIN_VALUE + 1,
                                                           's': SIGNATURE_S_MAX_VALUE + 1}).is_valid())

    def test_safe_multisig_tx_estimate_serializer(self):
        safe_address, _ = get_eth_address_with_key()
        eth_address, _ = get_eth_address_with_key()
        data = {
            'safe': safe_address,
            'to': None,
            'data': None,
            'value': 1,
            'operation': 0
        }
        serializer = SafeMultisigEstimateTxSerializer(data=data)

        # To and data cannot be empty
        self.assertFalse(serializer.is_valid())

        data = {
            'safe': safe_address,
            'to': eth_address,
            'data': '0x00',
            'value': 1,
            'operation': 2
        }
        serializer = SafeMultisigEstimateTxSerializer(data=data)
        # Operation cannot be contract creation and to set
        self.assertFalse(serializer.is_valid())

        # Create Operation has been disabled
        data = {
            'safe': safe_address,
            'to': None,
            'data': '0x00',
            'value': 1,
            'operation': 2
        }
        serializer = SafeMultisigEstimateTxSerializer(data=data)
        # Operation is not contract creation and to is not empty
        self.assertFalse(serializer.is_valid())
