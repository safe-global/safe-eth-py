import json
import os
import shutil
from contextlib import contextmanager

from git import Repo

SAFE_DEPLOYMENTS_URL = "https://github.com/safe-global/safe-deployments.git"
SAFE_DEPLOYMENTS_VERSION = "main"  # safe-deployments tag/branch
SAFE_DEPLOYMENTS_REPO_DIR = "safe-deployments"  # temporary folder to clone the repo
SAFE_DEPLOYMENTS_FOLDER = (
    SAFE_DEPLOYMENTS_REPO_DIR + "/src/assets"
)  # folder where the deployments are
CURRENT_DIRECTORY = os.path.dirname(__file__)
SAFE_ETH_PY_DEPLOYMENTS_FILE = os.path.join(
    CURRENT_DIRECTORY, "../../gnosis/safe/safe_deployments.py"
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


def generate_safe_deployments_py():
    """
    Get safe deployments addresses from https://github.com/safe-global/safe-deployments/ and generate python dictionary file
    """
    safe_deployments = {}
    # Clone repo
    with get_safe_deployments() as repo:
        repo.git.checkout(SAFE_DEPLOYMENTS_VERSION)
        for root, _, files in sorted(os.walk(SAFE_DEPLOYMENTS_FOLDER, topdown=False)):
            for filename in sorted(files):
                repo_safe_deployment = json.load(open(os.path.join(root, filename)))
                safe_deployments.setdefault(repo_safe_deployment["version"], {})[
                    repo_safe_deployment["contractName"]
                ] = repo_safe_deployment["networkAddresses"]

        # Write file
        with open(SAFE_ETH_PY_DEPLOYMENTS_FILE, "w") as file:
            file.write("safe_deployments = " + json.dumps(safe_deployments, indent=4))


if __name__ == "__main__":
    generate_safe_deployments_py()
