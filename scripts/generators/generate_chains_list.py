import json
import re
import shutil
from glob import glob
from operator import itemgetter

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


def convert_name(name: str) -> str:
    # Change every symbol that is not a word or digit for underscore
    name_converted = re.sub(r"[^\w\d]+", r"_", name.upper().replace(")", ""))
    # Add underscore at the beggining if start by digit
    if name_converted[0].isdigit():
        name_converted = "_" + name_converted

    return name_converted


def process_chains() -> None:
    """
    Reads all JSON files in the REPO_DIR directory and processes the data
    in order to write one line per JSON to a result.txt file. Each line is
    formatted as 'CHAIN_NAME = CHAIN_ID'
    """
    clean_resources()
    result_file = open(RESULT_FILE_PATH, "w")
    Repo.clone_from(GIT_URL, REPO_DIR)
    chains = []
    for f_name in glob(REPO_DIR + "/_data/chains/*.json"):
        f = open(f_name)
        data = json.load(f)
        chain = {
            "name": convert_name(data["name"]),
            "chainId": data["chainId"],
        }
        chains.append(chain)

    # sort the list by chainId
    chains = sorted(chains, key=itemgetter("chainId"))
    for chain in chains:
        result_file.write(
            "{} = {}\n".format(
                chain["name"].upper(),
                chain["chainId"],
            )
        )

    clean_resources()


if __name__ == "__main__":
    process_chains()
