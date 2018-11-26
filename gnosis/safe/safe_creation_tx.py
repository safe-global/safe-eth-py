import math
import os
from logging import getLogger
from typing import Dict, List, Tuple, Union

import rlp
from django_eth.constants import NULL_ADDRESS
from eth_account.internal.transactions import (encode_transaction,
                                               serializable_unsigned_transaction_from_dict)
from ethereum.exceptions import InvalidTransaction
from ethereum.transactions import Transaction, secpk1n
from ethereum.utils import checksum_encode, mk_contract_address
from hexbytes import HexBytes
from web3 import Web3

from .contracts import get_paying_proxy_contract, get_safe_contract

logger = getLogger(__name__)


class SafeCreationTx:
    def __init__(self, w3: Web3, owners: List[str], threshold: int, signature_s: int, master_copy: str,
                 gas_price: int, funder: Union[str, None], payment_token: Union[str, None]=None,
                 payment_token_eth_value: float=1.0, fixed_creation_cost: Union[int, None]=None):
        """
        Prepare Safe creation
        :param w3: Web3 instance
        :param owners: Owners of the Safe
        :param threshold: Minimum number of users required to operate the Safe
        :param signature_s: Random s value for ecdsa signature
        :param master_copy: Safe master copy address
        :param gas_price: Gas Price
        :param funder: Address to refund when the Safe is created. Address(0) if no need to refund
        :param payment_token: Payment token instead of paying the funder with ether. If None Ether will be used
        :param payment_token_eth_value: Value of payment token per 1 Ether
        :param fixed_creation_cost: Fixed creation cost of Safe (Wei)
        """

        assert 0 < threshold <= len(owners)

        self.owners = owners
        self.threshold = threshold
        self.s = signature_s
        self.master_copy = master_copy
        self.gas_price = gas_price
        self.funder = funder or NULL_ADDRESS
        self.payment_token = payment_token or NULL_ADDRESS

        self.gnosis_safe_contract = get_safe_contract(w3, master_copy)
        self.paying_proxy_contract = get_paying_proxy_contract(w3)

        safe_tx = self.get_initial_setup_safe_tx(owners, threshold)
        encoded_data = safe_tx['data']

        self.gas = self._calculate_gas(owners, encoded_data, payment_token)

        # Payment will be safe deploy cost + transfer fees for sending ether to the deployer
        self.payment_ether = (self.gas + 23000) * self.gas_price

        if fixed_creation_cost is None:
            # Calculate payment for tokens using the conversion (if used)
            self.payment = math.ceil(self.payment_ether / payment_token_eth_value)
        else:
            self.payment = fixed_creation_cost

        self.contract_creation_tx_dict = self._build_proxy_contract_creation_tx(master_copy=self.master_copy,
                                                                                initializer=encoded_data,
                                                                                funder=self.funder,
                                                                                payment_token=self.payment_token,
                                                                                payment=self.payment,
                                                                                gas=self.gas,
                                                                                gas_price=self.gas_price)

        (self.contract_creation_tx,
         self.v,
         self.r) = self._generate_valid_transaction(gas_price,
                                                    self.gas,
                                                    self.contract_creation_tx_dict['data'],
                                                    self.s)
        self.raw_tx = rlp.encode(self.contract_creation_tx)
        self.tx_hash = self.contract_creation_tx.hash
        self.deployer_address = checksum_encode(self.contract_creation_tx.sender)
        self.safe_address = checksum_encode(mk_contract_address(self.deployer_address, nonce=0))

    @staticmethod
    def find_valid_random_signature(s: int) -> Tuple[int, int]:
        """
        Find v and r valid values for a given s
        :param s: random value
        :return: v, r
        """
        for _ in range(10000):
            r = int(os.urandom(31).hex(), 16)
            v = (r % 2) + 27
            if r < secpk1n:
                tx = Transaction(0, 1, 21000, b'', 0, b'', v=v, r=r, s=s)
                try:
                    tx.sender
                    return v, r
                except (InvalidTransaction, ValueError):
                    logger.debug('Cannot find signature with v=%d r=%d s=%d', v, r, s)

        raise ValueError('Valid signature not found with s=%d', s)

    @staticmethod
    def _calculate_gas(owners: List[str], encoded_data: bytes, payment_token: str) -> int:
        # TODO Do gas calculation estimating the call instead this magic

        base_gas = 60580  # Transaction standard gas

        # TODO If we already have the token, we don't have to pay for storage, so it will be just 5K instead of 20K.
        # The other 1K is for overhead of making the call
        if payment_token != NULL_ADDRESS:
            payment_token_gas = 21000
        else:
            payment_token_gas = 0

        data_gas = 68 * len(encoded_data)  # Data gas
        gas_per_owner = 18020  # Magic number calculated by testing and averaging owners
        return base_gas + data_gas + payment_token_gas + 270000 + len(owners) * gas_per_owner

    def get_initial_setup_safe_tx(self, owners: List[str], threshold: int) -> Dict[any, any]:
        return self.gnosis_safe_contract.functions.setup(
            owners,
            threshold,
            NULL_ADDRESS,
            b''
        ).buildTransaction({
            'gas': 1,
            'gasPrice': 1,
        })

    def _build_proxy_contract_creation_tx(self,
                                          master_copy: str,
                                          initializer: bytes,
                                          funder: str,
                                          payment_token: str,
                                          payment: int,
                                          gas: int,
                                          gas_price: int,
                                          nonce: int=0):
        """
        :param master_copy: Master Copy of Gnosis Safe already deployed
        :param initializer: Data initializer to send to GnosisSafe setup method
        :param funder: Address that should get the payment (if payment set)
        :param payment_token: Address if a token is used. If not set, 0x0 will be ether
        :param payment: Payment
        :return: Transaction dictionary
        """
        if not funder or funder == NULL_ADDRESS:
            funder = NULL_ADDRESS
            payment = 0

        return self.paying_proxy_contract.constructor(
            master_copy,
            initializer,
            funder,
            payment_token,
            payment
        ).buildTransaction({
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

    def _generate_valid_transaction(self, gas_price: int, gas: int, data: str, s: int, nonce: int=0) -> Tuple[
                                                                                                        Transaction,
                                                                                                        int, int]:
        """
        :return: ContractCreationTx, v, r
        """
        zero_address = HexBytes('0x' + '0' * 40)
        f_address = HexBytes('0x' + 'f' * 40)
        for _ in range(100):
            try:
                v, r = self.find_valid_random_signature(s)
                contract_creation_tx = Transaction(nonce, gas_price, gas, b'', 0, HexBytes(data), v=v, r=r, s=s)
                sender = contract_creation_tx.sender
                if sender in (zero_address, f_address):
                    raise InvalidTransaction
                return contract_creation_tx, v, r
            except InvalidTransaction:
                pass
        raise ValueError('Valid signature not found with s=%d', s)

    @staticmethod
    def _sign_web3_transaction(tx: Dict[str, any], v: int, r: int, s: int) -> (bytes, HexBytes):
        """
        Signed transaction can be send with w3.eth.sendRawTransaction
        """
        unsigned_transaction = serializable_unsigned_transaction_from_dict(tx)
        rlp_encoded_transaction = encode_transaction(unsigned_transaction, vrs=(v, r, s))

        # To get the address signing, just do ecrecover_to_pub(unsigned_transaction.hash(), v, r, s)
        return rlp_encoded_transaction, unsigned_transaction.hash()
