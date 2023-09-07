from abc import ABCMeta, abstractmethod
from functools import cached_property
from typing import Callable, Optional

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract.contract import Contract, ContractFunction

from gnosis.eth import EthereumClient, EthereumTxSent
from gnosis.eth.contracts import (
    get_paying_proxy_deployed_bytecode,
    get_proxy_1_0_0_deployed_bytecode,
    get_proxy_1_1_1_deployed_bytecode,
    get_proxy_1_1_1_mainnet_deployed_bytecode,
    get_proxy_1_3_0_deployed_bytecode,
    get_proxy_factory_V1_0_0_contract,
    get_proxy_factory_V1_1_1_contract,
    get_proxy_factory_V1_3_0_contract,
)
from gnosis.eth.contracts.contract_common import ContractCommon
from gnosis.eth.utils import compare_byte_code, fast_is_checksum_address
from gnosis.util import cache


class ProxyFactoryBase(ContractCommon, metaclass=ABCMeta):
    def __init__(self, address: ChecksumAddress, ethereum_client: EthereumClient):
        assert fast_is_checksum_address(address), (
            "%s proxy factory address not valid" % address
        )
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.address = address

    @abstractmethod
    def get_contract_fn(self) -> Callable[[Web3, ChecksumAddress], Contract]:
        """
        :return: Contract function to get the proper ProxyFactory contract
        """
        raise NotImplementedError

    @cached_property
    def contract(self):
        return self.get_contract_fn()(self.ethereum_client.w3, self.address)

    def check_proxy_code(self, address: ChecksumAddress) -> bool:
        """
        Check if proxy bytecode matches any of the deployed by the supported Proxy Factories

        :param address: Ethereum address to check
        :return: ``True`` if proxy is valid, ``False`` otherwise
        """

        deployed_proxy_code = self.w3.eth.get_code(address)
        proxy_code_fns = (
            get_proxy_1_3_0_deployed_bytecode,
            get_proxy_1_1_1_deployed_bytecode,
            get_proxy_1_1_1_mainnet_deployed_bytecode,
            get_proxy_1_0_0_deployed_bytecode,
            get_paying_proxy_deployed_bytecode,
            self.get_proxy_runtime_code,
        )
        for proxy_code_fn in proxy_code_fns:
            if compare_byte_code(deployed_proxy_code, proxy_code_fn()):
                return True
        return False

    def _deploy_proxy_contract(
        self,
        deployer_account: LocalAccount,
        deploy_fn: ContractFunction,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
    ) -> EthereumTxSent:
        """
        Common logic for `createProxy` and `createProxyWithNonce`

        :param deployer_account:
        :param deploy_fn:
        :param gas:
        :param gas_price:
        :param nonce:
        :return: EthereumTxSent
        """

        tx_params = self.configure_tx_parameters(
            deployer_account.address, gas=gas, gas_price=gas_price, nonce=nonce
        )
        contract_address = deploy_fn.call(tx_params)
        tx = deploy_fn.build_transaction(tx_params)
        tx_hash = self.ethereum_client.send_unsigned_transaction(
            tx, private_key=deployer_account.key
        )

        return EthereumTxSent(tx_hash, tx, contract_address)

    def deploy_proxy_contract(
        self,
        deployer_account: LocalAccount,
        master_copy: ChecksumAddress,
        initializer: bytes = b"",
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
    ) -> EthereumTxSent:
        """
        Deploy proxy contract via ProxyFactory using `createProxy` function (CREATE opcode)

        :param deployer_account: Ethereum account
        :param master_copy: Address the proxy will point at
        :param initializer: Initializer for the deployed proxy
        :param gas: Gas
        :param gas_price: Gas Price
        :param nonce: Nonce
        :return: EthereumTxSent
        """
        create_proxy_fn = self.contract.functions.createProxy(master_copy, initializer)

        return self._deploy_proxy_contract(
            deployer_account, create_proxy_fn, gas=gas, gas_price=gas_price, nonce=nonce
        )

    def deploy_proxy_contract_with_nonce(
        self,
        deployer_account: LocalAccount,
        master_copy: ChecksumAddress,
        initializer: bytes,
        salt_nonce: int,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
    ) -> EthereumTxSent:
        """
        Deploy proxy contract via Proxy Factory using `createProxyWithNonce` (CREATE2 opcode)

        :param deployer_account: Ethereum account
        :param master_copy: Address the proxy will point at
        :param initializer: Initializer for the deployed proxy
        :param salt_nonce: Uint256 for ``CREATE2`` salt
        :param gas: Gas
        :param gas_price: Gas Price
        :param nonce: Nonce
        :return: EthereumTxSent
        """
        create_proxy_fn = self.contract.functions.createProxyWithNonce(
            master_copy, initializer, salt_nonce
        )

        return self._deploy_proxy_contract(
            deployer_account, create_proxy_fn, gas=gas, gas_price=gas_price, nonce=nonce
        )

    @classmethod
    def deploy_proxy_factory_contract(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy Proxy Factory contract

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        proxy_factory_contract = cls.get_contract_fn(cls)(ethereum_client.w3)
        constructor_data = proxy_factory_contract.constructor().build_transaction(
            {"gas": 0, "gasPrice": 0}
        )["data"]
        return ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data
        )

    @cache
    def get_proxy_runtime_code(self):
        """
        Get runtime code for current proxy factory
        """
        return self.contract.functions.proxyRuntimeCode().call()


class ProxyFactoryV100(ProxyFactoryBase):
    def get_contract_fn(self) -> Callable[[Web3, ChecksumAddress], Contract]:
        return get_proxy_factory_V1_0_0_contract


class ProxyFactoryV111(ProxyFactoryBase):
    def get_contract_fn(self) -> Callable[[Web3, ChecksumAddress], Contract]:
        return get_proxy_factory_V1_1_1_contract


class ProxyFactoryV130(ProxyFactoryBase):
    def get_contract_fn(self) -> Callable[[Web3, ChecksumAddress], Contract]:
        return get_proxy_factory_V1_3_0_contract


class ProxyFactory:
    versions = {
        "1.0.0": ProxyFactoryV100,
        "1.1.1": ProxyFactoryV111,
        "1.3.0": ProxyFactoryV130,
    }

    def __new__(
        cls,
        address: ChecksumAddress,
        ethereum_client: EthereumClient,
        version: str = "1.3.0",
    ):
        # Return default version 1.3.0
        proxy_factory_version = cls.versions.get(version, ProxyFactoryV130)
        instance = super().__new__(proxy_factory_version)
        instance.__init__(address, ethereum_client)
        return instance
