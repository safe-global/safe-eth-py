import json
import os
import shutil

from git import Repo

GIT_URL = "https://github.com/safe-global/safe-deployments.git"
SAFE_DEPLOYMENTS_VERSION = "v1.27.0"  # safe-deployments tag version
REPO_DIR = "safe-deployments"  # temporary folder to clone the repo
DEPLOYMENTS_FOLDER = REPO_DIR + "/src/assets"  # folder where are the deployments
SAFE_ETH_PY_DEPLOYMENTS_PATH = "../gnosis/safe/safe_deployments.py"  # Path and filename where the new dict is being stored


def clean_resources():
    """Removes the intermediate resources used (source repository)"""
    try:
        shutil.rmtree(REPO_DIR)
    except OSError:
        pass


def generate_safe_deployments_py():
    """
    Get safe deployments addresses from https://github.com/safe-global/safe-deployments/ and generate python dict file
    """
    safe_deployments = {}
    # Clone repo
    repo = Repo.clone_from(GIT_URL, REPO_DIR)
    repo.git.checkout(SAFE_DEPLOYMENTS_VERSION)
    for root, dirs, files in os.walk(DEPLOYMENTS_FOLDER, topdown=False):
        for filename in files:
            safe_deployment = json.load(open(os.path.join(root, filename)))
            safe_deployments[safe_deployment["version"]] = {
                safe_deployment["contractName"]: safe_deployment["networkAddresses"]
            }

    # Write file
    with open(SAFE_ETH_PY_DEPLOYMENTS_PATH, "w") as file:
        file.write("safe_deployments = " + json.dumps(safe_deployments, indent=2))


if __name__ == "__main__":
    generate_safe_deployments_py()
    clean_resources()
