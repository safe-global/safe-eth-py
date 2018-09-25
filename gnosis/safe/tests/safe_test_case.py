import logging

from django_eth.constants import NULL_ADDRESS

from ..contracts import get_safe_contract
from ..ethereum_service import EthereumService
from ..safe_creation_tx import SafeCreationTx
from ..safe_service import SafeService
from .factories import generate_valid_s

logger = logging.getLogger(__name__)


class TestCaseWithSafeContractMixin:
    # Ganache fixed seed keys
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
        cls.w3 = cls.ethereum_service.w3

        cls.safe_deployer = cls.w3.eth.accounts[0]
        cls.safe_contract_address = cls.safe_service.deploy_master_contract(deployer_account=
                                                                                     cls.safe_deployer)
        cls.safe_service.master_copy_address = cls.safe_contract_address
        cls.safe_service.valid_master_copy_addresses = [cls.safe_contract_address]
        cls.safe_contract = get_safe_contract(cls.w3, cls.safe_contract_address)

    def deploy_safe(self, max_owners=3):
        fund_amount = 10000000000000000000  # 1 ETH
        # Create Safe on blockchain
        s = generate_valid_s()
        funder = self.w3.eth.accounts[0]
        owners = self.w3.eth.accounts[0:max_owners]
        threshold = len(owners) - 1
        gas_price = self.GAS_PRICE

        safe_builder = SafeCreationTx(w3=self.w3,
                                      owners=owners,
                                      threshold=threshold,
                                      signature_s=s,
                                      master_copy=self.safe_contract_address,
                                      gas_price=gas_price,
                                      funder=NULL_ADDRESS)

        tx_hash = self.w3.eth.sendTransaction({
            'from': funder,
            'to': safe_builder.deployer_address,
            'value': safe_builder.payment
        })

        self.assertIsNotNone(tx_hash)

        logger.info("Create proxy contract with address %s", safe_builder.safe_address)

        tx_hash = self.w3.eth.sendRawTransaction(safe_builder.raw_tx)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        safe_address = tx_receipt.contractAddress
        safe_instance = get_safe_contract(self.w3, safe_address)

        self.assertEqual(safe_instance.functions.getThreshold().call(), threshold)
        self.assertEqual(safe_instance.functions.getOwners().call(), owners)

        tx_hash = self.w3.eth.sendTransaction({
            'from': funder,
            'to': safe_address,
            'value': fund_amount
        })

        return safe_address, safe_instance, owners, funder, fund_amount, threshold
