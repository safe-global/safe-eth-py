from unittest import TestCase
from unittest.mock import patch

from eth_typing import ChecksumAddress
from hexbytes import HexBytes

from gnosis.safe.api.transaction_service_api.transaction_service_messages import (
    get_delegate_message,
    get_remove_transaction_message,
    get_totp,
)


class TestTransactionServiceMessages(TestCase):
    def test_get_totp(self):
        mocked_time = 1615974000
        with patch("time.time", return_value=mocked_time):
            totp = get_totp()

        expected_totp = mocked_time // 3600
        self.assertEqual(totp, expected_totp)

    def test_get_delegate_message(self):
        chain_id = 1
        mocked_totp = 123
        delegate_address = ChecksumAddress("0x1234567890123456789012345678901234567890")

        expected_message = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                ],
                "Delegate": [
                    {"name": "delegateAddress", "type": "address"},
                    {"name": "totp", "type": "uint256"},
                ],
            },
            "primaryType": "Delegate",
            "domain": {
                "name": "Safe Transaction Service",
                "version": "1.0",
                "chainId": chain_id,
            },
            "message": {
                "delegateAddress": delegate_address,
                "totp": mocked_totp,
            },
        }

        with patch(
            "gnosis.safe.api.transaction_service_api.transaction_service_messages.get_totp",
            return_value=mocked_totp,
        ):
            message = get_delegate_message(delegate_address, chain_id)

        self.assertEqual(message, expected_message)

    def test_get_remove_transaction_message(self):
        chain_id = 1
        mocked_totp = 123
        delegate_address = ChecksumAddress("0x1234567890123456789012345678901234567890")
        safe_address = ChecksumAddress("0x1234567890123456789012345678901234567890")

        safe_tx_hash = HexBytes(
            "0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196"
        )

        expected_message = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "DeleteRequest": [
                    {"name": "safeTxHash", "type": "bytes32"},
                    {"name": "totp", "type": "uint256"},
                ],
            },
            "primaryType": "DeleteRequest",
            "domain": {
                "name": "Safe Transaction Service",
                "version": "1.0",
                "chainId": chain_id,
                "verifyingContract": safe_address,
            },
            "message": {
                "safeTxHash": safe_tx_hash,
                "totp": mocked_totp,
            },
        }

        with patch(
            "gnosis.safe.api.transaction_service_api.transaction_service_messages.get_totp",
            return_value=mocked_totp,
        ):
            message = get_remove_transaction_message(
                delegate_address, safe_tx_hash, chain_id
            )

        self.assertEqual(message, expected_message)
