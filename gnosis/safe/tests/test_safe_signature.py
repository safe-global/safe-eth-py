import logging

from django.test import TestCase

from eth_abi import encode_single
from eth_abi.packed import encode_single_packed
from eth_account import Account
from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.contracts import get_safe_contract

from ..safe_signature import SafeContractSignature, SafeSignature
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestSignature(TestCase):
    def test_contract_signature(self):
        owner = '0x05c85Ab5B09Eb8A55020d72daf6091E04e264af9'
        safe_tx_hash = HexBytes('0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196')
        signature = HexBytes('0x00000000000000000000000005c85ab5b09eb8a55020d72daf6091e04e264af900000000000000000000000'
                             '0000000000000000000000000000000000000000000')
        safe_signature = SafeSignature(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)

    def test_approved_hash_signature(self):
        owner = '0x05c85Ab5B09Eb8A55020d72daf6091E04e264af9'
        safe_tx_hash = HexBytes('0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196')
        signature = HexBytes('0x00000000000000000000000005c85ab5b09eb8a55020d72daf6091e04e264af900000000000000000000000'
                             '0000000000000000000000000000000000000000001')
        safe_signature = SafeSignature(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)

    def test_eth_sign_signature(self):
        account = Account.create()
        owner = account.address
        safe_tx_hash = HexBytes('0x123477d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf195')
        message = defunct_hash_message(primitive=safe_tx_hash)
        signature = account.signHash(message)['signature']
        signature = signature[:64] + HexBytes(signature[64] + 4)  # Add 4 to v
        safe_signature = SafeSignature(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)

    def test_eoa_signature(self):
        owner = '0xADb7CB706e9A1bd9F96a397da340bF34a9984E1E'
        safe_tx_hash = HexBytes('0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196')
        signature = HexBytes('0x5dccf9f1375cee56331a67867a0b05a828894c2b76dee84546ec663997d7548257cb2d606087ee7590b966e'
                             '958d97a65528ae941a0f7e5050949f618629509c81b')
        safe_signature = SafeSignature(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)

        account = Account.create()
        owner = account.address
        safe_tx_hash = HexBytes('0x123477d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf195')
        signature = account.signHash(safe_tx_hash)['signature']
        safe_signature = SafeSignature(signature, safe_tx_hash)
        self.assertEqual(safe_signature.owner, owner)

    def test_defunct_hash_message(self):
        safe_tx_hash = HexBytes('0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196')
        ethereum_signed_message = '\x19Ethereum Signed Message:\n32'
        encoded_message = encode_single_packed('(string,bytes32)',
                                               (ethereum_signed_message, HexBytes(safe_tx_hash)))
        encoded_hash = Web3.keccak(encoded_message)
        self.assertEqual(encoded_hash, defunct_hash_message(primitive=safe_tx_hash))

    def test_parse_signatures(self):
        owner_1 = '0x05c85Ab5B09Eb8A55020d72daf6091E04e264af9'
        owner_2 = '0xADb7CB706e9A1bd9F96a397da340bF34a9984E1E'
        safe_tx_hash = HexBytes('0x4c9577d1b1b8dec52329a983ae26238b65f74b7dd9fb28d74ad9548e92aaf196')
        signatures = HexBytes('0x00000000000000000000000005c85ab5b09eb8a55020d72daf6091e04e264af90000000000000000000000'
                              '000000000000000000000000000000000000000000015dccf9f1375cee56331a67867a0b05a828894c2b76de'
                              'e84546ec663997d7548257cb2d606087ee7590b966e958d97a65528ae941a0f7e5050949f618629509c81b')

        s1, s2 = SafeSignature.parse_signatures(signatures, safe_tx_hash)
        self.assertEqual(s1.owner, owner_1)
        self.assertEqual(s2.owner, owner_2)


class TestContractSignature(SafeTestCaseMixin, TestCase):
    def test_contract_signature(self):
        safe_account = self.ethereum_test_account
        safe = self.deploy_test_safe(owners=[safe_account.address], initial_funding_wei=Web3.toWei(0.01, 'ether'))
        safe_contract = get_safe_contract(self.ethereum_client.w3, safe.safe_address)
        safe_tx_hash = Web3.keccak(text='test')
        signature_r = HexBytes(safe.safe_address.replace('0x', '').rjust(64, '0'))
        signature_s = HexBytes('0' * 62 + '41')  # Position of end of signature
        signature_v = HexBytes('00')
        contract_signature = HexBytes('0' * 64)
        signature = signature_r + signature_s + signature_v + contract_signature

        safe_signature = SafeContractSignature(signature, safe_tx_hash, self.ethereum_client)
        self.assertFalse(safe_signature.ok)

        # Approve the hash
        tx = safe_contract.functions.approveHash(
            safe_tx_hash
        ).buildTransaction({'from': safe_account.address})
        self.ethereum_client.send_unsigned_transaction(tx, private_key=safe_account.key)

        safe_signature = SafeContractSignature(signature, safe_tx_hash, self.ethereum_client)
        self.assertFalse(safe_signature.ok)

        # Test with an owner signature
        safe_tx_hash_2 = Web3.keccak(text='test2')
        safe_tx_hash_2_message_hash = safe_contract.functions.getMessageHash(safe_tx_hash_2).call()
        safe_signature = SafeContractSignature(signature, safe_tx_hash_2, self.ethereum_client)
        self.assertFalse(safe_signature.ok)
        contract_signature = encode_single('bytes', safe_account.signHash(safe_tx_hash_2_message_hash)['signature'])
        signature = signature_r + signature_s + signature_v + contract_signature

        safe_signature = SafeContractSignature(signature, safe_tx_hash_2, self.ethereum_client)
        self.assertTrue(safe_signature.ok)
