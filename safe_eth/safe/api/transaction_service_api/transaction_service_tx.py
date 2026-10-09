from eth_typing import ChecksumAddress

from safe_eth.safe import SafeTx


class TransactionServiceTx(SafeTx):
    def __init__(self, proposer: ChecksumAddress | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proposer = proposer
