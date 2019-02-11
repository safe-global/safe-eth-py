import os
from typing import Tuple, Union

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


def generate_address_2(from_: Union[str, bytes], salt: Union[str, bytes], init_code: [str, bytes]) -> str:
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

    assert len(from_) == 20, "Address %s is not valid. Must be 20 bytes" % from_
    assert len(salt) == 32, "Salt %s is not valid. Must be 32 bytes" % salt
    assert len(init_code) > 0, "Init code %s is not valid" % init_code

    init_code_hash = Web3.sha3(init_code)
    contract_address = Web3.sha3(HexBytes('ff') + from_ + salt + init_code_hash)
    return Web3.toChecksumAddress(contract_address[12:])
