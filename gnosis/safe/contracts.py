from hexbytes import HexBytes
from web3 import Web3

from .abis import load_contract_interface

"""
Rinkeby contracts https://github.com/gnosis/safe-contracts/releases/tag/v0.0.2-alpha
-----------------
Safes
GnosisSafe: 0x2727d69c0bd14b1ddd28371b8d97e808adc1c2f7

Factories
ProxyFactory: 0xf81e35398b5d09d891db0199064ff4a53e7ecae6

Libraries
CreateAndAddModules: 0x5096cd7f7f5f2e621a480c1ae8969c03cb647a91
MultiSend: 0x607ecc85c613548367ebdee103d6d256d42d5978

Modules
StateChannelModule: 0x46060a29a9ea946b2e37058288e029554a9d73c8
DailyLimitModule: 0x6e3a1f364c112736ca88ea113b70dcae53a4def6
SocialRecoveryModule: 0x96967d1f6bade086b8e31f04b14753f9649b3d9e
WhitelistModule: 0xbb2d70bafda6dd0f8770713b71e7fecf74adfd95
"""

GNOSIS_SAFE_INTERFACE = load_contract_interface('GnosisSafe.json')
PAYING_PROXY_INTERFACE = load_contract_interface('PayingProxy.json')
ERC20_INTERFACE = load_contract_interface('ERC20.json')
ERC20_EXAMPLE_INTERFACE = load_contract_interface('ERC20TestToken.json')


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


def get_paying_proxy_deployed_bytecode() -> bytes:
    return HexBytes(PAYING_PROXY_INTERFACE['deployedBytecode'])
