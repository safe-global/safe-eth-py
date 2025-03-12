from abc import ABC
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
    URL_BY_NETWORK: Dict[EthereumNetwork, str] = {}

    def __init__(
        self,
        network: EthereumNetwork,
        ethereum_client: Optional[EthereumClient] = None,
        base_url: Optional[str] = None,
        request_timeout: int = 10,
    ):
        """
        :param network: Network for the transaction service
        :param ethereum_client:
        :param base_url: If a custom transaction service is used
        :raises: EthereumNetworkNotSupported
        """
        self.network = network
        self.ethereum_client = ethereum_client
        self.base_url = base_url or self.URL_BY_NETWORK.get(network, "")
        if not self.base_url:
            raise EthereumNetworkNotSupported(network)
        self.http_session = prepare_http_session(10, 100)
        self.request_timeout = request_timeout

    @classmethod
    def from_ethereum_client(cls, ethereum_client: EthereumClient) -> "SafeBaseAPI":
        ethereum_network = ethereum_client.get_network()
        return cls(ethereum_network, ethereum_client=ethereum_client)

    def _get_request(self, url: str) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        return self.http_session.get(full_url, timeout=self.request_timeout)

    def _post_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        return self.http_session.post(
            full_url,
            json=payload,
            headers={"Content-type": "application/json"},
            timeout=self.request_timeout,
        )

    def _delete_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = build_full_url(self.base_url, url)
        return self.http_session.delete(
            full_url,
            json=payload,
            headers={"Content-type": "application/json"},
            timeout=self.request_timeout,
        )
