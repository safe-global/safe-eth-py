from eth_typing import ChecksumAddress

from gnosis.safe import SafeTx


class TransactionServiceTx(SafeTx):
    def __init__(self, proposer: ChecksumAddress, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proposer = proposer
