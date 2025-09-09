import json
import logging
import os
import shutil
from contextlib import contextmanager
from typing import Dict, List

from git import Repo

logging.basicConfig(level=logging.INFO)

SAFE_DEPLOYMENTS_URL = "https://github.com/safe-global/safe-deployments.git"
# TODO: Use main branch
SAFE_DEPLOYMENTS_VERSION = "feature/add-network-1337"  # safe-deployments tag/branch
SAFE_DEPLOYMENTS_REPO_DIR = "safe-deployments"  # temporary folder to clone the repo
SAFE_DEPLOYMENTS_FOLDER = (
    SAFE_DEPLOYMENTS_REPO_DIR + "/src/assets"
)  # folder where the deployments are
CURRENT_DIRECTORY = os.path.dirname(__file__)
SAFE_ETH_PY_DEPLOYMENTS_FILE = os.path.join(
    CURRENT_DIRECTORY, "../../safe_eth/safe/safe_deployments.py"
)  # deployment dictionary to be stored


def clean_resources():
    """Removes the intermediate resources used (source repository)"""
    try:
        shutil.rmtree(SAFE_DEPLOYMENTS_REPO_DIR)
    except OSError:
        pass


@contextmanager
def get_safe_deployments(*args, **kwds):
    # Code to acquire resource, e.g.:
    repo = Repo.clone_from(SAFE_DEPLOYMENTS_URL, SAFE_DEPLOYMENTS_REPO_DIR)
    try:
        yield repo
    finally:
        # Code to release resource, e.g.:
        clean_resources()


def get_network_addresses_by_chain(safe_deployment: Dict) -> Dict[str, List[str]]:
    """
    Generates a dictionary mapping chains to their respective addresses.
    Translates address types to actual addresses from the safe_deployment dictionary.

    :param safe_deployment:
    :return: a dictionary of chains with lists of corresponding addresses.
    """
    network_addresses_by_chain = {}

    # Applying list because networkAddresses is not list for all networks
    for chain_id, address_types in safe_deployment["networkAddresses"].items():
        addresses: List[str] = []
        if not isinstance(address_types, list):
            address_types = [address_types]
        for address_type in address_types:
            address = safe_deployment["deployments"][address_type]["address"]
            addresses.append(address)

        network_addresses_by_chain[chain_id] = addresses

    return network_addresses_by_chain


def get_default_network_addresses(deployments: Dict) -> List[str]:
    """
    Get default safe addresses from the provided deployments dict.

    :param deployments:
    :return: list of addresses
    """
    addresses: List[str] = []

    # Ignoring if is canonical, eip155 or zksync
    for _, address_dict in deployments.items():
        addresses.append(address_dict["address"])

    return addresses


def generate_safe_deployments_py():
    """
    Get safe deployments addresses from https://github.com/safe-global/safe-deployments/ and generate python dictionary file
    """

    # Store the version with list of addresses
    safe_deployments: Dict[
        str, Dict[str, Dict[str, List[str]]]
    ] = {}  # Version -> Contract name -> ChainId -> List of addresses
    default_safe_addresses: Dict[
        str, Dict[str, List[str]]
    ] = {}  # Version -> Contract name -> List of addresses
    # Clone repo
    with get_safe_deployments() as repo:
        logging.info(
            f"Generating safe-deployments from {SAFE_DEPLOYMENTS_VERSION} {SAFE_DEPLOYMENTS_URL} "
        )
        repo.git.checkout(SAFE_DEPLOYMENTS_VERSION)
        for root, _, files in sorted(os.walk(SAFE_DEPLOYMENTS_FOLDER, topdown=False)):
            for filename in sorted(files):
                repo_safe_deployment = json.load(open(os.path.join(root, filename)))
                safe_deployments.setdefault(repo_safe_deployment["version"], {})[
                    repo_safe_deployment["contractName"]
                ] = get_network_addresses_by_chain(repo_safe_deployment)
                default_safe_addresses.setdefault(repo_safe_deployment["version"], {})[
                    repo_safe_deployment["contractName"]
                ] = get_default_network_addresses(repo_safe_deployment["deployments"])

        # Write file
        with open(SAFE_ETH_PY_DEPLOYMENTS_FILE, "w") as file:
            file.write(
                "safe_deployments = " + json.dumps(safe_deployments, indent=4) + "\n"
            )
            file.write(
                "default_safe_deployments = "
                + json.dumps(default_safe_addresses, indent=4)
            )


if __name__ == "__main__":
    generate_safe_deployments_py()
