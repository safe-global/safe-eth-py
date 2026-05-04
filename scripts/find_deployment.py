# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.27",
# ]
# ///
"""Find the deployment block and transaction hash for Safe contracts.

Uses binary search on eth_getCode to locate the first block where contract
bytecode is present, then scans that block for transactions sent to the Safe
singleton factory (SINGLETON_FACTORY) as deployment candidates.

Usage
-----
    uv run scripts/find_deployment.py --rpc-url <RPC_URL> [--start-block N] [--end-block N] <ADDRESS> [ADDRESS ...]

Arguments
---------
    --rpc-url       (required) JSON-RPC HTTP endpoint, e.g. https://eth.drpc.org
    --start-block   (optional) Lower bound for binary search. Defaults to 0.
    --end-block     (optional) Upper bound for binary search. Defaults to the latest block.
    ADDRESS         One or more contract addresses to look up.

Examples
--------
    # Single contract
    uv run scripts/find_deployment.py --rpc-url https://eth.drpc.org \
        0x14F2982D601c9458F93bd70B218933A6f8165e7b

    # Multiple contracts with a narrowed search window
    uv run scripts/find_deployment.py --rpc-url https://eth.drpc.org \
        --start-block 100000 \
        0x14F2982D601c9458F93bd70B218933A6f8165e7b \
        0xFf51A5898e281Db6DfC7855790607438dF2ca44b \
        0xEdd160fEBBD92E350D4D398fb636302fccd67C7e
"""

import argparse
import asyncio
import time
import warnings

import httpx

MAX_RPS = 100  # max requests per second

SINGLETON_FACTORY = "0x914d7Fec6aaC8cd542e72Bca78B30650d45643d7"

START_BLOCK = 0
END_BLOCK = "latest"

# Shared httpx client for all RPC calls. Created once inside ``main_async`` (an
# AsyncClient must be created and closed within a running event loop) and reused
# across every concurrent ``find_deployment`` task so connections are pooled
# instead of being torn down between requests.
_client: httpx.AsyncClient | None = None

# Serializes the rate-limiter check below. Without it, two coroutines could
# read ``_last_rpc_time`` simultaneously, each compute a zero wait, and both
# fire — exceeding ``MAX_RPS``.
_rate_lock = asyncio.Lock()

# Monotonic timestamp of the most recently dispatched RPC. Used to space
# requests at least ``1 / MAX_RPS`` seconds apart so we don't get throttled
# by the upstream JSON-RPC endpoint.
_last_rpc_time = 0.0


async def rpc(method: str, params: list, rpc_url: str):
    """Send a single JSON-RPC call and return the ``result`` field.

    Globally rate-limited to ``MAX_RPS`` requests per second across all
    concurrent callers. Raises ``RuntimeError`` if the response contains
    a JSON-RPC ``error``.
    """
    global _last_rpc_time
    assert _client is not None, "rpc() called before client was configured"
    async with _rate_lock:
        wait = (1.0 / MAX_RPS) - (time.monotonic() - _last_rpc_time)
        if wait > 0:
            await asyncio.sleep(wait)
        _last_rpc_time = time.monotonic()
    response = await _client.post(
        rpc_url,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        timeout=10,
    )
    result = response.json()
    if "error" in result:
        raise RuntimeError(f"RPC error: {result['error']}")
    return result["result"]


async def has_code(address: str, block: int, rpc_url: str) -> bool:
    """Return True if ``address`` has non-empty bytecode at ``block``."""
    code = await rpc("eth_getCode", [address, hex(block)], rpc_url)
    return len(code) > 2  # "0x" means no code


async def get_latest_block(rpc_url: str) -> int:
    """Return the latest block number known to the RPC endpoint."""
    return int(await rpc("eth_blockNumber", [], rpc_url), 16)


async def find_deployment_block(
    address: str,
    rpc_url: str,
    start_block: int = START_BLOCK,
    end_block: int | str = END_BLOCK,
) -> int:
    """Binary search for the first block at-or-after ``start_block`` where code exists.

    If code already exists at ``start_block``, returns ``start_block`` — the true
    deployment block may be earlier and is not searched for.
    """
    lo = start_block
    hi: int = (
        await get_latest_block(rpc_url) if end_block == "latest" else int(end_block)
    )
    while lo < hi:
        mid = (lo + hi) // 2
        if await has_code(address, mid, rpc_url):
            hi = mid
        else:
            lo = mid + 1
    return lo


async def find_possible_deployment_txs(
    address: str, block_num: int, rpc_url: str
) -> list[str]:
    """Return all tx hashes in the block that could have deployed the contract.

    Only considers transactions sent to SINGLETON_FACTORY.
    """
    block = await rpc("eth_getBlockByNumber", [hex(block_num), True], rpc_url)
    candidates = []
    for tx in block["transactions"]:
        if (tx.get("to") or "").lower() == SINGLETON_FACTORY.lower():
            candidates.append(tx["hash"])
    return candidates


async def find_deployment(
    address: str,
    rpc_url: str,
    start_block: int = START_BLOCK,
    end_block: int | str = END_BLOCK,
) -> tuple[int, list[str]]:
    """Locate the deployment block and candidate deployment tx hashes for ``address``.

    Resolves ``end_block`` (``"latest"`` or numeric), verifies the contract
    actually exists at that block (raises ``ValueError`` if not), binary-searches
    for the deployment block, and returns ``(block, [tx_hash, ...])``.
    """
    resolved_end: int = (
        await get_latest_block(rpc_url) if end_block == "latest" else int(end_block)
    )
    if not await has_code(address, resolved_end, rpc_url):
        raise ValueError(f"No code found at {address} at block {resolved_end}")
    block = await find_deployment_block(address, rpc_url, start_block, resolved_end)
    txs = await find_possible_deployment_txs(address, block, rpc_url)
    return block, txs


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments (see module docstring for the full usage)."""
    parser = argparse.ArgumentParser(
        description="Find the deployment block and transaction(s) for a contract."
    )
    parser.add_argument("--rpc-url", required=True, help="JSON-RPC endpoint URL")
    parser.add_argument(
        "--start-block",
        type=int,
        default=START_BLOCK,
        metavar="N",
        help=f"Block to start search from (default: {START_BLOCK})",
    )
    parser.add_argument(
        "--end-block",
        type=int,
        default=None,
        metavar="N",
        help="Block to end search at (default: latest)",
    )
    parser.add_argument(
        "contracts",
        nargs="+",
        metavar="ADDRESS",
        help="Contract address(es) to look up",
    )
    return parser.parse_args()


async def main_async() -> None:
    """Run ``find_deployment`` for every CLI-supplied address concurrently and print results."""
    global _client
    args = parse_args()
    end_block = args.end_block if args.end_block is not None else END_BLOCK
    print(f"RPC: {args.rpc_url}")
    print(f"Start block: {args.start_block}, End block: {end_block}\n")

    async with httpx.AsyncClient() as client:
        _client = client
        results = await asyncio.gather(
            *(
                find_deployment(address, args.rpc_url, args.start_block, end_block)
                for address in args.contracts
            ),
            return_exceptions=True,
        )

    for address, result in zip(args.contracts, results):
        print(f"Contract: {address}")
        if isinstance(result, ValueError):
            print(f"  Error: {result}")
        elif isinstance(result, BaseException):
            raise result
        else:
            block, txs = result
            if block == args.start_block and args.start_block > 0:
                # Binary search couldn't prove a deployment block: code already
                # existed at start_block, so the real deployment is somewhere in
                # [0, start_block] and reporting this block would be misleading.
                warnings.warn(
                    f"Code already present at --start-block ({args.start_block}) "
                    f"for {address}; true deployment is at or before this block "
                    f"but cannot be determined from the given range. "
                    f"Re-run with a lower --start-block to find the actual deployment."
                )
            else:
                print(f"  Deployed at block:       {block}")
                print(f"  Possible transaction(s): {txs}")
        print()


def main() -> None:
    """Synchronous entry point used by the script's ``__main__`` guard."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
