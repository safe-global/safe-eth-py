import logging

from django.conf import settings
from django.test import TestCase
from django_eth.constants import NULL_ADDRESS
from ethereum.utils import checksum_encode, ecrecover_to_pub, sha3

from ..contracts import get_safe_contract
from ..safe_creation_tx import SafeCreationTx
from .factories import generate_valid_s
from .test_safe_service import TestCaseWithSafeContractMixin

logger = logging.getLogger(__name__)

LOG_TITLE_WIDTH = 100

GAS_PRICE = settings.SAFE_GAS_PRICE


class TestSafeCreationTx(TestCase, TestCaseWithSafeContractMixin):
    @classmethod
    def setUpTestData(cls):
        cls.prepare_safe_tests()

    def test_safe_creation_tx_builder(self):
        logger.info("Test Safe Proxy creation without payment".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3

        s = generate_valid_s()

        funder = w3.eth.accounts[1]
        owners = w3.eth.accounts[2:6]
        threshold = len(owners) - 1
        gas_price = GAS_PRICE

        safe_builder = SafeCreationTx(w3=w3,
                                      owners=owners,
                                      threshold=threshold,
                                      signature_s=s,
                                      master_copy=self.safe_contract_address,
                                      gas_price=gas_price,
                                      funder=NULL_ADDRESS)

        logger.info("Send %d gwei to deployer %s",
                    w3.fromWei(safe_builder.payment, 'gwei'),
                    safe_builder.deployer_address)
        w3.eth.sendTransaction({
            'from': funder,
            'to': safe_builder.deployer_address,
            'value': safe_builder.payment
        })

        logger.info("Create proxy contract with address %s", safe_builder.safe_address)

        tx_hash = w3.eth.sendRawTransaction(safe_builder.raw_tx)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.contractAddress, safe_builder.safe_address)

        deployed_safe_proxy_contract = get_safe_contract(w3, tx_receipt.contractAddress)

        logger.info("Deployer account has still %d gwei left (will be lost)",
                    w3.fromWei(w3.eth.getBalance(safe_builder.deployer_address), 'gwei'))

        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)

    def test_safe_creation_tx_builder_with_payment(self):
        logger.info("Test Safe Proxy creation With Payment".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3

        s = generate_valid_s()

        funder = w3.eth.accounts[1]
        owners = w3.eth.accounts[2:4]
        threshold = len(owners) - 1
        user_external_account = w3.eth.accounts[6]
        gas_price = GAS_PRICE

        safe_builder = SafeCreationTx(w3=w3,
                                      owners=owners,
                                      threshold=threshold,
                                      signature_s=s,
                                      master_copy=self.safe_contract_address,
                                      gas_price=gas_price,
                                      funder=funder)

        ether = 0.01
        logger.info("Send %d ether to safe %s", ether, safe_builder.deployer_address)
        w3.eth.sendTransaction({
            'from': user_external_account,
            'to': safe_builder.safe_address,
            'value': w3.toWei(ether, 'ether')
        })
        self.assertEqual(w3.eth.getBalance(safe_builder.safe_address), w3.toWei(ether, 'ether'))

        ether = safe_builder.payment
        logger.info("Send %d gwei to deployer %s", w3.fromWei(ether, 'gwei'), safe_builder.deployer_address)
        w3.eth.sendTransaction({
            'from': funder,
            'to': safe_builder.deployer_address,
            'value': safe_builder.payment
        })

        logger.info("Create proxy contract with address %s", safe_builder.safe_address)

        funder_balance = w3.eth.getBalance(funder)

        # This tx will create the Safe Proxy and return ether to the funder
        tx_hash = w3.eth.sendRawTransaction(safe_builder.raw_tx)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.contractAddress, safe_builder.safe_address)

        self.assertEqual(w3.eth.getBalance(funder), funder_balance + safe_builder.payment)

        logger.info("Deployer account has still %d gwei left (will be lost)",
                    w3.fromWei(w3.eth.getBalance(safe_builder.deployer_address), 'gwei'))

        deployed_safe_proxy_contract = get_safe_contract(w3, tx_receipt.contractAddress)

        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)

    def test_safe_gas_with_multiple_owners(self):
        logger.info("Test Safe Proxy creation gas with multiple owners".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3
        number_of_accounts = len(w3.eth.accounts)
        for i in range(2, number_of_accounts):
            s = generate_valid_s()
            owners = w3.eth.accounts[1:i]
            threshold = len(owners)
            gas_price = w3.toWei(15, 'gwei')

            safe_builder = SafeCreationTx(w3=w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.safe_contract_address,
                                          gas_price=gas_price,
                                          funder=None)

            w3.eth.sendTransaction({
                'from': w3.eth.accounts[0],
                'to': safe_builder.deployer_address,
                'value': safe_builder.payment
            })
            tx_hash = w3.eth.sendRawTransaction(safe_builder.raw_tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            self.assertEqual(tx_receipt.contractAddress, safe_builder.safe_address)

            logger.info("Number of owners: %d - Gas estimated %d - Gas Used %d - Difference %d",
                        len(owners),
                        safe_builder.gas,
                        tx_receipt.gasUsed,
                        safe_builder.gas - tx_receipt.gasUsed)

    def test_w3_same_tx_pyethereum(self):
        w3 = self.w3

        owners = w3.eth.accounts[2:6]
        threshold = len(owners) - 1
        funder = w3.eth.accounts[1]
        gas_price = w3.toWei(15, 'gwei')

        s = generate_valid_s()

        safe_builder = SafeCreationTx(w3=w3,
                                      owners=owners,
                                      threshold=threshold,
                                      signature_s=s,
                                      master_copy=self.safe_contract_address,
                                      gas_price=gas_price,
                                      funder=funder)

        web3_transaction = safe_builder.contract_creation_tx_dict

        # Signing transaction
        v, r = safe_builder.v, safe_builder.r

        rlp_encoded_transaction, hash = SafeCreationTx._sign_web3_transaction(web3_transaction, v, r, s)

        address_64_encoded = ecrecover_to_pub(hash, v, r, s)
        address_bytes = sha3(address_64_encoded)[-20:]
        deployer_address = checksum_encode(address_bytes)

        self.assertEqual(safe_builder.raw_tx, rlp_encoded_transaction)
        self.assertEqual(safe_builder.deployer_address, deployer_address)
