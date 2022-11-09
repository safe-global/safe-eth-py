from unittest import TestCase

from gnosis.eth.eip712 import eip712_encode_hash


class TestEIP712(TestCase):
    def test_eip712_encode_hash(self):
        for value in [
            {},
            None,
        ]:
            with self.assertRaises(ValueError):
                eip712_encode_hash(value)

        address = "0x8e12f01dae5fe7f1122dc42f2cb084f2f9e8aa03"

        wrong_types = {
            "EIP712Domain": [
                {"name": "name", "type": "stringa"},
                {"name": "version", "type": "bstring"},
                {"name": "chainId", "type": "aaauint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Mailbox": [
                {"name": "owner", "type": "address"},
                {"name": "messages", "type": "Message[]"},
            ],
            "Message": [
                {"name": "sender", "type": "address"},
                {"name": "subject", "type": "string"},
                {"name": "isSpam", "type": "bool"},
                {"name": "body", "type": "string"},
            ],
        }

        types = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Mailbox": [
                {"name": "owner", "type": "address"},
                {"name": "messages", "type": "Message[]"},
            ],
            "Message": [
                {"name": "sender", "type": "address"},
                {"name": "subject", "type": "string"},
                {"name": "isSpam", "type": "bool"},
                {"name": "body", "type": "string"},
            ],
        }

        msgs = [
            {
                "sender": address,
                "subject": "Hello World",
                "body": "The sparrow flies at midnight.",
                "isSpam": False,
            },
            {
                "sender": address,
                "subject": "You may have already Won! :dumb-emoji:",
                "body": "Click here for sweepstakes!",
                "isSpam": True,
            },
        ]

        mailbox = {"owner": address, "messages": msgs}

        payload = {
            "types": wrong_types,
            "primaryType": "Mailbox",
            "domain": {
                "name": "MyDApp",
                "version": "3.0",
                "chainId": 41,
                "verifyingContract": address,
            },
            "message": mailbox,
        }

        with self.assertRaises(ValueError):
            eip712_encode_hash(payload)

        payload["types"] = types
        self.assertEqual(
            eip712_encode_hash(payload),
            b"\xd5N\xcbf7\xfa\x99\n\xae\x02\x86\xd4 \xacpe\x8d\xb9\x95\xaem\t\xcc\x9b\xb1\xda\xcf6J\x14\x17\xd0",
        )
