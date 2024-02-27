import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional

from eth_typing import ChecksumAddress, HexStr

from gnosis.util.http import prepare_http_session

from .exceptions import BundlerClientConnectionException, BundlerClientResponseException
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

    def __str__(self):
        return f"Bundler client at {self.url}"

    def _do_request(self, payload: Dict[Any, Any]) -> Optional[Dict[str, Any]]:
        """
        :param payload:
        :return: Result of the request
        :raises BundlerClientConnectionException: If there's a problem connecting to the bundler
        :raises BundlerClientResponseException: If the request from the bundler contains an error
        """
        try:
            response = self.http_session.post(self.url, json=payload)
        except IOError as exception:
            raise BundlerClientConnectionException(
                f"Error connecting to bundler {self.url} : {exception}"
            )

        if not response.ok:
            raise BundlerClientConnectionException(
                f"Error connecting to bundler {self.url} : {response.status_code} {response.content}"
            )

        response_json = response.json()
        result = response_json.get("result")
        if not result and "error" in response_json:
            error_str = f'Bundler returned error for payload {payload} : {response_json["error"]}'
            logger.warning(error_str)
            raise BundlerClientResponseException(error_str)
        return result

    @lru_cache(maxsize=1024)
    def get_user_operation_by_hash(
        self, user_operation_hash: HexStr
    ) -> Optional[UserOperation]:
        """
        https://docs.alchemy.com/reference/eth-getuseroperationbyhash

        :param user_operation_hash:
        :return:
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getUserOperationByHash",
            "params": [user_operation_hash],
            "id": 1,
        }
        result = self._do_request(payload)
        return (
            UserOperation.from_bundler_response(user_operation_hash, result)
            if result
            else None
        )

    @lru_cache(maxsize=1024)
    def get_user_operation_receipt(
        self, user_operation_hash: HexStr
    ) -> Optional[Dict[str, Any]]:
        """
        https://docs.alchemy.com/reference/eth-getuseroperationreceipt

        :param user_operation_hash:
        :return:
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getUserOperationReceipt",
            "params": [user_operation_hash],
            "id": 1,
        }
        return self._do_request(payload)

    @lru_cache(maxsize=None)
    def supported_entry_points(self) -> List[ChecksumAddress]:
        """
        https://docs.alchemy.com/reference/eth-supportedentrypoints

        :return:
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_supportedEntryPoints",
            "params": [],
            "id": 1,
        }
        return self._do_request(payload)
