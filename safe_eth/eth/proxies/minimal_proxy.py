from functools import cache
from typing import Optional

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.types import BlockIdentifier

from ..constants import NULL_ADDRESS
from ..utils import fast_to_checksum_address
from .proxy import Proxy


class MinimalProxy(Proxy):
    """
    Minimal proxy implementation, following EIP-1167

    https://eips.ethereum.org/EIPS/eip-1167
    """

    @staticmethod
    def get_deployment_data(implementation_address: ChecksumAddress) -> bytes:
        """
        :param implementation_address: Contract address the Proxy will point to
        :return: Deployment data for a minimal proxy pointing to the given `contract_address`
        """
        return (
            HexBytes("0x6c3d82803e903d91602b57fd5bf3600d527f363d3d373d3d3d363d73")
            + HexBytes(implementation_address)
            + HexBytes("5af4600052602d6000f3")
        )

    @staticmethod
    def get_expected_code(implementation_address: ChecksumAddress) -> bytes:
        """
        This method is only relevant to do checks and make sure the code deployed is the one expected

        :param implementation_address:
        :return: Expected code for a given `contract_address`
        """
        return (
            HexBytes("363d3d373d3d3d363d73")
            + HexBytes(implementation_address)
            + HexBytes("5af43d82803e903d91602b57fd5bf3")
        )

    @cache
    def get_implementation_address(
        self, block_identifier: Optional[BlockIdentifier] = "latest"
    ) -> ChecksumAddress:
        """
        Minimal proxies cannot be upgraded, so return value is cached

        :return: Address for the singleton contract the Proxy points to
        """
        code = self.get_code()
        if len(code) != 45:  # Not a minimal proxy implementation
            return NULL_ADDRESS

        return fast_to_checksum_address(code[10:30])
