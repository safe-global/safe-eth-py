import logging

from django.test import TestCase

from eth_account import Account
from web3 import Web3

from gnosis.eth import EthereumClient
from gnosis.eth.contracts import (
    get_proxy_1_0_0_deployed_bytecode,
    get_proxy_1_1_1_deployed_bytecode,
    get_proxy_1_3_0_deployed_bytecode,
)
from gnosis.eth.tests.utils import just_test_if_mainnet_node
from gnosis.eth.utils import compare_byte_code
from gnosis.safe import Safe
from gnosis.safe.proxy_factory import (
    ProxyFactory,
    ProxyFactoryV100,
    ProxyFactoryV111,
    ProxyFactoryV130,
)
from gnosis.safe.tests.safe_test_case import SafeTestCaseMixin
from gnosis.safe.tests.utils import generate_salt_nonce

logger = logging.getLogger(__name__)


class TestProxyFactory(SafeTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.proxy_factory = ProxyFactory(
            cls.proxy_factory_contract.address, cls.ethereum_client
        )

    def test_check_proxy_code(self):
        proxy_contract_address = self.deploy_test_safe().address
        self.assertTrue(self.proxy_factory.check_proxy_code(proxy_contract_address))

        self.assertFalse(
            self.proxy_factory.check_proxy_code(self.safe_contract.address)
        )

        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account, self.safe_contract.address
        )
        self.assertTrue(
            self.proxy_factory.check_proxy_code(ethereum_tx_sent.contract_address)
        )
        # Test every version
        versions = [
            ("1.0.0", ProxyFactoryV100, get_proxy_1_0_0_deployed_bytecode),
            ("1.1.1", ProxyFactoryV111, get_proxy_1_1_1_deployed_bytecode),
            ("1.3.0", ProxyFactoryV130, get_proxy_1_3_0_deployed_bytecode),
        ]
        for version, ProxyFactoryVersion, get_proxy_deployed_bytecode_fn in versions:
            with self.subTest(version=version):
                deployed_proxy_tx = ProxyFactoryVersion.deploy_contract(
                    self.ethereum_client, self.ethereum_test_account
                )
                proxy_factory = ProxyFactory(
                    deployed_proxy_tx.contract_address,
                    self.ethereum_client,
                    version=version,
                )
                deployed_proxy_contract_tx = (
                    proxy_factory.deploy_proxy_contract_with_nonce(
                        self.ethereum_test_account, self.safe_contract.address
                    )
                )
                self.assertTrue(
                    proxy_factory.check_proxy_code(
                        deployed_proxy_contract_tx.contract_address
                    )
                )
                self.assertTrue(
                    compare_byte_code(
                        get_proxy_deployed_bytecode_fn(),
                        self.w3.eth.get_code(
                            deployed_proxy_contract_tx.contract_address
                        ),
                    )
                )

    def test_check_proxy_code_mainnet(self):
        mainnet_node = just_test_if_mainnet_node()
        ethereum_client = EthereumClient(mainnet_node)
        last_proxy_factory_address = "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2"
        proxy_factory = ProxyFactory(last_proxy_factory_address, ethereum_client)

        # Random Safes deployed by the proxy_factory
        safes = [
            "0x7f2722741F997c63133e656a70aE5Ae0614aD7f5",  # v1.0.0
            "0x655A9e6b044d6B62F393f9990ec3eA877e966e18",  # v1.1.1
            # '',  # v1.2.0
            "0xDaB5dc22350f9a6Aff03Cf3D9341aAD0ba42d2a6",  # v1.3.0
        ]

        for safe in safes:
            with self.subTest(safe=safe):
                self.assertTrue(proxy_factory.check_proxy_code(safe))

    def test_calculate_proxy_address(self):
        salt_nonce = 12
        address = self.proxy_factory.calculate_proxy_address(
            self.safe_contract_V1_4_1.address, b"", salt_nonce
        )
        self.assertTrue(Web3.is_checksum_address(address))
        # Same call with same parameters should return the same address
        same_address = self.proxy_factory.calculate_proxy_address(
            self.safe_contract_V1_4_1.address, b"", salt_nonce
        )
        self.assertEqual(address, same_address)
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract_V1_4_1.address,
            initializer=b"",
            salt_nonce=salt_nonce,
        )
        self.assertEqual(ethereum_tx_sent.contract_address, address)

        # Calculating the proxy address after deployment should return the same address
        address_after_deploying = self.proxy_factory.calculate_proxy_address(
            self.safe_contract_V1_4_1.address, b"", salt_nonce
        )
        self.assertEqual(ethereum_tx_sent.contract_address, address_after_deploying)

        chain_specific_address = self.proxy_factory.calculate_proxy_address(
            self.safe_contract_V1_4_1.address, b"", salt_nonce, chain_specific=True
        )
        self.assertTrue(Web3.is_checksum_address(chain_specific_address))
        self.assertNotEqual(address, chain_specific_address)
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract_V1_4_1.address,
            initializer=b"",
            salt_nonce=salt_nonce,
            chain_specific=True,
        )
        self.assertEqual(ethereum_tx_sent.contract_address, chain_specific_address)

    def test_deploy_proxy_contract_with_nonce(self):
        salt_nonce = generate_salt_nonce()
        owners = [Account.create().address for _ in range(2)]
        threshold = 2
        payment_token = None
        safe_create2_tx = Safe.build_safe_create2_tx(
            self.ethereum_client,
            self.safe_contract.address,
            self.proxy_factory_contract.address,
            salt_nonce,
            owners,
            threshold,
            self.gas_price,
            payment_token,
        )
        # Send ether for safe deploying costs
        self.send_tx(
            {"to": safe_create2_tx.safe_address, "value": safe_create2_tx.payment},
            self.ethereum_test_account,
        )

        proxy_factory = ProxyFactory(
            self.proxy_factory_contract.address, self.ethereum_client
        )
        ethereum_tx_sent = proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            safe_create2_tx.master_copy_address,
            safe_create2_tx.safe_setup_data,
            salt_nonce,
            safe_create2_tx.gas,
            gas_price=self.gas_price,
        )
        receipt = self.ethereum_client.get_transaction_receipt(
            ethereum_tx_sent.tx_hash, timeout=20
        )
        self.assertEqual(receipt["status"], 1)
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        self.assertEqual(
            ethereum_tx_sent.contract_address, safe_create2_tx.safe_address
        )
        self.assertEqual(set(safe.retrieve_owners()), set(owners))
        self.assertEqual(
            safe.retrieve_master_copy_address(), safe_create2_tx.master_copy_address
        )

    def test_get_proxy_runtime_code(self):
        with self.assertRaises(NotImplementedError):
            self.proxy_factory.get_proxy_runtime_code()
