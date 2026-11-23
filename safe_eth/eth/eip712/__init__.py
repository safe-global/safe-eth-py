"""
Based on https://github.com/jvinet/eip712, adjustments by https://github.com/uxio0

Routines for EIP712 encoding and signing.

Copyright (C) 2022 Judd Vinet <jvinet@zeroflux.org>
                   Uxío Fuentefría <uxio@safe.global>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
from typing import Any

from eth_abi import encode as encode_abi
from eth_abi.exceptions import EncodingError, ParseError
from eth_typing import Hash32
from hexbytes import HexBytes

from ..utils import fast_keccak

_StructTypes = dict[str, list[dict[str, Any]]]


def _remove_array_suffix(type_name: str) -> str:
    return re.split(r"\W", type_name, maxsplit=1)[0]


class _TypedDataEncoder:
    """
    Encoder for the structs in ``types``. The dependencies, definition and hash of
    each struct type are computed once, and reused for every instance of the struct.
    """

    def __init__(self, types: _StructTypes) -> None:
        self.types = types
        self._referenced_types: dict[str, list[str]] = {}
        self._type_definitions: dict[str, str] = {}
        self._type_hashes: dict[str, Hash32] = {}

    def _get_referenced_types(self, type_name: str) -> list[str]:
        """
        :return: type of each field of ``type_name`` without array suffix
        """
        if type_name not in self._referenced_types:
            self._referenced_types[type_name] = [
                _remove_array_suffix(field["type"]) for field in self.types[type_name]
            ]
        return self._referenced_types[type_name]

    def _get_type_definition(self, type_name: str) -> str:
        if type_name not in self._type_definitions:
            fields = self.types[type_name]
            if not fields:
                raise ValueError(f"No type definition specified: {type_name}")
            field_definitions = [f"{field['type']} {field['name']}" for field in fields]
            self._type_definitions[type_name] = (
                type_name + "(" + ",".join(field_definitions) + ")"
            )
        return self._type_definitions[type_name]

    def find_type_dependencies(self, primary_type: str) -> list[str]:
        """
        :return: ``primary_type`` and every struct type it references, directly or
            not, in depth-first order
        """
        dependencies: dict[str, None] = {}
        pending_types = [_remove_array_suffix(primary_type)]
        while pending_types:
            type_name = pending_types.pop()
            if type_name in dependencies or not self.types.get(type_name):
                continue
            dependencies[type_name] = None
            pending_types.extend(reversed(self._get_referenced_types(type_name)))
        return list(dependencies)

    def encode_type(self, primary_type: str) -> str:
        dependencies = sorted(
            dependency
            for dependency in self.find_type_dependencies(primary_type)
            if dependency != primary_type
        )
        return "".join(
            self._get_type_definition(type_name)
            for type_name in [primary_type, *dependencies]
        )

    def hash_type(self, primary_type: str) -> Hash32:
        if primary_type not in self._type_hashes:
            self._type_hashes[primary_type] = fast_keccak(
                self.encode_type(primary_type).encode()
            )
        return self._type_hashes[primary_type]

    def encode_data(self, primary_type: str, data: dict[str, Any]) -> bytes:
        encoded_types = ["bytes32"]
        encoded_values = [self.hash_type(primary_type)]
        for field in self.types[primary_type]:
            field_type, field_value = self._encode_field(
                field["name"], field["type"], data[field["name"]]
            )
            encoded_types.append(field_type)
            encoded_values.append(field_value)
        return encode_abi(encoded_types, encoded_values)

    def hash_struct(self, primary_type: str, data: dict[str, Any]) -> Hash32:
        return fast_keccak(self.encode_data(primary_type, data))

    def _encode_field(self, name: str, typ: str, value: Any) -> list[Any]:
        if typ in self.types:
            if value is None:
                return [
                    "bytes32",
                    "0x0000000000000000000000000000000000000000000000000000000000000000",
                ]
            else:
                return ["bytes32", fast_keccak(self.encode_data(typ, value))]

        if value is None:
            raise ValueError(f"Missing value for field {name} of type {typ}")

        # Accept string bytes
        if "bytes" in typ and isinstance(value, str):
            value = HexBytes(value)

        # Accept string uint and int
        if "int" in typ and isinstance(value, str):
            value = int(value)

        if typ == "bytes":
            return ["bytes32", fast_keccak(value)]

        if typ == "string":
            # Convert string to bytes.
            value = value.encode("utf-8")
            return ["bytes32", fast_keccak(value)]

        if typ.endswith("]"):
            # Array type
            if value:
                parsed_type = typ[: typ.rindex("[")]
                type_value_pairs = [
                    self._encode_field(name, parsed_type, v) for v in value
                ]
                data_types, data_hashes = zip(*type_value_pairs, strict=False)
            else:
                # Empty array
                data_types, data_hashes = (), ()

            h = fast_keccak(encode_abi(data_types, data_hashes))
            return ["bytes32", h]

        return [typ, value]


def encode_data(primary_type: str, data: dict[str, Any], types: _StructTypes) -> bytes:
    """
    Encode structured data as per Ethereum's signTypeData_v4.

    https://docs.metamask.io/guide/signing-data.html#sign-typed-data-v4

    This code is ported from the Javascript "eth-sig-util" package.
    """
    return _TypedDataEncoder(types).encode_data(primary_type, data)


def encode_type(primary_type: str, types: _StructTypes) -> str:
    return _TypedDataEncoder(types).encode_type(primary_type)


def find_type_dependencies(primary_type: str, types: _StructTypes) -> list[str]:
    return _TypedDataEncoder(types).find_type_dependencies(primary_type)


def hash_type(primary_type: str, types: _StructTypes) -> Hash32:
    return _TypedDataEncoder(types).hash_type(primary_type)


def hash_struct(primary_type: str, data: dict[str, Any], types: _StructTypes) -> Hash32:
    return _TypedDataEncoder(types).hash_struct(primary_type, data)


def eip712_encode(typed_data: dict[str, Any]) -> tuple[bytes, Hash32, Hash32]:
    """
    Given a dict of structured data and types, return a 3-element tuple of
    the encoded, signable data.

      0: The magic & version (0x1901)
      1: The encoded types
      2: The encoded data
    """
    try:
        encoder = _TypedDataEncoder(typed_data["types"])
        domain_hash = encoder.hash_struct("EIP712Domain", typed_data["domain"])
        if typed_data["primaryType"] == "EIP712Domain":
            raise TypeError("primaryType cannot be EIP712Domain")

        return (
            bytes.fromhex("1901"),
            domain_hash,
            encoder.hash_struct(typed_data["primaryType"], typed_data["message"]),
        )

    except (
        KeyError,
        AttributeError,
        TypeError,
        IndexError,
        RecursionError,
        EncodingError,
        ParseError,
    ) as exc:
        raise ValueError("Not valid EIP712 typed data") from exc


def eip712_encode_hash(typed_data: dict[str, Any]) -> Hash32:
    """
    :param typed_data: EIP712 structured data and types
    :return: Keccak256 hash of encoded signable data
    """
    return fast_keccak(b"".join(eip712_encode(typed_data)))
