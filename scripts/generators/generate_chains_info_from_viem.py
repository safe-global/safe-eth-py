import re
import shutil
from glob import glob
from typing import Optional

import requests
from git import Repo

from safe_eth.eth.utils import fast_to_checksum_address

# GitHub repository config
GIT_URL = "https://github.com/wevm/viem.git"
LOCAL_REPO_DIR = "sources"

# Viem regex patterns
VIEM_ATTR_ID = "id"
VIEM_ATTR_URL = "url"
VIEM_ATTR_API_URL = "api_url"
VIEM_ATTR_MULTICALL_ADDRESS = "multicall_address"

VIEM_SEARCH_PATTERNS = {
    VIEM_ATTR_ID: re.compile(r"id\s*:\s*([\d_]+)"),
    VIEM_ATTR_URL: re.compile(r"url\s*:\s*[\'\"]([^\'\"]+)[\'\"]"),
    VIEM_ATTR_API_URL: re.compile(r"apiUrl\s*:\s*[\'\"]([^\'\"]+)[\'\"]"),
    VIEM_ATTR_MULTICALL_ADDRESS: re.compile(
        r"multicall3\s*:\s*{\s*address\s*:\s*[\'\"]([^\'\"]+)[\'\"]"
    ),
}


# Local processing regex patterns
NON_WORD_DIGIT_PATTERN = re.compile(r"[^\w\d]+")
CLOSING_PARENTHESIS_PATTERN = re.compile(r"\)")

ETHEREUM_NETWORK_CLASS_PATTERN = re.compile(
    r'class EthereumNetwork\(Enum\):(\s*\n\s*"""[^"]*"""\s*\n\s*)?(.+?)(\n\s*@.*)',
    re.MULTILINE | re.DOTALL,
)
ETHEREUM_NETWORK_CLASS_EXISTING_ENTRY_PATTERN = re.compile(r"^\s*(\w+)\s*=")

CONFIG_ENUM_ATTR_NETWORK_WITH_URL = "NETWORK_WITH_URL"
CONFIG_ENUM_ATTR_NETWORK_WITH_API_URL = "NETWORK_WITH_API_URL"
CONFIG_ENUM_ATTR_ADDRESSES = "ADDRESSES"

CONFIG_ENUM_PATTERNS = {
    CONFIG_ENUM_ATTR_NETWORK_WITH_URL: re.compile(
        r"NETWORK_WITH_URL = \{\n(.+?)(\n\s*}.*)", re.MULTILINE | re.DOTALL
    ),
    CONFIG_ENUM_ATTR_NETWORK_WITH_API_URL: re.compile(
        r"NETWORK_WITH_API_URL = \{\n(.+?)(\n\s*}.*)", re.MULTILINE | re.DOTALL
    ),
    CONFIG_ENUM_ATTR_ADDRESSES: re.compile(
        r"ADDRESSES = \{\n(.+?)(\n\s*}.*)", re.MULTILINE | re.DOTALL
    ),
}

DEFAULT_PATTERN = re.compile(r"$^")


def clean_resources() -> None:
    """Removes the intermediate resources used (source repository)"""
    try:
        shutil.rmtree(LOCAL_REPO_DIR)
    except OSError:
        pass


def convert_chain_name(name: str) -> str:
    """
    Converts a chain name into a valid constant name by replacing non-word characters
    with underscores and ensuring it does not start with a digit.

    :param name: The original chain name.
    :return: The converted chain name suitable for use as a constant.
    """
    # Change every symbol that is not a word or digit for underscore
    name_upper = CLOSING_PARENTHESIS_PATTERN.sub("", name.upper())
    name_converted = NON_WORD_DIGIT_PATTERN.sub("_", name_upper)
    # Add underscore at the beginning if start by digit
    if name_converted[0].isdigit():
        name_converted = "_" + name_converted
    return name_converted


def get_chain_enum_name(chain_id: int) -> Optional[str]:
    """
    Retrieves the chain name for a given chain ID from the Ethereum Chains GitHub repository.
    Converts the name to a constant format using `convert_chain_name`.

    :param chain_id: The ID of the chain.
    :return: The converted chain name as a string, or None if the request fails.
    """
    try:
        url = f"https://raw.githubusercontent.com/ethereum-lists/chains/master/_data/chains/eip155-{chain_id}.json"
        response = requests.get(url)
        if response.status_code == 200:
            return convert_chain_name(response.json().get("name"))
        return None
    except IOError as e:
        print(f"Error getting chain name: {e}")
        return None


def validate_api_url(api_url: str) -> bool:
    """
    Validates the API URL by making a request to the `ethsupply` endpoint
    and checking if the response status is '1'.

    :param api_url: The URL to validate.
    :return: True if the URL is valid, otherwise False.
    """
    try:
        url = f"{api_url}?module=stats&action=ethsupply"
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            tx_status = response.json().get("status", "")
            if tx_status == "1":
                return True
    except (IOError, ConnectionError) as e:
        print(f"Error validating Etherscan Client API URL: {e}")
    return False


def upsert_chain_id(chain_id: int, chain_enum_name: str) -> str:
    """
    Inserts or updates an entry in the `EthereumNetwork` enum for the given chain ID and name.
    If an entry with the same chain ID exists, it returns the existing constant name.
    Otherwise, it adds a new entry and returns the new constant name.

    :param chain_id: The ID of the chain.
    :param chain_enum_name: The name of the chain in constant format.
    :return: The name of the constant in the `EthereumNetwork` enum.
    """
    file_path = "safe_eth/eth/ethereum_network.py"
    with open(file_path, "r") as file:
        content = file.read()
    match = ETHEREUM_NETWORK_CLASS_PATTERN.search(content)
    if match:
        enum_lines = str(match.group(2).strip()).split("\n")
        existing_entry = next(
            (line for line in enum_lines if re.search(rf"\b{chain_id}\b", line)), None
        )
        if existing_entry:
            existing_entry_match = ETHEREUM_NETWORK_CLASS_EXISTING_ENTRY_PATTERN.match(
                existing_entry
            )
            if existing_entry_match:
                current_constant_name = existing_entry_match.group(1)
                print(
                    f"Entry with ID '{chain_id}' already exists with the name '{current_constant_name}'."
                )
                return current_constant_name
        else:
            new_entry = f"    {chain_enum_name} = {chain_id}"
            enum_lines.append(new_entry)
            enum_lines.sort(key=lambda x: int(x.split("=")[1].strip().replace("_", "")))
            updated_content = (
                content[: match.start()]
                + "class EthereumNetwork(Enum):"
                + match.group(1)
                + "\n".join(enum_lines)
                + match.group(3)
            )
            with open(file_path, "w") as file:
                file.write(updated_content)
            print(f"Entry '{chain_enum_name} = {chain_id}' added successfully.")
    else:
        print("Error: EthereumNetwork class definition not found in the file.")
    return chain_enum_name


def upsert_chain_info_enum_based(
    chain_enum_name: str,
    info_to_update: str,
    file_path: str,
    config_enum_name: str,
) -> None:
    """
    Updates or adds info for a given chain in the specified config enum.
    If the info already exists, it updates the entry. If not, it adds a new entry.

    :param chain_enum_name: The name of the chain constant in the enum.
    :param info_to_update: The info to add or update.
    :param file_path: The path to the file to update
    :param config_enum_name: The name of the configuration enum to update.
    :return: None
    """
    with open(file_path, "r") as file:
        content = file.read()
    match = CONFIG_ENUM_PATTERNS.get(config_enum_name, DEFAULT_PATTERN).search(content)
    if match:
        url_lines = str(match.group(1).strip()).split("\n")
        existing_entry_index = next(
            (
                i
                for i, line in enumerate(url_lines)
                if f"EthereumNetwork.{chain_enum_name}:" in line
            ),
            None,
        )
        if existing_entry_index is not None:
            url_lines[
                existing_entry_index
            ] = f'        EthereumNetwork.{chain_enum_name}: "{info_to_update}",'
            print(
                f"Updated entry {config_enum_name} EthereumNetwork.{chain_enum_name} with '{info_to_update}'."
            )
        else:
            new_entry = (
                f'        EthereumNetwork.{chain_enum_name}: "{info_to_update}",'
            )
            url_lines.append(new_entry)
            print(
                f"Added new entry {config_enum_name} EthereumNetwork.{chain_enum_name} with '{info_to_update}'."
            )
        updated_content = (
            content[: match.start()]
            + config_enum_name
            + " = {\n        "
            + "\n".join(url_lines)
            + match.group(2)
        )
        with open(file_path, "w") as file:
            file.write(updated_content)
    else:
        print(f"Error: Class definition {config_enum_name} not found in the file.")


def process_chains() -> None:
    """
    Processes the chain definitions from TypeScript files in the Viem GitHub repository.
    It clones the repository, extracts chain information, updates or adds chain IDs and etherscan client URLs,
    and writes multicall contract addresses to a JSON file.
    """
    clean_resources()
    Repo.clone_from(GIT_URL, LOCAL_REPO_DIR)

    chains_info = []

    for f_name in glob(
        LOCAL_REPO_DIR + "/src/chains/definitions/**/*.ts", recursive=True
    ):
        with open(f_name, "r") as file:
            content = file.read()
        chain_info = {}
        for key, pattern in VIEM_SEARCH_PATTERNS.items():
            match = re.search(pattern, content)
            if match:
                chain_info[key] = match.group(1)
        if chain_info:
            chains_info.append(chain_info)
    for chain_info in chains_info:
        chain_id = int(chain_info[VIEM_ATTR_ID].replace("_", ""))
        chain_name = get_chain_enum_name(chain_id)
        if chain_name:
            chain_enum_name = upsert_chain_id(chain_id, chain_name)

            if chain_info.get(VIEM_ATTR_URL) and chain_info.get(VIEM_ATTR_API_URL):
                chain_explorer_url = chain_info[VIEM_ATTR_URL]
                chain_explorer_api_url = chain_info[VIEM_ATTR_API_URL]
                is_valid_api_url = validate_api_url(chain_explorer_api_url)
                if is_valid_api_url:
                    upsert_chain_info_enum_based(
                        chain_enum_name,
                        chain_explorer_url,
                        "safe_eth/eth/clients/etherscan_client.py",
                        CONFIG_ENUM_ATTR_NETWORK_WITH_URL,
                    )
                    base_api_url = (
                        chain_explorer_api_url[: -len("/api")]
                        if chain_explorer_api_url.endswith("/api")
                        else chain_explorer_api_url
                    )
                    upsert_chain_info_enum_based(
                        chain_enum_name,
                        base_api_url,
                        "safe_eth/eth/clients/etherscan_client.py",
                        CONFIG_ENUM_ATTR_NETWORK_WITH_API_URL,
                    )

            if chain_info.get(VIEM_ATTR_MULTICALL_ADDRESS):
                upsert_chain_info_enum_based(
                    chain_enum_name,
                    fast_to_checksum_address(chain_info[VIEM_ATTR_MULTICALL_ADDRESS]),
                    "safe_eth/eth/multicall.py",
                    CONFIG_ENUM_ATTR_ADDRESSES,
                )

    clean_resources()


if __name__ == "__main__":
    process_chains()
