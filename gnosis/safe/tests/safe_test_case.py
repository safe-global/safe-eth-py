import logging

from ..contracts import get_safe_contract
from ..ethereum_service import EthereumService
from ..safe_service import SafeService

logger = logging.getLogger(__name__)


class TestCaseWithSafeContractMixin:
    # Ganache fixed seed keys
    FUNDER_PRIVATE_KEY = '4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
    SENDER_PRIVATE_KEY = '6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'
    SERVER_URL = 'http://localhost:8545'

    @classmethod
    def prepare_safe_tests(cls):
        cls.ethereum_service = EthereumService(cls.SERVER_URL,
                                               funder_private_key=cls.FUNDER_PRIVATE_KEY)
        cls.safe_service = SafeService(cls.ethereum_service,
                                       master_copy_address=None,
                                       valid_master_copy_addresses=[],
                                       tx_sender_private_key=cls.SENDER_PRIVATE_KEY,
                                       funder_private_key=cls.FUNDER_PRIVATE_KEY)
        cls.w3 = cls.ethereum_service.w3

        cls.safe_deployer = cls.w3.eth.accounts[0]
        cls.safe_contract_address = cls.safe_service.deploy_master_contract(deployer_account=
                                                                                     cls.safe_deployer)
        cls.safe_service.master_copy_address = cls.safe_contract_address
        cls.safe_service.valid_master_copy_addresses = [cls.safe_contract_address]
        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)
