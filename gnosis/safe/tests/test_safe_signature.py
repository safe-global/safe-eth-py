import logging

from django.test import TestCase

from eth_abi import encode_single
from eth_abi.packed import encode_single_packed
from eth_account import Account
from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes
from web3 import Web3

from .. import Safe
from ..safe_signature import SafeSignature, SafeSignatureType
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
        owner_1 = self.ethereum_test_account
        deployed_safe = self.deploy_test_safe(owners=[owner_1.address],
                                              initial_funding_wei=Web3.toWei(0.01, 'ether'))
        safe = Safe(deployed_safe.safe_address, self.ethereum_client)
        safe_contract = safe.get_contract()
        safe_tx_hash = Web3.keccak(text='test')
        signature_r = HexBytes(safe.address.replace('0x', '').rjust(64, '0'))
        signature_s = HexBytes('0' * 62 + '41')  # Position of end of signature `0x41 == 65`
        signature_v = HexBytes('00')
        contract_signature = encode_single('bytes', b'')
        signature = signature_r + signature_s + signature_v + contract_signature

        safe_signature = next(SafeSignature.parse_signatures(signature, safe_tx_hash))
        self.assertFalse(safe_signature.is_valid(self.ethereum_client, None))

        # Check with previously signedMessage
        tx = safe_contract.functions.signMessage(
            safe_tx_hash
        ).buildTransaction({'from': safe.address})
        safe_tx = safe.build_multisig_tx(safe.address, 0, tx['data'])
        safe_tx.sign(owner_1.key)
        safe_tx.execute(owner_1.key)

        safe_signature = next(SafeSignature.parse_signatures(signature, safe_tx_hash))
        self.assertTrue(safe_signature.is_valid(self.ethereum_client, None))

        # Check with crafted signature
        safe_tx_hash_2 = Web3.keccak(text='test2')
        safe_signature = next(SafeSignature.parse_signatures(signature, safe_tx_hash_2))
        self.assertFalse(safe_signature.is_valid(self.ethereum_client, None))

        safe_tx_hash_2_message_hash = safe_contract.functions.getMessageHash(safe_tx_hash_2).call()
        contract_signature = owner_1.signHash(safe_tx_hash_2_message_hash)['signature']
        encoded_contract_signature = encode_single('bytes', contract_signature)  # It will add size of bytes
        # `32` bytes with the abi encoded size of array. 65 bytes will be padded to next multiple of 32 -> 96
        # 96 - 65 = `31`
        self.assertEqual(len(encoded_contract_signature), len(contract_signature) + 32 + 31)
        crafted_signature = signature_r + signature_s + signature_v + encoded_contract_signature
        safe_signature = next(SafeSignature.parse_signatures(crafted_signature, safe_tx_hash_2))
        self.assertEqual(contract_signature, safe_signature.contract_signature)
        self.assertTrue(safe_signature.is_valid(self.ethereum_client, None))

    def test_contract_multiple_signatures(self):
        """
        Test decode of multiple `CONTRACT_SIGNATURE` together
        """
        owner_1 = self.ethereum_test_account
        deployed_safe = self.deploy_test_safe(owners=[owner_1.address],
                                              initial_funding_wei=Web3.toWei(0.01, 'ether'))
        safe = Safe(deployed_safe.safe_address, self.ethereum_client)
        safe_contract = safe.get_contract()
        safe_tx_hash = Web3.keccak(text='test')

        tx = safe_contract.functions.signMessage(
            safe_tx_hash
        ).buildTransaction({'from': safe.address})
        safe_tx = safe.build_multisig_tx(safe.address, 0, tx['data'])
        safe_tx.sign(owner_1.key)
        safe_tx.execute(owner_1.key)

        # Check multiple signatures. In this case we reuse signatures for the same owner, it won't make sense
        # in real life
        signature_r_1 = HexBytes(safe.address.replace('0x', '').rjust(64, '0'))
        signature_s_1 = HexBytes('0' * 62 + '82')  # Position of end of signature `0x82 == (65 * 2)`
        signature_v_1 = HexBytes('00')
        contract_signature_1 = b''
        encoded_contract_signature_1 = encode_single('bytes', contract_signature_1)

        signature_r_2 = HexBytes(safe.address.replace('0x', '').rjust(64, '0'))
        signature_s_2 = HexBytes('0' * 62 + 'c2')  # Position of end of signature `0xc2 == (65 * 2) + 64`
        signature_v_2 = HexBytes('00')
        safe_tx_hash_message_hash = safe_contract.functions.getMessageHash(safe_tx_hash).call()
        contract_signature_2 = owner_1.signHash(safe_tx_hash_message_hash)['signature']
        encoded_contract_signature_2 = encode_single('bytes', contract_signature_2)  # It will add size of bytes

        signature = (signature_r_1 + signature_s_1 + signature_v_1 +
                     signature_r_2 + signature_s_2 + signature_v_2 +
                     encoded_contract_signature_1 + encoded_contract_signature_2)

        count = 0
        for safe_signature, contract_signature in zip(SafeSignature.parse_signatures(signature, safe_tx_hash),
                                                      [contract_signature_1, contract_signature_2]):
            self.assertEqual(safe_signature.contract_signature, contract_signature)
            self.assertTrue(safe_signature.is_valid(self.ethereum_client, None))
            self.assertEqual(safe_signature.signature_type, SafeSignatureType.CONTRACT_SIGNATURE)
            count += 1
        self.assertEqual(count, 2)
