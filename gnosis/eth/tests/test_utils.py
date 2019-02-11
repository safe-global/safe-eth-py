from django.test import TestCase

from eth_abi import encode_abi
from eth_account import Account
from hexbytes import HexBytes

from ..constants import NULL_ADDRESS
from ..contracts import get_proxy_factory2_contract
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

        deployer_account = self.ethereum_test_account
        proxy_factory2_contract = get_proxy_factory2_contract(self.w3)
        nonce = self.w3.eth.getTransactionCount(deployer_account.address, 'pending')
        tx = proxy_factory2_contract.constructor().buildTransaction({'nonce': nonce,
                                                                     'from': deployer_account.address})
        signed_tx = deployer_account.signTransaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        proxy_factory2_contract = get_proxy_factory2_contract(self.w3, address=tx_receipt['contractAddress'])

        safe_initializer = b''  # Should be the setup() call with owners, threshold...
        payment_token = NULL_ADDRESS
        payment = 0
        creation_nonce = 0

        implementation = Account.create().address
        tx = proxy_factory2_contract.functions.createProxy(implementation, safe_initializer,
                                                           payment_token, payment,
                                                           creation_nonce).buildTransaction({
                                                                                    'nonce': nonce + 1,
                                                                                    'from': deployer_account.address,
                                                                                    })
        signed_tx = deployer_account.signTransaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        logs = proxy_factory2_contract.events.ProxyCreated().processReceipt(tx_receipt)
        log = logs[0]
        self.assertEqual(log['event'], 'ProxyCreated')
        proxy_address = log['args']['proxy']

        proxy_creation_code = proxy_factory2_contract.functions.proxyCreationCode().call()
        encoded_nonce = encode_abi(['uint256'], [creation_nonce])
        encoded_constructor_data = encode_abi(['address', 'address', 'uint256'], [implementation, payment_token, payment])
        address2 = generate_address_2(proxy_factory2_contract.address,
                                      self.w3.sha3(safe_initializer + encoded_nonce),
                                      proxy_creation_code + encoded_constructor_data)
        self.assertEqual(proxy_address, address2)
