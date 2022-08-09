from gnosis.eth.utils import fast_keccak


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

    from gnosis.eth import EthereumNetwork
    from gnosis.eth.constants import NULL_ADDRESS
    from gnosis.protocol import GnosisProtocolAPI, Order, OrderKind

    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    if not PRIVATE_KEY:
        print("Set PRIVATE_KEY as an environment variable")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Place orders on Gnosis Protocol V2")
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
    gnosis_protocol_api = GnosisProtocolAPI(EthereumNetwork[args.network.upper()])
    buy_amount_response = gnosis_protocol_api.get_estimated_amount(
        from_token, to_token, OrderKind.SELL, amount_wei
    )

    buy_amount = int(buy_amount_response.get("amount", "0"))
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
        appData=fast_keccak(text="gp-cli"),
        feeAmount=0,
        kind="sell",  # `sell` or `buy`
        partiallyFillable=not args.require_full_fill,
        sellTokenBalance="erc20",  # `erc20`, `external` or `internal`
        buyTokenBalance="erc20",  # `erc20` or `internal`
    )

    order["feeAmount"] = gnosis_protocol_api.get_fee(order)

    if confirm_prompt(
        f"Exchanging {amount_wei} {from_token} to {buy_amount} {to_token}?"
    ):
        result = gnosis_protocol_api.place_order(order, PRIVATE_KEY)
        if isinstance(result, dict):
            print(f"Cannot place order {result}")
        else:
            print(f"Placed order with UUID {result}")
