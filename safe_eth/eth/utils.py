from typing import Any, cast

import eth_abi
import rlp
import safe_eth_native
from eth_account import Account
from eth_typing import AnyAddress, ChecksumAddress, Hash32, HexStr
from eth_utils import to_normalized_address
from hexbytes import HexBytes
from web3.types import TxParams, Wei

from safe_eth.util.util import to_0x_hex_str


def get_empty_tx_params() -> TxParams:
    """
    :return: Empty tx params, so calls like `build_transaction` don't call the RPC trying to get information
    """
    return {
        "gas": Wei(1),
        "gasPrice": Wei(1),
    }


def fast_keccak(value: bytes) -> Hash32:
    """
    Calculates ethereum keccak256 using the native extension

    :param value:
    :return: Keccak256 used by ethereum as `HexBytes`
    """
    return Hash32(HexBytes(safe_eth_native.keccak256(value)))


def fast_keccak_text(value: str) -> Hash32:
    """
    Calculates ethereum keccak256 using the native extension

    :param value:
    :return: Keccak256 used by ethereum as `HexBytes`
    """
    return fast_keccak(value.encode())


def fast_keccak_hex(value: bytes) -> HexStr:
    """
    Same as `fast_keccak`, but returns a hex string

    :param value:
    :return: Keccak256 used by ethereum as a hex string (not 0x prefixed)
    """
    return HexStr(safe_eth_native.keccak256(value).hex())


def fast_to_checksum_address(value: AnyAddress | str | bytes) -> ChecksumAddress:
    """
    Converts to checksum_address using the native extension

    :param value:
    :return:
    """
    if isinstance(value, bytes):
        return fast_bytes_to_checksum_address(value)
    if isinstance(value, str):
        try:
            return cast(ChecksumAddress, safe_eth_native.to_checksum_address(value))
        except ValueError:
            # Raised below by `to_normalized_address`, with the eth-utils error message
            pass
    return cast(
        ChecksumAddress,
        safe_eth_native.to_checksum_address(to_normalized_address(value)),
    )


def fast_bytes_to_checksum_address(value: bytes) -> ChecksumAddress:
    """
    Converts 20 bytes, or an iterable of 20 byte values, to checksum_address using the
    native extension

    :param value:
    :return:
    """
    if not isinstance(value, bytes) and len(value) == 20:
        value = bytes(value)
    if len(value) != 20:
        raise ValueError(
            f"Cannot convert {bytes(value).hex()} to a checksum address, 20 bytes were expected"
        )
    return cast(ChecksumAddress, safe_eth_native.to_checksum_address(value))


def fast_is_checksum_address(value: AnyAddress | str | bytes) -> bool:
    """
    Fast version to check if an address is a checksum_address

    :param value:
    :return: `True` if checksummed, `False` otherwise
    """
    return safe_eth_native.is_checksum_address(value)


def get_eth_address_with_invalid_checksum() -> str:
    address = Account.create().address
    return "0x" + "".join(
        [c.lower() if c.isupper() else c.upper() for c in address[2:]]
    )


def decode_string_or_bytes32(data: bytes) -> str:
    try:
        return eth_abi.decode(["string"], data)[0]
    except (OverflowError, eth_abi.exceptions.DecodingError):
        name = eth_abi.decode(["bytes32"], data)[0]
        end_position = name.find(b"\x00")
        if end_position == -1:
            return name.decode()
        else:
            return name[:end_position].decode()


def remove_swarm_metadata(code: bytes) -> bytes:
    """
    Remove CBOR-encoded metadata (Swarm `bzzr0`/`bzzr1` or IPFS) appended by
    the Solidity compiler to the end of the bytecode.

    Solidity appends a CBOR map followed by its 2-byte big-endian length, e.g.
    ``0xa2 0x64 'ipfs' ... 0x64 'solc' ... <2-byte length>``. The trailing
    length lets us strip the metadata regardless of the encoding version.

    :param code:
    :return: Code without metadata
    """
    if len(code) >= 2:
        metadata_length = int.from_bytes(code[-2:], "big")
        metadata_start = len(code) - 2 - metadata_length
        # A valid metadata blob starts with a CBOR map header (0xa1/0xa2/0xa3)
        if 0 < metadata_length <= len(code) - 2 and code[metadata_start] in (
            0xA1,
            0xA2,
            0xA3,
        ):
            return code[:metadata_start]
    raise ValueError(f"Metadata not found in code {code.hex()}")


def compare_byte_code(code_1: bytes, code_2: bytes) -> bool:
    """
    Compare code, removing swarm metadata if necessary

    :param code_1:
    :param code_2:
    :return: True if same code, False otherwise
    """
    if code_1 == code_2:
        return True
    else:
        codes = []
        for code in (code_1, code_2):
            try:
                codes.append(remove_swarm_metadata(code))
            except ValueError:
                codes.append(code)

        return codes[0] == codes[1]


def mk_contract_address(address: str | bytes, nonce: int) -> ChecksumAddress:
    """
    Generate expected contract address when using EVM CREATE

    :param address:
    :param nonce:
    :return:
    """
    return fast_to_checksum_address(
        fast_keccak(rlp.encode([HexBytes(address), nonce]))[12:]
    )


def mk_contract_address_2(
    from_: ChecksumAddress | bytes,
    salt: HexStr | bytes,
    init_code: HexStr | bytes,
) -> ChecksumAddress:
    """
    Generate expected contract address when using EVM CREATE2.

    :param from_: The address which is creating this new address (need to be 20 bytes)
    :param salt: A salt (32 bytes)
    :param init_code: A init code of the contract being created
    :return: Address of the new contract
    """

    from_ = HexBytes(from_)
    salt = HexBytes(salt)
    init_code = HexBytes(init_code)

    assert len(from_) == 20, (
        f"Address {to_0x_hex_str(from_)} is not valid. Must be 20 bytes"
    )
    assert len(salt) == 32, f"Salt {to_0x_hex_str(salt)} is not valid. Must be 32 bytes"
    assert len(init_code) > 0, f"Init code {to_0x_hex_str(init_code)} is not valid"

    init_code_hash = fast_keccak(init_code)
    contract_address = fast_keccak(HexBytes("ff") + from_ + salt + init_code_hash)
    return fast_bytes_to_checksum_address(contract_address[12:])


def bytes_to_float(value: Any) -> float:
    """
    Convert a value of type Any to float.

    :param value: The value to convert.
    :return: The converted float value.
    :raises ValueError: If the value cannot be converted to float.
    """
    if value is None:
        raise ValueError("Cannot convert None to float")
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, bytes):
        try:
            return float(int.from_bytes(value, "big"))
        except (ValueError, OverflowError) as e:
            raise ValueError(f"Cannot convert bytes to float: {e}") from e
    else:
        raise ValueError(f"Unsupported type for conversion to float: {type(value)}")
