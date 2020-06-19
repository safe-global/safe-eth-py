from enum import Enum
from logging import getLogger
from typing import List, Union

from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth import EthereumClient
from gnosis.eth.contracts import get_multi_send_contract
from gnosis.eth.ethereum_client import EthereumTxSent
from gnosis.eth.typing import EthereumData

logger = getLogger(__name__)


class MultiSendOperation(Enum):
    CALL = 0
    DELEGATE_CALL = 1


class MultiSendTx:
    def __init__(self, operation: MultiSendOperation, to: str, value: int, data: EthereumData):
        self.operation = operation
        self.to = to
        self.value = value
        self.data = HexBytes(data) if data else b''

    def __eq__(self, other):
        if not isinstance(other, MultiSendTx):
            return NotImplemented

        return (self.operation == other.operation and self.to == other.to
                and self.value == other.value and self.data == other.data)

    def __len__(self):
        """
        :return: Size on bytes of the tx
        """
        return 21 + 32 * 2 + self.data_length

    def __str__(self):
        data = self.data[:4].hex() + ('...' if len(self.data) > 4 else '')
        return f'MultisendTx operation={self.operation.name} to={self.to} value={self.value}' \
               f' data={data}'

    @property
    def data_length(self) -> int:
        return len(self.data)

    @property
    def encoded_data(self):
        operation = HexBytes('{:0>2x}'.format(self.operation.value))  # Operation 1 byte
        to = HexBytes('{:0>40x}'.format(int(self.to, 16)))  # Address 20 bytes
        value = HexBytes('{:0>64x}'.format(self.value))  # Value 32 bytes
        data_length = HexBytes('{:0>64x}'.format(self.data_length))  # Data length 32 bytes
        return operation + to + value + data_length + self.data

    @classmethod
    def from_bytes(cls, encoded_multisend_tx: Union[str, bytes]) -> 'MultiSendTx':
        """
        Decodes one multisend transaction. If there's more data after `data` it's ignored. Structure:
        operation   -> MultiSendOperation 1 byte
        to          -> ethereum address 20 bytes
        value       -> tx value 32 bytes
        data_length -> 32 bytes
        data        -> `data_length` bytes
        :param encoded_multisend_tx: 1 multisend transaction encoded
        :return: Tx as a MultisendTx
        """
        encoded_multisend_tx = HexBytes(encoded_multisend_tx)

        operation = MultiSendOperation(encoded_multisend_tx[0])
        to = Web3.toChecksumAddress(encoded_multisend_tx[1:1 + 20])
        value = int.from_bytes(encoded_multisend_tx[21:21 + 32], byteorder='big')
        data_length = int.from_bytes(encoded_multisend_tx[21 + 32: 21 + 32 * 2], byteorder='big')
        data = encoded_multisend_tx[21 + 32 * 2: 21 + 32 * 2 + data_length]
        if data_length != len(data):
            raise ValueError('Data length is different from len(data)')

        return cls(operation, to, value, data)


class MultiSend:
    def __init__(self, address: str, ethereum_client: EthereumClient):
        assert Web3.isChecksumAddress(address), \
            '%s proxy factory address not valid' % address

        self.address = address
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    @classmethod
    def from_bytes(cls, encoded_multisend_txs: Union[str, bytes]) -> List[MultiSendTx]:
        """
        Decodes one or more multisend transactions from `bytes transactions` (Abi decoded)
        :param encoded_multisend_txs:
        :return: List of MultiSendTxs
        """
        if not encoded_multisend_txs:
            return []

        encoded_multisend_txs = HexBytes(encoded_multisend_txs)
        multisend_tx = MultiSendTx.from_bytes(encoded_multisend_txs)
        multisend_tx_size = len(multisend_tx)

        assert multisend_tx_size > 0, 'Multisend tx cannot be empty'  # This should never happen, just in case
        remaining_data = encoded_multisend_txs[multisend_tx_size:]

        return [multisend_tx] + cls.from_bytes(remaining_data)

    @classmethod
    def from_transaction_data(cls, multisend_data: Union[str, bytes]) -> List[MultiSendTx]:
        """
        Decodes multisend transactions from transaction data (ABI encoded with selector)
        :return:
        """
        try:
            _, data = get_multi_send_contract(Web3()).decode_function_input(multisend_data)
            return cls.from_bytes(data['transactions'])
        except ValueError:
            return []

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

        tx_hash = ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.key)
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt
        assert tx_receipt['status']
        contract_address = tx_receipt['contractAddress']
        logger.info("Deployed and initialized Proxy Factory Contract=%s by %s", contract_address,
                    deployer_account.address)
        return EthereumTxSent(tx_hash, tx, contract_address)

    def get_contract(self):
        return get_multi_send_contract(self.ethereum_client.w3, self.address)

    def build_tx_data(self, multi_send_txs: List[MultiSendTx]) -> bytes:
        """
        Txs don't need to be valid to get through
        :param multi_send_txs:
        :param sender:
        :return:
        """
        multisend_contract = self.get_contract()
        encoded_multisend_data = b''.join([x.encoded_data for x in multi_send_txs])
        return multisend_contract.functions.multiSend(encoded_multisend_data).buildTransaction({'gas': 1,
                                                                                               'gasPrice': 1})['data']
