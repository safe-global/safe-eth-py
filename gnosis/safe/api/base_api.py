from abc import ABC
from typing import Dict, Optional
from urllib.parse import urljoin

import requests

from gnosis.eth.ethereum_client import (
    EthereumClient,
    EthereumNetwork,
    EthereumNetworkNotSupported,
)


class SafeAPIException(Exception):
    pass


class SafeBaseAPI(ABC):
    URL_BY_NETWORK: Dict[EthereumNetwork, str] = {}

    def __init__(
        self,
        network: EthereumNetwork,
        ethereum_client: Optional[EthereumClient] = None,
        base_url: Optional[str] = None,
    ):
        """
        :param network: Network for the transaction service
        :param ethereum_client:
        :param base_url: If a custom transaction service is used
        :raises: EthereumNetworkNotSupported
        """
        self.network = network
        self.ethereum_client = ethereum_client
        self.base_url = base_url or self.URL_BY_NETWORK.get(network)
        if not self.base_url:
            raise EthereumNetworkNotSupported(network)

    @classmethod
    def from_ethereum_client(cls, ethereum_client: EthereumClient) -> "SafeBaseAPI":
        ethereum_network = ethereum_client.get_network()
        return cls(ethereum_network, ethereum_client=ethereum_client)

    def _get_request(self, url: str) -> requests.Response:
        full_url = urljoin(self.base_url, url)
        return requests.get(full_url)

    def _post_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = urljoin(self.base_url, url)
        return requests.post(
            full_url, json=payload, headers={"Content-type": "application/json"}
        )

    def _delete_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = urljoin(self.base_url, url)
        return requests.delete(
            full_url, json=payload, headers={"Content-type": "application/json"}
        )
