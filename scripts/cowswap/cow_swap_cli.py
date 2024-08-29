from typing import Union

from eth_typing import HexStr

from safe_eth.eth.clients.cowswap import CowSwapAPI, Order, OrderKind
from safe_eth.eth.clients.cowswap.cow_swap_api import ErrorResponse


def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").lower()
    return reply == "y"


if __name__ == "__main__":
    import argparse
    import os
    import sys
    import time

    from safe_eth.eth import EthereumNetwork
    from safe_eth.eth.constants import NULL_ADDRESS

    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    if not PRIVATE_KEY:
        print("Set PRIVATE_KEY as an environment variable")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Place orders on CowSwap")
    parser.add_argument(
        "--network",
        default=EthereumNetwork.RINKEBY.name,
        help="Mainnet, Rinkeby or xDAI",
    )
    parser.add_argument("--from-token", required=True)  # TODO Check checksummed address
    parser.add_argument("--to-token", required=True)
    parser.add_argument("--amount-wei", required=True, type=int)
    parser.add_argument("--require-full-fill", action="store_true", default=False)

    args = parser.parse_args()
    from_token = args.from_token
    to_token = args.to_token
    amount_wei = args.amount_wei
    cow_swap_api = CowSwapAPI(EthereumNetwork[args.network.upper()])
    buy_amount_response = cow_swap_api.get_estimated_amount(
        from_token, to_token, OrderKind.SELL, amount_wei
    )

    buy_amount = int(str(buy_amount_response.get("amount", "0")))
    if not buy_amount:
        print("Cannot calculate amount to receive, maybe token is not supported")
        sys.exit(1)

    order = Order(
        sellToken=from_token,
        buyToken=to_token,
        receiver=NULL_ADDRESS,
        sellAmount=amount_wei,
        buyAmount=buy_amount,
        validTo=int(time.time()) + (60 * 60),  # Valid for 1 hour
        appData={"version": "1.2.2", "appCode": "CowSwap CLI", "metadata": {}},
        feeAmount=0,
        kind="sell",  # `sell` or `buy`
        partiallyFillable=not args.require_full_fill,
        sellTokenBalance="erc20",  # `erc20`, `external` or `internal`
        buyTokenBalance="erc20",  # `erc20` or `internal`
    )

    fee: Union[int, ErrorResponse] = cow_swap_api.get_fee(order, NULL_ADDRESS)
    if isinstance(fee, int):
        order.feeAmount = fee

    if confirm_prompt(
        f"Exchanging {amount_wei} {from_token} to {buy_amount} {to_token}?"
    ):
        result = cow_swap_api.place_order(order, HexStr(PRIVATE_KEY))
        if isinstance(result, dict):
            print(f"Cannot place order {result}")
        else:
            print(f"Placed order with UUID {result}")
