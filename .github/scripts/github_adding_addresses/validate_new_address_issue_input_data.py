"""
Validates the issue inputs to add new Safe contract addresses.
Composes message for a comment in the ticket with the result of the validation. If the result is negative,
composes a list of errors.
"""

import json
import os
import re
import uuid
from typing import Any, Dict, Optional

import requests
import validators

from gnosis.eth import EthereumClient
from gnosis.eth.utils import mk_contract_address_2

ERRORS = []


def convert_chain_name(name: str) -> str:
    # Change every symbol that is not a word or digit for underscore
    name_converted = re.sub(r"[^\w\d]+", r"_", name.upper().replace(")", ""))
    # Add underscore at the beggining if start by digit
    if name_converted[0].isdigit():
        name_converted = "_" + name_converted
    return name_converted


def get_chain_enum_name(chain_id: int) -> Optional[str]:
    try:
        url = f"https://raw.githubusercontent.com/ethereum-lists/chains/master/_data/chains/eip155-{chain_id}.json"
        response = requests.get(url)

        if response.status_code == 200:
            return convert_chain_name(response.json().get("name"))
        return None
    except IOError as e:
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
    except IOError as e:
        print(f"Error validating RPC url: {e}")
        return None


def get_contract_address_and_block_from_tx_hash(
    rpc_url: str, tx_hash: str
) -> Optional[Dict[str, Any]]:
    ethereum_client = EthereumClient(rpc_url)
    tx = ethereum_client.get_transaction(tx_hash)
    if not tx:
        print(f"Transaction not found: {tx_hash}")
        return None
    return {
        "block": tx.get("blockNumber"),
        "address": mk_contract_address_2(
            tx.get("to"), tx.get("input")[:32], tx.get("input")[32:]
        ),
    }


def validate_chain(chain_id_input: str) -> Optional[Dict[str, Any]]:
    if not chain_id_input.isdigit():
        ERRORS.append("Chain ID is required.")
        return None

    if not chain_id_input:
        ERRORS.append("Chain ID is required.")
        return None

    chain_id = int(chain_id_input)
    chain_name = get_chain_enum_name(chain_id)
    if not chain_name:
        ERRORS.append(f"Chain with chain ID: {chain_id} not found.")
        return None

    print(f"Chain name: {chain_name}")
    return {"chain_id": chain_id, "chain_name": chain_name}


def validate_rpc(rpc_url: str, chain_id: int) -> None:
    if not rpc_url:
        ERRORS.append("RPC URL is required.")
        return None

    if not chain_id:
        ERRORS.append("Unable to validate RPC URL without chain ID.")
        return None

    rpc_chain_id = get_chain_id_from_rpc_url(rpc_url)
    if not rpc_chain_id:
        ERRORS.append(f"Unable to validate RPC URL {rpc_url}.")
        return None

    if rpc_chain_id != int(chain_id):
        ERRORS.append(
            f"Chain ID {chain_id} provided is different than chain id obtained from RPC URL {rpc_url} {rpc_chain_id}."
        )
        return None

    print(f"Chain ID obtained from rpc url: {rpc_chain_id}")


def validate_not_required_url(field_name: str, url: str) -> None:
    if url:
        if not validators.url(url):
            ERRORS.append(f"{field_name} URL ({url}) provided is not valid.")
            return None

        print(f"Validating {field_name} URL -> {url}")
        return None

    print(f"Skipping {field_name} URL validation!")


def validate_version(version: str) -> None:
    if version not in ["1.3.0", "1.3.0+L2", "1.4.1", "1.4.1+L2"]:
        ERRORS.append(f"Version {version} is not valid.")
        return None

    print(f"Validating version: {version}!")


def validate_master_copy_address_by_version(address: str, version: str) -> None:
    valid_versions_master_copy = {
        "1.3.0": [
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
        ],
        "1.3.0+L2": [
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
        ],
        "1.4.1": ["0x41675C099F32341bf84BFc5382aF534df5C7461a"],
        "1.4.1+L2": ["0x29fcB43b46531BcA003ddC8FCB67FFE91900C762"],
    }

    if version not in valid_versions_master_copy.keys():
        ERRORS.append("Unable to validate Master copy address without valid version.")
        return None

    if address not in valid_versions_master_copy[version]:
        ERRORS.append(
            f"Master copy address {address} is not valid for version {version}"
        )
        return None

    print(f"Master copy address {address} is valid for version {version}")


def validate_proxy_address_by_version(address: str, version: str) -> None:
    valid_versions_proxy = {
        "1.3.0": [
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
        ],
        "1.3.0+L2": [
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
        ],
        "1.4.1": ["0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67"],
        "1.4.1+L2": ["0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67"],
    }

    if version not in valid_versions_proxy.keys():
        ERRORS.append("Unable to validate Proxy address without valid version.")
        return None

    if address not in valid_versions_proxy[version]:
        ERRORS.append(f"Proxy address {address} is not valid for version {version}")
        return None

    print(f"Proxy address {address} is valid for version {version}")


def validate_address_and_transactions(
    type: str, address: str, tx_hash: str, rpc_url: str
) -> Optional[Dict[str, Any]]:
    if not address and not tx_hash:
        print("Skipping address and tx validation. Not data provided!")
        return None

    if not address:
        ERRORS.append(f"{type} address is required.")
        return None

    if not tx_hash:
        ERRORS.append(f"{type} tx_hash is required.")
        return None

    if not rpc_url:
        ERRORS.append(f"Unable to validate {type} address and tx without RPC URL.")
        return None

    tx_info = get_contract_address_and_block_from_tx_hash(rpc_url, tx_hash)
    if not tx_info:
        ERRORS.append(f"Unable to obtain {type} Tx info {tx_hash}")
        return None

    if tx_info["address"] != address:
        ERRORS.append(
            f"{type} address obtained from Tx is diferent than provided {tx_info['address']}"
        )
        return None

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
    chain_id_input = issue_body_info.get("chainId")
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
    print(f"Chain ID: {chain_id_input}")
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
    chain_info = validate_chain(chain_id_input)
    chain_id = chain_info.get("chain_id") if chain_info else None
    chain_name = chain_info.get("chain_name") if chain_info else None
    validate_rpc(rpc_url, chain_id)
    validate_not_required_url("BlockscoutClientUrl", blockscout_client_url)
    validate_not_required_url("EtherscanClientUrl", etherscan_client_url)
    validate_not_required_url("EtherscanClientApiUrl", etherscan_client_api_url)
    validate_version(version)
    validate_master_copy_address_by_version(address_master_copy, version)
    validate_proxy_address_by_version(address_proxy, version)
    tx_master_info = validate_address_and_transactions(
        "Master copy", address_master_copy, tx_hash_master_copy, rpc_url
    )
    tx_proxy_info = validate_address_and_transactions(
        "Proxy factory", address_proxy, tx_hash_proxy, rpc_url
    )

    if len(ERRORS) > 0:
        errors_comment = "\n- ".join(ERRORS)
        add_message_to_env(
            "Validation has failed with the following errors:"
            + f"\n- {errors_comment}"
            + "\n\n Validation failed!❌"
        )
        return None
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
