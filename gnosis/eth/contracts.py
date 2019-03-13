from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.abis import load_contract_interface

"""
Safe Addresses. Should be the same for every chain. Check:
https://github.com/gnosis/safe-contracts/blob/development/zos.mainnet.json
https://github.com/gnosis/safe-contracts/blob/development/zos.rinkeby.json

GnosisSafe: 0x8942595a2dc5181df0465af0d7be08c8f23c93af

Factories
ProxyFactory: 0x88cd603a5dc47857d02865bbc7941b588c533263

Libraries
CreateAndAddModules: 0xcbf223ccb3264e447167d4772c312df403ab87f0
MultiSend: 0xe74d6af1670fb6560dd61ee29eb57c7bc027ce4e
"""

GNOSIS_SAFE_INTERFACE = load_contract_interface('GnosisSafe.json')
OLD_GNOSIS_SAFE_INTERFACE = load_contract_interface('OldGnosisSafe.json')
ERC20_INTERFACE = load_contract_interface('ERC20.json')
ERC20_EXAMPLE_INTERFACE = load_contract_interface('ERC20TestToken.json')
PAYING_PROXY_INTERFACE = load_contract_interface('PayingProxy.json')
PROXY_FACTORY_INTERFACE = load_contract_interface('ProxyFactory2.json')


def get_safe_contract(w3: Web3, address=None):
    """
    Get Gnosis Safe Master contract. It should be used to access Safe methods on Proxy contracts.
    :param w3: Web3 instance
    :param address: address of the safe contract/proxy contract
    :return: Safe Contract
    """
    return w3.eth.contract(address,
                           abi=GNOSIS_SAFE_INTERFACE['abi'],
                           bytecode=GNOSIS_SAFE_INTERFACE['bytecode'])


def get_old_safe_contract(w3: Web3, address=None):
    """
    Get Old Gnosis Safe Master contract. It should be used to access Safe methods on Proxy contracts.
    :param w3: Web3 instance
    :param address: address of the safe contract/proxy contract
    :return: Safe Contract
    """
    return w3.eth.contract(address,
                           abi=OLD_GNOSIS_SAFE_INTERFACE['abi'],
                           bytecode=OLD_GNOSIS_SAFE_INTERFACE['bytecode'])


def get_paying_proxy_contract(w3: Web3, address=None):
    """
    Get Paying Proxy Contract. This should be used just for contract creation/changing master_copy
    If you want to call Safe methods you should use `get_safe_contract` with the Proxy address,
    so you can access every method of the Safe
    :param w3: Web3 instance
    :param address: address of the proxy contract
    :return: Paying Proxy Contract
    """
    return w3.eth.contract(address,
                           abi=PAYING_PROXY_INTERFACE['abi'],
                           bytecode=PAYING_PROXY_INTERFACE['bytecode'])


def get_erc20_contract(w3: Web3, address=None):
    """
    Get ERC20 interface
    :param w3: Web3 instance
    :param address: address of the proxy contract
    :return: ERC 20 contract
    """
    return w3.eth.contract(address,
                           abi=ERC20_INTERFACE['abi'],
                           bytecode=ERC20_INTERFACE['bytecode'])


def get_example_erc20_contract(w3: Web3, address=None):
    return w3.eth.contract(address,
                           abi=ERC20_EXAMPLE_INTERFACE['abi'],
                           bytecode=ERC20_EXAMPLE_INTERFACE['bytecode'])


def get_proxy_factory_contract(w3: Web3, address=None):
    return w3.eth.contract(address,
                           abi=PROXY_FACTORY_INTERFACE['abi'],
                           bytecode=PROXY_FACTORY_INTERFACE['bytecode'])


def get_paying_proxy_deployed_bytecode() -> bytes:
    return HexBytes(PAYING_PROXY_INTERFACE['deployedBytecode'])
