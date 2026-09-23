import asyncio
import os
import time
import unittest
from unittest import mock

from django.test import TestCase

import pytest
import requests

from ... import EthereumNetwork
from ...clients import (
    EtherscanClientException,
    EtherscanClientV2,
    EtherscanConnectionError,
    EtherscanHttpError,
    EtherscanRateLimitError,
)
from ...clients.etherscan_client_v2 import AsyncEtherscanClientV2
from .mocks import sourcify_safe_metadata

# Errors on the Etherscan side that are out of our control. Network tests skip on them,
# while any other `EtherscanClientException` (e.g. an invalid API key) fails the test
ETHERSCAN_TRANSIENT_ERRORS = (
    EtherscanRateLimitError,
    EtherscanConnectionError,
    EtherscanHttpError,
)


class TestEtherscanClientV2ResponseProcessing(unittest.TestCase):
    def test_process_response_json(self):
        result = [{"ContractName": "GnosisSafe", "ABI": "[]"}]
        self.assertEqual(
            EtherscanClientV2._process_response_json(
                {"status": "1", "message": "OK", "result": result}
            ),
            result,
        )

    def test_process_response_json_rate_limit(self):
        rate_limit_messages = (
            "Max rate limit reached, please use API Key for higher rate limit",
            "Max calls per sec rate limit reached (5/sec)",
            "Max daily rate limit reached. 100000 (100%) of 100000 day/limit",
        )
        for rate_limit_message in rate_limit_messages:
            with self.subTest(rate_limit_message=rate_limit_message):
                with self.assertRaises(EtherscanRateLimitError):
                    EtherscanClientV2._process_response_json(
                        {
                            "status": "0",
                            "message": "NOTOK",
                            "result": rate_limit_message,
                        }
                    )

    def test_process_response_json_not_found(self):
        self.assertIsNone(
            EtherscanClientV2._process_response_json(
                {
                    "status": "0",
                    "message": "NOTOK",
                    "result": "Contract source code not verified",
                }
            )
        )

    def test_process_response_json_error(self):
        with self.assertRaises(EtherscanClientException):
            EtherscanClientV2._process_response_json(
                {"status": "0", "message": "NOTOK", "result": "Invalid Address format"}
            )

        # `result` is null on some errors, the reason is then only in `message`
        with self.assertRaises(EtherscanClientException):
            EtherscanClientV2._process_response_json(
                {"status": "0", "message": "Invalid API Key", "result": None}
            )

        # Both null
        with self.assertRaises(EtherscanClientException):
            EtherscanClientV2._process_response_json(
                {"status": "0", "message": None, "result": None}
            )

    def test_build_http_error(self):
        self.assertIsInstance(
            EtherscanClientV2._build_http_error(429), EtherscanRateLimitError
        )
        http_error = EtherscanClientV2._build_http_error(500)
        self.assertIsInstance(http_error, EtherscanHttpError)
        self.assertEqual(http_error.status_code, 500)

    def test_retry_request_rate_limit(self):
        etherscan_client = EtherscanClientV2(EthereumNetwork.MAINNET)
        with (
            mock.patch.object(
                EtherscanClientV2, "_do_request", side_effect=EtherscanRateLimitError
            ) as do_request_mock,
            mock.patch.object(time, "sleep") as sleep_mock,
        ):
            with self.assertRaises(EtherscanRateLimitError):
                etherscan_client._retry_request("https://api.etherscan.io")
            self.assertEqual(do_request_mock.call_count, 3)
            self.assertEqual(sleep_mock.call_count, 2)

            do_request_mock.reset_mock()
            sleep_mock.reset_mock()
            with self.assertRaises(EtherscanRateLimitError):
                etherscan_client._retry_request("https://api.etherscan.io", retry=False)
            self.assertEqual(do_request_mock.call_count, 1)
            sleep_mock.assert_not_called()

    def test_retry_request_connection_error(self):
        # Only the rate limit is retried, a connection error is raised on the first attempt
        etherscan_client = EtherscanClientV2(EthereumNetwork.MAINNET)
        with (
            mock.patch.object(
                EtherscanClientV2, "_do_request", side_effect=EtherscanConnectionError
            ) as do_request_mock,
            mock.patch.object(time, "sleep") as sleep_mock,
        ):
            with self.assertRaises(EtherscanConnectionError):
                etherscan_client._retry_request("https://api.etherscan.io")
            self.assertEqual(do_request_mock.call_count, 1)
            sleep_mock.assert_not_called()

    def test_do_request_connection_error(self):
        etherscan_client = EtherscanClientV2(EthereumNetwork.MAINNET)
        with mock.patch.object(
            etherscan_client.http_session,
            "get",
            side_effect=requests.ConnectionError,
        ):
            with self.assertRaises(EtherscanConnectionError) as ctx:
                etherscan_client._do_request("https://api.etherscan.io")
            # It is also a builtin `ConnectionError`, and the `requests` exception is
            # kept as the cause
            self.assertIsInstance(ctx.exception, ConnectionError)
            self.assertIsInstance(ctx.exception.__cause__, requests.ConnectionError)


class TestAsyncEtherscanClientV2ResponseProcessing(unittest.IsolatedAsyncioTestCase):
    async def test_async_do_request_connection_error(self):
        etherscan_client = AsyncEtherscanClientV2(EthereumNetwork.MAINNET)
        self.addAsyncCleanup(etherscan_client.async_session.close)
        with mock.patch.object(
            etherscan_client.async_session,
            "get",
            side_effect=asyncio.TimeoutError,
        ):
            with self.assertRaises(EtherscanConnectionError) as ctx:
                await etherscan_client._async_do_request("https://api.etherscan.io")
            self.assertIsInstance(ctx.exception, ConnectionError)
            self.assertIsInstance(ctx.exception.__cause__, asyncio.TimeoutError)


@pytest.mark.network
class TestEtherscanClientV2(TestCase):
    @classmethod
    def get_etherscan_api(cls, network: EthereumNetwork):
        etherscan_api_key_variable_name = "ETHERSCAN_API_KEY"
        etherscan_api_key = os.environ.get(etherscan_api_key_variable_name)
        if not etherscan_api_key:
            pytest.skip(f"{etherscan_api_key_variable_name} needs to be defined")

        return EtherscanClientV2(network, api_key=etherscan_api_key)

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_etherscan_get_abi(self):
        try:
            etherscan_api = self.get_etherscan_api(EthereumNetwork.MAINNET)
            safe_master_copy_abi = sourcify_safe_metadata["output"]["abi"]
            safe_master_copy_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
            self.assertEqual(
                etherscan_api.get_contract_abi(safe_master_copy_address),
                safe_master_copy_abi,
            )

            contract_metadata = etherscan_api.get_contract_metadata(
                safe_master_copy_address
            )
            if contract_metadata is None:
                self.skipTest("Etherscan did not return the contract metadata")
            self.assertEqual(contract_metadata.name, "GnosisSafe")
            self.assertEqual(contract_metadata.abi, safe_master_copy_abi)
            self.assertIsNone(contract_metadata.implementation)

            random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
            self.assertIsNone(etherscan_api.get_contract_abi(random_address))
            self.assertIsNone(etherscan_api.get_contract_metadata(random_address))
        except ETHERSCAN_TRANSIENT_ERRORS as exc:
            self.skipTest(f"Etherscan not available: {exc}")

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_etherscan_get_contract_metadata(self):
        try:
            etherscan_api = self.get_etherscan_api(EthereumNetwork.MAINNET)
            proxy_address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

            contract_metadata = etherscan_api.get_contract_metadata(proxy_address)
            if contract_metadata is None:
                self.skipTest("Etherscan did not return the contract metadata")
            self.assertEqual(contract_metadata.name, "FiatTokenProxy")
            self.assertEqual(
                contract_metadata.implementation,
                "0x43506849d7c04f9138d1a2050bbf3a0c054402dd",
            )

        except ETHERSCAN_TRANSIENT_ERRORS as exc:
            self.skipTest(f"Etherscan not available: {exc}")

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_is_supported_network(self):
        self.assertTrue(EtherscanClientV2.is_supported_network(EthereumNetwork.GNOSIS))
        self.assertFalse(
            EtherscanClientV2.is_supported_network(EthereumNetwork.UNKNOWN)
        )

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_get_base_url(self):
        self.assertEqual(
            EtherscanClientV2(EthereumNetwork.POLYGON).get_base_url(),
            "https://polygonscan.com/",
        )


@pytest.mark.network
class TestAsyncEtherscanClientV2(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def get_etherscan_api(cls, network: EthereumNetwork):
        etherscan_api_key_variable_name = "ETHERSCAN_API_KEY"
        etherscan_api_key = os.environ.get(etherscan_api_key_variable_name)
        if not etherscan_api_key:
            pytest.skip(f"{etherscan_api_key_variable_name} needs to be defined")

        return AsyncEtherscanClientV2(network, api_key=etherscan_api_key)

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    async def test_async_etherscan_get_abi(self):
        try:
            etherscan_api = self.get_etherscan_api(EthereumNetwork.MAINNET)
            safe_master_copy_abi = sourcify_safe_metadata["output"]["abi"]
            safe_master_copy_address = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
            self.assertEqual(
                await etherscan_api.async_get_contract_abi(safe_master_copy_address),
                safe_master_copy_abi,
            )

            contract_metadata = await etherscan_api.async_get_contract_metadata(
                safe_master_copy_address
            )
            if contract_metadata is None:
                self.skipTest("Etherscan did not return the contract metadata")
            self.assertEqual(contract_metadata.name, "GnosisSafe")
            self.assertEqual(contract_metadata.abi, safe_master_copy_abi)

            random_address = "0xaE32496491b53841efb51829d6f886387708F99a"
            self.assertIsNone(
                await etherscan_api.async_get_contract_abi(random_address)
            )
            self.assertIsNone(
                await etherscan_api.async_get_contract_metadata(random_address)
            )
        except ETHERSCAN_TRANSIENT_ERRORS as exc:
            self.skipTest(f"Etherscan not available: {exc}")
