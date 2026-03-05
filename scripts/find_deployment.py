"""Find the deployment block and transaction hash for Safe contracts.

Uses binary search on eth_getCode to locate the first block where contract
bytecode is present, then scans that block for transactions sent to the Safe
singleton factory (SINGLETON_FACTORY) as deployment candidates.

Usage
-----
    python find_deployment.py --rpc-url <RPC_URL> [--start-block N] [--end-block N] <ADDRESS> [ADDRESS ...]

Arguments
---------
    --rpc-url       (required) JSON-RPC HTTP endpoint, e.g. https://rpc.moderato.tempo.xyz
    --start-block   (optional) Lower bound for binary search. Defaults to 0.
    --end-block     (optional) Upper bound for binary search. Defaults to the latest block.
    ADDRESS         One or more contract addresses to look up.

Examples
--------
    # Single contract
    python scripts/find_deployment.py --rpc-url https://rpc.moderato.tempo.xyz \
        0x14F2982D601c9458F93bd70B218933A6f8165e7b

    # Multiple contracts with a narrowed search window
    python scripts/find_deployment.py --rpc-url https://rpc.moderato.tempo.xyz \
        --start-block 100000 \
        0x14F2982D601c9458F93bd70B218933A6f8165e7b \
        0xFf51A5898e281Db6DfC7855790607438dF2ca44b \
        0xEdd160fEBBD92E350D4D398fb636302fccd67C7e
"""

import argparse
import time

import requests

MAX_RPS = 100  # max requests per second

SINGLETON_FACTORY = "0x914d7Fec6aaC8cd542e72Bca78B30650d45643d7"

START_BLOCK = 0
END_BLOCK = "latest"

_last_rpc_time = 0.0


def rpc(method: str, params: list, rpc_url: str):
    global _last_rpc_time
    wait = (1.0 / MAX_RPS) - (time.monotonic() - _last_rpc_time)
    if wait > 0:
        time.sleep(wait)
    response = requests.post(
        rpc_url,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        timeout=10,
    )
    _last_rpc_time = time.monotonic()
    result = response.json()
    if "error" in result:
        raise RuntimeError(f"RPC error: {result['error']}")
    return result["result"]


def has_code(address: str, block: int, rpc_url: str) -> bool:
    code = rpc("eth_getCode", [address, hex(block)], rpc_url)
    return len(code) > 2  # "0x" means no code


def get_latest_block(rpc_url: str) -> int:
    return int(rpc("eth_blockNumber", [], rpc_url), 16)


def find_deployment_block(
    address: str,
    rpc_url: str,
    start_block: int = START_BLOCK,
    end_block: int | str = END_BLOCK,
) -> int:
    """Binary search for the first block where the contract code exists."""
    lo = start_block
    hi: int = get_latest_block(rpc_url) if end_block == "latest" else int(end_block)
    while lo < hi:
        mid = (lo + hi) // 2
        if has_code(address, mid, rpc_url):
            hi = mid
        else:
            lo = mid + 1
    return lo


def find_possible_deployment_txs(
    address: str, block_num: int, rpc_url: str
) -> list[str]:
    """Return all tx hashes in the block that could have deployed the contract.

    Only considers transactions sent to SINGLETON_FACTORY.
    """
    block = rpc("eth_getBlockByNumber", [hex(block_num), True], rpc_url)
    candidates = []
    for tx in block["transactions"]:
        if (tx.get("to") or "").lower() == SINGLETON_FACTORY.lower():
            candidates.append(tx["hash"])
    return candidates


def find_deployment(
    address: str,
    rpc_url: str,
    start_block: int = START_BLOCK,
    end_block: int | str = END_BLOCK,
) -> tuple[int, list[str]]:
    resolved_end: int = (
        get_latest_block(rpc_url) if end_block == "latest" else int(end_block)
    )
    if not has_code(address, resolved_end, rpc_url):
        raise ValueError(f"No code found at {address} at block {resolved_end}")
    block = find_deployment_block(address, rpc_url, start_block, resolved_end)
    txs = find_possible_deployment_txs(address, block, rpc_url)
    return block, txs


def parse_args() -> argparse.Namespace:
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


def main():
    args = parse_args()
    end_block = args.end_block if args.end_block is not None else END_BLOCK
    print(f"RPC: {args.rpc_url}")
    print(f"Start block: {args.start_block}, End block: {end_block}\n")

    for address in args.contracts:
        print(f"Contract: {address}")
        try:
            block, txs = find_deployment(
                address, args.rpc_url, args.start_block, end_block
            )
            print(f"  Deployed at block:       {block}")
            print(f"  Possible transaction(s): {txs}")
        except ValueError as e:
            print(f"  Error: {e}")
        print()


if __name__ == "__main__":
    main()
