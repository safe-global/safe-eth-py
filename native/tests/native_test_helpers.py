"""
Helpers shared by the native extension tests. The references are pycryptodome and the pure
Python eth-keys backend, which install on every platform and Python the extension supports,
free-threaded builds included.
"""

import hashlib
import json
import os
import random
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.Hash import keccak as pycryptodome_keccak
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend

VECTORS_DIRECTORY = Path(__file__).parent / "vectors"
HASH_FUNCTIONS = {"SHA-256": hashlib.sha256, "SHA-512": hashlib.sha512}

SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
NATIVE_KEYS = KeyAPI(backend=NativeECCBackend)


class BytesSubclass(bytes):
    pass


class StrSubclass(str):
    pass


def reference_keccak256(data: bytes) -> bytes:
    return pycryptodome_keccak.new(data=data, digest_bits=256).digest()


def reference_checksum_address(address: bytes) -> str:
    """
    EIP-55 checksum address with the pycryptodome keccak, so the expected value does not
    depend on eth-utils, whose keccak is the native one when safe-eth-py is imported
    """
    lowercase_hex = address.hex()
    address_hash = reference_keccak256(lowercase_hex.encode()).hex()
    return "0x" + "".join(
        character.upper() if int(hash_digit, 16) > 7 else character
        for character, hash_digit in zip(lowercase_hex, address_hash, strict=False)
    )


def address_from_public_key(public_key: bytes) -> bytes:
    """
    :param public_key: 64 bytes ``x || y``
    :return: 20 bytes Ethereum address
    """
    return reference_keccak256(public_key)[12:]


def build_secp256k1_signatures(count: int) -> list[tuple[bytes, int, int, int, bytes]]:
    """
    :return: random ``(message_hash, v, r, s, signer)`` signatures, each one also in its
        high ``s`` form (``s' = n - s`` with the other ``v``)
    """
    signatures = []
    for _ in range(count):
        private_key = NATIVE_KEYS.PrivateKey(
            random.randrange(1, SECP256K1_N).to_bytes(32, "big")
        )
        message_hash = os.urandom(32)
        signature = private_key.sign_msg_hash(message_hash)
        signer = address_from_public_key(private_key.public_key.to_bytes())
        v = signature.v + 27
        signatures.append((message_hash, v, signature.r, signature.s, signer))
        signatures.append(
            (message_hash, 55 - v, signature.r, SECP256K1_N - signature.s, signer)
        )
    return signatures


class PrehashedSha256:
    """
    Hash object for pycryptodome ``DSS`` that returns a given digest, to sign any 256 bits
    value, also above the curve order
    """

    oid = SHA256.new().oid
    digest_size = 32

    def __init__(self, digest: bytes):
        self._digest = digest

    def digest(self) -> bytes:
        return self._digest


def sign_p256_digest(private_key: ECC.EccKey, digest: bytes) -> tuple[int, int]:
    signature = DSS.new(private_key, "fips-186-3").sign(PrehashedSha256(digest))
    return int.from_bytes(signature[:32], "big"), int.from_bytes(signature[32:], "big")


def build_p256_signatures(count: int) -> list[tuple[int, int, int, int, int]]:
    """
    :return: random ``(message_hash, r, s, public_key_x, public_key_y)`` signatures
    """
    signatures = []
    for _ in range(count):
        private_key = ECC.generate(curve="P-256")
        digest = os.urandom(32)
        r, s = sign_p256_digest(private_key, digest)
        signatures.append(
            (
                int.from_bytes(digest, "big"),
                r,
                s,
                int(private_key.pointQ.x),
                int(private_key.pointQ.y),
            )
        )
    return signatures


@dataclass(frozen=True)
class WycheproofEcdsaTest:
    test_id: int
    public_key_x: int
    public_key_y: int
    # Leftmost 256 bits of the message hash, as ECDSA uses it for 256 bits curves
    message_digest: bytes
    signature: bytes
    is_valid: bool


def load_wycheproof_ecdsa_tests(file_name: str) -> Iterator[WycheproofEcdsaTest]:
    test_data = json.loads((VECTORS_DIRECTORY / file_name).read_text())
    for test_group in test_data["testGroups"]:
        hash_function = HASH_FUNCTIONS[test_group["sha"]]
        public_key = test_group["publicKey"]
        for test in test_group["tests"]:
            assert test["result"] in ("valid", "invalid"), test
            yield WycheproofEcdsaTest(
                test_id=test["tcId"],
                public_key_x=int(public_key["wx"], 16),
                public_key_y=int(public_key["wy"], 16),
                message_digest=hash_function(bytes.fromhex(test["msg"])).digest()[:32],
                signature=bytes.fromhex(test["sig"]),
                is_valid=test["result"] == "valid",
            )


def load_keccak_256_known_answers() -> Iterator[tuple[bytes, bytes]]:
    with open(VECTORS_DIRECTORY / "keccak_256_short_msg_kat.txt") as kat_file:
        for line in kat_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            message_hex, digest_hex = line.split(",")
            yield bytes.fromhex(message_hex), bytes.fromhex(digest_hex)
