from abc import ABCMeta

from eth_typing import ChecksumAddress
from web3.types import BlockIdentifier

from ..ethereum_client import EthereumClient
from ..utils import fast_bytes_to_checksum_address


# Not abstract: Proxy is public and can be created directly, and
# get_implementation_address only fails when it is called
class Proxy(metaclass=ABCMeta):  # noqa: B024
    """
    Generic class for proxy contracts
    """

    # Cached on the instance: a cache on the method would keep every instance alive
    _code: bytes | None = None

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

    def get_code(self) -> bytes:
        if self._code is None:
            self._code = self.w3.eth.get_code(self.address)
        return self._code

    def get_implementation_address(
        self, block_identifier: BlockIdentifier | None = "latest"
    ) -> ChecksumAddress:
        """
        :return: Address for the singleton contract the Proxy points to
        """
        raise NotImplementedError
