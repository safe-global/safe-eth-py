from unittest import TestCase

from gnosis.eth.eip712 import eip712_encode_hash


class TestEIP712(TestCase):
    address = "0x8e12f01dae5fe7f1122dc42f2cb084f2f9e8aa03"
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

    def test_eip712_encode_hash(self):
        for value in [
            {},
            None,
        ]:
            with self.assertRaises(ValueError):
                eip712_encode_hash(value)

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

        payload = {
            "types": wrong_types,
            "primaryType": "Mailbox",
            "domain": {
                "name": "MyDApp",
                "version": "3.0",
                "chainId": 41,
                "verifyingContract": self.address,
            },
            "message": self.mailbox,
        }

        with self.assertRaises(ValueError):
            eip712_encode_hash(payload)

        payload["types"] = self.types
        self.assertEqual(
            eip712_encode_hash(payload),
            b"\xd5N\xcbf7\xfa\x99\n\xae\x02\x86\xd4 \xacpe\x8d\xb9\x95\xaem\t\xcc\x9b\xb1\xda\xcf6J\x14\x17\xd0",
        )

    def test_eip712_encode_hash_string_uint(self):
        # test string uint (chainId)
        payload = {
            "types": self.types,
            "primaryType": "Mailbox",
            "domain": {
                "name": "MyDApp",
                "version": "3.0",
                "chainId": "41",
                "verifyingContract": self.address,
            },
            "message": self.mailbox,
        }

        self.assertEqual(
            eip712_encode_hash(payload),
            b"\xd5N\xcbf7\xfa\x99\n\xae\x02\x86\xd4 \xacpe\x8d\xb9\x95\xaem\t\xcc\x9b\xb1\xda\xcf6J\x14\x17\xd0",
        )

    def test_eip712_encode_hash_string_bytes(self):
        types_with_bytes = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
            ],
            "Message": [
                {"name": "oneByte", "type": "bytes1"},
                {"name": "maxByte", "type": "bytes32"},
            ],
        }
        payload = {
            "types": types_with_bytes,
            "primaryType": "Message",
            "domain": {
                "name": "MyDApp",
            },
            "message": {
                "oneByte": "0x01",
                "maxByte": "0x6214da6089b8d8aaa6e6268977746aa0af19fd1ef5d56e225bb3390a697c3ec1",
            },
        }

        self.assertEqual(
            eip712_encode_hash(payload).hex(),
            "2950cf06416c6c20059f24a965e3baf51a24f4ef49a1e7b1a47ee13ee08cde1f",
        )
