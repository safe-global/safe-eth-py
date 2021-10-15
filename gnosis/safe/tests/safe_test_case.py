import logging
from typing import List, Optional

from django.conf import settings

from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract

from gnosis.eth.contracts import (
    get_compatibility_fallback_handler_V1_3_0_contract,
    get_multi_send_contract,
    get_proxy_factory_contract,
    get_safe_V1_0_0_contract,
    get_safe_V1_1_1_contract,
    get_safe_V1_3_0_contract,
)
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin
from gnosis.safe import Safe
from gnosis.safe.multi_send import MultiSend
from gnosis.safe.proxy_factory import ProxyFactory
from gnosis.safe.safe_create2_tx import SafeCreate2Tx

from ...eth.constants import NULL_ADDRESS
from .utils import generate_salt_nonce

logger = logging.getLogger(__name__)


_contract_addresses = {
    "safe_V0_0_1": Safe.deploy_master_contract_v0_0_1,
    "safe_V1_0_0": Safe.deploy_master_contract_v1_0_0,
    "safe_V1_1_1": Safe.deploy_master_contract_v1_1_1,
    "safe_v1_3_0": Safe.deploy_master_contract_v1_3_0,
    "compatibility_fallback_handler": Safe.deploy_compatibility_fallback_handler,
    "proxy_factory": ProxyFactory.deploy_proxy_factory_contract,
    "proxy_factory_V1_0_0": ProxyFactory.deploy_proxy_factory_contract_v1_0_0,
    "multi_send": MultiSend.deploy_contract,
}


class SafeTestCaseMixin(EthereumTestCaseMixin):
    safe_contract_address: ChecksumAddress
    safe_contract: Contract
    safe_contract_V1_1_1_address: ChecksumAddress
    safe_contract_V1_1_1: Contract
    safe_contract_V1_0_0_address: ChecksumAddress
    safe_contract_V1_0_0: Contract
    safe_contract_V0_0_1_address: ChecksumAddress
    safe_contract_V0_0_1: Contract
    proxy_factory_contract_address: ChecksumAddress
    proxy_factory_contract: Contract
    proxy_factory: ProxyFactory
    multi_send_contract: Contract
    multi_send: MultiSend

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        for key, value in _contract_addresses.items():
            if callable(value):
                _contract_addresses[key] = value(
                    cls.ethereum_client, cls.ethereum_test_account
                ).contract_address

        settings.SAFE_DEFAULT_CALLBACK_HANDLER = _contract_addresses[
            "compatibility_fallback_handler"
        ]
        settings.SAFE_MULTISEND_ADDRESS = _contract_addresses["multi_send"]
        settings.SAFE_CONTRACT_ADDRESS = _contract_addresses["safe_v1_3_0"]
        settings.SAFE_V1_1_1_CONTRACT_ADDRESS = _contract_addresses["safe_V1_1_1"]
        settings.SAFE_V1_0_0_CONTRACT_ADDRESS = _contract_addresses["safe_V1_0_0"]
        settings.SAFE_V0_0_1_CONTRACT_ADDRESS = _contract_addresses["safe_V0_0_1"]
        settings.SAFE_PROXY_FACTORY_ADDRESS = _contract_addresses["proxy_factory"]
        settings.SAFE_PROXY_FACTORY_V1_0_0_ADDRESS = _contract_addresses[
            "proxy_factory_V1_0_0"
        ]
        settings.SAFE_VALID_CONTRACT_ADDRESSES = {
            settings.SAFE_CONTRACT_ADDRESS,
            settings.SAFE_V1_1_1_CONTRACT_ADDRESS,
            settings.SAFE_V1_0_0_CONTRACT_ADDRESS,
            settings.SAFE_V0_0_1_CONTRACT_ADDRESS,
        }
        cls.compatibility_fallback_handler = (
            get_compatibility_fallback_handler_V1_3_0_contract(
                cls.w3, _contract_addresses["compatibility_fallback_handler"]
            )
        )
        cls.safe_contract_address = _contract_addresses["safe_v1_3_0"]
        cls.safe_contract = get_safe_V1_3_0_contract(cls.w3, cls.safe_contract_address)
        cls.safe_contract_V1_1_1_address = _contract_addresses["safe_V1_1_1"]
        cls.safe_contract_V1_1_1 = get_safe_V1_1_1_contract(
            cls.w3, cls.safe_contract_V1_1_1_address
        )
        cls.safe_contract_V1_0_0_address = _contract_addresses["safe_V1_0_0"]
        cls.safe_contract_V1_0_0 = get_safe_V1_0_0_contract(
            cls.w3, cls.safe_contract_V1_0_0_address
        )
        cls.safe_contract_V0_0_1_address = _contract_addresses["safe_V0_0_1"]
        cls.safe_contract_V0_0_1 = get_safe_V1_0_0_contract(
            cls.w3, cls.safe_contract_V0_0_1_address
        )
        cls.proxy_factory_contract_address = _contract_addresses["proxy_factory"]
        cls.proxy_factory_contract = get_proxy_factory_contract(
            cls.w3, cls.proxy_factory_contract_address
        )
        cls.proxy_factory = ProxyFactory(
            cls.proxy_factory_contract_address, cls.ethereum_client
        )
        cls.multi_send_contract = get_multi_send_contract(
            cls.w3, _contract_addresses["multi_send"]
        )
        cls.multi_send = MultiSend(cls.multi_send_contract.address, cls.ethereum_client)

    def build_test_safe(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[str]] = None,
        fallback_handler: Optional[str] = None,
    ) -> SafeCreate2Tx:
        salt_nonce = generate_salt_nonce()
        owners = (
            owners
            if owners
            else [Account.create().address for _ in range(number_owners)]
        )
        threshold = threshold if threshold else len(owners) - 1

        gas_price = self.ethereum_client.w3.eth.gas_price
        return Safe.build_safe_create2_tx(
            self.ethereum_client,
            self.safe_contract_address,
            self.proxy_factory_contract_address,
            salt_nonce,
            owners,
            threshold,
            fallback_handler=fallback_handler,
            gas_price=gas_price,
            payment_token=None,
            fixed_creation_cost=0,
        )

    def deploy_test_safe(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: ChecksumAddress = None,
    ) -> Safe:
        """
        Deploy a Safe v1.3.0

        :param number_owners:
        :param threshold:
        :param owners:
        :param initial_funding_wei:
        :param fallback_handler:
        :return:
        """
        fallback_handler = (
            fallback_handler or self.compatibility_fallback_handler.address
        )
        owners = (
            owners
            if owners
            else [Account.create().address for _ in range(number_owners)]
        )
        if not threshold:
            threshold = len(owners) - 1 if len(owners) > 1 else 1
        empty_parameters = {"gas": 1, "gasPrice": 1}
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract.functions.setup(
                owners,
                threshold,
                to,
                data,
                fallback_handler,
                payment_token,
                payment,
                payment_receiver,
            ).buildTransaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract(
            self.ethereum_test_account,
            self.safe_contract.address,
            initializer=initializer,
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        if initial_funding_wei:
            self.send_ether(safe.address, initial_funding_wei)

        self.assertEqual(safe.retrieve_version(), "1.3.0")
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe

    def deploy_test_safe_v1_1_1(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[str]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: Optional[str] = NULL_ADDRESS,
    ) -> Safe:
        owners = (
            owners
            if owners
            else [Account.create().address for _ in range(number_owners)]
        )
        if not threshold:
            threshold = len(owners) - 1 if len(owners) > 1 else 1
        empty_parameters = {"gas": 1, "gasPrice": 1}
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract_V1_1_1.functions.setup(
                owners,
                threshold,
                to,
                data,
                fallback_handler,
                payment_token,
                payment,
                payment_receiver,
            ).buildTransaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract(
            self.ethereum_test_account,
            self.safe_contract_V1_1_1.address,
            initializer=initializer,
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        if initial_funding_wei:
            self.send_ether(safe.address, initial_funding_wei)

        self.assertEqual(safe.retrieve_version(), "1.1.1")
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe

    def deploy_test_safe_v1_0_0(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
    ) -> Safe:
        owners = (
            owners
            if owners
            else [Account.create().address for _ in range(number_owners)]
        )
        if not threshold:
            threshold = len(owners) - 1 if len(owners) > 1 else 1
        empty_parameters = {"gas": 1, "gasPrice": 1}
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract_V1_0_0.functions.setup(
                owners, threshold, to, data, payment_token, payment, payment_receiver
            ).buildTransaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract(
            self.ethereum_test_account,
            self.safe_contract_V1_0_0_address,
            initializer=initializer,
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        if initial_funding_wei:
            self.send_ether(safe.address, initial_funding_wei)

        self.assertEqual(safe.retrieve_version(), "1.0.0")
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe
