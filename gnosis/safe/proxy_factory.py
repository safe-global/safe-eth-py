from logging import getLogger
from typing import Optional

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract

from gnosis.eth import EthereumClient
from gnosis.eth.contracts import (get_paying_proxy_deployed_bytecode,
                                  get_proxy_1_0_0_deployed_bytecode,
                                  get_proxy_factory_contract,
                                  get_proxy_factory_V1_0_0_contract)
from gnosis.eth.ethereum_client import EthereumTxSent
from gnosis.eth.utils import compare_byte_code

logger = getLogger(__name__)


class ProxyFactory:
    proxy_runtime_code: Optional[bytes] = None  # Cache runtime code

    def __init__(self, address: str, ethereum_client: EthereumClient):
        assert Web3.isChecksumAddress(address), \
            '%s proxy factory address not valid' % address

        self.address = address
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    @staticmethod
    def _deploy_proxy_factory_contract(ethereum_client: EthereumClient,
                                       deployer_account: LocalAccount, contract: Contract) -> EthereumTxSent:
        tx = contract.constructor().buildTransaction({'from': deployer_account.address})

        tx_hash = ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.key)
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=120)
        assert tx_receipt
        assert tx_receipt['status']
        contract_address = tx_receipt['contractAddress']
        logger.info("Deployed and initialized Proxy Factory Contract=%s by %s", contract_address,
                    deployer_account.address)
        return EthereumTxSent(tx_hash, tx, contract_address)

    @classmethod
    def deploy_proxy_factory_contract(cls, ethereum_client: EthereumClient,
                                      deployer_account: LocalAccount) -> EthereumTxSent:
        """
        Deploy proxy factory contract
        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        proxy_factory_contract = get_proxy_factory_contract(ethereum_client.w3)
        return cls._deploy_proxy_factory_contract(ethereum_client, deployer_account, proxy_factory_contract)

    @classmethod
    def deploy_proxy_factory_contract_v1_0_0(cls, ethereum_client: EthereumClient,
                                             deployer_account: LocalAccount) -> EthereumTxSent:
        """
        Deploy proxy factory contract
        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: deployed contract address
        """
        proxy_factory_contract = get_proxy_factory_V1_0_0_contract(ethereum_client.w3)
        return cls._deploy_proxy_factory_contract(ethereum_client, deployer_account, proxy_factory_contract)

    def check_proxy_code(self, address: ChecksumAddress) -> bool:
        """
        Check if proxy is valid
        :param address: Ethereum address to check
        :return: True if proxy is valid, False otherwise
        """

        deployed_proxy_code = self.w3.eth.get_code(address)
        proxy_code_fns = (get_paying_proxy_deployed_bytecode,
                          get_proxy_1_0_0_deployed_bytecode,
                          self.get_proxy_runtime_code)
        for proxy_code_fn in proxy_code_fns:
            if compare_byte_code(deployed_proxy_code, proxy_code_fn()):
                return True
        return False

    def deploy_proxy_contract(self, deployer_account: LocalAccount, master_copy: str, initializer: bytes = b'',
                              gas: Optional[int] = None, gas_price: Optional[int] = None) -> EthereumTxSent:
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
        create_proxy_fn = proxy_factory_contract.functions.createProxy(master_copy, initializer)

        tx_parameters = {
            'from': deployer_account.address
        }
        contract_address = create_proxy_fn.call(tx_parameters)

        if gas_price is not None:
            tx_parameters['gasPrice'] = gas_price

        if gas is not None:
            tx_parameters['gas'] = gas

        tx = create_proxy_fn.buildTransaction(tx_parameters)
        # Auto estimation of gas does not work. We use a little more gas just in case
        tx['gas'] = tx['gas'] + 50000
        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.key)
        return EthereumTxSent(tx_hash, tx, contract_address)

    def deploy_proxy_contract_with_nonce(self, deployer_account: LocalAccount, master_copy: str,
                                         initializer: bytes, salt_nonce: int,
                                         gas: Optional[int] = None, gas_price: Optional[int] = None,
                                         nonce: Optional[int] = None) -> EthereumTxSent:
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
        create_proxy_fn = proxy_factory_contract.functions.createProxyWithNonce(master_copy, initializer, salt_nonce)

        tx_parameters = {
            'from': deployer_account.address
        }
        contract_address = create_proxy_fn.call(tx_parameters)

        if gas_price is not None:
            tx_parameters['gasPrice'] = gas_price

        if gas is not None:
            tx_parameters['gas'] = gas

        if nonce is not None:
            tx_parameters['nonce'] = nonce

        tx = create_proxy_fn.buildTransaction(tx_parameters)
        # Auto estimation of gas does not work. We use a little more gas just in case
        tx['gas'] = tx['gas'] + 50000
        tx_hash = self.ethereum_client.send_unsigned_transaction(tx, private_key=deployer_account.key)
        return EthereumTxSent(tx_hash, tx, contract_address)

    def get_contract(self):
        return get_proxy_factory_contract(self.ethereum_client.w3, self.address)

    def get_proxy_runtime_code(self):
        if not self.proxy_runtime_code:
            self.proxy_runtime_code = self.get_contract().functions.proxyRuntimeCode().call()
        return self.proxy_runtime_code
