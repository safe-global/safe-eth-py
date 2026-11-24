import os
import time
from typing import Any
from unittest import TestCase, mock

from eth_abi.registry import registry as default_abi_registry

from safe_eth.eth.eip712 import (
    _MAX_FIELD_TYPE_LENGTH,
    _TypedDataEncoder,
    eip712_encode_hash,
    hash_struct,
)
from safe_eth.eth.utils import fast_keccak
from safe_eth.util.util import to_0x_hex_str

# Dimensions of the longest uint256 array type that fits in the max field type length
_MAX_ARRAY_DIMENSIONS = (_MAX_FIELD_TYPE_LENGTH - len("uint256")) // len("[]")


def _build_nested_list(dimensions: int) -> Any:
    """
    :return: ``1`` nested in ``dimensions`` lists
    """
    nested_list: Any = 1
    for _ in range(dimensions):
        nested_list = [nested_list]
    return nested_list


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
            to_0x_hex_str(eip712_encode_hash(payload)),
            "0x7c02fe79823722257b42ea95720e7dd31d51c3f6769dc0f56a271800dd030ef1",
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
            to_0x_hex_str(eip712_encode_hash(payload)),
            "0x7c02fe79823722257b42ea95720e7dd31d51c3f6769dc0f56a271800dd030ef1",
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
            to_0x_hex_str(eip712_encode_hash(payload)),
            "0x2950cf06416c6c20059f24a965e3baf51a24f4ef49a1e7b1a47ee13ee08cde1f",
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
            to_0x_hex_str(eip712_encode_hash(payload)),
            "0x2f6856dbd51836973c1e61852b64949556aa2e7f253d9e20e682f9a02d436791",
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
            to_0x_hex_str(eip712_encode_hash(payload)),
            "0x5dd3156111fb5e400606d4dd75ff097e36eb56614c84924b5eb6d1cf1b5038cf",
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
            to_0x_hex_str(eip712_encode_hash(payload)),
            "0x9a55335a1d86221594e96018fc3df611a1485d95b5b2afbef1540ac51f63d249",
        )

    @staticmethod
    def _build_typed_data(
        types: dict[str, Any], primary_type: str, message: Any
    ) -> dict[str, Any]:
        return {
            "types": {
                "EIP712Domain": [{"name": "name", "type": "string"}],
                **types,
            },
            "primaryType": primary_type,
            "domain": {"name": "MyDApp"},
            "message": message,
        }

    def test_eip712_encode_hash_invalid_values(self):
        """
        Invalid values and type definitions raise ValueError, including the errors
        raised by eth_abi
        """
        invalid_field_types_and_values = [
            ("uint8", 256),
            ("uint8", 1.5),
            ("uint8", None),
            ("bool", "yes"),
            ("address", "0x12"),
            ("uint8[", []),
            ("uint8[]", 1),
            ("(uint256)", [1]),
            ("(uint256)[]", [[1]]),
            (
                "uint256" + "[]" * (_MAX_ARRAY_DIMENSIONS + 1),
                _build_nested_list(_MAX_ARRAY_DIMENSIONS + 1),
            ),
        ]
        invalid_types_and_values: list[tuple[dict[str, Any], dict[str, Any]]] = [
            (
                {"Message": [{"name": "value", "type": field_type}]},
                {"value": field_value},
            )
            for field_type, field_value in invalid_field_types_and_values
        ]
        invalid_types_and_values += [
            ({"Message": []}, {}),
            (
                {"Message": [{"name": "value", "type": "Empty"}], "Empty": []},
                {"value": None},
            ),
        ]
        for types, message in invalid_types_and_values:
            with self.subTest(types=types, message=message):
                with self.assertRaises(ValueError):
                    eip712_encode_hash(
                        self._build_typed_data(types, "Message", message)
                    )

    def test_eip712_encode_null_struct(self):
        """
        A null struct, alone or in an array, is encoded as a zero word
        """
        types = {
            "Group": [
                {"name": "leader", "type": "Person"},
                {"name": "members", "type": "Person[]"},
            ],
            "Person": [{"name": "name", "type": "string"}],
        }
        group_type_hash = fast_keccak(
            b"Group(Person leader,Person[] members)Person(string name)"
        )
        self.assertEqual(
            hash_struct("Group", {"leader": None, "members": [None]}, types),
            fast_keccak(group_type_hash + bytes(32) + fast_keccak(bytes(32))),
        )

    def test_eip712_encode_hash_bytearray(self):
        """
        A bytearray value of a bytes field is hashed like bytes
        """
        types = {"Message": [{"name": "value", "type": "bytes"}]}
        value = os.urandom(32)
        self.assertEqual(
            eip712_encode_hash(
                self._build_typed_data(types, "Message", {"value": bytearray(value)})
            ),
            eip712_encode_hash(
                self._build_typed_data(types, "Message", {"value": value})
            ),
        )

    def test_eip712_encode_max_field_type_length(self):
        """
        An array with as many dimensions as fit in the max field type length is
        hashed
        """
        field_type = "uint256" + "[]" * _MAX_ARRAY_DIMENSIONS
        types = {"Message": [{"name": "value", "type": field_type}]}
        # Each array is hashed from the hashes of its elements
        encoded_value = (1).to_bytes(32, "big")
        for _ in range(_MAX_ARRAY_DIMENSIONS):
            encoded_value = fast_keccak(encoded_value)
        self.assertEqual(
            hash_struct(
                "Message", {"value": _build_nested_list(_MAX_ARRAY_DIMENSIONS)}, types
            ),
            fast_keccak(
                fast_keccak(f"Message({field_type} value)".encode()) + encoded_value
            ),
        )

    def test_eip712_encode_hash_type_hashed_once(self):
        """
        Each struct type is encoded once per call, not once per instance
        """
        types = {
            "Mailbox": [{"name": "messages", "type": "Message[]"}],
            "Message": [
                {"name": "sender", "type": "Person"},
                {"name": "body", "type": "string"},
            ],
            "Person": [{"name": "wallet", "type": "address"}],
        }
        message = {
            "messages": [
                {"sender": {"wallet": self.address}, "body": "Hello"} for _ in range(20)
            ]
        }
        with mock.patch.object(
            _TypedDataEncoder,
            "encode_type",
            autospec=True,
            wraps=_TypedDataEncoder.encode_type,
        ) as encode_type_mock:
            eip712_encode_hash(self._build_typed_data(types, "Mailbox", message))

        # EIP712Domain, Mailbox, Message and Person
        self.assertEqual(encode_type_mock.call_count, 4)

    def test_eip712_encode_hash_many_types_performance(self):
        """
        Arrays of structs that reference many types are encoded fast
        """
        chained_types: dict[str, Any] = {
            "Message": [{"name": "values", "type": "Type0[]"}],
            "Type599": [{"name": "value", "type": "uint8[]"}],
        }
        for index in range(599):
            chained_types[f"Type{index}"] = [
                {"name": "value", "type": f"Type{index + 1}[]"}
            ]
        chained_types_message = {"values": [{"value": []}] * 100}

        type_names = [f"Type{index}" for index in range(30)]
        # Every type references all the others, Wrapper references all of them
        connected_types: dict[str, Any] = {
            "Message": [{"name": "values", "type": "Wrapper[]"}],
            "Wrapper": [{"name": "value", "type": "Type0[]"}],
        }
        for type_name in type_names:
            connected_types[type_name] = [
                {"name": f"value{index}", "type": f"{referenced_type_name}[]"}
                for index, referenced_type_name in enumerate(type_names)
            ]
        connected_types_message = {"values": [{"value": []}] * 4500}

        for types, message in [
            (chained_types, chained_types_message),
            (connected_types, connected_types_message),
        ]:
            typed_data = self._build_typed_data(types, "Message", message)
            start = time.perf_counter()
            eip712_encode_hash(typed_data)
            self.assertLess(time.perf_counter() - start, 1)

    def test_eip712_encode_hash_deep_nesting(self):
        """
        Data nested in a long chain of struct types is hashed
        """
        deep_types: dict[str, Any] = {
            f"Type{index}": [
                {"name": "value", "type": "uint256"},
                {"name": "nested", "type": f"Type{index + 1}"},
            ]
            for index in range(300)
        }
        deep_types["Type300"] = [{"name": "value", "type": "uint256"}]
        deep_message: dict[str, Any] = {"value": 300}
        for index in reversed(range(300)):
            deep_message = {"value": index, "nested": deep_message}
        self.assertEqual(
            to_0x_hex_str(
                eip712_encode_hash(
                    self._build_typed_data(deep_types, "Type0", deep_message)
                )
            ),
            "0x81fe209ae442145eb871ffd4549d4237b328f45df0184d4fffc41236cfb8e310",
        )

    def test_eip712_encode_hash_too_deep_nesting(self):
        """
        Data too deep to encode raises ValueError
        """
        recursive_types = {"Node": [{"name": "children", "type": "Node[]"}]}
        recursive_message: dict[str, Any] = {"children": []}
        for _ in range(100_000):
            recursive_message = {"children": [recursive_message]}
        with self.assertRaises(ValueError):
            eip712_encode_hash(
                self._build_typed_data(recursive_types, "Node", recursive_message)
            )

    def test_eip712_encode_hash_abi_encoder_cache(self):
        """
        Arrays of any length and structs of any shape do not add entries to the
        eth_abi encoder caches
        """

        def get_abi_encoder_cache_sizes() -> tuple[int, int]:
            return (
                default_abi_registry.get_tuple_encoder.cache_info().currsize,
                default_abi_registry.get_encoder.cache_info().currsize,
            )

        sizes = range(1, 30)
        types: dict[str, Any] = {
            f"Message{size}": [
                {"name": f"value{index}", "type": "uint256"} for index in range(size)
            ]
            + [{"name": "values", "type": "address[]"}]
            for size in sizes
        }
        eip712_encode_hash(
            self._build_typed_data(
                types, "Message1", {"value0": 0, "values": [self.address]}
            )
        )
        abi_encoder_cache_sizes = get_abi_encoder_cache_sizes()

        for size in sizes:
            message = {f"value{index}": index for index in range(size)}
            message["values"] = [self.address] * size
            eip712_encode_hash(self._build_typed_data(types, f"Message{size}", message))

        self.assertEqual(get_abi_encoder_cache_sizes(), abi_encoder_cache_sizes)
