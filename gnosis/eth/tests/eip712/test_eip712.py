from unittest import TestCase

from gnosis.eth.eip712 import eip712_encode_hash


class TestEIP712(TestCase):
    address = "0x8e12f01DAE5FE7f1122Dc42f2cB084F2f9E8aA03"
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
            eip712_encode_hash(payload).hex(),
            "7c02fe79823722257b42ea95720e7dd31d51c3f6769dc0f56a271800dd030ef1",
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
            eip712_encode_hash(payload).hex(),
            "7c02fe79823722257b42ea95720e7dd31d51c3f6769dc0f56a271800dd030ef1",
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

    def test_eip712_encode_nested_with_array(self):
        payload = {
            "types": {
                "Nested": [
                    {"name": "nestedString", "type": "string"},
                    {"name": "nestedAddress", "type": "address"},
                    {"name": "nestedUint256", "type": "uint256"},
                    {"name": "nestedUint32", "type": "uint32"},
                    {"name": "nestedBytes32", "type": "bytes32"},
                    {"name": "nestedBoolean", "type": "bool"},
                ],
                "Example": [
                    {"name": "testString", "type": "string"},
                    {"name": "testAddress", "type": "address"},
                    {"name": "testUint256", "type": "uint256"},
                    {"name": "testUint32", "type": "uint32"},
                    {"name": "testBytes32", "type": "bytes32"},
                    {"name": "testBoolean", "type": "bool"},
                    {"name": "testNested", "type": "Nested"},
                    {"name": "testNestedArray", "type": "Nested[]"},
                ],
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
            },
            "domain": {
                "name": "EIP-1271 Example DApp",
                "version": "1.0",
                "chainId": "5",
                "verifyingContract": "0xaecdfd3a19f777f0c03e6bf99aafb59937d6467b",
            },
            "primaryType": "Example",
            "message": {
                "testString": "Hello Deeeeeemo",
                "testAddress": "0xaecdfd3a19f777f0c03e6bf99aafb59937d6467b",
                "testUint256": "115792089237316195423570985008687907853269984665640564039457584007908834671663",
                "testUint32": "123",
                "testBytes32": "0x00000000000000000000000000000000000000000000000000000000deadbeef",
                "testBoolean": True,
                "testNested": {
                    "nestedString": "Hello Deeeeeemo",
                    "nestedAddress": "0x0000000000000000000000000000000000000002",
                    "nestedUint256": "0",
                    "nestedUint32": "1",
                    "nestedBytes32": "0x000000000000000000000000000000000000000000000000000000000000da7a",
                    "nestedBoolean": False,
                },
                "testNestedArray": [
                    {
                        "nestedString": "Hello Deeeeeemo",
                        "nestedAddress": "0x0000000000000000000000000000000000000002",
                        "nestedUint256": "0",
                        "nestedUint32": "1",
                        "nestedBytes32": "0x000000000000000000000000000000000000000000000000000000000000da7a",
                        "nestedBoolean": False,
                    },
                    {
                        "nestedString": "Hello Deeeeeemo",
                        "nestedAddress": "0x0000000000000000000000000000000000000002",
                        "nestedUint256": "0",
                        "nestedUint32": "1",
                        "nestedBytes32": "0x000000000000000000000000000000000000000000000000000000000000da7a",
                        "nestedBoolean": False,
                    },
                ],
            },
        }
        self.assertEqual(
            eip712_encode_hash(payload).hex(),
            "2f6856dbd51836973c1e61852b64949556aa2e7f253d9e20e682f9a02d436791",
        )

    def test_eip712_encode_nested_with_empty_array(self):
        payload = {
            "types": {
                "Nested": [
                    {"name": "nestedString", "type": "string"},
                    {"name": "nestedAddress", "type": "address"},
                    {"name": "nestedUint256", "type": "uint256"},
                    {"name": "nestedUint32", "type": "uint32"},
                    {"name": "nestedBytes32", "type": "bytes32"},
                    {"name": "nestedBoolean", "type": "bool"},
                ],
                "Example": [
                    {"name": "testString", "type": "string"},
                    {"name": "testAddress", "type": "address"},
                    {"name": "testUint256", "type": "uint256"},
                    {"name": "testUint32", "type": "uint32"},
                    {"name": "testBytes32", "type": "bytes32"},
                    {"name": "testBoolean", "type": "bool"},
                    {"name": "testNested", "type": "Nested"},
                    {"name": "testNestedArray", "type": "Nested[]"},
                ],
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
            },
            "domain": {
                "name": "EIP-1271 Example DApp",
                "version": "1.0",
                "chainId": "5",
                "verifyingContract": "0xaecdfd3a19f777f0c03e6bf99aafb59937d6467b",
            },
            "primaryType": "Example",
            "message": {
                "testString": "Hello Deeeeeemo",
                "testAddress": "0xaecdfd3a19f777f0c03e6bf99aafb59937d6467b",
                "testUint256": "115792089237316195423570985008687907853269984665640564039457584007908834671663",
                "testUint32": "123",
                "testBytes32": "0x00000000000000000000000000000000000000000000000000000000deadbeef",
                "testBoolean": True,
                "testNested": {
                    "nestedString": "Hello Deeeeeemo",
                    "nestedAddress": "0x0000000000000000000000000000000000000002",
                    "nestedUint256": "0",
                    "nestedUint32": "1",
                    "nestedBytes32": "0x000000000000000000000000000000000000000000000000000000000000da7a",
                    "nestedBoolean": False,
                },
                "testNestedArray": [],
            },
        }
        self.assertEqual(
            eip712_encode_hash(payload).hex(),
            "5dd3156111fb5e400606d4dd75ff097e36eb56614c84924b5eb6d1cf1b5038cf",
        )

    def test_eip712_encode_nested_without_array(self):
        payload = {
            "types": {
                "Nested": [
                    {"name": "nestedString", "type": "string"},
                    {"name": "nestedAddress", "type": "address"},
                    {"name": "nestedUint256", "type": "uint256"},
                    {"name": "nestedUint32", "type": "uint32"},
                    {"name": "nestedBytes32", "type": "bytes32"},
                    {"name": "nestedBoolean", "type": "bool"},
                ],
                "Example": [
                    {"name": "testString", "type": "string"},
                    {"name": "testAddress", "type": "address"},
                    {"name": "testUint256", "type": "uint256"},
                    {"name": "testUint32", "type": "uint32"},
                    {"name": "testBytes32", "type": "bytes32"},
                    {"name": "testBoolean", "type": "bool"},
                    {"name": "testNested", "type": "Nested"},
                ],
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
            },
            "domain": {
                "name": "EIP-1271 Example DApp",
                "version": "1.0",
                "chainId": "5",
                "verifyingContract": "0xaecdfd3a19f777f0c03e6bf99aafb59937d6467b",
            },
            "primaryType": "Example",
            "message": {
                "testString": "Hello Deeeeeemo",
                "testAddress": "0xaecdfd3a19f777f0c03e6bf99aafb59937d6467b",
                "testUint256": "115792089237316195423570985008687907853269984665640564039457584007908834671663",
                "testUint32": "123",
                "testBytes32": "0x00000000000000000000000000000000000000000000000000000000deadbeef",
                "testBoolean": True,
                "testNested": {
                    "nestedString": "Hello Deeeeeemo",
                    "nestedAddress": "0x0000000000000000000000000000000000000002",
                    "nestedUint256": "0",
                    "nestedUint32": "1",
                    "nestedBytes32": "0x000000000000000000000000000000000000000000000000000000000000da7a",
                    "nestedBoolean": False,
                },
            },
        }

        self.assertEqual(
            eip712_encode_hash(payload).hex(),
            "9a55335a1d86221594e96018fc3df611a1485d95b5b2afbef1540ac51f63d249",
        )
