from logging import getLogger
from typing import Optional

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress

from gnosis.eth import EthereumClient, EthereumTxSent
from gnosis.eth.contract_common import ContractCommon
from gnosis.eth.contracts import (
    get_paying_proxy_deployed_bytecode,
    get_proxy_1_0_0_deployed_bytecode,
    get_proxy_1_1_1_deployed_bytecode,
    get_proxy_1_1_1_mainnet_deployed_bytecode,
    get_proxy_1_3_0_deployed_bytecode,
    get_proxy_factory_contract,
    get_proxy_factory_V1_0_0_contract,
    get_proxy_factory_V1_1_1_contract,
    get_proxy_factory_V1_3_0_contract,
)
from gnosis.eth.utils import compare_byte_code, fast_is_checksum_address
from gnosis.util import cache

logger = getLogger(__name__)


class ProxyFactory(ContractCommon):
    def __init__(self, address: ChecksumAddress, ethereum_client: EthereumClient):
        assert fast_is_checksum_address(address), (
            "%s proxy factory address not valid" % address
        )
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.address = address

    @classmethod
    def deploy_proxy_factory_contract(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy proxy factory contract last version (v1.3.0)

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        return cls.deploy_proxy_factory_contract_v1_3_0(
            ethereum_client, deployer_account
        )

    @classmethod
    def deploy_proxy_factory_contract_v1_3_0(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy proxy factory contract v1.3.0

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        proxy_factory_contract = get_proxy_factory_V1_3_0_contract(ethereum_client.w3)
        return cls.deploy_contract(
            ethereum_client, deployer_account, proxy_factory_contract
        )

    @classmethod
    def deploy_proxy_factory_contract_v1_1_1(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy proxy factory contract v1.1.1

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        proxy_factory_contract = get_proxy_factory_V1_1_1_contract(ethereum_client.w3)
        return cls.deploy_contract(
            ethereum_client, deployer_account, proxy_factory_contract
        )

    @classmethod
    def deploy_proxy_factory_contract_v1_0_0(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy proxy factory contract v1.0.0

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        proxy_factory_contract = get_proxy_factory_V1_0_0_contract(ethereum_client.w3)
        return cls.deploy_contract(
            ethereum_client, deployer_account, proxy_factory_contract
        )

    def check_proxy_code(self, address: ChecksumAddress) -> bool:
        """
        Check if proxy is valid
        :param address: Ethereum address to check
        :return: True if proxy is valid, False otherwise
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

    def deploy_proxy_contract(
        self,
        deployer_account: LocalAccount,
        master_copy: ChecksumAddress,
        initializer: bytes = b"",
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
    ) -> EthereumTxSent:
        """
        Deploy proxy contract via ProxyFactory using `createProxy` function
        :param deployer_account: Ethereum account
        :param master_copy: Address the proxy will point at
        :param initializer: Initializer
        :param gas: Gas
        :param gas_price: Gas Price
        :return: EthereumTxSent
        """
        proxy_factory_contract = self.get_contract()
        create_proxy_fn = proxy_factory_contract.functions.createProxy(
            master_copy, initializer
        )

        tx_parameters = self.configure_tx_parameters(
            deployer_account.address, gas, gas_price
        )
        # Auto estimation of gas does not work. We use a little more gas just in case (gas_increment)
        return self.deploy_contract_with_deploy_function(
            self.ethereum_client, deployer_account, create_proxy_fn, tx_parameters
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
        Deploy proxy contract via Proxy Factory using `createProxyWithNonce` (create2)

        :param deployer_account: Ethereum account
        :param master_copy: Address the proxy will point at
        :param initializer: Data for safe creation
        :param salt_nonce: Uint256 for `create2` salt
        :param gas: Gas
        :param gas_price: Gas Price
        :param nonce: Nonce
        :return: Tuple(tx-hash, tx, deployed contract address)
        """
        proxy_factory_contract = self.get_contract()
        create_proxy_fn = proxy_factory_contract.functions.createProxyWithNonce(
            master_copy, initializer, salt_nonce
        )

        tx_parameters = self.configure_tx_parameters(
            deployer_account.address, gas, gas_price, nonce
        )
        # Auto estimation of gas does not work. We use a little more gas just in case (gas_increment)
        return self.deploy_contract_with_deploy_function(
            self.ethereum_client,
            deployer_account,
            create_proxy_fn,
            tx_parameters,
            gas_increment=50000,
        )

    def get_contract(self, address: Optional[ChecksumAddress] = None):
        address = address or self.address
        return get_proxy_factory_contract(self.ethereum_client.w3, address)

    @cache
    def get_proxy_runtime_code(self, address: Optional[ChecksumAddress] = None):
        """
        Get runtime code for current proxy factory
        """
        address = address or self.address
        return self.get_contract(address=address).functions.proxyRuntimeCode().call()
