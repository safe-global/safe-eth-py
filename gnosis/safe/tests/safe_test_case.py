import logging
from typing import List

from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.ethereum_service import EthereumServiceProvider

from ..safe_service import SafeServiceProvider
from .factories import deploy_safe, generate_safe

logger = logging.getLogger(__name__)


class SafeTestCaseMixin:
    @classmethod
    def prepare_safe_tests(cls):
        cls.safe_service = SafeServiceProvider()
        cls.ethereum_service = EthereumServiceProvider()
        cls.w3 = cls.ethereum_service.w3

        cls.safe_deployer = cls.w3.eth.accounts[0]
        cls.safe_contract_address = cls.safe_service.deploy_master_contract(deployer_account=cls.safe_deployer)
        cls.safe_service.master_copy_address = cls.safe_contract_address
        cls.safe_service.valid_master_copy_addresses = [cls.safe_contract_address]
        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)

    def deploy_test_safe(self, max_owners=3, threshold: int = None, owners: List[str] = None,
                         initial_funding_wei: int = None):
        initial_funding_wei = initial_funding_wei if initial_funding_wei else self.w3.toWei(0.1, 'ether')
        owners = owners if owners else self.w3.eth.accounts[-max_owners:]
        threshold = threshold if threshold else len(owners) - 1
        funder = self.w3.eth.accounts[0]

        safe_creation_tx = generate_safe(self.safe_service,
                                         owners=owners,
                                         threshold=threshold)
        safe_address = deploy_safe(self.w3,
                                   safe_creation_tx,
                                   funder=self.w3.eth.accounts[0],
                                   initial_funding_wei=initial_funding_wei)

        safe_instance = get_safe_contract(self.w3, safe_address)

        self.assertEqual(safe_instance.functions.getThreshold().call(), threshold)
        self.assertEqual(safe_instance.functions.getOwners().call(), owners)

        return safe_address, safe_instance, owners, funder, initial_funding_wei, threshold
