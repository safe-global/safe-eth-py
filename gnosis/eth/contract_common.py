from logging import getLogger
from typing import Optional

from eth_account.signers.local import LocalAccount
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import TxParams

from gnosis.eth import EthereumClient, EthereumTxSent

logger = getLogger(__name__)


class ContractCommon:
    @staticmethod
    def deploy_contract(
        ethereum_client: EthereumClient,
        deployer_account: LocalAccount,
        contract: Contract,
    ) -> EthereumTxSent:
        tx = contract.constructor().build_transaction(
            {"from": deployer_account.address}
        )

        tx_hash = ethereum_client.send_unsigned_transaction(
            tx, private_key=deployer_account.key
        )
        tx_receipt = ethereum_client.get_transaction_receipt(
            tx_hash, timeout=ethereum_client.slow_timeout
        )
        assert tx_receipt
        assert tx_receipt["status"]
        contract_address = tx_receipt["contractAddress"]
        logger.info(
            "Deployed Contract=%s by %s",
            contract_address,
            deployer_account.address,
        )
        return EthereumTxSent(tx_hash, tx, contract_address)

    @staticmethod
    def deploy_contract_with_deploy_function(
        ethereum_client: EthereumClient,
        deployer_account: LocalAccount,
        deploy_function: ContractFunction,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
        gas_increment: Optional[int] = None,
    ):

        tx_parameters = ContractCommon.configure_tx_parameters(
            deployer_account.address, gas, gas_price, nonce
        )

        contract_address = deploy_function.call(tx_parameters)

        tx = deploy_function.build_transaction(tx_parameters)
        # Adjust gas
        if gas_increment:
            tx["gas"] = tx["gas"] + gas_increment

        tx_hash = ethereum_client.send_unsigned_transaction(
            tx, private_key=deployer_account.key
        )
        return EthereumTxSent(tx_hash, tx, contract_address)

    @staticmethod
    def configure_tx_parameters(
        from_address: str,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
    ) -> TxParams:
        tx_parameters = {"from": from_address}

        if gas_price is not None:
            tx_parameters["gasPrice"] = gas_price

        if gas is not None:
            tx_parameters["gas"] = gas

        if nonce is not None:
            tx_parameters["nonce"] = nonce

        return tx_parameters
