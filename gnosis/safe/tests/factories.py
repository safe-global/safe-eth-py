import os
from logging import getLogger

from django_eth.tests.factories import get_eth_address_with_key
from ethereum.transactions import secpk1n
from faker import Factory as FakerFactory
from faker import Faker

from ..contracts import get_example_erc20_contract
from ..safe_creation_tx import SafeCreationTx
from ..safe_service import SafeService

fakerFactory = FakerFactory.create()
faker = Faker()

logger = getLogger(__name__)


def generate_valid_s():
    while True:
        s = int(os.urandom(30).hex(), 16)
        if s <= (secpk1n // 2):
            return s


def generate_safe(safe_service: SafeService, owners=None, number_owners: int=3, threshold: int=None,
                  gas_price: int=1) -> SafeCreationTx:
    s = generate_valid_s()

    if not owners:
        owners = []
        for _ in range(number_owners):
            owner, _ = get_eth_address_with_key()
            owners.append(owner)

    threshold = threshold if threshold else len(owners)

    return safe_service.build_safe_creation_tx(s, owners, threshold, gas_price=gas_price, payment_token=None)


def deploy_safe(w3, safe_creation_tx: SafeCreationTx, funder: str, initial_funding_wei: int=0) -> str:
    w3.eth.waitForTransactionReceipt(
        w3.eth.sendTransaction({
            'from': funder,
            'to': safe_creation_tx.deployer_address,
            'value': safe_creation_tx.payment
        })
    )

    w3.eth.waitForTransactionReceipt(
        w3.eth.sendTransaction({
            'from': funder,
            'to': safe_creation_tx.safe_address,
            'value': safe_creation_tx.payment
        })
    )

    tx_hash = w3.eth.sendRawTransaction(bytes(safe_creation_tx.raw_tx))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert tx_receipt.contractAddress == safe_creation_tx.safe_address
    assert tx_receipt.status

    if initial_funding_wei > 0:
        w3.eth.waitForTransactionReceipt(
            w3.eth.sendTransaction({
                'from': funder,
                'to': safe_creation_tx.safe_address,
                'value': initial_funding_wei
            })
        )

    return safe_creation_tx.safe_address


def deploy_example_erc20(w3, amount: int, owner: str, deployer: str=None):
    deployer = deployer or w3.eth.accounts[0]
    erc20_contract = get_example_erc20_contract(w3)
    tx_hash = erc20_contract.constructor(amount, owner).transact({'from': deployer})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    erc20_address = tx_receipt.contractAddress
    deployed_erc20 = get_example_erc20_contract(w3, erc20_address)
    return deployed_erc20
