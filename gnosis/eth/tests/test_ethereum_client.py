from unittest import mock

from django.test import TestCase

from eth_account import Account
from hexbytes import HexBytes
from web3.datastructures import AttributeDict
from web3.net import Net

from ..constants import GAS_CALL_DATA_BYTE
from ..contracts import get_erc20_contract
from ..ethereum_client import (EthereumClientProvider, EthereumNetwork,
                               FromAddressNotFound, InsufficientFunds,
                               InvalidERC20Info, InvalidNonce,
                               SenderAccountNotFoundInNode)
from ..utils import get_eth_address_with_key
from .ethereum_test_case import EthereumTestCaseMixin


class TestERC20Module(EthereumTestCaseMixin, TestCase):
    def test_decode_erc20_or_erc721_log(self):
        logs = [AttributeDict({'address': '0x39C4BFa00b6edecCDd00fA9589E1BE76DE63e862',
                               'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27')],
                               'data': '0x000000000000000000000000000000000000000000000003aa2371d700680000',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 13,
                               'removed': False}),
                AttributeDict({'address': '0x39C4BFa00b6edecCDd00fA9589E1BE76DE63e862',
                               'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'),
                                          HexBytes('0x00000000000000000000000064da772dd84965f0ee58174941d78a9dfbccca2e')],
                               'data': '0x000000000000000000000000000000000000000000000001a055690d9db80000',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 14,
                               'removed': False}),
                AttributeDict({'address': '0x39C4BFa00b6edecCDd00fA9589E1BE76DE63e862',
                               'topics': [HexBytes('0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'),
                                          HexBytes('0x00000000000000000000000064da772dd84965f0ee58174941d78a9dfbccca2e'),
                                          HexBytes('0x00000000000000000000000080cdad25de6b439e866805b2dc6808d23ff57b5d')],
                               'data': '0x000000000000000000000000000000000000000000000001a055690d9db80000',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 15,
                               'removed': False}),
                AttributeDict({'address': '0x39C4BFa00b6edecCDd00fA9589E1BE76DE63e862',
                               'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
                                          HexBytes('0x00000000000000000000000064da772dd84965f0ee58174941d78a9dfbccca2e'),
                                          HexBytes('0x00000000000000000000000080cdad25de6b439e866805b2dc6808d23ff57b5d')],
                               'data': '0x000000000000000000000000000000000000000000000001a055690d9db80000',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 16,
                               'removed': False}),
                AttributeDict({'address': '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47',
                               'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
                                          HexBytes('0x00000000000000000000000099b9f9ba62002a9b43af6e540428277d5e52ef47'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'),
                                          HexBytes('0xcc292d3dab2c0fbbf616670ac57ec51162959c2d9cbe938819b6e8bc1c757335')],
                               'data': '0x',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 17,
                               'removed': False}),
                AttributeDict({'address': '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47',
                               'topics': [HexBytes('0x2114851a3e2a54429989f46c1ab0743e37ded205d9bbdfd85635aed5bd595a06'),
                                          HexBytes('0x00000000000000000000000099b9f9ba62002a9b43af6e540428277d5e52ef47'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'),
                                          HexBytes('0xcc292d3dab2c0fbbf616670ac57ec51162959c2d9cbe938819b6e8bc1c757335')],
                               'data': '0x0000000000000000000000000000000000000000000000000000000000000001',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 18,
                               'removed': False}),
                AttributeDict({'address': '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47',
                               'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
                                          HexBytes('0x00000000000000000000000099b9f9ba62002a9b43af6e540428277d5e52ef47'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'),
                                          HexBytes('0xe37edda38a308a6fae15178579aab28bc7f9e46e52fde30c3a46b82b7461aa08')],
                               'data': '0x',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 19,
                               'removed': False}),
                AttributeDict({'address': '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47',
                               'topics': [HexBytes('0x2114851a3e2a54429989f46c1ab0743e37ded205d9bbdfd85635aed5bd595a06'),
                                          HexBytes('0x00000000000000000000000099b9f9ba62002a9b43af6e540428277d5e52ef47'),
                                          HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'),
                                          HexBytes('0xe37edda38a308a6fae15178579aab28bc7f9e46e52fde30c3a46b82b7461aa08')],
                               'data': '0x0000000000000000000000000000000000000000000000000000000000000001',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 20,
                               'removed': False}),
                AttributeDict({'address': '0x64DA772DD84965f0Ee58174941d78a9DfBccca2e',
                               'topics': [HexBytes('0x3c8fbbba495ddb1296f967c80627bcca81b77be0b349ed8ae5f604365c22e9c7')],
                               'data': '0x6e4f8d9f6517dfa28f202b2e2582943d1bd567dfb0c4a774989715c29e4aed180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000039c4bfa00b6edeccdd00fa9589e1be76de63e862000000000000000000000000000000000000000000000003aa2371d7006800000000000000000000000000000000000000000000000000000000000000000001',
                               'blockNumber': 4357126,
                               'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'),
                               'transactionIndex': 14,
                               'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'),
                               'logIndex': 21,
                               'removed': False})]

        # TODO Test with ganache
        decoded_logs = self.ethereum_client.erc20.decode_logs(logs)
        self.assertEqual(len(decoded_logs), 5)
        self.assertEqual(len([event for event in decoded_logs if 'tokenId' in event['args']]), 2)
        self.assertEqual(len([event for event in decoded_logs if 'value' in event['args']]), 3)
        self.assertEqual(decoded_logs[1]['args']['value'], 30000000000000000000)
        self.assertEqual(decoded_logs[1]['args']['from'], '0x94E01661eBaef430fE862f958c03200b0F483f27')
        self.assertEqual(decoded_logs[1]['args']['to'], '0x64DA772DD84965f0Ee58174941d78a9DfBccca2e')
        self.assertEqual(decoded_logs[3]['args']['tokenId'],
                         92344574081811136966607054691835999266725413506859602442775390826469350798133)
        self.assertEqual(decoded_logs[3]['args']['from'], '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47')
        self.assertEqual(decoded_logs[3]['args']['to'], '0x94E01661eBaef430fE862f958c03200b0F483f27')
        self.assertEqual(decoded_logs[1]['blockNumber'], 4357126)

    def test_get_balance(self):
        amount = 1000
        address, _ = get_eth_address_with_key()
        erc20_contract = self.deploy_example_erc20(amount, address)
        token_balance = self.ethereum_client.erc20.get_balance(address, erc20_contract.address)
        self.assertTrue(token_balance, amount)

        another_account, _ = get_eth_address_with_key()
        token_balance = self.ethereum_client.erc20.get_balance(another_account, erc20_contract.address)
        self.assertEqual(token_balance, 0)

    def test_get_balances(self):
        account_address = Account.create().address
        self.assertEqual(self.ethereum_client.erc20.get_balances(account_address, []),
                         [{'token_address': None, 'balance': 0}])

        value = 7
        self.send_ether(account_address, 7)
        self.assertEqual(self.ethereum_client.erc20.get_balances(account_address, []),
                         [{'token_address': None, 'balance': value}])

        tokens_value = 12
        erc20 = self.deploy_example_erc20(tokens_value, account_address)
        self.assertCountEqual(self.ethereum_client.erc20.get_balances(account_address, [erc20.address]),
                              [{'token_address': None, 'balance': value},
                               {'token_address': erc20.address, 'balance': tokens_value}])

        tokens_value_2 = 19
        erc20_2 = self.deploy_example_erc20(tokens_value_2, account_address)
        self.assertCountEqual(self.ethereum_client.erc20.get_balances(account_address, [erc20.address,
                                                                                        erc20_2.address]),
                              [{'token_address': None, 'balance': value},
                               {'token_address': erc20.address, 'balance': tokens_value},
                               {'token_address': erc20_2.address, 'balance': tokens_value_2}
                               ])

    def test_batch_call(self):
        account_address = Account.create().address
        tokens_value = 12
        erc20 = self.deploy_example_erc20(tokens_value, account_address)
        results = self.ethereum_client.batch_call([erc20.functions.decimals(),
                                                   erc20.functions.symbol(),
                                                   erc20.functions.balanceOf(account_address)])
        decimals, symbol, balance_of = results
        self.assertEqual(decimals, erc20.functions.decimals().call())
        self.assertEqual(symbol, erc20.functions.symbol().call())
        self.assertEqual(balance_of, tokens_value)

        invalid_erc20 = get_erc20_contract(self.ethereum_client.w3, Account.create().address)
        with self.assertRaises(ValueError):
            self.ethereum_client.batch_call([invalid_erc20.functions.decimals(),
                                             invalid_erc20.functions.symbol(),
                                             invalid_erc20.functions.balanceOf(account_address)])
        # It shouldn't raise error and instead return None
        self.assertEqual(self.ethereum_client.batch_call([invalid_erc20.functions.decimals(),
                                                          invalid_erc20.functions.symbol(),
                                                          invalid_erc20.functions.balanceOf(account_address)],
                                                         raise_exception=False),
                         [None, None, None])

    def test_get_blocks(self):
        self.assertEqual(self.ethereum_client.get_blocks([]), [])
        # Generate 3 blocks
        to = Account.create().address
        value = 345
        for _ in range(3):
            self.send_ether(to, value)

        block_numbers = [self.ethereum_client.current_block_number - i for i in range(3)]
        blocks = self.ethereum_client.get_blocks(block_numbers, full_transactions=True)
        for i, block in enumerate(blocks):
            self.assertEqual(block['number'], block_numbers[i])
            self.assertEqual(len(block['hash']), 32)
            self.assertEqual(len(block['parentHash']), 32)
            self.assertGreaterEqual(len(block['transactions']), 0)

    def test_get_total_transfer_history(self):
        amount = 50
        owner_account = self.create_account(initial_ether=0.01)
        account_1 = self.create_account(initial_ether=0.01)
        account_2 = self.create_account(initial_ether=0.01)
        account_3 = self.create_account(initial_ether=0.01)
        erc20_contract = self.deploy_example_erc20(amount, owner_account.address)
        # `owner` sends `amount // 2` to `account_1` and `account_3`
        self.send_tx(erc20_contract.functions.transfer(account_1.address,
                                                       amount // 2).buildTransaction({'from': owner_account.address}),
                     owner_account)
        self.send_tx(erc20_contract.functions.transfer(account_3.address,
                                                       amount // 2).buildTransaction({'from': owner_account.address}),
                     owner_account)
        logs = self.ethereum_client.erc20.get_total_transfer_history([account_1.address])
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['args']['from'], owner_account.address)
        self.assertEqual(logs[0]['args']['to'], account_1.address)
        self.assertEqual(logs[0]['args']['value'], amount // 2)
        log_0_block_number = logs[0]['blockNumber']

        # `account1` sends `amount // 2` (all) to `account_2`
        self.send_tx(erc20_contract.functions.transfer(account_2.address,
                                                       amount // 2).buildTransaction({'from': account_1.address}),
                     account_1)
        logs = self.ethereum_client.erc20.get_total_transfer_history([account_1.address])
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[1]['args']['from'], account_1.address)
        self.assertEqual(logs[1]['args']['to'], account_2.address)
        self.assertEqual(logs[1]['args']['value'], amount // 2)
        self.assertGreaterEqual(logs[1]['blockNumber'], log_0_block_number)

        logs = self.ethereum_client.erc20.get_total_transfer_history([account_3.address])
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['args']['from'], owner_account.address)
        self.assertEqual(logs[0]['args']['to'], account_3.address)
        self.assertEqual(logs[0]['args']['value'], amount // 2)

        logs = self.ethereum_client.erc20.get_total_transfer_history([account_2.address, account_3.address])
        self.assertEqual(len(logs), 2)

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

        with self.assertRaises(InvalidERC20Info):
            self.ethereum_client.erc20.get_info(Account.create().address)

    def test_send_tokens(self):
        amount = 5
        owner = self.ethereum_test_account
        owner_2 = Account.create()
        erc20 = self.deploy_example_erc20(amount, owner.address)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner.address, erc20.address), amount)

        amount_2 = 3
        self.ethereum_client.erc20.send_tokens(owner_2.address, amount_2, erc20.address, owner.key)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner.address, erc20.address), amount - amount_2)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner_2.address, erc20.address), amount_2)


class TestParityModule(EthereumTestCaseMixin, TestCase):
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
            {
                "action": {
                    "callType": "call",
                    "from": "0xed85033a23027439fb20f381f5930ba67f1ebee0",
                    "gas": "0x0",
                    "input": "0x",
                    "to": "0x0affccd762f0a7fa1bca40c51afe1a806a74a6f9",
                    "value": "0x11c290633b7000"
                },
                "blockHash": "0xbf3a508137e72b20399852becdee1752c7b9986184f835014d12b10c01746f39",
                "blockNumber": 7556887,
                "error": "Out of gas",
                "subtraces": 0,
                "traceAddress": [],
                "transactionHash": "0xec7e447ce8eef033a8c85442a281bd34436e576553c7d98fbe859af7754a9064",
                "transactionPosition": 117,
                "type": "call"
            },
            {'action': {'address': '0x4440adafbc6c4e45c299451c0eedc7c8b98c14ac',
                        'balance': '0xa',
                        'refundAddress': '0x1240adafbc6c4e45c299451c0eedc7c8b98c2222'},
             'blockHash': '0x8512d367492371edf44ebcbbbd935bc434946dddc2b126cb558df5906012186c',
             'blockNumber': 7829689,
             'result': None,
             'subtraces': 0,
             'traceAddress': [0, 0, 0, 0, 0, 0],
             'transactionHash': '0x5f7af6aa390f9f8dd79ee692c37cbde76bb7869768b1bac438b6d176c94f637d',
             'transactionPosition': 35,
             'type': 'suicide'},
        ]
        at_least_one_error = False
        at_least_one_self_destruct = False
        decoded_traces = self.ethereum_client.parity._decode_traces(example_traces)
        for example_trace, decoded_trace in zip(example_traces, decoded_traces):
            if decoded_trace['type'] == 'suicide':
                self.assertEqual(decoded_trace['action']['address'], '0x4440AdaFBc6c4E45C299451C0eEdC7C8B98c14Ac')
                self.assertEqual(decoded_trace['action']['balance'], 10)
                self.assertEqual(decoded_trace['action']['refundAddress'], '0x1240aDafBC6C4e45C299451C0eEdC7c8B98C2222')
                at_least_one_self_destruct = True
            else:
                self.assertEqual(decoded_trace['action']['gas'], int(example_trace['action']['gas'], 16))
                self.assertEqual(decoded_trace['action']['value'], int(example_trace['action']['value'], 16))
                if 'error' in decoded_trace:
                    self.assertNotIn('result', decoded_trace)
                    at_least_one_error = True
                else:
                    self.assertEqual(decoded_trace['result']['gasUsed'], int(example_trace['result']['gasUsed'], 16))

        self.assertTrue(at_least_one_error)
        self.assertTrue(at_least_one_self_destruct)

        self.assertEqual(decoded_traces[0]['result']['output'], HexBytes(''))
        self.assertEqual(decoded_traces[1]['result']['address'],
                         self.w3.toChecksumAddress(example_traces[1]['result']['address']))
        self.assertEqual(decoded_traces[1]['result']['code'],
                         HexBytes(example_traces[1]['result']['code']))

        self.assertEqual(decoded_traces[2]['error'], 'Out of gas')

    def test_trace_filter(self):
        with self.assertRaisesMessage(AssertionError, 'at least'):
            self.ethereum_client.parity.trace_filter()

        with self.assertRaisesMessage(ValueError, 'Method trace_filter not supported'):
            self.ethereum_client.parity.trace_filter(from_address=Account.create().address)


class TestEthereumNetwork(EthereumTestCaseMixin, TestCase):
    def test_default_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(EthereumNetwork.default), EthereumNetwork.UNKNOWN)

    def test_default_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(2), EthereumNetwork.UNKNOWN)

    def test_mainnet_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(1), EthereumNetwork.MAINNET)

    def test_rinkeby_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(4), EthereumNetwork.RINKEBY)


class TestEthereumClient(EthereumTestCaseMixin, TestCase):
    def test_current_block_number(self):
        self.assertGreaterEqual(self.ethereum_client.current_block_number, 0)

    def test_get_transaction(self):
        to = Account.create().address
        value = 123
        tx_hash = self.send_ether(to, value)
        tx = self.ethereum_client.get_transaction(tx_hash)
        self.assertEqual(tx.to, to)
        self.assertEqual(tx.value, value)
        block = self.ethereum_client.get_block(tx.blockNumber)
        self.assertEqual(block.number, tx.blockNumber)

    def test_get_transactions(self):
        self.assertEqual(self.ethereum_client.get_transactions([]), [])
        to = Account.create().address
        values = [123, 234, 567]
        tx_hashes = [self.send_ether(to, values[i]) for i in range(3)]
        txs = self.ethereum_client.get_transactions(tx_hashes)
        for i, tx in enumerate(txs):
            self.assertEqual(tx['to'], to)
            self.assertEqual(tx['value'], values[i])

        self.assertEqual(self.ethereum_client.get_transaction_receipts([]), [])
        receipts = self.ethereum_client.get_transaction_receipts(tx_hashes)
        for i, receipt in enumerate(receipts):
            self.assertEqual(receipt['status'], 1)
            self.assertGreaterEqual(receipt['gasUsed'], 21000)

    def test_check_tx_with_confirmations(self):
        value = 1
        to, _ = get_eth_address_with_key()

        tx_hash = self.ethereum_client.send_eth_to(self.ethereum_test_account.key,
                                                   to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))

        _ = self.ethereum_client.send_eth_to(self.ethereum_test_account.key,
                                             to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))

        _ = self.ethereum_client.send_eth_to(self.ethereum_test_account.key,
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

    def test_get_ethereum_network_default(self):
        self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.UNKNOWN)

    @mock.patch.object(Net, 'version', return_value='1', new_callable=mock.PropertyMock)
    def test_mock_get_ethereum_network_mainnet(self, version_mock):
        self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.MAINNET)

    @mock.patch.object(Net, 'version', return_value='4', new_callable=mock.PropertyMock)
    def test_mock_get_ethereum_network_rinkeby(self, version_mock):
        self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.RINKEBY)

    def test_get_nonce(self):
        address = Account.create().address
        nonce = self.ethereum_client.get_nonce_for_account(address)
        self.assertEqual(nonce, 0)

        nonce = self.ethereum_client.get_nonce_for_account(address, block_identifier='pending')
        self.assertEqual(nonce, 0)

    def test_estimate_data_gas(self):
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('')), 0)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x00')), 4)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x000204')), 4 + GAS_CALL_DATA_BYTE * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x050204')), GAS_CALL_DATA_BYTE * 3)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x0502040000')), GAS_CALL_DATA_BYTE * 3 + 4 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x050204000001')), GAS_CALL_DATA_BYTE * 4 + 4 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x00050204000001')),
                         4 + GAS_CALL_DATA_BYTE * 4 + 4 * 2)

    def test_provider_singleton(self):
        ethereum_client1 = EthereumClientProvider()
        ethereum_client2 = EthereumClientProvider()
        self.assertEqual(ethereum_client1, ethereum_client2)

    def test_send_eth_to(self):
        address, _ = get_eth_address_with_key()
        value = 1
        self.ethereum_client.send_eth_to(self.ethereum_test_account.key, address, self.gas_price, value)
        self.assertEqual(self.ethereum_client.get_balance(address), value)

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

        with self.assertRaisesMessage(ValueError, 'Ethereum account was not configured'):
            self.ethereum_client.send_unsigned_transaction(tx)

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
        key = account.key
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

        tx_hash = self.ethereum_client.send_eth_to(self.ethereum_test_account.key,
                                                   to=to, gas_price=self.gas_price, value=value)
        receipt1 = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=None)
        receipt2 = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=20)
        self.assertIsNotNone(receipt1)
        self.assertEqual(receipt1, receipt2)

        fake_tx_hash = self.w3.keccak(0)
        self.assertIsNone(self.ethereum_client.get_transaction_receipt(fake_tx_hash, timeout=None))
        self.assertIsNone(self.ethereum_client.get_transaction_receipt(fake_tx_hash, timeout=1))
