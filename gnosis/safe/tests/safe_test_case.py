import logging
import os
from typing import List, Optional

from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract
from web3.types import Wei

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

        cls.configure_django_settings(cls)
        cls.configure_envvars(cls)

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

    def configure_django_settings(self):
        """
        Configure settings for django based applications

        :return:
        """

        try:
            from django.conf import settings

            settings.SAFE_CONTRACT_ADDRESS = _contract_addresses["safe_V1_4_1"]
            settings.SAFE_DEFAULT_CALLBACK_HANDLER = _contract_addresses[
                "compatibility_fallback_handler"
            ]
            settings.SAFE_MULTISEND_ADDRESS = _contract_addresses["multi_send"]
            settings.SAFE_PROXY_FACTORY_ADDRESS = _contract_addresses["proxy_factory"]
            settings.SAFE_V0_0_1_CONTRACT_ADDRESS = _contract_addresses["safe_V0_0_1"]
            settings.SAFE_V1_0_0_CONTRACT_ADDRESS = _contract_addresses["safe_V1_0_0"]
            settings.SAFE_V1_1_1_CONTRACT_ADDRESS = _contract_addresses["safe_V1_1_1"]
            settings.SAFE_V1_3_0_CONTRACT_ADDRESS = _contract_addresses["safe_V1_3_0"]
            settings.SAFE_V1_4_1_CONTRACT_ADDRESS = _contract_addresses["safe_V1_4_1"]
            settings.SAFE_SIMULATE_TX_ACCESSOR = _contract_addresses[
                "simulate_tx_accessor_V1_4_1"
            ]
            settings.SAFE_VALID_CONTRACT_ADDRESSES = {
                settings.SAFE_CONTRACT_ADDRESS,
                settings.SAFE_V1_3_0_CONTRACT_ADDRESS,
                settings.SAFE_V1_1_1_CONTRACT_ADDRESS,
                settings.SAFE_V1_0_0_CONTRACT_ADDRESS,
                settings.SAFE_V0_0_1_CONTRACT_ADDRESS,
            }

        except ModuleNotFoundError:
            logger.info("Django library is not installed")

    def configure_envvars(self):
        """
        Configure environment variables

        :return:
        """
        os.environ["SAFE_SIMULATE_TX_ACCESSOR_ADDRESS"] = _contract_addresses[
            "simulate_tx_accessor_V1_4_1"
        ]

    def deploy_test_safe(self, *args, **kwargs) -> Safe:
        """
        :param args:
        :param kwargs:
        :return: Deploy last available Safe
        """
        return self.deploy_test_safe_v1_4_1(*args, **kwargs)

    def _deploy_test_safe(
        self,
        initializer: bytes,
        master_copy_address: ChecksumAddress,
        initial_funding_wei: Optional[Wei] = None,
    ) -> Safe:
        """
        Internal method to deploy a Safe given the initializer and master copy

        :param initializer:
        :param master_copy_address:
        :param initial_funding_wei: If provided, funds will be sent to the Safe
        :return: A deployed Safe
        """
        ethereum_tx_sent = self.proxy_factory.deploy_proxy_contract_with_nonce(
            self.ethereum_test_account,
            master_copy_address,
            initializer=initializer,
        )
        safe = Safe(
            ethereum_tx_sent.contract_address,
            self.ethereum_client,
            simulate_tx_accessor_address=self.simulate_tx_accessor_V1_4_1.address,
        )

        if initial_funding_wei:
            self.send_ether(safe.address, initial_funding_wei)

        return safe

    def _deploy_new_test_safe(
        self,
        master_copy_version: str,
        master_copy_address: ChecksumAddress,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: Optional[ChecksumAddress] = None,
    ) -> Safe:
        """
        Internal method to deploy Safes from 1.1.1 to 1.4.1, as setup method didn't change

        :param master_copy_version:
        :param master_copy_address:
        :param number_owners:
        :param threshold:
        :param owners:
        :param initial_funding_wei:
        :param fallback_handler:
        :return: A deployed Safe
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
            ).build_transaction(get_empty_tx_params())["data"]
        )

        safe = self._deploy_test_safe(
            initializer, master_copy_address, initial_funding_wei=initial_funding_wei
        )

        self.assertEqual(safe.retrieve_version(), master_copy_version)
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe

    def deploy_test_safe_v1_4_1(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: Optional[ChecksumAddress] = None,
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
        return self._deploy_new_test_safe(
            "1.4.1",
            self.safe_contract_V1_4_1.address,
            number_owners=number_owners,
            threshold=threshold,
            owners=owners,
            initial_funding_wei=initial_funding_wei,
            fallback_handler=fallback_handler,
        )

    def deploy_test_safe_v1_3_0(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: Optional[ChecksumAddress] = None,
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
        return self._deploy_new_test_safe(
            "1.3.0",
            self.safe_contract_V1_3_0.address,
            number_owners=number_owners,
            threshold=threshold,
            owners=owners,
            initial_funding_wei=initial_funding_wei,
            fallback_handler=fallback_handler,
        )

    def deploy_test_safe_v1_1_1(
        self,
        number_owners: int = 3,
        threshold: Optional[int] = None,
        owners: Optional[List[ChecksumAddress]] = None,
        initial_funding_wei: int = 0,
        fallback_handler: Optional[ChecksumAddress] = NULL_ADDRESS,
    ) -> Safe:
        return self._deploy_new_test_safe(
            "1.1.1",
            self.safe_contract_V1_1_1.address,
            number_owners=number_owners,
            threshold=threshold,
            owners=owners,
            initial_funding_wei=initial_funding_wei,
            fallback_handler=fallback_handler,
        )

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
        to = NULL_ADDRESS
        data = b""
        payment_token = NULL_ADDRESS
        payment = 0
        payment_receiver = NULL_ADDRESS
        initializer = HexBytes(
            self.safe_contract_V1_0_0.functions.setup(
                owners, threshold, to, data, payment_token, payment, payment_receiver
            ).build_transaction(get_empty_tx_params())["data"]
        )
        safe = self._deploy_test_safe(
            initializer,
            self.safe_contract_V1_0_0.address,
            initial_funding_wei=initial_funding_wei,
        )

        self.assertEqual(safe.retrieve_version(), "1.0.0")
        self.assertEqual(safe.retrieve_threshold(), threshold)
        self.assertCountEqual(safe.retrieve_owners(), owners)

        return safe

    def deploy_example_guard(self) -> ChecksumAddress:
        """
        :return: An example DebugTransactionGuard (from safe contracts v1.4.1) supporting IERC165
        """

        bytecode = "0x608060405234801561001057600080fd5b50610929806100206000396000f3fe608060405234801561001057600080fd5b50600436106100505760003560e01c806301ffc9a71461005357806375f0bb52146100b657806393271368146102be578063ddbdba63146102f857610051565b5b005b61009e6004803603602081101561006957600080fd5b8101908080357bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916906020019092919050505061033a565b60405180821515815260200191505060405180910390f35b6102bc60048036036101608110156100cd57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291908035906020019064010000000081111561011457600080fd5b82018360208201111561012657600080fd5b8035906020019184600183028401116401000000008311171561014857600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290803560ff169060200190929190803590602001909291908035906020019092919080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291908035906020019064010000000081111561021657600080fd5b82018360208201111561022857600080fd5b8035906020019184600183028401116401000000008311171561024a57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061040c565b005b6102f6600480360360408110156102d457600080fd5b81019080803590602001909291908035151590602001909291905050506107de565b005b6103246004803603602081101561030e57600080fd5b81019080803590602001909291905050506108db565b6040518082815260200191505060405180910390f35b60007fe6d7a83a000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916148061040557507f01ffc9a7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916145b9050919050565b600080600033905060018173ffffffffffffffffffffffffffffffffffffffff1663affed0e06040518163ffffffff1660e01b815260040160206040518083038186803b15801561045c57600080fd5b505afa158015610470573d6000803e3d6000fd5b505050506040513d602081101561048657600080fd5b81019080805190602001909291905050500392508073ffffffffffffffffffffffffffffffffffffffff1663d8d11f788f8f8f8f8f8f8f8f8f8d6040518b63ffffffff1660e01b8152600401808b73ffffffffffffffffffffffffffffffffffffffff1681526020018a81526020018060200189600181111561050557fe5b81526020018881526020018781526020018681526020018573ffffffffffffffffffffffffffffffffffffffff1681526020018473ffffffffffffffffffffffffffffffffffffffff16815260200183815260200182810382528a818151815260200191508051906020019080838360005b83811015610592578082015181840152602081019050610577565b50505050905090810190601f1680156105bf5780820380516001836020036101000a031916815260200191505b509b50505050505050505050505060206040518083038186803b1580156105e557600080fd5b505afa1580156105f9573d6000803e3d6000fd5b505050506040513d602081101561060f57600080fd5b8101908080519060200190929190505050915050803373ffffffffffffffffffffffffffffffffffffffff167fa65fef32cd19a6639a4bf7a6d196f132c151e4f0bbd2706f7f831b3a778e1ac08f8f8f8f8f60008f118a8d8d604051808a73ffffffffffffffffffffffffffffffffffffffff1681526020018981526020018060200188600181111561069e57fe5b81526020018781526020018615158152602001858152602001806020018473ffffffffffffffffffffffffffffffffffffffff16815260200183810383528a818151815260200191508051906020019080838360005b8381101561070f5780820151818401526020810190506106f4565b50505050905090810190601f16801561073c5780820380516001836020036101000a031916815260200191505b50838103825285818151815260200191508051906020019080838360005b8381101561077557808201518184015260208101905061075a565b50505050905090810190601f1680156107a25780820380516001836020036101000a031916815260200191505b509b50505050505050505050505060405180910390a3816000808381526020019081526020016000208190555050505050505050505050505050565b6000806000848152602001908152602001600020549050600081141561086c576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260138152602001807f436f756c64206e6f7420676574206e6f6e63650000000000000000000000000081525060200191505060405180910390fd5b60008060008581526020019081526020016000208190555080833373ffffffffffffffffffffffffffffffffffffffff167f0dcc0fb56a30b6fe6b188f45b47369bc7f3c928a9748e245a79fc3f54ddd05688560405180821515815260200191505060405180910390a4505050565b6000602052806000526040600020600091509050548156fea26469706673582212206b4220320ac3fc43010ac2089f4931c4c383ca9873db22b0040a28af93142dd864736f6c63430007060033"
        guard_contract = self.w3.eth.contract(abi=[], bytecode=bytecode)
        tx_hash = guard_contract.constructor().transact(
            {"from": self.w3.eth.accounts[0]}
        )
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        assert tx_receipt["status"] == 1, "Problem deploying example guard"
        return tx_receipt["contractAddress"]
