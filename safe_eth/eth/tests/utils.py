import functools
import json
import os
from copy import deepcopy
from typing import Any

import pytest
import requests
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract
from web3.types import TxParams

from ...util.util import to_0x_hex_str
from ..contracts import get_example_erc20_contract


def just_test_if_node_available(node_url_variable_name: str) -> str:
    """
    Just run the test if ``node url`` is defined on the ``node_url_variable_name`` environment variable
    and it's accessible. Node JSON RPC url will only be tested the first call to this function.

    :param node_url_variable_name: Environment variable name for ``node url``
    :return: ``node url``
    """
    node_url = getattr(just_test_if_node_available, node_url_variable_name, None)
    if node_url:  # Just check node first time
        return node_url

    node_url = os.environ.get(node_url_variable_name)
    if not node_url:
        pytest.skip(
            f"{node_url_variable_name} not defined, skipping test",
            allow_module_level=True,
        )
    else:
        try:
            response = requests.post(
                node_url,
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
                    f"Problem connecting to node {node_url}: {response.status_code} - {response.content!r}"
                )
        except IOError:
            pytest.fail(f"Problem connecting to {node_url}")
    setattr(just_test_if_node_available, node_url_variable_name, node_url)
    return node_url


def just_test_if_mainnet_node() -> str:
    return just_test_if_node_available("ETHEREUM_MAINNET_NODE")


def just_test_if_polygon_node() -> str:
    return just_test_if_node_available("ETHEREUM_POLYGON_NODE")


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
    signed_tx = account.sign_transaction(tx)  # type: ignore
    tx_hash = w3.eth.send_raw_transaction(bytes(signed_tx.raw_transaction))
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    assert tx_receipt["status"] == 1, "Error with tx %s - %s" % (
        to_0x_hex_str(tx_hash),
        tx,
    )
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
    ).build_transaction()
    tx["nonce"] = w3.eth.get_transaction_count(
        account.address, block_identifier="pending"
    )
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

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
        return to_0x_hex_str(o)
    if isinstance(o, dict):
        o = dict(o)  # Remove AttributeDict
        for k in o.keys():
            o[k] = bytes_to_str(o[k])
    elif isinstance(o, list):
        o = deepcopy(o)
        for i, v in enumerate(o):
            o[i] = bytes_to_str(o[i])
    elif isinstance(o, tuple):
        o = tuple(bytes_to_str(v) for v in o)
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
