from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes

from ..ethereum_client import (EthereumClientProvider,
                               EtherLimitExceeded, FromAddressNotFound,
                               InsufficientFunds, InvalidNonce,
                               SenderAccountNotFoundInNode)
from ..utils import get_eth_address_with_key
from .ethereum_test_case import EthereumTestCaseMixin


class TestERC20Module(EthereumTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_get_balance(self):
        amount = 1000
        address, _ = get_eth_address_with_key()
        erc20_contract = self.deploy_example_erc20(amount, address)
        token_balance = self.ethereum_client.erc20.get_balance(address, erc20_contract.address)
        self.assertTrue(token_balance, amount)

        another_account, _ = get_eth_address_with_key()
        token_balance = self.ethereum_client.erc20.get_balance(another_account, erc20_contract.address)
        self.assertEqual(token_balance, 0)

    def test_get_transfer_history(self):
        amount = 1000
        owner_account = self.create_account(initial_ether=0.01)

        # Owner will send amount / 2 to receiver and receiver2. Then receiver1 and receiver 2
        # will send amount / 4 to receiver3
        receiver_account = self.create_account(initial_ether=0.01)
        receiver2_account = self.create_account(initial_ether=0.01)
        receiver3_account = self.create_account(initial_ether=0.01)
        erc20_contract = self.deploy_example_erc20(amount, owner_account.address)
        block_number = self.w3.eth.blockNumber
        events = self.ethereum_client.erc20.get_transfer_history(block_number, token_address=erc20_contract.address)
        self.assertFalse(events)

        self.send_tx(erc20_contract.functions.transfer(receiver_account.address,
                                                       amount // 2).buildTransaction({'from': owner_account.address}),
                     owner_account)
        self.send_tx(erc20_contract.functions.transfer(receiver2_account.address,
                                                       amount // 2).buildTransaction({'from': owner_account.address}),
                     owner_account)

        self.send_tx(erc20_contract.functions.transfer(receiver3_account.address,
                                                       amount // 4).buildTransaction({'from': receiver_account.address}),
                     receiver_account)
        self.send_tx(erc20_contract.functions.transfer(receiver3_account.address,
                                                       amount // 4).buildTransaction({'from': receiver2_account.address}),
                     receiver2_account)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, token_address=erc20_contract.address)
        self.assertEqual(len(events), 4)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=owner_account.address)
        self.assertEqual(len(events), 2)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver_account.address)
        self.assertEqual(len(events), 1)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver2_account.address)
        self.assertEqual(len(events), 1)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver3_account.address)
        self.assertEqual(len(events), 0)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, to_address=receiver2_account.address)
        self.assertEqual(len(events), 1)

        events = self.ethereum_client.erc20.get_transfer_history(block_number, to_address=receiver3_account.address)
        self.assertEqual(len(events), 2)
        for event in events:
            self.assertEqual(event.args.value, amount // 4)
            self.assertEqual(event.args.to, receiver3_account.address)

        events = self.ethereum_client.erc20.get_transfer_history(block_number,
                                                                  from_address=receiver2_account.address,
                                                                  to_address=receiver3_account.address)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.args.value, amount // 4)
        self.assertEqual(event.args['from'], receiver2_account.address)
        self.assertEqual(event.args.to, receiver3_account.address)

    def test_get_info(self):
        amount = 1
        owner = Account.create().address
        erc20_contract = self.deploy_example_erc20(amount, owner)
        erc20_info = self.ethereum_client.erc20.get_info(erc20_contract.address)
        self.assertEqual(erc20_info.decimals, 18)

    def test_send_tokens(self):
        amount = 5
        owner = self.ethereum_test_account
        owner_2 = Account.create()
        erc20 = self.deploy_example_erc20(amount, owner.address)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner.address, erc20.address), amount)

        amount_2 = 3
        self.ethereum_client.erc20.send_tokens(owner_2.address, amount_2, erc20.address, owner.privateKey)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner.address, erc20.address), amount - amount_2)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner_2.address, erc20.address), amount_2)


class TestParityModule(EthereumTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_decode_trace(self):
        example_traces = [
            {
                "action": {
                    "callType": "call",
                    "from": "0x32be343b94f860124dc4fee278fdcbd38c102d88",
                    "gas": "0x4c40d",
                    "input": "0x",
                    "to": "0x8bbb73bcb5d553b5a556358d27625323fd781d37",
                    "value": "0x3f0650ec47fd240000"
                },
                "blockHash": "0x86df301bcdd8248d982dbf039f09faf792684e1aeee99d5b58b77d620008b80f",
                "blockNumber": 3068183,
                "result": {
                    "gasUsed": "0x0",
                    "output": "0x"
                },
                "subtraces": 0,
                "traceAddress": [],
                "transactionHash": "0x3321a7708b1083130bd78da0d62ead9f6683033231617c9d268e2c7e3fa6c104",
                "transactionPosition": 3,
                "type": "call"
            },
            {
                "action": {
                    "from": "0x3b169a0fb55ea0b6bafe54c272b1fe4983742bf7",
                    "gas": "0x49b0b",
                    "init": "0x608060405234801561001057600080fd5b5060405161060a38038061060a833981018060405281019080805190602001909291908051820192919060200180519060200190929190805190602001909291908051906020019092919050505084848160008173ffffffffffffffffffffffffffffffffffffffff1614151515610116576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260248152602001807f496e76616c6964206d617374657220636f707920616464726573732070726f7681526020017f696465640000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506000815111156101a35773ffffffffffffffffffffffffffffffffffffffff60005416600080835160208501846127105a03f46040513d6000823e600082141561019f573d81fd5b5050505b5050600081111561036d57600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614156102b7578273ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f1935050505015156102b2576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f436f756c64206e6f74207061792073616665206372656174696f6e207769746881526020017f206574686572000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b61036c565b6102d1828483610377640100000000026401000000009004565b151561036b576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f436f756c64206e6f74207061792073616665206372656174696f6e207769746881526020017f20746f6b656e000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b5050505050610490565b600060608383604051602401808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001925050506040516020818303038152906040527fa9059cbb000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff838183161783525050505090506000808251602084016000896127105a03f16040513d6000823e3d60008114610473576020811461047b5760009450610485565b829450610485565b8151158315171594505b505050509392505050565b61016b8061049f6000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634555d5c91461008b5780635c60da1b146100b6575b73ffffffffffffffffffffffffffffffffffffffff600054163660008037600080366000845af43d6000803e6000811415610086573d6000fd5b3d6000f35b34801561009757600080fd5b506100a061010d565b6040518082815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610116565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006002905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050905600a165627a7a7230582007fffd557dfc8c4d2fdf56ba6381a6ce5b65b6260e1492d87f26c6d4f1d0410800290000000000000000000000008942595a2dc5181df0465af0d7be08c8f23c93af00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d9e09beaeb338d81a7c5688358df0071d498811500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001b15f91a8c35300000000000000000000000000000000000000000000000000000000000001640ec78d9e00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000004000000000000000000000000f763ea5fbb191d47dc4b083dcdc3cdfb586468f8000000000000000000000000ad25c9717d04c0a12086a1d352c1ccf4bf5fcbf80000000000000000000000000da7155692446c80a4e7ad72018e586f20fa3bfe000000000000000000000000bce0cc48ce44e0ac9ee38df4d586afbacef191fa0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "value": "0x0"
                },
                "blockHash": "0x03f9f64dfeb7807b5df608e6957dd4d521fd71685aac5533451d27f0abe03660",
                "blockNumber": 3793534,
                "result": {
                    "address": "0x61a7cc907c47c133d5ff5b685407201951fcbd08",
                    "code": "0x60806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634555d5c91461008b5780635c60da1b146100b6575b73ffffffffffffffffffffffffffffffffffffffff600054163660008037600080366000845af43d6000803e6000811415610086573d6000fd5b3d6000f35b34801561009757600080fd5b506100a061010d565b6040518082815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610116565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006002905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050905600a165627a7a7230582007fffd557dfc8c4d2fdf56ba6381a6ce5b65b6260e1492d87f26c6d4f1d041080029",
                    "gasUsed": "0x4683f"
                },
                "subtraces": 2,
                "traceAddress": [],
                "transactionHash": "0x6c7e8f8778d33d81b29c4bd7526ee50a4cea340d69eed6c89ada4e6fab731789",
                "transactionPosition": 1,
                "type": "create"
            },
        ]
        decoded_traces = self.ethereum_client.parity._decode_traces(example_traces)
        for example_trace, decoded_trace in zip(example_traces, decoded_traces):
            self.assertEqual(decoded_trace['action']['gas'], int(example_trace['action']['gas'], 16))
            self.assertEqual(decoded_trace['action']['value'], int(example_trace['action']['value'], 16))
            self.assertEqual(decoded_trace['result']['gasUsed'], int(example_trace['result']['gasUsed'], 16))

        self.assertEqual(decoded_traces[0]['result']['output'], HexBytes(''))
        self.assertEqual(decoded_traces[1]['result']['address'],
                         self.w3.toChecksumAddress(example_traces[1]['result']['address']))
        self.assertEqual(decoded_traces[1]['result']['code'],
                         HexBytes(example_traces[1]['result']['code']))


class TestEthereumClient(EthereumTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_check_tx_with_confirmations(self):
        value = 1
        to, _ = get_eth_address_with_key()

        tx_hash = self.ethereum_client.send_eth_to(self.ethereum_test_account.privateKey,
                                                    to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))

        _ = self.ethereum_client.send_eth_to(self.ethereum_test_account.privateKey,
                                              to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))

        _ = self.ethereum_client.send_eth_to(self.ethereum_test_account.privateKey,
                                              to=to, gas_price=self.gas_price, value=value)
        self.assertTrue(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))

    def test_estimate_gas(self):
        send_ether_gas = 21000
        from_ = self.ethereum_test_account.address
        to, _ = get_eth_address_with_key()
        gas = self.ethereum_client.estimate_gas(from_, to, 5, None, block_identifier='pending')
        self.assertEqual(gas, send_ether_gas)

        gas = self.ethereum_client.estimate_gas(from_, to, 5, b'')
        self.assertEqual(gas, send_ether_gas)

        gas = self.ethereum_client.estimate_gas(from_, to, 5, None)
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
        #    self.ethereum_client.estimate_gas(from_, to, 0, data, block_identifier='pending')
        # `to` is not a contract, no functions will be triggered
        # gas = self.ethereum_client.estimate_gas(from_, to, 0, data, block_identifier='pending')
        # self.assertGreater(gas, send_ether_gas)
        # self.assertLess(gas, send_ether_gas + 2000)

        gas = self.ethereum_client.estimate_gas(from_, erc20_contract.address, 0, data, block_identifier='pending')
        self.assertGreater(gas, send_ether_gas)

        # We do the real erc20 transfer for the next test case
        self.send_tx(transfer_tx, from_account)
        token_balance = self.ethereum_client.erc20.get_balance(to, erc20_contract.address)
        self.assertTrue(token_balance, amount_to_send)

        # Gas will be lowest now because you don't have to pay for storage
        gas2 = self.ethereum_client.estimate_gas(from_, erc20_contract.address, 0, data, block_identifier='pending')
        self.assertLess(gas2, gas)

    def test_get_nonce(self):
        address, _ = get_eth_address_with_key()
        nonce = self.ethereum_client.get_nonce_for_account(address)
        self.assertEqual(nonce, 0)

        nonce = self.ethereum_client.get_nonce_for_account(address, block_identifier='pending')
        self.assertEqual(nonce, 0)

    def test_estimate_data_gas(self):
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('')), 0)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x00')), 4)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x000204')), 4 + 68 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x050204')), 68 * 3)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x0502040000')), 68 * 3 + 4 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x050204000001')), 68 * 4 + 4 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x00050204000001')), 4 + 68 * 4 + 4 * 2)

    def test_provider_singleton(self):
        ethereum_client1 = EthereumClientProvider()
        ethereum_client2 = EthereumClientProvider()
        self.assertEqual(ethereum_client1, ethereum_client2)

    def test_send_eth_to(self):
        address, _ = get_eth_address_with_key()
        value = 1
        self.ethereum_client.send_eth_to(self.ethereum_test_account.privateKey, address, self.gas_price, value)
        self.assertEqual(self.ethereum_client.get_balance(address), value)

        with self.assertRaises(EtherLimitExceeded):
            max_eth_to_send = 1
            value = self.w3.toWei(max_eth_to_send, 'ether') + 1
            self.ethereum_client.send_eth_to(self.ethereum_test_account.privateKey, address, self.gas_price, value,
                                              max_eth_to_send=max_eth_to_send)

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
            'nonce': self.ethereum_client.get_nonce_for_account(address)
        }

        with self.assertRaises(FromAddressNotFound):
            self.ethereum_client.send_transaction(tx)

        # Random address not in the node
        tx['from'] = Account.create().address
        with self.assertRaises(SenderAccountNotFoundInNode):
            self.ethereum_client.send_transaction(tx)

        tx['from'] = address
        self.ethereum_client.send_transaction(tx)
        self.assertEqual(self.ethereum_client.get_balance(to), 1)

        with self.assertRaises(InvalidNonce):
            self.ethereum_client.send_transaction(tx)

        tx['value'] = self.ethereum_client.get_balance(address) + 1
        tx['nonce'] = self.ethereum_client.get_nonce_for_account(address)
        with self.assertRaises(InsufficientFunds):
            self.ethereum_client.send_transaction(tx)

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

        self.ethereum_client.send_unsigned_transaction(tx, public_key=address)
        self.assertEqual(self.ethereum_client.get_balance(to), value)
        first_nonce = tx['nonce']
        self.assertGreaterEqual(first_nonce, 0)

        # Will use the same nonce
        with self.assertRaisesMessage(InvalidNonce, 'correct nonce'):
            self.ethereum_client.send_unsigned_transaction(tx, public_key=address)

        # With retry, everything should work
        self.ethereum_client.send_unsigned_transaction(tx, public_key=address, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 1)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 2)

        # We try again with the first nonce, and should work too
        tx['nonce'] = first_nonce
        self.ethereum_client.send_unsigned_transaction(tx, public_key=address, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 2)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 3)

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

        self.ethereum_client.send_unsigned_transaction(tx, private_key=key)
        self.assertEqual(self.ethereum_client.get_balance(to), value)
        first_nonce = tx['nonce']
        self.assertGreaterEqual(first_nonce, 0)

        # Will use the same nonce
        with self.assertRaisesMessage(InvalidNonce, 'correct nonce'):
            self.ethereum_client.send_unsigned_transaction(tx, private_key=key)

        # With retry, everything should work
        self.ethereum_client.send_unsigned_transaction(tx, private_key=key, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 1)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 2)

        # We try again with the first nonce, and should work too
        tx['nonce'] = first_nonce
        self.ethereum_client.send_unsigned_transaction(tx, private_key=key, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 2)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 3)

    def test_wait_for_tx_receipt(self):
        value = 1
        to = Account.create().address

        tx_hash = self.ethereum_client.send_eth_to(self.ethereum_test_account.privateKey,
                                                    to=to, gas_price=self.gas_price, value=value)
        receipt1 = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=None)
        receipt2 = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=20)
        self.assertIsNotNone(receipt1)
        self.assertEqual(receipt1, receipt2)

        fake_tx_hash = self.w3.sha3(0)
        self.assertIsNone(self.ethereum_client.get_transaction_receipt(fake_tx_hash, timeout=None))
        self.assertIsNone(self.ethereum_client.get_transaction_receipt(fake_tx_hash, timeout=1))
