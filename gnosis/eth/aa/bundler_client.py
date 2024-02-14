import logging
from typing import Any, Dict, List, Optional

from eth_typing import ChecksumAddress, HexStr

from gnosis.util.http import prepare_http_session

from .user_operation import UserOperation

logger = logging.getLogger(__name__)


class BundlerClient:
    """
    Account Abstraction client for EIP4337 bundlers
    """

    def __init__(
        self,
        url: str,
        retry_count: int = 1,
    ):
        self.url = url
        self.retry_count = retry_count
        self.http_session = prepare_http_session(1, 100, retry_count=retry_count)

    def _do_request(self, payload: Dict[Any, Any]) -> Optional[Dict[str, Any]]:
        response = self.http_session.post(self.url, json=payload)
        if not response.ok:
            raise ConnectionError(
                f"Error connecting to bundler {self.url} : {response.status_code} {response.content}"
            )

        response_json = response.json()
        result = response_json.get("result")
        if not result and "error" in response_json:
            logger.warning(
                "Bundler returned error for payload %s : %s",
                payload,
                response_json["error"],
            )
        return result

    def get_user_operation_by_hash(
        self, user_operation_hash: HexStr
    ) -> Optional[UserOperation]:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getUserOperationByHash",
            "params": [user_operation_hash],
            "id": 1,
        }
        result = self._do_request(payload)
        return UserOperation(user_operation_hash, result) if result else None

    def get_user_operation_receipt(
        self, user_operation_hash: HexStr
    ) -> Optional[Dict[str, Any]]:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getUserOperationReceipt",
            "params": [user_operation_hash],
            "id": 1,
        }
        return self._do_request(payload)

    def supported_entry_points(self) -> List[ChecksumAddress]:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_supportedEntryPoints",
            "params": [],
            "id": 1,
        }
        return self._do_request(payload)
