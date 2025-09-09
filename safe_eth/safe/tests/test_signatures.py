from django.test import TestCase

from eth_account import Account

from safe_eth.eth.constants import NULL_ADDRESS
from safe_eth.eth.contracts import get_compatibility_fallback_handler_contract
from safe_eth.eth.utils import fast_keccak_text

from ..signatures import get_signing_address
from .safe_test_case import SafeTestCaseMixin


class TestSafeSignature(SafeTestCaseMixin, TestCase):
    EIP1271_MAGIC_VALUE = "20c13b0b"
    EIP1271_MAGIC_VALUE = "1626ba7e"

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

        # Use deprecated isValidSignature method (receives bytes)
        signature = owner.unsafe_sign_hash(safe_message_hash)
        is_valid_bytes_fn = compatibility_contract.get_function_by_signature(
            "isValidSignature(bytes32,bytes)"
        )
        self.assertEqual(
            is_valid_bytes_fn(message.encode(), signature.signature).call(),
            bytes.fromhex(self.EIP1271_MAGIC_VALUE),
        )

        # Use new isValidSignature method (receives bytes32 == hash of the message)
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
            bytes.fromhex(self.EIP1271_MAGIC_VALUE),
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
