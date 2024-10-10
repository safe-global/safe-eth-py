from typing import Optional

from eth_typing import ChecksumAddress
from web3.types import BlockIdentifier

from .proxy import Proxy


class SafeProxy(Proxy):
    """
    Proxy implementation from Safe
    """

    def get_implementation_address(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        """
        :return: Address for the singleton contract the Proxy points to
        """
        storage_bytes = self.w3.eth.get_storage_at(
            self.address, 0, block_identifier=block_identifier
        )
        return self._parse_address_in_storage(storage_bytes)
