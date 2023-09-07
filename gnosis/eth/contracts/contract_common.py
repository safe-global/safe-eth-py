from logging import getLogger
from typing import Optional

from web3.types import TxParams

logger = getLogger(__name__)


class ContractCommon:
    def configure_tx_parameters(
        self,
        from_address: str,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
    ) -> TxParams:
        tx_parameters = {"from": from_address}

        if gas_price is not None:
            tx_parameters["gasPrice"] = gas_price

        if gas is not None:
            tx_parameters["gas"] = gas

        if nonce is not None:
            tx_parameters["nonce"] = nonce

        return tx_parameters
