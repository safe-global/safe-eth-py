from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes

from ..ethereum_service import (EthereumServiceProvider, EtherLimitExceeded,
                                FromAddressNotFound, InsufficientFunds,
                                InvalidNonce, SenderAccountNotFoundInNode)
from ..utils import get_eth_address_with_key
from .ethereum_test_case import EthereumTestCaseMixin


class TestEthereumService(EthereumTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_check_tx_with_confirmations(self):
        value = 1
        to, _ = get_eth_address_with_key()

        tx_hash = self.ethereum_service.send_eth_to(to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_service.check_tx_with_confirmations(tx_hash, 2))

        _ = self.ethereum_service.send_eth_to(to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_service.check_tx_with_confirmations(tx_hash, 2))

        _ = self.ethereum_service.send_eth_to(to=to, gas_price=self.gas_price, value=value)
        self.assertTrue(self.ethereum_service.check_tx_with_confirmations(tx_hash, 2))

    def test_erc20_balance(self):
        amount = 1000
        address, _ = get_eth_address_with_key()
        erc20_contract = self.deploy_example_erc20(amount, address)
        token_balance = self.ethereum_service.get_erc20_balance(address, erc20_contract.address)
        self.assertTrue(token_balance, amount)

        another_account, _ = get_eth_address_with_key()
        token_balance = self.ethereum_service.get_erc20_balance(another_account, erc20_contract.address)
        self.assertEqual(token_balance, 0)

    def test_estimate_gas(self):
        send_ether_gas = 21000
        from_ = self.ethereum_test_account.address
        to, _ = get_eth_address_with_key()
        gas = self.ethereum_service.estimate_gas(from_, to, 5, None, block_identifier='pending')
        self.assertEqual(gas, send_ether_gas)

        gas = self.ethereum_service.estimate_gas(from_, to, 5, b'')
        self.assertEqual(gas, send_ether_gas)

        gas = self.ethereum_service.estimate_gas(from_, to, 5, None)
        self.assertEqual(gas, send_ether_gas)

    def test_estimate_gas_with_erc20(self):
        send_ether_gas = 21000
        amount_tokens = 5000
        amount_to_send = amount_tokens // 2
        from_account = self.ethereum_test_account
        from_ = from_account.address
        to, _ = get_eth_address_with_key()

        erc20_contract = self.deploy_example_erc20(amount_tokens, from_)
        transfer_tx = erc20_contract.functions.transfer(to, amount_to_send).buildTransaction({'from': from_})
        data = transfer_tx['data']

        # Ganache does not cares about all this anymore
        # ---------------------------------------------
        # Ganache returns error because there is data but address is not a contract
        # with self.assertRaisesMessage(ValueError, 'transaction which calls a contract function'):
        #    self.ethereum_service.estimate_gas(from_, to, 0, data, block_identifier='pending')
        # `to` is not a contract, no functions will be triggered
        # gas = self.ethereum_service.estimate_gas(from_, to, 0, data, block_identifier='pending')
        # self.assertGreater(gas, send_ether_gas)
        # self.assertLess(gas, send_ether_gas + 2000)

        gas = self.ethereum_service.estimate_gas(from_, erc20_contract.address, 0, data, block_identifier='pending')
        self.assertGreater(gas, send_ether_gas)

        # We do the real erc20 transfer for the next test case
        self.send_tx(transfer_tx, from_account)
        token_balance = self.ethereum_service.get_erc20_balance(to, erc20_contract.address)
        self.assertTrue(token_balance, amount_to_send)

        # Gas will be lowest now because you don't have to pay for storage
        gas2 = self.ethereum_service.estimate_gas(from_, erc20_contract.address, 0, data, block_identifier='pending')
        self.assertLess(gas2, gas)

    def test_get_nonce(self):
        address, _ = get_eth_address_with_key()
        nonce = self.ethereum_service.get_nonce_for_account(address)
        self.assertEqual(nonce, 0)

        nonce = self.ethereum_service.get_nonce_for_account(address, block_identifier='pending')
        self.assertEqual(nonce, 0)

    def test_estimate_data_gas(self):
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('')), 0)
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('0x00')), 4)
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('0x000204')), 4 + 68 * 2)
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('0x050204')), 68 * 3)
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('0x0502040000')), 68 * 3 + 4 * 2)
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('0x050204000001')), 68 * 4 + 4 * 2)
        self.assertEqual(self.ethereum_service.estimate_data_gas(HexBytes('0x00050204000001')), 4 + 68 * 4 + 4 * 2)

    def test_provider_singleton(self):
        ethereum_service1 = EthereumServiceProvider()
        ethereum_service2 = EthereumServiceProvider()
        self.assertEqual(ethereum_service1, ethereum_service2)

    def test_send_eth_to(self):
        address, _ = get_eth_address_with_key()
        value = 1
        self.ethereum_service.send_eth_to(address, self.gas_price, value)
        self.assertEqual(self.ethereum_service.get_balance(address), value)

        value = self.w3.toWei(self.ethereum_service.max_eth_to_send, 'ether') + 1
        with self.assertRaises(EtherLimitExceeded):
            self.ethereum_service.send_eth_to(address, self.gas_price, value)

    def test_send_eth_without_key(self):
        with self.settings(SAFE_FUNDER_PRIVATE_KEY=None):
            self.test_send_eth_to()

    def test_send_transaction(self):
        account = self.ethereum_test_account
        address = account.address
        to, _ = get_eth_address_with_key()
        value = 1
        tx = {
            'to': to,
            'value': value,
            'gas': 23000,
            'gasPrice': self.gas_price,
            'nonce': self.ethereum_service.get_nonce_for_account(address)
        }

        with self.assertRaises(FromAddressNotFound):
            self.ethereum_service.send_transaction(tx)

        # Random address not in the node
        tx['from'] = Account.create().address
        with self.assertRaises(SenderAccountNotFoundInNode):
            self.ethereum_service.send_transaction(tx)

        tx['from'] = address
        self.ethereum_service.send_transaction(tx)
        self.assertEqual(self.ethereum_service.get_balance(to), 1)

        with self.assertRaises(InvalidNonce):
            self.ethereum_service.send_transaction(tx)

        tx['value'] = self.ethereum_service.get_balance(address) + 1
        tx['nonce'] = self.ethereum_service.get_nonce_for_account(address)
        with self.assertRaises(InsufficientFunds):
            self.ethereum_service.send_transaction(tx)

    def test_send_unsigned_transaction(self):
        account = self.ethereum_test_account
        address = account.address
        to, _ = get_eth_address_with_key()
        value = 4

        tx = {
            'to': to,
            'value': value,
            'gas': 23000,
            'gasPrice': 1,
        }

        self.ethereum_service.send_unsigned_transaction(tx, public_key=address)
        self.assertEqual(self.ethereum_service.get_balance(to), value)
        first_nonce = tx['nonce']
        self.assertGreaterEqual(first_nonce, 0)

        # Will use the same nonce
        with self.assertRaisesMessage(InvalidNonce, 'correct nonce'):
            self.ethereum_service.send_unsigned_transaction(tx, public_key=address)

        # With retry, everything should work
        self.ethereum_service.send_unsigned_transaction(tx, public_key=address, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 1)
        self.assertEqual(self.ethereum_service.get_balance(to), value * 2)

        # We try again with the first nonce, and should work too
        tx['nonce'] = first_nonce
        self.ethereum_service.send_unsigned_transaction(tx, public_key=address, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 2)
        self.assertEqual(self.ethereum_service.get_balance(to), value * 3)

    def test_send_unsigned_transaction_with_private_key(self):
        account = self.create_account(initial_ether=0.1)
        key = account.privateKey
        to, _ = get_eth_address_with_key()
        value = 4

        tx = {
            'to': to,
            'value': value,
            'gas': 23000,
            'gasPrice': self.gas_price,
        }

        self.ethereum_service.send_unsigned_transaction(tx, private_key=key)
        self.assertEqual(self.ethereum_service.get_balance(to), value)
        first_nonce = tx['nonce']
        self.assertGreaterEqual(first_nonce, 0)

        # Will use the same nonce
        with self.assertRaisesMessage(InvalidNonce, 'correct nonce'):
            self.ethereum_service.send_unsigned_transaction(tx, private_key=key)

        # With retry, everything should work
        self.ethereum_service.send_unsigned_transaction(tx, private_key=key, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 1)
        self.assertEqual(self.ethereum_service.get_balance(to), value * 2)

        # We try again with the first nonce, and should work too
        tx['nonce'] = first_nonce
        self.ethereum_service.send_unsigned_transaction(tx, private_key=key, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 2)
        self.assertEqual(self.ethereum_service.get_balance(to), value * 3)

    def test_wait_for_tx_receipt(self):
        value = 1
        to = Account.create().address

        tx_hash = self.ethereum_service.send_eth_to(to=to, gas_price=self.gas_price, value=value)
        receipt1 = self.ethereum_service.get_transaction_receipt(tx_hash, timeout=None)
        receipt2 = self.ethereum_service.get_transaction_receipt(tx_hash, timeout=20)
        self.assertIsNotNone(receipt1)
        self.assertEqual(receipt1, receipt2)

        fake_tx_hash = self.w3.sha3(0)
        self.assertIsNone(self.ethereum_service.get_transaction_receipt(fake_tx_hash, timeout=None))
        self.assertIsNone(self.ethereum_service.get_transaction_receipt(fake_tx_hash, timeout=1))
