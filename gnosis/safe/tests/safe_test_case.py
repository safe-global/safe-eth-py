import logging
from typing import List

from django_eth.constants import NULL_ADDRESS

from ..contracts import get_safe_contract
from ..ethereum_service import EthereumService
from ..safe_creation_tx import SafeCreationTx
from ..safe_service import SafeService, SafeServiceProvider
from .factories import deploy_safe, generate_safe, generate_valid_s

logger = logging.getLogger(__name__)


class TestCaseWithSafeContractMixin:
    # Ganache fixed seed keys (run ganache with -d)
    FUNDER_PRIVATE_KEY = '4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
    SENDER_PRIVATE_KEY = '6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'
    SERVER_URL = 'http://localhost:8545'
    GAS_PRICE = 1

    @classmethod
    def prepare_safe_tests(cls):
        cls.ethereum_service = EthereumService(cls.SERVER_URL,
                                               funder_private_key=cls.FUNDER_PRIVATE_KEY)
        cls.safe_service = SafeService(cls.ethereum_service,
                                       master_copy_address=None,
                                       valid_master_copy_addresses=[],
                                       tx_sender_private_key=cls.SENDER_PRIVATE_KEY,
                                       funder_private_key=cls.FUNDER_PRIVATE_KEY)
        SafeServiceProvider.instance = cls.safe_service
        cls.w3 = cls.ethereum_service.w3

        cls.safe_deployer = cls.w3.eth.accounts[0]
        cls.safe_contract_address = cls.safe_service.deploy_master_contract(deployer_account=cls.safe_deployer)
        cls.safe_service.master_copy_address = cls.safe_contract_address
        cls.safe_service.valid_master_copy_addresses = [cls.safe_contract_address]
        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)

    def deploy_test_safe(self, max_owners=3, threshold: int=None, owners: List[str]=None, initial_funding_wei: int=None):
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
