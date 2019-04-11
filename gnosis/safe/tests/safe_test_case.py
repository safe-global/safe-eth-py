import logging
from typing import List

from eth_account import Account

from gnosis.eth.contracts import (get_old_safe_contract,
                                  get_proxy_factory_contract,
                                  get_safe_contract)
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin
from gnosis.eth.utils import get_eth_address_with_key
from gnosis.safe.safe_create2_tx import SafeCreate2Tx

from ..safe_creation_tx import SafeCreationTx
from ..safe_service import SafeServiceProvider
from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)


class SafeTestCaseMixin(EthereumTestCaseMixin):
    @classmethod
    def prepare_tests(cls):
        super().prepare_tests()
        cls.safe_service = SafeServiceProvider()

        # If safe master copy not deployed we do
        cls.safe_contract_address = cls.safe_service.master_copy_address
        if not cls.w3.eth.getCode(cls.safe_service.master_copy_address):
            cls.safe_contract_address = cls.safe_service.deploy_master_contract(deployer_private_key=
                                                                                cls.ethereum_test_account.privateKey)
            cls.safe_service.master_copy_address = cls.safe_contract_address

        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)

        cls.safe_old_contract_address = cls.safe_service.master_copy_old_address
        if not cls.w3.eth.getCode(cls.safe_old_contract_address):
            cls.safe_old_contract_address = cls.safe_service.deploy_old_master_contract(deployer_private_key=
                                                                                        cls.ethereum_test_account.privateKey)
            cls.safe_service.master_copy_old_address = cls.safe_old_contract_address
        cls.safe_old_contract = get_old_safe_contract(cls.w3, cls.safe_old_contract_address)

        cls.proxy_factory_contract_address = cls.safe_service.proxy_factory_address
        if not cls.w3.eth.getCode(cls.safe_service.proxy_factory_address):
            cls.proxy_factory_contract_address = cls.safe_service.deploy_proxy_factory_contract(deployer_private_key=
                                                                                                cls.ethereum_test_account.privateKey)
            cls.safe_service.proxy_factory_address = cls.proxy_factory_contract_address
        cls.proxy_factory_contract = get_proxy_factory_contract(cls.w3, cls.proxy_factory_contract_address)

    def build_test_safe(self, number_owners: int = 3, threshold: int = None,
                        owners: List[str] = None)-> SafeCreate2Tx:
        salt_nonce = generate_salt_nonce()
        owners = owners if owners else [Account.create().address for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners) - 1

        gas_price = self.ethereum_client.w3.eth.gasPrice
        return self.safe_service.build_safe_create2_tx(salt_nonce, owners, threshold, gas_price=gas_price,
                                                       payment_token=None,
                                                       fixed_creation_cost=0)

    def deploy_test_safe(self, number_owners: int = 3, threshold: int = None, owners: List[str] = None,
                         initial_funding_wei: int = 0) -> SafeCreate2Tx:
        owners = owners if owners else [get_eth_address_with_key()[0] for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners) - 1
        safe_creation_tx = self.build_test_safe(threshold=threshold, owners=owners)
        funder_account = self.ethereum_test_account

        (tx_hash, _,
         safe_address) = self.safe_service.deploy_proxy_contract_with_nonce(safe_creation_tx.salt_nonce,
                                                                            safe_creation_tx.safe_setup_data,
                                                                            safe_creation_tx.gas,
                                                                            safe_creation_tx.gas_price,
                                                                            deployer_private_key=funder_account.privateKey)

        if initial_funding_wei:
            self.send_ether(safe_address, initial_funding_wei)

        safe_instance = get_safe_contract(self.w3, safe_address)

        self.assertEqual(safe_instance.functions.getThreshold().call(), threshold)
        self.assertEqual(safe_instance.functions.getOwners().call(), owners)
        self.assertEqual(safe_address, safe_creation_tx.safe_address)

        return safe_creation_tx
