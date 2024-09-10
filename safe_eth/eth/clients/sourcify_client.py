import os
from functools import cache
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from ...util.http import prepare_http_session
from .. import EthereumNetwork
from ..utils import fast_is_checksum_address
from .contract_metadata import ContractMetadata


class SourcifyClientException(Exception):
    pass


class SourcifyClientConfigurationProblem(Exception):
    pass


class SourcifyClient:
    """
    Get contract metadata from Sourcify. Matches can be full or partial:

      - Full: Both the source files as well as the meta data files were an exact match between the deployed bytecode
        and the published files.
      - Partial: Source code compiles to the same bytecode and thus the contract behaves in the same way,
        but the source code can be different: Variables can have misleading names,
        comments can be different and especially the NatSpec comments could have been modified.

    """

    def __init__(
        self,
        network: EthereumNetwork = EthereumNetwork.MAINNET,
        base_url_api: str = "https://sourcify.dev",
        base_url_repo: str = "https://repo.sourcify.dev/",
        request_timeout: int = int(
            os.environ.get("SOURCIFY_CLIENT_REQUEST_TIMEOUT", 10)
        ),
    ):
        self.network = network
        self.base_url_api = base_url_api
        self.base_url_repo = base_url_repo
        self.http_session = prepare_http_session(10, 100)
        self.request_timeout = request_timeout

        if not self.is_chain_supported(network.value):
            raise SourcifyClientConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )

    def _get_abi_from_metadata(self, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        return metadata["output"]["abi"]

    def _get_name_from_metadata(self, metadata: Dict[str, Any]) -> Optional[str]:
        values = list(metadata["settings"].get("compilationTarget", {}).values())
        if values:
            return values[0]
        return None

    def _do_request(self, url: str) -> Optional[Dict[str, Any]]:
        response = self.http_session.get(url, timeout=self.request_timeout)
        if not response.ok:
            return None

        return response.json()

    def is_chain_supported(self, chain_id: int) -> bool:
        chains = self.get_chains()
        if not chains:
            raise IOError("Cannot get chains for SourcifyClient")
        for chain in chains:
            if not isinstance(chain, dict):
                continue
            chain_id_str = chain.get("chainId")
            if chain_id_str is None:
                continue
            try:
                if chain_id == int(chain_id_str):
                    return True
            except ValueError:
                continue
        return False

    @cache
    def get_chains(self) -> Dict[str, Any]:
        url = urljoin(self.base_url_api, "/server/chains")
        result = self._do_request(url)
        return result or {}

    def get_contract_metadata(
        self, contract_address: str
    ) -> Optional[ContractMetadata]:
        assert fast_is_checksum_address(
            contract_address
        ), "Expecting a checksummed address"

        for match_type in ("full_match", "partial_match"):
            url = urljoin(
                self.base_url_repo,
                f"/contracts/{match_type}/{self.network.value}/{contract_address}/metadata.json",
            )
            metadata = self._do_request(url)
            if metadata:
                abi = self._get_abi_from_metadata(metadata)
                name = self._get_name_from_metadata(metadata)
                return ContractMetadata(name, abi, match_type == "partial_match")
        return None
