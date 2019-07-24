import logging

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes

from ..multi_send import MultiSendOperation, MultiSendTx
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestMultiSend(SafeTestCaseMixin, TestCase):
    def test_multi_send_tx_from_bytes(self):
        operation = MultiSendOperation.DELEGATE_CALL
        address = Account.create().address
        value = 876
        data = HexBytes('0x123456789a')
        multi_send_tx = MultiSendTx(operation, address, value, data)
        new_multi_send_tx = MultiSendTx.from_bytes(multi_send_tx.encoded_data)

        self.assertEqual(new_multi_send_tx, multi_send_tx)
        self.assertEqual(new_multi_send_tx.operation, operation)
        self.assertEqual(new_multi_send_tx.address, address)
        self.assertEqual(new_multi_send_tx.value, value)
        self.assertEqual(new_multi_send_tx.data, data)
