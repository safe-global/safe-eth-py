import logging
from typing import List

from gnosis.eth.contracts import get_safe_contract
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin
from gnosis.eth.utils import get_eth_address_with_key

from ..safe_creation_tx import SafeCreationTx
from ..safe_service import SafeServiceProvider
from .utils import deploy_safe, generate_safe

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
        cls.safe_service.valid_master_copy_addresses = [cls.safe_contract_address]
        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)

    def build_test_safe(self, number_owners: int = 3, threshold: int = None,
                        owners: List[str] = None)-> SafeCreationTx:
        owners = owners if owners else [get_eth_address_with_key()[0] for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners) - 1

        safe_creation_tx = generate_safe(self.safe_service,
                                         owners=owners,
                                         threshold=threshold)
        return safe_creation_tx

    def deploy_test_safe(self, number_owners: int = 3, threshold: int = None, owners: List[str] = None,
                         initial_funding_wei: int = 0) -> SafeCreationTx:
        owners = owners if owners else [get_eth_address_with_key()[0] for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners) - 1
        safe_creation_tx = self.build_test_safe(threshold=threshold, owners=owners)
        funder_account = self.ethereum_test_account
        safe_address = deploy_safe(self.w3,
                                   safe_creation_tx,
                                   funder_account.address,
                                   funder_account=funder_account,
                                   initial_funding_wei=initial_funding_wei)

        safe_instance = get_safe_contract(self.w3, safe_address)

        self.assertEqual(safe_instance.functions.getThreshold().call(), threshold)
        self.assertEqual(safe_instance.functions.getOwners().call(), owners)
        self.assertEqual(safe_address, safe_creation_tx.safe_address)

        return safe_creation_tx
