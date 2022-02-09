from typing import List, Tuple, Union

from eth_keys import keys
from eth_keys.exceptions import BadSignature
from hexbytes import HexBytes

from gnosis.eth.constants import NULL_ADDRESS


def signature_split(
    signatures: Union[bytes, str], pos: int = 0
) -> Tuple[int, int, int]:
    """
    :param signatures: signatures in form of {bytes32 r}{bytes32 s}{uint8 v}
    :param pos: position of the signature
    :return: Tuple with v, r, s
    """
    signatures = HexBytes(signatures)
    signature_pos = 65 * pos
    if len(signatures[signature_pos : signature_pos + 65]) < 65:
        raise ValueError(f"Signature must be at least 65 bytes {signatures.hex()}")
    r = int.from_bytes(signatures[signature_pos : 32 + signature_pos], "big")
    s = int.from_bytes(signatures[32 + signature_pos : 64 + signature_pos], "big")
    v = signatures[64 + signature_pos]

    return v, r, s


def signature_to_bytes(v: int, r: int, s: int) -> bytes:
    """
    Convert ecdsa signature to bytes
    :param v:
    :param r:
    :param s:
    :return: signature in form of {bytes32 r}{bytes32 s}{uint8 v}
    """

    byte_order = "big"

    return (
        r.to_bytes(32, byteorder=byte_order)
        + s.to_bytes(32, byteorder=byte_order)
        + v.to_bytes(1, byteorder=byte_order)
    )


def signatures_to_bytes(signatures: List[Tuple[int, int, int]]) -> bytes:
    """
    Convert signatures to bytes
    :param signatures: list of tuples(v, r, s)
    :return: 65 bytes per signature
    """
    return b"".join([signature_to_bytes(v, r, s) for v, r, s in signatures])


def get_signing_address(signed_hash: Union[bytes, str], v: int, r: int, s: int) -> str:
    """
    :return: checksummed ethereum address, for example `0x568c93675A8dEb121700A6FAdDdfE7DFAb66Ae4A`
    :rtype: str or `NULL_ADDRESS` if signature is not valid
    """
    try:
        public_key = keys.ecdsa_recover(signed_hash, keys.Signature(vrs=(v - 27, r, s)))
        return public_key.to_checksum_address()
    except BadSignature:
        return NULL_ADDRESS
