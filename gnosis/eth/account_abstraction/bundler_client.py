import logging
from functools import cache, lru_cache
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes

from gnosis.util.http import prepare_http_session

from .exceptions import BundlerClientConnectionException, BundlerClientResponseException
from .user_operation import UserOperation
from .user_operation_receipt import UserOperationReceipt

logger = logging.getLogger(__name__)


class BundlerClient:
    """
    Account Abstraction client for EIP4337 bundlers
    """

    def __init__(
        self,
        url: str,
        retry_count: int = 0,
    ):
        self.url = url
        self.retry_count = retry_count
        self.http_session = prepare_http_session(1, 100, retry_count=retry_count)

    def __str__(self):
        return f"Bundler client at {self.url}"

    def _do_request(
        self, payload: Union[Dict[Any, Any], Sequence[Dict[Any, Any]]]
    ) -> Union[Optional[Union[Dict[str, Any]]], Optional[List[Dict[str, Any]]]]:
        """
        :param payload: Allows simple request or a batch request
        :return: Result of the request
        :raises BundlerClientConnectionException: If there's a problem connecting to the bundler
        :raises BundlerClientResponseException: If the request from the bundler contains an error
        """
        try:
            response = self.http_session.post(self.url, json=payload)
        except IOError as exception:
            raise BundlerClientConnectionException(
                f"Error connecting to bundler {self.url} : {exception}"
            ) from exception

        if not response.ok:
            raise BundlerClientConnectionException(
                f"Error connecting to bundler {self.url} : {response.status_code} {response.content}"
            )

        bundler_responses = response.json()
        if not isinstance(bundler_responses, list):
            bundler_responses = [bundler_responses]

        results = []
        for rpc_response in bundler_responses:
            result = rpc_response.get("result")
            if not result and "error" in rpc_response:
                error_str = f'Bundler returned error for payload {payload} : {rpc_response["error"]}'
                logger.warning(error_str)
                raise BundlerClientResponseException(error_str)
            results.append(result)

        if not isinstance(payload, list):
            return results[0]
        return results

    @staticmethod
    def _parse_user_operation_receipt(
        user_operation_receipt: Dict[str, Any]
    ) -> UserOperationReceipt:
        return UserOperationReceipt(
            HexBytes(user_operation_receipt["userOpHash"]),
            user_operation_receipt["entryPoint"],
            user_operation_receipt["sender"],
            int(user_operation_receipt["nonce"], 16),
            user_operation_receipt["paymaster"],
            int(user_operation_receipt["actualGasCost"], 16),
            int(user_operation_receipt["actualGasUsed"], 16),
            user_operation_receipt["success"],
            user_operation_receipt["reason"],
            user_operation_receipt["logs"],
        )

    @staticmethod
    def _get_user_operation_by_hash_payload(
        user_operation_hash: HexStr, request_id: int = 1
    ) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "method": "eth_getUserOperationByHash",
            "params": [user_operation_hash],
            "id": request_id,
        }

    @staticmethod
    def _get_user_operation_receipt_payload(
        user_operation_hash: HexStr, request_id: int = 1
    ) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "method": "eth_getUserOperationReceipt",
            "params": [user_operation_hash],
            "id": request_id,
        }

    @cache
    def get_chain_id(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_chainId",
            "params": [],
            "id": 1,
        }
        result = self._do_request(payload)
        return int(result, 16)

    @lru_cache(maxsize=1024)
    def get_user_operation_by_hash(
        self, user_operation_hash: HexStr
    ) -> Optional[UserOperation]:
        """
        https://docs.alchemy.com/reference/eth-getuseroperationbyhash

        :param user_operation_hash:
        :return: ``UserOperation`` or ``None`` if not found
        :raises BundlerClientConnectionException:
        :raises BundlerClientResponseException:
        """
        payload = self._get_user_operation_by_hash_payload(user_operation_hash)
        result = self._do_request(payload)
        return (
            UserOperation.from_bundler_response(user_operation_hash, result)
            if result
            else None
        )

    @lru_cache(maxsize=1024)
    def get_user_operation_receipt(
        self, user_operation_hash: HexStr
    ) -> Optional[UserOperationReceipt]:
        """
        https://docs.alchemy.com/reference/eth-getuseroperationreceipt

        :param user_operation_hash:
        :return: ``UserOperationReceipt`` or ``None`` if not found
        :raises BundlerClientConnectionException:
        :raises BundlerClientResponseException:
        """
        payload = self._get_user_operation_receipt_payload(user_operation_hash)
        result = self._do_request(payload)
        return UserOperationReceipt.from_bundler_response(result) if result else None

    @lru_cache(maxsize=1024)
    def get_user_operation_and_receipt(
        self, user_operation_hash: HexStr
    ) -> Optional[Tuple[UserOperation, UserOperationReceipt]]:
        """
        Get UserOperation and UserOperationReceipt in the same request using a batch query.
        NOTE: Batch requests are not supported by Pimlico

        :param user_operation_hash:
        :return: Tuple with ``UserOperation`` and ``UserOperationReceipt``, or ``None`` if not found
        :raises BundlerClientConnectionException:
        :raises BundlerClientResponseException:
        """
        payload = [
            self._get_user_operation_by_hash_payload(user_operation_hash, request_id=1),
            self._get_user_operation_receipt_payload(user_operation_hash, request_id=2),
        ]
        result = self._do_request(payload)
        if not (result and result[0]):
            return None

        return UserOperation.from_bundler_response(
            user_operation_hash, result[0]
        ), self._parse_user_operation_receipt(result[1])

    @lru_cache(maxsize=None)
    def supported_entry_points(self) -> List[ChecksumAddress]:
        """
        https://docs.alchemy.com/reference/eth-supportedentrypoints

        :return: List of supported entrypoints
        :raises BundlerClientConnectionException:
        :raises BundlerClientResponseException:
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_supportedEntryPoints",
            "params": [],
            "id": 1,
        }
        return self._do_request(payload)
