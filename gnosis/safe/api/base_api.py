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
        self.base_url = base_url or self.URL_BY_NETWORK.get(network)
        if not self.base_url:
            raise EthereumNetworkNotSupported(network)
        self.http_session = self._prepare_http_session()
        self.request_timeout = request_timeout

    def _prepare_http_session(self) -> requests.Session:
        """
        Prepare http session with custom pooling. See:
        https://urllib3.readthedocs.io/en/stable/advanced-usage.html
        https://docs.python-requests.org/en/v1.2.3/api/#requests.adapters.HTTPAdapter
        https://web3py.readthedocs.io/en/stable/providers.html#httpprovider
        """
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,  # Doing all the connections to the same url
            pool_maxsize=100,  # Number of concurrent connections
            pool_block=False,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @classmethod
    def from_ethereum_client(cls, ethereum_client: EthereumClient) -> "SafeBaseAPI":
        ethereum_network = ethereum_client.get_network()
        return cls(ethereum_network, ethereum_client=ethereum_client)

    def _get_request(self, url: str) -> requests.Response:
        full_url = urljoin(self.base_url, url)
        return self.http_session.get(full_url, timeout=self.request_timeout)

    def _post_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = urljoin(self.base_url, url)
        return self.http_session.post(
            full_url,
            json=payload,
            headers={"Content-type": "application/json"},
            timeout=self.request_timeout,
        )

    def _delete_request(self, url: str, payload: Dict) -> requests.Response:
        full_url = urljoin(self.base_url, url)
        return self.http_session.delete(
            full_url,
            json=payload,
            headers={"Content-type": "application/json"},
            timeout=self.request_timeout,
        )
