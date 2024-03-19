import json
import os
import uuid
from typing import Any, Dict, Optional

import requests
import validators
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth.utils import mk_contract_address_2

ERRORS = []


def get_chain_name(chain_id: str) -> Optional[str]:
    try:
        url = f"https://raw.githubusercontent.com/ethereum-lists/chains/master/_data/chains/eip155-{chain_id}.json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get("name")
        return None
    except Exception as e:
        print(f"Error getting chain name: {e}")
        return None


def get_chain_id_from_rpc_url(rpc_url: str) -> Optional[int]:
    try:
        response = requests.post(
            rpc_url,
            json={"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1},
        )

        if response.status_code == 200:
            return int(response.json().get("result"), 16)
        return None
    except Exception as e:
        print(f"Error validating RPC url: {e}")
        return None


def get_contract_address_and_block_from_tx_hash(
    rpc_url: str, tx_hash: str
) -> Optional[Dict[str, Any]]:
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        tx = w3.eth.get_transaction(HexBytes(tx_hash))
        return {
            "block": tx.blockNumber,
            "address": mk_contract_address_2(tx.to, tx.input[:32], tx.input[32:]),
        }
    except Exception as e:
        print(f"Error getting transaction: {e}")
        return None


def validate_chain(chain_id: str) -> Optional[str]:
    if not chain_id:
        ERRORS.append("Chain ID is required.")
        return

    chain_name = get_chain_name(chain_id)
    if not chain_name:
        ERRORS.append(f"Chain with chain ID: {chain_id} not found.")
        return

    print(f"Chain name: {chain_name}")
    return chain_name


def validate_rpc(rpc_url: str, chain_id: str) -> None:
    if not rpc_url:
        ERRORS.append("RPC URL is required.")
        return

    if not chain_id:
        ERRORS.append("Unable to validate RPC URL without chain ID.")
        return

    rpc_chain_id = get_chain_id_from_rpc_url(rpc_url)
    if not rpc_chain_id:
        ERRORS.append(f"Unable to validate RPC URL {rpc_url}.")
        return

    if rpc_chain_id != int(chain_id):
        ERRORS.append(
            f"Chain ID {chain_id} provided is different than chain id obtained from RPC URL {rpc_url} {rpc_chain_id}."
        )
        return

    print(f"Chain ID obtained from rpc url: {rpc_chain_id}")


def validate_not_required_url(field_name: str, url: str) -> None:
    if url:
        if not validators.url(url):
            ERRORS.append(f"{field_name} URL ({url}) provided is not valid.")
            return

        print(f"Validating {field_name} URL -> {url}")

    print(f"Skipping {field_name} URL validation!")


def validate_version(version: str) -> None:
    if version not in ["1.3.0", "1.3.0 L2", "1.4.1", "1.4.1 L2"]:
        ERRORS.append(f"Version {version} is not valid.")
        return

    print(f"Validating version: {version}!")


def validate_address_and_transactions(
    type: str, address: str, tx_hash: str, rpc_url: str
) -> Optional[Dict[str, Any]]:
    if not address and not tx_hash:
        print("Skipping address and tx validation. Not data provided!")
        return

    if not address:
        ERRORS.append(f"{type} address is required.")
        return

    if not tx_hash:
        ERRORS.append(f"{type} tx_hash is required.")
        return

    if not rpc_url:
        ERRORS.append(f"Unable to validate {type} address and tx without RPC URL.")
        return

    tx_info = get_contract_address_and_block_from_tx_hash(rpc_url, tx_hash)
    if not tx_info:
        ERRORS.append(f"Unable to obtain {type} Tx info {tx_hash}")
        return

    if tx_info["address"] != address:
        ERRORS.append(
            f"{type} address obtained from Tx is diferent than provided {tx_info['address']}"
        )
        return

    print(f"{type} Tx. info: {tx_info}")
    return tx_info


def add_message_to_env(message: str) -> None:
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        delimiter = uuid.uuid1()
        print(f"comment_message<<{delimiter}", file=fh)
        print(message, file=fh)
        print(delimiter, file=fh)


def validate_issue_inputs() -> None:
    issue_body_info = json.loads(os.environ.get("ISSUE_BODY_INFO"))
    chain_id = issue_body_info.get("chainId")
    rpc_url = issue_body_info.get("rpcUrl")
    blockscout_client_url = issue_body_info.get("blockscoutClientUrl")
    etherscan_client_url = issue_body_info.get("etherscanClientUrl")
    etherscan_client_api_url = issue_body_info.get("etherscanClientApiUrl")
    version = issue_body_info.get("version")
    address_master_copy = issue_body_info.get("addressMasterCopy")
    tx_hash_master_copy = issue_body_info.get("txHashMasterCopy")
    address_proxy = issue_body_info.get("addressProxy")
    tx_hash_proxy = issue_body_info.get("txHashProxy")

    print("Inputs to validate:")
    print(f"Chain ID: {chain_id}")
    print(f"RPC URL: {rpc_url}")
    print(f"Blockscout Client URL: {blockscout_client_url}")
    print(f"Etherscan Client URL: {etherscan_client_url}")
    print(f"Etherscan Client API URL: {etherscan_client_api_url}")
    print(f"Version: {version}")
    print(f"Address (Master copy): {address_master_copy}")
    print(f"Deployment Tx hash (Master copy): {tx_hash_master_copy}")
    print(f"Address (Proxy factory): {address_proxy}")
    print(f"Deployment Tx hash (Proxy factory): {tx_hash_proxy}")

    print("Start validation:")
    chain_name = validate_chain(chain_id)
    validate_rpc(rpc_url, chain_id)
    validate_not_required_url("BlockscoutClientUrl", blockscout_client_url)
    validate_not_required_url("EtherscanClientUrl", etherscan_client_url)
    validate_not_required_url("EtherscanClientApiUrl", etherscan_client_api_url)
    validate_version(version)
    tx_master_info = validate_address_and_transactions(
        "Master copy", address_master_copy, tx_hash_master_copy, rpc_url
    )
    tx_proxy_info = validate_address_and_transactions(
        "Proxy factory", address_proxy, tx_hash_proxy, rpc_url
    )

    if len(ERRORS) > 0:
        errors_comment = "\n".join(ERRORS)
        add_message_to_env(
            "Validation has failed with the following errors:"
            + f"\n- {errors_comment}"
            + "\n\n Validation failed!❌"
        )
        return
    chain_name_comment = chain_name if chain_name else "N/A"
    tx_master_block_comment = tx_master_info.get("block") if tx_master_info else "N/A"
    tx_proxy_block_comment = tx_proxy_info.get("block") if tx_proxy_info else "N/A"
    add_message_to_env(
        "All elements have been validated and are correct:"
        + f"\n- Chain ID: {chain_id}"
        + f"\n- Chain Name: {chain_name_comment}"
        + f"\n- RPC URL: {rpc_url}"
        + f"\n- Blockscout Client URL: {blockscout_client_url}"
        + f"\n- Etherscan Client URL: {etherscan_client_url}"
        + f"\n- Etherscan Client API URL: {etherscan_client_api_url}"
        + f"\n- Version: {version}"
        + f"\n- Address Master Copy: {address_master_copy}"
        + f"\n- Tx Hash Master Copy: {tx_hash_master_copy}"
        + f"\n- Tx Block Master Copy: {tx_master_block_comment}"
        + f"\n- Address Proxy: {address_proxy}"
        + f"\n- Tx Hash Proxy: {tx_hash_proxy}"
        + f"\n- Tx Block Proxy: {tx_proxy_block_comment}"
        + "\n\n Validation successful!✅"
    )


if __name__ == "__main__":
    validate_issue_inputs()
