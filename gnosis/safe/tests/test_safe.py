import logging

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.utils import get_eth_address_with_key

from ..exceptions import CouldNotPayGasWithEther, CouldNotPayGasWithToken
from ..safe import Safe
from ..signatures import signature_to_bytes, signatures_to_bytes
from .safe_test_case import SafeTestCaseMixin

logger = logging.getLogger(__name__)


class TestSafe(TestCase, SafeTestCaseMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_create(self):
        owners = [self.ethereum_test_account.address]
        threshold = 1
        master_copy_address = self.safe_contract_address

        ethereum_tx_sent = Safe.create(self.ethereum_client, self.ethereum_test_account, master_copy_address,
                                       owners, threshold, proxy_factory_address=self.proxy_factory_contract_address)
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_master_copy_address(), master_copy_address)
        self.assertEqual(safe.retrieve_owners(), owners)
        self.assertEqual(safe.retrieve_threshold(), threshold)

    def test_check_funds_for_tx_gas(self):
        safe = Safe(self.deploy_test_safe().safe_address, self.ethereum_client)
        safe_tx_gas = 2
        base_gas = 4
        gas_price = 10
        self.assertFalse(safe.check_funds_for_tx_gas(safe_tx_gas, base_gas, gas_price, NULL_ADDRESS))
        self.send_ether(safe.address, (safe_tx_gas + base_gas) * gas_price)
        self.assertTrue(safe.check_funds_for_tx_gas(safe_tx_gas, base_gas, gas_price, NULL_ADDRESS))

    def test_estimate_safe_creation(self):
        number_owners = 4
        gas_price = self.gas_price
        payment_token = NULL_ADDRESS
        safe_creation_estimate = Safe.estimate_safe_creation(self.ethereum_client, self.safe_old_contract_address,
                                                             number_owners, gas_price, payment_token)
        self.assertGreater(safe_creation_estimate.gas_price, 0)
        self.assertGreater(safe_creation_estimate.gas, 0)
        self.assertGreater(safe_creation_estimate.payment, 0)

    def test_estimate_safe_creation_2(self):
        number_owners = 4
        gas_price = self.gas_price
        payment_token = NULL_ADDRESS
        safe_creation_estimate = Safe.estimate_safe_creation_2(self.ethereum_client, self.safe_contract_address,
                                                               self.proxy_factory_contract_address,
                                                               number_owners, gas_price, payment_token)
        self.assertGreater(safe_creation_estimate.gas_price, 0)
        self.assertGreater(safe_creation_estimate.gas, 0)
        self.assertGreater(safe_creation_estimate.payment, 0)

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
        safe = Safe(my_safe_address, self.ethereum_client)

        to = funder
        value = safe_balance // 2
        data = HexBytes('')
        operation = 0
        safe_tx_gas = 100000
        base_gas = 300000
        gas_price = 1
        gas_token = NULL_ADDRESS
        refund_receiver = NULL_ADDRESS
        nonce = None
        safe_multisig_tx = safe.build_multisig_tx(to=to,
                                                  value=value,
                                                  data=data,
                                                  operation=operation,
                                                  safe_tx_gas=safe_tx_gas,
                                                  base_gas=base_gas,
                                                  gas_price=gas_price,
                                                  gas_token=gas_token,
                                                  refund_receiver=refund_receiver,
                                                  safe_nonce=nonce)
        safe_multisig_tx_hash = safe_multisig_tx.safe_tx_hash

        nonce = safe.retrieve_nonce()
        self.assertEqual(safe.build_multisig_tx(to=to,
                                                value=value,
                                                data=data,
                                                operation=operation,
                                                safe_tx_gas=safe_tx_gas,
                                                base_gas=base_gas,
                                                gas_price=gas_price,
                                                gas_token=gas_token,
                                                refund_receiver=refund_receiver,
                                                safe_nonce=nonce).safe_tx_hash, safe_multisig_tx_hash)
        # Just to make sure we are not miscalculating tx_hash
        contract_multisig_tx_hash = my_safe_contract.functions.getTransactionHash(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            nonce).call()

        self.assertEqual(safe_multisig_tx_hash, contract_multisig_tx_hash)

        for private_key in keys:
            safe_multisig_tx.sign(private_key)

        signatures = safe_multisig_tx.signatures
        self.assertEqual(set(safe_multisig_tx.signers), set(owners))

        # Check owners are the same
        contract_owners = my_safe_contract.functions.getOwners().call()
        self.assertEqual(set(contract_owners), set(owners))
        self.assertEqual(w3.eth.getBalance(owners[0]), owner0_balance)

        with self.assertRaises(CouldNotPayGasWithEther):
            safe.send_multisig_tx(
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                base_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signatures,
                tx_sender_private_key=keys[0],
                tx_gas_price=self.gas_price,
            )

        # Send something to the safe
        self.send_tx({
            'to': my_safe_address,
            'value': safe_balance
        }, funder_account)

        ethereum_tx_sent = safe.send_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
            tx_sender_private_key=keys[0],
            tx_gas_price=self.gas_price,
        )

        tx_receipt = w3.eth.waitForTransactionReceipt(ethereum_tx_sent.tx_hash)
        self.assertTrue(tx_receipt['status'])
        owner0_new_balance = w3.eth.getBalance(owners[0])
        gas_used = tx_receipt['gasUsed']
        gas_cost = gas_used * self.gas_price
        estimated_payment = (base_gas + gas_used) * gas_price
        real_payment = owner0_new_balance - (owner0_balance - gas_cost)
        # Estimated payment will be bigger, because it uses all the tx gas. Real payment only uses gas left
        # in the point of calculation of the payment, so it will be slightly lower
        self.assertTrue(estimated_payment > real_payment > 0)
        self.assertTrue(owner0_new_balance > owner0_balance - ethereum_tx_sent.tx['gas'] * self.gas_price)
        self.assertEqual(safe.retrieve_nonce(), 1)

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
        safe = Safe(my_safe_address, self.ethereum_client)

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
        base_gas = 300000
        gas_price = 2
        gas_token = erc20_contract.address
        refund_receiver = NULL_ADDRESS

        with self.assertRaises(CouldNotPayGasWithToken):
            safe.send_multisig_tx(
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                base_gas,
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

        safe.send_multisig_tx(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
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

    def test_estimate_tx_base_gas(self):
        safe_address = self.deploy_test_safe().safe_address
        safe = Safe(safe_address, self.ethereum_client)
        to = Account().create().address
        value = int('abc', 16)
        data = HexBytes('0xabcdef')
        operation = 1
        gas_token = NULL_ADDRESS
        estimate_tx_gas = int('ccdd', 16)
        base_gas = safe.estimate_tx_base_gas(to, value, data, operation, gas_token, estimate_tx_gas)
        self.assertGreater(base_gas, 0)

        data = HexBytes('0xabcdefbb')  # A byte that was 00 now is bb, so -4 + 68
        data_gas2 = safe.estimate_tx_base_gas(to, value, data, operation, gas_token, estimate_tx_gas)
        self.assertEqual(data_gas2, base_gas + 68 - 4)

    def test_estimate_tx_gas(self):
        to = Account().create().address
        value = 123
        data = HexBytes('0xabcdef')
        operation = 1
        safe = Safe(self.deploy_test_safe(initial_funding_wei=value + 23000).safe_address, self.ethereum_client)

        safe_tx_gas = safe.estimate_tx_gas(to, value, data, operation)
        self.assertGreater(safe_tx_gas, 0)
        operation = 0
        safe_tx_gas = safe.estimate_tx_gas(to, value, data, operation)
        self.assertGreater(safe_tx_gas, 0)

    def test_estimate_tx_operational_gas(self):
        for threshold in range(2, 5):
            safe_creation = self.deploy_test_safe(threshold=threshold, number_owners=6)
            safe = Safe(safe_creation.safe_address, self.ethereum_client)
            tx_signature_gas_estimation = safe.estimate_tx_operational_gas(0)
            self.assertGreaterEqual(tx_signature_gas_estimation, 20000)

    def test_retrieve_code(self):
        self.assertEqual(Safe(NULL_ADDRESS, self.ethereum_client).retrieve_code(), HexBytes('0x'))
        self.assertIsNotNone(Safe(self.deploy_test_safe().safe_address,
                                  self.ethereum_client).retrieve_code())

    def test_retrieve_info(self):
        safe_creation = self.deploy_test_safe()
        safe = Safe(safe_creation.safe_address, self.ethereum_client)
        self.assertEqual(safe.retrieve_master_copy_address(), self.safe_contract_address)
        self.assertEqual(safe.retrieve_nonce(), 0)
        self.assertEqual(set(safe.retrieve_owners()), set(safe_creation.owners))
        self.assertEqual(safe.retrieve_threshold(), safe_creation.threshold)

        # Versions must be semantic, like 0.1.0, so we count 3 points
        self.assertTrue(safe.retrieve_version().count('.'), 3)

        for owner in safe_creation.owners:
            self.assertTrue(safe.retrieve_is_owner(owner))

    def test_retrieve_is_hash_approved(self):
        safe_creation = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        safe = Safe(safe_creation.safe_address, self.ethereum_client)
        safe_contract = safe.get_contract()
        fake_tx_hash = Web3.sha3(text='Knopfler')
        another_tx_hash = Web3.sha3(text='Marc')
        tx = safe_contract.functions.approveHash(fake_tx_hash).buildTransaction()
        tx['gas'] = tx['gas'] * 2

        self.ethereum_client.send_unsigned_transaction(tx, private_key=self.ethereum_test_account.privateKey)
        self.assertTrue(safe.retrieve_is_hash_approved(self.ethereum_test_account.address, fake_tx_hash))
        self.assertFalse(safe.retrieve_is_hash_approved(self.ethereum_test_account.address, another_tx_hash))

    def test_retrieve_is_message_signed(self):
        safe_creation = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        safe = Safe(safe_creation.safe_address, self.ethereum_client)
        safe_contract = safe.get_contract()
        message = b'12345'
        message_hash = safe_contract.functions.getMessageHash(message).call()
        sign_message_data = HexBytes(safe_contract.functions.signMessage(message).buildTransaction()['data'])
        safe_tx = safe.build_multisig_tx(safe.address, 0, sign_message_data)
        safe_tx.sign(self.ethereum_test_account.privateKey)
        safe_tx.execute(tx_sender_private_key=self.ethereum_test_account.privateKey)
        self.assertTrue(safe.retrieve_is_message_signed(message_hash))

    def test_retrieve_is_owner(self):
        safe_creation = self.deploy_test_safe(owners=[self.ethereum_test_account.address])
        safe = Safe(safe_creation.safe_address, self.ethereum_client)
        self.assertTrue(safe.retrieve_is_owner(self.ethereum_test_account.address))
        self.assertFalse(safe.retrieve_is_owner(Account.create().address))

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
        safe = Safe(safe_address, self.ethereum_client)
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
        nonce = safe.retrieve_nonce()

        self.assertEqual(nonce, 0)

        safe_tx_hash = safe.build_multisig_tx(to, value, data, operation, safe_tx_gas,
                                              data_gas, gas_price, gas_token, refund_receiver,
                                              safe_nonce=nonce).safe_tx_hash

        safe_tx_contract_hash = safe_instance.functions.getTransactionHash(to, value, data, operation,
                                                                           safe_tx_gas, data_gas, gas_price, gas_token,
                                                                           refund_receiver, nonce).call()

        self.assertEqual(safe_tx_hash, safe_tx_contract_hash)

        approve_hash_fn = safe_instance.functions.approveHash(safe_tx_hash)
        for account in accounts[:2]:
            self.send_tx(approve_hash_fn.buildTransaction({'from': account.address}), account)

        for owner in (owners[0], owners[1]):
            is_approved = safe.retrieve_is_hash_approved(owner, safe_tx_hash)
            self.assertTrue(is_approved)

        # Prepare signatures. v must be 1 for previously signed and r the owner
        signatures = (1, int(owners[0], 16), 0), (1, int(owners[1], 16), 0)
        signature_bytes = signatures_to_bytes(signatures)

        safe.send_multisig_tx(to, value, data, operation, safe_tx_gas,
                              data_gas, gas_price, gas_token, refund_receiver, signature_bytes,
                              self.ethereum_test_account.privateKey)

        balance = self.w3.eth.getBalance(to)
        self.assertEqual(value, balance)
