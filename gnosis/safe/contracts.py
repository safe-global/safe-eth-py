from hexbytes import HexBytes
from web3 import Web3

from .abis import load_contract_interface

"""
Rinkeby contracts https://github.com/gnosis/safe-contracts/releases/tag/v0.0.1
-----------------
ProxyFactory: 0x075794c3797bb4cfea74a75d1aae636036af37cd
GnosisSafe: 0xC65f75fbFFb1628293F9320168500ed336CF3E24
DailyLimitModule: 0xac94a500b707fd5c4cdb89777f29b3b28bde2f0c
CreateAndAddModules: 0x8513246e65c474ad05e88ae8ca7c5a6b04246550
MultiSend: 0x7830ceb6f513568c05bd995d0767cceea2ef9662
"""

GNOSIS_SAFE_OWNER_MANAGER_INTERFACE = load_contract_interface('GnosisSafeOwnerManager.json')
GNOSIS_SAFE_INTERFACE = load_contract_interface('GnosisSafe.json')
PAYING_PROXY_INTERFACE = load_contract_interface('PayingProxy.json')


def get_safe_contract(w3: Web3, address=None):
    """
    Get Safe Personal Contract. It should be used to access Safe methods on Proxy contracts.
    :param w3: Web3 instance
    :param address: address of the safe contract/proxy contract
    :return: Safe Contract
    """
    return w3.eth.contract(address,
                           abi=GNOSIS_SAFE_INTERFACE['abi'],
                           bytecode=GNOSIS_SAFE_INTERFACE['bytecode'])


def get_safe_owner_manager_contract(w3: Web3, address=None):
    """
    Get Safe Contract - OwnerManager class.
    :param w3: Web3 instance
    :param address: address of the safe contract/proxy contract
    :return: Safe Contract
    """
    return w3.eth.contract(Web3.toChecksumAddress(address),
                           abi=GNOSIS_SAFE_OWNER_MANAGER_INTERFACE['abi'],
                           bytecode=GNOSIS_SAFE_OWNER_MANAGER_INTERFACE['bytecode'])


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


def get_paying_proxy_deployed_bytecode() -> bytes:
    return HexBytes(PAYING_PROXY_INTERFACE['deployedBytecode'])
