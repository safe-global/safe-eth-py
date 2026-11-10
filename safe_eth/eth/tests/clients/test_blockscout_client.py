import asyncio
import json
import os
import unittest
from contextlib import AbstractContextManager
from typing import Any, Self
from unittest import mock

import pytest
import requests

from ... import EthereumNetwork
from ...clients import (
    BlockscoutApiKeyError,
    BlockscoutClient,
    BlockScoutConfigurationProblem,
    BlockscoutConnectionError,
    BlockscoutHttpError,
    BlockscoutRateLimitError,
)
from ...clients.blockscout_client import AsyncBlockscoutClient
from .mocks import safe_proxy_abi_mock, sourcify_safe_metadata

SAFE_MASTER_COPY_ADDRESS = "0x6851D6fDFAfD08c0295C392436245E5bc78B0185"
SAFE_PROXY_ADDRESS = "0xfca7Da0a0290D7BcBEcD93bE124756fC9B6F8E6A"
SAFE_PROXY_IMPLEMENTATION_ADDRESS = "0x3E5c63644E683549055b9Be8653de26E0B4CD36E"
RANDOM_ADDRESS = "0xaE32496491b53841efb51829d6f886387708F99a"

NOT_FOUND_BODY = '{"message":"Not found"}'
# Bodies of a 404 that does not mean "no verified contract": a dead instance and a
# network not served by the PRO API
OTHER_NOT_FOUND_BODIES = (
    "<html>404 page not found</html>",
    '["Not found"]',
    '{"error":"Network not supported","source":"internal"}',
)
# Status code returned by Blockscout and the exception the client must raise for it
HTTP_ERROR_STATUS_EXCEPTIONS = (
    (401, BlockscoutApiKeyError),
    (402, BlockscoutApiKeyError),
    (403, BlockscoutHttpError),
    (422, BlockscoutHttpError),
    (429, BlockscoutRateLimitError),
    (500, BlockscoutHttpError),
)


def get_blockscout_api_key() -> str:
    blockscout_api_key_variable_name = "BLOCKSCOUT_API_KEY"
    blockscout_api_key = os.environ.get(blockscout_api_key_variable_name)
    if not blockscout_api_key:
        pytest.skip(f"{blockscout_api_key_variable_name} needs to be defined")
    return blockscout_api_key


def build_requests_response(status_code: int, body: str) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = body.encode()
    return response


class AiohttpResponseMock:
    def __init__(self, status: int, body: str) -> None:
        self.status = status
        self.body = body

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> bool:
        return False

    async def text(self, errors: str = "strict") -> str:
        return self.body


class TestBlockscoutClientConfiguration(unittest.TestCase):
    def test_not_supported_network(self):
        """
        A network with no Blockscout instance and not served by the PRO API is rejected
        """
        with self.assertRaises(BlockScoutConfigurationProblem):
            BlockscoutClient(EthereumNetwork.MAINNET)

    def test_pro_api_network_needs_api_key(self):
        """
        A network only served by the PRO API is rejected when no API key is provided
        """
        for api_key in (None, ""):
            with self.subTest(api_key=api_key):
                with self.assertRaisesRegex(
                    BlockScoutConfigurationProblem, "PRO API key"
                ):
                    BlockscoutClient(EthereumNetwork.GNOSIS, api_key=api_key)
                with self.assertRaisesRegex(
                    BlockScoutConfigurationProblem, "PRO API key"
                ):
                    AsyncBlockscoutClient(EthereumNetwork.GNOSIS, api_key=api_key)

    def test_pro_api_network_url(self):
        """
        A network only served by the PRO API uses the multichain url, and the API key
        goes in the Authorization header, not in the url
        """
        blockscout_client = BlockscoutClient(EthereumNetwork.GNOSIS, api_key="test-key")
        self.assertEqual(
            blockscout_client.build_url("smart-contracts/0x01"),
            "https://api.blockscout.com/100/api/v2/smart-contracts/0x01",
        )
        self.assertEqual(
            blockscout_client.http_session.headers["Authorization"], "Bearer test-key"
        )

    def test_instance_network_url(self):
        """
        A network with its own Blockscout instance uses the instance url, and the API
        key is never sent to it
        """
        blockscout_client = BlockscoutClient(
            EthereumNetwork.CELO_MAINNET, api_key="test-key"
        )
        self.assertEqual(
            blockscout_client.build_url("smart-contracts/0x01"),
            BlockscoutClient.NETWORK_WITH_URL[EthereumNetwork.CELO_MAINNET]
            + "smart-contracts/0x01",
        )
        self.assertNotIn("Authorization", blockscout_client.http_session.headers)


class TestBlockscoutClientProcessResponse(unittest.TestCase):
    def test_process_response(self):
        """
        A successful response is decoded
        """
        self.assertEqual(
            BlockscoutClient._process_response(200, '{"name": "GnosisSafe"}'),
            {"name": "GnosisSafe"},
        )

    def test_process_response_not_found(self):
        """
        HTTP 404 with the Blockscout "Not found" body means there is no verified
        contract for the address. Any other 404 is an error
        """
        self.assertIsNone(BlockscoutClient._process_response(404, NOT_FOUND_BODY))
        self.assertIsNone(
            BlockscoutClient._process_response(
                404, '{"message":"Not found","status":"0"}'
            )
        )
        for body in OTHER_NOT_FOUND_BODIES:
            with self.subTest(body=body):
                with self.assertRaises(BlockscoutHttpError) as ctx:
                    BlockscoutClient._process_response(404, body)
                self.assertEqual(ctx.exception.status_code, 404)

    def test_process_response_http_errors(self):
        """
        Any other non ok status raises its exception
        """
        for status_code, exception_class in HTTP_ERROR_STATUS_EXCEPTIONS:
            with self.subTest(status_code=status_code):
                with self.assertRaises(exception_class):
                    BlockscoutClient._process_response(status_code, "{}")


class TestBlockscoutClientRequest(unittest.TestCase):
    def setUp(self):
        self.blockscout_client = BlockscoutClient(
            EthereumNetwork.GNOSIS, api_key="test-key"
        )

    def patch_session_get(self, **kwargs: Any) -> AbstractContextManager[Any]:
        return mock.patch.object(self.blockscout_client.http_session, "get", **kwargs)

    def test_get_contract_metadata_not_found(self):
        """
        No verified contract for the address returns None
        """
        with self.patch_session_get(
            return_value=build_requests_response(404, NOT_FOUND_BODY)
        ):
            self.assertIsNone(self.blockscout_client.get_contract_metadata("0x01"))

    def test_get_contract_metadata_http_error(self):
        """
        A non ok status is raised through the sync transport
        """
        with self.patch_session_get(return_value=build_requests_response(401, "{}")):
            with self.assertRaises(BlockscoutApiKeyError):
                self.blockscout_client.get_contract_metadata("0x01")

    def test_get_contract_metadata_connection_error(self):
        """
        Connection errors and a response that is not JSON are raised as
        BlockscoutConnectionError, without the API key in the message
        """
        with self.patch_session_get(side_effect=requests.ConnectionError):
            with self.assertRaises(BlockscoutConnectionError) as ctx:
                self.blockscout_client.get_contract_metadata("0x01")
            self.assertIsInstance(ctx.exception, ConnectionError)
            self.assertIsInstance(ctx.exception.__cause__, requests.ConnectionError)
            self.assertNotIn("test-key", str(ctx.exception))

        with self.patch_session_get(
            return_value=build_requests_response(200, "<html>not json</html>")
        ):
            with self.assertRaises(BlockscoutConnectionError) as ctx:
                self.blockscout_client.get_contract_metadata("0x01")
            self.assertIsInstance(ctx.exception.__cause__, json.JSONDecodeError)


class TestAsyncBlockscoutClientRequest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.blockscout_client = AsyncBlockscoutClient(
            EthereumNetwork.GNOSIS, api_key="test-key"
        )
        self.addAsyncCleanup(self.blockscout_client.async_session.close)

    def patch_session_get(self, **kwargs: Any) -> AbstractContextManager[Any]:
        return mock.patch.object(self.blockscout_client.async_session, "get", **kwargs)

    async def test_async_session_headers(self):
        """
        The aiohttp session sends the API key to the PRO API only
        """
        self.assertEqual(
            self.blockscout_client.async_session.headers["Authorization"],
            "Bearer test-key",
        )
        instance_blockscout_client = AsyncBlockscoutClient(
            EthereumNetwork.CELO_MAINNET, api_key="test-key"
        )
        self.addAsyncCleanup(instance_blockscout_client.async_session.close)
        self.assertNotIn(
            "Authorization", instance_blockscout_client.async_session.headers
        )

    async def test_async_get_contract_metadata_not_found(self):
        """
        No verified contract for the address returns None
        """
        with self.patch_session_get(
            return_value=AiohttpResponseMock(404, NOT_FOUND_BODY)
        ):
            self.assertIsNone(
                await self.blockscout_client.async_get_contract_metadata("0x01")
            )

    async def test_async_get_contract_metadata_http_error(self):
        """
        A non ok status is raised through the async transport
        """
        with self.patch_session_get(return_value=AiohttpResponseMock(401, "{}")):
            with self.assertRaises(BlockscoutApiKeyError):
                await self.blockscout_client.async_get_contract_metadata("0x01")

    async def test_async_get_contract_metadata_connection_error(self):
        """
        A timeout and a response that is not JSON are raised as
        BlockscoutConnectionError
        """
        with self.patch_session_get(side_effect=asyncio.TimeoutError):
            with self.assertRaises(BlockscoutConnectionError) as ctx:
                await self.blockscout_client.async_get_contract_metadata("0x01")
            self.assertIsInstance(ctx.exception.__cause__, asyncio.TimeoutError)

        with self.patch_session_get(
            return_value=AiohttpResponseMock(200, "<html>not json</html>")
        ):
            with self.assertRaises(BlockscoutConnectionError) as ctx:
                await self.blockscout_client.async_get_contract_metadata("0x01")
            self.assertIsInstance(ctx.exception.__cause__, json.JSONDecodeError)


@pytest.mark.network
class TestBlockscoutClient(unittest.TestCase):
    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_blockscout_client(self):
        blockscout_client = BlockscoutClient(
            EthereumNetwork.GNOSIS, api_key=get_blockscout_api_key()
        )
        contract_metadata = blockscout_client.get_contract_metadata(
            SAFE_MASTER_COPY_ADDRESS
        )
        self.assertEqual(contract_metadata.name, "GnosisSafe")
        self.assertEqual(contract_metadata.abi, sourcify_safe_metadata["output"]["abi"])
        self.assertEqual(contract_metadata.implementation, None)

        contract_metadata = blockscout_client.get_contract_metadata(SAFE_PROXY_ADDRESS)
        self.assertEqual(contract_metadata.name, "GnosisSafeProxy")
        self.assertEqual(
            contract_metadata.implementation, SAFE_PROXY_IMPLEMENTATION_ADDRESS
        )
        self.assertEqual(contract_metadata.abi, safe_proxy_abi_mock)

        self.assertIsNone(blockscout_client.get_contract_metadata(RANDOM_ADDRESS))

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_blockscout_client_wrong_api_key(self):
        """
        The PRO API rejects a wrong key, and the client raises instead of returning
        None
        """
        blockscout_client = BlockscoutClient(
            EthereumNetwork.GNOSIS, api_key="proapi_wrong"
        )
        with self.assertRaises(BlockscoutApiKeyError):
            blockscout_client.get_contract_metadata(SAFE_MASTER_COPY_ADDRESS)


@pytest.mark.network
class TestAsyncBlockscoutClient(unittest.IsolatedAsyncioTestCase):
    async def test_async_blockscout_client(self):
        blockscout_client = AsyncBlockscoutClient(
            EthereumNetwork.GNOSIS, api_key=get_blockscout_api_key()
        )
        self.addAsyncCleanup(blockscout_client.async_session.close)
        contract_metadata = await blockscout_client.async_get_contract_metadata(
            SAFE_MASTER_COPY_ADDRESS
        )
        self.assertEqual(contract_metadata.name, "GnosisSafe")
        self.assertEqual(contract_metadata.abi, sourcify_safe_metadata["output"]["abi"])
        self.assertEqual(contract_metadata.implementation, None)

        contract_metadata = await blockscout_client.async_get_contract_metadata(
            SAFE_PROXY_ADDRESS
        )
        self.assertEqual(contract_metadata.name, "GnosisSafeProxy")
        self.assertEqual(
            contract_metadata.implementation, SAFE_PROXY_IMPLEMENTATION_ADDRESS
        )
        self.assertEqual(contract_metadata.abi, safe_proxy_abi_mock)

        self.assertIsNone(
            await blockscout_client.async_get_contract_metadata(RANDOM_ADDRESS)
        )
