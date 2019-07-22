from logging import getLogger

from eth_account.signers.local import LocalAccount
from web3 import Web3

from gnosis.eth import EthereumClient
from gnosis.eth.contracts import get_multi_send_contract
from gnosis.eth.ethereum_client import EthereumTxSent

logger = getLogger(__name__)


class MultiSend:
    def __init__(self, address: str, ethereum_client: EthereumClient):
        assert Web3.isChecksumAddress(address), \
            '%s proxy factory address not valid' % address

        self.address = address
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    @staticmethod
    def deploy_contract(ethereum_client: EthereumClient, deployer_account: LocalAccount) -> EthereumTxSent:
        """
        Deploy proxy factory contract
        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        contract = get_multi_send_contract(ethereum_client.w3)
        tx = contract.constructor().buildTransaction({'from': deployer_account.address})

        tx_hash = ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.privateKey)
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt.status
        contract_address = tx_receipt.contractAddress
        logger.info("Deployed and initialized Proxy Factory Contract=%s by %s", contract_address,
                    deployer_account.address)
        return EthereumTxSent(tx_hash, tx, contract_address)

    def get_contract(self):
        return get_multi_send_contract(self.ethereum_client.w3, self.address)
