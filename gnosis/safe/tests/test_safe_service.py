import logging

from django.conf import settings
from django.test import TestCase
from django_eth.constants import NULL_ADDRESS
from django_eth.tests.factories import get_eth_address_with_key
from hexbytes import HexBytes

from ..contracts import get_safe_contract
from ..safe_service import (GasPriceTooLow, InvalidMasterCopyAddress,
                            NotEnoughFundsForMultisigTx, SafeServiceProvider)
from .factories import deploy_example_erc20, deploy_safe, generate_safe
from .safe_test_case import TestCaseWithSafeContractMixin

logger = logging.getLogger(__name__)

GAS_PRICE = settings.SAFE_GAS_PRICE


class TestSafeService(TestCase, TestCaseWithSafeContractMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_safe_tests()

    def test_send_multisig_tx(self):
        # Create Safe
        w3 = self.w3
        funder = w3.eth.accounts[0]
        owners_with_keys = [get_eth_address_with_key(), get_eth_address_with_key()]
        # Signatures must be sorted!
        owners_with_keys.sort(key=lambda x: x[0].lower())
        owners = [x[0] for x in owners_with_keys]
        keys = [x[1] for x in owners_with_keys]
        threshold = len(owners_with_keys)

        safe_creation = generate_safe(self.safe_service, owners=owners, threshold=threshold)
        my_safe_address = deploy_safe(w3, safe_creation, funder)

        # The balance we will send to the safe
        safe_balance = w3.toWei(0.01, 'ether')

        # Send something to the owner[0], who will be sending the tx
        owner0_balance = safe_balance
        w3.eth.waitForTransactionReceipt(w3.eth.sendTransaction({
            'from': funder,
            'to': owners[0],
            'value': owner0_balance
        }))

        my_safe_contract = get_safe_contract(w3, my_safe_address)

        to = funder
        value = safe_balance // 2
        data = HexBytes(0x00)
        operation = 0
        safe_tx_gas = 100000
        data_gas = 300000
        gas_price = 1
        gas_token = NULL_ADDRESS
        refund_receiver = NULL_ADDRESS
        nonce = self.safe_service.retrieve_nonce(my_safe_address)
        safe_multisig_tx_hash = self.safe_service.get_hash_for_safe_tx(safe_address=my_safe_address,
                                                                       to=to,
                                                                       value=value,
                                                                       data=data,
                                                                       operation=operation,
                                                                       safe_tx_gas=safe_tx_gas,
                                                                       data_gas=data_gas,
                                                                       gas_price=gas_price,
                                                                       gas_token=gas_token,
                                                                       refund_receiver=refund_receiver,
                                                                       nonce=nonce)

        # Just to make sure we are not miscalculating tx_hash
        contract_multisig_tx_hash = my_safe_contract.functions.getTransactionHash(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            nonce).call()

        self.assertEqual(safe_multisig_tx_hash, contract_multisig_tx_hash)

        signatures = [w3.eth.account.signHash(safe_multisig_tx_hash, private_key) for private_key in keys]
        signature_pairs = [(s['v'], s['r'], s['s']) for s in signatures]
        signatures_packed = self.safe_service.signatures_to_bytes(signature_pairs)

        # {bytes32 r}{bytes32 s}{uint8 v} = 65 bytes
        self.assertEqual(len(signatures_packed), 65 * len(owners))

        # Recover key is now a private function
        # Make sure the contract retrieves the same owners
        # for i, owner in enumerate(owners):
        #    recovered_owner = my_safe_contract.functions.recoverKey(safe_multisig_tx_hash, signatures_packed, i).call()
        #    self.assertEqual(owner, recovered_owner)

        self.assertTrue(self.safe_service.check_hash(safe_multisig_tx_hash, signatures_packed, owners))

        # Check owners are the same
        contract_owners = my_safe_contract.functions.getOwners().call()
        self.assertEqual(set(contract_owners), set(owners))
        self.assertEqual(w3.eth.getBalance(owners[0]), owner0_balance)

        valid_master_copy_addresses = self.safe_service.valid_master_copy_addresses
        self.safe_service.valid_master_copy_addresses = []
        with self.assertRaises(InvalidMasterCopyAddress):
            self.safe_service.send_multisig_tx(
                my_safe_address,
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                data_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signatures_packed,
                tx_sender_private_key=keys[0],
                tx_gas_price=GAS_PRICE,
            )

        self.safe_service.valid_master_copy_addresses = valid_master_copy_addresses

        with self.assertRaises(NotEnoughFundsForMultisigTx):
            self.safe_service.send_multisig_tx(
                my_safe_address,
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                data_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signatures_packed,
                tx_sender_private_key=keys[0],
                tx_gas_price=GAS_PRICE,
            )

        # Send something to the safe
        w3.eth.waitForTransactionReceipt(w3.eth.sendTransaction({
            'from': funder,
            'to': my_safe_address,
            'value': safe_balance
        }))

        sent_tx_hash, tx = self.safe_service.send_multisig_tx(
            my_safe_address,
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures_packed,
            tx_sender_private_key=keys[0],
            tx_gas_price=GAS_PRICE,
        )

        tx_receipt = w3.eth.waitForTransactionReceipt(sent_tx_hash)
        self.assertTrue(tx_receipt['status'])
        owner0_new_balance = w3.eth.getBalance(owners[0])
        gas_used = tx_receipt['gasUsed']
        gas_cost = gas_used * GAS_PRICE
        estimated_payment = (data_gas + gas_used) * gas_price
        real_payment = owner0_new_balance - (owner0_balance - gas_cost)
        # Estimated payment will be bigger, because it uses all the tx gas. Real payment only uses gas left
        # in the point of calculation of the payment, so it will be slightly lower
        self.assertTrue(estimated_payment > real_payment > 0)
        self.assertTrue(owner0_new_balance > owner0_balance - tx['gas'] * GAS_PRICE)
        self.assertEqual(self.safe_service.retrieve_nonce(my_safe_address), 1)

    def test_send_multisig_tx_gas_token(self):
        # Create safe with one owner, fund the safe and the owner with `safe_balance`
        owner, owner_key = get_eth_address_with_key()
        receiver, _ = get_eth_address_with_key()
        threshold = 1
        funder = self.w3.eth.accounts[0]
        safe_balance = self.w3.toWei(0.01, 'ether')
        self.w3.eth.waitForTransactionReceipt(self.w3.eth.sendTransaction({
            'from': funder,
            'to': owner,
            'value': safe_balance
        }))
        safe_creation = generate_safe(self.safe_service, owners=[owner], threshold=threshold)
        my_safe_address = deploy_safe(self.w3, safe_creation, funder, initial_funding_wei=safe_balance)

        # Give erc20 tokens to the safe
        amount_token = int(1e18)
        funder = self.w3.eth.accounts[0]
        erc20_contract = deploy_example_erc20(self.w3, amount_token, my_safe_address, funder)
        safe_token_balance = self.ethereum_service.get_erc20_balance(my_safe_address, erc20_contract.address)
        self.assertEqual(safe_token_balance, amount_token)

        signature_packed = self.safe_service.signature_to_bytes((1, int(owner, 16), 0))

        to = receiver
        value = safe_balance
        data = HexBytes(0x00)
        operation = 0
        safe_tx_gas = 100000
        data_gas = 300000
        gas_price = 2
        gas_token = erc20_contract.address
        refund_receiver = NULL_ADDRESS

        self.safe_service.send_multisig_tx(
            my_safe_address,
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signature_packed,
            tx_sender_private_key=owner_key,
            tx_gas_price=GAS_PRICE,
        )

        safe_token_balance = self.ethereum_service.get_erc20_balance(my_safe_address, erc20_contract.address)

        # Token was used for tx gas costs. Sender must have some tokens now and safe should have less
        self.assertLess(safe_token_balance, amount_token)
        owner_token_balance = self.ethereum_service.get_erc20_balance(owner, erc20_contract.address)
        self.assertGreater(owner_token_balance, 0)

        # All ether on safe was transferred to receiver
        receiver_balance = self.w3.eth.getBalance(receiver)
        self.assertEqual(receiver_balance, safe_balance)

    def test_check_proxy_code(self):
        proxy_contract_address = self.safe_service.deploy_proxy_contract(deployer_account=self.w3.eth.accounts[0])
        self.assertTrue(self.safe_service.check_proxy_code(proxy_contract_address))

        safe_contract_address = self.safe_service.deploy_master_contract(deployer_account=self.w3.eth.accounts[0])
        self.assertFalse(self.safe_service.check_proxy_code(safe_contract_address))

    def test_estimate_tx_data_gas(self):
        safe_address = self.safe_service.deploy_proxy_contract(deployer_account=self.w3.eth.accounts[0])
        to, _ = get_eth_address_with_key()
        value = int('abc', 16)
        data = HexBytes('0xabcdef')
        operation = 1
        gas_token = NULL_ADDRESS
        estimate_tx_gas = int('ccdd', 16)
        data_gas = self.safe_service.estimate_tx_data_gas(safe_address, to, value, data, operation, gas_token,
                                                          estimate_tx_gas)
        self.assertGreater(data_gas, 0)

        data = HexBytes('0xabcdefbb')  # A byte that was 00 now is bb, so -4 + 68
        data_gas2 = self.safe_service.estimate_tx_data_gas(safe_address, to, value, data, operation, gas_token,
                                                           estimate_tx_gas)
        self.assertEqual(data_gas2, data_gas + 68 - 4)

    def test_estimate_tx_gas(self):
        safe_address = self.safe_service.deploy_proxy_contract(deployer_account=self.w3.eth.accounts[0])
        to, _ = get_eth_address_with_key()
        value = int('abc', 16)
        data = HexBytes('0xabcdef')
        operation = 1
        data_gas = self.safe_service.estimate_tx_gas(safe_address, to, value, data, operation)
        self.assertGreater(data_gas, 0)

    def test_estimate_tx_operational_gas(self):
        for threshold in range(2, 5):
            safe_creation = generate_safe(self.safe_service, number_owners=6, threshold=threshold)
            proxy_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0])
            tx_signature_gas_estimation = self.safe_service.estimate_tx_operational_gas(proxy_address, 0)
            self.assertGreaterEqual(tx_signature_gas_estimation, 20000)

    def test_hash_safe_multisig_tx(self):
        expected_hash = HexBytes('0xc9d69a2350aede7978fdee58e702647e4bbdc82168577aa4a43b66ad815c6d1a')
        tx_hash = self.safe_service.get_hash_for_safe_tx('0x692a70d2e424a56d2c6c27aa97d1a86395877b3a',
                                                         '0x5AC255889882aaB35A2aa939679E3F3d4Cea221E',
                                                         5000000,
                                                         HexBytes('0x00'),
                                                         0,
                                                         50000,
                                                         100,
                                                         10000,
                                                         '0x' + '0' * 40,
                                                         '0x' + '0' * 40,
                                                         67)
        self.assertEqual(expected_hash, tx_hash)

        expected_hash = HexBytes('0x8ca8db91d72b379193f6e229eb2dff0d0621b6ef452d90638ee3206e9b7349b3')
        tx_hash = self.safe_service.get_hash_for_safe_tx('0x692a70d2e424a56d2c6c27aa97d1a86395877b3a',
                                                         '0x' + '0' * 40,
                                                         80000000,
                                                         HexBytes('0x562944'),
                                                         2,
                                                         54522,
                                                         773,
                                                         22000000,
                                                         '0x' + '0' * 40,
                                                         '0x' + '0' * 40,
                                                         257000)
        self.assertEqual(expected_hash, tx_hash)

        # Expected hash must be the same calculated by `getTransactionHash` of the contract
        expected_hash = self.safe_contract.functions.getTransactionHash(
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
        tx_hash = self.safe_service.get_hash_for_safe_tx(self.safe_contract_address,
                                                         '0x5AC255889882aaB35A2aa939679E3F3d4Cea221E',
                                                         5212459,
                                                         HexBytes(0x00),
                                                         1,
                                                         123456,
                                                         122,
                                                         12345,
                                                         '0x' + '2' * 40,
                                                         '0x' + '2' * 40,
                                                         10789)
        self.assertEqual(HexBytes(expected_hash), tx_hash)

    def test_is_master_copy_deployed(self):
        self.assertTrue(self.safe_service.is_master_copy_deployed())
        random_address, _ = get_eth_address_with_key()
        master_copy = self.safe_service.master_copy_address
        self.safe_service.master_copy_address = random_address
        self.assertFalse(self.safe_service.is_master_copy_deployed())
        self.safe_service.master_copy_address = master_copy

    def test_provider_singleton(self):
        safe_service1 = SafeServiceProvider()
        safe_service2 = SafeServiceProvider()
        self.assertEqual(safe_service1, safe_service2)

    def test_retrieve_master_copy_address(self):
        proxy_address = self.safe_service.deploy_proxy_contract(deployer_account=self.w3.eth.accounts[0])
        self.assertEqual(self.safe_service.retrieve_master_copy_address(proxy_address),
                         self.safe_service.master_copy_address)

    def test_retrieve_is_owner(self):
        safe_creation = generate_safe(self.safe_service, number_owners=3, threshold=2)
        proxy_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0])
        for owner in safe_creation.owners:
            self.assertTrue(self.safe_service.retrieve_is_owner(proxy_address, owner))

        random_address, _ = get_eth_address_with_key()
        self.assertFalse(self.safe_service.retrieve_is_owner(proxy_address, random_address))

    def test_retrieve_nonce(self):
        safe_creation = generate_safe(self.safe_service, number_owners=3, threshold=2)
        proxy_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0])
        self.assertEqual(self.safe_service.retrieve_nonce(proxy_address), 0)

    def test_retrieve_owners(self):
        safe_creation = generate_safe(self.safe_service, number_owners=3, threshold=2)
        proxy_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0])
        owners = self.safe_service.retrieve_owners(proxy_address)
        self.assertEqual(set(owners), set(safe_creation.owners))

    def test_retrieve_threshold(self):
        safe_creation = generate_safe(self.safe_service, number_owners=3, threshold=2)
        proxy_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0])
        self.assertEqual(self.safe_service.retrieve_threshold(proxy_address), 2)

    def test_token_balance(self):
        funder = self.w3.eth.accounts[0]
        amount = 200
        deployed_erc20 = deploy_example_erc20(self.w3, amount, funder, deployer=funder)

        safe_creation = generate_safe(self.safe_service, number_owners=3, threshold=2)
        proxy_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0])

        balance = self.ethereum_service.get_erc20_balance(proxy_address, deployed_erc20.address)
        self.assertEqual(balance, 0)

        deployed_erc20.functions.transfer(proxy_address, amount).transact({'from': funder})
        balance = self.ethereum_service.get_erc20_balance(proxy_address, deployed_erc20.address)
        self.assertEqual(balance, amount)

    # TODO Test approve tx from another contract
    def test_send_previously_approved_tx(self):
        owners = self.w3.eth.accounts[:4]
        safe_creation = generate_safe(self.safe_service, owners=owners, threshold=2)
        safe_address = deploy_safe(self.w3, safe_creation, self.w3.eth.accounts[0],
                                   initial_funding_wei=self.w3.toWei(0.01, 'ether'))
        safe_instance = get_safe_contract(self.w3, safe_address)

        to, _ = get_eth_address_with_key()
        value = self.w3.toWei(0.001, 'ether')
        data = b''
        operation = 0
        safe_tx_gas = 500000
        data_gas = 500000
        gas_price = 1
        gas_token = NULL_ADDRESS
        refund_receiver = NULL_ADDRESS
        nonce = self.safe_service.retrieve_nonce(safe_address)

        self.assertEqual(nonce, 0)

        safe_tx_hash = self.safe_service.get_hash_for_safe_tx(safe_address, to, value, data, operation, safe_tx_gas,
                                                              data_gas, gas_price, gas_token, refund_receiver, nonce)

        safe_tx_contract_hash = safe_instance.functions.getTransactionHash(to, value, data, operation,
                                                                           safe_tx_gas, data_gas, gas_price, gas_token,
                                                                           refund_receiver, nonce).call()

        self.assertEqual(safe_tx_hash, safe_tx_contract_hash)

        safe_instance.functions.approveHash(safe_tx_hash).transact({'from': owners[0]})
        safe_instance.functions.approveHash(safe_tx_hash).transact({'from': owners[1]})

        for owner in (owners[0], owners[1]):
            is_approved = self.safe_service.retrieve_is_hash_approved(safe_address, owner, safe_tx_hash)
            self.assertTrue(is_approved)

        # Prepare signatures. v must be 1 for previously signed and r the owner
        signatures = (1, int(owners[0], 16), 0), (1, int(owners[1], 16), 0)
        signature_bytes = self.safe_service.signatures_to_bytes(signatures)

        self.safe_service.send_multisig_tx(safe_address, to, value, data, operation, safe_tx_gas,
                                           data_gas, gas_price, gas_token, refund_receiver, signature_bytes)

        balance = self.w3.eth.getBalance(to)
        self.assertEqual(value, balance)
