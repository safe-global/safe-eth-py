from typing import Optional

from eth_typing import ChecksumAddress
from web3.types import BlockIdentifier

from ..constants import NULL_ADDRESS
from .proxy import Proxy


class StandardProxy(Proxy):
    """
    Standard proxy implementation, following EIP-1967

    https://eips.ethereum.org/EIPS/eip-1967
    """

    # bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1))
    LOGIC_CONTRACT_SLOT = (
        0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC
    )

    # bytes32(uint256(keccak256('eip1967.proxy.beacon')) - 1)
    BEACON_CONTRACT_SLOT = (
        0xA3F0AD74E5423AEBFD80D3EF4346578335A9A72AEAEE59FF6CB3582B35133D50
    )

    # bytes32(uint256(keccak256('eip1967.proxy.admin')) - 1)
    ADMIN_CONTRACT_SLOT = (
        0xB53127684A568B3173AE13B9F8A6016E243E63B6E8EE1178D6A717850B5D6103
    )

    def get_implementation_address(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        """
        :param block_identifier:
        :return: address of the logic contract that this proxy delegates to or the beacon contract
                 the proxy relies on (fallback)
        """
        for slot in (self.LOGIC_CONTRACT_SLOT, self.BEACON_CONTRACT_SLOT):
            storage_bytes = self.w3.eth.get_storage_at(
                self.address, slot, block_identifier=block_identifier
            )
            address = self._parse_address_in_storage(storage_bytes)
            if address != NULL_ADDRESS:
                return address
        return NULL_ADDRESS

    def get_admin_address(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        """
        :param block_identifier:
        :return: address that is allowed to upgrade the logic contract address for the proxy (optional)
        """
        storage_bytes = self.w3.eth.get_storage_at(
            self.address, self.ADMIN_CONTRACT_SLOT, block_identifier=block_identifier
        )
        address = self._parse_address_in_storage(storage_bytes)
        return address
