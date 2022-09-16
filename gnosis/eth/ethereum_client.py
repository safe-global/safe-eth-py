import os
from enum import Enum
from functools import wraps
from logging import getLogger
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import eth_abi
import requests
from eth_abi.exceptions import DecodingError
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import URI, BlockNumber, ChecksumAddress, Hash32, HexStr
from hexbytes import HexBytes
from web3 import HTTPProvider, Web3
from web3._utils.abi import map_abi_data
from web3._utils.method_formatters import (
    block_formatter,
    receipt_formatter,
    transaction_result_formatter,
)
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import ContractFunction
from web3.datastructures import AttributeDict
from web3.exceptions import (
    BadFunctionCallOutput,
    BlockNotFound,
    TimeExhausted,
    TransactionNotFound,
)
from web3.middleware import geth_poa_middleware, simple_cache_middleware
from web3.types import (
    BlockData,
    BlockIdentifier,
    FilterParams,
    LogReceipt,
    Nonce,
    ParityBlockTrace,
    ParityFilterParams,
    ParityFilterTrace,
    TxData,
    TxParams,
    TxReceipt,
    Wei,
)

from gnosis.eth.utils import (
    fast_is_checksum_address,
    fast_to_checksum_address,
    mk_contract_address,
)
from gnosis.util import cache, cached_property, chunks

from .constants import (
    ERC20_721_TRANSFER_TOPIC,
    GAS_CALL_DATA_BYTE,
    GAS_CALL_DATA_ZERO_BYTE,
    NULL_ADDRESS,
)
from .contracts import get_erc20_contract, get_erc721_contract
from .ethereum_network import EthereumNetwork, EthereumNetworkNotSupported
from .exceptions import (
    BatchCallFunctionFailed,
    ChainIdIsRequired,
    FromAddressNotFound,
    GasLimitExceeded,
    InsufficientFunds,
    InvalidERC20Info,
    InvalidERC721Info,
    InvalidNonce,
    NonceTooHigh,
    NonceTooLow,
    ParityTraceDecodeException,
    ReplacementTransactionUnderpriced,
    SenderAccountNotFoundInNode,
    TransactionAlreadyImported,
    TransactionGasPriceTooLow,
    TransactionQueueLimitReached,
    UnknownAccount,
)
from .typing import BalanceDict, EthereumData, EthereumHash
from .utils import decode_string_or_bytes32

logger = getLogger(__name__)


def tx_with_exception_handling(func):
    """
    Parity
        - https://github.com/openethereum/openethereum/blob/main/rpc/src/v1/helpers/errors.rs
    Geth
        - https://github.com/ethereum/go-ethereum/blob/master/core/error.go
        - https://github.com/ethereum/go-ethereum/blob/master/core/tx_pool.go
    Comparison
        - https://gist.github.com/kunal365roy/3c37ac9d1c3aaf31140f7c5faa083932

    :param func:
    :return:
    """
    error_with_exception: Dict[str, Exception] = {
        "EIP-155": ChainIdIsRequired,
        "Transaction with the same hash was already imported": TransactionAlreadyImported,
        "replacement transaction underpriced": ReplacementTransactionUnderpriced,  # https://github.com/ethereum/go-ethereum/blob/eaccdba4ab310e3fb98edbc4b340b5e7c4d767fd/core/tx_pool.go#L72
        "There is another transaction with same nonce in the queue": ReplacementTransactionUnderpriced,  # https://github.com/openethereum/openethereum/blob/f1dc6821689c7f47d8fd07dfc0a2c5ad557b98ec/crates/rpc/src/v1/helpers/errors.rs#L374
        "There are too many transactions in the queue. Your transaction was dropped due to limit. Try increasing "
        "the fee": TransactionQueueLimitReached,  # https://github.com/openethereum/openethereum/blob/f1dc6821689c7f47d8fd07dfc0a2c5ad557b98ec/crates/rpc/src/v1/helpers/errors.rs#L380
        "txpool is full": TransactionQueueLimitReached,  # https://github.com/ethereum/go-ethereum/blob/eaccdba4ab310e3fb98edbc4b340b5e7c4d767fd/core/tx_pool.go#L68
        "transaction underpriced": TransactionGasPriceTooLow,  # https://github.com/ethereum/go-ethereum/blob/eaccdba4ab310e3fb98edbc4b340b5e7c4d767fd/core/tx_pool.go#L64
        "Transaction gas price is too low": TransactionGasPriceTooLow,  # https://github.com/openethereum/openethereum/blob/f1dc6821689c7f47d8fd07dfc0a2c5ad557b98ec/crates/rpc/src/v1/helpers/errors.rs#L386
        "from not found": FromAddressNotFound,
        "correct nonce": InvalidNonce,
        "nonce too low": NonceTooLow,  # https://github.com/ethereum/go-ethereum/blob/bbfb1e4008a359a8b57ec654330c0e674623e52f/core/error.go#L46
        "nonce too high": NonceTooHigh,  # https://github.com/ethereum/go-ethereum/blob/bbfb1e4008a359a8b57ec654330c0e674623e52f/core/error.go#L46
        "insufficient funds": InsufficientFunds,  # https://github.com/openethereum/openethereum/blob/f1dc6821689c7f47d8fd07dfc0a2c5ad557b98ec/crates/rpc/src/v1/helpers/errors.rs#L389
        "doesn't have enough funds": InsufficientFunds,
        "sender account not recognized": SenderAccountNotFoundInNode,
        "unknown account": UnknownAccount,
        "exceeds block gas limit": GasLimitExceeded,  # Geth
        "exceeds current gas limit": GasLimitExceeded,  # https://github.com/openethereum/openethereum/blob/f1dc6821689c7f47d8fd07dfc0a2c5ad557b98ec/crates/rpc/src/v1/helpers/errors.rs#L392
    }

    @wraps(func)
    def with_exception_handling(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            str_exc = str(exc).lower()
            for reason, custom_exception in error_with_exception.items():
                if reason.lower() in str_exc:
                    raise custom_exception(str(exc)) from exc
            raise exc

    return with_exception_handling


class EthereumTxSent(NamedTuple):
    tx_hash: bytes
    tx: TxParams
    contract_address: Optional[str]


class Erc20Info(NamedTuple):
    name: str
    symbol: str
    decimals: int


class Erc721Info(NamedTuple):
    name: str
    symbol: str


class TokenBalance(NamedTuple):
    token_address: str
    balance: int


class TxSpeed(Enum):
    SLOWEST = 0
    VERY_SLOW = 1
    SLOW = 2
    NORMAL = 3
    FAST = 4
    VERY_FAST = 5
    FASTEST = 6


class EthereumClientProvider:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            from django.conf import settings

            cls.instance = EthereumClient(
                settings.ETHEREUM_NODE_URL,
                provider_timeout=int(os.environ.get("ETHEREUM_RPC_TIMEOUT", 10)),
                slow_provider_timeout=int(
                    os.environ.get("ETHEREUM_RPC_SLOW_TIMEOUT", 60)
                ),
                retry_count=int(os.environ.get("ETHEREUM_RPC_RETRY_COUNT", 60)),
                batch_request_max_size=int(
                    os.environ.get("ETHEREUM_RPC_BATCH_REQUEST_MAX_SIZE", 500)
                ),
            )
        return cls.instance


class EthereumClientManager:
    def __init__(self, ethereum_client: "EthereumClient"):
        self.ethereum_client = ethereum_client
        self.ethereum_node_url = ethereum_client.ethereum_node_url
        self.w3 = ethereum_client.w3
        self.slow_w3 = ethereum_client.slow_w3
        self.http_session = ethereum_client.http_session
        self.timeout = ethereum_client.timeout
        self.slow_timeout = ethereum_client.slow_timeout


class BatchCallManager(EthereumClientManager):
    def batch_call_custom(
        self,
        payloads: Iterable[Dict[str, Any]],
        raise_exception: bool = True,
        block_identifier: Optional[BlockIdentifier] = "latest",
        batch_size: Optional[int] = None,
    ) -> List[Optional[Any]]:
        """
        Do batch requests of multiple contract calls (`eth_call`)

        :param payloads: Iterable of Dictionaries with at least {'data': '<hex-string>',
            'output_type': <solidity-output-type>, 'to': '<checksummed-address>'}. `from` can also be provided and if
            `fn_name` is provided it will be used for debugging purposes
        :param raise_exception: If False, exception will not be raised if there's any problem and instead `None` will
            be returned as the value
        :param block_identifier: `latest` by default
        :param batch_size: If `payload` length is bigger than size, it will be split into smaller chunks before
            sending to the server
        :return: List with the ABI decoded return values
        :raises: ValueError if raise_exception=True
        """
        if not payloads:
            return []

        queries = []
        for i, payload in enumerate(payloads):
            assert "data" in payload, "`data` not present"
            assert "to" in payload, "`to` not present"
            assert "output_type" in payload, "`output-type` not present"

            query_params = {"to": payload["to"], "data": payload["data"]}  # Balance of
            if "from" in payload:
                query_params["from"] = payload["from"]

            queries.append(
                {
                    "jsonrpc": "2.0",
                    "method": "eth_call",
                    "params": [
                        query_params,
                        hex(block_identifier)
                        if isinstance(block_identifier, int)
                        else block_identifier,
                    ],
                    "id": i,
                }
            )

        batch_size = batch_size or self.ethereum_client.batch_request_max_size
        all_results = []
        for chunk in chunks(queries, batch_size):
            response = self.http_session.post(
                self.ethereum_node_url, json=chunk, timeout=self.slow_timeout
            )
            if not response.ok:
                raise ConnectionError(
                    f"Error connecting to {self.ethereum_node_url}: {response.text}"
                )

            results = response.json()

            # If there's an error some nodes return a json instead of a list
            if isinstance(results, dict) and "error" in results:
                logger.error(
                    "Batch call custom problem with payload=%s, result=%s)",
                    chunk,
                    results,
                )
                raise ValueError(f"Batch request error: {results}")

            all_results.extend(results)

        return_values: List[Optional[Any]] = []
        errors = []
        for payload, result in zip(
            payloads, sorted(all_results, key=lambda x: x["id"])
        ):
            if "error" in result:
                fn_name = payload.get("fn_name", HexBytes(payload["data"]).hex())
                errors.append(f'`{fn_name}`: {result["error"]}')
                return_values.append(None)
            else:
                output_type = payload["output_type"]
                try:
                    decoded_values = self.w3.codec.decode_abi(
                        output_type, HexBytes(result["result"])
                    )
                    normalized_data = map_abi_data(
                        BASE_RETURN_NORMALIZERS, output_type, decoded_values
                    )
                    if len(normalized_data) == 1:
                        return_values.append(normalized_data[0])
                    else:
                        return_values.append(normalized_data)
                except (DecodingError, OverflowError):
                    fn_name = payload.get("fn_name", HexBytes(payload["data"]).hex())
                    errors.append(f"`{fn_name}`: DecodingError, cannot decode")
                    return_values.append(None)

        if errors and raise_exception:
            raise BatchCallFunctionFailed(f"Errors returned {errors}")
        else:
            return return_values

    def batch_call(
        self,
        contract_functions: Iterable[ContractFunction],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Any]]:
        """
        Do batch requests of multiple contract calls

        :param contract_functions: Iterable of contract functions using web3.py contracts. For instance, a valid
            argument would be [erc20_contract.functions.balanceOf(address), erc20_contract.functions.decimals()]
        :param from_address: Use this address as `from` in every call if provided
        :param block_identifier: `latest` by default
        :param raise_exception: If False, exception will not be raised if there's any problem and instead `None` will
            be returned as the value.
        :return: List with the ABI decoded return values
        """
        if not contract_functions:
            return []
        payloads = []
        params: TxParams = {"gas": Wei(0), "gasPrice": Wei(0)}
        for _, contract_function in enumerate(contract_functions):
            if not contract_function.address:
                raise ValueError(
                    f"Missing address for batch_call in `{contract_function.fn_name}`"
                )

            payload = {
                "to": contract_function.address,
                "data": contract_function.build_transaction(params)["data"],
                "output_type": [
                    output["type"] for output in contract_function.abi["outputs"]
                ],
                "fn_name": contract_function.fn_name,  # For debugging purposes
            }
            if from_address:
                payload["from"] = from_address
            payloads.append(payload)

        return self.batch_call_custom(
            payloads, raise_exception=raise_exception, block_identifier=block_identifier
        )

    def batch_call_same_function(
        self,
        contract_function: ContractFunction,
        contract_addresses: Sequence[ChecksumAddress],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Any]]:
        """
        Do batch requests using the same function to multiple address. ``batch_call`` could be used to achieve that,
        but generating the ContractFunction is slow, so this function allows to use the same contract_function for
        multiple addresses

        :param contract_function:
        :param contract_addresses:
        :param from_address:
        :param raise_exception:
        :param block_identifier:
        :return:
        """

        assert contract_function, "Contract function is required"

        if not contract_addresses:
            return []

        contract_function.address = NULL_ADDRESS  # It's required by web3.py
        params: TxParams = {"gas": Wei(0), "gasPrice": Wei(0)}
        data = contract_function.build_transaction(params)["data"]
        output_type = [output["type"] for output in contract_function.abi["outputs"]]
        fn_name = contract_function.fn_name

        payloads = []
        for contract_address in contract_addresses:
            payload = {
                "to": contract_address,
                "data": data,
                "output_type": output_type,
                "fn_name": fn_name,  # For debugging purposes
            }
            if from_address:
                payload["from"] = from_address
            payloads.append(payload)

        return self.batch_call_custom(
            payloads, raise_exception=raise_exception, block_identifier=block_identifier
        )


class Erc20Manager(EthereumClientManager):
    """
    Manager for ERC20 operations
    """

    # keccak('Transfer(address,address,uint256)')
    # ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
    TRANSFER_TOPIC = HexBytes(ERC20_721_TRANSFER_TOPIC)

    def decode_logs(self, logs: List[LogReceipt]):
        decoded_logs = []
        for log in logs:
            decoded = self._decode_transfer_log(log["data"], log["topics"])
            if decoded:
                log_copy = dict(log)
                log_copy["args"] = decoded
                decoded_logs.append(log_copy)
        return decoded_logs

    def _decode_transfer_log(
        self, data: EthereumData, topics: Sequence[bytes]
    ) -> Optional[Dict[str, Any]]:
        topics_len = len(topics)
        if topics_len and topics[0] == self.TRANSFER_TOPIC:
            if topics_len == 1:
                # Not standard Transfer(address from, address to, uint256 unknown)
                # 1 topic (transfer topic)
                _from, to, unknown = eth_abi.decode_abi(
                    ["address", "address", "uint256"], HexBytes(data)
                )
                return {"from": _from, "to": to, "unknown": unknown}
            elif topics_len == 3:
                # ERC20 Transfer(address indexed from, address indexed to, uint256 value)
                # 3 topics (transfer topic + from + to)
                try:
                    value_data = HexBytes(data)
                    value = eth_abi.decode_single("uint256", value_data)
                except DecodingError:
                    logger.warning(
                        "Cannot decode Transfer event `uint256 value` from data=%s",
                        value_data.hex(),
                    )
                    return None
                try:
                    from_to_data = b"".join(topics[1:])
                    _from, to = (
                        fast_to_checksum_address(address)
                        for address in eth_abi.decode_abi(
                            ["address", "address"], from_to_data
                        )
                    )
                except DecodingError:
                    logger.warning(
                        "Cannot decode Transfer event `address from, address to` from topics=%s",
                        HexBytes(from_to_data).hex(),
                    )
                    return None
                return {"from": _from, "to": to, "value": value}
            elif topics_len == 4:
                # ERC712 Transfer(address indexed from, address indexed to, uint256 indexed tokenId)
                # 4 topics (transfer topic + from + to + tokenId)
                _from, to, token_id = eth_abi.decode_abi(
                    ["address", "address", "uint256"], b"".join(topics[1:])
                )
                _from, to = [
                    fast_to_checksum_address(address) for address in (_from, to)
                ]
                return {"from": _from, "to": to, "tokenId": token_id}
        return None

    def get_balance(self, address: str, token_address: str) -> int:
        """
        Get balance of address for `erc20_address`

        :param address: owner address
        :param token_address: erc20 token address
        :return: balance
        """
        return (
            get_erc20_contract(self.w3, token_address)
            .functions.balanceOf(address)
            .call()
        )

    def get_balances(
        self, address: str, token_addresses: List[str]
    ) -> List[BalanceDict]:
        """
        Get balances for Ether and tokens for an `address`

        :param address: Owner address checksummed
        :param token_addresses: token addresses to check
        :return: ``List[BalanceDict]``
        """

        balances = self.ethereum_client.batch_call_same_function(
            get_erc20_contract(self.ethereum_client.w3).functions.balanceOf(address),
            token_addresses,
            raise_exception=False,
        )

        return_balances = [
            {
                "token_address": token_address,
                "balance": balance
                if isinstance(balance, int)
                else 0,  # A `revert` with bytes can be returned
            }
            for token_address, balance in zip(token_addresses, balances)
        ]

        # Add ether balance response
        return [
            {
                "token_address": None,
                "balance": self.ethereum_client.get_balance(address),
            }
        ] + return_balances

    def get_name(self, erc20_address: str) -> str:
        erc20 = get_erc20_contract(self.w3, erc20_address)
        data = erc20.functions.name().build_transaction(
            {"gas": Wei(0), "gasPrice": Wei(0)}
        )["data"]
        result = self.w3.eth.call({"to": erc20_address, "data": data})
        return decode_string_or_bytes32(result)

    def get_symbol(self, erc20_address: str) -> str:
        erc20 = get_erc20_contract(self.w3, erc20_address)
        data = erc20.functions.symbol().build_transaction(
            {"gas": Wei(0), "gasPrice": Wei(0)}
        )["data"]
        result = self.w3.eth.call({"to": erc20_address, "data": data})
        return decode_string_or_bytes32(result)

    def get_decimals(self, erc20_address: str) -> int:
        erc20 = get_erc20_contract(self.w3, erc20_address)
        return erc20.functions.decimals().call()

    def get_info(self, erc20_address: str) -> Erc20Info:
        """
        Get erc20 information (`name`, `symbol` and `decimals`). Use batching to get
        all info in the same request.

        :param erc20_address:
        :return: Erc20Info
        :raises: InvalidERC20Info
        """
        erc20 = get_erc20_contract(self.w3, erc20_address)
        params: TxParams = {
            "gas": Wei(0),
            "gasPrice": Wei(0),
        }  # Prevent executing tx, we are just interested on `data`
        datas = [
            erc20.functions.name().build_transaction(params)["data"],
            erc20.functions.symbol().build_transaction(params)["data"],
            erc20.functions.decimals().build_transaction(params)["data"],
        ]
        payload = [
            {
                "id": i,
                "jsonrpc": "2.0",
                "method": "eth_call",
                "params": [{"to": erc20_address, "data": data}, "latest"],
            }
            for i, data in enumerate(datas)
        ]
        response = self.http_session.post(
            self.ethereum_client.ethereum_node_url,
            json=payload,
            timeout=self.slow_timeout,
        )
        if not response.ok:
            raise InvalidERC20Info(response.content)
        try:
            response_json = sorted(response.json(), key=lambda x: x["id"])
            errors = [r["error"] for r in response_json if "error" in r]
            if errors:
                raise InvalidERC20Info(f"{erc20_address} - {errors}")
            results = [HexBytes(r["result"]) for r in response_json]
            name = decode_string_or_bytes32(results[0])
            symbol = decode_string_or_bytes32(results[1])
            decimals = self.ethereum_client.w3.codec.decode_single("uint8", results[2])
            return Erc20Info(name, symbol, decimals)
        except (ValueError, BadFunctionCallOutput, DecodingError) as e:
            raise InvalidERC20Info from e

    def get_total_transfer_history(
        self,
        addresses: Optional[Sequence[ChecksumAddress]] = None,
        from_block: BlockIdentifier = BlockNumber(0),
        to_block: Optional[BlockIdentifier] = None,
        token_address: Optional[ChecksumAddress] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get events for erc20 and erc721 transfers from and to an `address`. We decode it manually.
        Example of an erc20 event:

        .. code-block:: python

            {'logIndex': 0,
             'transactionIndex': 0,
             'transactionHash': HexBytes('0x4d0f25313603e554e3b040667f7f391982babbd195c7ae57a8c84048189f7794'),
             'blockHash': HexBytes('0x90fa67d848a0eaf3be625235dae28815389f5292d4465c48d1139f0c207f8d42'),
             'blockNumber': 791,
             'address': '0xf7d0Bd47BF3214494E7F5B40E392A25cb4788620',
             'data': '0x000000000000000000000000000000000000000000000000002001f716742000',
             'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
              HexBytes('0x000000000000000000000000f5984365fca2e3bc7d2e020abb2c701df9070eb7'),
              HexBytes('0x0000000000000000000000001df62f291b2e969fb0849d99d9ce41e2f137006e')],
             'type': 'mined'
             'args': {'from': '0xf5984365FcA2e3bc7D2E020AbB2c701DF9070eB7',
                      'to': '0x1dF62f291b2E969fB0849d99D9Ce41e2F137006e',
                      'value': 9009360000000000
                     }
            }
            An example of an erc721 event
            {'address': '0x6631FcbB50677DfC6c02CCDcc03a8f68Db427a64',
             'blockHash': HexBytes('0x95c71c6c9373e9a8ca2c767dda1cd5083eb6addcce36fc216c9e1f458d6970f9'),
             'blockNumber': 5341681,
             'data': '0x',
             'logIndex': 0,
             'removed': False,
             'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
              HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
              HexBytes('0x000000000000000000000000b5239c032ab9fb5abfc3903e770a4b6a9095542c'),
              HexBytes('0x0000000000000000000000000000000000000000000000000000000000000063')],
             'transactionHash': HexBytes('0xce8c8af0503e6f8a421345c10cdf92834c95186916a3f5b1437d2bba63d2db9e'),
             'transactionIndex': 0,
             'transactionLogIndex': '0x0',
             'type': 'mined',
             'args': {'from': '0x0000000000000000000000000000000000000000',
                      'to': '0xb5239C032AB9fB5aBFc3903e770A4B6a9095542C',
                      'tokenId': 99
                     }
             }
            An example of unknown transfer event (no indexed parts), could be a ERC20 or ERC721 transfer:
            {'address': '0x6631FcbB50677DfC6c02CCDcc03a8f68Db427a64',
             'blockHash': HexBytes('0x95c71c6c9373e9a8ca2c767dda1cd5083eb6addcce36fc216c9e1f458d6970f9'),
             'blockNumber': 5341681,
             'data': '0x',
             'logIndex': 0,
             'removed': False,
             'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
              HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
              HexBytes('0x000000000000000000000000b5239c032ab9fb5abfc3903e770a4b6a9095542c'),
              HexBytes('0x0000000000000000000000000000000000000000000000000000000000000063')],
             'transactionHash': HexBytes('0xce8c8af0503e6f8a421345c10cdf92834c95186916a3f5b1437d2bba63d2db9e'),
             'transactionIndex': 0,
             'transactionLogIndex': '0x0',
             'type': 'mined',
             'args': {'from': '0x0000000000000000000000000000000000000000',
                      'to': '0xb5239C032AB9fB5aBFc3903e770A4B6a9095542C',
                      'unknown': 99
                     }
             }

        :param addresses: Search events `from` and `to` these `addresses`. If not, every transfer event within the
            range will be retrieved
        :param from_block: Block to start querying from
        :param to_block: Block to stop querying from
        :param token_address: Address of the token
        :return: List of events sorted by blockNumber
        """
        topic_0 = self.TRANSFER_TOPIC.hex()
        if addresses:
            addresses_encoded = [
                HexBytes(eth_abi.encode_single("address", address)).hex()
                for address in addresses
            ]
            # Topics for transfer `to` and `from` an address
            all_topics = [
                [topic_0, addresses_encoded],  # Topics from
                [topic_0, None, addresses_encoded],  # Topics to
            ]
        else:
            all_topics = [[topic_0]]  # All transfer events
        parameters: FilterParams = {"fromBlock": from_block}
        if to_block:
            parameters["toBlock"] = to_block
        if token_address:
            parameters["address"] = token_address

        all_events: List[LogReceipt] = []
        # Do the request to `eth_getLogs`
        for topics in all_topics:
            parameters["topics"] = topics
            all_events.extend(self.slow_w3.eth.get_logs(parameters))

        # Decode events. Just pick valid ERC20 Transfer events (ERC721 `Transfer` has the same signature)
        erc20_events = []
        for event in all_events:
            e = LogReceipt(event)  # Convert `AttributeDict` to `Dict`
            e["args"] = self._decode_transfer_log(e["data"], e["topics"])
            if e["args"]:
                erc20_events.append(e)
        erc20_events.sort(key=lambda x: x["blockNumber"])
        return erc20_events

    def get_transfer_history(
        self,
        from_block: int,
        to_block: Optional[int] = None,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        token_address: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        DON'T USE, it will fail in some cases until they fix https://github.com/ethereum/web3.py/issues/1351
        Get events for erc20/erc721 transfers. At least one of `from_address`, `to_address` or `token_address` must be
        defined. Example of decoded event:

        .. code-block:: python

            {
                "args": {
                    "from": "0x1Ce67Ea59377A163D47DFFc9BaAB99423BE6EcF1",
                    "to": "0xaE9E15896fd32E59C7d89ce7a95a9352D6ebD70E",
                    "value": 15000000000000000
                },
                "event": "Transfer",
                "logIndex": 42,
                "transactionIndex": 60,
                "transactionHash": "0x71d6d83fef3347bad848e83dfa0ab28296e2953de946ee152ea81c6dfb42d2b3",
                "address": "0xfecA834E7da9D437645b474450688DA9327112a5",
                "blockHash": "0x054de9a496fc7d10303068cbc7ee3e25181a3b26640497859a5e49f0342e7db2",
                "blockNumber": 7265022
            }

        :param from_block: Block to start querying from
        :param to_block: Block to stop querying from
        :param from_address: Address sending the erc20 transfer
        :param to_address: Address receiving the erc20 transfer
        :param token_address: Address of the token
        :return: List of events (decoded)
        :throws: ReadTimeout
        """
        assert (
            from_address or to_address or token_address
        ), "At least one parameter must be provided"

        erc20 = get_erc20_contract(self.slow_w3)

        argument_filters = {}
        if from_address:
            argument_filters["from"] = from_address
        if to_address:
            argument_filters["to"] = to_address

        return erc20.events.Transfer.createFilter(
            fromBlock=from_block,
            toBlock=to_block,
            address=token_address,
            argument_filters=argument_filters,
        ).get_all_entries()

    def send_tokens(
        self,
        to: str,
        amount: int,
        erc20_address: str,
        private_key: str,
        nonce: Optional[int] = None,
        gas_price: Optional[int] = None,
        gas: Optional[int] = None,
    ) -> bytes:
        """
        Send tokens to address

        :param to:
        :param amount:
        :param erc20_address:
        :param private_key:
        :param nonce:
        :param gas_price:
        :param gas:
        :return: tx_hash
        """
        erc20 = get_erc20_contract(self.w3, erc20_address)
        account = Account.from_key(private_key)
        tx_options: TxParams = {"from": account.address}
        if nonce:
            tx_options["nonce"] = Nonce(nonce)
        if gas_price:
            tx_options["gasPrice"] = Wei(gas_price)
        if gas:
            tx_options["gas"] = Wei(gas)

        tx = erc20.functions.transfer(to, amount).build_transaction(tx_options)
        return self.ethereum_client.send_unsigned_transaction(
            tx, private_key=private_key
        )


class Erc721Manager(EthereumClientManager):
    # keccak('Transfer(address,address,uint256)')
    # ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
    TRANSFER_TOPIC = Erc20Manager.TRANSFER_TOPIC

    def get_balance(self, address: str, token_address: str) -> int:
        """
        Get balance of address for `erc20_address`

        :param address: owner address
        :param token_address: erc721 token address
        :return: balance
        """
        return (
            get_erc721_contract(self.w3, token_address)
            .functions.balanceOf(address)
            .call()
        )

    def get_balances(
        self, address: str, token_addresses: List[str]
    ) -> List[TokenBalance]:
        """
        Get balances for tokens for an `address`. If there's a problem with a token_address `0` will be
        returned for balance

        :param address: Owner address checksummed
        :param token_addresses: token addresses to check
        :return:
        """
        balances = self.ethereum_client.batch_call_same_function(
            get_erc721_contract(self.ethereum_client.w3)
            .functions.balanceOf(address)
            .token_addresses,
            raise_exception=False,
        )
        return [
            TokenBalance(token_address, balance if isinstance(balance, int) else 0)
            for (token_address, balance) in zip(token_addresses, balances)
        ]

    def get_info(self, token_address: str) -> Erc721Info:
        """
        Get erc721 information (`name`, `symbol`). Use batching to get
        all info in the same request.

        :param token_address:
        :return: Erc721Info
        """
        erc721_contract = get_erc721_contract(self.w3, token_address)
        try:
            name, symbol = cast(
                List[str],
                self.ethereum_client.batch_call(
                    [
                        erc721_contract.functions.name(),
                        erc721_contract.functions.symbol(),
                    ]
                ),
            )
            return Erc721Info(name, symbol)
        except (DecodingError, ValueError):  # Not all the ERC721 have metadata
            raise InvalidERC721Info

    def get_owners(
        self, token_addresses_with_token_ids: Sequence[Tuple[str, int]]
    ) -> List[Optional[ChecksumAddress]]:
        """
        :param token_addresses_with_token_ids: Tuple(token_address: str, token_id: int)
        :return: List of owner addresses, `None` if not found
        """
        return [
            ChecksumAddress(owner) if isinstance(owner, str) else None
            for owner in self.ethereum_client.batch_call(
                [
                    get_erc721_contract(
                        self.ethereum_client.w3, token_address
                    ).functions.ownerOf(token_id)
                    for token_address, token_id in token_addresses_with_token_ids
                ],
                raise_exception=False,
            )
        ]

    def get_token_uris(
        self, token_addresses_with_token_ids: Sequence[Tuple[str, int]]
    ) -> List[Optional[str]]:
        """
        :param token_addresses_with_token_ids: Tuple(token_address: str, token_id: int)
        :return: List of token_uris, `None` if not found
        """
        return [
            token_uri if isinstance(token_uri, str) else None
            for token_uri in self.ethereum_client.batch_call(
                [
                    get_erc721_contract(
                        self.ethereum_client.w3, token_address
                    ).functions.tokenURI(token_id)
                    for token_address, token_id in token_addresses_with_token_ids
                ],
                raise_exception=False,
            )
        ]


class ParityManager(EthereumClientManager):
    # TODO Test with mock
    def _decode_trace_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        decoded = {}

        # CALL, DELEGATECALL, CREATE or CREATE2
        if "from" in action:
            decoded["from"] = fast_to_checksum_address(action["from"])
        if "gas" in action:
            decoded["gas"] = int(action["gas"], 16)
        if "value" in action:
            decoded["value"] = int(action["value"], 16)

        # CALL or DELEGATECALL
        if "callType" in action:
            decoded["callType"] = action["callType"]
        if "input" in action:
            decoded["input"] = HexBytes(action["input"])
        if "to" in action:
            decoded["to"] = fast_to_checksum_address(action["to"])

        # CREATE or CREATE2
        if "init" in action:
            decoded["init"] = HexBytes(action["init"])

        # SELF-DESTRUCT
        if "address" in action:
            decoded["address"] = fast_to_checksum_address(action["address"])
        if "balance" in action:
            decoded["balance"] = int(action["balance"], 16)
        if "refundAddress" in action:
            decoded["refundAddress"] = fast_to_checksum_address(action["refundAddress"])

        return decoded

    def _decode_trace_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        decoded: Dict[str, Any] = {
            "gasUsed": int(result["gasUsed"], 16),
        }

        # CALL or DELEGATECALL
        if "output" in result:
            decoded["output"] = HexBytes(result["output"])

        # CREATE or CREATE2
        if "code" in result:
            decoded["code"] = HexBytes(result["code"])
        if "address" in result:
            decoded["address"] = fast_to_checksum_address(result["address"])

        return decoded

    def _decode_traces(
        self, traces: Sequence[Union[ParityBlockTrace, ParityFilterTrace]]
    ) -> List[Dict[str, Any]]:
        new_traces: List[Dict[str, Any]] = []
        for trace in traces:
            if isinstance(trace, dict):
                trace_copy = trace.copy()
            elif isinstance(trace, AttributeDict):
                trace_copy = trace.__dict__.copy()
            else:
                raise ParityTraceDecodeException(
                    "Expected dictionary, but found unexpected trace %s" % trace
                )
            new_traces.append(trace_copy)
            # Txs with `error` field don't have `result` field
            # Txs with `type=suicide` have `result` field but is `None`
            if "result" in trace and trace["result"]:
                trace_copy["result"] = self._decode_trace_result(trace["result"])
            trace_copy["action"] = self._decode_trace_action(trace["action"])
        return new_traces

    def filter_out_errored_traces(
        self, internal_txs: Sequence[Dict[str, Any]]
    ) -> Sequence[Dict[str, Any]]:
        """
        Filter out errored transactions (traces that are errored or that have an errored parent)

        :param internal_txs: Traces for the SAME ethereum tx, sorted ascending by `trace_address`
            `sorted(t, key = lambda i: i['traceAddress'])`. It's the default output from methods returning `traces` like
            `trace_block` or `trace_transaction`
        :return: List of not errored traces
        """
        new_list = []
        errored_trace_address: Optional[List[int]] = None
        for internal_tx in internal_txs:
            if internal_tx.get("error") is not None:
                errored_trace_address = internal_tx["traceAddress"]
            elif (
                errored_trace_address is not None
                and internal_tx["traceAddress"][: len(errored_trace_address)]
                == errored_trace_address
            ):
                continue
            else:
                new_list.append(internal_tx)
        return new_list

    def get_previous_trace(
        self,
        tx_hash: EthereumHash,
        trace_address: Sequence[int],
        number_traces: int = 1,
        skip_delegate_calls: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        :param tx_hash:
        :param trace_address:
        :param number_traces: Number of traces to skip, by default get the immediately previous one
        :param skip_delegate_calls: If True filter out delegate calls
        :return: Parent trace for a trace
        :raises: ``ValueError`` if tracing is not supported
        """
        if len(trace_address) < number_traces:
            return None

        trace_address = trace_address[:-number_traces]
        traces = reversed(self.trace_transaction(tx_hash))
        for trace in traces:
            if trace_address == trace["traceAddress"]:
                if (
                    skip_delegate_calls
                    and trace["action"].get("callType") == "delegatecall"
                ):
                    trace_address = trace_address[:-1]
                else:
                    return trace

    def get_next_traces(
        self,
        tx_hash: EthereumHash,
        trace_address: Sequence[int],
        remove_delegate_calls: bool = False,
        remove_calls: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        :param tx_hash:
        :param trace_address:
        :param remove_delegate_calls: If True remove delegate calls from result
        :param remove_calls: If True remove calls from result
        :return: Children for a trace, E.g. if address is [0, 1] and number_traces = 1, it will return [0, 1, x]
        :raises: ``ValueError`` if tracing is not supported
        """
        trace_address_len = len(trace_address)
        traces = []
        for trace in self.trace_transaction(tx_hash):
            if (
                trace_address_len + 1 == len(trace["traceAddress"])
                and trace_address == trace["traceAddress"][:-1]
            ):
                if (
                    remove_delegate_calls
                    and trace["action"].get("callType") == "delegatecall"
                ):
                    pass
                elif remove_calls and trace["action"].get("callType") == "call":
                    pass
                else:
                    traces.append(trace)
        return traces

    def trace_block(self, block_identifier: BlockIdentifier) -> List[Dict[str, Any]]:
        try:
            return self._decode_traces(
                self.slow_w3.parity.trace_block(block_identifier)
            )
        except ParityTraceDecodeException as exc:
            logger.warning("Problem decoding trace: %s - Retrying", exc)
            return self._decode_traces(
                self.slow_w3.parity.trace_block(block_identifier)
            )

    def trace_blocks(
        self, block_identifiers: List[BlockIdentifier]
    ) -> List[List[Dict[str, Any]]]:
        if not block_identifiers:
            return []
        payload = [
            {
                "id": i,
                "jsonrpc": "2.0",
                "method": "trace_block",
                "params": [
                    hex(block_identifier)
                    if isinstance(block_identifier, int)
                    else block_identifier
                ],
            }
            for i, block_identifier in enumerate(block_identifiers)
        ]

        results = self.ethereum_client.raw_batch_request(payload)
        traces = []
        for raw_tx in results:
            if raw_tx:
                try:
                    decoded_traces = self._decode_traces(raw_tx)
                except ParityTraceDecodeException as exc:
                    logger.warning("Problem decoding trace: %s - Retrying", exc)
                    decoded_traces = self._decode_traces(raw_tx)
                traces.append(decoded_traces)
            else:
                traces.append([])
        return traces

    def trace_transaction(self, tx_hash: EthereumHash) -> List[Dict[str, Any]]:
        """
        :param tx_hash:
        :return: List of internal txs for `tx_hash`
        """
        try:
            return self._decode_traces(self.slow_w3.parity.trace_transaction(tx_hash))
        except ParityTraceDecodeException as exc:
            logger.warning("Problem decoding trace: %s - Retrying", exc)
            return self._decode_traces(self.slow_w3.parity.trace_transaction(tx_hash))

    def trace_transactions(
        self, tx_hashes: Sequence[EthereumHash]
    ) -> List[List[Dict[str, Any]]]:
        """
        :param tx_hashes:
        :return: For every `tx_hash` a list of internal txs (in the same order as the `tx_hashes` were provided)
        """
        if not tx_hashes:
            return []
        payload = [
            {
                "id": i,
                "jsonrpc": "2.0",
                "method": "trace_transaction",
                "params": [HexBytes(tx_hash).hex()],
            }
            for i, tx_hash in enumerate(tx_hashes)
        ]
        results = self.ethereum_client.raw_batch_request(payload)
        traces = []
        for raw_tx in results:
            if raw_tx:
                try:
                    decoded_traces = self._decode_traces(raw_tx)
                except ParityTraceDecodeException as exc:
                    logger.warning("Problem decoding trace: %s - Retrying", exc)
                    decoded_traces = self._decode_traces(raw_tx)
                traces.append(decoded_traces)
            else:
                traces.append([])
        return traces

    def trace_filter(
        self,
        from_block: int = 1,
        to_block: Optional[int] = None,
        from_address: Optional[Sequence[ChecksumAddress]] = None,
        to_address: Optional[Sequence[ChecksumAddress]] = None,
        after: Optional[int] = None,
        count: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get events using ``trace_filter`` method

        :param from_block: Quantity or Tag - (optional) From this block. `0` is not working, it needs to be `>= 1`
        :param to_block: Quantity or Tag - (optional) To this block.
        :param from_address: Array - (optional) Sent from these addresses.
        :param to_address: Address - (optional) Sent to these addresses.
        :param after: Quantity - (optional) The offset trace number
        :param count: Quantity - (optional) Integer number of traces to display in a batch.
        :return:

        .. code-block:: python

            [
                {
                    "action": {
                        "callType": "call",
                        "from": "0x32be343b94f860124dc4fee278fdcbd38c102d88",
                        "gas": "0x4c40d",
                        "input": "0x",
                        "to": "0x8bbb73bcb5d553b5a556358d27625323fd781d37",
                        "value": "0x3f0650ec47fd240000"
                    },
                    "blockHash": "0x86df301bcdd8248d982dbf039f09faf792684e1aeee99d5b58b77d620008b80f",
                    "blockNumber": 3068183,
                    "result": {
                        "gasUsed": "0x0",
                        "output": "0x"
                    },
                    "subtraces": 0,
                    "traceAddress": [],
                    "transactionHash": "0x3321a7708b1083130bd78da0d62ead9f6683033231617c9d268e2c7e3fa6c104",
                    "transactionPosition": 3,
                    "type": "call"
                },
                {
                    "action": {
                        "from": "0x3b169a0fb55ea0b6bafe54c272b1fe4983742bf7",
                        "gas": "0x49b0b",
                        "init": "0x608060405234801561001057600080fd5b5060405161060a38038061060a833981018060405281019080805190602001909291908051820192919060200180519060200190929190805190602001909291908051906020019092919050505084848160008173ffffffffffffffffffffffffffffffffffffffff1614151515610116576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260248152602001807f496e76616c6964206d617374657220636f707920616464726573732070726f7681526020017f696465640000000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506000815111156101a35773ffffffffffffffffffffffffffffffffffffffff60005416600080835160208501846127105a03f46040513d6000823e600082141561019f573d81fd5b5050505b5050600081111561036d57600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614156102b7578273ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f1935050505015156102b2576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f436f756c64206e6f74207061792073616665206372656174696f6e207769746881526020017f206574686572000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b61036c565b6102d1828483610377640100000000026401000000009004565b151561036b576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f436f756c64206e6f74207061792073616665206372656174696f6e207769746881526020017f20746f6b656e000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b5050505050610490565b600060608383604051602401808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001925050506040516020818303038152906040527fa9059cbb000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19166020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff838183161783525050505090506000808251602084016000896127105a03f16040513d6000823e3d60008114610473576020811461047b5760009450610485565b829450610485565b8151158315171594505b505050509392505050565b61016b8061049f6000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634555d5c91461008b5780635c60da1b146100b6575b73ffffffffffffffffffffffffffffffffffffffff600054163660008037600080366000845af43d6000803e6000811415610086573d6000fd5b3d6000f35b34801561009757600080fd5b506100a061010d565b6040518082815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610116565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006002905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050905600a165627a7a7230582007fffd557dfc8c4d2fdf56ba6381a6ce5b65b6260e1492d87f26c6d4f1d0410800290000000000000000000000008942595a2dc5181df0465af0d7be08c8f23c93af00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d9e09beaeb338d81a7c5688358df0071d498811500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001b15f91a8c35300000000000000000000000000000000000000000000000000000000000001640ec78d9e00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000004000000000000000000000000f763ea5fbb191d47dc4b083dcdc3cdfb586468f8000000000000000000000000ad25c9717d04c0a12086a1d352c1ccf4bf5fcbf80000000000000000000000000da7155692446c80a4e7ad72018e586f20fa3bfe000000000000000000000000bce0cc48ce44e0ac9ee38df4d586afbacef191fa0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                        "value": "0x0"
                    },
                    "blockHash": "0x03f9f64dfeb7807b5df608e6957dd4d521fd71685aac5533451d27f0abe03660",
                    "blockNumber": 3793534,
                    "result": {
                        "address": "0x61a7cc907c47c133d5ff5b685407201951fcbd08",
                        "code": "0x60806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634555d5c91461008b5780635c60da1b146100b6575b73ffffffffffffffffffffffffffffffffffffffff600054163660008037600080366000845af43d6000803e6000811415610086573d6000fd5b3d6000f35b34801561009757600080fd5b506100a061010d565b6040518082815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610116565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b60006002905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050905600a165627a7a7230582007fffd557dfc8c4d2fdf56ba6381a6ce5b65b6260e1492d87f26c6d4f1d041080029",
                        "gasUsed": "0x4683f"
                    },
                    "subtraces": 2,
                    "traceAddress": [],
                    "transactionHash": "0x6c7e8f8778d33d81b29c4bd7526ee50a4cea340d69eed6c89ada4e6fab731789",
                    "transactionPosition": 1,
                    "type": "create"
                },
                {
                    'action': {
                        'address': '0x4440adafbc6c4e45c299451c0eedc7c8b98c14ac',
                        'balance': '0x0',
                        'refundAddress': '0x0000000000000000000000000000000000000000'
                    },
                    'blockHash': '0x8512d367492371edf44ebcbbbd935bc434946dddc2b126cb558df5906012186c',
                    'blockNumber': 7829689,
                    'result': None,
                    'subtraces': 0,
                    'traceAddress': [0, 0, 0, 0, 0, 0],
                    'transactionHash': '0x5f7af6aa390f9f8dd79ee692c37cbde76bb7869768b1bac438b6d176c94f637d',
                    'transactionPosition': 35,
                    'type': 'suicide'
                }
            ]

        """
        assert (
            from_address or to_address
        ), "You must provide at least `from_address` or `to_address`"
        parameters: ParityFilterParams = {}
        if after:
            parameters["after"] = after
        if count:
            parameters["count"] = count
        if from_block:
            parameters["fromBlock"] = HexStr("0x%x" % from_block)
        if to_block:
            parameters["toBlock"] = HexStr("0x%x" % to_block)
        if from_address:
            parameters["fromAddress"] = from_address
        if to_address:
            parameters["toAddress"] = to_address

        try:
            return self._decode_traces(self.slow_w3.parity.trace_filter(parameters))
        except ParityTraceDecodeException as exc:
            logger.warning("Problem decoding trace: %s - Retrying", exc)
            return self._decode_traces(self.slow_w3.parity.trace_filter(parameters))


class EthereumClient:
    """
    Manage ethereum operations. Uses web3 for the most part, but some other stuff is implemented from scratch.
    Note: If you want to use `pending` state with `Parity`, it must be run with `--pruning=archive` or `--force-sealing`
    """

    NULL_ADDRESS = NULL_ADDRESS

    def __init__(
        self,
        ethereum_node_url: URI = URI("http://localhost:8545"),
        provider_timeout: int = 15,
        slow_provider_timeout: int = 60,
        retry_count: int = 3,
        use_caching_middleware: bool = True,
        batch_request_max_size: int = 500,
    ):
        """
        :param ethereum_node_url: Ethereum RPC uri
        :param provider_timeout: Timeout for regular RPC queries
        :param slow_provider_timeout: Timeout for slow (tracing, logs...) and custom RPC queries
        :param retry_count: Retry count for failed requests
        :param use_caching_middleware: Use web3 simple cache middleware: https://web3py.readthedocs.io/en/stable/middleware.html#web3.middleware.construct_simple_cache_middleware
        :param batch_request_max_size: Max size for JSON RPC Batch requests. Some providers have a limitation on 500
        """
        self.http_session = self._prepare_http_session(retry_count)
        self.ethereum_node_url: str = ethereum_node_url
        self.timeout = provider_timeout
        self.slow_timeout = slow_provider_timeout
        self.w3_provider = HTTPProvider(
            self.ethereum_node_url,
            request_kwargs={"timeout": provider_timeout},
            session=self.http_session,
        )
        self.w3_slow_provider = HTTPProvider(
            self.ethereum_node_url,
            request_kwargs={"timeout": slow_provider_timeout},
            session=self.http_session,
        )
        self.w3: Web3 = Web3(self.w3_provider)
        self.slow_w3: Web3 = Web3(self.w3_slow_provider)
        self.erc20: Erc20Manager = Erc20Manager(self)
        self.erc721: Erc721Manager = Erc721Manager(self)
        self.parity: ParityManager = ParityManager(self)
        self.batch_call_manager: BatchCallManager = BatchCallManager(self)
        try:
            if self.get_network() != EthereumNetwork.MAINNET:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # For tests using dummy connections (like IPC)
        except (IOError, FileNotFoundError):
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.use_caching_middleware = use_caching_middleware
        if self.use_caching_middleware:
            self.w3.middleware_onion.add(simple_cache_middleware)
            self.slow_w3.middleware_onion.add(simple_cache_middleware)

        self.batch_request_max_size = batch_request_max_size

    def __str__(self):
        return f"EthereumClient for url={self.ethereum_node_url}"

    def _prepare_http_session(self, retry_count: int) -> requests.Session:
        """
        Prepare http session with custom pooling. See:
        https://urllib3.readthedocs.io/en/stable/advanced-usage.html
        https://2.python-requests.org/en/latest/api/#requests.adapters.HTTPAdapter
        https://web3py.readthedocs.io/en/stable/providers.html#httpprovider
        """
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=1,  # Doing all the connections to the same url
            pool_maxsize=100,  # Number of concurrent connections
            max_retries=retry_count,  # Nodes are not very responsive some times
            pool_block=False,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def raw_batch_request(
        self, payload: List[Dict[str, Any]], batch_size: Optional[int] = None
    ) -> Iterable[Optional[Dict[str, Any]]]:
        """
        Perform a raw batch JSON RPC call

        :param payload: Batch request payload. Make sure all provided `ids` inside the payload are different
        :param batch_size: If `payload` length is bigger than size, it will be split into smaller chunks before
            sending to the server
        :return:
        :raises: ValueError
        """

        batch_size = batch_size or self.batch_request_max_size

        all_results = []
        for chunk in chunks(payload, batch_size):
            response = self.http_session.post(
                self.ethereum_node_url, json=chunk, timeout=self.slow_timeout
            )

            if not response.ok:
                logger.error(
                    "Problem doing raw batch request with payload=%s status_code=%d result=%s",
                    chunk,
                    response.status_code,
                    response.content,
                )
                raise ValueError(f"Batch request error: {response.content}")

            results = response.json()

            # If there's an error some nodes return a json instead of a list
            if isinstance(results, dict) and "error" in results:
                logger.error(
                    "Batch request problem with payload=%s, result=%s)", chunk, results
                )
                raise ValueError(f"Batch request error: {results}")

            all_results.extend(results)

        # Nodes like Erigon send back results out of order
        for query, result in zip(payload, sorted(all_results, key=lambda x: x["id"])):
            if "result" not in result:
                message = f"Problem with payload=`{query}` result={result}"
                logger.error(message)
                raise ValueError(message)

            yield result["result"]

    @property
    def current_block_number(self):
        return self.w3.eth.block_number

    @cache
    def get_chain_id(self) -> int:
        """
        :return: ChainId returned by the RPC `eth_chainId` method. It should never change, so it's cached.
        """
        return int(self.w3.eth.chain_id)

    @cache
    def get_client_version(self) -> str:
        """
        :return: RPC version information
        """
        return self.w3.clientVersion

    def get_network(self) -> EthereumNetwork:
        """
        Get network name based on the chainId

        :return: EthereumNetwork based on the chainId. If network is not
            on our list, `EthereumNetwork.UNKOWN` is returned
        """
        return EthereumNetwork(self.get_chain_id())

    @cache
    def is_eip1559_supported(self) -> EthereumNetwork:
        """
        :return: `True` if EIP1559 is supported by the node, `False` otherwise
        """
        try:
            self.w3.eth.fee_history(1, "latest", reward_percentiles=[50])
            return True
        except ValueError:
            return False

    @cached_property
    def multicall(self) -> "Multicall":  # noqa F821
        from .multicall import Multicall

        try:
            return Multicall(self)
        except EthereumNetworkNotSupported:
            logger.warning("Multicall not supported for this network")
            return None

    def batch_call(
        self,
        contract_functions: Iterable[ContractFunction],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        force_batch_call: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Union[bytes, Any]]]:
        """
        Call multiple functions. Multicall contract by MakerDAO will be used by default if available

        :param contract_functions:
        :param from_address: Only available when ``Multicall`` is not used
        :param raise_exception: If ``True``, raise ``BatchCallException`` if one of the calls fails
        :param force_batch_call: If ``True``, ignore multicall and always use batch calls to get the
            result (less optimal). If ``False``, more optimal way will be tried.
        :param block_identifier:
        :return: List of elements decoded to their types, ``None`` if they cannot be decoded and
            bytes if a revert error is returned and ``raise_exception=False``
        :raises: BatchCallException
        """
        if self.multicall and not force_batch_call:  # Multicall is more optimal
            return [
                result.return_data_decoded
                for result in self.multicall.try_aggregate(
                    contract_functions,
                    require_success=raise_exception,
                    block_identifier=block_identifier,
                )
            ]
        else:
            return self.batch_call_manager.batch_call(
                contract_functions,
                from_address=from_address,
                raise_exception=raise_exception,
                block_identifier=block_identifier,
            )

    def batch_call_same_function(
        self,
        contract_function: ContractFunction,
        contract_addresses: Sequence[ChecksumAddress],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        force_batch_call: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Union[bytes, Any]]]:
        """
        Call the same function in multiple contracts. Way more optimal than using `batch_call` generating multiple
        ``ContractFunction`` objects.

        :param contract_function:
        :param contract_addresses:
        :param from_address: Only available when ``Multicall`` is not used
        :param raise_exception: If ``True``, raise ``BatchCallException`` if one of the calls fails
        :param force_batch_call: If ``True``, ignore multicall and always use batch calls to get the
            result (less optimal). If ``False``, more optimal way will be tried.
        :param block_identifier:
        :return: List of elements decoded to the same type, ``None`` if they cannot be decoded and
            bytes if a revert error is returned and ``raise_exception=False``
        :raises: BatchCallException
        """
        if self.multicall and not force_batch_call:  # Multicall is more optimal
            return [
                result.return_data_decoded
                for result in self.multicall.try_aggregate_same_function(
                    contract_function,
                    contract_addresses,
                    require_success=raise_exception,
                    block_identifier=block_identifier,
                )
            ]
        else:
            return self.batch_call_manager.batch_call_same_function(
                contract_function,
                contract_addresses,
                from_address=from_address,
                raise_exception=raise_exception,
                block_identifier=block_identifier,
            )

    def deploy_and_initialize_contract(
        self,
        deployer_account: LocalAccount,
        constructor_data: bytes,
        initializer_data: bytes = b"",
        check_receipt: bool = True,
    ):
        contract_address: Optional[ChecksumAddress] = None
        for data in (constructor_data, initializer_data):
            # Because initializer_data is not mandatory
            if data:
                tx: TxParams = {
                    "from": deployer_account.address,
                    "data": data,
                    "gasPrice": self.w3.eth.gas_price,
                    "value": Wei(0),
                    "to": contract_address if contract_address else "",
                }
                tx["gas"] = self.w3.eth.estimate_gas(tx)
                tx_hash = self.send_unsigned_transaction(
                    tx, private_key=deployer_account.key
                )
                if check_receipt:
                    tx_receipt = self.get_transaction_receipt(
                        Hash32(tx_hash), timeout=60
                    )
                    assert tx_receipt
                    assert tx_receipt["status"]

                if not contract_address:
                    contract_address = ChecksumAddress(
                        mk_contract_address(tx["from"], tx["nonce"])
                    )

        return EthereumTxSent(tx_hash, tx, contract_address)

    def get_nonce_for_account(
        self,
        address: ChecksumAddress,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ):
        """
        Get nonce for account. `getTransactionCount` is the only method for what `pending` is currently working
        (Geth and Parity)

        :param address:
        :param block_identifier:
        :return:
        """
        return self.w3.eth.get_transaction_count(
            address, block_identifier=block_identifier
        )

    def estimate_gas(
        self,
        to: str,
        from_: Optional[str] = None,
        value: Optional[int] = None,
        data: Optional[EthereumData] = None,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> int:
        """
        Estimate gas calling `eth_estimateGas`

        :param from_:
        :param to:
        :param value:
        :param data:
        :param gas:
        :param gas_price:
        :param block_identifier: Be careful, `Geth` does not support `pending` when estimating
        :return: Amount of gas needed for transaction
        :raises: ValueError
        """
        tx: TxParams = {"to": to}
        if from_:
            tx["from"] = from_
        if value:
            tx["value"] = value
        if data:
            tx["data"] = data
        if gas:
            tx["gas"] = gas
        if gas_price:
            tx["gasPrice"] = gas_price
        try:
            return self.w3.eth.estimate_gas(tx, block_identifier=block_identifier)
        except ValueError:
            if (
                block_identifier is not None
            ):  # Geth does not support setting `block_identifier`
                return self.w3.eth.estimate_gas(tx, block_identifier=None)
            else:
                raise

    @staticmethod
    def estimate_data_gas(data: bytes):
        if isinstance(data, str):
            data = HexBytes(data)

        gas = 0
        for byte in data:
            if not byte:
                gas += GAS_CALL_DATA_ZERO_BYTE
            else:
                gas += GAS_CALL_DATA_BYTE
        return gas

    def estimate_fee_eip1559(
        self, tx_speed: TxSpeed = TxSpeed.NORMAL
    ) -> Tuple[int, int]:
        """
        Check https://github.com/ethereum/execution-apis/blob/main/src/eth/fee_market.json#L15

        :return: Tuple[BaseFeePerGas, MaxPriorityFeePerGas]
        :raises: ValueError if not supported on the network
        """
        if tx_speed == TxSpeed.SLOWEST:
            percentile = 0
        elif tx_speed == TxSpeed.VERY_SLOW:
            percentile = 10
        elif tx_speed == TxSpeed.SLOW:
            percentile = 25
        elif tx_speed == TxSpeed.NORMAL:
            percentile = 50
        elif tx_speed == TxSpeed.FAST:
            percentile = 75
        elif tx_speed == TxSpeed.VERY_FAST:
            percentile = 90
        elif tx_speed == TxSpeed.FASTEST:
            percentile = 100

        result = self.w3.eth.fee_history(1, "latest", reward_percentiles=[percentile])
        # Get next block `base_fee_per_gas`
        base_fee_per_gas = result["baseFeePerGas"][-1]
        max_priority_fee_per_gas = result["reward"][0][0]
        return base_fee_per_gas, max_priority_fee_per_gas

    def set_eip1559_fees(
        self, tx: TxParams, tx_speed: TxSpeed = TxSpeed.NORMAL
    ) -> TxParams:
        """
        :return: TxParams in EIP1559 format
        :raises: ValueError if EIP1559 not supported
        """
        base_fee_per_gas, max_priority_fee_per_gas = self.estimate_fee_eip1559(tx_speed)
        tx = dict(tx)  # Don't modify provided tx
        if "gasPrice" in tx:
            del tx["gasPrice"]

        if "chainId" not in tx:
            tx["chainId"] = self.get_chain_id()

        tx["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        tx["maxFeePerGas"] = base_fee_per_gas + max_priority_fee_per_gas
        return tx

    def get_balance(
        self,
        address: ChecksumAddress,
        block_identifier: Optional[BlockIdentifier] = None,
    ):
        return self.w3.eth.get_balance(address, block_identifier)

    def get_transaction(self, tx_hash: EthereumHash) -> Optional[TxData]:
        try:
            return self.w3.eth.get_transaction(tx_hash)
        except TransactionNotFound:
            return None

    def get_transactions(self, tx_hashes: List[EthereumHash]) -> List[Optional[TxData]]:
        if not tx_hashes:
            return []
        payload = [
            {
                "id": i,
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": [HexBytes(tx_hash).hex()],
            }
            for i, tx_hash in enumerate(tx_hashes)
        ]
        results = self.raw_batch_request(payload)
        return [
            transaction_result_formatter(raw_tx) if raw_tx else None
            for raw_tx in results
        ]

    def get_transaction_receipt(
        self, tx_hash: EthereumHash, timeout=None
    ) -> Optional[TxReceipt]:
        try:
            if not timeout:
                tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            else:
                try:
                    tx_receipt = self.w3.eth.wait_for_transaction_receipt(
                        tx_hash, timeout=timeout
                    )
                except TimeExhausted:
                    return None

            # Parity returns tx_receipt even is tx is still pending, so we check `blockNumber` is not None
            return (
                tx_receipt
                if tx_receipt and tx_receipt["blockNumber"] is not None
                else None
            )
        except TransactionNotFound:
            return None

    def get_transaction_receipts(
        self, tx_hashes: Sequence[EthereumData]
    ) -> List[Optional[TxReceipt]]:
        if not tx_hashes:
            return []
        payload = [
            {
                "id": i,
                "jsonrpc": "2.0",
                "method": "eth_getTransactionReceipt",
                "params": [HexBytes(tx_hash).hex()],
            }
            for i, tx_hash in enumerate(tx_hashes)
        ]
        results = self.raw_batch_request(payload)
        receipts = []
        for tx_receipt in results:
            # Parity returns tx_receipt even is tx is still pending, so we check `blockNumber` is not None
            if tx_receipt and tx_receipt["blockNumber"] is not None:
                receipts.append(receipt_formatter(tx_receipt))
            else:
                receipts.append(None)
        return receipts

    def get_block(
        self, block_identifier: BlockIdentifier, full_transactions: bool = False
    ) -> Optional[BlockData]:
        try:
            return self.w3.eth.get_block(
                block_identifier, full_transactions=full_transactions
            )
        except BlockNotFound:
            return None

    def _parse_block_identifier(self, block_identifier: BlockIdentifier) -> str:
        if isinstance(block_identifier, int):
            return hex(block_identifier)
        elif isinstance(block_identifier, bytes):
            return HexBytes(block_identifier).hex()
        else:
            return block_identifier

    def get_blocks(
        self,
        block_identifiers: Iterable[BlockIdentifier],
        full_transactions: bool = False,
    ) -> List[Optional[BlockData]]:
        if not block_identifiers:
            return []
        payload = [
            {
                "id": i,
                "jsonrpc": "2.0",
                "method": "eth_getBlockByNumber"
                if isinstance(block_identifier, int)
                else "eth_getBlockByHash",
                "params": [
                    self._parse_block_identifier(block_identifier),
                    full_transactions,
                ],
            }
            for i, block_identifier in enumerate(block_identifiers)
        ]
        results = self.raw_batch_request(payload)
        blocks = []
        for raw_block in results:
            if raw_block:
                if "extraData" in raw_block:
                    del raw_block[
                        "extraData"
                    ]  # Remove extraData, raises some problems on parsing
                blocks.append(block_formatter(raw_block))
            else:
                blocks.append(None)
        return blocks

    def is_contract(self, contract_address: ChecksumAddress) -> bool:
        return bool(self.w3.eth.get_code(contract_address))

    @tx_with_exception_handling
    def send_transaction(self, transaction_dict: TxParams) -> HexBytes:
        return self.w3.eth.send_transaction(transaction_dict)

    @tx_with_exception_handling
    def send_raw_transaction(self, raw_transaction: EthereumData) -> HexBytes:
        return self.w3.eth.send_raw_transaction(bytes(raw_transaction))

    def send_unsigned_transaction(
        self,
        tx: TxParams,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        retry: bool = False,
        block_identifier: Optional[BlockIdentifier] = "pending",
    ) -> HexBytes:
        """
        Send a tx using an unlocked public key in the node or a private key. Both `public_key` and
        `private_key` cannot be `None`

        :param tx:
        :param private_key:
        :param public_key:
        :param retry: Retry if a problem with nonce is found
        :param block_identifier: For nonce calculation, recommended is `pending`
        :return: tx hash
        """

        # TODO Refactor this method, it's not working well with new version of the nodes
        if private_key:
            address = Account.from_key(private_key).address
        elif public_key:
            address = public_key
        else:
            logger.error(
                "No ethereum account provided. Need a public_key or private_key"
            )
            raise ValueError(
                "Ethereum account was not configured or unlocked in the node"
            )

        if tx.get("nonce") is None:
            tx["nonce"] = self.get_nonce_for_account(
                address, block_identifier=block_identifier
            )

        number_errors = 5
        while number_errors >= 0:
            try:
                if private_key:
                    signed_tx = self.w3.eth.account.sign_transaction(
                        tx, private_key=private_key
                    )
                    logger.debug(
                        "Sending %d wei from %s to %s", tx["value"], address, tx["to"]
                    )
                    try:
                        return self.send_raw_transaction(signed_tx.rawTransaction)
                    except TransactionAlreadyImported as e:
                        # Sometimes Parity 2.2.11 fails with Transaction already imported, even if it's not, but it's
                        # processed
                        tx_hash = signed_tx.hash
                        logger.error(
                            "Transaction with tx-hash=%s already imported: %s"
                            % (tx_hash.hex(), str(e))
                        )
                        return tx_hash
                elif public_key:
                    tx["from"] = address
                    return self.send_transaction(tx)
            except ReplacementTransactionUnderpriced as e:
                if not retry or not number_errors:
                    raise e
                current_nonce = tx["nonce"]
                tx["nonce"] = max(
                    current_nonce + 1,
                    self.get_nonce_for_account(
                        address, block_identifier=block_identifier
                    ),
                )
                logger.error(
                    "Tx with nonce=%d was already sent for address=%s, retrying with nonce=%s",
                    current_nonce,
                    address,
                    tx["nonce"],
                )
            except InvalidNonce as e:
                if not retry or not number_errors:
                    raise e
                logger.error(
                    "address=%s Tx with invalid nonce=%d, retrying recovering nonce again",
                    address,
                    tx["nonce"],
                )
                tx["nonce"] = self.get_nonce_for_account(
                    address, block_identifier=block_identifier
                )
                number_errors -= 1

    def send_eth_to(
        self,
        private_key: str,
        to: str,
        gas_price: int,
        value: Wei,
        gas: Optional[int] = None,
        nonce: Optional[int] = None,
        retry: bool = False,
        block_identifier: Optional[BlockIdentifier] = "pending",
    ) -> bytes:
        """
        Send ether using configured account

        :param private_key: to
        :param to: to
        :param gas_price: gas_price
        :param value: value(wei)
        :param gas: gas, defaults to 22000
        :param retry: Retry if a problem is found
        :param nonce: Nonce of sender account
        :param block_identifier: Block identifier for nonce calculation
        :return: tx_hash
        """

        assert fast_is_checksum_address(to)

        account = Account.from_key(private_key)

        tx: TxParams = {
            "from": account.address,
            "to": to,
            "value": value,
            "gas": gas or Wei(self.estimate_gas(to, account.address, value)),
            "gasPrice": Wei(gas_price),
        }

        if nonce is not None:
            tx["nonce"] = Nonce(nonce)

        return self.send_unsigned_transaction(
            tx, private_key=private_key, retry=retry, block_identifier=block_identifier
        )

    def check_tx_with_confirmations(
        self, tx_hash: EthereumHash, confirmations: int
    ) -> bool:
        """
        Check tx hash and make sure it has the confirmations required

        :param tx_hash: Hash of the tx
        :param confirmations: Minimum number of confirmations required
        :return: True if tx was mined with the number of confirmations required, False otherwise
        """
        tx_receipt = self.get_transaction_receipt(tx_hash)
        if not tx_receipt or tx_receipt["blockNumber"] is None:
            # If `tx_receipt` exists but `blockNumber` is `None`, tx is still pending (just Parity)
            return False
        else:
            return (
                self.w3.eth.block_number - tx_receipt["blockNumber"]
            ) >= confirmations

    @staticmethod
    def private_key_to_address(private_key):
        return Account.from_key(private_key).address
