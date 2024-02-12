import functools
import json
import os
from copy import deepcopy
from typing import Any

import pytest
import requests
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract
from web3.types import TxParams

from ..contracts import get_example_erc20_contract


def just_test_if_mainnet_node() -> str:
    mainnet_node_url = os.environ.get("ETHEREUM_MAINNET_NODE")
    if hasattr(just_test_if_mainnet_node, "checked"):  # Just check node first time
        return mainnet_node_url

    if not mainnet_node_url:
        pytest.skip("Mainnet node not defined, skipping test", allow_module_level=True)
    else:
        try:
            response = requests.post(
                mainnet_node_url,
                timeout=5,
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_blockNumber",
                    "params": [],
                    "id": 1,
                },
            )
            if not response.ok:
                pytest.fail(
                    f"Problem connecting to mainnet node {response.status_code} - {response.content}"
                )
        except IOError:
            pytest.fail("Problem connecting to the mainnet node")
    just_test_if_mainnet_node.checked = True
    return mainnet_node_url


def just_test_if_polygon_node() -> str:
    polygon_node_url = os.environ.get("ETHEREUM_POLYGON_NODE")
    if hasattr(just_test_if_polygon_node, "checked"):  # Just check node first time
        return polygon_node_url

    if not polygon_node_url:
        pytest.skip(
            "Polygon node not defined, cannot test oracles", allow_module_level=True
        )
    else:
        try:
            if not requests.post(
                polygon_node_url,
                timeout=5,
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_blockNumber",
                    "params": [],
                    "id": 1,
                },
            ).ok:
                pytest.skip("Cannot connect to polygon node", allow_module_level=True)
        except IOError:
            pytest.skip(
                "Problem connecting to the polygon node", allow_module_level=True
            )
    just_test_if_polygon_node.checked = True
    return polygon_node_url


def skip_on(exception, reason="Test skipped due to a controlled exception"):
    """
    Decorator to skip a test if an exception is raised instead of failing it

    :param exception:
    :param reason:
    :return:
    """

    def decorator_func(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Run the test
                return f(*args, **kwargs)
            except exception:
                pytest.skip(reason)

        return wrapper

    return decorator_func


# TODO Move this to EthereumClient
def send_tx(w3: Web3, tx: TxParams, account: LocalAccount) -> bytes:
    tx["from"] = account.address
    if "nonce" not in tx:
        tx["nonce"] = w3.eth.get_transaction_count(
            account.address, block_identifier="pending"
        )

    if "gasPrice" not in tx and "maxFeePerGas" not in tx:
        tx["gasPrice"] = w3.eth.gas_price

    if "gas" not in tx:
        tx["gas"] = w3.eth.estimate_gas(tx)

    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(bytes(signed_tx.rawTransaction))
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    assert tx_receipt["status"] == 1, "Error with tx %s - %s" % (tx_hash.hex(), tx)
    return tx_hash


def deploy_erc20(
    w3: Web3,
    account: LocalAccount,
    name: str,
    symbol: str,
    owner: ChecksumAddress,
    amount: int,
    decimals: int = 18,
) -> Contract:
    erc20_contract = get_example_erc20_contract(w3)
    tx = erc20_contract.constructor(
        name, symbol, decimals, owner, amount
    ).build_transaction(
        {
            "nonce": w3.eth.get_transaction_count(
                account.address, block_identifier="pending"
            )
        }
    )
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    erc20_address = tx_receipt["contractAddress"]
    deployed_erc20 = get_example_erc20_contract(w3, erc20_address)
    assert deployed_erc20.functions.balanceOf(owner).call() == amount
    return deployed_erc20


def bytes_to_str(o: Any) -> Any:
    """
    Converts bytes (and hexbytes) fields to `str` in nested data types

    :param o:
    :return:
    """
    if isinstance(o, bytes):
        return HexBytes(o).hex()
    if isinstance(o, dict):
        o = dict(o)  # Remove AttributeDict
        for k in o.keys():
            o[k] = bytes_to_str(o[k])
    elif isinstance(o, (list, tuple)):
        o = deepcopy(o)
        for i, v in enumerate(o):
            o[i] = bytes_to_str(o[i])
    elif isinstance(o, set):
        o = {bytes_to_str(element) for element in o}
    return o


def to_json_with_hexbytes(o: Any) -> str:
    """
    Convert RPC calls with nested bytes/Hexbytes to json and compare. Useful for RPC calls

    :param o:
    :return: Object as JSON with Hexbytes/bytes parsed correctly as a hex string
    """
    return json.dumps(bytes_to_str(o), indent=4, sort_keys=True)
