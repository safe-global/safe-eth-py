import array
import os
import random
import unittest
from typing import Any

from django.test import TestCase

from eth_abi.packed import encode_packed
from eth_typing import ChecksumAddress
from eth_utils import is_checksum_address, to_checksum_address
from hexbytes import HexBytes

from ...util.tests.native_test_utils import (
    assert_same_outcome_as_reference,
    reference_keccak256,
)
from ..constants import SECPK1_N, SIGNATURE_R_MAX_VALUE, SIGNATURE_S_MAX_VALUE
from ..contracts import get_proxy_1_0_0_deployed_bytecode, get_proxy_factory_contract
from ..utils import (
    compare_byte_code,
    decode_string_or_bytes32,
    fast_bytes_to_checksum_address,
    fast_is_checksum_address,
    fast_keccak,
    fast_keccak_hex,
    fast_keccak_text,
    fast_to_checksum_address,
    mk_contract_address,
    mk_contract_address_2,
)
from .ethereum_test_case import EthereumTestCaseMixin


class TestUtils(EthereumTestCaseMixin, TestCase):
    def test_mk_contract_address_2(self):
        from_ = "0x8942595A2dC5181Df0465AF0D7be08c8f23C93af"
        salt = self.w3.keccak(text="aloha")
        init_code = "0x00abcd"
        expected = "0x8D02C796Dd019916F65EBa1C9D65a7079Ece00E0"
        address2 = mk_contract_address_2(from_, salt, init_code)
        self.assertEqual(address2, expected)

        from_ = HexBytes("0x8942595A2dC5181Df0465AF0D7be08c8f23C93af")
        salt = self.w3.keccak(text="aloha").hex()
        init_code = HexBytes("0x00abcd")
        expected = "0x8D02C796Dd019916F65EBa1C9D65a7079Ece00E0"
        address2 = mk_contract_address_2(from_, salt, init_code)
        self.assertEqual(address2, expected)

    def test_generate_address2_with_proxy(self):
        deployer_account = self.ethereum_test_account
        proxy_factory_contract = get_proxy_factory_contract(self.w3)
        nonce = self.w3.eth.get_transaction_count(
            deployer_account.address, block_identifier="pending"
        )
        tx = proxy_factory_contract.constructor().build_transaction(
            {"nonce": nonce, "from": deployer_account.address}
        )
        signed_tx = deployer_account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.wait_for_receipt(tx_hash)
        proxy_factory_contract = get_proxy_factory_contract(
            self.w3, address=tx_receipt["contractAddress"]
        )

        initializer = b""  # Should be the safe `setup()` call with `owners`, `threshold`, `payment`...
        salt_nonce = 0  # Random. For sure. I used a dice

        # From v1.4.1 createProxyWithNonce requires a valid singleton address, so we will use any deployed contract
        master_copy = proxy_factory_contract.address
        tx = proxy_factory_contract.functions.createProxyWithNonce(
            master_copy, initializer, salt_nonce
        ).build_transaction(
            {
                "nonce": nonce + 1,
                "from": deployer_account.address,
            }
        )
        signed_tx = deployer_account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.wait_for_receipt(tx_hash)
        logs = proxy_factory_contract.events.ProxyCreation().process_receipt(tx_receipt)
        log = logs[0]
        self.assertEqual(log["event"], "ProxyCreation")
        proxy_address = log["args"]["proxy"]

        proxy_creation_code = (
            proxy_factory_contract.functions.proxyCreationCode().call()
        )
        salt = self.w3.keccak(
            encode_packed(
                ["bytes", "uint256"], [self.w3.keccak(initializer), salt_nonce]
            )
        )
        deployment_data = encode_packed(
            ["bytes", "uint256"], [proxy_creation_code, int(master_copy, 16)]
        )
        address2 = mk_contract_address_2(
            proxy_factory_contract.address, salt, deployment_data
        )
        self.assertEqual(proxy_address, address2)

    def test_decode_string_or_bytes32(self):
        # Abi encoded string
        gnosis_hex = HexBytes(
            "0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000"
            "00000000000000000000000000000000000000000c476e6f73697320546f6b656e0000000000000000000000"
            "000000000000000000"
        )

        # Abi encoded bytes32
        dai_hex = HexBytes(
            "0x44616920537461626c65636f696e2076312e3000000000000000000000000000"
        )

        self.assertEqual(decode_string_or_bytes32(gnosis_hex), "Gnosis Token")
        self.assertEqual(decode_string_or_bytes32(dai_hex), "Dai Stablecoin v1.0")

    def test_compare_byte_code(self):
        proxy_with_metadata = get_proxy_1_0_0_deployed_bytecode()
        proxy_with_different_metadata = HexBytes(
            "0x608060405273ffffffffffffffffffffffffffffffffffffffff60005416366000"
            "8037600080366000845af43d6000803e6000811415603d573d6000fd5b3d6000f3fe"
            "a165627a7a72305820b7f4e514a2bdfeb2e729e84f7101233a43b51d677007041e70"
            "8067e4b88bec480029"
        )
        self.assertTrue(
            compare_byte_code(proxy_with_metadata, proxy_with_different_metadata)
        )

    def test_fast_keccak(self):
        """Known keccak256 digests from `fast_keccak`"""
        text = "chidori"
        self.assertEqual(
            fast_keccak(text.encode()),
            HexBytes(
                "0xd20148e42186a9e7698e652e255c809851633d62bad625a55d05efd7f718449c"
            ),
        )

        binary = b""
        self.assertEqual(
            fast_keccak(binary),
            HexBytes(
                "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
            ),
        )

        binary = b"1234"
        self.assertEqual(
            fast_keccak(binary),
            HexBytes(
                "0x387a8233c96e1fc0ad5e284353276177af2186e7afa85296f106336e376669f7"
            ),
        )

    def test_fast_to_checksum_address(self):
        for _ in range(10):
            address = os.urandom(20).hex()
            self.assertEqual(
                fast_to_checksum_address(address), to_checksum_address(address)
            )

    def test_fast_bytes_to_checksum_address(self):
        with self.assertRaises(ValueError):
            fast_bytes_to_checksum_address(os.urandom(19))

        with self.assertRaises(ValueError):
            fast_bytes_to_checksum_address(os.urandom(21))

        # `bytes()` of these would be 20 zero bytes, or bytes from the generator
        class IndexLike:
            def __index__(self) -> int:
                return 20

        for value_without_length in (20, IndexLike(), (byte for byte in bytes(20))):
            with self.assertRaises(TypeError):
                fast_bytes_to_checksum_address(value_without_length)

        # 20 items of 2 bytes are 40 bytes
        with self.assertRaises(ValueError):
            fast_bytes_to_checksum_address(array.array("H", range(20)))

        # Any iterable of byte values is accepted, like `bytes()` does
        address = os.urandom(20)
        for address_bytes in (list(address), tuple(address), bytearray(address)):
            self.assertEqual(
                fast_bytes_to_checksum_address(address_bytes),
                to_checksum_address(address),
            )

        for _ in range(10):
            address = os.urandom(20)
            self.assertEqual(
                fast_bytes_to_checksum_address(address), to_checksum_address(address)
            )

    def test_fast_is_checksum_address(self):
        self.assertFalse(fast_is_checksum_address(None))
        self.assertFalse(fast_is_checksum_address(""))
        self.assertFalse(
            fast_is_checksum_address(0x6ED857DC1DA2C41470A95589BB482152000773E9)
        )
        self.assertFalse(fast_is_checksum_address(2))
        self.assertFalse(fast_is_checksum_address("2"))
        self.assertFalse(
            fast_is_checksum_address("0x6ed857dc1da2c41470A95589bB482152000773e9")
        )
        self.assertTrue(
            fast_is_checksum_address("0x6ED857dc1da2c41470A95589bB482152000773e9")
        )

    def test_mk_contract_address(self):
        self.assertEqual(
            mk_contract_address("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 129),
            "0x5A317285cD83092fD40153C4B7c3Df64d8482Da8",
        )
        self.assertEqual(
            mk_contract_address("0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B", 399),
            "0xF03b503CC9Ee8aAA3B17856942a440be0c77Cd84",
        )

        # Vectors generated with py-evm `generate_contract_address`. Nonces 0, 127,
        # 128 and 2**32 hit the different RLP integer encodings
        sender = "0x6ac7ea33f8831ea9dcc53393aaa88b25a785dbf0"
        expected_address_by_nonce = {
            0: "0xcd234A471b72ba2F1Ccf0A70FCABA648a5eeCD8d",
            1: "0x343c43A37D37dfF08AE8C4A11544c718AbB4fCF8",
            127: "0x06d9a77f5E4b311Bae8D559DB9CDB4dF94104aA0",
            128: "0x08e190dcB7b73F5fcDAbb43e102215c83659A76D",
            2**32: "0xf4bf328880432064068338F915C49f817dC4Ce18",
        }
        for nonce, expected_address in expected_address_by_nonce.items():
            with self.subTest(nonce=nonce):
                self.assertEqual(mk_contract_address(sender, nonce), expected_address)
                self.assertEqual(
                    mk_contract_address(HexBytes(sender), nonce), expected_address
                )

    def test_secpk1_n(self):
        """
        SECPK1_N is the secp256k1 curve order and the signature limits derive from it
        """
        self.assertEqual(
            SECPK1_N,
            115792089237316195423570985008687907852837564279074904382605163141518161494337,
        )
        self.assertEqual(SIGNATURE_R_MAX_VALUE, SECPK1_N - 1)
        self.assertEqual(SIGNATURE_S_MAX_VALUE, SECPK1_N // 2)


class StrSubclass(str):
    pass


def build_address_values(address_bytes: bytes) -> list:
    """
    The same address in every form, and invalid values built from it
    """
    lowercase_hex = address_bytes.hex()
    checksum_address = to_checksum_address(address_bytes)
    position = random.randrange(40)
    return [
        address_bytes,
        HexBytes(address_bytes),
        bytearray(address_bytes),
        memoryview(address_bytes),
        "0x" + lowercase_hex,
        "0X" + lowercase_hex.upper(),
        lowercase_hex,
        checksum_address,
        checksum_address.lower(),
        checksum_address[2:],
        "0x" + checksum_address[2:].swapcase(),
        StrSubclass(checksum_address),
        int.from_bytes(address_bytes, "big"),
        # 2 bytes per item: the number of items is not the number of bytes
        array.array("H", address_bytes),
        array.array("H", address_bytes * 2),
        # Invalid values
        address_bytes[:19],
        address_bytes + b"\x00",
        checksum_address.encode(),
        "0x" + lowercase_hex[:39],
        "0x" + lowercase_hex + "0",
        " " + checksum_address,
        "0x" + lowercase_hex[:position] + "g" + lowercase_hex[position + 1 :],
        "0x" + lowercase_hex[:position] + "\u0661" + lowercase_hex[position + 1 :],
        "0x" + lowercase_hex[:position] + "\ud800" + lowercase_hex[position + 1 :],
        "",
        "0x",
        None,
        1.0,
        [address_bytes],
    ]


def reference_bytes_to_checksum_address(value: Any) -> ChecksumAddress:
    """`fast_bytes_to_checksum_address` built on eth-utils, which only takes `bytes`"""
    if not isinstance(value, bytes) and len(value) == 20:
        value = bytes(value)
    if len(value) != 20:
        raise ValueError(
            f"Cannot convert {bytes(value).hex()} to a checksum address, 20 bytes were expected"
        )
    return to_checksum_address(value)


class TestFastHelpersSameAsReference(unittest.TestCase):
    """
    The fast helpers return the same values as pycryptodome and eth-utils, and raise the
    same errors with the same messages as eth-utils
    """

    def test_fast_keccak(self):
        """`fast_keccak`, `fast_keccak_hex` and `fast_keccak_text` for bytes of every length and other buffers"""
        values = [
            b"",
            b"1234",
            HexBytes(os.urandom(32)),
            os.urandom(5000),
            memoryview(os.urandom(32)),
            bytearray(os.urandom(32)),
            bytearray(os.urandom(2000)),
            memoryview(bytearray(os.urandom(32))),
            memoryview(os.urandom(32)).cast("I"),
            array.array("b", os.urandom(32)),
            array.array("I", os.urandom(32)),
        ] + [os.urandom(length) for length in range(300)]
        for value in values:
            with self.subTest(value=value):
                expected_digest = reference_keccak256(value)
                self.assertEqual(fast_keccak(value), HexBytes(expected_digest))
                self.assertIsInstance(fast_keccak(value), HexBytes)
                self.assertEqual(fast_keccak_hex(value), expected_digest.hex())
        for text in ("", "chidori", "ñ" * 100):
            self.assertEqual(fast_keccak_text(text), reference_keccak256(text.encode()))

    def test_fast_keccak_invalid_values(self):
        """Values that are not a buffer raise `TypeError`, and non contiguous buffers `BufferError`"""
        for value, error in (
            ("text", TypeError),
            (None, TypeError),
            (1, TypeError),
            ([1, 2], TypeError),
            (memoryview(os.urandom(32))[::2], BufferError),
        ):
            for function in (fast_keccak, fast_keccak_hex):
                with self.subTest(function=function.__name__, value=value):
                    with self.assertRaises(error):
                        function(value)

    def test_checksum_address_helpers(self):
        """The checksum helpers for every form of an address and for invalid values"""
        for address_bytes in [bytes(20), b"\xff" * 20] + [
            os.urandom(20) for _ in range(300)
        ]:
            for value in build_address_values(address_bytes):
                if isinstance(value, bytes) and len(value) != 20:
                    with self.assertRaisesRegex(ValueError, "20 bytes were expected"):
                        fast_to_checksum_address(value)
                else:
                    assert_same_outcome_as_reference(
                        self, fast_to_checksum_address, to_checksum_address, value
                    )
                assert_same_outcome_as_reference(
                    self,
                    fast_bytes_to_checksum_address,
                    reference_bytes_to_checksum_address,
                    value,
                )
                assert_same_outcome_as_reference(
                    self, fast_is_checksum_address, is_checksum_address, value
                )
