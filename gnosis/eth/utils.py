from secrets import token_bytes
from typing import Tuple, Union

import eth_abi
from eth._utils.address import generate_contract_address
from eth_keys import keys
from eth_typing import AnyAddress, ChecksumAddress, HexStr
from eth_utils import to_normalized_address
from hexbytes import HexBytes
from sha3 import keccak_256
from web3.types import TxParams, Wei


def get_empty_tx_params() -> TxParams:
    """
    :return: Empty tx params, so calls like `build_transaction` don't call the RPC trying to get information
    """
    return {
        "gas": Wei(1),
        "gasPrice": Wei(1),
    }


def fast_keccak(value: bytes) -> bytes:
    """
    Calculates ethereum keccak256 using fast library `pysha3`
    :param value:
    :return: Keccak256 used by ethereum as `bytes`
    """
    return keccak_256(value).digest()


def fast_keccak_hex(value: bytes) -> HexStr:
    """
    Same as `fast_keccak`, but it's a little more optimal calling `hexdigest()`
    than calling `digest()` and then `hex()`

    :param value:
    :return: Keccak256 used by ethereum as a hex string (not 0x prefixed)
    """
    return HexStr(keccak_256(value).hexdigest())


def _build_checksum_address(
    norm_address: HexStr, address_hash: HexStr
) -> ChecksumAddress:
    """
    https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md

    :param norm_address: address in lowercase (not 0x prefixed)
    :param address_hash: keccak256 of `norm_address` (not 0x prefixed)
    :return:
    """
    return ChecksumAddress(
        "0x"
        + (
            "".join(
                (
                    norm_address[i].upper()
                    if int(address_hash[i], 16) > 7
                    else norm_address[i]
                )
                for i in range(0, 40)
            )
        )
    )


def fast_to_checksum_address(value: Union[AnyAddress, str, bytes]) -> ChecksumAddress:
    """
    Converts to checksum_address. Uses more optimal `pysha3` instead of `eth_utils` for keccak256 calculation

    :param value:
    :return:
    """
    norm_address = to_normalized_address(value)[2:]
    address_hash = fast_keccak_hex(norm_address.encode())
    return _build_checksum_address(norm_address, address_hash)


def fast_bytes_to_checksum_address(value: bytes) -> ChecksumAddress:
    """
    Converts to checksum_address. Uses more optimal `pysha3` instead of `eth_utils` for keccak256 calculation.
    As input is already in bytes, some checks and conversions can be skipped, providing a speedup of ~50%

    :param value:
    :return:
    """
    if len(value) != 20:
        raise ValueError(
            "Cannot convert %s to a checksum address, 20 bytes were expected"
        )
    norm_address = bytes(value).hex()
    address_hash = fast_keccak_hex(norm_address.encode())
    return _build_checksum_address(norm_address, address_hash)


def fast_is_checksum_address(value: Union[AnyAddress, str, bytes]) -> bool:
    """
    Fast version to check if an address is a checksum_address

    :param value:
    :return: `True` if checksummed, `False` otherwise
    """
    if not isinstance(value, str) or len(value) != 42 or not value.startswith("0x"):
        return False
    try:
        return fast_to_checksum_address(value) == value
    except ValueError:
        return False


def get_eth_address_with_key() -> Tuple[str, bytes]:
    private_key = keys.PrivateKey(token_bytes(32))
    address = private_key.public_key.to_checksum_address()
    return address, private_key.to_bytes()


def get_eth_address_with_invalid_checksum() -> str:
    address, _ = get_eth_address_with_key()
    return "0x" + "".join(
        [c.lower() if c.isupper() else c.upper() for c in address[2:]]
    )


def decode_string_or_bytes32(data: bytes) -> str:
    try:
        return eth_abi.decode(["string"], data)[0]
    except OverflowError:
        name = eth_abi.decode(["bytes32"], data)[0]
        end_position = name.find(b"\x00")
        if end_position == -1:
            return name.decode()
        else:
            return name[:end_position].decode()


def remove_swarm_metadata(code: bytes) -> bytes:
    """
    Remove swarm metadata from Solidity bytecode

    :param code:
    :return: Code without metadata
    """
    swarm = b"\xa1\x65bzzr0"
    position = code.rfind(swarm)
    if position == -1:
        raise ValueError("Swarm metadata not found in code %s" % code.hex())
    return code[:position]


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


def mk_contract_address(address: Union[str, bytes], nonce: int) -> ChecksumAddress:
    """
    Generate expected contract address when using EVM CREATE

    :param address:
    :param nonce:
    :return:
    """
    return fast_to_checksum_address(generate_contract_address(HexBytes(address), nonce))


def mk_contract_address_2(
    from_: Union[str, bytes], salt: Union[str, bytes], init_code: Union[str, bytes]
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

    assert len(from_) == 20, f"Address {from_.hex()} is not valid. Must be 20 bytes"
    assert len(salt) == 32, f"Salt {salt.hex()} is not valid. Must be 32 bytes"
    assert len(init_code) > 0, f"Init code {init_code.hex()} is not valid"

    init_code_hash = fast_keccak(init_code)
    contract_address = fast_keccak(HexBytes("ff") + from_ + salt + init_code_hash)
    return fast_bytes_to_checksum_address(contract_address[12:])
