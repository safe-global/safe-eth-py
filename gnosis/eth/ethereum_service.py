from functools import wraps
from logging import getLogger
from typing import Dict, List, Union, NamedTuple

import requests
from ethereum.utils import (check_checksum, checksum_encode, ecrecover_to_pub,
                            privtoaddr, sha3)
from hexbytes import HexBytes
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from web3.providers import AutoProvider, BaseProvider
from web3.utils.threads import Timeout

from gnosis.eth.constants import NULL_ADDRESS

from .contracts import get_erc20_contract, get_example_erc20_contract

logger = getLogger(__name__)


class TransactionAlreadyImported(ValueError):
    pass


class ReplacementTransactionUnderpriced(ValueError):
    pass


class FromAddressNotFound(ValueError):
    pass


class InvalidNonce(ValueError):
    pass


class InsufficientFunds(ValueError):
    pass


class EtherLimitExceeded(ValueError):
    pass


class SenderAccountNotFoundInNode(ValueError):
    pass


def tx_with_exception_handling(func):
    error_with_exception: Dict[str, Exception] = {
        'Transaction with the same hash was already imported': TransactionAlreadyImported,
        'replacement transaction underpriced': ReplacementTransactionUnderpriced,
        'from not found': FromAddressNotFound,
        'correct nonce': InvalidNonce,
        'insufficient funds': InsufficientFunds,
        "doesn't have enough funds": InsufficientFunds,
        'sender account not recognized': SenderAccountNotFoundInNode,
    }

    @wraps(func)
    def with_exception_handling(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            str_exc = str(exc).lower()
            for reason, custom_exception in error_with_exception.items():
                if reason.lower() in str_exc:
                    raise custom_exception(str(exc)) from exc
            raise exc
    return with_exception_handling


class Erc20_Info(NamedTuple):
    name: str
    symbol: str
    decimals: int


class EthereumServiceProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            from django.conf import settings
            cls.instance = EthereumService(settings.ETHEREUM_NODE_URL)
        return cls.instance


class Erc20Manager:
    def __init__(self, ethereum_service, slow_provider_timeout: int = 30):
        self.ethereum_service = ethereum_service
        self.w3 = ethereum_service.w3
        self.slow_w3 = Web3(self.get_slow_provider(self.w3.providers[0],
                                                   timeout=slow_provider_timeout))

    @staticmethod
    def get_slow_provider(provider: BaseProvider, timeout: int):
        """
        Get web3 provider for slow queries. Default `HTTPProvider` timeouts after 10 seconds
        :param provider: Configured Web3 provider
        :param timeout: Timeout to configure for internal requests (default is 10)
        :return: A new web3 provider with the `slow_provider_timeout`
        """
        if isinstance(provider, AutoProvider):
            return HTTPProvider(endpoint_uri='http://localhost:8545',
                                request_kwargs={'timeout': timeout})
        elif isinstance(provider, HTTPProvider):
            return HTTPProvider(endpoint_uri=provider.endpoint_uri,
                                request_kwargs={'timeout': timeout})
        else:
            return provider

    def get_balance(self, address: str, erc20_address: str) -> int:
        """
        Get balance of address for `erc20_address`
        :param address: owner address
        :param erc20_address: erc20 token address
        :return: balance
        """
        return get_erc20_contract(self.w3, erc20_address).functions.balanceOf(address).call()

    def get_info(self, erc20_address: str) -> Erc20_Info:
        """
        Get erc20 information (`name`, `symbol` and `decimals`)
        :param erc20_address:
        :return: Erc20_Info
        """
        # We use the `example erc20` as the `erc20 interface` doesn't have `name`, `symbol` nor `decimals`
        erc20 = get_example_erc20_contract(self.w3, erc20_address)
        name = erc20.functions.name().call()
        symbol = erc20.functions.symbol().call()
        decimals = erc20.functions.decimals().call()
        return Erc20_Info(name, symbol, decimals)

    def get_transfer_history(self, from_block: int, to_block: int = 0,
                             from_address: str = '', to_address: str = '',
                             token_address: str = '') -> List[Dict[str, any]]:
        """
        Get events for erc20 transfers. At least one of `from_address`, `to_address` or `token_address` must be
        defined
        An example of event:
        {
            "args": {
                "from": "0x1Ce67Ea59377A163D47DFFc9BaAB99423BE6EcF1",
                "to": "0xaE9E15896fd32E59C7d89ce7a95a9352D6ebD70E",
                "value": 15000000000000000
            },
            "event": "Transfer",
            "logIndex": 42,
            "transactionIndex": 60,
            "transactionHash": "0x71d6d83fef3347bad848e83dfa0ab28296e2953de946ee152ea81c6dfb42d2b3",
            "address": "0xfecA834E7da9D437645b474450688DA9327112a5",
            "blockHash": "0x054de9a496fc7d10303068cbc7ee3e25181a3b26640497859a5e49f0342e7db2",
            "blockNumber": 7265022
        }
        :param from_block: Block to start querying from
        :param to_block: Block to stop querying from (0 would be last block)
        :param from_address: Address sending the erc20 transfer
        :param to_address: Address receiving the erc20 transfer
        :param token_address: Address of the token
        :return: List of events
        :throws: ReadTimeout
        """
        assert from_address or to_address or token_address, 'At least one parameter must be provided'

        erc20 = get_erc20_contract(self.w3)

        argument_filters = {}
        if from_address:
            argument_filters['from'] = from_address
        if to_address:
            argument_filters['to'] = to_address

        return erc20.events.Transfer.createFilter(fromBlock=from_block,
                                                  toBlock=to_block if to_block else None,
                                                  address=token_address if token_address else None,
                                                  argument_filters=argument_filters).get_all_entries()

    def send_tokens(self, to: str, amount: int, erc20_address: str):
        """
        Send tokens to address
        :param to:
        :param amount:
        :param erc20_address:
        :return:
        """


class EthereumService:
    """
    Manage ethereum operations. Uses web3 for the most part, but some other stuff is implemented from scratch.
    Note: If you want to use `pending` state with `Parity`, it must be run with `--pruning=archive` or `--force-sealing`
    """
    NULL_ADDRESS = NULL_ADDRESS

    def __init__(self, ethereum_node_url: str):
        self.ethereum_node_url: str = ethereum_node_url
        self.w3: Web3 = Web3(HTTPProvider(self.ethereum_node_url))
        self.erc20: Erc20Manager = Erc20Manager(self)
        try:
            if int(self.w3.net.version) != 1:
                self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
            # For tests using dummy connections (like IPC)
        except (ConnectionError, FileNotFoundError):
            self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    def get_nonce_for_account(self, address, block_identifier=None):
        return self.w3.eth.getTransactionCount(address, block_identifier=block_identifier)

    @property
    def current_block_number(self):
        return self.w3.eth.blockNumber

    def estimate_gas(self, from_: str, to: str, value: int, data: bytes, block_identifier=None):
        data = data or b''
        params = [
            {"from": from_,
             "to": to,
             "data": HexBytes(data).hex(),
             "value": "0x{:x}".format(value),  # No leading zeroes
             },
        ]
        if block_identifier:
            params.append(block_identifier)

        payload = {
            "method": "eth_estimateGas",
            "params": params,
            "jsonrpc": "2.0",
            "id": 1
        }

        response = requests.post(url=self.ethereum_node_url, json=payload)
        response_json = response.json()
        if 'error' in response_json:
            # When using `pending`, Geth returns
            """
            {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32602,
                    "message": "too many arguments, want at most 1"
                }
            }
            """
            if response_json['error']['code'] == -32602:
                return self.w3.eth.estimateGas({
                    "from": from_,
                    "to": to,
                    "data": data,
                    "value": value,
                })
            else:
                raise ValueError(response_json['error'])
        else:
            return int(response_json['result'], 16)

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

    def get_transaction(self, tx_hash):
        return self.w3.eth.getTransaction(tx_hash)

    def get_transaction_receipt(self, tx_hash, timeout=None):
        if not timeout:
            tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        else:
            try:
                tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)
            except Timeout:
                return None

        # Parity returns tx_receipt even is tx is still pending, so we check `blockNumber` is not None
        return tx_receipt if tx_receipt and tx_receipt['blockNumber'] is not None else None

    def get_block(self, block_number, full_transactions=False):
        return self.w3.eth.getBlock(block_number, full_transactions=full_transactions)

    @tx_with_exception_handling
    def send_transaction(self, transaction_dict: Dict[str, any]) -> bytes:
        return self.w3.eth.sendTransaction(transaction_dict)

    @tx_with_exception_handling
    def send_raw_transaction(self, raw_transaction) -> bytes:
        return self.w3.eth.sendRawTransaction(bytes(raw_transaction))

    def send_unsigned_transaction(self, tx: Dict[str, any], private_key: Union[None, str]=None,
                                  public_key: Union[None, str]=None, retry: bool=False,
                                  block_identifier: Union[None, str]=None) -> bytes:
        """
        Send a tx using an unlocked public key in the node or a private key. Both `public_key` and
        `private_key` cannot be `None`
        :param tx:
        :param private_key:
        :param public_key:
        :param retry: Retry if a problem with nonce is found
        :param block_identifier:
        :return:
        """
        if private_key:
            address = self.private_key_to_address(private_key)
        elif public_key:
            address = public_key
        else:
            logger.error('No ethereum account provided. Need a public_key or private_key')
            raise ValueError("Ethereum account was not configured or unlocked in the node")

        if tx.get('nonce') is None:
            tx['nonce'] = self.get_nonce_for_account(address, block_identifier=block_identifier)

        number_errors = 5
        while number_errors >= 0:
            try:
                if private_key:
                    signed_tx = self.w3.eth.account.signTransaction(tx, private_key=private_key)
                    logger.debug('Sending %d wei from %s to %s', tx['value'], address, tx['to'])
                    return self.send_raw_transaction(signed_tx.rawTransaction)
                elif public_key:
                    tx['from'] = address
                    return self.send_transaction(tx)
            except ReplacementTransactionUnderpriced as e:
                if not retry or not number_errors:
                    raise e
                logger.error('address=%s Tx with nonce=%d was already sent, retrying with nonce + 1',
                             address, tx['nonce'])
                tx['nonce'] += 1
            except InvalidNonce as e:
                if not retry or not number_errors:
                    raise e
                logger.error('address=%s Tx with invalid nonce=%d, retrying recovering nonce again',
                             address, tx['nonce'])
                tx['nonce'] = self.get_nonce_for_account(address, block_identifier=block_identifier)
                number_errors -= 1

    def send_eth_to(self, private_key: str, to: str, gas_price: int, value: int, gas: int=22000,
                    retry: bool = False, block_identifier=None, max_eth_to_send: int = 0) -> bytes:
        """
        Send ether using configured account
        :param to: to
        :param gas_price: gas_price
        :param value: value(wei)
        :param gas: gas, defaults to 22000
        :param retry: Retry if a problem is found
        :param block_identifier: None default, 'pending' not confirmed txs
        :return: tx_hash
        """

        assert check_checksum(to)
        if max_eth_to_send and value > self.w3.toWei(max_eth_to_send, 'ether'):
            raise EtherLimitExceeded('%d is bigger than %f' % (value, max_eth_to_send))

        tx = {
            'to': to,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
        }

        return self.send_unsigned_transaction(tx, private_key=private_key, retry=retry,
                                              block_identifier=block_identifier)

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
