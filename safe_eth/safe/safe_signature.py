from abc import ABC, abstractmethod
from enum import Enum
from logging import getLogger
from typing import (
    Any,
    ClassVar,
    List,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)

from eth_abi import decode as decode_abi
from eth_abi import encode as encode_abi
from eth_abi.exceptions import DecodingError
from eth_account.messages import defunct_hash_message
from eth_typing import BlockIdentifier, ChecksumAddress, HexAddress, HexStr
from hexbytes import HexBytes
from typing_extensions import Self
from web3 import AsyncWeb3
from web3.exceptions import Web3Exception, Web3RPCError, Web3ValueError

from safe_eth.eth import EthereumClient
from safe_eth.eth.contracts import (
    get_compatibility_fallback_handler_contract,
    get_safe_contract,
)
from safe_eth.eth.utils import fast_to_checksum_address
from safe_eth.safe.signatures import (
    get_signing_address,
    signature_split,
    signature_to_bytes,
)

logger = getLogger(__name__)


EthereumBytes = Union[bytes, str]


class SafeSignatureException(Exception):
    pass


class CannotCheckEIP1271ContractSignature(SafeSignatureException):
    pass


class SafeSignatureType(Enum):
    CONTRACT_SIGNATURE = 0
    APPROVED_HASH = 1
    EOA = 2
    ETH_SIGN = 3

    @staticmethod
    def from_v(v: int):
        if v == 0:
            return SafeSignatureType.CONTRACT_SIGNATURE
        elif v == 1:
            return SafeSignatureType.APPROVED_HASH
        elif v > 30:
            return SafeSignatureType.ETH_SIGN
        else:
            return SafeSignatureType.EOA


def uint_to_address(value: int) -> ChecksumAddress:
    """
    Convert a Solidity `uint` value to a checksummed `address`, removing
    invalid padding bytes if present

    :return: Checksummed address
    """
    encoded = encode_abi(["uint"], [value])
    # Remove padding bytes, as Solidity will ignore it but `eth_abi` will not
    encoded_without_padding_bytes = b"\x00" * 12 + encoded[-20:]
    return fast_to_checksum_address(
        decode_abi(["address"], encoded_without_padding_bytes)[0]
    )


TSafeSignature = TypeVar("TSafeSignature", bound="SafeSignatureBase")


@runtime_checkable
class SupportsContractSignature(Protocol):
    contract_signature: HexBytes


class SafeSignatureBase(ABC):
    contract_signature_cls: ClassVar[Optional[Type["SafeSignatureBase"]]] = None
    approved_hash_cls: ClassVar[Optional[Type["SafeSignatureBase"]]] = None
    eoa_cls: ClassVar[Optional[Type["SafeSignatureBase"]]] = None
    eth_sign_cls: ClassVar[Optional[Type["SafeSignatureBase"]]] = None

    def __init__(self, signature: EthereumBytes, safe_hash: EthereumBytes):
        """
        :param signature: Owner signature
        :param safe_hash: Signed hash for the Safe (message or transaction)
        """
        self.signature = HexBytes(signature)
        self.safe_hash = HexBytes(safe_hash)
        v, r, s = signature_split(self.signature)
        self.v: int = v
        self.r: int = r
        self.s: int = s

    def __str__(self):
        return f"SafeSignature type={self.signature_type.name} owner={self.owner}"

    @classmethod
    def parse_signature(
        cls: Type[TSafeSignature],
        signatures: EthereumBytes,
        safe_hash: EthereumBytes,
        safe_hash_preimage: Optional[EthereumBytes] = None,
        ignore_trailing: bool = True,
    ) -> List[TSafeSignature]:
        """
        :param signatures: One or more signatures appended. EIP1271 data at the end is supported.
        :param safe_hash: Signed hash for the Safe (message or transaction)
        :param safe_hash_preimage: ``safe_hash`` preimage for EIP1271 validation
        :param ignore_trailing: Ignore trailing data on the signature. Some libraries pad it and add some zeroes at
            the end
        :return: List of SafeSignatures decoded
        """
        if not signatures:
            return []
        elif isinstance(signatures, str):
            signatures = HexBytes(signatures)

        signature_size = 65  # For contract signatures there'll be some data at the end
        data_position = len(
            signatures
        )  # For contract signatures, to stop parsing at data position

        safe_signatures: List[TSafeSignature] = []
        for i in range(0, len(signatures), signature_size):
            if (
                i >= data_position
            ):  # If contract signature data position is reached, stop
                break

            signature = signatures[i : i + signature_size]
            if ignore_trailing and len(signature) < 65:
                # Trailing stuff
                break
            v, r, s = signature_split(signature)
            signature_type = SafeSignatureType.from_v(v)
            if signature_type == SafeSignatureType.CONTRACT_SIGNATURE:
                if s < data_position:
                    data_position = s
                contract_signature_len = int.from_bytes(
                    signatures[s : s + 32], "big"
                )  # Len size is 32 bytes
                contract_signature = signatures[
                    s + 32 : s + 32 + contract_signature_len
                ]  # Skip array size (32 bytes)
                safe_signature_cls = cls._get_contract_signature_cls()
                safe_signature = cast(
                    TSafeSignature,
                    cast(Type[Any], safe_signature_cls)(
                        signature,
                        safe_hash,
                        safe_hash_preimage or safe_hash,
                        contract_signature,
                    ),
                )
            elif signature_type == SafeSignatureType.APPROVED_HASH:
                safe_signature_cls = cls._get_approved_hash_cls()
                safe_signature = cast(
                    TSafeSignature,
                    cast(Type[Any], safe_signature_cls)(signature, safe_hash),
                )
            elif signature_type == SafeSignatureType.EOA:
                safe_signature_cls = cls._get_eoa_cls()
                safe_signature = cast(
                    TSafeSignature,
                    cast(Type[Any], safe_signature_cls)(signature, safe_hash),
                )
            elif signature_type == SafeSignatureType.ETH_SIGN:
                safe_signature_cls = cls._get_eth_sign_cls()
                safe_signature = cast(
                    TSafeSignature,
                    cast(Type[Any], safe_signature_cls)(signature, safe_hash),
                )
            else:
                logger.warning("Unexpected signature %s", signature)
                continue

            safe_signatures.append(safe_signature)
        return safe_signatures

    @classmethod
    def export_signatures(
        cls, safe_signatures: Sequence["SafeSignatureBase"]
    ) -> HexBytes:
        """
        Takes a list of SafeSignature objects and exports them as a valid signature for the contract

        :param safe_signatures:
        :return: Valid signature for the Safe contract
        """

        signature = b""
        dynamic_part = b""
        dynamic_offset = len(safe_signatures) * 65
        contract_signature_cls = cls._get_contract_signature_cls()

        # Signatures must be sorted by owner
        for safe_signature in sorted(safe_signatures, key=lambda s: s.owner.lower()):
            if isinstance(safe_signature, contract_signature_cls):
                contract_signature_holder = cast(
                    SupportsContractSignature, safe_signature
                )
                signature += signature_to_bytes(
                    safe_signature.v, safe_signature.r, dynamic_offset
                )
                # encode_abi adds {32 bytes offset}{32 bytes size}. We don't need offset
                contract_signature_padded = encode_abi(
                    ["bytes"], [contract_signature_holder.contract_signature]
                )[32:]
                contract_signature = contract_signature_padded[
                    : 32 + len(contract_signature_holder.contract_signature)
                ]
                dynamic_part += contract_signature
                dynamic_offset += len(contract_signature)
            else:
                signature += safe_signature.export_signature()
        return HexBytes(signature + dynamic_part)

    def export_signature(self) -> HexBytes:
        """
        Exports signature in a format that's valid individually. That's important for contract signatures, as it
        will fix the offset

        :return:
        """
        return self.signature

    @property
    @abstractmethod
    def owner(self) -> ChecksumAddress:
        """
        :return: Decode owner from signature, without any further validation (signature can be not valid)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def signature_type(self) -> SafeSignatureType:
        raise NotImplementedError

    @classmethod
    def _ensure_class(
        cls,
        candidate: Optional[Type["SafeSignatureBase"]],
        attribute: str,
    ) -> Type["SafeSignatureBase"]:
        if candidate is None:
            raise SafeSignatureException(f"{cls.__name__} does not define {attribute}")
        return candidate

    @classmethod
    def _get_contract_signature_cls(cls) -> Type["SafeSignatureBase"]:
        return cls._ensure_class(cls.contract_signature_cls, "contract_signature_cls")

    @classmethod
    def _get_approved_hash_cls(cls) -> Type["SafeSignatureBase"]:
        return cls._ensure_class(cls.approved_hash_cls, "approved_hash_cls")

    @classmethod
    def _get_eoa_cls(cls) -> Type["SafeSignatureBase"]:
        return cls._ensure_class(cls.eoa_cls, "eoa_cls")

    @classmethod
    def _get_eth_sign_cls(cls) -> Type["SafeSignatureBase"]:
        return cls._ensure_class(cls.eth_sign_cls, "eth_sign_cls")


class SafeSignature(SafeSignatureBase):
    @abstractmethod
    def is_valid(
        self,
        ethereum_client: Optional[EthereumClient] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        """
        :param ethereum_client: Required for Contract Signature and Approved Hash check
        :param safe_address: Required for Approved Hash check
        :return: `True` if signature is valid, `False` otherwise
        """
        raise NotImplementedError


class SafeSignatureAsync(SafeSignatureBase):
    @abstractmethod
    async def is_valid(
        self,
        web3: Optional[AsyncWeb3] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        raise NotImplementedError


class SafeSignatureContractMixin(SafeSignatureBase):
    EIP1271_MAGIC_VALUE = HexBytes(0x20C13B0B)
    EIP1271_MAGIC_VALUE_UPDATED = HexBytes(0x1626BA7E)

    def __init__(
        self,
        signature: EthereumBytes,
        safe_hash: EthereumBytes,
        safe_hash_preimage: EthereumBytes,
        contract_signature: EthereumBytes,
    ):
        super().__init__(signature, safe_hash)
        self.safe_hash_preimage: HexBytes = HexBytes(safe_hash_preimage)
        self.contract_signature: HexBytes = HexBytes(contract_signature)

    @classmethod
    def from_values(
        cls,
        safe_owner: ChecksumAddress,
        safe_hash: EthereumBytes,
        safe_hash_preimage: EthereumBytes,
        contract_signature: EthereumBytes,
    ) -> Self:
        signature = signature_to_bytes(
            0, int.from_bytes(HexBytes(safe_owner), byteorder="big"), 65
        )
        return cls(signature, safe_hash, safe_hash_preimage, contract_signature)

    @property
    def owner(self) -> ChecksumAddress:
        return uint_to_address(self.r)

    @property
    def signature_type(self) -> SafeSignatureType:
        return SafeSignatureType.CONTRACT_SIGNATURE

    def export_signature(self) -> HexBytes:
        # encode_abi adds {32 bytes offset}{32 bytes size}. We don't need offset
        contract_signature_padded = encode_abi(["bytes"], [self.contract_signature])[
            32:
        ]
        contract_signature = contract_signature_padded[
            : 32 + len(self.contract_signature)
        ]
        dynamic_offset = 65

        return HexBytes(
            signature_to_bytes(self.v, self.r, dynamic_offset) + contract_signature
        )


class SafeSignatureApprovedHashMixin(SafeSignatureBase):
    @property
    def owner(self) -> ChecksumAddress:
        return uint_to_address(self.r)

    @property
    def signature_type(self) -> SafeSignatureType:
        return SafeSignatureType.APPROVED_HASH

    @classmethod
    def build_for_owner(cls, owner: str, safe_hash: str) -> Self:
        r = owner.lower().replace("0x", "").rjust(64, "0")
        s = "0" * 64
        v = "01"
        return cls(HexBytes(r + s + v), safe_hash)


class SafeSignatureEthSignMixin(SafeSignatureBase):
    @property
    def owner(self) -> ChecksumAddress:
        # defunct_hash_message prepends `\x19Ethereum Signed Message:\n32`
        message_hash = defunct_hash_message(primitive=self.safe_hash)
        return cast(
            ChecksumAddress,
            get_signing_address(message_hash, self.v - 4, self.r, self.s),
        )

    @property
    def signature_type(self) -> SafeSignatureType:
        return SafeSignatureType.ETH_SIGN


class SafeSignatureEOAMixin(SafeSignatureBase):
    @property
    def owner(self) -> ChecksumAddress:
        return cast(
            ChecksumAddress,
            get_signing_address(self.safe_hash, self.v, self.r, self.s),
        )

    @property
    def signature_type(self) -> SafeSignatureType:
        return SafeSignatureType.EOA


class SafeSignatureContract(SafeSignatureContractMixin, SafeSignature):
    def is_valid(
        self,
        ethereum_client: Optional[EthereumClient] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        if ethereum_client is None:
            raise ValueError(
                "ethereum_client is required to validate contract signature"
            )
        compatibility_fallback_handler = get_compatibility_fallback_handler_contract(
            ethereum_client.w3, self.owner
        )
        is_valid_signature_fn = (
            compatibility_fallback_handler.get_function_by_signature(
                "isValidSignature(bytes,bytes)"
            )
        )
        try:
            return is_valid_signature_fn(
                bytes(self.safe_hash_preimage), bytes(self.contract_signature)
            ).call() in (
                self.EIP1271_MAGIC_VALUE,
                self.EIP1271_MAGIC_VALUE_UPDATED,
            )
        except (Web3Exception, DecodingError, Web3ValueError, Web3RPCError):
            # Error using `pending` block identifier or contract does not exist
            logger.warning(
                "Cannot check EIP1271 signature from contract %s", self.owner
            )
        return False


class SafeSignatureApprovedHash(SafeSignatureApprovedHashMixin, SafeSignature):
    def is_valid(
        self,
        ethereum_client: Optional[EthereumClient] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        if ethereum_client is None:
            raise ValueError("ethereum_client is required to validate approved hash")
        if safe_address is None:
            raise ValueError("safe_address is required to validate approved hash")

        safe_contract = get_safe_contract(
            ethereum_client.w3, ChecksumAddress(HexAddress(HexStr(safe_address)))
        )
        exception: Optional[Exception] = None

        block_identifiers: List[BlockIdentifier] = ["pending", "latest"]
        for block_identifier in block_identifiers:
            try:
                return (
                    safe_contract.functions.approvedHashes(
                        self.owner, self.safe_hash
                    ).call(block_identifier=block_identifier)
                    == 1
                )
            except (Web3Exception, DecodingError, Web3ValueError, Web3RPCError) as e:
                exception = e
        if exception:
            raise exception
        raise SafeSignatureException("Could not validate approved hash signature")


class SafeSignatureEthSign(SafeSignatureEthSignMixin, SafeSignature):
    def is_valid(
        self,
        ethereum_client: Optional[EthereumClient] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        return True


class SafeSignatureEOA(SafeSignatureEOAMixin, SafeSignature):
    def is_valid(
        self,
        ethereum_client: Optional[EthereumClient] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        return True


class SafeSignatureContractAsync(SafeSignatureContractMixin, SafeSignatureAsync):
    async def is_valid(
        self,
        web3: Optional[AsyncWeb3] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        if web3 is None:
            raise ValueError("web3 is required to validate contract signature")
        compatibility_fallback_handler = get_compatibility_fallback_handler_contract(
            cast(Any, web3), self.owner
        )
        is_valid_signature_fn = (
            compatibility_fallback_handler.get_function_by_signature(
                "isValidSignature(bytes,bytes)"
            )
        )
        try:
            result = await is_valid_signature_fn(
                bytes(self.safe_hash_preimage), bytes(self.contract_signature)
            ).call()
            return result in (
                self.EIP1271_MAGIC_VALUE,
                self.EIP1271_MAGIC_VALUE_UPDATED,
            )
        except (Web3Exception, DecodingError, Web3ValueError, Web3RPCError):
            logger.warning(
                "Cannot check EIP1271 signature from contract %s", self.owner
            )
        return False


class SafeSignatureApprovedHashAsync(
    SafeSignatureApprovedHashMixin, SafeSignatureAsync
):
    async def is_valid(
        self,
        web3: Optional[AsyncWeb3] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        if web3 is None:
            raise ValueError("web3 is required to validate approved hash")
        if safe_address is None:
            raise ValueError("safe_address is required to validate approved hash")

        safe_contract = get_safe_contract(
            cast(Any, web3), ChecksumAddress(HexAddress(HexStr(safe_address)))
        )
        exception: Optional[Exception] = None

        block_identifiers: List[BlockIdentifier] = ["pending", "latest"]
        for block_identifier in block_identifiers:
            try:
                approved_hashes = await safe_contract.functions.approvedHashes(
                    self.owner, self.safe_hash
                ).call(block_identifier=block_identifier)
                return approved_hashes == 1
            except (Web3Exception, DecodingError, Web3ValueError, Web3RPCError) as e:
                exception = e
        if exception:
            raise exception
        raise SafeSignatureException("Could not validate approved hash signature")


class SafeSignatureEthSignAsync(SafeSignatureEthSignMixin, SafeSignatureAsync):
    async def is_valid(
        self,
        web3: Optional[AsyncWeb3] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        return True


class SafeSignatureEOAAsync(SafeSignatureEOAMixin, SafeSignatureAsync):
    async def is_valid(
        self,
        web3: Optional[AsyncWeb3] = None,
        safe_address: Optional[str] = None,
    ) -> bool:
        return True


SafeSignature.contract_signature_cls = SafeSignatureContract
SafeSignature.approved_hash_cls = SafeSignatureApprovedHash
SafeSignature.eoa_cls = SafeSignatureEOA
SafeSignature.eth_sign_cls = SafeSignatureEthSign

SafeSignatureAsync.contract_signature_cls = SafeSignatureContractAsync
SafeSignatureAsync.approved_hash_cls = SafeSignatureApprovedHashAsync
SafeSignatureAsync.eoa_cls = SafeSignatureEOAAsync
SafeSignatureAsync.eth_sign_cls = SafeSignatureEthSignAsync
