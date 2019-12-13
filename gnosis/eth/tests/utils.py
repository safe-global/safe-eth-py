from eth_account.signers.local import LocalAccount
from web3 import Web3

from ..contracts import get_example_erc20_contract


def send_tx(w3: Web3, tx, account: LocalAccount) -> bytes:
    tx['from'] = account.address
    if 'nonce' not in tx:
        tx['nonce'] = w3.eth.getTransactionCount(account.address, block_identifier='pending')

    if 'gasPrice' not in tx:
        tx['gasPrice'] = w3.eth.gasPrice

    if 'gas' not in tx:
        tx['gas'] = w3.eth.estimateGas(tx)
    else:
        tx['gas'] *= 2

    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.sendRawTransaction(bytes(signed_tx.rawTransaction))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert tx_receipt.status == 1, 'Error with tx %s - %s' % (tx_hash.hex(), tx)
    return tx_hash


def deploy_example_erc20(w3, amount: int, owner: str, deployer: str=None, account: LocalAccount=None):
    if account:
        erc20_contract = get_example_erc20_contract(w3)
        tx = erc20_contract.constructor(amount, owner).buildTransaction()
        if 'nonce' not in tx:
            tx['nonce'] = w3.eth.getTransactionCount(account.address, block_identifier='pending')
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        erc20_address = tx_receipt.contractAddress
        deployed_erc20 = get_example_erc20_contract(w3, erc20_address)
        assert deployed_erc20.functions.balanceOf(owner).call() == amount
        return deployed_erc20

    deployer = deployer or w3.eth.accounts[0]
    erc20_contract = get_example_erc20_contract(w3)
    tx_hash = erc20_contract.constructor(amount, owner).transact({'from': deployer})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    erc20_address = tx_receipt.contractAddress
    deployed_erc20 = get_example_erc20_contract(w3, erc20_address)
    assert deployed_erc20.functions.balanceOf(owner).call() == amount
    return deployed_erc20
