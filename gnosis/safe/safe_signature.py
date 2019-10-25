from logging import getLogger
from typing import Union, Iterable

from eth_account.messages import defunct_hash_message
from ethereum.utils import checksum_encode
from hexbytes import HexBytes

from gnosis.eth import EthereumClient
from gnosis.safe.signatures import signature_split

logger = getLogger(__name__)


EthereumBytes = Union[bytes, str]


class SafeSignature:
    def __init__(self, signature: EthereumBytes, safe_tx_hash: EthereumBytes):
        self.signature = HexBytes(signature)
        self.v, self.r, self.s = signature_split(self.signature)
        self.owner = self.decode_owner(self.v, self.r, self.s, safe_tx_hash)

    @classmethod
    def parse_signatures(cls, signatures: EthereumBytes, safe_tx_hash: EthereumBytes) -> Iterable['SafeSignature']:
        signature_size = 65
        for i in range(0, len(signatures), signature_size):
            yield cls(signatures[i: i + signature_size], safe_tx_hash)

    def decode_owner(self, v: int, r: int, s: int, safe_tx_hash: EthereumBytes):
        # TODO End contract signatures
        if v == 0:  # Contract signature
            raise NotImplemented
        elif v == 1:  # Approved hash
            return checksum_encode(r)
        elif v > 30:  # Support eth_sign
            # defunct_hash_message preprends `\x19Ethereum Signed Message:\n32`
            message_hash = defunct_hash_message(primitive=safe_tx_hash)
            return EthereumClient.get_signing_address(message_hash, v - 4, r, s)
        else:  # EOA signature
            return EthereumClient.get_signing_address(safe_tx_hash, v, r, s)

