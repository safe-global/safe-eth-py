import re
from operator import itemgetter

import requests

CHAINLIST_URL = "https://chainlist.org/rpcs.json"
RESULT_FILE_PATH = "result.txt"


def convert_name(name: str) -> str:
    # Change every symbol that is not a word or digit for underscore
    name_converted = re.sub(r"[^\w\d]+", r"_", name.upper().replace(")", ""))
    # Add underscore at the beginning if start by digit
    if name_converted[0].isdigit():
        name_converted = "_" + name_converted

    return name_converted


def process_chains() -> None:
    """
    Fetches chain data from chainlist.org/rpcs.json and processes the data
    in order to write one line per chain to a result.txt file. Each line is
    formatted as 'CHAIN_NAME = CHAIN_ID'
    """
    result_file = open(RESULT_FILE_PATH, "w")

    # Fetch chains data from chainlist.org
    response = requests.get(CHAINLIST_URL)
    response.raise_for_status()
    chains_data = response.json()

    chains = []
    for chain_data in chains_data:
        if "name" in chain_data and "chainId" in chain_data:
            chain = {
                "name": convert_name(chain_data["name"]),
                "chainId": chain_data["chainId"],
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


if __name__ == "__main__":
    process_chains()
