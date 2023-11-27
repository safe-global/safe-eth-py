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
        EthereumNetwork.BINANCE_SMART_CHAIN_MAINNET: "https://bscscan.com",
        EthereumNetwork.POLYGON: "https://polygonscan.com",
        EthereumNetwork.POLYGON_ZKEVM: "https://zkevm.polygonscan.com",
        EthereumNetwork.OPTIMISM: "https://optimistic.etherscan.io",
        EthereumNetwork.ARBITRUM_ONE: "https://arbiscan.io",
        EthereumNetwork.ARBITRUM_NOVA: "https://nova.arbiscan.io",
        EthereumNetwork.ARBITRUM_GOERLI: "https://goerli.arbiscan.io",
        EthereumNetwork.AVALANCHE_C_CHAIN: "https://snowtrace.io",
        EthereumNetwork.GNOSIS: "https://gnosisscan.io",
        EthereumNetwork.MOONBEAM: "https://moonscan.io",
        EthereumNetwork.MOONRIVER: "https://moonriver.moonscan.io",
        EthereumNetwork.MOONBASE_ALPHA: "https://moonbase.moonscan.io",
        EthereumNetwork.CRONOS_MAINNET_BETA: "https://cronoscan.com",
        EthereumNetwork.CRONOS_TESTNET: "https://testnet.cronoscan.com",
        EthereumNetwork.CELO_MAINNET: "https://celoscan.io",
        EthereumNetwork.BASE_GOERLI_TESTNET: "https://goerli.basescan.org",
        EthereumNetwork.NEON_EVM_DEVNET: "https://devnet.neonscan.org",
        EthereumNetwork.NEON_EVM_MAINNET: "https://neonscan.org",
        EthereumNetwork.SEPOLIA: "https://sepolia.etherscan.io",
        EthereumNetwork.ZKSYNC_V2: "https://explorer.zksync.io/",
        EthereumNetwork.FANTOM_OPERA: "https://ftmscan.com",
        EthereumNetwork.FANTOM_TESTNET: "https://testnet.ftmscan.com/",
        EthereumNetwork.LINEA: "https://www.lineascan.build",
        EthereumNetwork.LINEA_TESTNET: "https://goerli.lineascan.build",
        EthereumNetwork.MANTLE: "https://explorer.mantle.xyz",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "https://sepolia.scrollscan.dev",
        EthereumNetwork.SCROLL: "https://scrollscan.com",
    }

    NETWORK_WITH_API_URL = {
        EthereumNetwork.MAINNET: "https://api.etherscan.io",
        EthereumNetwork.RINKEBY: "https://api-rinkeby.etherscan.io",
        EthereumNetwork.ROPSTEN: "https://api-ropsten.etherscan.io",
        EthereumNetwork.GOERLI: "https://api-goerli.etherscan.io",
        EthereumNetwork.KOVAN: "https://api-kovan.etherscan.io",
        EthereumNetwork.BINANCE_SMART_CHAIN_MAINNET: "https://api.bscscan.com",
        EthereumNetwork.POLYGON: "https://api.polygonscan.com",
        EthereumNetwork.POLYGON_ZKEVM: "https://api-zkevm.polygonscan.com",
        EthereumNetwork.OPTIMISM: "https://api-optimistic.etherscan.io",
        EthereumNetwork.ARBITRUM_ONE: "https://api.arbiscan.io",
        EthereumNetwork.ARBITRUM_NOVA: "https://api-nova.arbiscan.io",
        EthereumNetwork.ARBITRUM_GOERLI: "https://api-goerli.arbiscan.io",
        EthereumNetwork.ARBITRUM_SEPOLIA: "https://api-sepolia.arbiscan.io",
        EthereumNetwork.AVALANCHE_C_CHAIN: "https://api.snowtrace.io",
        EthereumNetwork.GNOSIS: "https://api.gnosisscan.io",
        EthereumNetwork.MOONBEAM: "https://api-moonbeam.moonscan.io",
        EthereumNetwork.MOONRIVER: "https://api-moonriver.moonscan.io",
        EthereumNetwork.MOONBASE_ALPHA: "https://api-moonbase.moonscan.io",
        EthereumNetwork.CRONOS_MAINNET_BETA: "https://api.cronoscan.com",
        EthereumNetwork.CRONOS_TESTNET: "https://api-testnet.cronoscan.com",
        EthereumNetwork.CELO_MAINNET: "https://api.celoscan.io",
        EthereumNetwork.BASE_GOERLI_TESTNET: "https://api-goerli.basescan.org",
        EthereumNetwork.NEON_EVM_DEVNET: "https://devnet-api.neonscan.org",
        EthereumNetwork.NEON_EVM_MAINNET: "https://api.neonscan.org",
        EthereumNetwork.SEPOLIA: "https://api-sepolia.etherscan.io",
        EthereumNetwork.ZKSYNC_V2: "https://block-explorer-api.mainnet.zksync.io/",
        EthereumNetwork.FANTOM_OPERA: "https://api.ftmscan.com",
        EthereumNetwork.FANTOM_TESTNET: "https://api-testnet.ftmscan.com",
        EthereumNetwork.LINEA: "https://api.lineascan.build",
        EthereumNetwork.LINEA_TESTNET: "https://api-testnet.lineascan.build",
        EthereumNetwork.MANTLE: "https://explorer.mantle.xyz",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org/api",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org/api",
        EthereumNetwork.SCROLL_SEPOLIA_TESTNET: "https://api-sepolia.scrollscan.dev",
        EthereumNetwork.SCROLL: "https://api.scrollscan.com",
    }
    HTTP_HEADERS = {
        "User-Agent": "curl/7.77.0",
    }

    def __init__(
        self,
        network: EthereumNetwork,
        api_key: Optional[str] = None,
        request_timeout: int = 10,
    ):
        self.network = network
        self.api_key = api_key
        self.base_url = self.NETWORK_WITH_URL.get(network)
        self.base_api_url = self.NETWORK_WITH_API_URL.get(network)
        if self.base_api_url is None:
            raise EtherscanClientConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )
        self.http_session = self._prepare_http_session()
        self.http_session.headers = self.HTTP_HEADERS
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
            pool_connections=10,
            pool_maxsize=100,
            pool_block=False,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def build_url(self, path: str):
        url = urljoin(self.base_api_url, path)
        if self.api_key:
            url += f"&apikey={self.api_key}"
        return url

    def _do_request(self, url: str) -> Optional[Dict[str, Any]]:
        response = self.http_session.get(url, timeout=self.request_timeout)

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
