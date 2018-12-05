from logging import getLogger

from django_eth.constants import NULL_ADDRESS
from ethereum.utils import (check_checksum, checksum_encode, ecrecover_to_pub,
                            privtoaddr, sha3)
from hexbytes import HexBytes
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from web3.utils.threads import Timeout

from .contracts import get_erc20_contract

logger = getLogger(__name__)


class EthereumServiceProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            from django.conf import settings
            cls.instance = EthereumService(settings.ETHEREUM_NODE_URL,
                                           settings.SAFE_FUNDER_MAX_ETH,
                                           settings.SAFE_FUNDER_PRIVATE_KEY)
        return cls.instance


class EthereumService:
    NULL_ADDRESS = NULL_ADDRESS

    def __init__(self, ethereum_node_url, max_eth_to_send=0.1, funder_private_key=None):
        self.ethereum_node_url = ethereum_node_url
        self.max_eth_to_send = max_eth_to_send
        self.funder_private_key = funder_private_key
        self.w3 = Web3(HTTPProvider(self.ethereum_node_url))
        try:
            if self.w3.net.chainId != 1:
                self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
            # For tests using dummy connections (like IPC)
        except (ConnectionError, FileNotFoundError):
            self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    def get_nonce_for_account(self, address, block_identifier=None):
        return self.w3.eth.getTransactionCount(address, block_identifier=block_identifier)

    @property
    def current_block_number(self):
        return self.w3.eth.blockNumber

    @staticmethod
    def estimate_data_gas(data: bytes):
        if isinstance(data, str):
            data = HexBytes(data)

        gas = 0
        for byte in data:
            if not byte:
                gas += 4  # Byte 0 -> 4 Gas
            else:
                gas += 68  # Any other byte -> 68 Gas
        return gas

    def get_balance(self, address: str, block_identifier=None):
        return self.w3.eth.getBalance(address, block_identifier)

    def get_erc20_balance(self, address: str, erc20_address: str):
        return get_erc20_contract(self.w3, erc20_address).functions.balanceOf(address).call()

    def get_transaction(self, tx_hash):
        return self.w3.eth.getTransaction(tx_hash)

    def get_transaction_receipt(self, tx_hash, timeout=None):
        if not timeout:
            return self.w3.eth.getTransactionReceipt(tx_hash)
        else:
            try:
                tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)
                # Parity returns tx_receipt even is tx is still pending, so we check `blockNumber` is not None
                return None if tx_receipt['blockNumber'] is None else tx_receipt
            except Timeout:
                return None

    def get_block(self, block_number, full_transactions=False):
        return self.w3.eth.getBlock(block_number, full_transactions=full_transactions)

    def send_raw_transaction(self, raw_transaction):
        return self.w3.eth.sendRawTransaction(bytes(raw_transaction))

    def send_eth_to(self, to: str, gas_price: int, value: int, gas: int=22000, block_identifier=None) -> bytes:
        """
        Send ether using configured account
        :param to: to
        :param gas_price: gas_price
        :param value: value(wei)
        :param gas: gas, defaults to 22000
        :return: tx_hash
        """

        assert check_checksum(to)
        assert value < self.w3.toWei(self.max_eth_to_send, 'ether')

        private_key = self.funder_private_key

        if private_key:
            ethereum_account = self.private_key_to_address(private_key)
            tx = {
                    'to': to,
                    'value': value,
                    'gas': gas,
                    'gasPrice': gas_price,
                    'nonce': self.get_nonce_for_account(ethereum_account, block_identifier=block_identifier),
                }

            signed_tx = self.w3.eth.account.signTransaction(tx, private_key=private_key)
            logger.debug('Sending %d wei from %s to %s', value, ethereum_account, to)
            return self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        elif self.w3.eth.accounts:
            ethereum_account = self.w3.eth.accounts[0]
            tx = {
                    'from': ethereum_account,
                    'to': to,
                    'value': value,
                    'gas': gas,
                    'gasPrice': gas_price,
                    'nonce': self.get_nonce_for_account(ethereum_account, block_identifier=block_identifier),
                }
            logger.debug('Sending %d wei from %s to %s', value, ethereum_account, to)
            return self.w3.eth.sendTransaction(tx)
        else:
            logger.error('No ethereum account configured')
            raise ValueError("Ethereum account was not configured or unlocked in the node")

    def check_tx_with_confirmations(self, tx_hash: str, confirmations: int) -> bool:
        """
        Check tx hash and make sure it has the confirmations required
        :param w3: Web3 instance
        :param tx_hash: Hash of the tx
        :param confirmations: Minimum number of confirmations required
        :return: True if tx was mined with the number of confirmations required, False otherwise
        """
        tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        if not tx_receipt or tx_receipt['blockNumber'] is None:
            # If tx_receipt exists but blockNumber is None, tx is still pending (just Parity)
            return False
        else:
            return (self.w3.eth.blockNumber - tx_receipt['blockNumber']) >= confirmations

    @staticmethod
    def private_key_to_address(private_key):
        return checksum_encode(privtoaddr(private_key))

    @staticmethod
    def get_signing_address(hash, v, r, s) -> str:
        """
        :return: checksum encoded address starting by 0x, for example `0x568c93675A8dEb121700A6FAdDdfE7DFAb66Ae4A`
        :rtype: str
        """
        encoded_64_address = ecrecover_to_pub(hash, v, r, s)
        address_bytes = sha3(encoded_64_address)[-20:]
        return checksum_encode(address_bytes)
