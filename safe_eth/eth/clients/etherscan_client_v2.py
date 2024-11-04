import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests

from safe_eth.eth import EthereumNetwork
from safe_eth.eth.clients import EtherscanClient


class EtherscanClientV2(EtherscanClient):
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
        :return: True if the network is supported; False otherwise.
        """
        supported_networks = cls.get_supported_networks()
        return any(
            item.get("chainid") == str(network.value) for item in supported_networks
        )
