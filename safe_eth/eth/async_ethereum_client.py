"""
Asynchronous counterpart of :mod:`safe_eth.eth.ethereum_client`.

``AsyncEthereumClient`` mirrors the feature set of ``EthereumClient`` but performs
I/O with Python's async stack (``web3`` :class:`~web3.AsyncWeb3` + ``aiohttp``).

To avoid duplicating logic, it **subclasses** ``EthereumClient`` (and the async
managers subclass the sync managers), reusing every pure/I-O-free helper
(payload builders, response decoders, tx error mapping, trace selectors...).
The only thing re-implemented is the transport: each ``async_<name>`` coroutine
mirrors its sync ``<name>`` sibling, ``await``-ing the async backend instead of
the blocking one. Any sync method that is *not* overridden keeps working through
the inherited blocking ``w3``/``requests`` session.

``batch_call``/``batch_call_same_function`` mirror the sync dispatch: they use
``Multicall`` (via :class:`~safe_eth.eth.multicall.AsyncMulticall`) when available
unless ``force_batch_call=True``, falling back to the JSON-RPC ``eth_call`` batch
path otherwise — so results match the sync client, including raw revert bytes for
failed calls on the Multicall path.
"""

import asyncio
import os
from functools import cache, cached_property, wraps
from logging import getLogger
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import aiohttp
from eth_abi.exceptions import DecodingError
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import URI, BlockNumber, ChecksumAddress, Hash32, HexAddress, HexStr
from hexbytes import HexBytes
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3._utils.method_formatters import trace_list_result_formatter
from web3.contract.contract import ContractFunction
from web3.exceptions import (
    BlockNotFound,
    TimeExhausted,
    TransactionNotFound,
    Web3Exception,
)
from web3.middleware import ExtraDataToPOAMiddleware
from web3.types import (
    BlockData,
    BlockIdentifier,
    BlockTrace,
    FilterTrace,
    Nonce,
    TxData,
    TxParams,
    TxReceipt,
    Wei,
)

from safe_eth.eth.utils import (
    fast_is_checksum_address,
    mk_contract_address,
    mk_contract_address_2,
)
from safe_eth.util import chunks

from ..util.util import to_0x_hex_str
from .constants import SAFE_SINGLETON_FACTORY_ADDRESS
from .contracts import get_erc20_contract, get_erc721_contract
from .ethereum_client import (
    BatchCallManager,
    Erc20Info,
    Erc20Manager,
    Erc721Info,
    Erc721Manager,
    EthereumClient,
    EthereumClientManager,
    EthereumTxSent,
    TracingManager,
    TxSpeed,
    build_eth_call_queries,
    build_jsonrpc_batch_payload,
    decode_eth_call_results,
    map_tx_exception,
    process_raw_batch_results,
    validate_batch_chunk,
)
from .ethereum_network import EthereumNetwork, EthereumNetworkNotSupported
from .exceptions import (
    BatchCallFunctionFailed,
    ContractAlreadyDeployed,
    InvalidERC20Info,
    InvalidERC721Info,
    InvalidNonce,
    ReplacementTransactionUnderpriced,
    TransactionAlreadyImported,
)
from .typing import BalanceDict, EthereumData, EthereumHash, LogReceiptDecoded
from .utils import decode_string_or_bytes32

logger = getLogger(__name__)


def async_tx_with_exception_handling(func):
    """Async counterpart of ``tx_with_exception_handling``."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (Web3Exception, ValueError) as exc:
            map_tx_exception(exc)

    return wrapper


class AsyncEthereumClientManager(EthereumClientManager):
    """Base manager exposing the async backends in addition to the sync ones."""

    def __init__(self, ethereum_client: "AsyncEthereumClient"):
        super().__init__(ethereum_client)
        self.ethereum_client: "AsyncEthereumClient" = ethereum_client
        self.async_w3: AsyncWeb3 = ethereum_client.async_w3
        self.async_slow_w3: AsyncWeb3 = ethereum_client.async_slow_w3


class AsyncBatchCallManager(BatchCallManager, AsyncEthereumClientManager):
    async def async_batch_call_custom(
        self,
        payloads: Sequence[Dict[str, Any]],
        raise_exception: bool = True,
        block_identifier: Optional[BlockIdentifier] = "latest",
        batch_size: Optional[int] = None,
    ) -> List[Optional[Any]]:
        payloads = list(payloads)
        if not payloads:
            return []

        queries = build_eth_call_queries(payloads, block_identifier)
        batch_size = batch_size or self.ethereum_client.batch_request_max_size
        session = await self.ethereum_client.get_async_session()
        all_results: List[Any] = []
        for chunk in chunks(queries, batch_size):
            async with session.post(
                self.ethereum_node_url,
                json=chunk,
                timeout=aiohttp.ClientTimeout(total=self.slow_timeout),
            ) as response:
                if not response.ok:
                    raise ConnectionError(
                        f"Error connecting to {self.ethereum_node_url}: {await response.text()}"
                    )
                all_results.extend(validate_batch_chunk(await response.json(), chunk))

        return_values, errors = decode_eth_call_results(payloads, all_results)
        if errors and raise_exception:
            raise BatchCallFunctionFailed(f"Errors returned {errors}")
        return return_values

    async def async_batch_call(
        self,
        contract_functions: Sequence[ContractFunction],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Any]]:
        if not contract_functions:
            return []
        payloads = self._build_call_payloads(contract_functions, from_address)
        return await self.async_batch_call_custom(
            payloads, raise_exception=raise_exception, block_identifier=block_identifier
        )

    async def async_batch_call_same_function(
        self,
        contract_function: ContractFunction,
        contract_addresses: Sequence[ChecksumAddress],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Any]]:
        if contract_function is None:
            raise ValueError("Contract function is required")
        if not contract_addresses:
            return []
        payloads = self._build_same_function_payloads(
            contract_function, contract_addresses, from_address
        )
        return await self.async_batch_call_custom(
            payloads, raise_exception=raise_exception, block_identifier=block_identifier
        )


class AsyncErc20Manager(Erc20Manager, AsyncEthereumClientManager):
    async def async_get_balance(
        self, address: ChecksumAddress, token_address: ChecksumAddress
    ) -> int:
        return (
            await get_erc20_contract(self.async_w3, token_address)
            .functions.balanceOf(address)
            .call()
        )

    async def async_get_balances(
        self,
        address: ChecksumAddress,
        token_addresses: Sequence[ChecksumAddress],
        include_native_balance: bool = True,
    ) -> List[BalanceDict]:
        balances = await self.ethereum_client.async_batch_call_same_function(
            get_erc20_contract(self.w3).functions.balanceOf(address),
            token_addresses,
            raise_exception=False,
        )
        return_balances = self._build_balance_dicts(token_addresses, balances)
        if not include_native_balance:
            return return_balances
        native_balance = await self.ethereum_client.async_get_balance(address)
        return [
            BalanceDict(balance=native_balance, token_address=None)
        ] + return_balances

    async def async_get_name(self, erc20_address: ChecksumAddress) -> str:
        data = self._build_fn_call_data(self.w3, erc20_address, "name")
        return decode_string_or_bytes32(
            await self.async_w3.eth.call({"to": erc20_address, "data": data})
        )

    async def async_get_symbol(self, erc20_address: ChecksumAddress) -> str:
        data = self._build_fn_call_data(self.w3, erc20_address, "symbol")
        return decode_string_or_bytes32(
            await self.async_w3.eth.call({"to": erc20_address, "data": data})
        )

    async def async_get_decimals(self, erc20_address: ChecksumAddress) -> int:
        return (
            await get_erc20_contract(self.async_w3, erc20_address)
            .functions.decimals()
            .call()
        )

    async def async_get_info(self, erc20_address: ChecksumAddress) -> Erc20Info:
        payload = self._build_info_payload(erc20_address)
        session = await self.ethereum_client.get_async_session()
        async with session.post(
            self.ethereum_node_url,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=self.slow_timeout),
        ) as response:
            if not response.ok:
                raise InvalidERC20Info(await response.read())
            return self._parse_info_response(erc20_address, await response.json())

    async def async_get_total_transfer_history(
        self,
        addresses: Optional[Sequence[ChecksumAddress]] = None,
        from_block: BlockIdentifier = BlockNumber(0),
        to_block: Optional[BlockIdentifier] = None,
        token_address: Optional[ChecksumAddress] = None,
    ) -> List[LogReceiptDecoded]:
        all_topics, parameters = self._build_transfer_history_filters(
            addresses, from_block, to_block, token_address
        )
        events_per_topic = [
            await self.async_slow_w3.eth.get_logs({**parameters, "topics": topics})
            for topics in all_topics
        ]
        return self._decode_and_sort_transfer_events(events_per_topic)

    async def async_send_tokens(
        self,
        to: str,
        amount: int,
        erc20_address: ChecksumAddress,
        private_key: str,
        nonce: Optional[int] = None,
        gas_price: Optional[int] = None,
        gas: Optional[int] = None,
    ) -> bytes:
        erc20 = get_erc20_contract(self.async_w3, erc20_address)
        account = Account.from_key(private_key)
        tx_options: TxParams = {"from": account.address}
        if nonce:
            tx_options["nonce"] = Nonce(nonce)
        if gas_price:
            tx_options["gasPrice"] = Wei(gas_price)
        if gas:
            tx_options["gas"] = Wei(gas)

        tx = await erc20.functions.transfer(to, amount).build_transaction(tx_options)
        return await self.ethereum_client.async_send_unsigned_transaction(
            tx, private_key=private_key
        )


class AsyncErc721Manager(Erc721Manager, AsyncEthereumClientManager):
    async def async_get_balance(
        self, address: ChecksumAddress, token_address: ChecksumAddress
    ) -> int:
        return (
            await get_erc721_contract(self.async_w3, token_address)
            .functions.balanceOf(address)
            .call()
        )

    async def async_get_balances(
        self, address: ChecksumAddress, token_addresses: Sequence[ChecksumAddress]
    ) -> List:
        function = get_erc721_contract(self.w3).functions.balanceOf(address)
        balances = await self.ethereum_client.async_batch_call_same_function(
            function,
            token_addresses,
            raise_exception=False,
        )
        return self._build_token_balances(token_addresses, balances)

    async def async_get_info(self, token_address: ChecksumAddress) -> Erc721Info:
        erc721_contract = get_erc721_contract(self.w3, token_address)
        try:
            name, symbol = cast(
                List[str],
                await self.ethereum_client.async_batch_call(
                    [
                        erc721_contract.functions.name(),
                        erc721_contract.functions.symbol(),
                    ]
                ),
            )
            return Erc721Info(name, symbol)
        except (DecodingError, ValueError):  # Not all the ERC721 have metadata
            raise InvalidERC721Info

    async def async_get_owners(
        self, token_addresses_with_token_ids: Sequence[Tuple[ChecksumAddress, int]]
    ) -> List[Optional[ChecksumAddress]]:
        functions = self._build_token_id_functions(
            "ownerOf", token_addresses_with_token_ids
        )
        return self._format_owners(
            await self.ethereum_client.async_batch_call(
                functions, raise_exception=False
            )
        )

    async def async_get_token_uris(
        self, token_addresses_with_token_ids: Sequence[Tuple[ChecksumAddress, int]]
    ) -> List[Optional[str]]:
        functions = self._build_token_id_functions(
            "tokenURI", token_addresses_with_token_ids
        )
        return self._format_token_uris(
            await self.ethereum_client.async_batch_call(
                functions, raise_exception=False
            )
        )


class AsyncTracingManager(TracingManager, AsyncEthereumClientManager):
    async def _async_trace_rpc(self, method: str, params: Sequence[Any]) -> Any:
        """Perform a single tracing JSON-RPC call (``AsyncWeb3`` has no ``tracing`` module)."""
        payload = build_jsonrpc_batch_payload([(method, params)])
        results = await self.ethereum_client.async_raw_batch_request(payload)
        return results[0]

    async def async_trace_block(
        self, block_identifier: BlockIdentifier
    ) -> List[BlockTrace]:
        result = await self._async_trace_rpc(
            "trace_block",
            [
                (
                    hex(block_identifier)
                    if isinstance(block_identifier, int)
                    else block_identifier
                )
            ],
        )
        return trace_list_result_formatter(result)  # type: ignore[arg-type]

    async def async_trace_blocks(
        self, block_identifiers: Sequence[BlockIdentifier]
    ) -> List[List[BlockTrace]]:
        if not block_identifiers:
            return []
        payload = build_jsonrpc_batch_payload(
            [
                ("trace_block", [hex(b) if isinstance(b, int) else b])
                for b in block_identifiers
            ]
        )
        results = await self.ethereum_client.async_raw_batch_request(payload)
        return [trace_list_result_formatter(block_traces) for block_traces in results]  # type: ignore[arg-type]

    async def async_trace_transaction(self, tx_hash: EthereumHash) -> List[FilterTrace]:
        result = await self._async_trace_rpc(
            "trace_transaction", [to_0x_hex_str(HexBytes(tx_hash))]
        )
        return trace_list_result_formatter(result)  # type: ignore[arg-type]

    async def async_trace_transactions(
        self, tx_hashes: Sequence[EthereumHash]
    ) -> List[List[FilterTrace]]:
        if not tx_hashes:
            return []
        payload = build_jsonrpc_batch_payload(
            [
                ("trace_transaction", [to_0x_hex_str(HexBytes(tx_hash))])
                for tx_hash in tx_hashes
            ]
        )
        results = await self.ethereum_client.async_raw_batch_request(payload)
        return [trace_list_result_formatter(tx_traces) for tx_traces in results]  # type: ignore[arg-type]

    async def async_trace_filter(
        self,
        from_block: int = 1,
        to_block: Optional[int] = None,
        from_address: Optional[Sequence[ChecksumAddress]] = None,
        to_address: Optional[Sequence[ChecksumAddress]] = None,
        after: Optional[int] = None,
        count: Optional[int] = None,
    ) -> List[FilterTrace]:
        """
        Async counterpart of :meth:`TracingManager.trace_filter`.

        .. note::
            Tracing is issued as a raw JSON-RPC call (``AsyncWeb3`` has no
            ``tracing`` module). A node error (e.g. ``trace_filter`` unsupported)
            therefore surfaces as a ``ValueError`` from the batch layer, not as
            web3's ``Web3RPCError`` raised by the sync path.
        """
        parameters = self._build_trace_filter_params(
            from_block, to_block, from_address, to_address, after, count
        )
        result = await self._async_trace_rpc("trace_filter", [parameters])
        return trace_list_result_formatter(result)  # type: ignore[arg-type]

    async def async_get_previous_trace(
        self,
        tx_hash: EthereumHash,
        trace_address: Sequence[int],
        number_traces: int = 1,
        skip_delegate_calls: bool = False,
    ) -> Optional[Dict[str, Any]]:
        if len(trace_address) < number_traces:
            return None
        return self._select_previous_trace(
            await self.async_trace_transaction(tx_hash),
            trace_address,
            number_traces,
            skip_delegate_calls,
        )

    async def async_get_next_traces(
        self,
        tx_hash: EthereumHash,
        trace_address: Sequence[int],
        remove_delegate_calls: bool = False,
        remove_calls: bool = False,
    ) -> List[FilterTrace]:
        return self._select_next_traces(
            await self.async_trace_transaction(tx_hash),
            trace_address,
            remove_delegate_calls,
            remove_calls,
        )


class AsyncEthereumClient(EthereumClient):
    """
    Async version of :class:`~safe_eth.eth.ethereum_client.EthereumClient`.

    Build it like the sync client and use the ``async_``-prefixed coroutines. The
    blocking ``w3``/``http_session`` are still available for the inherited sync
    methods, so a single instance exposes both worlds.

    The ``aiohttp`` session used for JSON-RPC batches is created lazily, one per
    running event loop, so the same instance works across loops (and is safe to
    create outside a running loop, e.g. in ``__init__``).
    """

    def __init__(
        self,
        ethereum_node_url: URI = URI("http://localhost:8545"),
        provider_timeout: int = 15,
        slow_provider_timeout: int = 60,
        retry_count: int = 1,
        use_request_caching: bool = True,
        batch_request_max_size: int = 500,
    ):
        # Builds the blocking w3/slow_w3 + detects the network (cached chainId)
        super().__init__(
            ethereum_node_url,
            provider_timeout=provider_timeout,
            slow_provider_timeout=slow_provider_timeout,
            retry_count=retry_count,
            use_request_caching=use_request_caching,
            batch_request_max_size=batch_request_max_size,
        )

        # aiohttp sessions for raw JSON-RPC batches, one per event loop
        self._async_http_sessions: Dict[Any, aiohttp.ClientSession] = {}

        self.async_w3_provider = AsyncHTTPProvider(
            self.ethereum_node_url,
            cache_allowed_requests=use_request_caching,
            request_kwargs={"timeout": aiohttp.ClientTimeout(total=provider_timeout)},
        )
        self.async_w3_slow_provider = AsyncHTTPProvider(
            self.ethereum_node_url,
            cache_allowed_requests=use_request_caching,
            request_kwargs={
                "timeout": aiohttp.ClientTimeout(total=slow_provider_timeout)
            },
        )
        self.async_w3: AsyncWeb3 = AsyncWeb3(self.async_w3_provider)
        self.async_slow_w3: AsyncWeb3 = AsyncWeb3(self.async_w3_slow_provider)

        for async_w3 in self.async_w3, self.async_slow_w3:
            # Don't spend resources converting dictionaries to attribute dictionaries
            async_w3.middleware_onion.remove("attrdict")

        # POA middleware (reuse the network already detected by the sync __init__)
        try:
            inject_poa = self.get_network() != EthereumNetwork.MAINNET
        except (IOError, OSError):
            inject_poa = True
        if inject_poa:
            for async_w3 in self.async_w3, self.async_slow_w3:
                async_w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        # Replace the sync managers built by super().__init__ with async-capable ones
        self.erc20 = AsyncErc20Manager(self)
        self.erc721 = AsyncErc721Manager(self)
        self.tracing = AsyncTracingManager(self)
        self.batch_call_manager = AsyncBatchCallManager(self)

    def __str__(self):
        return f"AsyncEthereumClient for url={self.ethereum_node_url}"

    @cached_property
    def multicall(self) -> Optional["AsyncMulticall"]:  # type: ignore # noqa F821
        """Async ``Multicall`` for this network, or ``None`` if unsupported."""
        # Imported lazily to avoid a circular import (multicall imports the package),
        # mirroring EthereumClient.multicall.
        from .multicall import AsyncMulticall

        try:
            return AsyncMulticall(self)
        except EthereumNetworkNotSupported:
            logger.warning("Multicall not supported for this network")
            return None

    # --- Session lifecycle ------------------------------------------------

    async def get_async_session(self) -> aiohttp.ClientSession:
        """
        Return (creating if needed) the ``aiohttp`` session bound to the running loop.

        Intended usage is a single long-lived event loop (e.g. an ``asyncio`` /
        FastAPI app), with :meth:`aclose` (or ``async with self``) closing the
        session on shutdown.

        .. warning::
            Do **not** drive this client with repeated ``asyncio.run(...)`` calls:
            each builds a session on a throwaway loop that can no longer be
            ``await``-ed to ``close()`` once that loop is gone. The pruning below
            only frees the bookkeeping entry — the orphaned session still emits
            "Unclosed client session" until garbage-collected. Reuse one loop and
            call :meth:`aclose`.
        """
        loop = asyncio.get_running_loop()
        # Drop sessions whose event loop is already closed (they can't be awaited
        # to `close()` anymore); prevents unbounded growth under run-per-call usage.
        for stale_loop in [
            stale for stale in self._async_http_sessions if stale.is_closed()
        ]:
            self._async_http_sessions.pop(stale_loop, None)

        session = self._async_http_sessions.get(loop)
        if session is None or session.closed:
            session = aiohttp.ClientSession()
            self._async_http_sessions[loop] = session
        return session

    async def aclose(self) -> None:
        """Close every open ``aiohttp`` session and the async providers."""
        for session in list(self._async_http_sessions.values()):
            if not session.closed:
                await session.close()
        self._async_http_sessions.clear()

    async def __aenter__(self) -> "AsyncEthereumClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()

    # --- Raw batch --------------------------------------------------------

    async def async_raw_batch_request(
        self, payload: Sequence[Dict[str, Any]], batch_size: Optional[int] = None
    ) -> List[Any]:
        """Async version of :meth:`EthereumClient.raw_batch_request` (returns a list)."""
        batch_size = batch_size or self.batch_request_max_size
        session = await self.get_async_session()
        all_results: List[Any] = []
        for payload_chunk in chunks(payload, batch_size):
            async with session.post(
                self.ethereum_node_url,
                json=payload_chunk,
                timeout=aiohttp.ClientTimeout(total=self.slow_timeout),
            ) as response:
                if not response.ok:
                    content = await response.read()
                    logger.error(
                        "Problem doing raw batch request with payload=%s status_code=%d result=%s",
                        payload_chunk,
                        response.status,
                        content,
                    )
                    raise ValueError(f"Batch request error: {content!r}")
                results = await response.json()
            all_results.extend(process_raw_batch_results(results, payload_chunk))
        return all_results

    # --- Cached / metadata getters ---------------------------------------

    async def async_get_block_number(self) -> int:
        return await self.async_w3.eth.block_number

    async def async_get_chain_id(self) -> int:
        if "chain_id" not in self._cache:
            self._cache["chain_id"] = int(await self.async_w3.eth.chain_id)
        return self._cache["chain_id"]

    async def async_get_client_version(self) -> str:
        if "client_version" not in self._cache:
            self._cache["client_version"] = await self.async_w3.client_version
        return self._cache["client_version"]

    async def async_get_network(self) -> EthereumNetwork:
        return EthereumNetwork(await self.async_get_chain_id())

    async def async_is_eip1559_supported(self) -> bool:
        if "is_eip1559_supported" not in self._cache:
            try:
                await self.async_w3.eth.fee_history(
                    1, "latest", reward_percentiles=[50]
                )
                self._cache["is_eip1559_supported"] = True
            except (Web3Exception, ValueError):
                self._cache["is_eip1559_supported"] = False
        return self._cache["is_eip1559_supported"]

    async def async_get_singleton_factory_address(
        self,
    ) -> Optional[ChecksumAddress]:
        if "singleton_factory_address" not in self._cache:
            address = os.environ.get(
                "SAFE_SINGLETON_FACTORY_ADDRESS", SAFE_SINGLETON_FACTORY_ADDRESS
            )
            address_checksum = ChecksumAddress(HexAddress(HexStr(address)))
            self._cache["singleton_factory_address"] = (
                address_checksum
                if await self.async_is_contract(address_checksum)
                else None
            )
        return self._cache["singleton_factory_address"]

    # --- Reads ------------------------------------------------------------

    async def async_get_balance(
        self,
        address: ChecksumAddress,
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> int:
        return await self.async_w3.eth.get_balance(address, block_identifier)

    async def async_get_transaction(self, tx_hash: EthereumHash) -> Optional[TxData]:
        try:
            return await self.async_w3.eth.get_transaction(tx_hash)
        except TransactionNotFound:
            return None

    async def async_get_transactions(
        self, tx_hashes: Sequence[EthereumHash]
    ) -> List[Optional[TxData]]:
        if not tx_hashes:
            return []
        payload = build_jsonrpc_batch_payload(
            [
                ("eth_getTransactionByHash", [to_0x_hex_str(HexBytes(tx_hash))])
                for tx_hash in tx_hashes
            ]
        )
        return self._format_transactions(await self.async_raw_batch_request(payload))

    async def async_get_transaction_receipt(
        self, tx_hash: EthereumHash, timeout=None
    ) -> Optional[TxReceipt]:
        try:
            if not timeout:
                tx_receipt = await self.async_w3.eth.get_transaction_receipt(tx_hash)
            else:
                try:
                    tx_receipt = await self.async_w3.eth.wait_for_transaction_receipt(
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

    async def async_get_transaction_receipts(
        self, tx_hashes: Sequence[EthereumData]
    ) -> List[Optional[TxReceipt]]:
        if not tx_hashes:
            return []
        payload = build_jsonrpc_batch_payload(
            [
                ("eth_getTransactionReceipt", [to_0x_hex_str(HexBytes(tx_hash))])
                for tx_hash in tx_hashes
            ]
        )
        return self._format_receipts(await self.async_raw_batch_request(payload))

    async def async_get_block(
        self, block_identifier: BlockIdentifier, full_transactions: bool = False
    ) -> Optional[BlockData]:
        try:
            return await self.async_w3.eth.get_block(
                block_identifier, full_transactions=full_transactions
            )
        except BlockNotFound:
            return None

    async def async_get_blocks(
        self,
        block_identifiers: Sequence[BlockIdentifier],
        full_transactions: bool = False,
    ) -> List[Optional[BlockData]]:
        if not block_identifiers:
            return []
        payload = build_jsonrpc_batch_payload(
            [
                (
                    (
                        "eth_getBlockByNumber"
                        if isinstance(block_identifier, int)
                        else "eth_getBlockByHash"
                    ),
                    [self._parse_block_identifier(block_identifier), full_transactions],
                )
                for block_identifier in block_identifiers
            ]
        )
        return self._format_blocks(await self.async_raw_batch_request(payload))

    async def async_is_contract(self, contract_address: ChecksumAddress) -> bool:
        return bool(await self.async_w3.eth.get_code(contract_address))

    async def async_get_nonce_for_account(
        self,
        address: ChecksumAddress,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> Nonce:
        return await self.async_w3.eth.get_transaction_count(
            address, block_identifier=block_identifier
        )

    # --- Gas / fees -------------------------------------------------------

    async def async_estimate_gas(
        self,
        to: str,
        from_: Optional[str] = None,
        value: Optional[int] = None,
        data: Optional[EthereumData] = None,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> int:
        tx: TxParams = {"to": to}
        if from_:
            tx["from"] = from_
        if value:
            tx["value"] = Wei(value)
        if data:
            tx["data"] = data
        if gas:
            tx["gas"] = gas
        if gas_price:
            tx["gasPrice"] = Wei(gas_price)
        try:
            return await self.async_w3.eth.estimate_gas(
                tx, block_identifier=block_identifier
            )
        except (Web3Exception, ValueError):
            if block_identifier is not None:
                # Geth does not support setting `block_identifier`
                return await self.async_w3.eth.estimate_gas(tx, block_identifier=None)
            raise

    async def async_estimate_fee_eip1559(
        self, tx_speed: TxSpeed = TxSpeed.NORMAL
    ) -> Tuple[int, int]:
        percentile = self._tx_speed_percentile(tx_speed)
        result = await self.async_w3.eth.fee_history(
            1, "latest", reward_percentiles=[percentile]
        )
        return self._parse_fee_history(result)

    async def async_set_eip1559_fees(
        self, tx: TxParams, tx_speed: TxSpeed = TxSpeed.NORMAL
    ) -> TxParams:
        base_fee_per_gas, max_priority_fee_per_gas = (
            await self.async_estimate_fee_eip1559(tx_speed)
        )
        tx = TxParams(**tx)  # Don't modify provided tx
        if "gasPrice" in tx:
            del tx["gasPrice"]
        if "chainId" not in tx:
            tx["chainId"] = await self.async_get_chain_id()
        tx["maxPriorityFeePerGas"] = Wei(max_priority_fee_per_gas)
        tx["maxFeePerGas"] = Wei(base_fee_per_gas + max_priority_fee_per_gas)
        return tx

    # --- Batch call (no Multicall, always JSON-RPC batch path) ------------

    async def async_batch_call(
        self,
        contract_functions: Sequence[ContractFunction],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        force_batch_call: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Union[bytes, Any]]]:
        """
        Async counterpart of :meth:`EthereumClient.batch_call`. Uses ``Multicall``
        when available (unless ``force_batch_call=True``), matching the sync client,
        including raw revert bytes for failed calls on the Multicall path.
        """
        if self.multicall and not force_batch_call:  # Multicall is more optimal
            return [
                result.return_data_decoded
                for result in await self.multicall.async_try_aggregate(
                    contract_functions,
                    require_success=raise_exception,
                    block_identifier=block_identifier,
                )
            ]
        return await self.batch_call_manager.async_batch_call(
            contract_functions,
            from_address=from_address,
            raise_exception=raise_exception,
            block_identifier=block_identifier,
        )

    async def async_batch_call_same_function(
        self,
        contract_function: ContractFunction,
        contract_addresses: Sequence[ChecksumAddress],
        from_address: Optional[ChecksumAddress] = None,
        raise_exception: bool = True,
        force_batch_call: bool = False,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> List[Optional[Union[bytes, Any]]]:
        """
        Async counterpart of :meth:`EthereumClient.batch_call_same_function`. Uses
        ``Multicall`` when available (unless ``force_batch_call=True``), matching the
        sync client.
        """
        if self.multicall and not force_batch_call:  # Multicall is more optimal
            return [
                result.return_data_decoded
                for result in await self.multicall.async_try_aggregate_same_function(
                    contract_function,
                    contract_addresses,
                    require_success=raise_exception,
                    block_identifier=block_identifier,
                )
            ]
        return await self.batch_call_manager.async_batch_call_same_function(
            contract_function,
            contract_addresses,
            from_address=from_address,
            raise_exception=raise_exception,
            block_identifier=block_identifier,
        )

    # --- Sends ------------------------------------------------------------

    @async_tx_with_exception_handling
    async def async_send_transaction(self, transaction_dict: TxParams) -> HexBytes:
        return await self.async_w3.eth.send_transaction(transaction_dict)

    @async_tx_with_exception_handling
    async def async_send_raw_transaction(
        self, raw_transaction: EthereumData
    ) -> HexBytes:
        return await self.async_w3.eth.send_raw_transaction(HexBytes(raw_transaction))

    async def async_send_unsigned_transaction(
        self,
        tx: TxParams,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        retry: bool = False,
        block_identifier: Optional[BlockIdentifier] = "pending",
    ) -> HexBytes:
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
            tx["nonce"] = await self.async_get_nonce_for_account(
                address, block_identifier=block_identifier
            )

        number_errors = 5
        while number_errors >= 0:
            try:
                if private_key:
                    signed_tx = self.async_w3.eth.account.sign_transaction(
                        tx, private_key=private_key
                    )
                    logger.debug(
                        "Sending %d wei from %s to %s", tx["value"], address, tx["to"]
                    )
                    try:
                        return await self.async_send_raw_transaction(
                            signed_tx.raw_transaction
                        )
                    except TransactionAlreadyImported as e:
                        # Parity 2.2.11 sometimes fails with "already imported" even if processed
                        tx_hash = signed_tx.hash
                        logger.error(
                            "Transaction with tx-hash=%s already imported: %s"
                            % (tx_hash.hex(), str(e))
                        )
                        return tx_hash
                elif public_key:
                    tx["from"] = address
                    return await self.async_send_transaction(tx)
            except ReplacementTransactionUnderpriced as e:
                if not retry or not number_errors:
                    raise e
                current_nonce = tx["nonce"]
                tx["nonce"] = max(
                    current_nonce + 1,
                    await self.async_get_nonce_for_account(
                        address, block_identifier=block_identifier
                    ),
                )
                logger.error(
                    "Tx with nonce=%d was already sent for address=%s, retrying with nonce=%s",
                    current_nonce,
                    address,
                    tx["nonce"],
                )
                number_errors -= 1
            except InvalidNonce as e:
                if not retry or not number_errors:
                    raise e
                logger.error(
                    "address=%s Tx with invalid nonce=%d, retrying recovering nonce again",
                    address,
                    tx["nonce"],
                )
                tx["nonce"] = await self.async_get_nonce_for_account(
                    address, block_identifier=block_identifier
                )
                number_errors -= 1
        raise ValueError(
            f"Could not send transaction for address={address}, retries exhausted"
        )

    async def async_send_eth_to(
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
        assert fast_is_checksum_address(to)
        account = Account.from_key(private_key)
        tx: TxParams = {
            "from": account.address,
            "to": to,
            "value": value,
            "gas": gas
            or Wei(await self.async_estimate_gas(to, account.address, value)),
            "gasPrice": Wei(gas_price),
            "chainId": await self.async_get_chain_id(),
        }
        if nonce is not None:
            tx["nonce"] = Nonce(nonce)
        return await self.async_send_unsigned_transaction(
            tx, private_key=private_key, retry=retry, block_identifier=block_identifier
        )

    async def async_check_tx_with_confirmations(
        self, tx_hash: EthereumHash, confirmations: int
    ) -> bool:
        tx_receipt = await self.async_get_transaction_receipt(tx_hash)
        if not tx_receipt or tx_receipt["blockNumber"] is None:
            return False
        return (
            await self.async_w3.eth.block_number - tx_receipt["blockNumber"]
        ) >= confirmations

    async def async_deploy_and_initialize_contract(
        self,
        deployer_account: LocalAccount,
        constructor_data: Union[bytes, HexStr],
        initializer_data: Optional[Union[bytes, HexStr]] = None,
        check_receipt: bool = True,
        deterministic: bool = True,
    ) -> EthereumTxSent:
        contract_address: Optional[ChecksumAddress] = None
        assert (
            constructor_data or initializer_data
        ), "At least constructor_data or initializer_data must be provided"
        tx_hash: Optional[HexBytes] = None
        tx: Optional[TxParams] = None
        gas_price = await self.async_w3.eth.gas_price
        chain_id = await self.async_get_chain_id()
        for data in (constructor_data, initializer_data):
            if data:  # initializer_data is not mandatory
                data = HexBytes(data)
                tx = {
                    "from": deployer_account.address,
                    "data": data,
                    "gasPrice": gas_price,
                    "value": Wei(0),
                    "to": contract_address if contract_address else "",
                    "chainId": chain_id,
                    "nonce": await self.async_get_nonce_for_account(
                        deployer_account.address
                    ),
                }
                if not contract_address:
                    if deterministic and (
                        singleton_factory_address := await self.async_get_singleton_factory_address()
                    ):
                        salt = HexBytes("0" * 64)
                        tx["data"] = salt + data  # 32 bytes salt for singleton factory
                        tx["to"] = singleton_factory_address
                        contract_address = mk_contract_address_2(
                            singleton_factory_address, salt, data
                        )
                        if await self.async_is_contract(contract_address):
                            raise ContractAlreadyDeployed(
                                f"Contract {contract_address} already deployed",
                                contract_address,
                            )
                    else:
                        contract_address = mk_contract_address(tx["from"], tx["nonce"])

                tx["gas"] = await self.async_w3.eth.estimate_gas(tx)
                tx_hash = await self.async_send_unsigned_transaction(
                    tx, private_key=to_0x_hex_str(deployer_account.key)
                )
                if check_receipt:
                    tx_receipt = await self.async_get_transaction_receipt(
                        Hash32(tx_hash), timeout=60
                    )
                    assert tx_receipt
                    assert tx_receipt["status"]

        if tx_hash is not None and tx is not None:
            return EthereumTxSent(tx_hash, tx, contract_address)
        raise ValueError("No contract was deployed/initialized")


@cache
def get_auto_async_ethereum_client() -> "AsyncEthereumClient":
    """
    Build an ``AsyncEthereumClient`` from environment variables and cache it as a
    singleton (mirrors ``get_auto_ethereum_client``).
    """
    try:
        from django.conf import settings

        ethereum_node_url = settings.ETHEREUM_NODE_URL
    except ModuleNotFoundError:
        ethereum_node_url = os.environ.get("ETHEREUM_NODE_URL")
    return AsyncEthereumClient(
        ethereum_node_url,
        provider_timeout=int(os.environ.get("ETHEREUM_RPC_TIMEOUT", 10)),
        slow_provider_timeout=int(os.environ.get("ETHEREUM_RPC_SLOW_TIMEOUT", 60)),
        retry_count=int(os.environ.get("ETHEREUM_RPC_RETRY_COUNT", 1)),
        batch_request_max_size=int(
            os.environ.get("ETHEREUM_RPC_BATCH_REQUEST_MAX_SIZE", 500)
        ),
    )
