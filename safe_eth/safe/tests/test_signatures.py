import os
import random
import unittest
from unittest import mock

from django.test import TestCase

import safe_eth_native
from eth_account import Account
from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes

from safe_eth.eth.constants import NULL_ADDRESS, SECPK1_N
from safe_eth.eth.contracts import get_compatibility_fallback_handler_contract
from safe_eth.eth.utils import fast_keccak_text
from safe_eth.util.tests.native_test_utils import assert_same_outcome_as_reference

from ..signatures import _get_signing_address_with_eth_keys, get_signing_address
from .safe_test_case import SafeTestCaseMixin


class TestSafeSignature(SafeTestCaseMixin, TestCase):
    EIP1271_MAGIC_VALUE = "20c13b0b"
    EIP1271_MAGIC_VALUE_UPDATED = "1626ba7e"

    def test_get_signing_address(self):
        account = Account.create()
        # Random hash
        random_hash = fast_keccak_text("tanxugueiras")
        signature = account.unsafe_sign_hash(random_hash)
        self.assertEqual(
            get_signing_address(random_hash, signature.v, signature.r, signature.s),
            account.address,
        )

        # Invalid signature will return the `NULL_ADDRESS`
        self.assertEqual(
            get_signing_address(random_hash, signature.v - 8, signature.r, signature.s),
            NULL_ADDRESS,
        )

    def test_eip1271_signing(self):
        owner = Account.create()
        message = "luar_na_lubre"
        safe = self.deploy_test_safe(threshold=1, owners=[owner.address])

        self.assertEqual(
            safe.contract.functions.domainSeparator().call(), safe.domain_separator
        )

        compatibility_contract = get_compatibility_fallback_handler_contract(
            self.w3, safe.address
        )
        safe_message_hash = safe.get_message_hash(message)
        self.assertEqual(
            compatibility_contract.functions.getMessageHash(message.encode()).call(),
            safe_message_hash,
        )

        # Use new isValidSignature method (receives bytes32 == hash of the message)
        # isValidSignature method (receives bytes) was finally deprecated in version 1.5.0
        # Message needs to be hashed first
        message_hash = fast_keccak_text(message)
        safe_message_hash = safe.get_message_hash(message_hash)
        self.assertEqual(
            compatibility_contract.functions.getMessageHash(message_hash).call(),
            safe_message_hash,
        )

        signature = owner.unsafe_sign_hash(safe_message_hash)
        is_valid_bytes_fn = compatibility_contract.get_function_by_signature(
            "isValidSignature(bytes32,bytes)"
        )
        self.assertEqual(
            is_valid_bytes_fn(message_hash, signature.signature).call(),
            bytes.fromhex(self.EIP1271_MAGIC_VALUE_UPDATED),
        )

    def test_eip1271_signing_v1_1_1_contract(self):
        owner = Account.create()
        message = "luar_na_lubre"
        safe = self.deploy_test_safe_v1_1_1(threshold=1, owners=[owner.address])

        self.assertEqual(
            safe.contract.functions.domainSeparator().call(), safe.domain_separator
        )

        contract = safe.contract
        safe_message_hash = safe.get_message_hash(message)
        self.assertEqual(
            contract.functions.getMessageHash(message.encode()).call(),
            safe_message_hash,
        )

        # Use isValidSignature method (receives bytes)
        signature = owner.unsafe_sign_hash(safe_message_hash)

        self.assertEqual(
            contract.functions.isValidSignature(
                message.encode(), signature.signature
            ).call(),
            bytes.fromhex(self.EIP1271_MAGIC_VALUE),
        )


class IntSubclass(int):
    pass


class TestGetSigningAddressSameAsEthKeys(unittest.TestCase):
    """
    `get_signing_address` and eth-keys recover the same address, or return
    `NULL_ADDRESS`, or raise the same error
    """

    def test_valid_signatures(self):
        """Low `s` and high `s` signatures, over raw and EIP-191 hashes"""
        for _ in range(10):
            account = Account.create()
            for signed_hash in (
                os.urandom(32),
                HexBytes(os.urandom(32)),
                defunct_hash_message(primitive=os.urandom(32)),
            ):
                signature = account.unsafe_sign_hash(signed_hash)
                high_s_v = 55 - signature.v
                high_s = SECPK1_N - signature.s
                for v, s in ((signature.v, signature.s), (high_s_v, high_s)):
                    self.assertEqual(
                        get_signing_address(signed_hash, v, signature.r, s),
                        account.address,
                    )
                    assert_same_outcome_as_reference(
                        self,
                        get_signing_address,
                        _get_signing_address_with_eth_keys,
                        signed_hash,
                        v,
                        signature.r,
                        s,
                    )
                    assert_same_outcome_as_reference(
                        self,
                        get_signing_address,
                        _get_signing_address_with_eth_keys,
                        signed_hash,
                        55 - v,
                        signature.r,
                        s,
                    )

    def test_random_values(self):
        """Random `r` and `s`, about half of them without a point on the curve"""
        for _ in range(100):
            assert_same_outcome_as_reference(
                self,
                get_signing_address,
                _get_signing_address_with_eth_keys,
                os.urandom(32),
                random.choice((27, 28)),
                random.randrange(1, SECPK1_N),
                random.randrange(1, SECPK1_N),
            )

    def test_invalid_values(self):
        """Values the precompile rejects give `NULL_ADDRESS`"""
        account = Account.create()
        signed_hash = os.urandom(32)
        signature = account.unsafe_sign_hash(signed_hash)
        v, r, s = signature.v, signature.r, signature.s
        for invalid_v, invalid_r, invalid_s in (
            (0, r, s),
            (1, r, s),
            (26, r, s),
            (29, r, s),
            (31, r, s),
            (32, r, s),
            (v + 4, r, s),
            (v - 8, r, s),
            (-1, r, s),
            (2**64 + v, r, s),
            (v, 0, s),
            (v, r, 0),
            (v, SECPK1_N, s),
            (v, r, SECPK1_N),
            (v, 2**256, s),
            (v, r, 2**256),
            (v, -1, s),
            (v, r, -1),
            # 5 is not the x coordinate of a point
            (v, 5, s),
        ):
            with self.subTest(v=invalid_v, r=invalid_r, s=invalid_s):
                self.assertEqual(
                    get_signing_address(signed_hash, invalid_v, invalid_r, invalid_s),
                    NULL_ADDRESS,
                )
                assert_same_outcome_as_reference(
                    self,
                    get_signing_address,
                    _get_signing_address_with_eth_keys,
                    signed_hash,
                    invalid_v,
                    invalid_r,
                    invalid_s,
                )

    def test_values_that_are_not_int(self):
        """`v`, `r` and `s` that are not exactly `int` go to eth-keys"""
        account = Account.create()
        signed_hash = os.urandom(32)
        signature = account.unsafe_sign_hash(signed_hash)
        v, r, s = signature.v, signature.r, signature.s
        for not_int_v, not_int_r, not_int_s in (
            (float(v), r, s),
            (str(v), r, s),
            (v, float(r), s),
            (v, r, str(s)),
            (v, True, s),
            (v, r, True),
            (v, IntSubclass(r), s),
            (v, None, s),
        ):
            with (
                self.subTest(v=not_int_v, r=not_int_r, s=not_int_s),
                mock.patch.object(
                    safe_eth_native, "ecrecover", wraps=safe_eth_native.ecrecover
                ) as native_ecrecover,
            ):
                assert_same_outcome_as_reference(
                    self,
                    get_signing_address,
                    _get_signing_address_with_eth_keys,
                    signed_hash,
                    not_int_v,
                    not_int_r,
                    not_int_s,
                )
                native_ecrecover.assert_not_called()
        self.assertEqual(
            get_signing_address(signed_hash, v, IntSubclass(r), s), account.address
        )
        # The same values as `int` go to the native extension
        with mock.patch.object(
            safe_eth_native, "ecrecover", wraps=safe_eth_native.ecrecover
        ) as native_ecrecover:
            self.assertEqual(get_signing_address(signed_hash, v, r, s), account.address)
        native_ecrecover.assert_called_once_with(signed_hash, v, r, s)

    def test_invalid_hashes(self):
        """Hashes the native extension does not take go to eth-keys"""
        account = Account.create()
        signed_hash = os.urandom(32)
        signature = account.unsafe_sign_hash(signed_hash)
        for invalid_hash in (
            b"",
            signed_hash[:31],
            signed_hash + b"\x00",
            signed_hash.hex(),
            "0x" + signed_hash.hex(),
            bytearray(signed_hash),
            memoryview(signed_hash),
            None,
        ):
            with (
                self.subTest(signed_hash=invalid_hash),
                mock.patch.object(
                    safe_eth_native, "ecrecover", wraps=safe_eth_native.ecrecover
                ) as native_ecrecover,
            ):
                assert_same_outcome_as_reference(
                    self,
                    get_signing_address,
                    _get_signing_address_with_eth_keys,
                    invalid_hash,
                    signature.v,
                    signature.r,
                    signature.s,
                )
                native_ecrecover.assert_not_called()
