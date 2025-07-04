from abc import ABC, abstractmethod
from typing import Dict, Optional

import requests

from safe_eth.eth.ethereum_client import (
    EthereumClient,
    EthereumNetwork,
    EthereumNetworkNotSupported,
)
from safe_eth.util.http import build_full_url, prepare_http_session


class SafeAPIException(Exception):
    pass


class SafeBaseAPI(ABC):
    def __init__(
        self,
        network: EthereumNetwork,
        ethereum_client: Optional[EthereumClient] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        request_timeout: int = 10,
    ):
        """
        :param network: Network for the transaction service
        :param ethereum_client:
        :param base_url: If a custom transaction service is used
        :param api_key: Api key of authenticated Safe services
        :raises: EthereumNetworkNotSupported
        """
        self.network = network
        self.ethereum_client = ethereum_client
        self.base_url = self._get_api_base_url(network, base_url)
        self.api_key = api_key
        self.http_session = prepare_http_session(10, 100)
        self.request_timeout = request_timeout

    @abstractmethod
    def _get_url_by_network(self, network: EthereumNetwork) -> Optional[str]:
        """
        Should return the base URL for the given network.
        :param network: EthereumNetwork to get the base URL for.
        :return: base URL for the given network. None if not found.
        """
        pass

    def _get_api_base_url(
        self, network: EthereumNetwork, custom_base_url: Optional[str] = None
    ) -> str:
        """
        Returns the base API URL for the specified Ethereum network.
        If a custom_base_url is provided, it will be used instead of the default.
        Otherwise, the method attempts to retrieve the URL associated with the given network.

        :param network: The EthereumNetwork to get the base URL for.
        :param custom_base_url: Optional custom base URL to override the default.
        :return: The base URL corresponding to the specified network.
        :raises EthereumNetworkNotSupported: If the network is not supported and no URL is found.
        """
        base_url = custom_base_url or self._get_url_by_network(network)
        if not base_url:
            raise EthereumNetworkNotSupported(network)
        return base_url

    @classmethod
    def from_ethereum_client(
        cls,
        ethereum_client: EthereumClient,
        api_key: Optional[str] = None,
    ) -> "SafeBaseAPI":
        ethereum_network = ethereum_client.get_network()
        return cls(ethereum_network, ethereum_client=ethereum_client, api_key=api_key)

    def _get_request_headers(self, include_json_body: bool = False) -> Dict[str, str]:
        """
        Build the default HTTP headers for a request.

        :param include_json_body: If it includes the JSON Content-Type header.
        :return: Dictionary of headers to include in the request.
        """
        headers = {}
        if include_json_body:
            headers["Content-Type"] = "application/json"
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _get_request(self, url: str) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        return self.http_session.get(
            full_url, headers=self._get_request_headers(), timeout=self.request_timeout
        )

    def _post_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        return self.http_session.post(
            full_url,
            json=payload,
            headers=self._get_request_headers(include_json_body=True),
            timeout=self.request_timeout,
        )

    def _delete_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        return self.http_session.delete(
            full_url,
            json=payload,
            headers=self._get_request_headers(include_json_body=True),
            timeout=self.request_timeout,
        )
