import logging
from typing import List

from django.conf import settings

from eth_account import Account

from gnosis.eth.contracts import (get_old_safe_contract,
                                  get_proxy_factory_contract,
                                  get_safe_contract)
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin
from gnosis.eth.utils import get_eth_address_with_key
from gnosis.safe import Safe
from gnosis.safe.proxy_factory import ProxyFactory
from gnosis.safe.safe_create2_tx import SafeCreate2Tx

from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)


contract_addresses = {
    'safe': None,
    'old_safe': None,
    'proxy_factory': None,
}


class SafeTestCaseMixin(EthereumTestCaseMixin):
    @classmethod
    def prepare_tests(cls):
        super().prepare_tests()

        for key, value in contract_addresses.items():
            if not value:
                if key == 'safe':
                    fn = Safe.deploy_master_contract
                elif key == 'old_safe':
                    fn = Safe.deploy_old_master_contract
                elif key == 'proxy_factory':
                    fn = ProxyFactory.deploy_proxy_factory_contract
                contract_addresses[key] = fn(cls.ethereum_client, cls.ethereum_test_account).contract_address

        settings.SAFE_CONTRACT_ADDRESS = contract_addresses['safe']
        settings.SAFE_OLD_CONTRACT_ADDRESS = contract_addresses['old_safe']
        settings.SAFE_PROXY_FACTORY_ADDRESS = contract_addresses['proxy_factory']
        settings.SAFE_VALID_CONTRACT_ADDRESSES = {settings.SAFE_CONTRACT_ADDRESS, settings.SAFE_OLD_CONTRACT_ADDRESS}
        cls.safe_contract_address = contract_addresses['safe']
        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)
        cls.safe_old_contract_address = contract_addresses['old_safe']
        cls.safe_old_contract = get_old_safe_contract(cls.w3, cls.safe_old_contract_address)
        cls.proxy_factory_contract_address = contract_addresses['proxy_factory']
        cls.proxy_factory_contract = get_proxy_factory_contract(cls.w3, cls.proxy_factory_contract_address)
        cls.proxy_factory = ProxyFactory(cls.proxy_factory_contract_address, cls.ethereum_client)

    def build_test_safe(self, number_owners: int = 3, threshold: int = None,
                        owners: List[str] = None) -> SafeCreate2Tx:
        salt_nonce = generate_salt_nonce()
        owners = owners if owners else [Account.create().address for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners) - 1

        gas_price = self.ethereum_client.w3.eth.gasPrice
        return Safe.build_safe_create2_tx(self.ethereum_client, self.safe_contract_address,
                                          self.proxy_factory_contract_address, salt_nonce, owners, threshold,
                                          gas_price=gas_price, payment_token=None, fixed_creation_cost=0)

    def deploy_test_safe(self, number_owners: int = 3, threshold: int = None, owners: List[str] = None,
                         initial_funding_wei: int = 0) -> SafeCreate2Tx:
        owners = owners if owners else [get_eth_address_with_key()[0] for _ in range(number_owners)]
        if not threshold:
            threshold = len(owners) - 1 if len(owners) > 1 else 1
        safe_creation_tx = self.build_test_safe(threshold=threshold, owners=owners)
        funder_account = self.ethereum_test_account

        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(funder_account,
                                                                               self.safe_contract_address,
                                                                               safe_creation_tx.safe_setup_data,
                                                                               safe_creation_tx.salt_nonce)

        safe_address = ethereum_tx_sent.contract_address
        if initial_funding_wei:
            self.send_ether(safe_address, initial_funding_wei)

        safe_instance = get_safe_contract(self.w3, safe_address)

        self.assertEqual(safe_instance.functions.getThreshold().call(), threshold)
        self.assertEqual(safe_instance.functions.getOwners().call(), owners)
        self.assertEqual(safe_address, safe_creation_tx.safe_address)

        return safe_creation_tx
