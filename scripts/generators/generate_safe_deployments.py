import json
import os
import shutil
from contextlib import contextmanager
from typing import Dict, List

from git import Repo

SAFE_DEPLOYMENTS_URL = "https://github.com/safe-global/safe-deployments.git"
SAFE_DEPLOYMENTS_VERSION = "main"  # safe-deployments tag/branch
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


def get_network_addresses(safe_deployment: Dict) -> Dict[str, List[str]]:
    """
    Convert canonical and non-canonical from safe-deployments json to the corresponding addresses.

    :param safe_deployment:
    :return:
    """
    network_addresses = {}

    # Applying list because networkAddresses is not list for all networks
    for chain_id, address_types in safe_deployment["networkAddresses"].items():
        addresses: List[str] = []
        if not isinstance(address_types, list):
            address_types = [address_types]
        for address_type in address_types:
            address = safe_deployment["deployments"][address_type]["address"]
            addresses.append(address)

        network_addresses[chain_id] = addresses

    return network_addresses


def generate_safe_deployments_py():
    """
    Get safe deployments addresses from https://github.com/safe-global/safe-deployments/ and generate python dictionary file
    """

    # Store the version with list of addresses
    safe_deployments: Dict[str, List[str]] = {}
    # Clone repo
    with get_safe_deployments() as repo:
        repo.git.checkout(SAFE_DEPLOYMENTS_VERSION)
        for root, _, files in sorted(os.walk(SAFE_DEPLOYMENTS_FOLDER, topdown=False)):
            for filename in sorted(files):
                repo_safe_deployment = json.load(open(os.path.join(root, filename)))
                safe_deployments.setdefault(repo_safe_deployment["version"], {})[
                    repo_safe_deployment["contractName"]
                ] = get_network_addresses(repo_safe_deployment)

        # Write file
        with open(SAFE_ETH_PY_DEPLOYMENTS_FILE, "w") as file:
            file.write("safe_deployments = " + json.dumps(safe_deployments, indent=4))


if __name__ == "__main__":
    generate_safe_deployments_py()
