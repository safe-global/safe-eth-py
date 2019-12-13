import logging

from django.test import TestCase

from eth_account import Account
from ethereum.utils import ecrecover_to_pub

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.utils import get_eth_address_with_key

from ..safe_creation_tx import SafeCreationTx
from .safe_test_case import SafeTestCaseMixin
from .utils import generate_valid_s

logger = logging.getLogger(__name__)

LOG_TITLE_WIDTH = 100


class TestSafeCreationTx(SafeTestCaseMixin, TestCase):
    def test_safe_creation_tx_builder(self):
        logger.info("Test Safe Proxy creation without payment".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3

        s = generate_valid_s()

        funder_account = self.ethereum_test_account
        owners = [get_eth_address_with_key()[0] for _ in range(4)]
        threshold = len(owners) - 1
        gas_price = self.gas_price

        safe_creation_tx = SafeCreationTx(w3=w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.safe_contract_V0_0_1_address,
                                          gas_price=gas_price,
                                          funder=NULL_ADDRESS)

        logger.info("Send %d gwei to deployer %s",
                    w3.fromWei(safe_creation_tx.payment_ether, 'gwei'),
                    safe_creation_tx.deployer_address)

        self.send_tx({
            'to': safe_creation_tx.deployer_address,
            'value': safe_creation_tx.payment_ether
        }, funder_account)

        logger.info("Create proxy contract with address %s", safe_creation_tx.safe_address)

        tx_hash = w3.eth.sendRawTransaction(safe_creation_tx.tx_raw)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.contractAddress, safe_creation_tx.safe_address)

        deployed_safe_proxy_contract = get_safe_contract(w3, tx_receipt.contractAddress)

        logger.info("Deployer account has still %d gwei left (will be lost)",
                    w3.fromWei(w3.eth.getBalance(safe_creation_tx.deployer_address), 'gwei'))

        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)

    def test_safe_creation_tx_builder_with_not_enough_funds(self):
        w3 = self.w3
        s = generate_valid_s()
        funder_account = self.ethereum_test_account
        owners = [get_eth_address_with_key()[0] for _ in range(4)]
        threshold = len(owners) - 1
        gas_price = self.gas_price

        safe_creation_tx = SafeCreationTx(w3=w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.safe_contract_V0_0_1_address,
                                          gas_price=gas_price,
                                          funder=NULL_ADDRESS)

        logger.info("Send %d gwei to deployer %s",
                    w3.fromWei(safe_creation_tx.payment_ether - 1, 'gwei'),
                    safe_creation_tx.deployer_address)
        self.send_tx({
            'to': safe_creation_tx.deployer_address,
            'value': safe_creation_tx.payment_ether - 1
        }, funder_account)

        with self.assertRaisesMessage(ValueError, 'enough funds'):
            w3.eth.sendRawTransaction(safe_creation_tx.tx_raw)

    def test_safe_creation_tx_builder_with_payment(self):
        logger.info("Test Safe Proxy creation With Payment".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3

        s = generate_valid_s()

        funder_account = self.ethereum_test_account
        owners = [get_eth_address_with_key()[0] for _ in range(2)]
        threshold = len(owners) - 1
        gas_price = self.gas_price

        safe_creation_tx = SafeCreationTx(w3=w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.safe_contract_V0_0_1_address,
                                          gas_price=gas_price,
                                          funder=funder_account.address)

        user_external_account = Account.create()
        # Send some ether to that account
        safe_balance = w3.toWei(0.01, 'ether')
        self.send_tx({
            'to': user_external_account.address,
            'value': safe_balance * 2
        }, funder_account)

        logger.info("Send %d ether to safe %s", w3.fromWei(safe_balance, 'ether'), safe_creation_tx.safe_address)
        self.send_tx({
            'to': safe_creation_tx.safe_address,
            'value': safe_balance
        }, user_external_account)
        self.assertEqual(w3.eth.getBalance(safe_creation_tx.safe_address), safe_balance)

        logger.info("Send %d gwei to deployer %s", w3.fromWei(safe_creation_tx.payment_ether, 'gwei'),
                    safe_creation_tx.deployer_address)
        self.send_tx({
            'to': safe_creation_tx.deployer_address,
            'value': safe_creation_tx.payment_ether
        }, funder_account)

        logger.info("Create proxy contract with address %s", safe_creation_tx.safe_address)

        funder_balance = w3.eth.getBalance(funder_account.address)

        # This tx will create the Safe Proxy and return ether to the funder
        tx_hash = w3.eth.sendRawTransaction(safe_creation_tx.tx_raw)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.contractAddress, safe_creation_tx.safe_address)

        self.assertEqual(w3.eth.getBalance(funder_account.address),
                         funder_balance + safe_creation_tx.payment)

        logger.info("Deployer account has still %d gwei left (will be lost)",
                    w3.fromWei(w3.eth.getBalance(safe_creation_tx.deployer_address), 'gwei'))

        deployed_safe_proxy_contract = get_safe_contract(w3, tx_receipt.contractAddress)

        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)

    def test_safe_creation_tx_builder_with_token_payment(self):
        logger.info("Test Safe Proxy creation With Gas Payment".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3

        s = generate_valid_s()

        erc20_deployer = Account.create()
        funder_account = self.ethereum_test_account

        # Send something to the erc20 deployer
        self.send_tx({
            'to': erc20_deployer.address,
            'value': w3.toWei(1, 'ether')
        }, funder_account)

        funder = funder_account.address
        owners = [get_eth_address_with_key()[0] for _ in range(2)]
        threshold = len(owners) - 1
        gas_price = self.gas_price
        token_amount = int(1e18)
        erc20_contract = self.deploy_example_erc20(token_amount, erc20_deployer.address)
        self.assertEqual(erc20_contract.functions.balanceOf(erc20_deployer.address).call(), token_amount)

        safe_creation_tx = SafeCreationTx(w3=w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.safe_contract_V0_0_1_address,
                                          gas_price=gas_price,
                                          payment_token=erc20_contract.address,
                                          funder=funder)

        # In this test we will pretend that ether value = token value, so we send tokens as ether payment
        payment = safe_creation_tx.payment
        deployer_address = safe_creation_tx.deployer_address
        safe_address = safe_creation_tx.safe_address
        logger.info("Send %d tokens to safe %s", payment, safe_address)
        self.send_tx(erc20_contract.functions.transfer(safe_address,
                                                       payment).buildTransaction({'from': erc20_deployer.address}),
                     erc20_deployer)
        self.assertEqual(erc20_contract.functions.balanceOf(safe_address).call(), payment)

        logger.info("Send %d ether to deployer %s", w3.fromWei(payment, 'ether'), deployer_address)
        self.send_tx({
            'to': safe_creation_tx.deployer_address,
            'value': safe_creation_tx.payment
        }, funder_account)

        logger.info("Create proxy contract with address %s", safe_creation_tx.safe_address)
        funder_balance = w3.eth.getBalance(funder)

        # This tx will create the Safe Proxy and return tokens to the funder
        tx_hash = w3.eth.sendRawTransaction(safe_creation_tx.tx_raw)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.contractAddress, safe_address)
        self.assertEqual(w3.eth.getBalance(funder), funder_balance)
        self.assertEqual(erc20_contract.functions.balanceOf(funder).call(), payment)
        self.assertEqual(erc20_contract.functions.balanceOf(safe_address).call(), 0)

        logger.info("Deployer account has still %d gwei left (will be lost)",
                    w3.fromWei(w3.eth.getBalance(safe_creation_tx.deployer_address), 'gwei'))

        deployed_safe_proxy_contract = get_safe_contract(w3, tx_receipt.contractAddress)

        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)

        # Payment should be <= when payment_token_eth_value is 1.0
        # Funder will already have tokens so no storage need to be paid)
        safe_creation_tx_2 = SafeCreationTx(w3=w3,
                                            owners=owners,
                                            threshold=threshold,
                                            signature_s=s,
                                            master_copy=self.safe_contract_V0_0_1_address,
                                            gas_price=gas_price,
                                            payment_token=erc20_contract.address,
                                            payment_token_eth_value=1.0,
                                            funder=funder)
        self.assertLessEqual(safe_creation_tx_2.payment, safe_creation_tx.payment)

        # Now payment should be equal when payment_token_eth_value is 1.0
        safe_creation_tx_3 = SafeCreationTx(w3=w3,
                                            owners=owners,
                                            threshold=threshold,
                                            signature_s=s,
                                            master_copy=self.safe_contract_V0_0_1_address,
                                            gas_price=gas_price,
                                            payment_token=erc20_contract.address,
                                            payment_token_eth_value=1.0,
                                            funder=funder)
        self.assertEqual(safe_creation_tx_3.payment, safe_creation_tx_2.payment)

        # Check that payment is less when payment_token_eth_value is set(token value > ether)
        safe_creation_tx_4 = SafeCreationTx(w3=w3,
                                            owners=owners,
                                            threshold=threshold,
                                            signature_s=s,
                                            master_copy=self.safe_contract_V0_0_1_address,
                                            gas_price=gas_price,
                                            payment_token=erc20_contract.address,
                                            payment_token_eth_value=1.1,
                                            funder=funder)
        self.assertLess(safe_creation_tx_4.payment, safe_creation_tx.payment)

        # Check that payment is more when payment_token_eth_value is set(token value < ether)
        safe_creation_tx_5 = SafeCreationTx(w3=w3,
                                            owners=owners,
                                            threshold=threshold,
                                            signature_s=s,
                                            master_copy=self.safe_contract_V0_0_1_address,
                                            gas_price=gas_price,
                                            payment_token=erc20_contract.address,
                                            payment_token_eth_value=0.1,
                                            funder=funder)
        self.assertGreater(safe_creation_tx_5.payment, safe_creation_tx.payment)

    def test_safe_creation_tx_builder_with_fixed_cost(self):
        logger.info("Test Safe Proxy creation With Fixed Cost".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3

        s = generate_valid_s()

        funder_account = self.ethereum_test_account
        owners = [get_eth_address_with_key()[0] for _ in range(2)]
        threshold = len(owners) - 1
        gas_price = self.gas_price
        fixed_creation_cost = 123  # Wei

        safe_creation_tx = SafeCreationTx(w3=w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.safe_contract_V0_0_1_address,
                                          gas_price=gas_price,
                                          payment_token=None,
                                          funder=funder_account.address,
                                          fixed_creation_cost=fixed_creation_cost)

        self.assertEqual(safe_creation_tx.payment, fixed_creation_cost)
        self.assertEqual(safe_creation_tx.payment_ether, safe_creation_tx.gas * safe_creation_tx.gas_price)

        deployer_address = safe_creation_tx.deployer_address
        safe_address = safe_creation_tx.safe_address
        safe_balance = w3.toWei(0.01, 'ether')
        logger.info("Send %d ether to safe %s", w3.fromWei(safe_balance, 'ether'), safe_address)
        self.send_tx({
            'to': safe_address,
            'value': safe_balance
        }, funder_account)
        self.assertEqual(w3.eth.getBalance(safe_address), safe_balance)

        logger.info("Send %d ether to deployer %s", w3.fromWei(safe_creation_tx.payment_ether, 'ether'),
                    deployer_address)
        self.send_tx({
            'to': deployer_address,
            'value': safe_creation_tx.payment_ether
        }, funder_account)

        logger.info("Create proxy contract with address %s", safe_creation_tx.safe_address)

        funder_balance = w3.eth.getBalance(funder_account.address)

        # This tx will create the Safe Proxy and return tokens to the funder
        tx_hash = w3.eth.sendRawTransaction(safe_creation_tx.tx_raw)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(tx_receipt.contractAddress, safe_address)
        self.assertEqual(w3.eth.getBalance(safe_address), safe_balance - fixed_creation_cost)
        self.assertLess(w3.eth.getBalance(deployer_address), safe_creation_tx.payment_ether)
        self.assertEqual(w3.eth.getBalance(funder_account.address), funder_balance + safe_creation_tx.payment)

        logger.info("Deployer account has still %d gwei left (will be lost)",
                    w3.fromWei(w3.eth.getBalance(safe_creation_tx.deployer_address), 'gwei'))

        deployed_safe_proxy_contract = get_safe_contract(w3, safe_address)

        self.assertEqual(deployed_safe_proxy_contract.functions.getThreshold().call(), threshold)
        self.assertEqual(deployed_safe_proxy_contract.functions.getOwners().call(), owners)

    def test_safe_gas_with_multiple_owners(self):
        logger.info("Test Safe Proxy creation gas with multiple owners".center(LOG_TITLE_WIDTH, '-'))
        w3 = self.w3
        funder_account = self.ethereum_test_account
        number_of_accounts = 10
        for i in range(2, number_of_accounts):
            s = generate_valid_s()
            owners = [get_eth_address_with_key()[0] for _ in range(i + 1)]
            threshold = len(owners)
            gas_price = w3.toWei(15, 'gwei')

            safe_creation_tx = SafeCreationTx(w3=w3,
                                              owners=owners,
                                              threshold=threshold,
                                              signature_s=s,
                                              master_copy=self.safe_contract_V0_0_1_address,
                                              gas_price=gas_price,
                                              funder=None)

            self.send_tx({
                'to': safe_creation_tx.deployer_address,
                'value': safe_creation_tx.payment
            }, funder_account)
            tx_hash = w3.eth.sendRawTransaction(safe_creation_tx.tx_raw)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            self.assertEqual(tx_receipt.contractAddress, safe_creation_tx.safe_address)

            logger.info("Number of owners: %d - Gas estimated %d - Gas Used %d - Difference %d",
                        len(owners),
                        safe_creation_tx.gas,
                        tx_receipt.gasUsed,
                        safe_creation_tx.gas - tx_receipt.gasUsed)
