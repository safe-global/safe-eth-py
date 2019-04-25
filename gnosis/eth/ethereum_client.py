from functools import wraps
from logging import getLogger
from typing import Dict, List, NamedTuple, Optional, Union

import requests
from eth_account import Account
from ethereum.utils import (check_checksum, checksum_encode, ecrecover_to_pub,
                            privtoaddr, sha3)
from hexbytes import HexBytes
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from web3.providers import AutoProvider, BaseProvider
from web3.utils.threads import Timeout

from .constants import NULL_ADDRESS
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


class NonceTooLow(ValueError):
    pass


class InsufficientFunds(ValueError):
    pass


class EtherLimitExceeded(ValueError):
    pass


class SenderAccountNotFoundInNode(ValueError):
    pass


class UnknownAccount(ValueError):
    pass


class ParityTraceDecodeException(Exception):
    pass


def tx_with_exception_handling(func):
    error_with_exception: Dict[str, Exception] = {
        'Transaction with the same hash was already imported': TransactionAlreadyImported,
        'replacement transaction underpriced': ReplacementTransactionUnderpriced,
        'There is another transaction with same nonce in the queue': ReplacementTransactionUnderpriced,  # Parity
        'from not found': FromAddressNotFound,
        'correct nonce': InvalidNonce,
        'nonce too low': NonceTooLow,
        'insufficient funds': InsufficientFunds,
        "doesn't have enough funds": InsufficientFunds,
        'sender account not recognized': SenderAccountNotFoundInNode,
        'unknown account': UnknownAccount,
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


class EthereumClientProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            from django.conf import settings
            cls.instance = EthereumClient(settings.ETHEREUM_NODE_URL)
        return cls.instance


class Erc20Manager:
    def __init__(self, ethereum_client, slow_provider_timeout: int = 30):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.slow_w3 = Web3(self.ethereum_client.get_slow_provider(timeout=slow_provider_timeout))

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

    def get_transfer_history(self, from_block: int, to_block: Optional[int] = None,
                             from_address: Optional[str] = None, to_address: Optional[str] = None,
                             token_address: Optional[str] = None) -> List[Dict[str, any]]:
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
        :param to_block: Block to stop querying from
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
                                                  toBlock=to_block,
                                                  address=token_address,
                                                  argument_filters=argument_filters).get_all_entries()

    def send_tokens(self, to: str, amount: int, erc20_address: str, private_key: str) -> bytes:
        """
        Send tokens to address
        :param to:
        :param amount:
        :param erc20_address:
        :param private_key:
        :return: tx_hash
        """
        erc20 = get_erc20_contract(self.w3, erc20_address)
        account = Account.privateKeyToAccount(private_key)
        tx = erc20.functions.transfer(to, amount).buildTransaction({'from': account.address})
        return self.ethereum_client.send_unsigned_transaction(tx, private_key=private_key)


class ParityManager:
    def __init__(self, ethereum_client, slow_provider_timeout: int = 100):
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.slow_w3 = Web3(self.ethereum_client.get_slow_provider(timeout=slow_provider_timeout))

    #TODO Test with mock
    def _decode_trace_action(self, action: Dict[str, any]) -> Dict[str, any]:
        decoded = {
            'from': self.w3.toChecksumAddress(action['from']),
            'gas': int(action['gas'], 16),
            'value': int(action['value'], 16),
        }
        # CALL or DELEGATECALL
        if 'callType' in action:
            decoded['callType'] = action['callType']
        if 'input' in action:
            decoded['input'] = HexBytes(action['input'])
        if 'to' in action:
            decoded['to'] = self.w3.toChecksumAddress(action['to'])

        # CREATE or CREATE2
        if 'init' in action:
            decoded['init'] = HexBytes(action['init'])
        return decoded

    def _decode_trace_result(self, result: Dict[str, any]) -> Dict[str, any]:
        decoded = {
            'gasUsed': int(result['gasUsed'], 16),
        }

        # CALL or DELEGATECALL
        if 'output' in result:
            decoded['output'] = HexBytes(result['output'])

        # CREATE or CREATE2
        if 'code' in result:
            decoded['code'] = HexBytes(result['code'])
        if 'address' in result:
            decoded['address'] = self.w3.toChecksumAddress(result['address'])

        return decoded

    def _decode_traces(self, traces: List[Dict[str, any]]) -> List[Dict[str, any]]:
        new_traces = []
        for trace in traces:
            if not isinstance(trace, dict):
                raise ParityTraceDecodeException('Expected dictionary, but found unexpected trace %s' % trace)
            trace_copy = trace.copy()
            new_traces.append(trace_copy)
            # Txs with `error` field don't have `result` field
            if 'result' in trace:
                trace_copy['result'] = self._decode_trace_result(trace['result'])
            trace_copy['action'] = self._decode_trace_action(trace['action'])
        return new_traces

    def trace_transaction(self, tx_hash: str) -> Dict[str, any]:
        try:
            return self._decode_traces(self.slow_w3.parity.traceTransaction(parameters))
        except ParityTraceDecodeException as exc:
            logger.warning('Problem decoding trace: %s - Retrying', exc)
            return self._decode_traces(self.slow_w3.parity.traceTransaction(parameters))

    def trace_filter(self, from_block: int = 1, to_block: Optional[int] = None,
                     from_address: Optional[List[str]] = None, to_address: Optional[List[str]] = None,
                     after: Optional[int] = None, count: Optional[int] = None) -> List[Dict[str, any]]:
        """
        :param from_block: Quantity or Tag - (optional) From this block. `0` is not working, it needs to be `>= 1`
        :param to_block: Quantity or Tag - (optional) To this block.
        :param from_address: Array - (optional) Sent from these addresses.
        :param to_address: Address - (optional) Sent to these addresses.
        :param after: Quantity - (optional) The offset trace number
        :param count: Quantity - (optional) Integer number of traces to display in a batch.
        :return:
          [
            {
              "action": {
                "callType": "call",
                "from": "0x32be343b94f860124dc4fee278fdcbd38c102d88",
                "gas": "0x4c40d",
                "input": "0x",
                "to": "0x8bbb73bcb5d553b5a556358d27625323fd781d37",
                "value": "0x3f0650ec47fd240000"
              },
              "blockHash": "0x86df301bcdd8248d982dbf039f09faf792684e1aeee99d5b58b77d620008b80f",
              "blockNumber": 3068183,
              "result": {
                "gasUsed": "0x0",
                "output": "0x"
              },
              "subtraces": 0,
              "traceAddress": [],
              "transactionHash": "0x3321a7708b1083130bd78da0d62ead9f6683033231617c9d268e2c7e3fa6c104",
              "transactionPosition": 3,
              "type": "call"
            },
          {
            "action": {
              "from": "0x3b169a0fb55ea0b6bafe54c272b1fe4983742bf7",
              "gas": "0x49b0b",
              "init": "0x608060405234801561001057600080fd5b5060405161060a38038061060a833981018060405281019080805190602001909291908051820192919060200180519060200190929190805190602001909291908051906020019092919050505084848160008173ffffffffffffffffffffffffffffffffffffffff1614151515610116576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260248152602001807f496e76616c6964206d617374657220636f707920616464726573732070726f7681526020017f696465640000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506000815111156101a35773ffffffffffffffffffffffffffffffffffffffff60005416600080835160208501846127105a03f46040513d6000823e600082141561019f573d81fd5b5050505b5050600081111561036d57600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614156102b7578273ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f1935050505015156102b2576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f436f756c64206e6f74207061792073616665206372656174696f6e207769746881526020017f206574686572000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b61036c565b6102d1828483610377640100000000026401000000009004565b151561036b576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f436f756c64206e6f74207061792073616665206372656174696f6e207769746881526020017f20746f6b656e000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b5050505050610490565b600060608383604051602401808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001925050506040516020818303038152906040527fa9059cbb000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff838183161783525050505090506000808251602084016000896127105a03f16040513d6000823e3d60008114610473576020811461047b5760009450610485565b829450610485565b8151158315171594505b505050509392505050565b61016b8061049f6000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634555d5c91461008b5780635c60da1b146100b6575b73ffffffffffffffffffffffffffffffffffffffff600054163660008037600080366000845af43d6000803e6000811415610086573d6000fd5b3d6000f35b34801561009757600080fd5b506100a061010d565b6040518082815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610116565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006002905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050905600a165627a7a7230582007fffd557dfc8c4d2fdf56ba6381a6ce5b65b6260e1492d87f26c6d4f1d0410800290000000000000000000000008942595a2dc5181df0465af0d7be08c8f23c93af00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d9e09beaeb338d81a7c5688358df0071d498811500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001b15f91a8c35300000000000000000000000000000000000000000000000000000000000001640ec78d9e00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000004000000000000000000000000f763ea5fbb191d47dc4b083dcdc3cdfb586468f8000000000000000000000000ad25c9717d04c0a12086a1d352c1ccf4bf5fcbf80000000000000000000000000da7155692446c80a4e7ad72018e586f20fa3bfe000000000000000000000000bce0cc48ce44e0ac9ee38df4d586afbacef191fa0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
              "value": "0x0"
            },
            "blockHash": "0x03f9f64dfeb7807b5df608e6957dd4d521fd71685aac5533451d27f0abe03660",
            "blockNumber": 3793534,
            "result": {
              "address": "0x61a7cc907c47c133d5ff5b685407201951fcbd08",
              "code": "0x60806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634555d5c91461008b5780635c60da1b146100b6575b73ffffffffffffffffffffffffffffffffffffffff600054163660008037600080366000845af43d6000803e6000811415610086573d6000fd5b3d6000f35b34801561009757600080fd5b506100a061010d565b6040518082815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610116565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006002905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050905600a165627a7a7230582007fffd557dfc8c4d2fdf56ba6381a6ce5b65b6260e1492d87f26c6d4f1d041080029",
              "gasUsed": "0x4683f"
            },
            "subtraces": 2,
            "traceAddress": [],
            "transactionHash": "0x6c7e8f8778d33d81b29c4bd7526ee50a4cea340d69eed6c89ada4e6fab731789",
            "transactionPosition": 1,
            "type": "create"
          },
          ...
        ]
        """
        assert from_address or to_address, 'You must provide at least `from_address` or `to_address`'
        parameters = {}
        if from_block:
            parameters['fromBlock'] = '0x%x' % from_block
        if to_block:
            parameters['toBlock'] = '0x%x' % to_block
        if from_address:
            parameters['fromAddress'] = from_address
        if to_address:
            parameters['toAddress'] = to_address
        if after:
            parameters['after'] = after
        if count:
            parameters['count'] = count

        try:
            return self._decode_traces(self.slow_w3.parity.traceFilter(parameters))
        except ParityTraceDecodeException as exc:
            logger.warning('Problem decoding trace: %s - Retrying', exc)
            return self._decode_traces(self.slow_w3.parity.traceFilter(parameters))


class EthereumClient:
    """
    Manage ethereum operations. Uses web3 for the most part, but some other stuff is implemented from scratch.
    Note: If you want to use `pending` state with `Parity`, it must be run with `--pruning=archive` or `--force-sealing`
    """
    NULL_ADDRESS = NULL_ADDRESS

    def __init__(self, ethereum_node_url: str):
        self.ethereum_node_url: str = ethereum_node_url
        self.w3_provider = HTTPProvider(self.ethereum_node_url)
        self.w3: Web3 = Web3(self.w3_provider)
        self.erc20: Erc20Manager = Erc20Manager(self)
        self.parity: ParityManager = ParityManager(self)
        try:
            if int(self.w3.net.version) != 1:
                self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
            # For tests using dummy connections (like IPC)
        except (ConnectionError, FileNotFoundError):
            self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    def get_slow_provider(self, timeout: int):
        """
        Get web3 provider for slow queries. Default `HTTPProvider` timeouts after 10 seconds
        :param provider: Configured Web3 provider
        :param timeout: Timeout to configure for internal requests (default is 10)
        :return: A new web3 provider with the `slow_provider_timeout`
        """
        if isinstance(self.w3_provider, AutoProvider):
            return HTTPProvider(endpoint_uri='http://localhost:8545',
                                request_kwargs={'timeout': timeout})
        elif isinstance(self.w3_provider, HTTPProvider):
            return HTTPProvider(endpoint_uri=self.w3_provider.endpoint_uri,
                                request_kwargs={'timeout': timeout})
        else:
            return self.w3_provider

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

    def get_block(self, block_number: int, full_transactions=False):
        return self.w3.eth.getBlock(block_number, full_transactions=full_transactions)

    def is_contract(self, contract_address: str):
        return bool(self.w3.eth.getCode(contract_address))

    @tx_with_exception_handling
    def send_transaction(self, transaction_dict: Dict[str, any]) -> bytes:
        return self.w3.eth.sendTransaction(transaction_dict)

    @tx_with_exception_handling
    def send_raw_transaction(self, raw_transaction) -> bytes:
        return self.w3.eth.sendRawTransaction(bytes(raw_transaction))

    def send_unsigned_transaction(self, tx: Dict[str, any], private_key: Optional[str] = None,
                                  public_key: Optional[str] = None, retry: bool = False,
                                  block_identifier: Optional[str] = None) -> bytes:
        """
        Send a tx using an unlocked public key in the node or a private key. Both `public_key` and
        `private_key` cannot be `None`
        :param tx:
        :param private_key:
        :param public_key:
        :param retry: Retry if a problem with nonce is found
        :param block_identifier:
        :return: tx hash
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
                    try:
                        return self.send_raw_transaction(signed_tx.rawTransaction)
                    except TransactionAlreadyImported as e:
                        # Sometimes Parity 2.2.11 fails with Transaction already imported, even if it's not, but it's
                        # processed
                        tx_hash = signed_tx.hash
                        logger.error('Transaction with tx-hash=%s already imported: %s' % (tx_hash.hex(), str(e)))
                        return tx_hash
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
    def get_signing_address(hash: Union[bytes, str], v: int, r: int, s: int) -> str:
        """
        :return: checksum encoded address starting by 0x, for example `0x568c93675A8dEb121700A6FAdDdfE7DFAb66Ae4A`
        :rtype: str
        """
        encoded_64_address = ecrecover_to_pub(hash, v, r, s)
        address_bytes = sha3(encoded_64_address)[-20:]
        return checksum_encode(address_bytes)
