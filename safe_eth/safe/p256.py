"""
``secp256r1`` (NIST P-256) ECDSA signature **verification**, with the native extension.

This is used to validate Safe ``secp256r1`` owner signatures off-chain (the ``v == 2``
case introduced in Safe ``1.5.0``). On-chain those signatures are verified through the
``RIP-7212`` / ``EIP-7951`` ``P256VERIFY`` precompile; here we reproduce the same check
without an RPC call.
"""

from operator import index

import safe_eth_native

# Order of the P-256 group
_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


def verify(
    message_hash: int, r: int, s: int, public_key_x: int, public_key_y: int
) -> bool:
    """
    Verify a ``secp256r1`` (P-256) ECDSA signature, with the rules of the ``P256VERIFY``
    precompile: ``r`` and ``s`` in ``[1, n - 1]``, high ``s`` values accepted, and a public
    key on the curve.

    :param message_hash: Hash of the signed message as an integer. It must already be the
        digest, exactly as fed to the ``P256VERIFY`` precompile (no extra hashing is done here)
    :param r: ECDSA signature ``r`` value
    :param s: ECDSA signature ``s`` value
    :param public_key_x: ``x`` coordinate of the signer public key
    :param public_key_y: ``y`` coordinate of the signer public key
    :return: ``True`` if the signature is valid, ``False`` otherwise
    :raises TypeError: if a value is not an integer
    """
    # Only ``message_hash`` modulo n is used, also by the precompile
    return safe_eth_native.p256_verify(
        index(message_hash) % _N,
        index(r),
        index(s),
        index(public_key_x),
        index(public_key_y),
    )
