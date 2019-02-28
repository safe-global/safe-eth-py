import logging

from django.test import TestCase

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.utils import get_eth_address_with_key

from ..safe_create2_tx import SafeCreate2TxBuilder
from .test_safe_service import SafeTestCaseMixin
from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)

LOG_TITLE_WIDTH = 100


class TestSafeCreationTx(TestCase, SafeTestCaseMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_tests()

    def test_safe_create2_tx_builder(self):
        w3 = self.w3

        salt_nonce = generate_salt_nonce()
        funder_account = self.ethereum_test_account
        owners = [get_eth_address_with_key()[0] for _ in range(4)]
        threshold = len(owners) - 1
        gas_price = self.gas_price

        safe_creation_tx = SafeCreate2TxBuilder(w3=w3,
                                                master_copy_address=self.safe_contract_address,
                                                proxy_factory_address=self.proxy_factory_contract_address
                                                ).build(owners=owners,
                                                        threshold=threshold,
                                                        salt_nonce=salt_nonce,
                                                        gas_price=gas_price,
                                                        payment_receiver=NULL_ADDRESS)

        self.send_tx({
            'to': safe_creation_tx.safe_address,
            'value': safe_creation_tx.payment_ether
        }, funder_account)

        tx_hash, contract_address = self.safe_service.deploy_proxy_contract_with_nonce(salt_nonce,
                                                                                       safe_creation_tx.safe_setup_data,
                                                                                       safe_creation_tx.gas,
                                                                                       safe_creation_tx.gas_price,
                                                                                       deployer_private_key=funder_account.privateKey)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.status, 1)
        logs = self.proxy_factory_contract.events.ProxyCreation().processReceipt(tx_receipt)
        log = logs[0]
        self.assertIsNone(tx_receipt.contractAddress)
        self.assertEqual(log['event'], 'ProxyCreation')
        proxy_address = log['args']['proxy']
        self.assertEqual(proxy_address, safe_creation_tx.safe_address)
        self.assertEqual(contract_address, safe_creation_tx.safe_address)

        deployed_safe_proxy_contract = get_safe_contract(w3, proxy_address)
        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)
        self.assertEqual(self.ethereum_service.get_balance(proxy_address), 0)
