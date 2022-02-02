import os
import random
from logging import getLogger

from eth.constants import SECPK1_N
from web3 import Web3

from gnosis.eth.tests.utils import send_tx

from ..safe_creation_tx import SafeCreationTx

logger = getLogger(__name__)


def generate_salt_nonce() -> int:
    return random.getrandbits(256) - 1


def generate_valid_s() -> int:
    while True:
        s = int(os.urandom(30).hex(), 16)
        if s <= (SECPK1_N // 2):
            return s


def deploy_safe(
    w3: Web3,
    safe_creation_tx: SafeCreationTx,
    funder: str,
    initial_funding_wei: int = 0,
    funder_account=None,
) -> str:
    if funder_account:
        send_tx(
            w3,
            {
                "to": safe_creation_tx.deployer_address,
                "value": safe_creation_tx.payment,
            },
            funder_account,
        )

        send_tx(
            w3,
            {
                "to": safe_creation_tx.safe_address,
                "value": safe_creation_tx.payment + initial_funding_wei,
            },
            funder_account,
        )
    else:
        w3.eth.wait_for_transaction_receipt(
            w3.eth.send_transaction(
                {
                    "from": funder,
                    "to": safe_creation_tx.deployer_address,
                    "value": safe_creation_tx.payment,
                }
            )
        )

        w3.eth.wait_for_transaction_receipt(
            w3.eth.send_transaction(
                {
                    "from": funder,
                    "to": safe_creation_tx.safe_address,
                    "value": safe_creation_tx.payment + initial_funding_wei,
                }
            )
        )

    tx_hash = w3.eth.send_raw_transaction(bytes(safe_creation_tx.tx_raw))
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    assert tx_receipt.contractAddress == safe_creation_tx.safe_address
    assert tx_receipt.status

    return safe_creation_tx.safe_address
