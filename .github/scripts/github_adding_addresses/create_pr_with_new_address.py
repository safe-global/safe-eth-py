"""
Creates a PR with the necessary changes to add the new addresses.
Verify and apply the necessary changes.
"""

import json
import os
import re
from typing import Optional

import requests
from github import Github
from github.GithubException import GithubException
from github.Repository import Repository

from gnosis.eth import EthereumClient


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


def get_contract_block_from_tx_hash(rpc_url: str, tx_hash: str) -> Optional[int]:
    ethereum_client = EthereumClient(rpc_url)
    tx = ethereum_client.get_transaction(tx_hash)
    if not tx:
        print(f"Transaction not found: {tx_hash}")
        return None
    return tx.get("blockNumber")


def get_github_repository(github_token: str, repository_name: str) -> Repository:
    print(f"Getting repository {repository_name}")
    github = Github(github_token)
    return github.get_repo(repository_name)


def create_issue_branch(repo: Repository, chain_id: int, version: str) -> str:
    branch_name = f"add-new-chain-{chain_id}-{version}-addresses"
    print(f"Creating branch {branch_name}")
    try:
        repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=repo.get_branch("main").commit.sha
        )
    except GithubException as e:
        print(f"Unable to create pull request: {e}")
    return branch_name


def create_pr(
    repo: Repository,
    branch_name: str,
    chain_enum_name: str,
    version: str,
    issue_number: int,
) -> None:
    try:
        created_pull_request = repo.create_pull(
            title=f"Add addresses {version} for chain {chain_enum_name}",
            body=f"Automatic PR to add new address {version} to {chain_enum_name} chain\n Closes #{issue_number}",
            head=branch_name,
            base="main",
        )
        created_pull_request.add_to_labels("add-new-address")
    except GithubException as e:
        print(f"Unable to create pull request: {e}")


def upsert_chain_id(
    repo: Repository, branch_name: str, chain_id: int, chain_enum_name: str
) -> None:
    file_path = "gnosis/eth/ethereum_network.py"
    file = repo.get_contents(file_path, ref=branch_name)
    content = file.decoded_content.decode("utf-8")

    match = re.search(
        r'class EthereumNetwork\(Enum\):(\s*\n\s*"""[^"]*"""\s*\n\s*)?(.+?)(\n\s*@.*)',
        content,
        re.MULTILINE | re.DOTALL,
    )

    if match:
        enum_lines = str(match.group(2).strip()).split("\n")

        existing_entry = next(
            (line for line in enum_lines if re.search(rf"\b{chain_id}\b", line)), None
        )

        if existing_entry:
            print(f"Entry with ID '{chain_id}' already exists.")
        else:
            new_entry = f"    {chain_enum_name} = {chain_id}"
            enum_lines.append(new_entry)
            enum_lines.sort(key=lambda x: int(x.split("=")[1].strip()))

            updated_content = (
                content[: match.start()]
                + "class EthereumNetwork(Enum):"
                + match.group(1)
                + "\n".join(enum_lines)
                + match.group(3)
            )

            repo.update_file(
                file_path,
                f"Add new chain {chain_id}",
                updated_content,
                file.sha,
                branch_name,
            )

            print(f"Entry '{chain_enum_name} = {chain_id}' added successfully.")
    else:
        print("Error: EthereumNetwork class definition not found in the file.")


def upsert_explorer_client_url(
    repo: Repository,
    branch_name: str,
    chain_enum_name: str,
    client_url: str,
    file_path: str,
    config_enum_name: str,
) -> None:
    file = repo.get_contents(file_path, ref=branch_name)
    content = file.decoded_content.decode("utf-8")

    match = re.search(
        config_enum_name + r" = \{\n(.+?)(\n\s*}.*)", content, re.MULTILINE | re.DOTALL
    )

    if match:
        url_lines = str(match.group(1).strip()).split("\n")

        existing_entry = next(
            (
                line
                for line in url_lines
                if re.search(f'EthereumNetwork.{chain_enum_name}: "{client_url}"', line)
            ),
            None,
        )

        if existing_entry:
            print(f"Entry with URL '{client_url}' already exists.")
        else:
            new_entry = f'        EthereumNetwork.{chain_enum_name}: "{client_url}",'
            url_lines.append(new_entry)

            updated_content = (
                content[: match.start()]
                + config_enum_name
                + " = {\n        "
                + "\n".join(url_lines)
                + match.group(2)
            )

            repo.update_file(
                file_path,
                f"Add new explorer client URL: {client_url}",
                updated_content,
                file.sha,
                branch_name,
            )

            print(
                f'Entry EthereumNetwork.{chain_enum_name}: "{client_url}" added successfully.'
            )
    else:
        print("Error: Class definition not found in the file.")


def upsert_contract_address_master_copy(
    repo: Repository,
    branch_name: str,
    chain_enum_name: str,
    address: str,
    block_number: int,
    version: str,
) -> None:
    file_path = "gnosis/safe/addresses.py"
    file = repo.get_contents(file_path, ref=branch_name)
    content = file.decoded_content.decode("utf-8")

    print(
        f"Updating Master Copy address chain {chain_enum_name} address '{address}' and block_number {block_number}"
    )

    match_network = re.search(
        r"(MASTER_COPIES: Dict\[EthereumNetwork, List\[Tuple\[str, int, str]]] = \{.+EthereumNetwork\."
        + re.escape(chain_enum_name)
        + r": \[)(.+?)(].+PROXY_FACTORIES.+)",
        content,
        re.MULTILINE | re.DOTALL,
    )

    if match_network:
        match_contract = re.search(
            r"(\(\n?\s*\""
            + re.escape(address)
            + r"\",\n?\s*"
            + re.escape(str(block_number))
            + r",\n?\s*\""
            + re.escape(version)
            + r"\",?\n?\s*\))",
            match_network.group(2),
            re.MULTILINE | re.DOTALL,
        )

        if match_contract:
            print(
                f"Entry in chain {chain_enum_name} with address '{address}' and block_number {block_number}"
                + f" and version {version} already exists."
            )
        else:
            new_entry = (
                f'    ("{address}", {block_number}, "{version}"),  # v{version}\n    '
            )
            updated_content = (
                content[: match_network.start()]
                + match_network.group(1)
                + match_network.group(2)
                + new_entry
                + match_network.group(3)
            )
            repo.update_file(
                file_path,
                f"Add new master copy address {address}",
                updated_content,
                file.sha,
                branch_name,
            )
    else:
        match = re.search(
            r"(MASTER_COPIES: Dict\[EthereumNetwork, List\[Tuple\[str, int, str]]] = \{)(.+?)(}.+PROXY_FACTORIES.+)",
            content,
            re.MULTILINE | re.DOTALL,
        )

        if match:
            new_entry = (
                f'    EthereumNetwork.{chain_enum_name}: [\n        ("{address}", {block_number}, '
                + f'"{version}"),  # v{version}\n    ],\n'
            )
            updated_content = (
                content[: match.start()]
                + match.group(1)
                + match.group(2)
                + new_entry
                + match.group(3)
            )
            repo.update_file(
                file_path,
                f"Add new master copy address {address}",
                updated_content,
                file.sha,
                branch_name,
            )
        else:
            print("Error: MASTER_COPIES definition not found in the file.")


def upsert_contract_address_proxy_factory(
    repo: Repository,
    branch_name: str,
    chain_enum_name: str,
    address: str,
    block_number: int,
    version: str,
) -> None:
    file_path = "gnosis/safe/addresses.py"
    file = repo.get_contents(file_path, ref=branch_name)
    content = file.decoded_content.decode("utf-8")
    version = version.replace("+L2", "")
    print(
        f"Updating Proxy Factory address chain {chain_enum_name} address '{address}' and block_number {block_number}"
    )

    match_network = re.search(
        r"(PROXY_FACTORIES: Dict\[EthereumNetwork, List\[Tuple\[str, int]]] = \{.+EthereumNetwork\."
        + re.escape(chain_enum_name)
        + r": \[)(.+?)(].+)",
        content,
        re.MULTILINE | re.DOTALL,
    )

    if match_network:
        match_contract = re.search(
            r"(\(\n?\s*\""
            + re.escape(address)
            + r"\",\n?\s*"
            + re.escape(str(block_number))
            + r",?\n?\s*\))",
            match_network.group(2),
            re.MULTILINE | re.DOTALL,
        )

        if match_contract:
            print(
                f"Entry in chain {chain_enum_name} with address '{address}' and block_number {block_number}"
                + " already exists."
            )
        else:
            new_entry = f'    ("{address}", {block_number}), # v{version}\n    '
            updated_content = (
                content[: match_network.start()]
                + match_network.group(1)
                + match_network.group(2)
                + new_entry
                + match_network.group(3)
            )
            repo.update_file(
                file_path,
                f"Add new proxy address {address}",
                updated_content,
                file.sha,
                branch_name,
            )
    else:
        match = re.search(
            r"(PROXY_FACTORIES: Dict\[EthereumNetwork, List\[Tuple\[str, int]]] = \{)(.+?)(}.+)",
            content,
            re.MULTILINE | re.DOTALL,
        )

        if match:
            new_entry = (
                f'    EthereumNetwork.{chain_enum_name}: [\n        ("{address}", {block_number}'
                + f"),  # v{version}\n    ],\n"
            )
            updated_content = (
                content[: match.start()]
                + match.group(1)
                + match.group(2)
                + new_entry
                + match.group(3)
            )
            repo.update_file(
                file_path,
                f"Add new proxy address {address}",
                updated_content,
                file.sha,
                branch_name,
            )
        else:
            print("Error: PROXY_FACTORIES definition not found in the file.")


def execute_issue_changes() -> None:
    github_token = os.environ.get("GITHUB_TOKEN")
    repository_name = os.environ.get("GITHUB_REPOSITORY_NAME")
    issue_number = int(os.environ.get("ISSUE_NUMBER"))
    issue_body_info = json.loads(os.environ.get("ISSUE_BODY_INFO"))
    chain_id = int(issue_body_info.get("chainId"))
    version = issue_body_info.get("version")
    blockscout_client_url = issue_body_info.get("blockscoutClientUrl")
    etherscan_client_url = issue_body_info.get("etherscanClientUrl")
    etherscan_client_api_url = issue_body_info.get("etherscanClientApiUrl")
    rpc_url = issue_body_info.get("rpcUrl")
    address_master_copy = issue_body_info.get("addressMasterCopy")
    tx_hash_master_copy = issue_body_info.get("txHashMasterCopy")
    address_master_copy_l2 = issue_body_info.get("addressMasterCopyL2")
    tx_hash_master_copy_l2 = issue_body_info.get("txHashMasterCopyL2")
    address_proxy = issue_body_info.get("addressProxy")
    tx_hash_proxy = issue_body_info.get("txHashProxy")

    repo = get_github_repository(github_token, repository_name)

    chain_enum_name = get_chain_enum_name(chain_id)
    if not chain_enum_name:
        return None

    branch_name = create_issue_branch(repo, chain_id, version)

    upsert_chain_id(repo, branch_name, chain_id, chain_enum_name)

    if blockscout_client_url:
        print("Updating Blockscout client")
        file_path = "gnosis/eth/clients/blockscout_client.py"
        upsert_explorer_client_url(
            repo,
            branch_name,
            chain_enum_name,
            blockscout_client_url,
            file_path,
            "NETWORK_WITH_URL",
        )

    if etherscan_client_url:
        print("Updating Etherscan client")
        file_path = "gnosis/eth/clients/etherscan_client.py"
        upsert_explorer_client_url(
            repo,
            branch_name,
            chain_enum_name,
            etherscan_client_url,
            file_path,
            "NETWORK_WITH_URL",
        )
    if etherscan_client_api_url:
        print("Updating Etherscan API client")
        file_path = "gnosis/eth/clients/etherscan_client.py"
        upsert_explorer_client_url(
            repo,
            branch_name,
            chain_enum_name,
            etherscan_client_api_url,
            file_path,
            "NETWORK_WITH_API_URL",
        )

    if rpc_url and address_master_copy and tx_hash_master_copy:
        tx_block = get_contract_block_from_tx_hash(rpc_url, tx_hash_master_copy)
        if tx_block:
            upsert_contract_address_master_copy(
                repo,
                branch_name,
                chain_enum_name,
                address_master_copy,
                tx_block,
                version,
            )

    if rpc_url and address_master_copy_l2 and tx_hash_master_copy_l2:
        tx_block = get_contract_block_from_tx_hash(rpc_url, tx_hash_master_copy_l2)
        if tx_block:
            upsert_contract_address_master_copy(
                repo,
                branch_name,
                chain_enum_name,
                address_master_copy_l2,
                tx_block,
                version + "+L2",
            )

    if rpc_url and address_proxy and tx_hash_proxy:
        tx_block = get_contract_block_from_tx_hash(rpc_url, tx_hash_proxy)
        if tx_block:
            upsert_contract_address_proxy_factory(
                repo, branch_name, chain_enum_name, address_proxy, tx_block, version
            )

    create_pr(repo, branch_name, chain_enum_name, version, issue_number)


if __name__ == "__main__":
    execute_issue_changes()
