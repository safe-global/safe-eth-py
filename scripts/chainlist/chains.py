import json
import shutil
from glob import glob

from git import Repo

GIT_URL = "https://github.com/ethereum-lists/chains.git"
REPO_DIR = "sources"
RESULT_FILE_PATH = "result.txt"


def clean_resources() -> None:
    """Removes the intermediate resources used (source repository)"""
    try:
        shutil.rmtree(REPO_DIR)
    except OSError:
        pass


def process_chains() -> None:
    """
    Reads all JSON files in the REPO_DIR directory and processes the data
    in order to write one line per JSON to a result.txt file. Each line is
    formatted as 'CHAIN_NAME = CHAIN_ID'
    """
    clean_resources()
    result_file = open(RESULT_FILE_PATH, "w")
    Repo.clone_from(GIT_URL, REPO_DIR)

    for f_name in glob(REPO_DIR + "/_data/chains/*.json"):
        f = open(f_name)
        data = json.load(f)

        result_file.write(
            "{} = {}\n".format(
                data["name"].upper().replace("-", "_").replace(" ", "_"),
                data["chainId"],
            )
        )

    clean_resources()


if __name__ == "__main__":
    process_chains()
