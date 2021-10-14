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
    """
    Wrapper for a single MultiSendTx
    """

    def __init__(
        self,
        operation: MultiSendOperation,
        to: str,
        value: int,
        data: EthereumData,
        old_encoding: bool = False,
    ):
        """
        :param operation: MultisendOperation, CALL or DELEGATE_CALL
        :param to: Address
        :param value: Value in Wei
        :param data: data as hex string or bytes
        :param old_encoding: True if using old multisend ABI Encoded data, False otherwise
        """
        self.operation = operation
        self.to = to
        self.value = value
        self.data = HexBytes(data) if data else b""
        self.old_encoding = old_encoding

    def __eq__(self, other):
        if not isinstance(other, MultiSendTx):
            return NotImplemented

        return (
            self.operation == other.operation
            and self.to == other.to
            and self.value == other.value
            and self.data == other.data
        )

    def __len__(self):
        """
        :return: Size on bytes of the tx
        """
        return 21 + 32 * 2 + self.data_length

    def __repr__(self):
        data = self.data[:4].hex() + ("..." if len(self.data) > 4 else "")
        return (
            f"MultisendTx operation={self.operation.name} to={self.to} value={self.value} "
            f"data={data}"
        )

    @property
    def data_length(self) -> int:
        return len(self.data)

    @property
    def encoded_data(self):
        operation = HexBytes("{:0>2x}".format(self.operation.value))  # Operation 1 byte
        to = HexBytes("{:0>40x}".format(int(self.to, 16)))  # Address 20 bytes
        value = HexBytes("{:0>64x}".format(self.value))  # Value 32 bytes
        data_length = HexBytes(
            "{:0>64x}".format(self.data_length)
        )  # Data length 32 bytes
        return operation + to + value + data_length + self.data

    @classmethod
    def from_bytes(cls, encoded_multisend_tx: Union[str, bytes]) -> "MultiSendTx":
        """
        Decoded one MultiSend transaction. ABI must be used to get the `transactions` parameter and use that data
        for this function
        :param encoded_multisend_tx:
        :return:
        """
        encoded_multisend_tx = HexBytes(encoded_multisend_tx)
        try:
            return cls._decode_multisend_data(encoded_multisend_tx)
        except ValueError:
            # Try using the old decoding method
            return cls._decode_multisend_old_transaction(encoded_multisend_tx)

    @classmethod
    def _decode_multisend_data(cls, encoded_multisend_tx: Union[str, bytes]):
        """
        Decodes one Multisend transaction. If there's more data after `data` it's ignored. Fallbacks to the old
        multisend structure if this structure cannot be decoded.
        https://etherscan.io/address/0x8D29bE29923b68abfDD21e541b9374737B49cdAD#code
        Structure:
            - operation   -> MultiSendOperation 1 byte
            - to          -> ethereum address 20 bytes
            - value       -> tx value 32 bytes
            - data_length -> 32 bytes
            - data        -> `data_length` bytes
        :param encoded_multisend_tx: 1 multisend transaction encoded
        :return: Tx as a MultisendTx
        """
        encoded_multisend_tx = HexBytes(encoded_multisend_tx)
        operation = MultiSendOperation(encoded_multisend_tx[0])
        to = Web3.toChecksumAddress(encoded_multisend_tx[1 : 1 + 20])
        value = int.from_bytes(encoded_multisend_tx[21 : 21 + 32], byteorder="big")
        data_length = int.from_bytes(
            encoded_multisend_tx[21 + 32 : 21 + 32 * 2], byteorder="big"
        )
        data = encoded_multisend_tx[21 + 32 * 2 : 21 + 32 * 2 + data_length]
        len_data = len(data)
        if len_data != data_length:
            raise ValueError(
                f"Data length {data_length} is different from len(data) {len_data}"
            )
        return cls(operation, to, value, data, old_encoding=False)

    @classmethod
    def _decode_multisend_old_transaction(
        cls, encoded_multisend_tx: Union[str, bytes]
    ) -> "MultiSendTx":
        """
        Decodes one old multisend transaction. If there's more data after `data` it's ignored. The difference with
        the new MultiSend is that every value but `data` is padded to 32 bytes, wasting a lot of bytes.
        https://etherscan.io/address/0xE74d6AF1670FB6560dd61EE29eB57C7Bc027Ce4E#code
        Structure:
            - operation   -> MultiSendOperation 32 byte
            - to          -> ethereum address 32 bytes
            - value       -> tx value 32 bytes
            - data_length -> 32 bytes
            - data        -> `data_length` bytes
        :param encoded_multisend_tx: 1 multisend transaction encoded
        :return: Tx as a MultisendTx
        """
        encoded_multisend_tx = HexBytes(encoded_multisend_tx)
        operation = MultiSendOperation(
            int.from_bytes(encoded_multisend_tx[:32], byteorder="big")
        )
        to = Web3.toChecksumAddress(encoded_multisend_tx[32:64][-20:])
        value = int.from_bytes(encoded_multisend_tx[64:96], byteorder="big")
        data_length = int.from_bytes(encoded_multisend_tx[128:160], byteorder="big")
        data = encoded_multisend_tx[160 : 160 + data_length]
        len_data = len(data)
        if len_data != data_length:
            raise ValueError(
                f"Data length {data_length} is different from len(data) {len_data}"
            )
        return cls(operation, to, value, data, old_encoding=True)


class MultiSend:
    dummy_w3 = Web3()

    def __init__(self, address: str, ethereum_client: EthereumClient):
        assert Web3.isChecksumAddress(address), (
            "%s proxy factory address not valid" % address
        )

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

        assert (
            multisend_tx_size > 0
        ), "Multisend tx cannot be empty"  # This should never happen, just in case
        if multisend_tx.old_encoding:
            next_data_position = (
                (multisend_tx.data_length + 0x1F) // 0x20 * 0x20
            ) + 0xA0
        else:
            next_data_position = multisend_tx_size
        remaining_data = encoded_multisend_txs[next_data_position:]

        return [multisend_tx] + cls.from_bytes(remaining_data)

    @classmethod
    def from_transaction_data(
        cls, multisend_data: Union[str, bytes]
    ) -> List[MultiSendTx]:
        """
        Decodes multisend transactions from transaction data (ABI encoded with selector)
        :return:
        """
        try:
            _, data = get_multi_send_contract(cls.dummy_w3).decode_function_input(
                multisend_data
            )
            return cls.from_bytes(data["transactions"])
        except ValueError:
            return []

    @staticmethod
    def deploy_contract(
        ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy proxy factory contract
        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        contract = get_multi_send_contract(ethereum_client.w3)
        tx = contract.constructor().buildTransaction({"from": deployer_account.address})

        tx_hash = ethereum_client.send_unsigned_transaction(
            tx, private_key=deployer_account.key
        )
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt
        assert tx_receipt["status"]
        contract_address = tx_receipt["contractAddress"]
        logger.info(
            "Deployed and initialized Proxy Factory Contract=%s by %s",
            contract_address,
            deployer_account.address,
        )
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
        encoded_multisend_data = b"".join([x.encoded_data for x in multi_send_txs])
        return multisend_contract.functions.multiSend(
            encoded_multisend_data
        ).buildTransaction({"gas": 1, "gasPrice": 1})["data"]
