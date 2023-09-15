from abc import ABCMeta, abstractmethod
from functools import cached_property
from logging import getLogger
from typing import Callable, Optional

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract

logger = getLogger(__name__)


class ContractBase(metaclass=ABCMeta):
    def __init__(
        self,
        address: ChecksumAddress,
        ethereum_client: "EthereumClient",  # noqa F821
        *args,
        **kwargs
    ):
        self.address = address
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3

    @abstractmethod
    def get_contract_fn(self) -> Callable[[Web3, Optional[ChecksumAddress]], Contract]:
        """
        :return: Contract function to get the proper contract
        """
        raise NotImplementedError

    @cached_property
    def contract(self) -> Contract:
        return self.get_contract_fn()(self.ethereum_client.w3, self.address)
