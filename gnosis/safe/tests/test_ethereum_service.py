import logging

from django.test import TestCase
from django_eth.tests.factories import get_eth_address_with_key

from ..ethereum_service import (EthereumServiceProvider, FromAddressNotFound,
                                InsufficientFunds, InvalidNonce)
from .factories import deploy_example_erc20
from .test_safe_service import TestCaseWithSafeContractMixin

logger = logging.getLogger(__name__)


class TestSafeCreationTx(TestCase, TestCaseWithSafeContractMixin):
    @classmethod
    def setUpTestData(cls):
        cls.gas_price = 1
        cls.ethereum_service = EthereumServiceProvider()
        cls.w3 = cls.ethereum_service.w3

    def test_erc20_balance(self):
        amount = 1000
        address, _ = get_eth_address_with_key()
        erc20_contract = deploy_example_erc20(self.w3, amount, address, deployer=self.w3.eth.accounts[0])
        token_balance = self.ethereum_service.get_erc20_balance(address, erc20_contract.address)
        self.assertTrue(token_balance, amount)

        another_account, _ = get_eth_address_with_key()
        token_balance = self.ethereum_service.get_erc20_balance(another_account, erc20_contract.address)
        self.assertEqual(token_balance, 0)

    def test_estimate_gas(self):
        send_ether_gas = 21000
        from_ = self.w3.eth.accounts[0]
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
        from_ = self.w3.eth.accounts[0]
        to, _ = get_eth_address_with_key()

        erc20_contract = deploy_example_erc20(self.w3, amount_tokens, from_, deployer=self.w3.eth.accounts[0])
        data = erc20_contract.functions.transfer(to, amount_to_send).buildTransaction()['data']

        # Ganache returns error because there is data but address is not a contract
        with self.assertRaisesMessage(ValueError, 'transaction which calls a contract function'):
            self.ethereum_service.estimate_gas(from_, to, 0, data, block_identifier='pending')
        # `to` is not a contract, no functions will be triggered
        # gas = self.ethereum_service.estimate_gas(from_, to, 0, data, block_identifier='pending')
        # self.assertGreater(gas, send_ether_gas)
        # self.assertLess(gas, send_ether_gas + 2000)

        gas = self.ethereum_service.estimate_gas(from_, erc20_contract.address, 0, data, block_identifier='pending')
        self.assertGreater(gas, send_ether_gas)

        # We do the real erc20 transfer for the next test case
        erc20_contract.functions.transfer(to, amount_to_send).transact({'from': from_})
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

    def test_send_eth_to(self):
        address, _ = get_eth_address_with_key()
        self.ethereum_service.send_eth_to(address, self.gas_price, value=1)
        self.assertEqual(self.ethereum_service.get_balance(address), 1)

    def test_send_transaction(self):
        address = self.w3.eth.accounts[0]
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
        address = self.w3.eth.accounts[5]
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
