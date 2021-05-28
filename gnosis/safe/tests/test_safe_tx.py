import logging

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes

from ...eth.contracts import get_safe_contract
from ..exceptions import NotEnoughSafeTransactionGas, SignaturesDataTooShort
from ..multi_send import MultiSendOperation, MultiSendTx
from ..safe import Safe, SafeOperation
from ..safe_tx import SafeTx
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestSafeTx(SafeTestCaseMixin, TestCase):
    def test_multi_send_safe_tx(self):
        owners = [Account.create() for _ in range(2)]
        owner_addresses = [owner.address for owner in owners]
        threshold = 1
        safe_creation = self.deploy_test_safe(owners=owner_addresses, threshold=threshold,
                                              initial_funding_wei=self.w3.toWei(0.1, 'ether'))
        safe_address = safe_creation.safe_address
        safe = Safe(safe_address, self.ethereum_client)
        safe_contract = safe.get_contract()
        to = self.multi_send_contract.address
        value = 0
        safe_tx_gas = 600000
        base_gas = 200000

        # Atomic swap the owner of a Safe
        new_owner = Account.create()
        owner_to_remove = owners[-1]
        prev_owner = owners[-2]
        owners_expected = [x.address for x in owners[:-1]] + [new_owner.address]
        new_threshold = threshold + 1
        data = HexBytes(safe_contract.functions.addOwnerWithThreshold(new_owner.address,
                                                                      new_threshold).buildTransaction({'gas': 0})['data'])
        data_2 = HexBytes(safe_contract.functions.removeOwner(prev_owner.address, owner_to_remove.address,
                                                              new_threshold).buildTransaction({'gas': 0})['data'])

        multisend_txs = [MultiSendTx(MultiSendOperation.CALL, safe_address, value, d) for d in (data, data_2)]
        safe_multisend_data = self.multi_send.build_tx_data(multisend_txs)
        safe_tx = SafeTx(self.ethereum_client, safe_address, to,
                         0, safe_multisend_data, SafeOperation.DELEGATE_CALL.value,
                         safe_tx_gas, base_gas, self.gas_price, None, None, safe_nonce=0)
        safe_tx.sign(owners[0].key)

        self.assertEqual(safe_tx.call(tx_sender_address=self.ethereum_test_account.address), 1)
        tx_hash, _ = safe_tx.execute(tx_sender_private_key=self.ethereum_test_account.key)
        self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        self.assertEqual(safe.retrieve_nonce(), 1)
        self.assertEqual(safe.retrieve_threshold(), new_threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners_expected)

    def test_send_safe_tx(self):
        owners = [Account.create() for _ in range(2)]
        owner_addresses = [owner.address for owner in owners]
        threshold = 1
        safe_creation = self.deploy_test_safe(owners=owner_addresses, threshold=threshold,
                                              initial_funding_wei=self.w3.toWei(0.1, 'ether'))
        safe_address = safe_creation.safe_address
        to = Account().create().address
        value = self.w3.toWei(0.01, 'ether')
        safe_tx_gas = 200000
        data_gas = 100000

        safe_tx = SafeTx(self.ethereum_client, safe_address, to, value, b'', 0, safe_tx_gas, data_gas, self.gas_price,
                         None, None, safe_nonce=0)

        with self.assertRaises(SignaturesDataTooShort):
            safe_tx.call(tx_sender_address=self.ethereum_test_account.address)

        # Check signing
        self.assertFalse(safe_tx.signers)
        safe_tx.sign(owners[0].key)
        self.assertIn(owners[0].address, safe_tx.signers)

        with self.assertRaises(NotEnoughSafeTransactionGas):
            safe_tx.call(tx_sender_address=self.ethereum_test_account.address, tx_gas=safe_tx_gas // 2)

        self.assertEqual(safe_tx.call(tx_sender_address=self.ethereum_test_account.address), 1)
        tx_hash, _ = safe_tx.execute(tx_sender_private_key=self.ethereum_test_account.key)
        self.ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        self.assertEqual(self.ethereum_client.get_balance(to), value)

        safe_tx.unsign(owners[0].address)
        self.assertFalse(safe_tx.signers)

    def test_sign_safe_tx(self):
        owners = [Account.create() for _ in range(3)]
        owners_unsorted = sorted(owners, key=lambda x: int(x.address, 16), reverse=True)
        owner_addresses = [owner.address for owner in owners_unsorted]
        threshold = 1
        safe_creation = self.deploy_test_safe(owners=owner_addresses, threshold=threshold,
                                              initial_funding_wei=self.w3.toWei(0.1, 'ether'))
        safe_address = safe_creation.safe_address
        to = Account().create().address
        value = self.w3.toWei(0.01, 'ether')

        safe_tx = SafeTx(self.ethereum_client, safe_address, to, value, b'', 0, 200000, 100000, self.gas_price,
                         None, None, safe_nonce=0)

        safe_tx.sign(owners_unsorted[0].key)
        safe_tx.sign(owners_unsorted[2].key)
        signers = [owner_addresses[0], owner_addresses[2]]

        self.assertEqual(safe_tx.signers, safe_tx.sorted_signers)
        self.assertNotEqual(signers, safe_tx.signers)
        self.assertEqual(set(signers), set(safe_tx.signers))
        self.assertEqual(len(safe_tx.signers), 2)

        safe_tx.sign(owners_unsorted[1].key)
        signers = owner_addresses
        self.assertEqual(safe_tx.signers, safe_tx.sorted_signers)
        self.assertNotEqual(signers, safe_tx.signers)
        self.assertEqual(set(signers), set(safe_tx.signers))
        self.assertEqual(len(safe_tx.signers), 3)

        # Sign again
        safe_tx.sign(owners_unsorted[0].key)
        self.assertEqual(len(safe_tx.signers), 3)

        # Sign again
        safe_tx.unsign(owners_unsorted[1].address)
        signers = [owner_addresses[0], owner_addresses[2]]
        self.assertEqual(set(signers), set(safe_tx.signers))
        self.assertEqual(len(safe_tx.signers), 2)

    def test_hash_safe_multisig_tx(self):
        # -------- Old version of the contract --------------------------
        expected_hash = HexBytes('0xc9d69a2350aede7978fdee58e702647e4bbdc82168577aa4a43b66ad815c6d1a')
        tx_hash = SafeTx(self.ethereum_client, '0x692a70d2e424a56d2c6c27aa97d1a86395877b3a',
                         '0x5AC255889882aaB35A2aa939679E3F3d4Cea221E',
                         5000000,
                         HexBytes('0x00'),
                         0,
                         50000,
                         100,
                         10000,
                         '0x' + '0' * 40,
                         '0x' + '0' * 40,
                         safe_nonce=67, safe_version='0.1.0').safe_tx_hash
        self.assertEqual(expected_hash, tx_hash)

        expected_hash = HexBytes('0x8ca8db91d72b379193f6e229eb2dff0d0621b6ef452d90638ee3206e9b7349b3')
        tx_hash = SafeTx(self.ethereum_client, '0x692a70d2e424a56d2c6c27aa97d1a86395877b3a',
                         '0x' + '0' * 40,
                         80000000,
                         HexBytes('0x562944'),
                         2,
                         54522,
                         773,
                         22000000,
                         '0x' + '0' * 40,
                         '0x' + '0' * 40,
                         safe_nonce=257000, safe_version='0.1.0').safe_tx_hash
        self.assertEqual(expected_hash, tx_hash)

        # -------- New version of the contract --------------------------
        expected_hash = HexBytes('0x7c60341f3e1b4483575f38e84e97d6b332a2dd55b9290f39e6e26eef29a04fe7')
        tx_hash = SafeTx(self.ethereum_client, '0x692a70D2e424a56D2C6C27aA97D1a86395877b3A',
                         '0x5AC255889882aaB35A2aa939679E3F3d4Cea221E',
                         5000000,
                         HexBytes('0x00'),
                         0,
                         50000,
                         100,
                         10000,
                         '0x' + '0' * 40,
                         '0x' + '0' * 40,
                         safe_nonce=67,
                         safe_version='1.0.0').safe_tx_hash
        self.assertEqual(expected_hash, tx_hash)

        expected_hash = HexBytes('0xf585279fd867c94738096f4eab964e9e202014d2f0d5155d751099ad85cbe504')
        tx_hash = SafeTx(self.ethereum_client, '0x692a70D2e424a56D2C6C27aA97D1a86395877b3A',
                         '0x' + '0' * 40,
                         80000000,
                         HexBytes('0x562944'),
                         2,
                         54522,
                         773,
                         22000000,
                         '0x' + '0' * 40,
                         '0x' + '0' * 40,
                         safe_nonce=257000,
                         safe_version='1.0.0').safe_tx_hash
        self.assertEqual(expected_hash, tx_hash)

        safe_create2_tx = self.deploy_test_safe()
        safe_address = safe_create2_tx.safe_address
        # Expected hash must be the same calculated by `getTransactionHash` of the contract
        expected_hash = get_safe_contract(self.ethereum_client.w3, safe_address).functions.getTransactionHash(
            '0x5AC255889882aaB35A2aa939679E3F3d4Cea221E',
            5212459,
            HexBytes(0x00),
            1,
            123456,
            122,
            12345,
            '0x' + '2' * 40,
            '0x' + '2' * 40,
            10789).call()
        safe_tx_hash = SafeTx(self.ethereum_client, safe_address,
                              '0x5AC255889882aaB35A2aa939679E3F3d4Cea221E',
                              5212459,
                              HexBytes(0x00),
                              1,
                              123456,
                              122,
                              12345,
                              '0x' + '2' * 40,
                              '0x' + '2' * 40,
                              safe_nonce=10789,
                              safe_version='1.0.0').safe_tx_hash
        self.assertEqual(HexBytes(expected_hash), safe_tx_hash)

    def test_hash_safe_multisig_tx_1_3(self):
        safe_address = '0x2B0b9cBDA3D7b0F760187c52A8FFB18C48E5d96A'
        expected_hash = '0x01d42a801ac44d3ebd43592be980dea0756d7f7b27d718d3016a42ea7ce85587'
        to = '0x79613FD49472C3C7a32188e45ff00e7bdC8a897d'
        data = HexBytes('0x1212')
        value = 2
        operation = 0
        safe_tx_gas = 0
        base_gas = 0
        gas_price = 0
        gas_token = '0xFA995c7a0d32A4e7497508a5C380369BE8dB49Db'
        refund_receiver = '0x6b92f5E5360bfCa8F5d3FcE65D87382967847983'
        safe_nonce = 17
        chain_id = 4  # Rinkeby
        safe_tx_hash = SafeTx(self.ethereum_client, safe_address,
                              to,
                              value,
                              data,
                              operation,
                              safe_tx_gas,
                              base_gas,
                              gas_price,
                              gas_token,
                              refund_receiver,
                              safe_nonce=safe_nonce,
                              safe_version='1.3.0',
                              chain_id=chain_id,
                              ).safe_tx_hash
        self.assertEqual(HexBytes(expected_hash), safe_tx_hash)

        # Test with ganache master copy contract v1.3.0
        chain_id = self.ethereum_client.w3.eth.chain_id
        safe_tx_hash = SafeTx(self.ethereum_client, self.safe_contract_V1_3_0_address,
                              to,
                              value,
                              data,
                              operation,
                              safe_tx_gas,
                              base_gas,
                              gas_price,
                              gas_token,
                              refund_receiver,
                              safe_nonce=safe_nonce,
                              safe_version='1.3.0',
                              chain_id=chain_id,
                              ).safe_tx_hash
        expected_hash = self.safe_contract_V1_3_0.functions.getTransactionHash(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            safe_nonce
        ).call()
        self.assertEqual(HexBytes(expected_hash), safe_tx_hash)
