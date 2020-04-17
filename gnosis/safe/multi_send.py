from enum import Enum
from logging import getLogger
from typing import Any, Dict, List, Union

from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth import EthereumClient
from gnosis.eth.contracts import get_multi_send_contract
from gnosis.eth.ethereum_client import EthereumTxSent

logger = getLogger(__name__)


class MultiSendOperation(Enum):
    CALL = 0
    DELEGATE_CALL = 1


class MultiSendTx:
    def __init__(self, operation: MultiSendOperation, address: str, value: int, data: Union[str, bytes]):
        self.operation = operation
        self.address = address
        self.value = value
        self.data = HexBytes(data)

    def __eq__(self, other):
        if not isinstance(other, MultiSendTx):
            return NotImplemented

        return (self.operation == other.operation and self.address == other.address
                and self.value == other.value and self.data == other.data)

    @classmethod
    def from_bytes(cls, encoded_multisend_tx: bytes):
        operation = MultiSendOperation(encoded_multisend_tx[0])
        address = Web3.toChecksumAddress(encoded_multisend_tx[1:1 + 20])
        value = int.from_bytes(encoded_multisend_tx[21:21 + 32], byteorder='big')
        # data_lenght = int.from_bytes(encoded_multisend_tx[21 + 32: 21 + 32 * 2], byteorder='big)
        data = encoded_multisend_tx[21 + 32 * 2:]
        return cls(operation, address, value, data)

    @property
    def encoded_data(self):
        multisend_operation = HexBytes('{:0>2x}'.format(self.operation.value))  # Operation 1 byte
        multisend_address = HexBytes('{:0>40x}'.format(int(self.address, 16)))  # Address 20 bytes
        multisend_value = HexBytes('{:0>64x}'.format(self.value))  # Value 32 bytes
        data_lenght = HexBytes('{:0>64x}'.format(len(self.data)))  # Data length 32 bytes
        return multisend_operation + multisend_address + multisend_value + data_lenght + self.data


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

        tx_hash = ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.key)
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt.status
        contract_address = tx_receipt.contractAddress
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
        multisig_contract = self.get_contract()
        encoded_multisend_data = b''.join([x.encoded_data for x in multi_send_txs])
        return multisig_contract.functions.multiSend(encoded_multisend_data).buildTransaction({'gas': 1,
                                                                                               'gasPrice': 1})['data']
