import os
from dataclasses import dataclass
from functools import cache
from typing import Any, Dict, List, Optional, Union

import requests
from eth_typing import HexStr
from hexbytes import HexBytes


class EnsClient:
    """
    Resolves Ethereum Name Service domains using ``thegraph`` API
    """

    @dataclass
    class Config:
        base_url: str

        @property
        def url(self) -> str:
            return self.base_url

    @dataclass
    class SubgraphConfig(Config):
        api_key: str
        subgraph_id: str

        @property
        def url(self):
            return f"{self.base_url}/api/{self.api_key}/subgraphs/id/{self.subgraph_id}"

    def __init__(self, config: Config):
        self.config = config
        self.request_timeout = int(
            os.environ.get("ENS_CLIENT_REQUEST_TIMEOUT", 5)
        )  # Seconds
        self.request_session = requests.Session()

    def is_available(self) -> bool:
        """
        :return: True if service is available, False if it's down
        """
        query = {"query": "{ __schema { queryType { name } } }"}
        try:
            response = self.request_session.post(
                self.config.url, json=query, timeout=self.request_timeout
            )
            return response.ok
        except IOError:
            return False

    @staticmethod
    def domain_hash_to_hex_str(domain_hash: Union[HexStr, bytes, int]) -> HexStr:
        """
        :param domain_hash:
        :return: Domain hash as an hex string of 66 chars (counting with 0x), padding with zeros if needed
        """
        if not domain_hash:
            domain_hash = b""
        return HexStr("0x" + HexBytes(domain_hash).hex()[2:].rjust(64, "0"))

    @cache
    def _query_by_domain_hash(self, domain_hash_str: HexStr) -> Optional[str]:
        query = """
                {
                    domains(where: {labelhash: "domain_hash"}) {
                        labelName
                    }
                }
                """.replace(
            "domain_hash", domain_hash_str
        )
        try:
            response = self.request_session.post(
                self.config.url,
                json={"query": query},
                timeout=self.request_timeout,
            )
        except IOError:
            return None

        """
        Example:
        {
            "data": {
                "domains": [
                    {
                        "labelName": "safe-multisig"
                    }
                ]
            }
        }
        """
        if response.ok:
            data = response.json()
            if data:
                domains = data.get("data", {}).get("domains")
                if domains:
                    return domains[0].get("labelName")
        return None

    def query_by_domain_hash(
        self, domain_hash: Union[HexStr, bytes, int]
    ) -> Optional[str]:
        """
        Get domain label from domain_hash (keccak of domain name without the TLD, don't confuse with namehash)
        used for ENS ERC721 token_id. Use another method for caching purposes (use same parameter type)

        :param domain_hash: keccak of domain name without the TLD, don't confuse with namehash. E.g. For
            batman.eth it would be just keccak('batman')
        :return: domain label if found
        """
        domain_hash_str = self.domain_hash_to_hex_str(domain_hash)
        return self._query_by_domain_hash(domain_hash_str)

    def query_by_account(self, account: str) -> Optional[List[Dict[str, Any]]]:
        """
        :param account: ethereum account to search for ENS registered addresses
        :return: None if there's a problem or not found, otherwise example of dictionary returned:
        {
            "registrations": [
                {
                    "domain": {
                        "isMigrated": true,
                        "labelName": "gilfoyle",
                        "labelhash": "0xadfd886b420023026d5c0b1be0ffb5f18bb2f37143dff545aeaea0d23a4ba910",
                        "name": "gilfoyle.eth",
                        "parent": {
                            "name": "eth"
                        }
                    },
                    "expiryDate": "1905460880"
                }
            ]
        }
        """
        query = """query getRegistrations {
          account(id: "account_id") {
            registrations {
              expiryDate
              domain {
                labelName
                labelhash
                name
                isMigrated
                parent {
                  name
                }
              }
            }
          }
        }""".replace(
            "account_id", account.lower()
        )
        try:
            response = self.request_session.post(
                self.config.url,
                json={"query": query},
                timeout=self.request_timeout,
            )
        except IOError:
            return None

        if response.ok:
            data = response.json()
            if data:
                return data.get("data", {}).get("account")
        return None
