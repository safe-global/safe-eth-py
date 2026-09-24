import json
import os
import time
from typing import Any, Dict, List, MutableMapping, Optional, Union
from urllib.parse import urljoin

import aiohttp
import requests

from safe_eth.eth import EthereumNetwork
from safe_eth.eth.clients import ContractMetadata
from safe_eth.util.http import prepare_http_session, wrap_http_exceptions


class EtherscanClientException(Exception):
    pass


class EtherscanClientConfigurationProblem(Exception):
    pass


class EtherscanRateLimitError(EtherscanClientException):
    pass


class EtherscanDailyRateLimitError(EtherscanRateLimitError):
    """
    Daily quota of the API key is used. It is not retried, as it only resets the next
    day.
    """


class EtherscanConnectionError(EtherscanClientException, ConnectionError):
    """
    Etherscan could not be reached, or its response could not be decoded. It is also
    a builtin ``ConnectionError``, so callers that catch connection errors catch it.
    """


class EtherscanHttpError(EtherscanClientException):
    """
    Etherscan answered with a non ok HTTP status code other than the rate limit one.
    """

    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Error connecting to Etherscan, HTTP {status_code}")


class EtherscanClientV2:
    """
    Etherscan API V2 supports multiple chains in the same url.

    Reference: https://docs.etherscan.io/etherscan-v2
    """

    BASE_API_V2_URL = "https://api.etherscan.io"
    HTTP_HEADERS: MutableMapping[str, Union[str, bytes]] = {
        "User-Agent": "curl/7.77.0",
    }
    # Error meaning the request was fine but Etherscan has nothing indexed for the
    # address, returned by ``getabi`` with ``status: "0"`` (``getsourcecode`` returns
    # ``status: "1"`` with an empty ABI instead, handled in
    # ``_process_get_contract_source_code_response``)
    NOT_FOUND_MESSAGE = "contract source code not verified"

    def __init__(
        self,
        network: EthereumNetwork,
        api_key: Optional[str] = None,
        request_timeout: int = int(
            os.environ.get("ETHERSCAN_CLIENT_REQUEST_TIMEOUT", 10)
        ),
    ):
        self.api_key = api_key
        self.network = network
        self.base_api_url = self.BASE_API_V2_URL
        self.http_session = prepare_http_session(10, 100)
        self.http_session.headers = self.HTTP_HEADERS
        self.request_timeout = request_timeout

    def build_url(self, query: str) -> str:
        url = urljoin(self.base_api_url, f"v2/api?chainid={self.network.value}&{query}")
        if self.api_key:
            url += f"&apikey={self.api_key}"
        return url

    @staticmethod
    def _build_http_error(status_code: int) -> EtherscanClientException:
        """
        :param status_code: Status code of a not ok HTTP response
        :return: Exception matching the status code
        """
        if status_code == 429:
            return EtherscanRateLimitError(f"Rate limit reached, HTTP {status_code}")
        return EtherscanHttpError(status_code)

    @classmethod
    def _process_response_json(
        cls, response_json: Dict[str, Any]
    ) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        """
        Etherscan answers with HTTP 200 for errors too, they are encoded in the payload:
        ``status`` is ``"0"`` and ``result`` holds the error message.

        :param response_json: Decoded Etherscan response
        :return: ``result`` if the query succeeded, ``None`` if the query was valid but
            Etherscan has nothing indexed for the address
        :raises EtherscanRateLimitError: If any of the rate limits was reached
        :raises EtherscanClientException: For any other API error
        """
        result = response_json.get("result")
        if response_json.get("status") == "1":
            return result

        # `result` holds the error message, but it can be null for some errors. `message`
        # can be null too, so `or ""` is needed on top of the `.get` default
        message = (
            result
            if isinstance(result, str)
            else str(response_json.get("message") or "")
        )
        lowered_message = message.lower()
        if "rate limit" in lowered_message:
            # The per second, per day and free tier limits each have their own wording
            if "daily" in lowered_message:
                raise EtherscanDailyRateLimitError(message)
            raise EtherscanRateLimitError(message)
        if cls.NOT_FOUND_MESSAGE in lowered_message:
            return None
        raise EtherscanClientException(message or "Unknown Etherscan API error")

    def _do_request(self, url: str) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        with wrap_http_exceptions(url, EtherscanConnectionError):
            response = self.http_session.get(url, timeout=self.request_timeout)
            if not response.ok:
                raise self._build_http_error(response.status_code)
            return self._process_response_json(response.json())

    def _retry_request(
        self, url: str, retry: bool = True
    ) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        """
        :param url: Url to request
        :param retry: If ``True``, wait and try again when the rate limit is reached,
            up to 3 attempts
        :return: Decoded ``result`` of the response, ``None`` if Etherscan has nothing
            indexed for the address
        :raises EtherscanRateLimitError: If the rate limit is still reached on the last
            attempt
        :raises EtherscanDailyRateLimitError: When the daily quota is used, with no retry
        :raises EtherscanClientException: For any other error, with no retry
        """
        for _ in range(2):
            try:
                return self._do_request(url)
            except EtherscanDailyRateLimitError:
                raise
            except EtherscanRateLimitError:
                if not retry:
                    raise
                time.sleep(5)
        return self._do_request(url)

    @classmethod
    def get_supported_networks(cls) -> List[Dict[str, Any]]:
        """
        Fetches a list of supported networks by the Etherscan API v2.

        :return: List of supported networks, or empty list if request fails.

        Example response
        ```
        {
            "chainname":"Ethereum Mainnet",
            "chainid":"1",
            "blockexplorer":"https://etherscan.io",
            "apiurl":"https://api.etherscan.io/v2/api?chainid=1",
            "status":1
        },
        {
            "chainname":"Sepolia Testnet",
            "chainid":"11155111",
            "blockexplorer":"https://sepolia.etherscan.io",
            "apiurl":"https://api.etherscan.io/v2/api?chainid=11155111",
            "status":1
        }
        ```
        """
        url = urljoin(cls.BASE_API_V2_URL, "v2/chainlist")
        response = requests.get(url)
        if response.ok:
            return response.json().get("result", [])
        return []

    @classmethod
    def is_supported_network(cls, network: EthereumNetwork) -> bool:
        """
        Checks if a given Ethereum network is supported by the Etherscan API v2.

        :param network: The Ethereum network to check.
        :return: `True` if the network is supported; `False` otherwise.
        """
        supported_networks = cls.get_supported_networks()
        return any(
            item.get("chainid") == str(network.value) for item in supported_networks
        )

    def get_base_url(self) -> Optional[str]:
        """
        :param network: The Ethereum network to check.
        :return: Base url for the current network
        """
        for network in self.get_supported_networks():
            if network.get("chainid") == str(self.network.value):
                return network.get("blockexplorer")
        return None

    @staticmethod
    def _process_contract_metadata(
        contract_data: Dict[str, Any],
    ) -> Optional[ContractMetadata]:
        contract_name = contract_data["ContractName"]
        contract_abi = contract_data["ABI"]
        contract_proxy_implementation_address = (
            contract_data.get("Implementation") or None
        )
        if contract_abi:
            return ContractMetadata(
                contract_name,
                contract_abi,
                False,
                contract_proxy_implementation_address,
            )
        return None

    def get_contract_metadata(
        self, contract_address: str, retry: bool = True
    ) -> Optional[ContractMetadata]:
        contract_source_code = self.get_contract_source_code(
            contract_address, retry=retry
        )
        if contract_source_code:
            return self._process_contract_metadata(contract_source_code)
        return None

    @staticmethod
    def _process_get_contract_source_code_response(response):
        if response and isinstance(response, list):
            result = response[0]
            abi_str = result.get("ABI")

            if isinstance(abi_str, str) and abi_str.startswith("["):
                try:
                    result["ABI"] = json.loads(abi_str)
                except json.JSONDecodeError:
                    result["ABI"] = None  # Handle the case where JSON decoding fails
            else:
                result["ABI"] = None

            return result

    def get_contract_source_code(self, contract_address: str, retry: bool = True):
        """
        Get source code for a contract. Source code query also returns:

            - ContractName: "",
            - CompilerVersion: "",
            - OptimizationUsed: "",
            - Runs: "",
            - ConstructorArguments: ""
            - EVMVersion: "Default",
            - Library: "",
            - LicenseType: "",
            - Proxy: "0",
            - Implementation: "",
            - SwarmSource: ""

        :param contract_address:
        :param retry: if ``True``, try again if there's Rate Limit Error
        :return:
        """
        url = self.build_url(
            f"module=contract&action=getsourcecode&address={contract_address}"
        )
        response = self._retry_request(url, retry=retry)  # Returns a list
        return self._process_get_contract_source_code_response(response)

    def get_contract_abi(self, contract_address: str, retry: bool = True):
        url = self.build_url(
            f"module=contract&action=getabi&address={contract_address}"
        )
        result = self._retry_request(url, retry=retry)
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                pass
        return None


class AsyncEtherscanClientV2(EtherscanClientV2):
    def __init__(
        self,
        network: EthereumNetwork,
        api_key: Optional[str] = None,
        request_timeout: int = int(
            os.environ.get("ETHERSCAN_CLIENT_REQUEST_TIMEOUT", 10)
        ),
        max_requests: int = int(os.environ.get("ETHERSCAN_CLIENT_MAX_REQUESTS", 100)),
    ):
        super().__init__(network, api_key, request_timeout)
        self.async_session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit_per_host=max_requests)
        )

    async def _async_do_request(
        self, url: str
    ) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        """
        Async version of _do_request
        """
        with wrap_http_exceptions(url, EtherscanConnectionError):
            async with self.async_session.get(
                url, timeout=self.request_timeout
            ) as response:
                if not response.ok:
                    raise self._build_http_error(response.status)
                return self._process_response_json(await response.json())

    async def async_get_contract_source_code(
        self,
        contract_address: str,
    ):
        """
        Asynchronous version of get_contract_source_code
        Does not implement retries

        :param contract_address:
        """
        url = self.build_url(
            f"module=contract&action=getsourcecode&address={contract_address}"
        )
        response = await self._async_do_request(url)  # Returns a list
        return self._process_get_contract_source_code_response(response)

    async def async_get_contract_metadata(
        self, contract_address: str
    ) -> Optional[ContractMetadata]:
        contract_source_code = await self.async_get_contract_source_code(
            contract_address
        )
        if contract_source_code:
            return self._process_contract_metadata(contract_source_code)
        return None

    async def async_get_contract_abi(self, contract_address: str):
        url = self.build_url(
            f"module=contract&action=getabi&address={contract_address}"
        )
        result = await self._async_do_request(url)
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                pass
        return None
