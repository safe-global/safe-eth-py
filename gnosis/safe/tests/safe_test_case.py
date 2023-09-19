import logging
import os
from typing import List, Optional

from django.conf import settings

from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract

from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import (
    get_compatibility_fallback_handler_contract,
    get_multi_send_contract,
    get_proxy_factory_contract,
    get_safe_V1_0_0_contract,
    get_safe_V1_1_1_contract,
    get_safe_V1_3_0_contract,
    get_safe_V1_4_1_contract,
    get_simulate_tx_accessor_V1_4_1_contract,
)
from gnosis.eth.tests.ethereum_test_case import EthereumTestCaseMixin
from gnosis.eth.utils import get_empty_tx_params
from gnosis.safe import Safe
from gnosis.safe.multi_send import MultiSend
from gnosis.safe.proxy_factory import ProxyFactory, ProxyFactoryV141

from ..safe import SafeV001, SafeV100, SafeV111, SafeV130, SafeV141

logger = logging.getLogger(__name__)


_contract_addresses = {}


class SafeTestCaseMixin(EthereumTestCaseMixin):
    compatibility_fallback_handler: Contract
    multi_send: MultiSend
    multi_send_contract: Contract
    proxy_factory: ProxyFactory
    proxy_factory_contract: Contract
    safe_contract_V1_4_1: Contract
    safe_contract_V0_0_1: Contract
    safe_contract_V1_0_0: Contract
    safe_contract_V1_1_1: Contract
    safe_contract_V1_3_0: Contract
    safe_contract_address: ChecksumAddress
    simulate_tx_accessor_V1_4_1: Contract

    contract_deployers = {
        "safe_V0_0_1": SafeV001.deploy_contract,
        "safe_V1_0_0": SafeV100.deploy_contract,
        "safe_V1_1_1": SafeV111.deploy_contract,
        "safe_V1_3_0": SafeV130.deploy_contract,
        "safe_V1_4_1": SafeV141.deploy_contract,
        "compatibility_fallback_handler": Safe.deploy_compatibility_fallback_handler,
        "simulate_tx_accessor_V1_4_1": Safe.deploy_simulate_tx_accessor,
        "proxy_factory": ProxyFactoryV141.deploy_contract,
        "multi_send": MultiSend.deploy_contract,
    }

    @property
    def safe_contract(self):
        """
        :return: Last Safe Contract available
        """
        return self.safe_contract_V1_4_1

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if not _contract_addresses:
            # First time mixin is called, deploy Safe contracts
            for key, function in cls.contract_deployers.items():
                _contract_addresses[key] = function(
                    cls.ethereum_client, cls.ethereum_test_account
                ).contract_address

        settings.SAFE_CONTRACT_ADDRESS = _contract_addresses["safe_V1_4_1"]
        settings.SAFE_DEFAULT_CALLBACK_HANDLER = _contract_addresses[
            "compatibility_fallback_handler"
        ]
        settings.SAFE_MULTISEND_ADDRESS = _contract_addresses["multi_send"]
        settings.SAFE_PROXY_FACTORY_ADDRESS = _contract_addresses["proxy_factory"]
        os.environ["SAFE_SIMULATE_TX_ACCESSOR_ADDRESS"] = _contract_addresses[
            "simulate_tx_accessor_V1_4_1"
        ]
        settings.SAFE_SIMULATE_TX_ACCESSOR = _contract_addresses[
            "simulate_tx_accessor_V1_4_1"
        ]
        settings.SAFE_V0_0_1_CONTRACT_ADDRESS = _contract_addresses["safe_V0_0_1"]
        settings.SAFE_V1_0_0_CONTRACT_ADDRESS = _contract_addresses["safe_V1_0_0"]
        settings.SAFE_V1_1_1_CONTRACT_ADDRESS = _contract_addresses["safe_V1_1_1"]
        settings.SAFE_V1_3_0_CONTRACT_ADDRESS = _contract_addresses["safe_V1_3_0"]
        settings.SAFE_VALID_CONTRACT_ADDRESSES = {
            settings.SAFE_CONTRACT_ADDRESS,
            settings.SAFE_V1_3_0_CONTRACT_ADDRESS,
            settings.SAFE_V1_1_1_CONTRACT_ADDRESS,
            settings.SAFE_V1_0_0_CONTRACT_ADDRESS,
            settings.SAFE_V0_0_1_CONTRACT_ADDRESS,
        }
        cls.compatibility_fallback_handler = (
            get_compatibility_fallback_handler_contract(
                cls.w3, _contract_addresses["compatibility_fallback_handler"]
            )
        )
        cls.simulate_tx_accessor_V1_4_1 = get_simulate_tx_accessor_V1_4_1_contract(
            cls.w3, _contract_addresses["simulate_tx_accessor_V1_4_1"]
        )
        cls.safe_contract_V1_4_1 = get_safe_V1_4_1_contract(
            cls.w3, _contract_addresses["safe_V1_4_1"]
        )
        cls.safe_contract_V1_3_0 = get_safe_V1_3_0_contract(
            cls.w3, _contract_addresses["safe_V1_3_0"]
        )
        cls.safe_contract_V1_1_1 = get_safe_V1_1_1_contract(
            cls.w3, _contract_addresses["safe_V1_1_1"]
        )
        cls.safe_contract_V1_0_0 = get_safe_V1_0_0_contract(
            cls.w3, _contract_addresses["safe_V1_0_0"]
        )
        cls.safe_contract_V0_0_1 = get_safe_V1_0_0_contract(
            cls.w3, _contract_addresses["safe_V0_0_1"]
        )
        cls.proxy_factory_contract = get_proxy_factory_contract(
            cls.w3, _contract_addresses["proxy_factory"]
        )
        cls.proxy_factory = ProxyFactory(
            cls.proxy_factory_contract.address, cls.ethereum_client
        )
        cls.multi_send_contract = get_multi_send_contract(
            cls.w3, _contract_addresses["multi_send"]
        )
        cls.multi_send = MultiSend(
            cls.ethereum_client, address=cls.multi_send_contract.address
        )

    def deploy_test_safe(self, *args, **kwargs) -> Safe:
        """
        :param args:
        :param kwargs:
        :return: Deploy last available Safe
        """
        return self.deploy_test_safe_v1_4_1(*args, **kwargs)

    # TODO Refactor this
    def deploy_test_safe_v1_4_1(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: ChecksumAddress = None,
    ) -> Safe:
        """
        Deploy a Safe v1.4.1

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
        empty_parameters = get_empty_tx_params()
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract_V1_4_1.functions.setup(
                owners,
                threshold,
                to,
                data,
                fallback_handler,
                payment_token,
                payment,
                payment_receiver,
            ).build_transaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract_V1_4_1.address,
            initializer=initializer,
        )
        safe = Safe(
            ethereum_tx_sent.contract_address,
            self.ethereum_client,
            simulate_tx_accessor_address=self.simulate_tx_accessor_V1_4_1.address,
        )

        if initial_funding_wei:
            self.send_ether(safe.address, initial_funding_wei)

        self.assertEqual(safe.retrieve_version(), "1.4.1")
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe

    def deploy_test_safe_v1_3_0(
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
        empty_parameters = get_empty_tx_params()
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract_V1_3_0.functions.setup(
                owners,
                threshold,
                to,
                data,
                fallback_handler,
                payment_token,
                payment,
                payment_receiver,
            ).build_transaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract_V1_3_0.address,
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
        empty_parameters = get_empty_tx_params()
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
            ).build_transaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
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
        empty_parameters = get_empty_tx_params()
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract_V1_0_0.functions.setup(
                owners, threshold, to, data, payment_token, payment, payment_receiver
            ).build_transaction(empty_parameters)["data"]
        )
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            self.safe_contract_V1_0_0.address,
            initializer=initializer,
        )
        safe = Safe(ethereum_tx_sent.contract_address, self.ethereum_client)
        if initial_funding_wei:
            self.send_ether(safe.address, initial_funding_wei)

        self.assertEqual(safe.retrieve_version(), "1.0.0")
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe
