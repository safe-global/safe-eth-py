from ..contracts import get_example_erc20_contract


def deploy_example_erc20(w3, amount: int, owner: str, deployer: str=None):
    deployer = deployer or w3.eth.accounts[0]
    erc20_contract = get_example_erc20_contract(w3)
    tx_hash = erc20_contract.constructor(amount, owner).transact({'from': deployer})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    erc20_address = tx_receipt.contractAddress
    deployed_erc20 = get_example_erc20_contract(w3, erc20_address)
    return deployed_erc20
