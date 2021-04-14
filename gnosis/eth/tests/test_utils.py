from django.test import TestCase

from eth_abi.packed import encode_abi_packed
from eth_account import Account
from hexbytes import HexBytes

from ..contracts import (get_proxy_1_0_0_deployed_bytecode,
                         get_proxy_factory_contract)
from ..utils import (compare_byte_code, decode_string_or_bytes32,
                     generate_address_2)
from .ethereum_test_case import EthereumTestCaseMixin


class TestUtils(EthereumTestCaseMixin, TestCase):
    def test_generate_address_2(self):
        from_ = '0x8942595A2dC5181Df0465AF0D7be08c8f23C93af'
        salt = self.w3.keccak(text='aloha')
        init_code = '0x00abcd'
        expected = '0x8D02C796Dd019916F65EBa1C9D65a7079Ece00E0'
        address2 = generate_address_2(from_, salt, init_code)
        self.assertEqual(address2, expected)

        from_ = HexBytes('0x8942595A2dC5181Df0465AF0D7be08c8f23C93af')
        salt = self.w3.keccak(text='aloha').hex()
        init_code = HexBytes('0x00abcd')
        expected = '0x8D02C796Dd019916F65EBa1C9D65a7079Ece00E0'
        address2 = generate_address_2(from_, salt, init_code)
        self.assertEqual(address2, expected)

    def test_generate_address2_with_proxy(self):
        deployer_account = self.ethereum_test_account
        proxy_factory_contract = get_proxy_factory_contract(self.w3)
        nonce = self.w3.eth.get_transaction_count(deployer_account.address, block_identifier='pending')
        tx = proxy_factory_contract.constructor().buildTransaction({'nonce': nonce,
                                                                    'from': deployer_account.address})
        signed_tx = deployer_account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
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
        signed_tx = deployer_account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        logs = proxy_factory_contract.events.ProxyCreation().processReceipt(tx_receipt)
        log = logs[0]
        self.assertEqual(log['event'], 'ProxyCreation')
        proxy_address = log['args']['proxy']

        proxy_creation_code = proxy_factory_contract.functions.proxyCreationCode().call()
        salt = self.w3.keccak(encode_abi_packed(['bytes', 'uint256'], [self.w3.keccak(initializer), salt_nonce]))
        deployment_data = encode_abi_packed(['bytes', 'uint256'], [proxy_creation_code, int(master_copy, 16)])
        address2 = generate_address_2(proxy_factory_contract.address, salt, deployment_data)
        self.assertEqual(proxy_address, address2)

    def test_decode_string_or_bytes32(self):
        # Abi encoded string
        gnosis_hex = HexBytes('0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000'
                              '00000000000000000000000000000000000000000c476e6f73697320546f6b656e0000000000000000000000'
                              '000000000000000000')

        # Abi encoded bytes32
        dai_hex = HexBytes('0x44616920537461626c65636f696e2076312e3000000000000000000000000000')

        self.assertEqual(decode_string_or_bytes32(gnosis_hex), 'Gnosis Token')
        self.assertEqual(decode_string_or_bytes32(dai_hex), 'Dai Stablecoin v1.0')

    def test_compare_byte_code(self):
        proxy_with_metadata = get_proxy_1_0_0_deployed_bytecode()
        proxy_with_different_metadata = HexBytes('0x608060405273ffffffffffffffffffffffffffffffffffffffff60005416366000'
                                                 '8037600080366000845af43d6000803e6000811415603d573d6000fd5b3d6000f3fe'
                                                 'a165627a7a72305820b7f4e514a2bdfeb2e729e84f7101233a43b51d677007041e70'
                                                 '8067e4b88bec480029')
        self.assertTrue(compare_byte_code(proxy_with_metadata, proxy_with_different_metadata))
