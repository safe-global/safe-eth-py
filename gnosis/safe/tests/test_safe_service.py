import logging

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.utils import get_eth_address_with_key

from ..exceptions import CouldNotPayGasWithEther, CouldNotPayGasWithToken
from ..safe_service import SafeServiceProvider
from ..signatures import signature_to_bytes, signatures_to_bytes
from .safe_test_case import SafeTestCaseMixin
from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)


class TestSafeService(TestCase, SafeTestCaseMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_estimate_safe_creation(self):
        number_owners = 4
        gas_price = self.gas_price
        payment_token = NULL_ADDRESS
        safe_creation_estimate = self.safe_service.estimate_safe_creation(number_owners, gas_price, payment_token)
        self.assertGreater(safe_creation_estimate.gas_price, 0)
        self.assertGreater(safe_creation_estimate.gas, 0)
        self.assertGreater(safe_creation_estimate.payment, 0)

    def test_deploy_proxy_contract_with_nonce(self):
        salt_nonce = generate_salt_nonce()
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        payment_token = None
        private_key = self.ethereum_test_account.privateKey
        safe_create2_tx = self.safe_service.build_safe_create2_tx(salt_nonce, owners, threshold, self.gas_price,
                                                                  payment_token)
        # Send ether for safe deploying costs
        self.send_tx({
            'to': safe_create2_tx.safe_address,
            'value': safe_create2_tx.payment
        }, self.ethereum_test_account)

        tx_hash, _, safe_address = self.safe_service.deploy_proxy_contract_with_nonce(salt_nonce,
                                                                                      safe_create2_tx.safe_setup_data,
                                                                                      safe_create2_tx.gas,
                                                                                      self.gas_price,
                                                                                      deployer_private_key=private_key)
        receipt = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=20)
        self.assertEqual(receipt.status, 1)
        self.assertEqual(safe_address, safe_create2_tx.safe_address)
        self.assertEqual(set(self.safe_service.retrieve_owners(safe_address)), set(owners))

    def test_send_multisig_tx(self):
        # Create Safe
        w3 = self.w3
        funder_account = self.ethereum_test_account
        funder = funder_account.address
        owners_with_keys = [get_eth_address_with_key(), get_eth_address_with_key()]
        # Signatures must be sorted!
        owners_with_keys.sort(key=lambda x: x[0].lower())
        owners = [x[0] for x in owners_with_keys]
        keys = [x[1] for x in owners_with_keys]
        threshold = len(owners_with_keys)

        safe_creation = self.deploy_test_safe(threshold=threshold, owners=owners)
        my_safe_address = safe_creation.safe_address

        # The balance we will send to the safe
        safe_balance = w3.toWei(0.02, 'ether')

        # Send something to the owner[0], who will be sending the tx
        owner0_balance = safe_balance
        self.send_tx({
            'to': owners[0],
            'value': owner0_balance
        }, funder_account)

        my_safe_contract = get_safe_contract(w3, my_safe_address)

        to = funder
        value = safe_balance // 2
        data = HexBytes('')
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
        signatures_packed = signatures_to_bytes(signature_pairs)

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

        with self.assertRaises(CouldNotPayGasWithEther):
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
                tx_gas_price=self.gas_price,
            )

        # Send something to the safe
        self.send_tx({
            'to': my_safe_address,
            'value': safe_balance
        }, funder_account)

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
            tx_gas_price=self.gas_price,
        )

        tx_receipt = w3.eth.waitForTransactionReceipt(sent_tx_hash)
        self.assertTrue(tx_receipt['status'])
        owner0_new_balance = w3.eth.getBalance(owners[0])
        gas_used = tx_receipt['gasUsed']
        gas_cost = gas_used * self.gas_price
        estimated_payment = (data_gas + gas_used) * gas_price
        real_payment = owner0_new_balance - (owner0_balance - gas_cost)
        # Estimated payment will be bigger, because it uses all the tx gas. Real payment only uses gas left
        # in the point of calculation of the payment, so it will be slightly lower
        self.assertTrue(estimated_payment > real_payment > 0)
        self.assertTrue(owner0_new_balance > owner0_balance - tx['gas'] * self.gas_price)
        self.assertEqual(self.safe_service.retrieve_nonce(my_safe_address), 1)

    def test_send_multisig_tx_gas_token(self):
        # Create safe with one owner, fund the safe and the owner with `safe_balance`
        receiver, _ = get_eth_address_with_key()
        threshold = 1
        funder_account = self.ethereum_test_account
        funder = funder_account.address
        safe_balance_ether = 0.02
        safe_balance = self.w3.toWei(safe_balance_ether, 'ether')
        owner_account = self.create_account(initial_ether=safe_balance_ether)
        owner = owner_account.address

        safe_creation = self.deploy_test_safe(threshold=threshold, owners=[owner], initial_funding_wei=safe_balance)
        my_safe_address = safe_creation.safe_address

        # Give erc20 tokens to the funder
        amount_token = int(1e18)
        erc20_contract = self.deploy_example_erc20(amount_token, funder)
        self.assertEqual(self.ethereum_client.erc20.get_balance(funder, erc20_contract.address), amount_token)

        signature_packed = signature_to_bytes((1, int(owner, 16), 0))

        to = receiver
        value = safe_balance
        data = HexBytes('')
        operation = 0
        safe_tx_gas = 100000
        data_gas = 300000
        gas_price = 2
        gas_token = erc20_contract.address
        refund_receiver = NULL_ADDRESS

        with self.assertRaises(CouldNotPayGasWithToken):
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
                tx_sender_private_key=owner_account.privateKey,
                tx_gas_price=self.gas_price,
            )

        # Give erc20 tokens to the safe
        self.ethereum_client.erc20.send_tokens(my_safe_address, amount_token, erc20_contract.address,
                                                funder_account.privateKey)

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
            tx_sender_private_key=owner_account.privateKey,
            tx_gas_price=self.gas_price,
        )

        safe_token_balance = self.ethereum_client.erc20.get_balance(my_safe_address, erc20_contract.address)

        # Token was used for tx gas costs. Sender must have some tokens now and safe should have less
        self.assertLess(safe_token_balance, amount_token)
        owner_token_balance = self.ethereum_client.erc20.get_balance(owner, erc20_contract.address)
        self.assertGreater(owner_token_balance, 0)

        # All ether on safe was transferred to receiver
        receiver_balance = self.w3.eth.getBalance(receiver)
        self.assertEqual(receiver_balance, safe_balance)

    def test_check_proxy_code(self):
        proxy_contract_address = self.deploy_test_safe().safe_address
        self.assertTrue(self.safe_service.check_proxy_code(proxy_contract_address))

        safe_contract_address = self.safe_service.deploy_master_contract(deployer_private_key=
                                                                         self.ethereum_test_account.privateKey)
        self.assertFalse(self.safe_service.check_proxy_code(safe_contract_address))

        proxy_contract_address = self.safe_service.deploy_proxy_contract(deployer_private_key=
                                                                         self.ethereum_test_account.privateKey)
        self.assertTrue(self.safe_service.check_proxy_code(proxy_contract_address))

    def test_estimate_tx_data_gas(self):
        safe_address = self.deploy_test_safe().safe_address
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
        safe_address = self.deploy_test_safe().safe_address
        to, _ = get_eth_address_with_key()
        value = int('abc', 16)
        data = HexBytes('0xabcdef')
        operation = 1
        data_gas = self.safe_service.estimate_tx_gas(safe_address, to, value, data, operation)
        self.assertGreater(data_gas, 0)

    def test_estimate_tx_operational_gas(self):
        for threshold in range(2, 5):
            safe_creation = self.deploy_test_safe(threshold=threshold, number_owners=6)
            my_safe_address = safe_creation.safe_address
            tx_signature_gas_estimation = self.safe_service.estimate_tx_operational_gas(my_safe_address, 0)
            self.assertGreaterEqual(tx_signature_gas_estimation, 20000)

    def test_hash_safe_multisig_tx(self):
        # -------- Old version of the contract --------------------------
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
                                                         67, safe_version='0.1.0')
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
                                                         257000, safe_version='0.1.0')
        self.assertEqual(expected_hash, tx_hash)

        # -------- New version of the contract --------------------------
        expected_hash = HexBytes('0x7c60341f3e1b4483575f38e84e97d6b332a2dd55b9290f39e6e26eef29a04fe7')
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

        expected_hash = HexBytes('0xf585279fd867c94738096f4eab964e9e202014d2f0d5155d751099ad85cbe504')
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

    def test_is_safe_deployed(self):
        random_address = Account.create().address
        self.assertFalse(self.safe_service.is_safe_deployed(random_address))

        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address
        self.assertTrue(self.safe_service.is_safe_deployed(my_safe_address))

    def test_provider_singleton(self):
        safe_service1 = SafeServiceProvider()
        safe_service2 = SafeServiceProvider()
        self.assertEqual(safe_service1, safe_service2)

    def test_retrieve_master_copy_address(self):
        proxy_address = self.deploy_test_safe().safe_address
        self.assertEqual(self.safe_service.retrieve_master_copy_address(proxy_address),
                         self.safe_service.master_copy_address)

    def test_retrieve_is_owner(self):
        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address
        for owner in safe_creation.owners:
            self.assertTrue(self.safe_service.retrieve_is_owner(my_safe_address, owner))

        random_address, _ = get_eth_address_with_key()
        self.assertFalse(self.safe_service.retrieve_is_owner(my_safe_address, random_address))

    def test_retrieve_nonce(self):
        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address
        self.assertEqual(self.safe_service.retrieve_nonce(my_safe_address), 0)

    def test_retrieve_owners(self):
        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address
        owners = self.safe_service.retrieve_owners(my_safe_address)
        self.assertEqual(set(owners), set(safe_creation.owners))

    def test_retrieve_threshold(self):
        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address
        self.assertEqual(self.safe_service.retrieve_threshold(my_safe_address), 2)

    def test_retrieve_version(self):
        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address
        # Versions must be semantic, like 0.1.0, so we count 3 points
        self.assertTrue(self.safe_service.retrieve_version(my_safe_address).count('.'), 3)

    def test_token_balance(self):
        funder_account = self.ethereum_test_account
        funder = funder_account.address
        amount = 200
        deployed_erc20 = self.deploy_example_erc20(amount, funder)

        safe_creation = self.deploy_test_safe(threshold=2, number_owners=3)
        my_safe_address = safe_creation.safe_address

        balance = self.ethereum_client.erc20.get_balance(my_safe_address, deployed_erc20.address)
        self.assertEqual(balance, 0)

        transfer_tx = deployed_erc20.functions.transfer(my_safe_address, amount).buildTransaction({'from': funder})
        self.send_tx(transfer_tx, funder_account)

        balance = self.ethereum_client.erc20.get_balance(my_safe_address, deployed_erc20.address)
        self.assertEqual(balance, amount)

    # TODO Test approve tx from another contract
    def test_send_previously_approved_tx(self):
        number_owners = 4
        accounts = [self.create_account(initial_ether=0.01) for _ in range(number_owners)]
        accounts.sort(key=lambda x: x.address.lower())
        owners = [account.address for account in accounts]

        safe_creation = self.deploy_test_safe(threshold=2, owners=owners,
                                              initial_funding_wei=self.w3.toWei(0.01, 'ether'))
        safe_address = safe_creation.safe_address
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

        approve_hash_fn = safe_instance.functions.approveHash(safe_tx_hash)
        for account in accounts[:2]:
            self.send_tx(approve_hash_fn.buildTransaction({'from': account.address}), account)

        for owner in (owners[0], owners[1]):
            is_approved = self.safe_service.retrieve_is_hash_approved(safe_address, owner, safe_tx_hash)
            self.assertTrue(is_approved)

        # Prepare signatures. v must be 1 for previously signed and r the owner
        signatures = (1, int(owners[0], 16), 0), (1, int(owners[1], 16), 0)
        signature_bytes = signatures_to_bytes(signatures)

        self.safe_service.send_multisig_tx(safe_address, to, value, data, operation, safe_tx_gas,
                                           data_gas, gas_price, gas_token, refund_receiver, signature_bytes,
                                           self.ethereum_test_account.privateKey)

        balance = self.w3.eth.getBalance(to)
        self.assertEqual(value, balance)
