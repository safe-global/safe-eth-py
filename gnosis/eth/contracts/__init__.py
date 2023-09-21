# flake8: noqa F401
"""
Safe Addresses. Should be the same for every chain except for the ones with `chainId` protection. Check:
https://github.com/safe-global/safe-deployments/tree/main/src/assets

Safe V1.4.1: 0x41675C099F32341bf84BFc5382aF534df5C7461a
GnosisSafe V1.3.0: 0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552
GnosisSafe V1.1.1: 0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F
GnosisSafe V1.1.0: 0xaE32496491b53841efb51829d6f886387708F99B
GnosisSafe V1.0.0: 0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A

Factories
SafeProxyFactory V1.4.1: 0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67
ProxyFactory V1.3.0: 0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2
ProxyFactory V1.1.0: 0x50e55Af101C777bA7A1d560a774A82eF002ced9F
ProxyFactory V1.0.0: 0x12302fE9c02ff50939BaAaaf415fc226C078613C

FallbackHandler
CompatibilityFallBackHandler V1.4.1: 0xfd0732Dc9E303f09fCEf3a7388Ad10A83459Ec99
CompatibilityFallBackHandler V1.3.0: 0xf48f2B2d2a534e402487b3ee7C18c33Aec0Fe5e4

Libraries
CreateAndAddModules: 0x1a56aE690ab0818aF5cA349b7D21f1d7e76a3d36
MultiSend: 0x38869bf66a61cF6bDB996A6aE40D5853Fd43B526
MultiSendCallOnly: 0x9641d764fc13c8B624c04430C7356C1C7C8102e2
SimulateTxAccessor: 0x3d4BA2E0884aa488718476ca2FB8Efc291A46199
SignMessageLib: 0xd53cd0aB83D845Ac265BE939c57F53AD838012c9
"""

import json
import os
import sys
from typing import Any, Callable, Dict, Optional

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract

from gnosis.util import cache

from .abis.multicall import multicall_v3_abi, multicall_v3_bytecode
from .contract_base import ContractBase

current_module = sys.modules[__name__]
contracts = {
    "compatibility_fallback_handler_V1_3_0": "CompatibilityFallbackHandler_V1_3_0.json",
    "compatibility_fallback_handler_V1_4_1": "CompatibilityFallbackHandler_V1_4_1.json",
    "cpk_factory": "CPKFactory.json",
    "delegate_constructor_proxy": "DelegateConstructorProxy.json",
    "erc1155": "ERC1155.json",
    "erc20": "ERC20.json",
    "erc721": "ERC721.json",
    "example_erc20": "ERC20TestToken.json",
    "kyber_network_proxy": "kyber_network_proxy.json",
    "multi_send": "MultiSend.json",
    "paying_proxy": "PayingProxy.json",
    "proxy": "Proxy_V1_1_1.json",
    "proxy_factory_V1_0_0": "ProxyFactory_V1_0_0.json",
    "proxy_factory_V1_1_1": "ProxyFactory_V1_1_1.json",
    "proxy_factory_V1_3_0": "ProxyFactory_V1_3_0.json",
    "proxy_factory_V1_4_1": "ProxyFactory_V1_4_1.json",
    "safe_V0_0_1": "GnosisSafe_V0_0_1.json",
    "safe_V1_0_0": "GnosisSafe_V1_0_0.json",
    "safe_V1_1_1": "GnosisSafe_V1_1_1.json",
    "safe_V1_3_0": "GnosisSafe_V1_3_0.json",
    "safe_V1_4_1": "Safe_V1_4_1.json",
    "simulate_tx_accessor_V1_4_1": "SimulateTxAccessor_V1_4_1.json",
    "uniswap_exchange": "uniswap_exchange.json",
    "uniswap_factory": "uniswap_factory.json",
    "uniswap_v2_factory": "uniswap_v2_factory.json",
    "uniswap_v2_pair": "uniswap_v2_pair.json",
    "uniswap_v2_router": "uniswap_v2_router.json",  # Router02
}


def load_contract_interface(file_name: str) -> Dict[str, Any]:
    """
    :param file_name:
    :return: Get parsed JSON to ABI with the relative filename to this file path
    """
    return _load_json_file(_abi_file_path(file_name))


def _abi_file_path(file_name: str) -> str:
    """
    :param file_name:
    :return: Full path to the provided ``file_name``
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "abis", file_name))


def _load_json_file(path) -> Dict[str, Any]:
    """
    :param path:
    :return: Parsed json for the provided file
    """
    with open(path) as f:
        return json.load(f)


def generate_contract_fn(
    contract: Dict[str, Any]
) -> Callable[[Web3, Optional[ChecksumAddress]], Contract]:
    """
    Dynamically generate a function to build a Web3 Contract for the provided contract ABI

    :param contract:
    :return: function that will return a Web3 Contract from an ABI
    """

    def fn(w3: Web3, address: Optional[ChecksumAddress] = None) -> Contract:
        return w3.eth.contract(
            address=address, abi=contract["abi"], bytecode=contract.get("bytecode")
        )

    return fn


# Anotate functions that will be generated later with `setattr` so typing does not complain
def get_safe_contract(w3: Web3, address: Optional[ChecksumAddress] = None) -> Contract:
    """
    :param w3:
    :param address:
    :return: Latest available Safe Contract
    """
    return get_safe_V1_4_1_contract(w3, address=address)


def get_safe_V0_0_1_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_safe_V1_0_0_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_safe_V1_1_1_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_safe_V1_3_0_contract(w3: Web3, address: Optional[str] = None) -> Contract:
    pass


def get_safe_V1_4_1_contract(w3: Web3, address: Optional[str] = None) -> Contract:
    pass


def get_compatibility_fallback_handler_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    """
    :param w3:
    :param address: Usually a Safe address
    :return: Latest available Compatibility Fallback handler contract
    """
    return get_compatibility_fallback_handler_V1_4_1_contract(w3, address=address)


def get_compatibility_fallback_handler_V1_3_0_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_compatibility_fallback_handler_V1_4_1_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_erc20_contract(w3: Web3, address: Optional[ChecksumAddress] = None) -> Contract:
    pass


def get_erc721_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_erc1155_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_example_erc20_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_delegate_constructor_proxy_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_multi_send_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_paying_proxy_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_proxy_factory_contract(w3: Web3, address: Optional[str] = None) -> Contract:
    """
    :param w3:
    :param address:
    :return: Latest available Safe Proxy Factory
    """
    return get_proxy_factory_V1_4_1_contract(w3, address=address)


def get_proxy_factory_V1_0_0_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_proxy_factory_V1_1_1_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_proxy_factory_V1_3_0_contract(
    w3: Web3, address: Optional[str] = None
) -> Contract:
    pass


def get_proxy_factory_V1_4_1_contract(
    w3: Web3, address: Optional[str] = None
) -> Contract:
    pass


def get_proxy_contract(w3: Web3, address: Optional[ChecksumAddress] = None) -> Contract:
    pass


def get_simulate_tx_accessor_V1_4_1_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_uniswap_exchange_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_uniswap_factory_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_uniswap_v2_factory_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_uniswap_v2_pair_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_uniswap_v2_router_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_kyber_network_proxy_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_cpk_factory_contract(
    w3: Web3, address: Optional[ChecksumAddress] = None
) -> Contract:
    pass


def get_multicall_v3_contract(w3: Web3, address: Optional[ChecksumAddress] = None):
    return w3.eth.contract(
        address=address,
        abi=multicall_v3_abi,
        bytecode=multicall_v3_bytecode,
    )


@cache
def get_proxy_1_0_0_deployed_bytecode() -> bytes:
    return HexBytes(load_contract_interface("Proxy_V1_0_0.json")["deployedBytecode"])


@cache
def get_proxy_1_1_1_deployed_bytecode() -> bytes:
    return HexBytes(load_contract_interface("Proxy_V1_1_1.json")["deployedBytecode"])


def get_proxy_1_1_1_mainnet_deployed_bytecode() -> bytes:
    """
    Somehow it's different from the generated version compiling the contracts
    """
    return HexBytes(
        "0x608060405273ffffffffffffffffffffffffffffffffffffffff600054167fa619486e0000000000000000000000000000000000000000000000000000000060003514156050578060005260206000f35b3660008037600080366000845af43d6000803e60008114156070573d6000fd5b3d6000f3fea265627a7a72315820d8a00dc4fe6bf675a9d7416fc2d00bb3433362aa8186b750f76c4027269667ff64736f6c634300050e0032"
    )


@cache
def get_proxy_1_3_0_deployed_bytecode() -> bytes:
    return HexBytes(load_contract_interface("Proxy_V1_3_0.json")["deployedBytecode"])


@cache
def get_proxy_1_4_1_deployed_bytecode() -> bytes:
    return HexBytes(load_contract_interface("Proxy_V1_4_1.json")["deployedBytecode"])


@cache
def get_paying_proxy_deployed_bytecode() -> bytes:
    return HexBytes(load_contract_interface("PayingProxy.json")["deployedBytecode"])


# Dynamically create the functions for getting the contracts
for contract_name, json_contract_filename in contracts.items():
    fn_name = "get_{}_contract".format(contract_name)
    contract_dict = load_contract_interface(json_contract_filename)
    if not contract_dict:
        raise ValueError(f"{contract_name} json cannot be empty")
    setattr(current_module, fn_name, generate_contract_fn(contract_dict))
