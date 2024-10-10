from abc import ABCMeta
from functools import cache
from typing import Optional

from eth_typing import ChecksumAddress
from web3.types import BlockIdentifier

from ..ethereum_client import EthereumClient
from ..utils import fast_bytes_to_checksum_address


class Proxy(metaclass=ABCMeta):
    """
    Generic class for proxy contracts
    """

    def __init__(self, address: ChecksumAddress, ethereum_client: EthereumClient):
        """
        :param address: Proxy address
        """
        self.address = address
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    def _parse_address_in_storage(self, storage_bytes: bytes) -> ChecksumAddress:
        """
        :param storage_slot:
        :return: A checksummed address in a slot
        """
        address = storage_bytes[-20:].rjust(20, b"\0")
        return fast_bytes_to_checksum_address(address)

    @cache
    def get_code(self):
        return self.w3.eth.get_code(self.address)

    def get_implementation_address(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        """
        :return: Address for the singleton contract the Proxy points to
        """
        raise NotImplementedError
