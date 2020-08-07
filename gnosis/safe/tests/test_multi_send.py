import logging

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes

from ..multi_send import MultiSend, MultiSendOperation, MultiSendTx
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
        self.assertEqual(new_multi_send_tx.to, address)
        self.assertEqual(new_multi_send_tx.value, value)
        self.assertEqual(new_multi_send_tx.data, data)
        self.assertTrue(str(new_multi_send_tx))  # Test __str__

    def test_multi_send_from_bytes(self):
        encoded_multisend_txs = b''
        values = [876 * i for i in range(3)]
        datas = [HexBytes('0x123456789a') * i for i in range(3)]
        for value, data in zip(values, datas):  # Craft the same transaction three times
            operation = MultiSendOperation.DELEGATE_CALL
            address = Account.create().address
            multi_send_tx = MultiSendTx(operation, address, value, data)
            new_multi_send_tx = MultiSendTx.from_bytes(multi_send_tx.encoded_data)

            self.assertEqual(new_multi_send_tx, multi_send_tx)
            self.assertEqual(new_multi_send_tx.operation, operation)
            self.assertEqual(new_multi_send_tx.to, address)
            self.assertEqual(new_multi_send_tx.value, value)
            self.assertEqual(new_multi_send_tx.data, data)
            encoded_multisend_txs += multi_send_tx.encoded_data

        multisend_txs = MultiSend.from_bytes(encoded_multisend_txs)
        self.assertEqual(len(multisend_txs), 3)
        for multi_send_tx, value, data in zip(multisend_txs, values, datas):
            self.assertEqual(multi_send_tx.value, value)
            self.assertEqual(multi_send_tx.data, data)

    def test_multisend_parse_real_transaction(self):
        # Change Safe contract master copy and set fallback manager multisend transaction
        safe_contract_address = '0x5B9ea52Aaa931D4EEf74C8aEaf0Fe759434FeD74'
        data = HexBytes('0x8d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000'
                        '00000000000000000000000000000000000000000000f2005b9ea52aaa931d4eef74c8aeaf0fe759434fed740000'
                        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                        '000000000000000000000000000000247de7edef00000000000000000000000034cfac646f301356faa8b21e9422'
                        '7e3583fe3f5f005b9ea52aaa931d4eef74c8aeaf0fe759434fed7400000000000000000000000000000000000000'
                        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000024f0'
                        '8a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf440000000000000000000000'
                        '000000')
        change_master_copy_data = HexBytes('0x7de7edef00000000000000000000000034cfac646f301356faa8b21e94227e3583fe3f5f')
        change_fallback_manager_data = HexBytes('0xf08a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cd'
                                                'bdf44')
        multisend_txs = MultiSend.from_transaction_data(data)
        self.assertEqual(len(multisend_txs), 2)
        for multisend_tx, expected_data in zip(multisend_txs, (change_master_copy_data, change_fallback_manager_data)):
            self.assertEqual(multisend_tx.to, safe_contract_address)
            self.assertEqual(multisend_tx.data, expected_data)
            self.assertEqual(multisend_tx.value, 0)

    def test_multisend_parse_invalid_transaction(self):
        # Remove some data but keep the selector
        data = HexBytes('0x8d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000'
                        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                        '000000000000000000000000000000247de7edef00000000000000000000000034cfac646f301356faa8b21e9422'
                        '7e3583fe3f5f005b9ea52aaa931d4eef74c8aeaf0fe759434fed7400000000000000000000000000000000000000'
                        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000024f0'
                        '8a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf440000000000000000000000'
                        '000000')
        multisend_txs = MultiSend.from_transaction_data(data)
        self.assertEqual(multisend_txs, [])

        # Keep the data but change the selector
        data = HexBytes('0x1d80ff0a0000000000000000000000000000000000000000000000000000000000000020000000000000000000'
                        '00000000000000000000000000000000000000000000f2005b9ea52aaa931d4eef74c8aeaf0fe759434fed740000'
                        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                        '000000000000000000000000000000247de7edef00000000000000000000000034cfac646f301356faa8b21e9422'
                        '7e3583fe3f5f005b9ea52aaa931d4eef74c8aeaf0fe759434fed7400000000000000000000000000000000000000'
                        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000024f0'
                        '8a0323000000000000000000000000d5d82b6addc9027b22dca772aa68d5d74cdbdf440000000000000000000000'
                        '000000')
        multisend_txs = MultiSend.from_transaction_data(data)
        self.assertEqual(multisend_txs, [])
