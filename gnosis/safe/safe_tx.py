from typing import Dict, List, Optional, Tuple

from eth_account import Account
from hexbytes import HexBytes
from packaging.version import Version
from web3.exceptions import BadFunctionCallOutput

from py_eth_sig_utils.eip712 import encode_typed_data

from gnosis.eth import EthereumClient
from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract

from .exceptions import (CouldNotPayGasWithEther, CouldNotPayGasWithToken,
                         HashHasNotBeenApproved, InvalidInternalTx,
                         InvalidMultisigTx, InvalidSignaturesProvided,
                         NotEnoughSafeTransactionGas,
                         SignatureNotProvidedByOwner, SignaturesDataTooShort)
from .signatures import signature_split, signature_to_bytes


class SafeTx:
    tx: Dict[str, any]  # If executed, `tx` is set
    tx_hash: bytes  # If executed, `tx_hash` is set

    def __init__(self,
                 ethereum_client: EthereumClient,
                 safe_address: str,
                 to: str,
                 value: int,
                 data: bytes,
                 operation: int,
                 safe_tx_gas: int,
                 base_gas: int,
                 gas_price: int,
                 gas_token: str,
                 refund_receiver: str,
                 signatures: bytes = b'',
                 safe_nonce: Optional[int] = None,
                 safe_version: str = '1.0.0'):

        assert isinstance(signatures, bytes), "Signatures must be bytes"
        self.ethereum_client = ethereum_client
        self.safe_address = safe_address
        self.to = to or NULL_ADDRESS
        self.value = value
        self.data = data or b''
        self.operation = operation
        self.safe_tx_gas = safe_tx_gas
        self.base_gas = base_gas
        self.gas_price = gas_price
        self.gas_token = gas_token or NULL_ADDRESS
        self.refund_receiver = refund_receiver or NULL_ADDRESS
        self.safe_nonce = safe_nonce
        self.signatures = signatures
        self.safe_version = safe_version

    @property
    def w3(self):
        return self.ethereum_client.w3

    @property
    def safe_tx_hash(self) -> HexBytes:
        if self.safe_nonce is None:
            raise ValueError('`safe_nonce` must be set to calculate hash')
        data = self.data.hex() if self.data else ''
        base_gas_name = 'baseGas' if Version(self.safe_version) >= Version('1.0.0') else 'dataGas'

        data = {
            'types': {
                'EIP712Domain': [
                    {'name': 'verifyingContract', 'type': 'address'},
                ],
                'SafeTx': [
                    {'name': 'to', 'type': 'address'},
                    {'name': 'value', 'type': 'uint256'},
                    {'name': 'data', 'type': 'bytes'},
                    {'name': 'operation', 'type': 'uint8'},
                    {'name': 'safeTxGas', 'type': 'uint256'},
                    {'name': base_gas_name, 'type': 'uint256'},
                    {'name': 'gasPrice', 'type': 'uint256'},
                    {'name': 'gasToken', 'type': 'address'},
                    {'name': 'refundReceiver', 'type': 'address'},
                    {'name': 'nonce', 'type': 'uint256'}
                ]
            },
            'primaryType': 'SafeTx',
            'domain': {
                'verifyingContract': self.safe_address,
            },
            'message': {
                'to': self.to,
                'value': self.value,
                'data': data,
                'operation': self.operation,
                'safeTxGas': self.safe_tx_gas,
                base_gas_name: self.base_gas,
                'gasPrice': self.gas_price,
                'gasToken': self.gas_token,
                'refundReceiver': self.refund_receiver,
                'nonce': self.safe_nonce,
            },
        }

        return HexBytes(encode_typed_data(data))

    @property
    def signers(self) -> List[str]:
        owners = []
        for i in range(len(self.signatures) // 65):
            v, r, s = signature_split(self.signatures, i)
            owners.append(EthereumClient.get_signing_address(self.safe_tx_hash, v, r, s))
        return owners

    @property
    def sorted_signers(self):
        return sorted(self.signers, key=lambda x: x.lower())

    @property
    def w3_tx(self):
        """
        :return: Web3 contract tx prepared for `call`, `transact` or `buildTransaction`
        """
        safe_contract = get_safe_contract(self.w3, address=self.safe_address)
        return safe_contract.functions.execTransaction(
            self.to,
            self.value,
            self.data,
            self.operation,
            self.safe_tx_gas,
            self.base_gas,
            self.gas_price,
            self.gas_token,
            self.refund_receiver,
            self.signatures)

    def _parse_vm_exception(self, message: str):
        error_with_exception: Dict[str, Exception] = {
            'Could not pay gas costs with ether': CouldNotPayGasWithEther,
            'Could not pay gas costs with token': CouldNotPayGasWithToken,
            'Hash has not been approved': HashHasNotBeenApproved,
            'Invalid signatures provided': InvalidSignaturesProvided,
            'Not enough gas to execute safe transaction': NotEnoughSafeTransactionGas,
            'Signature not provided by owner': SignatureNotProvidedByOwner,
            'Signatures data too short': SignaturesDataTooShort,
        }
        for reason, custom_exception in error_with_exception.items():
            if reason in message:
                raise custom_exception(message)
        raise InvalidMultisigTx(message)

    def call(self, tx_sender_address: Optional[str] = None, tx_gas: Optional[int] = None,
             block_identifier='pending') -> int:
        """
        :param tx_sender_address:
        :param tx_gas: Force a gas limit
        :param block_identifier:
        :return: `1` if everything ok
        """
        parameters = {}
        if tx_sender_address:
            parameters['from'] = tx_sender_address
        if tx_gas:
            parameters['gas'] = tx_gas
        try:
            success = self.w3_tx.call(parameters, block_identifier=block_identifier)

            if not success:
                raise InvalidInternalTx('Success bit is %d, should be equal to 1' % success)
            return success
        except BadFunctionCallOutput as exc:  # Geth
            return self._parse_vm_exception(str(exc))
        except ValueError as exc:  # Parity
            """
            Parity throws a ValueError, e.g.
            {'code': -32015,
             'message': 'VM execution error.',
             'data': 'Reverted 0x08c379a0000000000000000000000000000000000000000000000000000000000000020000000000000000
                      000000000000000000000000000000000000000000000001b496e76616c6964207369676e6174757265732070726f7669
                      6465640000000000'
            }
            """
            error_dict = exc.args[0]
            data = error_dict.get('data')
            if not data:
                raise exc
            elif isinstance(data, str) and 'Reverted ' in data:
                # Parity
                result = HexBytes(data.replace('Reverted ', ''))
                return self._parse_vm_exception(str(result))

    def execute(self,
                tx_sender_private_key: str,
                tx_gas: Optional[int] = None,
                tx_gas_price: Optional[int] = None,
                tx_nonce: Optional[int] = None,
                block_identifier='pending') -> Tuple[bytes, Dict[str, any]]:
        """
        Send multisig tx to the Safe
        :param tx_sender_private_key: Sender private key
        :param tx_gas: Gas for the external tx. If not, `(safe_tx_gas + base_gas) * 2` will be used
        :param tx_gas_price: Gas price of the external tx. If not, `gas_price` will be used
        :param tx_nonce: Force nonce for `tx_sender`
        :param block_identifier: `latest` or `pending`
        :return: Tuple(tx_hash, tx)
        :raises: InvalidMultisigTx: If user tx cannot go through the Safe
        """

        tx_gas_price = tx_gas_price or self.gas_price  # Use wrapped tx gas_price if not provided
        safe_total_gas = self.safe_tx_gas + self.base_gas
        tx_gas = tx_gas or (safe_total_gas * 2) or (self.w3_tx.estimateGas() + 25000)
        tx_sender_address = Account.privateKeyToAccount(tx_sender_private_key).address

        tx_parameters = {
            'from': tx_sender_address,
            'gas': tx_gas,
            'gasPrice': tx_gas_price,
        }
        if tx_nonce is not None:
            tx_parameters['nonce'] = tx_nonce

        self.tx = self.w3_tx.buildTransaction(tx_parameters)
        self.tx_hash = self.ethereum_client.send_unsigned_transaction(self.tx,
                                                                      private_key=tx_sender_private_key,
                                                                      retry=True,
                                                                      block_identifier=block_identifier)

        # Set signatures empty after executing the tx. `Nonce` is increased even if it fails,
        # so signatures are not valid anymore
        self.signatures = b''
        return self.tx_hash, self.tx

    def sign(self, private_key: str) -> bytes:
        """
        {bytes32 r}{bytes32 s}{uint8 v}
        :param private_key:
        :return:
        """
        account = Account.privateKeyToAccount(private_key)
        signature_dict = account.signHash(self.safe_tx_hash)
        signature = signature_to_bytes((signature_dict['v'],
                                        signature_dict['r'],
                                        signature_dict['s']))

        # Insert signature sorted
        if account.address not in self.signers:
            new_owners = self.signers + [account.address]
            new_owner_pos = sorted(new_owners, key=lambda x: x.lower()).index(account.address)
            self.signatures = (self.signatures[: 65 * new_owner_pos] + signature +
                               self.signatures[65 * new_owner_pos:])
        return signature

    def unsign(self, address: str) -> bool:
        for pos, signer in enumerate(self.signers):
            if signer == address:
                self.signatures = self.signatures.replace(self.signatures[pos * 65: pos * 65 + 65], b'')
                return True
        return False
