import logging
from typing import List, NamedTuple, Optional

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from hexbytes import HexBytes

from gnosis.eth import EthereumClient, EthereumTxSent
from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import (
    get_compatibility_fallback_handler_contract,
    get_delegate_constructor_proxy_contract,
    get_safe_contract,
    get_simulate_tx_accessor_V1_4_1_contract,
)
from gnosis.eth.utils import get_empty_tx_params

from .exceptions import InvalidPaymentToken
from .proxy_factory import ProxyFactory
from .safe_create2_tx import InvalidERC20Token, SafeCreate2Tx, SafeCreate2TxBuilder

logger = logging.getLogger(__name__)


class SafeCreationEstimate(NamedTuple):
    gas: int
    gas_price: int
    payment: int
    payment_token: Optional[str]


class SafeCreator:
    @staticmethod
    def create(
        ethereum_client: EthereumClient,
        deployer_account: LocalAccount,
        master_copy_address: ChecksumAddress,
        owners: List[ChecksumAddress],
        threshold: int,
        fallback_handler: Optional[ChecksumAddress] = NULL_ADDRESS,
        proxy_factory_address: Optional[ChecksumAddress] = None,
        payment_token: Optional[ChecksumAddress] = NULL_ADDRESS,
        payment: int = 0,
        payment_receiver: Optional[ChecksumAddress] = NULL_ADDRESS,
    ) -> EthereumTxSent:
        """
        Deploy new Safe proxy pointing to the specified `master_copy` address and configured
        with the provided `owners` and `threshold`. By default, payment for the deployer of the tx will be `0`.
        If `proxy_factory_address` is set deployment will be done using the proxy factory instead of calling
        the `constructor` of a new `DelegatedProxy`
        Using `proxy_factory_address` is recommended

        :param ethereum_client:
        :param deployer_account:
        :param master_copy_address:
        :param owners:
        :param threshold:
        :param fallback_handler:
        :param proxy_factory_address:
        :param payment_token:
        :param payment:
        :param payment_receiver:
        :return:
        """

        assert owners, "At least one owner must be set"
        assert 1 <= threshold <= len(owners), "Threshold=%d must be <= %d" % (
            threshold,
            len(owners),
        )

        initializer = (
            get_safe_contract(ethereum_client.w3, NULL_ADDRESS)
            .functions.setup(
                owners,
                threshold,
                NULL_ADDRESS,  # Contract address for optional delegate call
                b"",  # Data payload for optional delegate call
                fallback_handler,  # Handler for fallback calls to this contract,
                payment_token,
                payment,
                payment_receiver,
            )
            .build_transaction(get_empty_tx_params())["data"]
        )

        if proxy_factory_address:
            proxy_factory = ProxyFactory(proxy_factory_address, ethereum_client)
            return proxy_factory.deploy_proxy_contract_with_nonce(
                deployer_account, master_copy_address, initializer=HexBytes(initializer)
            )

        proxy_contract = get_delegate_constructor_proxy_contract(ethereum_client.w3)
        tx = proxy_contract.constructor(
            master_copy_address, initializer
        ).build_transaction({"from": deployer_account.address})
        tx_hash = ethereum_client.send_unsigned_transaction(
            tx, private_key=deployer_account.key
        )
        tx_receipt = ethereum_client.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt
        assert tx_receipt["status"]

        contract_address = tx_receipt["contractAddress"]
        return EthereumTxSent(tx_hash, tx, contract_address)

    @staticmethod
    def deploy_compatibility_fallback_handler(
        ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy Last compatibility Fallback handler

        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: ``EthereumTxSent`` with the deployed contract address
        """

        contract = get_compatibility_fallback_handler_contract(ethereum_client.w3)
        constructor_data = contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]
        ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data
        )
        logger.info(
            "Deployed and initialized Compatibility Fallback Handler version=%s on address %s by %s",
            "1.4.1",
            ethereum_tx_sent.contract_address,
            deployer_account.address,
        )
        return ethereum_tx_sent

    @staticmethod
    def deploy_simulate_tx_accessor(
        ethereum_client: EthereumClient, deployer_account: LocalAccount
    ) -> EthereumTxSent:
        """
        Deploy Last compatibility Fallback handler

        :param ethereum_client:
        :param deployer_account: Ethereum account
        :return: ``EthereumTxSent`` with the deployed contract address
        """

        contract = get_simulate_tx_accessor_V1_4_1_contract(ethereum_client.w3)
        constructor_data = contract.constructor().build_transaction(
            get_empty_tx_params()
        )["data"]
        ethereum_tx_sent = ethereum_client.deploy_and_initialize_contract(
            deployer_account, constructor_data
        )
        logger.info(
            "Deployed and initialized Simulate Tx Accessor contract version=%s on address %s by %s",
            "1.4.1",
            ethereum_tx_sent.contract_address,
            deployer_account.address,
        )
        return ethereum_tx_sent

    @staticmethod
    def estimate_safe_creation_2(
        ethereum_client: EthereumClient,
        master_copy_address: ChecksumAddress,
        proxy_factory_address: ChecksumAddress,
        number_owners: int,
        gas_price: int,
        payment_token: Optional[ChecksumAddress],
        payment_receiver: ChecksumAddress = NULL_ADDRESS,
        fallback_handler: Optional[ChecksumAddress] = None,
        payment_token_eth_value: float = 1.0,
        fixed_creation_cost: Optional[int] = None,
    ) -> SafeCreationEstimate:
        """
        :param ethereum_client:
        :param master_copy_address:
        :param proxy_factory_address:
        :param number_owners:
        :param gas_price:
        :param payment_token:
        :param payment_receiver:
        :param fallback_handler:
        :param payment_token_eth_value:
        :param fixed_creation_cost:
        :return: An estimation for creating a Safe with the provided parameters
        """
        salt_nonce = 15
        owners = [Account.create().address for _ in range(number_owners)]
        threshold = number_owners
        if not fallback_handler:
            fallback_handler = (
                Account.create().address
            )  # Better estimate it, it's required for new Safes
        safe_creation_tx = SafeCreate2TxBuilder(
            w3=ethereum_client.w3,
            master_copy_address=master_copy_address,
            proxy_factory_address=proxy_factory_address,
        ).build(
            owners=owners,
            threshold=threshold,
            fallback_handler=fallback_handler,
            salt_nonce=salt_nonce,
            gas_price=gas_price,
            payment_receiver=payment_receiver,
            payment_token=payment_token,
            payment_token_eth_value=payment_token_eth_value,
            fixed_creation_cost=fixed_creation_cost,
        )
        return SafeCreationEstimate(
            safe_creation_tx.gas,
            safe_creation_tx.gas_price,
            safe_creation_tx.payment,
            safe_creation_tx.payment_token,
        )

    @staticmethod
    def build_safe_create2_tx(
        ethereum_client: EthereumClient,
        master_copy_address: ChecksumAddress,
        proxy_factory_address: ChecksumAddress,
        salt_nonce: int,
        owners: List[ChecksumAddress],
        threshold: int,
        gas_price: int,
        payment_token: Optional[ChecksumAddress],
        payment_receiver: Optional[
            ChecksumAddress
        ] = None,  # If none, it will be `tx.origin`
        fallback_handler: Optional[ChecksumAddress] = NULL_ADDRESS,
        payment_token_eth_value: float = 1.0,
        fixed_creation_cost: Optional[int] = None,
    ) -> SafeCreate2Tx:
        """
        Prepare safe proxy deployment for being relayed. It calculates and sets the costs of deployment to be returned
        to the sender of the tx. If you are an advanced user you may prefer to use `create` function
        """
        try:
            safe_creation_tx = SafeCreate2TxBuilder(
                w3=ethereum_client.w3,
                master_copy_address=master_copy_address,
                proxy_factory_address=proxy_factory_address,
            ).build(
                owners=owners,
                threshold=threshold,
                fallback_handler=fallback_handler,
                salt_nonce=salt_nonce,
                gas_price=gas_price,
                payment_receiver=payment_receiver,
                payment_token=payment_token,
                payment_token_eth_value=payment_token_eth_value,
                fixed_creation_cost=fixed_creation_cost,
            )
        except InvalidERC20Token as exc:
            raise InvalidPaymentToken(
                "Invalid payment token %s" % payment_token
            ) from exc

        return safe_creation_tx
