from enum import Enum
from logging import getLogger
from typing import Iterable, Union

from eth_account.messages import defunct_hash_message
from ethereum.utils import checksum_encode
from hexbytes import HexBytes

from gnosis.eth import EthereumClient
from gnosis.eth.contracts import get_safe_contract
from gnosis.safe.signatures import get_signing_address, signature_split

logger = getLogger(__name__)


EthereumBytes = Union[bytes, str]


class SafeSignatureType(Enum):
    CONTRACT_SIGNATURE = 0
    APPROVED_HASH = 1
    EOA_SIGNATURE = 2
    ETH_SIGN = 3

    @staticmethod
    def from_v(v: int):
        if v == 0:
            return SafeSignatureType.CONTRACT_SIGNATURE
        elif v == 1:
            return SafeSignatureType.APPROVED_HASH
        elif v > 30:
            return SafeSignatureType.ETH_SIGN
        else:
            return SafeSignatureType.EOA_SIGNATURE


# TODO Create method to generate signature based on multiple `SafeSignature`. This is very important to
# prepare the payloads for CONTRACT_SIGNATUREs. Also, signatures must be sorted by owner
class SafeSignature:
    EIP1271_MAGIC_VALUE = HexBytes(0x20c13b0b)

    def __init__(self, signature: EthereumBytes, safe_tx_hash: EthereumBytes, contract_signature: EthereumBytes = b''):
        self.signature = HexBytes(signature)
        self.safe_tx_hash = safe_tx_hash
        self.contract_signature = contract_signature

        self.v, self.r, self.s = signature_split(self.signature)
        self.signature_type = SafeSignatureType.from_v(self.v)

    @property
    def owner(self):
        """
        :return: Decode owner from signature, without any further validation (signature can be not valid)
        """
        v, r, s, safe_tx_hash = self.v, self.r, self.s, self.safe_tx_hash
        if v == 0:  # Contract signature
            # We don't need further checks to get the owner
            contract_address = checksum_encode(r)
            return contract_address
        elif v == 1:  # Approved hash
            return checksum_encode(r)
        elif v > 30:  # Eth_sign, v = v + 4 to be different from EOA signature
            # defunct_hash_message prepends `\x19Ethereum Signed Message:\n32`
            message_hash = defunct_hash_message(primitive=safe_tx_hash)
            return get_signing_address(message_hash, v - 4, r, s)
        else:  # EOA signature
            return get_signing_address(safe_tx_hash, v, r, s)

    def is_valid(self, ethereum_client: EthereumClient, safe_address: str) -> bool:
        """
        :param ethereum_client: Required for Contract Signature and Approved Hash check
        :param safe_address: Required for Approved Hash check
        :return: `True` if signature is valid, `False` otherwise
        """
        if self.signature_type == SafeSignatureType.CONTRACT_SIGNATURE:
            safe_contract = get_safe_contract(ethereum_client.w3, self.owner)
            return safe_contract.functions.isValidSignature(self.safe_tx_hash,
                                                            self.contract_signature
                                                            ).call() == self.EIP1271_MAGIC_VALUE
        elif self.signature_type == SafeSignatureType.APPROVED_HASH:
            safe_contract = get_safe_contract(ethereum_client.w3, safe_address)
            return safe_contract.functions.approvedHashes(self.owner,
                                                          self.safe_tx_hash).call() == 1
        else:  # EOA and Eth sign must be validated
            return True

    @classmethod
    def parse_signatures(cls, signatures: EthereumBytes, safe_tx_hash: EthereumBytes) -> Iterable['SafeSignature']:
        signature_size = 65  # For contract signatures there'll be some data at the end
        data_position = len(signatures)  # For contract signatures, to stop parsing at data position

        for i in range(0, len(signatures), signature_size):
            if i >= data_position:  # If contract signature data position is reached, stop
                break

            signature = signatures[i: i + signature_size]
            v, r, s = signature_split(signature)
            if v == 0:  # Contract signature
                if s < data_position:
                    data_position = s
                contract_signature_len = int.from_bytes(signatures[s:s + 32], 'big')  # Len size is 32 bytes
                contract_signature = signatures[s + 32:s + 32 + contract_signature_len]  # Skip array size (32 bytes)
            else:
                contract_signature = None

            yield cls(signature, safe_tx_hash, contract_signature=contract_signature)
