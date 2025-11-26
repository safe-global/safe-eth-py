from abc import ABCMeta
from typing import Callable, Optional

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract.contract import Contract

from safe_eth.eth import EthereumClient, EthereumTxSent
from safe_eth.eth.contracts import (
    ContractBase,
    get_extensible_fallback_handler_V1_5_0_contract,
)
from safe_eth.eth.utils import get_empty_tx_params


class ExtensibleFallbackHandler(ContractBase, metaclass=ABCMeta):
    def __new__(
        cls, *args, version: str = "1.5.0", **kwargs
    ) -> "ExtensibleFallbackHandler":
        if cls is not ExtensibleFallbackHandler:
            return super().__new__(cls)

        versions = {
            "1.5.0": ExtensibleFallbackHandlerV150,
        }
        instance_class = versions[version]
        instance = super().__new__(instance_class)
        return instance

    @classmethod
    def deploy_contract(
        cls, ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy Extensible Fallback Handler contract

        :param ethereum_client:
        :param deployer_account: Ethereum Account
        :return: ``EthereumTxSent`` with the deployed contract address
        """
        contract_fn = cls.get_contract_fn(cls)  # type: ignore[arg-type]
        contract = contract_fn(ethereum_client.w3, None)
        constructor_data = contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]
        return ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data
        )


class ExtensibleFallbackHandlerV150(ExtensibleFallbackHandler):
    def get_contract_fn(self) -> Callable[[Web3, Optional[ChecksumAddress]], Contract]:
        return get_extensible_fallback_handler_V1_5_0_contract
