import logging

from django.test import TestCase

from eth_abi import encode_single
from eth_abi.packed import encode_single_packed
from eth_account import Account
from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes
from web3 import Web3

from ...eth.tests.ethereum_test_case import EthereumTestCaseMixin
from ..safe_signature import (
    SafeSignature,
    SafeSignatureApprovedHash,
    SafeSignatureContract,
    SafeSignatureEOA,
    SafeSignatureEthSign,
    SafeSignatureType,
)
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestSafeSignature(EthereumTestCaseMixin, TestCase):
    def test_contract_signature(self):
        owner = "0x05c85Ab5B09Eb8A55020d72daf6091E04e264af9"
        safe_tx_hash = HexBytes(
            "0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196"
        )
        signature = HexBytes(
            "0x00000000000000000000000005c85ab5b09eb8a55020d72daf6091e04e264af900000000000000000000000"
            "0000000000000000000000000000000000000000000"
        )
        safe_signature = SafeSignatureContract(signature, safe_tx_hash, b"")
        self.assertEqual(safe_signature.owner, owner)
        self.assertEqual(
            safe_signature.signature_type, SafeSignatureType.CONTRACT_SIGNATURE
        )
        self.assertTrue(str(safe_signature))  # Test __str__
        self.assertFalse(safe_signature.is_valid(self.ethereum_client))

    def test_approved_hash_signature(self):
        owner = "0x05c85Ab5B09Eb8A55020d72daf6091E04e264af9"
        safe_tx_hash = HexBytes(
            "0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196"
        )
        signature = HexBytes(
            "0x00000000000000000000000005c85ab5b09eb8a55020d72daf6091e04e264af900000000000000000000000"
            "0000000000000000000000000000000000000000001"
        )
        safe_signature = SafeSignatureApprovedHash(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)
        self.assertEqual(safe_signature.signature_type, SafeSignatureType.APPROVED_HASH)
        self.assertTrue(str(safe_signature))  # Test __str__

        # Problematic signature found on rinkeby tx-hash 0x10df7fd8b75297af360ae335ca7562be92cafbbd39cc72172e17fcaebccc4f42
        # Note the ff preceding the address
        signature = HexBytes(
            "0x0000000000000000000000ffdc5299b629ef24fdecfbb240c00fc79fabb9cf97000000000000000000000000000000000000000000000000000000000000000001"
        )
        # Safe tx hash is not relevant for this case, use the same one
        safe_signature = SafeSignatureApprovedHash(signature, b"")
        self.assertEqual(
            safe_signature.owner, "0xdC5299b629Ef24fDECfBb240C00Fc79FAbB9cf97"
        )

    def test_approved_hash_signature_build(self):
        owner = Account.create().address
        safe_tx_hash = Web3.keccak(text="random")
        safe_signature = SafeSignatureApprovedHash.build_for_owner(owner, safe_tx_hash)
        self.assertEqual(len(safe_signature.signature), 65)
        self.assertEqual(safe_signature.signature_type, SafeSignatureType.APPROVED_HASH)
        self.assertEqual(safe_signature.owner, owner)

        # Check parse signature get the same result
        safe_signature = SafeSignature.parse_signature(
            safe_signature.signature, safe_tx_hash
        )[0]
        self.assertEqual(safe_signature.signature_type, SafeSignatureType.APPROVED_HASH)
        self.assertEqual(safe_signature.owner, owner)

    def test_eth_sign_signature(self):
        account = Account.create()
        owner = account.address
        safe_tx_hash = HexBytes(
            "0x123477d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf195"
        )
        message = defunct_hash_message(primitive=safe_tx_hash)
        signature = account.signHash(message)["signature"]
        signature = signature[:64] + HexBytes(signature[64] + 4)  # Add 4 to v
        safe_signature = SafeSignatureEthSign(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)
        self.assertEqual(safe_signature.signature_type, SafeSignatureType.ETH_SIGN)
        self.assertTrue(safe_signature.is_valid())
        self.assertTrue(str(safe_signature))  # Test __str__

    def test_eoa_signature(self):
        owner = "0xADb7CB706e9A1bd9F96a397da340bF34a9984E1E"
        safe_tx_hash = HexBytes(
            "0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196"
        )
        signature = HexBytes(
            "0x5dccf9f1375cee56331a67867a0b05a828894c2b76dee84546ec663997d7548257cb2d606087ee7590b966e"
            "958d97a65528ae941a0f7e5050949f618629509c81b"
        )
        safe_signature = SafeSignatureEOA(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)
        self.assertEqual(safe_signature.signature_type, SafeSignatureType.EOA)
        self.assertTrue(safe_signature.is_valid())

        account = Account.create()
        owner = account.address
        safe_tx_hash = HexBytes(
            "0x123477d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf195"
        )
        signature = account.signHash(safe_tx_hash)["signature"]
        safe_signature = SafeSignatureEOA(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)
        self.assertEqual(safe_signature.signature_type, SafeSignatureType.EOA)
        self.assertTrue(safe_signature.is_valid())
        self.assertTrue(str(safe_signature))  # Test __str__

    def test_defunct_hash_message(self):
        safe_tx_hash = HexBytes(
            "0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196"
        )
        ethereum_signed_message = "\x19Ethereum Signed Message:\n32"
        encoded_message = encode_single_packed(
            "(string,bytes32)", (ethereum_signed_message, HexBytes(safe_tx_hash))
        )
        encoded_hash = Web3.keccak(encoded_message)
        self.assertEqual(encoded_hash, defunct_hash_message(primitive=safe_tx_hash))

    def test_parse_signature(self):
        owner_1 = "0x05c85Ab5B09Eb8A55020d72daf6091E04e264af9"
        owner_2 = "0xADb7CB706e9A1bd9F96a397da340bF34a9984E1E"
        safe_tx_hash = HexBytes(
            "0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196"
        )
        signatures = HexBytes(
            "0x00000000000000000000000005c85ab5b09eb8a55020d72daf6091e04e264af90000000000000000000000"
            "000000000000000000000000000000000000000000015dccf9f1375cee56331a67867a0b05a828894c2b76de"
            "e84546ec663997d7548257cb2d606087ee7590b966e958d97a65528ae941a0f7e5050949f618629509c81b"
        )

        s1, s2 = SafeSignature.parse_signature(signatures, safe_tx_hash)
        self.assertEqual(s1.owner, owner_1)
        self.assertEqual(s1.signature_type, SafeSignatureType.APPROVED_HASH)
        self.assertIsInstance(s1, SafeSignatureApprovedHash)
        self.assertEqual(s2.signature_type, SafeSignatureType.EOA)
        self.assertEqual(s2.owner, owner_2)
        self.assertTrue(s2.is_valid())
        self.assertIsInstance(s2, SafeSignatureEOA)

    def test_parse_signature_with_trailing_zeroes(self):
        signatures = HexBytes(
            "0x9173a0b0895c28cdc82729f0a66e3645820a2e395cadad588463ab483e42b3df6e8b05d258e58c5255136"
            "0e032733b507f731001cce6b5391b7750439c8cffc020000000000000000000000000dc5299b629ef24fdec"
            "fbb240c00fc79fabb9cf9700000000000000000000000000000000000000000000000000000000000000000"
            "1000000000000000000000000000000000000000000000000000000000000"
        )
        parsed_signatures = SafeSignature.parse_signature(signatures, "")
        self.assertEqual(len(parsed_signatures), 2)
        self.assertEqual(
            parsed_signatures[0].signature_type, SafeSignatureType.ETH_SIGN
        )
        self.assertEqual(
            parsed_signatures[1].signature_type, SafeSignatureType.APPROVED_HASH
        )

    def test_parse_signature_empty(self):
        safe_tx_hash = Web3.keccak(text="Legoshi")
        for value in (b"", "", None):
            self.assertEqual(SafeSignature.parse_signature(value, safe_tx_hash), [])


class TestSafeContractSignature(SafeTestCaseMixin, TestCase):
    def test_contract_signature(self):
        owner_1 = self.ethereum_test_account
        safe = self.deploy_test_safe_v1_1_1(
            owners=[owner_1.address], initial_funding_wei=Web3.toWei(0.01, "ether")
        )
        safe_contract = safe.get_contract()
        safe_tx_hash = Web3.keccak(text="test")
        signature_r = HexBytes(safe.address.replace("0x", "").rjust(64, "0"))
        signature_s = HexBytes(
            "0" * 62 + "41"
        )  # Position of end of signature `0x41 == 65`
        signature_v = HexBytes("00")
        contract_signature = encode_single("bytes", b"")
        signature = signature_r + signature_s + signature_v + contract_signature

        safe_signature = SafeSignature.parse_signature(signature, safe_tx_hash)[0]
        self.assertFalse(safe_signature.is_valid(self.ethereum_client, None))

        # Check with previously signedMessage
        tx = safe_contract.functions.signMessage(safe_tx_hash).build_transaction(
            {"from": safe.address}
        )
        safe_tx = safe.build_multisig_tx(safe.address, 0, tx["data"])
        safe_tx.sign(owner_1.key)
        safe_tx.execute(owner_1.key)

        safe_signature = SafeSignature.parse_signature(signature, safe_tx_hash)[0]
        self.assertTrue(safe_signature.is_valid(self.ethereum_client, None))
        self.assertIsInstance(safe_signature, SafeSignatureContract)

        # Check with crafted signature
        safe_tx_hash_2 = Web3.keccak(text="test2")
        safe_signature = SafeSignature.parse_signature(signature, safe_tx_hash_2)[0]
        self.assertFalse(safe_signature.is_valid(self.ethereum_client, None))

        safe_tx_hash_2_message_hash = safe_contract.functions.getMessageHash(
            safe_tx_hash_2
        ).call()
        contract_signature = owner_1.signHash(safe_tx_hash_2_message_hash)["signature"]
        encoded_contract_signature = encode_single(
            "bytes", contract_signature
        )  # It will add size of bytes
        # `32` bytes with the abi encoded size of array. 65 bytes will be padded to next multiple of 32 -> 96
        # 96 - 65 = `31`
        self.assertEqual(
            len(encoded_contract_signature), len(contract_signature) + 32 + 31
        )
        crafted_signature = (
            signature_r + signature_s + signature_v + encoded_contract_signature
        )
        safe_signature = SafeSignature.parse_signature(
            crafted_signature, safe_tx_hash_2
        )[0]
        self.assertEqual(contract_signature, safe_signature.contract_signature)
        self.assertTrue(safe_signature.is_valid(self.ethereum_client, None))

    def test_contract_multiple_signatures(self):
        """
        Test decode of multiple `CONTRACT_SIGNATURE` together
        """
        owner_1 = self.ethereum_test_account
        safe = self.deploy_test_safe_v1_1_1(
            owners=[owner_1.address], initial_funding_wei=Web3.toWei(0.01, "ether")
        )
        safe_contract = safe.get_contract()
        safe_tx_hash = Web3.keccak(text="test")

        tx = safe_contract.functions.signMessage(safe_tx_hash).build_transaction(
            {"from": safe.address}
        )
        safe_tx = safe.build_multisig_tx(safe.address, 0, tx["data"])
        safe_tx.sign(owner_1.key)
        safe_tx.execute(owner_1.key)

        # Check multiple signatures. In this case we reuse signatures for the same owner, it won't make sense
        # in real life
        signature_r_1 = HexBytes(safe.address.replace("0x", "").rjust(64, "0"))
        signature_s_1 = HexBytes(
            "0" * 62 + "82"
        )  # Position of end of signature `0x82 == (65 * 2)`
        signature_v_1 = HexBytes("00")
        contract_signature_1 = b""
        encoded_contract_signature_1 = encode_single("bytes", contract_signature_1)

        signature_r_2 = HexBytes(safe.address.replace("0x", "").rjust(64, "0"))
        signature_s_2 = HexBytes(
            "0" * 62 + "c2"
        )  # Position of end of signature `0xc2 == (65 * 2) + 64`
        signature_v_2 = HexBytes("00")
        safe_tx_hash_message_hash = safe_contract.functions.getMessageHash(
            safe_tx_hash
        ).call()
        contract_signature_2 = owner_1.signHash(safe_tx_hash_message_hash)["signature"]
        encoded_contract_signature_2 = encode_single(
            "bytes", contract_signature_2
        )  # It will add size of bytes

        signature = (
            signature_r_1
            + signature_s_1
            + signature_v_1
            + signature_r_2
            + signature_s_2
            + signature_v_2
            + encoded_contract_signature_1
            + encoded_contract_signature_2
        )

        count = 0
        for safe_signature, contract_signature in zip(
            SafeSignature.parse_signature(signature, safe_tx_hash),
            [contract_signature_1, contract_signature_2],
        ):
            self.assertEqual(safe_signature.contract_signature, contract_signature)
            self.assertTrue(safe_signature.is_valid(self.ethereum_client, None))
            self.assertEqual(
                safe_signature.signature_type, SafeSignatureType.CONTRACT_SIGNATURE
            )
            # Test exported signature
            exported_signature = SafeSignature.parse_signature(
                safe_signature.export_signature(), safe_tx_hash
            )[0]
            self.assertEqual(
                exported_signature.contract_signature, safe_signature.contract_signature
            )
            self.assertTrue(exported_signature.is_valid(self.ethereum_client, None))
            count += 1
        self.assertEqual(count, 2)
