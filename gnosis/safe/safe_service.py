from enum import Enum
from logging import getLogger
from typing import List, Set, Tuple, Union

from django_eth.constants import NULL_ADDRESS
from ethereum.utils import check_checksum
from hexbytes import HexBytes
from py_eth_sig_utils.eip712 import encode_typed_data
from web3.exceptions import BadFunctionCallOutput

from .contracts import (get_paying_proxy_contract,
                        get_paying_proxy_deployed_bytecode, get_safe_contract)
from .ethereum_service import EthereumService, EthereumServiceProvider
from .safe_creation_tx import SafeCreationTx

logger = getLogger(__name__)


class SafeServiceException(Exception):
    pass


class GasPriceTooLow(SafeServiceException):
    pass


class NotEnoughFundsForMultisigTx(SafeServiceException):
    pass


class InvalidRefundReceiver(SafeServiceException):
    pass


class InvalidProxyContract(SafeServiceException):
    pass


class InvalidMasterCopyAddress(SafeServiceException):
    pass


class SafeGasEstimationError(SafeServiceException):
    pass


class InvalidChecksumAddress(SafeServiceException):
    pass


class InvalidMultisigTx(SafeServiceException):
    pass


class InvalidInternalTx(InvalidMultisigTx):
    pass


class SignatureNotProvidedByOwner(InvalidMultisigTx):
    pass


class InvalidSignaturesProvided(InvalidMultisigTx):
    pass


class CannotPayGasWithEther(InvalidMultisigTx):
    pass


class SafeOperation(Enum):
    CALL = 0
    DELEGATE_CALL = 1
    CREATE = 2


class SafeServiceProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            from django.conf import settings
            ethereum_service = EthereumServiceProvider()
            cls.instance = SafeService(ethereum_service,
                                       settings.SAFE_CONTRACT_ADDRESS,
                                       settings.SAFE_VALID_CONTRACT_ADDRESSES,
                                       settings.SAFE_TX_SENDER_PRIVATE_KEY,
                                       settings.SAFE_FUNDER_PRIVATE_KEY)
        return cls.instance

    @classmethod
    def del_singleton(cls):
        if hasattr(cls, "instance"):
            del cls.instance


class SafeService:
    GAS_FOR_MASTER_DEPLOY = 6000000
    GAS_FOR_PROXY_DEPLOY = 5125602

    def __init__(self, ethereum_service: EthereumService,
                 master_copy_address: str,
                 valid_master_copy_addresses: Set[str],
                 tx_sender_private_key: str=None,
                 funder_private_key: str=None):
        self.ethereum_service = ethereum_service
        self.w3 = self.ethereum_service.w3

        for address in [master_copy_address] + list(valid_master_copy_addresses):
            if address and not check_checksum(address):
                raise InvalidChecksumAddress('Master copy without checksum')

        self.master_copy_address = master_copy_address
        self.valid_master_copy_addresses = set(valid_master_copy_addresses)
        if master_copy_address:
            self.valid_master_copy_addresses.add(master_copy_address)
        else:
            logger.warning('Master copy address for SafeService is None')

        self.tx_sender_private_key = tx_sender_private_key
        self.funder_private_key = funder_private_key
        if self.funder_private_key:
            self.funder_address = self.ethereum_service.private_key_to_address(self.funder_private_key)
        else:
            self.funder_address = None

    def get_contract(self, safe_address=None):
        if safe_address:
            return get_safe_contract(self.w3, address=safe_address)
        else:
            return get_safe_contract(self.w3)

    def build_safe_creation_tx(self, s: int, owners: List[str], threshold: int, gas_price: int,
                               payment_token: Union[str, None], payment_token_eth_value: float=1.0,
                               fixed_creation_cost: Union[int, None]=None) -> SafeCreationTx:
        safe_creation_tx = SafeCreationTx(w3=self.w3,
                                          owners=owners,
                                          threshold=threshold,
                                          signature_s=s,
                                          master_copy=self.master_copy_address,
                                          gas_price=gas_price,
                                          funder=self.funder_address,
                                          payment_token=payment_token,
                                          payment_token_eth_value=payment_token_eth_value,
                                          fixed_creation_cost=fixed_creation_cost)

        assert safe_creation_tx.contract_creation_tx.nonce == 0
        return safe_creation_tx

    def deploy_master_contract(self, deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy master contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key

        safe_contract = self.get_contract()
        constructor = safe_contract.constructor()
        gas = self.GAS_FOR_MASTER_DEPLOY

        if deployer_private_key:
            deployer_account = self.ethereum_service.private_key_to_address(deployer_private_key)
            tx = constructor.transact({'gas': gas}).buildTransaction()
            signed_tx = self.w3.eth.account.signTransaction(tx, private_key=deployer_private_key)
            tx_hash = self.ethereum_service.send_raw_transaction(signed_tx.rawTransaction)
        else:
            tx_hash = constructor.transact({'from': deployer_account, 'gas': gas})

        tx_receipt = self.ethereum_service.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        contract_address = tx_receipt.contractAddress

        # Init master copy
        master_safe = self.get_contract(contract_address)
        setup_function = master_safe.functions.setup(
            # We use 2 owners that nobody controls for the master copy
            ["0x0000000000000000000000000000000000000002", "0x0000000000000000000000000000000000000003"],
            # Maximum security
            2,
            NULL_ADDRESS,
            b''
        )

        if deployer_private_key:
            tx = setup_function.transact({'gas': gas}).buildTransaction()
            signed_tx = self.w3.eth.account.signTransaction(tx, private_key=deployer_private_key)
            tx_hash = self.ethereum_service.send_raw_transaction(signed_tx.rawTransaction)
        else:
            tx_hash = setup_function.transact({'from': deployer_account})

        tx_receipt = self.ethereum_service.get_transaction_receipt(tx_hash, timeout=60)
        assert tx_receipt.status

        logger.info("Deployed and initialized Safe Master Contract=%s by %s", contract_address, deployer_account)
        return contract_address

    def deploy_proxy_contract(self, deployer_account=None, deployer_private_key=None) -> str:
        """
        Deploy proxy contract. Takes deployer_account (if unlocked in the node) or the deployer private key
        :param deployer_account: Unlocked ethereum account
        :param deployer_private_key: Private key of an ethereum account
        :return: deployed contract address
        """
        assert deployer_account or deployer_private_key

        safe_proxy_contract = get_paying_proxy_contract(self.w3)
        constructor = safe_proxy_contract.constructor(self.master_copy_address, b'', NULL_ADDRESS, NULL_ADDRESS, 0)
        gas = self.GAS_FOR_PROXY_DEPLOY

        if deployer_account:
            tx_hash = constructor.transact({'from': deployer_account, 'gas': gas})
        else:
            tx = constructor.transact({'gas': gas}).buildTransaction()
            signed_tx = self.w3.eth.account.signTransaction(tx, private_key=deployer_private_key)
            tx_hash = self.ethereum_service.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = self.ethereum_service.get_transaction_receipt(tx_hash, timeout=60)

        contract_address = tx_receipt.contractAddress
        return contract_address

    def check_master_copy(self, address) -> bool:
        return self.retrieve_master_copy_address(address) in self.valid_master_copy_addresses

    def check_proxy_code(self, address) -> bool:
        """
        Check if proxy is valid
        :param address: address of the proxy
        :return: True if proxy is valid, False otherwise
        """
        deployed_proxy_code = self.w3.eth.getCode(address)
        proxy_code = get_paying_proxy_deployed_bytecode()

        return deployed_proxy_code == proxy_code

    def get_refund_receiver(self):
        return NULL_ADDRESS

    def is_master_copy_deployed(self):
        code = self.w3.eth.getCode(self.master_copy_address)
        return not (code == b'\x00')

    def retrieve_master_copy_address(self, safe_address, block_identifier='pending') -> str:
        return get_paying_proxy_contract(self.w3, safe_address).functions.implementation().call(
            block_identifier=block_identifier)

    def retrieve_is_hash_approved(self, safe_address, owner: str, safe_hash: bytes, block_identifier='pending') -> bool:
        return self.get_contract(safe_address
                                 ).functions.approvedHashes(owner,
                                                            safe_hash).call(block_identifier=block_identifier) == 1

    def retrieve_is_message_signed(self, safe_address, message_hash: bytes, block_identifier='pending') -> bool:
        return self.get_contract(safe_address
                                 ).functions.signedMessages(message_hash).call(block_identifier=block_identifier)

    def retrieve_is_owner(self, safe_address, owner: str, block_identifier='pending') -> bool:
        return self.get_contract(safe_address).functions.isOwner(owner).call(block_identifier=block_identifier)

    def retrieve_nonce(self, safe_address, block_identifier='pending') -> int:
        return self.get_contract(safe_address).functions.nonce().call(block_identifier=block_identifier)

    def retrieve_owners(self, safe_address, block_identifier='pending')-> List[str]:
        return self.get_contract(safe_address).functions.getOwners().call(block_identifier=block_identifier)

    def retrieve_threshold(self, safe_address, block_identifier='pending') -> int:
        return self.get_contract(safe_address).functions.getThreshold().call(block_identifier=block_identifier)

    def estimate_tx_gas(self, safe_address: str, to: str, value: int, data: bytes, operation: int) -> int:
        """
        :return: int: Estimated gas
        :raises: SafeGasEstimationError: If gas cannot be estimated
        :raises: ValueError: Cannot decode received data
        """
        data = data or b''
        # Add 10k else we will fail in case of nested calls
        base_gas = 10000
        try:
            tx = self.get_contract(safe_address).functions.requiredTxGas(
                to,
                value,
                data,
                operation
            ).buildTransaction({
                'from': safe_address,
                'gas': int(1e7),
                'gasPrice': 0,
            })
            # If we build the tx web3 will not try to decode it for us
            result = self.w3.eth.call(tx, block_identifier='pending').hex()
            # 2 - 0x
            # 8 - error method id
            # 64 - position
            # 64 - length
            estimated_gas_hex = result[138:]

            # Estimated gas in hex must be 64
            if len(estimated_gas_hex) != 64:
                logger.warning('Exception estimating gas, returned value is %s', result)
                raise SafeGasEstimationError(result)

            estimated_gas = int(estimated_gas_hex, 16)
            return estimated_gas + base_gas
        except ValueError as e:
            data = e.args[0]['data']
            key = list(data.keys())[0]
            result = data[key]['return']
            if result == '0x0':
                raise e
            else:
                # Ganache-Cli with no `--noVMErrorsOnRPCResponse` flag enabled
                logger.warning('You should use `--noVMErrorsOnRPCResponse` flag with Ganache-cli')
                estimated_gas_hex = result[138:]
                assert len(estimated_gas_hex) == 64
                estimated_gas = int(estimated_gas_hex, 16)
                return estimated_gas + base_gas

    def estimate_tx_data_gas(self, safe_address: str, to: str, value: int, data: bytes,
                             operation: int, gas_token: str, estimate_tx_gas: int) -> int:
        data = data or b''
        paying_proxy_contract = self.get_contract(safe_address)
        threshold = self.retrieve_threshold(safe_address)

        # Calculate gas for signatures
        signature_gas = threshold * (1 * 68 + 2 * 32 * 68)

        safe_tx_gas = estimate_tx_gas
        data_gas = 0
        gas_price = 1
        gas_token = gas_token or NULL_ADDRESS
        signatures = b''
        refund_receiver = NULL_ADDRESS
        data = HexBytes(paying_proxy_contract.functions.execTransaction(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
        ).buildTransaction({
            'gas': 1,
            'gasPrice': 1
        })['data'])

        data_gas = signature_gas + self.ethereum_service.estimate_data_gas(data)

        # Add aditional gas costs
        if data_gas > 65536:
            data_gas += 64
        else:
            data_gas += 128

        data_gas += 32000  # Base tx costs, transfer costs...

        return data_gas

    def estimate_tx_operational_gas(self, safe_address: str, data_bytes_length: int):
        """
        Estimates the gas for the verification of the signatures and other safe related tasks
        before and after executing a transaction.
        Calculation will be the sum of:
          - Base cost of 15000 gas
          - 100 of gas per word of `data_bytes`
          - Validate the signatures 5000 * threshold (ecrecover for ecdsa ~= 4K gas)
        :param safe_address: Address of the safe
        :return: gas costs per signature * threshold of Safe
        """
        threshold = self.retrieve_threshold(safe_address)
        return 15000 + data_bytes_length // 32 * 100 + 5000 * threshold

    def check_funds_for_tx_gas(self, safe_address: str, safe_tx_gas: int, data_gas: int, gas_price: int,
                               gas_token: str)-> bool:
        """
        Check safe has enough funds to pay for a tx
        :param safe_address: Address of the safe
        :param safe_tx_gas: Start gas
        :param data_gas: Data gas
        :param gas_price: Gas Price
        :param gas_token: Gas Token, to use token instead of ether for the gas
        :return: True if enough funds, False, otherwise
        """
        if gas_token == NULL_ADDRESS:
            balance = self.ethereum_service.get_balance(safe_address)
        else:
            balance = self.ethereum_service.get_erc20_balance(safe_address, gas_token)
        return balance >= (safe_tx_gas + data_gas) * gas_price

    def check_refund_receiver(self, refund_receiver: str) -> bool:
        """
        We only support tx.origin as refund receiver right now
        In the future we can also accept transactions where it is set to our service account to receive the payments.
        This would prevent that anybody can front-run our service
        """
        return refund_receiver == NULL_ADDRESS

    def send_multisig_tx(self,
                         safe_address: str,
                         to: str,
                         value: int,
                         data: bytes,
                         operation: int,
                         safe_tx_gas: int,
                         data_gas: int,
                         gas_price: int,
                         gas_token: str,
                         refund_receiver: str,
                         signatures: bytes,
                         tx_sender_private_key=None,
                         tx_gas=None,
                         tx_gas_price=None) -> Tuple[str, any]:
        """
        Send multisig tx to the Safe
        :param tx_gas: Gas for the external tx. If not, `(safe_tx_gas + data_gas) * 2` will be used
        :param tx_gas_price: Gas price of the external tx. If not, `gas_price` will be used
        :return: Tuple(tx_hash, tx)
        :raises: InvalidMultisigTx: If user tx cannot go through the Safe
        """

        data = data or b''
        gas_token = gas_token or NULL_ADDRESS
        refund_receiver = refund_receiver or NULL_ADDRESS
        to = to or NULL_ADDRESS
        tx_gas_price = tx_gas_price or gas_price  # Use wrapped tx gas_price if not provided

        # Make sure proxy contract is ours
        if not self.check_proxy_code(safe_address):
            raise InvalidProxyContract(safe_address)

        # Make sure master copy is valid
        if not self.check_master_copy(safe_address):
            raise InvalidMasterCopyAddress

        # Check enough funds to pay for the gas
        if not self.check_funds_for_tx_gas(safe_address, safe_tx_gas, data_gas, gas_price, gas_token):
            raise NotEnoughFundsForMultisigTx

        safe_tx_gas_estimation = self.estimate_tx_gas(safe_address, to, value, data, operation)
        safe_data_gas_estimation = self.estimate_tx_data_gas(safe_address, to, value, data, operation,
                                                             gas_token, safe_tx_gas_estimation)
        if safe_tx_gas < safe_tx_gas_estimation or data_gas < safe_data_gas_estimation:
            raise SafeGasEstimationError("Gas should be at least equal to safe-tx-gas=%d and data-gas=%d" %
                                         (safe_tx_gas_estimation, safe_data_gas_estimation))

        tx_gas = tx_gas or (safe_tx_gas + data_gas) * 2
        tx_sender_private_key = tx_sender_private_key or self.tx_sender_private_key
        # TODO Use EthereumService, as it's a static method
        tx_sender_address = self.ethereum_service.private_key_to_address(tx_sender_private_key)

        safe_contract = get_safe_contract(self.w3, address=safe_address)
        try:
            success = safe_contract.functions.execTransaction(
                to,
                value,
                data,
                operation,
                safe_tx_gas,
                data_gas,
                gas_price,
                gas_token,
                refund_receiver,
                signatures,
            ).call({'from': tx_sender_address}, block_identifier='pending')

            if not success:
                raise InvalidInternalTx
        except BadFunctionCallOutput as exc:
            str_exc = str(exc)
            if 'Signature not provided by owner' in str_exc:
                raise SignatureNotProvidedByOwner(str_exc)
            elif 'Invalid signatures provided' in str_exc:
                raise InvalidSignaturesProvided(str_exc)
            elif 'Could not pay gas costs with ether' in str_exc:
                raise CannotPayGasWithEther(str_exc)
            else:
                raise InvalidMultisigTx(str_exc)

        tx = safe_contract.functions.execTransaction(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            data_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
        ).buildTransaction({
            'from': tx_sender_address,
            'gas': tx_gas,
            'gasPrice': tx_gas_price,
            'nonce': self.ethereum_service.get_nonce_for_account(tx_sender_address)
        })

        tx_signed = self.w3.eth.account.signTransaction(tx, tx_sender_private_key)

        return self.w3.eth.sendRawTransaction(tx_signed.rawTransaction), tx

    @staticmethod
    def get_hash_for_safe_tx(safe_address: str, to: str, value: int, data: bytes,
                             operation: int, safe_tx_gas: int, data_gas: int, gas_price: int,
                             gas_token: str, refund_receiver: str, nonce: int) -> HexBytes:

        data = data.hex() if data else ''
        gas_token = gas_token or NULL_ADDRESS
        refund_receiver = refund_receiver or NULL_ADDRESS
        to = to or NULL_ADDRESS

        data = {
                "types": {
                    "EIP712Domain": [
                        { "name": 'verifyingContract', "type": 'address' },
                    ],
                    "SafeTx": [
                        { "name": 'to', "type": 'address' },
                        { "name": 'value', "type": 'uint256' },
                        { "name": 'data', "type": 'bytes' },
                        { "name": 'operation', "type": 'uint8' },
                        { "name": 'safeTxGas', "type": 'uint256' },
                        { "name": 'dataGas', "type": 'uint256' },
                        { "name": 'gasPrice', "type": 'uint256' },
                        { "name": 'gasToken', "type": 'address' },
                        { "name": 'refundReceiver', "type": 'address' },
                        { "name": 'nonce', "type": 'uint256' }
                    ]
                },
                "primaryType": 'SafeTx',
                "domain": {
                    "verifyingContract": safe_address,
                },
                "message": {
                    "to": to,
                    "value": value,
                    "data": data,
                    "operation": operation,
                    "safeTxGas": safe_tx_gas,
                    "dataGas": data_gas,
                    "gasPrice": gas_price,
                    "gasToken": gas_token,
                    "refundReceiver": refund_receiver,
                    "nonce": nonce,
                },
            }

        return HexBytes(encode_typed_data(data))

    def check_hash(self, tx_hash: str, signatures: bytes, owners: List[str]) -> bool:
        for i, owner in enumerate(sorted(owners, key=lambda x: x.lower())):
            v, r, s = self.signature_split(signatures, i)
            if self.ethereum_service.get_signing_address(tx_hash, v, r, s) != owner:
                return False
        return True

    @staticmethod
    def signature_split(signatures: bytes, pos: int) -> Tuple[int, int, int]:
        """
        :param signatures: signatures in form of {bytes32 r}{bytes32 s}{uint8 v}
        :param pos: position of the signature
        :return: Tuple with v, r, s
        """
        signature_pos = 65 * pos
        v = signatures[64 + signature_pos]
        r = int.from_bytes(signatures[signature_pos:32 + signature_pos], 'big')
        s = int.from_bytes(signatures[32 + signature_pos:64 + signature_pos], 'big')

        return v, r, s

    @classmethod
    def signatures_to_bytes(cls, signatures: List[Tuple[int, int, int]]) -> bytes:
        """
        Convert signatures to bytes
        :param signatures: list of tuples(v, r, s)
        :return: 65 bytes per signature
        """
        return b''.join([cls.signature_to_bytes(vrs) for vrs in signatures])

    @staticmethod
    def signature_to_bytes(vrs: Tuple[int, int, int]) -> bytes:
        """
        Convert signature to bytes
        :param vrs: tuple of v, r, s
        :return: signature in form of {bytes32 r}{bytes32 s}{uint8 v}
        """

        byte_order = 'big'

        v, r, s = vrs

        return (r.to_bytes(32, byteorder=byte_order) +
                s.to_bytes(32, byteorder=byte_order) +
                v.to_bytes(1, byteorder=byte_order))
