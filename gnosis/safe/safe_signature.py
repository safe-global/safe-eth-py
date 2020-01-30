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


# TODO Refactor
class SafeSignature:
    def __init__(self, signature: EthereumBytes, safe_tx_hash: EthereumBytes):
        self.signature = HexBytes(signature)
        self.v, self.r, self.s = signature_split(self.signature)
        self.signature_type = SafeSignatureType.from_v(self.v)
        self.owner = self.decode_owner(self.v, self.r, self.s, safe_tx_hash)

    @classmethod
    def parse_signatures(cls, signatures: EthereumBytes, safe_tx_hash: EthereumBytes) -> Iterable['SafeSignature']:
        signature_size = 65
        for i in range(0, len(signatures), signature_size):
            yield cls(signatures[i: i + signature_size], safe_tx_hash)

    def decode_owner(self, v: int, r: int, s: int, safe_tx_hash: EthereumBytes):
        if v == 0:  # Contract signature
            # We don't need further checks
            contract_address = checksum_encode(r)
            return contract_address
        elif v == 1:  # Approved hash
            return checksum_encode(r)
        elif v > 30:  # Support eth_sign
            # defunct_hash_message preprends `\x19Ethereum Signed Message:\n32`
            message_hash = defunct_hash_message(primitive=safe_tx_hash)
            return get_signing_address(message_hash, v - 4, r, s)
        else:  # EOA signature
            return get_signing_address(safe_tx_hash, v, r, s)


# TODO Support Multiple Contract Signatures
class SafeContractSignature:
    """
    Decode one contract signature
    """
    EIP1271_MAGIC_VALUE = HexBytes(0x20c13b0b)

    def __init__(self, signature: EthereumBytes, safe_tx_hash: EthereumBytes, ethereum_client: EthereumClient):
        assert len(signature) > 65, 'Signature must be at least 65'

        # v = signature type, r = contract, s = offset of dynamic signature data
        self.v, self.r, self.s = signature_split(signature)
        assert self.v == 0, 'v must be 0'

        self.signature = HexBytes(signature)
        self.safe_tx_hash = safe_tx_hash
        self.ethereum_client = ethereum_client
        self.owner = checksum_encode(self.r)
        self.ok = self._check_signature()

    def _check_signature(self) -> bool:
        contract_signature_len = int.from_bytes(self.signature[self.s:self.s + 32], 'big')
        contract_signature = self.signature[self.s + 32:self.s + 32 + contract_signature_len]
        safe_contract = get_safe_contract(self.ethereum_client.w3, self.owner)
        return safe_contract.functions.isValidSignature(self.safe_tx_hash,
                                                        contract_signature
                                                        ).call() == self.EIP1271_MAGIC_VALUE
