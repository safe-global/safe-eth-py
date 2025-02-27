import json
import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import aiohttp
import requests

from safe_eth.eth import EthereumNetwork
from safe_eth.eth.clients import (
    ContractMetadata,
    EtherscanClient,
    EtherscanRateLimitError,
)


class EtherscanClientV2(EtherscanClient):
    """
    Etherscan API V2 supports multiple chains in the same url.

    Reference: https://docs.etherscan.io/etherscan-v2
    """

    BASE_API_V2_URL = "https://api.etherscan.io"

    def __init__(
        self,
        network: EthereumNetwork,
        api_key: Optional[str] = None,
        request_timeout: int = int(
            os.environ.get("ETHERSCAN_CLIENT_REQUEST_TIMEOUT", 10)
        ),
    ):
        super().__init__(EthereumNetwork.MAINNET, api_key, request_timeout)
        self.network = network
        self.base_api_url = self.BASE_API_V2_URL

    def build_url(self, query: str) -> str:
        url = urljoin(self.base_api_url, f"v2/api?chainid={self.network.value}&{query}")
        if self.api_key:
            url += f"&apikey={self.api_key}"
        return url

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
