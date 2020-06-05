import os
from typing import Tuple, Union

import eth_abi
from ethereum import utils
from hexbytes import HexBytes
from web3 import Web3


def get_eth_address_with_key() -> Tuple[str, bytes]:
    # import secp256k1
    # private_key = secp256k1.PrivateKey().private_key
    private_key = utils.sha3(os.urandom(4096))
    public_key = utils.checksum_encode(utils.privtoaddr(private_key))
    # If you want to use secp256k1 to calculate public_key
    # utils.checksum_encode(utils.sha3(p.pubkey.serialize(compressed=False)[1:])[-20:])

    return public_key, private_key


def get_eth_address_with_invalid_checksum() -> str:
    address, _ = get_eth_address_with_key()
    return '0x' + ''.join([c.lower() if c.isupper() else c.upper() for c in address[2:]])


def generate_address_2(from_: Union[str, bytes], salt: Union[str, bytes], init_code: Union[str, bytes]) -> str:
    """
    Generates an address for a contract created using CREATE2.
    :param from_: The address which is creating this new address (need to be 20 bytes)
    :param salt: A salt (32 bytes)
    :param init_code: A init code of the contract being created
    :return: Address of the new contract
    """

    from_ = HexBytes(from_)
    salt = HexBytes(salt)
    init_code = HexBytes(init_code)

    assert len(from_) == 20, f'Address {from_.hex()} is not valid. Must be 20 bytes'
    assert len(salt) == 32, f'Salt {salt.hex()} is not valid. Must be 32 bytes'
    assert len(init_code) > 0, f'Init code {init_code.hex()} is not valid'

    init_code_hash = Web3.keccak(init_code)
    contract_address = Web3.keccak(HexBytes('ff') + from_ + salt + init_code_hash)
    return Web3.toChecksumAddress(contract_address[12:])


def decode_string_or_bytes32(data: bytes) -> str:
    try:
        return eth_abi.decode_abi(['string'], data)[0]
    except OverflowError:
        name = eth_abi.decode_abi(['bytes32'], data)[0]
        end_position = name.find(b'\x00')
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
    swarm = b'\xa1\x65bzzr0'
    position = code.find(swarm)
    if position == -1:
        raise ValueError('Swarm metadata not found in code %s' % code.hex())
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
