from typing import Any, Dict, List, NoReturn, Optional, Tuple, Type

from eth_account import Account
from hexbytes import HexBytes
from packaging.version import Version
from web3.exceptions import BadFunctionCallOutput, ContractLogicError
from web3.types import BlockIdentifier, TxParams, Wei

from py_eth_sig_utils.eip712 import encode_typed_data

from gnosis.eth import EthereumClient
from gnosis.eth.constants import NULL_ADDRESS
from gnosis.eth.contracts import get_safe_contract

from .exceptions import (
    CouldNotFinishInitialization,
    CouldNotPayGasWithEther,
    CouldNotPayGasWithToken,
    HashHasNotBeenApproved,
    InvalidContractSignatureLocation,
    InvalidInternalTx,
    InvalidMultisigTx,
    InvalidOwnerProvided,
    InvalidSignaturesProvided,
    MethodCanOnlyBeCalledFromThisContract,
    ModuleManagerException,
    NotEnoughSafeTransactionGas,
    OnlyOwnersCanApproveAHash,
    OwnerManagerException,
    SafeTransactionFailedWhenGasPriceAndSafeTxGasEmpty,
    SignatureNotProvidedByOwner,
    SignaturesDataTooShort,
    ThresholdNeedsToBeDefined,
)
from .safe_signature import SafeSignature
from .signatures import signature_to_bytes

try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property


class SafeTx:
    tx: TxParams  # If executed, `tx` is set
    tx_hash: bytes  # If executed, `tx_hash` is set

    def __init__(
        self,
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
        signatures: bytes = b"",
        safe_nonce: Optional[int] = None,
        safe_version: str = None,
        chain_id: Optional[int] = None,
    ):
        """
        :param ethereum_client:
        :param safe_address:
        :param to:
        :param value:
        :param data:
        :param operation:
        :param safe_tx_gas:
        :param base_gas:
        :param gas_price:
        :param gas_token:
        :param refund_receiver:
        :param signatures:
        :param safe_nonce: Current nonce of the Safe. If not provided, it will be retrieved from network
        :param safe_version: Safe version 1.0.0 renamed `baseGas` to `dataGas`. Safe version 1.3.0 added `chainId` to
        the `domainSeparator`. If not provided, it will be retrieved from network
        :param chain_id: Ethereum network chain_id is used in hash calculation for Safes >= 1.3.0. If not provided,
        it will be retrieved from the provided ethereum_client
        """

        assert isinstance(signatures, bytes), "Signatures must be bytes"
        self.ethereum_client = ethereum_client
        self.safe_address = safe_address
        self.to = to or NULL_ADDRESS
        self.value = value
        self.data = HexBytes(data) if data else b""
        self.operation = operation
        self.safe_tx_gas = safe_tx_gas
        self.base_gas = base_gas
        self.gas_price = gas_price
        self.gas_token = gas_token or NULL_ADDRESS
        self.refund_receiver = refund_receiver or NULL_ADDRESS
        self.signatures = signatures
        self._safe_nonce = safe_nonce
        self._safe_version = safe_version
        self._chain_id = chain_id

    def __str__(self):
        return (
            f"SafeTx - safe={self.safe_address} - to={self.to} - value={self.value} - data={self.data.hex()} - "
            f"operation={self.operation} - safe-tx-gas={self.safe_tx_gas} - base-gas={self.base_gas} - "
            f"gas-price={self.gas_price} - gas-token={self.gas_token} - refund-receiver={self.refund_receiver} - "
            f"signers = {self.signers}"
        )

    @property
    def w3(self):
        return self.ethereum_client.w3

    @cached_property
    def contract(self):
        return get_safe_contract(self.w3, address=self.safe_address)

    @cached_property
    def chain_id(self) -> int:
        if self._chain_id is not None:
            return self._chain_id
        else:
            return self.w3.eth.chain_id

    @cached_property
    def safe_nonce(self) -> str:
        if self._safe_nonce is not None:
            return self._safe_nonce
        else:
            return self.contract.functions.nonce().call()

    @cached_property
    def safe_version(self) -> str:
        if self._safe_version is not None:
            return self._safe_version
        else:
            return self.contract.functions.VERSION().call()

    @property
    def safe_tx_hash(self) -> HexBytes:
        data = self.data.hex() if self.data else ""

        # Safes >= 1.0.0 Renamed `baseGas` to `dataGas`
        safe_version = Version(self.safe_version)
        base_gas_name = "baseGas" if safe_version >= Version("1.0.0") else "dataGas"

        structured_data = {
            "types": {
                "EIP712Domain": [
                    {"name": "verifyingContract", "type": "address"},
                ],
                "SafeTx": [
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "data", "type": "bytes"},
                    {"name": "operation", "type": "uint8"},
                    {"name": "safeTxGas", "type": "uint256"},
                    {"name": base_gas_name, "type": "uint256"},
                    {"name": "gasPrice", "type": "uint256"},
                    {"name": "gasToken", "type": "address"},
                    {"name": "refundReceiver", "type": "address"},
                    {"name": "nonce", "type": "uint256"},
                ],
            },
            "primaryType": "SafeTx",
            "domain": {
                "verifyingContract": self.safe_address,
            },
            "message": {
                "to": self.to,
                "value": self.value,
                "data": data,
                "operation": self.operation,
                "safeTxGas": self.safe_tx_gas,
                base_gas_name: self.base_gas,
                "gasPrice": self.gas_price,
                "gasToken": self.gas_token,
                "refundReceiver": self.refund_receiver,
                "nonce": self.safe_nonce,
            },
        }

        # Safes >= 1.3.0 Added `chainId` to the domain
        if safe_version >= Version("1.3.0"):
            # EIP712Domain(uint256 chainId,address verifyingContract)
            structured_data["types"]["EIP712Domain"].insert(
                0, {"name": "chainId", "type": "uint256"}
            )
            structured_data["domain"]["chainId"] = self.chain_id

        return HexBytes(encode_typed_data(structured_data))

    @property
    def signers(self) -> List[str]:
        return [
            safe_signature.owner
            for safe_signature in SafeSignature.parse_signature(
                self.signatures, self.safe_tx_hash
            )
        ]

    @property
    def sorted_signers(self):
        return sorted(self.signers, key=lambda x: int(x, 16))

    @property
    def w3_tx(self):
        """
        :return: Web3 contract tx prepared for `call`, `transact` or `buildTransaction`
        """
        return self.contract.functions.execTransaction(
            self.to,
            self.value,
            self.data,
            self.operation,
            self.safe_tx_gas,
            self.base_gas,
            self.gas_price,
            self.gas_token,
            self.refund_receiver,
            self.signatures,
        )

    def _raise_safe_vm_exception(self, message: str) -> NoReturn:
        error_with_exception: Dict[str, Type[InvalidMultisigTx]] = {
            # https://github.com/gnosis/safe-contracts/blob/v1.3.0/docs/error_codes.md
            "GS000": CouldNotFinishInitialization,
            "GS001": ThresholdNeedsToBeDefined,
            "Could not pay gas costs with ether": CouldNotPayGasWithEther,
            "GS011": CouldNotPayGasWithEther,
            "Could not pay gas costs with token": CouldNotPayGasWithToken,
            "GS012": CouldNotPayGasWithToken,
            "GS013": SafeTransactionFailedWhenGasPriceAndSafeTxGasEmpty,
            "Hash has not been approved": HashHasNotBeenApproved,
            "Hash not approved": HashHasNotBeenApproved,
            "GS025": HashHasNotBeenApproved,
            "Invalid contract signature location: data not complete": InvalidContractSignatureLocation,
            "GS023": InvalidContractSignatureLocation,
            "Invalid contract signature location: inside static part": InvalidContractSignatureLocation,
            "GS021": InvalidContractSignatureLocation,
            "Invalid contract signature location: length not present": InvalidContractSignatureLocation,
            "GS022": InvalidContractSignatureLocation,
            "Invalid contract signature provided": InvalidContractSignatureLocation,
            "GS024": InvalidContractSignatureLocation,
            "Invalid owner provided": InvalidOwnerProvided,
            "Invalid owner address provided": InvalidOwnerProvided,
            "GS026": InvalidOwnerProvided,
            "Invalid signatures provided": InvalidSignaturesProvided,
            "Not enough gas to execute safe transaction": NotEnoughSafeTransactionGas,
            "GS010": NotEnoughSafeTransactionGas,
            "Only owners can approve a hash": OnlyOwnersCanApproveAHash,
            "GS030": OnlyOwnersCanApproveAHash,
            "GS031": MethodCanOnlyBeCalledFromThisContract,
            "Signature not provided by owner": SignatureNotProvidedByOwner,
            "Signatures data too short": SignaturesDataTooShort,
            "GS020": SignaturesDataTooShort,
            # ModuleManager
            "GS100": ModuleManagerException,
            "Invalid module address provided": ModuleManagerException,
            "GS101": ModuleManagerException,
            "GS102": ModuleManagerException,
            "Invalid prevModule, module pair provided": ModuleManagerException,
            "GS103": ModuleManagerException,
            "Method can only be called from an enabled module": ModuleManagerException,
            "GS104": ModuleManagerException,
            "Module has already been added": ModuleManagerException,
            # OwnerManager
            "Address is already an owner": OwnerManagerException,
            "GS200": OwnerManagerException,  # Owners have already been setup
            "GS201": OwnerManagerException,  # Threshold cannot exceed owner count
            "GS202": OwnerManagerException,  # Invalid owner address provided
            "GS203": OwnerManagerException,  # Invalid ower address provided
            "GS204": OwnerManagerException,  # Address is already an owner
            "GS205": OwnerManagerException,  # Invalid prevOwner, owner pair provided
            "Invalid prevOwner, owner pair provided": OwnerManagerException,
            "New owner count needs to be larger than new threshold": OwnerManagerException,
            "Threshold cannot exceed owner count": OwnerManagerException,
            "Threshold needs to be greater than 0": OwnerManagerException,
        }

        for reason, custom_exception in error_with_exception.items():
            if reason in message:
                raise custom_exception(message)
        raise InvalidMultisigTx(message)

    def call(
        self,
        tx_sender_address: Optional[str] = None,
        tx_gas: Optional[int] = None,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> int:
        """
        :param tx_sender_address:
        :param tx_gas: Force a gas limit
        :param block_identifier:
        :return: `1` if everything ok
        """
        parameters: Dict[str, Any] = {
            "from": tx_sender_address if tx_sender_address else self.safe_address
        }

        if tx_gas:
            parameters["gas"] = tx_gas
        try:
            success = self.w3_tx.call(parameters, block_identifier=block_identifier)

            if not success:
                raise InvalidInternalTx(
                    "Success bit is %d, should be equal to 1" % success
                )
            return success
        except (ContractLogicError, BadFunctionCallOutput) as exc:
            # e.g. web3.exceptions.ContractLogicError: execution reverted: Invalid owner provided
            return self._raise_safe_vm_exception(str(exc))
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
            data = error_dict.get("data")
            if data and isinstance(data, str) and "Reverted " in data:
                # Parity
                result = HexBytes(data.replace("Reverted ", ""))
                return self._raise_safe_vm_exception(str(result))
            else:
                raise exc

    def recommended_gas(self) -> Wei:
        """
        :return: Recommended gas to use on the ethereum_tx
        """
        return Wei(self.base_gas + self.safe_tx_gas + 75000)

    def execute(
        self,
        tx_sender_private_key: str,
        tx_gas: Optional[int] = None,
        tx_gas_price: Optional[int] = None,
        tx_nonce: Optional[int] = None,
        block_identifier: Optional[BlockIdentifier] = "latest",
    ) -> Tuple[HexBytes, TxParams]:
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

        sender_account = Account.from_key(tx_sender_private_key)
        tx_gas_price = tx_gas_price or self.gas_price or self.w3.eth.gas_price

        tx_parameters = {
            "from": sender_account.address,
            "gasPrice": tx_gas_price,
        }

        if tx_gas:
            tx_parameters["gas"] = tx_gas
        if tx_nonce is not None:
            tx_parameters["nonce"] = tx_nonce

        self.tx = self.w3_tx.buildTransaction(tx_parameters)
        self.tx["gas"] = Wei(
            tx_gas or (max(self.tx["gas"] + 75000, self.recommended_gas()))
        )

        self.tx_hash = self.ethereum_client.send_unsigned_transaction(
            self.tx,
            private_key=sender_account.key,
            retry=False if tx_nonce is not None else True,
            block_identifier=block_identifier,
        )

        # Set signatures empty after executing the tx. `Nonce` is increased even if it fails,
        # so signatures are not valid anymore
        self.signatures = b""
        return self.tx_hash, self.tx

    def sign(self, private_key: str) -> bytes:
        """
        {bytes32 r}{bytes32 s}{uint8 v}
        :param private_key:
        :return: Signature
        """
        account = Account.from_key(private_key)
        signature_dict = account.signHash(self.safe_tx_hash)
        signature = signature_to_bytes(
            signature_dict["v"], signature_dict["r"], signature_dict["s"]
        )

        # Insert signature sorted
        if account.address not in self.signers:
            new_owners = self.signers + [account.address]
            new_owner_pos = sorted(new_owners, key=lambda x: int(x, 16)).index(
                account.address
            )
            self.signatures = (
                self.signatures[: 65 * new_owner_pos]
                + signature
                + self.signatures[65 * new_owner_pos :]
            )
        return signature

    def unsign(self, address: str) -> bool:
        for pos, signer in enumerate(self.signers):
            if signer == address:
                self.signatures = self.signatures.replace(
                    self.signatures[pos * 65 : pos * 65 + 65], b""
                )
                return True
        return False
