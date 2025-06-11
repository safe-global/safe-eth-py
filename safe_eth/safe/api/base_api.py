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
        base_url = base_url or self.get_url_by_network(network)
        if not base_url:
            raise EthereumNetworkNotSupported(network)
        self.base_url = base_url
        self.api_key = api_key
        self.http_session = prepare_http_session(10, 100)
        self.request_timeout = request_timeout

    @abstractmethod
    def get_url_by_network(self, network: EthereumNetwork) -> Optional[str]:
        """
        Should return the base URL for the given network.
        :param network: EthereumNetwork to get the base URL for.
        :return: base URL for the given network. None if not found.
        """
        pass

    @classmethod
    def from_ethereum_client(cls, ethereum_client: EthereumClient) -> "SafeBaseAPI":
        ethereum_network = ethereum_client.get_network()
        return cls(ethereum_network, ethereum_client=ethereum_client)

    def _get_request(self, url: str) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return self.http_session.get(
            full_url, headers=headers, timeout=self.request_timeout
        )

    def _post_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return self.http_session.post(
            full_url,
            json=payload,
            headers=headers,
            timeout=self.request_timeout,
        )

    def _delete_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return self.http_session.delete(
            full_url,
            json=payload,
            headers=headers,
            timeout=self.request_timeout,
        )
