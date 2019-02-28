from django.test import TestCase

from eth_abi2.packed import encode_abi_packed
from eth_account import Account
from hexbytes import HexBytes

from ..contracts import get_proxy_factory_contract
from ..utils import generate_address_2
from .ethereum_test_case import EthereumTestCaseMixin


class TestUtils(EthereumTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_generate_address_2(self):
        from_ = '0x8942595A2dC5181Df0465AF0D7be08c8f23C93af'
        salt = self.w3.sha3(text='aloha')
        init_code = '0x00abcd'
        expected = '0x8D02C796Dd019916F65EBa1C9D65a7079Ece00E0'
        address2 = generate_address_2(from_, salt, init_code)
        self.assertEqual(address2, expected)

        from_ = HexBytes('0x8942595A2dC5181Df0465AF0D7be08c8f23C93af')
        salt = self.w3.sha3(text='aloha').hex()
        init_code = HexBytes('0x00abcd')
        expected = '0x8D02C796Dd019916F65EBa1C9D65a7079Ece00E0'
        address2 = generate_address_2(from_, salt, init_code)
        self.assertEqual(address2, expected)

    def test_generate_address2_with_proxy(self):
        deployer_account = self.ethereum_test_account
        proxy_factory_contract = get_proxy_factory_contract(self.w3)
        nonce = self.w3.eth.getTransactionCount(deployer_account.address, 'pending')
        tx = proxy_factory_contract.constructor().buildTransaction({'nonce': nonce,
                                                                    'from': deployer_account.address})
        signed_tx = deployer_account.signTransaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        proxy_factory_contract = get_proxy_factory_contract(self.w3, address=tx_receipt['contractAddress'])

        initializer = b''  # Should be the safe `setup()` call with `owners`, `threshold`, `payment`...
        salt_nonce = 0  # Random. For sure. I used a dice

        master_copy = Account.create().address
        tx = proxy_factory_contract.functions.createProxyWithNonce(master_copy,
                                                                   initializer,
                                                                   salt_nonce
                                                                   ).buildTransaction({'nonce': nonce + 1,
                                                                                       'from': deployer_account.address,
                                                                                       })
        signed_tx = deployer_account.signTransaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        logs = proxy_factory_contract.events.ProxyCreation().processReceipt(tx_receipt)
        log = logs[0]
        self.assertEqual(log['event'], 'ProxyCreation')
        proxy_address = log['args']['proxy']

        proxy_creation_code = proxy_factory_contract.functions.proxyCreationCode().call()
        salt = self.w3.sha3(encode_abi_packed(['bytes', 'uint256'], [self.w3.sha3(initializer), salt_nonce]))
        deployment_data = encode_abi_packed(['bytes', 'uint256'], [proxy_creation_code, int(master_copy, 16)])
        address2 = generate_address_2(proxy_factory_contract.address, salt, deployment_data)
        self.assertEqual(proxy_address, address2)
