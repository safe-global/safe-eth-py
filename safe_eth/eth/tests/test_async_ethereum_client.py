"""
Reuse the synchronous ``EthereumClient`` test suites against ``AsyncEthereumClient``.

A tiny :class:`SyncCallProxy` exposes every ``async_<name>`` coroutine of the async
client (and its managers) under its plain ``<name>``, running it on a persistent
event loop. The async test classes simply subclass the sync ones and swap
``cls.ethereum_client`` for the proxy, so the existing test bodies run verbatim
but exercise the async I/O paths. Methods without an ``async_`` sibling
(pure helpers, the deprecated ``get_transfer_history``) transparently fall back
to the inherited synchronous implementation.

Only the handful of tests that mock a *synchronous* internal (or the ``requests``
transport) need a thin override here to target the async equivalent.
"""

import asyncio
from unittest import mock

import aiohttp
from eth_account import Account

from ..async_ethereum_client import (
    AsyncEthereumClient,
    AsyncTracingManager,
    get_auto_async_ethereum_client,
)
from ..contracts import get_erc20_contract
from ..ethereum_network import EthereumNetwork
from .mocks.mock_internal_txs import creation_internal_txs, internal_txs_errored
from .test_ethereum_client import (
    FAILED_BATCH_CALL_RESULT,
    UNREACHABLE_NODE_URL,
    TestERC20Module,
    TestEthereumClient,
    TestEthereumClientConstruction,
    TestTracingManager,
    forbid_rpc_calls,
)

# Manager attributes that must themselves be wrapped in a proxy
_MANAGER_ATTRS = frozenset(("erc20", "erc721", "tracing", "batch_call_manager"))


class SyncCallProxy:
    """
    Drive an ``AsyncEthereumClient`` (or one of its managers) synchronously: an
    attribute ``foo`` resolves to ``async_foo`` run on ``loop`` when that coroutine
    exists, otherwise to the plain (synchronous) attribute.
    """

    def __init__(self, target, loop: asyncio.AbstractEventLoop):
        object.__setattr__(self, "_target", target)
        object.__setattr__(self, "_loop", loop)

    def __getattr__(self, name: str):
        target = object.__getattribute__(self, "_target")
        loop = object.__getattribute__(self, "_loop")

        async_attr = getattr(target, f"async_{name}", None)
        if async_attr is not None and callable(async_attr):

            def runner(*args, **kwargs):
                return loop.run_until_complete(async_attr(*args, **kwargs))

            runner.__name__ = name
            return runner

        attr = getattr(target, name)
        if name in _MANAGER_ATTRS:
            return SyncCallProxy(attr, loop)
        return attr


class AsyncEthereumClientTestMixin:
    """Swap ``cls.ethereum_client`` for a proxy wrapping a fresh AsyncEthereumClient."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()  # sets sync cls.ethereum_client / cls.w3, deploys Multicall
        cls._sync_ethereum_client = cls.ethereum_client
        cls._async_loop = asyncio.new_event_loop()
        cls._async_ethereum_client = AsyncEthereumClient(cls.ethereum_node_url)
        cls.ethereum_client = SyncCallProxy(cls._async_ethereum_client, cls._async_loop)

    @classmethod
    def tearDownClass(cls):
        cls._async_loop.run_until_complete(cls._async_ethereum_client.aclose())
        cls._async_loop.close()
        cls.ethereum_client = cls._sync_ethereum_client
        super().tearDownClass()


class TestAsyncERC20Module(AsyncEthereumClientTestMixin, TestERC20Module):
    def test_get_balances_with_failed_calls(self):
        with mock.patch.object(
            AsyncEthereumClient,
            "async_batch_call_same_function",
            return_value=FAILED_BATCH_CALL_RESULT,
        ):
            self._get_balances_with_failed_calls()


class TestAsyncTracingManager(AsyncEthereumClientTestMixin, TestTracingManager):
    def test_get_previous_trace(self):
        with mock.patch.object(
            AsyncTracingManager,
            "async_trace_transaction",
            return_value=internal_txs_errored,
        ):
            super().test_get_previous_trace()

    def test_get_next_traces(self):
        with mock.patch.object(
            AsyncTracingManager,
            "async_trace_transaction",
            return_value=creation_internal_txs,
        ):
            super().test_get_next_traces()

    def test_trace_filter(self):
        with self.assertRaisesMessage(AssertionError, "at least"):
            self.ethereum_client.tracing.trace_filter()

        # Ganache does not implement `trace_filter`; the async batch path surfaces
        # the node error as a ValueError instead of web3's Web3RPCError.
        with self.assertRaises(ValueError):
            self.ethereum_client.tracing.trace_filter(
                to_address=[Account.create().address]
            )

    def test_raw_batch_request(self):
        payload = [
            {
                "id": 0,
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": "0x5afea3f32970a22f4e63a815c174fa989e3b659826e5f52496662bb256baf3b2",
            },
            {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": "0x12ab96991ddd4ac55c28ace4e7b59bc64c514b55747e1b0ea3f5b269fbb39f6b",
            },
        ]
        with mock.patch.object(
            aiohttp.ClientResponse, "json", new_callable=mock.AsyncMock
        ) as json_mock:
            # Ankr: error dict instead of a list
            json_mock.return_value = {
                "jsonrpc": "2.0",
                "error": {
                    "code": 0,
                    "message": "you can't send more than 1000 requests in a batch",
                },
                "id": None,
            }
            with self.assertRaisesMessage(
                ValueError,
                "Batch request error: {'jsonrpc': '2.0', 'error': {'code': 0, 'message': "
                "\"you can't send more than 1000 requests in a batch\"}, 'id': None}",
            ):
                list(self.ethereum_client.raw_batch_request(payload))

            # Nodereal: list of a single error element
            json_mock.return_value = [
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32000,
                        "message": "batch length does not support more than 500",
                    },
                }
            ]
            with self.assertRaisesMessage(
                ValueError, f"Batch request error: {json_mock.return_value}"
            ):
                list(self.ethereum_client.raw_batch_request(payload))

            # Batching in chunks of 1: one result per chunk -> 2 results
            json_mock.return_value = [
                {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "result": {
                        "blockHash": "0x13e9e3262d9cf1c4d07d7324d95e6bddf27f07d7bddbdcc7df4e4ffb42a2e921",
                        "blockNumber": "0xa81a59",
                    },
                }
            ]
            results = list(
                self.ethereum_client.raw_batch_request(payload, batch_size=1)
            )
            self.assertEqual(len(results), 2)

            # Different number of results than payload requests
            big_payload = [
                {
                    "id": i,
                    "jsonrpc": "2.0",
                    "method": "eth_getTransactionByHash",
                    "params": "0x5afea3f32970a22f4e63a815c174fa989e3b659826e5f52496662bb256baf3b2",
                }
                for i in range(10)
            ]
            json_mock.return_value = [{}, {}]
            with self.assertRaisesMessage(
                ValueError,
                "Batch request error: Different number of results than payload requests were returned",
            ):
                list(self.ethereum_client.raw_batch_request(big_payload))


class TestAsyncEthereumClient(AsyncEthereumClientTestMixin, TestEthereumClient):
    def test_get_ethereum_network(self):
        # The sync test patches the synchronous `Eth.chain_id`, which does not
        # affect the async `AsyncEth` path. Caching behaviour is covered by the
        # sync suite; here we only check the happy path.
        self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.GANACHE)

    def test_set_eip1559_fees(self):
        with mock.patch.object(
            AsyncEthereumClient,
            "async_estimate_fee_eip1559",
            return_value=(2, 5),
        ):
            super().test_set_eip1559_fees()

    def test_get_auto_async_ethereum_client_is_cached(self):
        # Mirrors the sync `get_auto_ethereum_client` singleton behaviour
        self.assertIsInstance(get_auto_async_ethereum_client(), AsyncEthereumClient)
        self.assertIs(
            get_auto_async_ethereum_client(), get_auto_async_ethereum_client()
        )

    def test_async_batch_call_matches_sync(self):
        # Full parity: async batch_call uses Multicall just like the sync client, so
        # the result of a failed/undecodable call is identical on both paths.
        self.assertIsNotNone(
            self.ethereum_client.multicall, "Multicall path must be exercised"
        )
        random_address = Account.create().address

        def make_function():
            return get_erc20_contract(self.w3, random_address).functions.balanceOf(
                random_address
            )

        async_result = self.ethereum_client.batch_call(
            [make_function()], raise_exception=False
        )
        sync_result = self._sync_ethereum_client.batch_call(
            [make_function()], raise_exception=False
        )
        self.assertEqual(async_result, sync_result)


class TestAsyncEthereumClientConstruction(TestEthereumClientConstruction):
    """Reuse the sync construction tests, checking the async w3 instances too."""

    ethereum_client_cls = AsyncEthereumClient

    def get_w3_instances(self, ethereum_client):
        return (
            ethereum_client.w3,
            ethereum_client.slow_w3,
            ethereum_client.async_w3,
            ethereum_client.async_slow_w3,
        )

    def test_init_inside_running_event_loop(self):
        # Building the client in a coroutine (e.g. a FastAPI handler) must not
        # perform blocking calls, even with an unreachable RPC
        async def build():
            return self.ethereum_client_cls(UNREACHABLE_NODE_URL)

        with forbid_rpc_calls():
            asyncio.run(build())

    def test_async_get_multicall_performs_no_sync_requests(self):
        # First use of Multicall detects its address, but must do it through the
        # async RPC methods, never blocking the event loop
        async def run():
            async_ethereum_client = self.ethereum_client_cls(UNREACHABLE_NODE_URL)
            with mock.patch.object(
                AsyncEthereumClient,
                "async_get_chain_id",
                new_callable=mock.AsyncMock,
                return_value=EthereumNetwork.GNOSIS.value,
            ):
                multicall = await async_ethereum_client.async_get_multicall()
            self.assertIsNotNone(multicall)
            # Memoized, and shared with the `multicall` cached property
            self.assertIs(await async_ethereum_client.async_get_multicall(), multicall)
            self.assertIs(async_ethereum_client.multicall, multicall)

        with forbid_rpc_calls():
            asyncio.run(run())

    def test_async_get_multicall_network_not_supported(self):
        async def run():
            async_ethereum_client = self.ethereum_client_cls(UNREACHABLE_NODE_URL)
            with (
                mock.patch.object(
                    AsyncEthereumClient,
                    "async_get_chain_id",
                    new_callable=mock.AsyncMock,
                    return_value=4_815_162_342,  # EthereumNetwork.UNKNOWN
                ),
                mock.patch.object(
                    AsyncEthereumClient,
                    "async_is_contract",
                    new_callable=mock.AsyncMock,
                    return_value=False,
                ),
            ):
                self.assertIsNone(await async_ethereum_client.async_get_multicall())

        with forbid_rpc_calls():
            asyncio.run(run())
