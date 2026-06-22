"""
Pure-Python ``secp256r1`` (NIST P-256) ECDSA signature **verification**.

This is used to validate Safe ``secp256r1`` owner signatures off-chain (the ``v == 2``
case introduced in Safe ``1.5.0``). On-chain those signatures are verified through the
``RIP-7212`` / ``EIP-7951`` ``P256VERIFY`` precompile; here we reproduce the same check
without an RPC call.

Only verification is implemented. No private-key operations are performed, so every input
is public and the lack of constant-time guarantees is not a concern.

The verification follows the standard ECDSA algorithm. The message hash is used directly as
the integer ``z`` (matching the precompile, which is fed a pre-computed digest), so the caller
is responsible for hashing the message beforehand.
"""

from typing import Optional, Tuple

# Domain parameters for the NIST P-256 (a.k.a. secp256r1, prime256v1) curve.
# See https://www.secg.org/sec2-v2.pdf section 2.4.2.
_P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
_A = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
_B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
_GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
_GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

# Affine point. ``None`` represents the point at infinity (the group identity).
Point = Optional[Tuple[int, int]]

# Jacobian point ``(X, Y, Z)`` representing affine ``(X / Z**2, Y / Z**3)``. ``Z == 0`` is the
# identity. Jacobian coordinates avoid a modular inversion on every group operation, which keeps
# scalar multiplication cheap in pure Python.
_JacobianPoint = Tuple[int, int, int]
_IDENTITY: _JacobianPoint = (0, 0, 0)


def _is_on_curve(x: int, y: int) -> bool:
    """
    :return: ``True`` if ``(x, y)`` is a valid affine point on the P-256 curve
    """
    if not (0 <= x < _P and 0 <= y < _P):
        return False
    return (y * y - (x * x * x + _A * x + _B)) % _P == 0


def _jacobian_double(point: _JacobianPoint) -> _JacobianPoint:
    x1, y1, z1 = point
    if z1 == 0 or y1 == 0:
        return _IDENTITY
    # Generic doubling formulas (valid for any ``a``).
    xx = (x1 * x1) % _P
    yy = (y1 * y1) % _P
    yyyy = (yy * yy) % _P
    zz = (z1 * z1) % _P
    s = (2 * (((x1 + yy) ** 2) - xx - yyyy)) % _P
    m = (3 * xx + _A * zz * zz) % _P
    x3 = (m * m - 2 * s) % _P
    y3 = (m * (s - x3) - 8 * yyyy) % _P
    z3 = (((y1 + z1) ** 2) - yy - zz) % _P
    return (x3, y3, z3)


def _jacobian_add(p: _JacobianPoint, q: _JacobianPoint) -> _JacobianPoint:
    x1, y1, z1 = p
    x2, y2, z2 = q
    if z1 == 0:
        return q
    if z2 == 0:
        return p
    z1z1 = (z1 * z1) % _P
    z2z2 = (z2 * z2) % _P
    u1 = (x1 * z2z2) % _P
    u2 = (x2 * z1z1) % _P
    s1 = (y1 * z2 * z2z2) % _P
    s2 = (y2 * z1 * z1z1) % _P
    if u1 == u2:
        if s1 != s2:
            return _IDENTITY  # p == -q, result is the identity
        return _jacobian_double(p)  # p == q
    h = (u2 - u1) % _P
    i = (4 * h * h) % _P
    j = (h * i) % _P
    r = (2 * (s2 - s1)) % _P
    v = (u1 * i) % _P
    x3 = (r * r - j - 2 * v) % _P
    y3 = (r * (v - x3) - 2 * s1 * j) % _P
    z3 = (((z1 + z2) ** 2 - z1z1 - z2z2) * h) % _P
    return (x3, y3, z3)


def _scalar_mult(k: int, point: _JacobianPoint) -> _JacobianPoint:
    result = _IDENTITY
    addend = point
    while k:
        if k & 1:
            result = _jacobian_add(result, addend)
        addend = _jacobian_double(addend)
        k >>= 1
    return result


def _to_affine(point: _JacobianPoint) -> Point:
    x, y, z = point
    if z == 0:
        return None
    z_inv = pow(z, -1, _P)
    z_inv2 = (z_inv * z_inv) % _P
    return ((x * z_inv2) % _P, (y * z_inv2 * z_inv) % _P)


def verify(
    message_hash: int, r: int, s: int, public_key_x: int, public_key_y: int
) -> bool:
    """
    Verify a ``secp256r1`` (P-256) ECDSA signature.

    :param message_hash: Hash of the signed message as an integer. It must already be the
        digest, exactly as fed to the ``P256VERIFY`` precompile (no extra hashing is done here)
    :param r: ECDSA signature ``r`` value
    :param s: ECDSA signature ``s`` value
    :param public_key_x: ``x`` coordinate of the signer public key
    :param public_key_y: ``y`` coordinate of the signer public key
    :return: ``True`` if the signature is valid, ``False`` otherwise
    """
    if not (1 <= r < _N and 1 <= s < _N):
        return False
    if not _is_on_curve(public_key_x, public_key_y):
        return False

    w = pow(s, -1, _N)
    u1 = (message_hash * w) % _N
    u2 = (r * w) % _N
    point = _jacobian_add(
        _scalar_mult(u1, (_GX, _GY, 1)),
        _scalar_mult(u2, (public_key_x, public_key_y, 1)),
    )
    affine = _to_affine(point)
    if affine is None:
        return False
    # SEC1 v2 4.1.4 step 7: accept iff (x_R mod n) == r. ``r`` is already in [1, _N) by the
    # guard above, so it needs no reduction. Matching ``mod _N`` (rather than a bare equality)
    # is the standard check and is what the RIP-7212 / EIP-7951 P256VERIFY precompile does.
    return affine[0] % _N == r
