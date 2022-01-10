import json
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .. import EthereumNetwork
from .contract_metadata import ContractMetadata


class EtherscanClientException(Exception):
    pass


class EtherscanClientConfigurationProblem(Exception):
    pass


class EtherscanRateLimitError(EtherscanClientException):
    pass


class EtherscanClient:
    NETWORK_WITH_URL = {
        EthereumNetwork.MAINNET: "https://etherscan.io",
        EthereumNetwork.RINKEBY: "https://rinkeby.etherscan.io",
        EthereumNetwork.ROPSTEN: "https://ropsten.etherscan.io",
        EthereumNetwork.GOERLI: "https://goerli.etherscan.io",
        EthereumNetwork.KOVAN: "https://kovan.etherscan.io",
        EthereumNetwork.BINANCE: "https://bscscan.com",
        EthereumNetwork.MATIC: "https://polygonscan.com",
        EthereumNetwork.OPTIMISTIC: "https://optimistic.etherscan.io",
        EthereumNetwork.ARBITRUM: "https://arbiscan.io",
        EthereumNetwork.AVALANCHE: "https://snowtrace.io",
    }

    NETWORK_WITH_API_URL = {
        EthereumNetwork.MAINNET: "https://api.etherscan.io",
        EthereumNetwork.RINKEBY: "https://api-rinkeby.etherscan.io",
        EthereumNetwork.ROPSTEN: "https://api-ropsten.etherscan.io",
        EthereumNetwork.GOERLI: "https://api-goerli.etherscan.io/",
        EthereumNetwork.KOVAN: "https://api-kovan.etherscan.io/",
        EthereumNetwork.BINANCE: "https://api.bscscan.com",
        EthereumNetwork.MATIC: "https://api.polygonscan.com",
        EthereumNetwork.OPTIMISTIC: "https://api-optimistic.etherscan.io",
        EthereumNetwork.ARBITRUM: "https://api.arbiscan.io",
        EthereumNetwork.AVALANCHE: "https://api.snowtrace.io",
    }
    HTTP_HEADERS = {
        "User-Agent": "curl/7.77.0",
    }

    def __init__(self, network: EthereumNetwork, api_key: Optional[str] = None):
        self.network = network
        self.api_key = api_key
        self.base_url = self.NETWORK_WITH_URL.get(network)
        self.base_api_url = self.NETWORK_WITH_API_URL.get(network)
        if self.base_api_url is None:
            raise EtherscanClientConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )
        self.http_session = requests.Session()
        self.http_session.headers = self.HTTP_HEADERS

    def build_url(self, path: str):
        url = urljoin(self.base_api_url, path)
        if self.api_key:
            url += f"&apikey={self.api_key}"
        return url

    def _do_request(self, url: str) -> Optional[Dict[str, Any]]:
        response = self.http_session.get(url)

        if response.ok:
            response_json = response.json()
            result = response_json["result"]
            if "Max rate limit reached" in result:
                # Max rate limit reached, please use API Key for higher rate limit
                raise EtherscanRateLimitError
            if response_json["status"] == "1":
                return result

    def _retry_request(self, url: str, retry: bool = True) -> Optional[Dict[str, Any]]:
        for _ in range(3):
            try:
                return self._do_request(url)
            except EtherscanRateLimitError as exc:
                if not retry:
                    raise exc
                else:
                    time.sleep(5)

    def get_contract_metadata(
        self, contract_address: str, retry: bool = True
    ) -> Optional[ContractMetadata]:
        contract_source_code = self.get_contract_source_code(
            contract_address, retry=retry
        )
        if contract_source_code:
            contract_name = contract_source_code["ContractName"]
            contract_abi = contract_source_code["ABI"]
            if contract_abi:
                return ContractMetadata(contract_name, contract_abi, False)

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
            f"api?module=contract&action=getsourcecode&address={contract_address}"
        )
        result = self._retry_request(url, retry=retry)  # Returns a list
        if result:
            result = result[0]
            abi_str = result["ABI"]
            result["ABI"] = json.loads(abi_str) if abi_str.startswith("[") else None
            return result

    def get_contract_abi(self, contract_address: str, retry: bool = True):
        url = self.build_url(
            f"api?module=contract&action=getabi&address={contract_address}"
        )
        result = self._retry_request(url, retry=retry)
        if result:
            return json.loads(result)
