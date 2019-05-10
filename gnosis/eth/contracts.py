import sys
from typing import Dict, Optional

from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.abis import load_contract_interface

current_module = sys.modules[__name__]

"""
Safe Addresses. Should be the same for every chain. Check:
https://github.com/gnosis/safe-contracts/blob/development/zos.mainnet.json
https://github.com/gnosis/safe-contracts/blob/development/zos.rinkeby.json

GnosisSafe: 0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A

Factories
ProxyFactory: 0x12302fE9c02ff50939BaAaaf415fc226C078613C

Libraries
CreateAndAddModules: 0x1a56aE690ab0818aF5cA349b7D21f1d7e76a3d36
MultiSend: 0xD4B7B161E4779629C2717385114Bf78D612aEa72
"""

contracts = {
    'safe': 'GnosisSafe.json',
    'old_safe': 'OldGnosisSafe.json',
    'erc20': 'ERC20.json',
    'erc721': 'ERC721.json',
    'example_erc20': 'ERC20TestToken.json',
    'delegate_constructor_proxy': 'DelegateConstructorProxy.json',
    'paying_proxy': 'PayingProxy.json',
    'proxy_factory': 'ProxyFactory.json',
    'proxy': 'Proxy.json',
}


def generate_contract_fn(contract: Dict[str, any]):
    """
    Dynamically generate functions to work with the contracts
    :param json_contract_filename:
    :return:
    """
    def fn(w3: Web3, address: Optional[str] = None):
        return w3.eth.contract(address,
                               abi=contract['abi'],
                               bytecode=contract['bytecode'])
    return fn


for contract_name, json_contract_filename in contracts.items():
    fn_name = 'get_{}_contract'.format(contract_name)
    contract_dict = load_contract_interface(json_contract_filename)
    setattr(current_module, fn_name, generate_contract_fn(contract_dict))


def get_paying_proxy_deployed_bytecode() -> bytes:
    return HexBytes(load_contract_interface('PayingProxy.json')['deployedBytecode'])
