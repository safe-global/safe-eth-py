import json
import os
import time
from typing import Any, Dict, List, MutableMapping, Optional, Union
from urllib.parse import urljoin

import aiohttp
import requests

from safe_eth.eth import EthereumNetwork
from safe_eth.eth.clients import ContractMetadata
from safe_eth.util.http import prepare_http_session


class EtherscanClientException(Exception):
    pass


class EtherscanClientConfigurationProblem(Exception):
    pass


class EtherscanRateLimitError(EtherscanClientException):
    pass


class EtherscanClientV2:
    """
    Etherscan API V2 supports multiple chains in the same url.

    Reference: https://docs.etherscan.io/etherscan-v2
    """

    BASE_API_V2_URL = "https://api.etherscan.io"
    HTTP_HEADERS: MutableMapping[str, Union[str, bytes]] = {
        "User-Agent": "curl/7.77.0",
    }

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

    def _do_request(self, url: str) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        response = self.http_session.get(url, timeout=self.request_timeout)

        if response.ok:
            response_json = response.json()
            result = response_json["result"]
            if "Max rate limit reached" in result:
                # Max rate limit reached, please use API Key for higher rate limit
                raise EtherscanRateLimitError
            if response_json["status"] == "1":
                return result
        return None

    def _retry_request(
        self, url: str, retry: bool = True
    ) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        for _ in range(3):
            try:
                return self._do_request(url)
            except EtherscanRateLimitError as exc:
                if not retry:
                    raise exc
                else:
                    time.sleep(5)
        return None

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
        contract_data: Dict[str, Any]
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
        async with self.async_session.get(
            url, timeout=self.request_timeout
        ) as response:
            if response.ok:
                response_json = await response.json()
                result = response_json["result"]
                if "Max rate limit reached" in result:
                    # Max rate limit reached, please use API Key for higher rate limit
                    raise EtherscanRateLimitError
                if response_json["status"] == "1":
                    return result
            return None

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
