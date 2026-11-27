# safe-eth-native

Native (Rust) versions of the hot paths of [safe-eth-py](https://github.com/safe-global/safe-eth-py):

| Function | Replaces | Backed by |
| --- | --- | --- |
| `ecrecover(message_hash, v, r, s) -> bytes \| None` | eth-keys `ecdsa_recover` | [libsecp256k1](https://github.com/bitcoin-core/secp256k1) |
| `p256_verify(message_hash, r, s, public_key_x, public_key_y) -> bool` | the pure Python P-256 verifier that `safe_eth.safe.p256` used to have | RustCrypto [`p256`](https://github.com/RustCrypto/elliptic-curves) |
| `keccak256(data) -> bytes` | the eth-hash backend (pycryptodome) | [`tiny-keccak`](https://github.com/debris/tiny-keccak) |
| `to_checksum_address(value) -> str` | `fast_to_checksum_address` | |
| `is_checksum_address(value) -> bool` | `fast_is_checksum_address` | |

`ecrecover` and `p256_verify` follow the input rules of the EVM `ecrecover` and `P256VERIFY`
precompiles: `v` must be 27 or 28, `r` and `s` in `[1, n - 1]`, and high `s` values are
accepted. Values out of those ranges return `None` / `False` instead of raising; only a
wrong type, or a hash that is not 32 bytes for `ecrecover`, raises. Both release the GIL
while they run, and so does `keccak256` for inputs of 2048 bytes or more. `keccak256` hashes
the raw bytes of `bytes` or of any C-contiguous buffer, like `hashlib`.

The package is not meant to be used directly. safe-eth-py requires it, so it is installed with
it:

```bash
pip install safe-eth-py
```

## Usage

The extension is meant to be used through safe-eth-py, but the functions can also be called
directly:

```python
import hashlib

import safe_eth_native

# keccak256 of bytes, or of any C-contiguous buffer (bytearray, memoryview...)
safe_eth_native.keccak256(b"").hex()
# 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
safe_eth_native.keccak256(bytearray(b"Transfer(address,address,uint256)")).hex()
# 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

# EIP-55 checksum address, from hex text in any case or from 20 bytes
safe_eth_native.to_checksum_address("0x5aaeb6053f3e94c9b9a09f33669435e7ef1beaed")
# '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed'
safe_eth_native.to_checksum_address(bytes.fromhex("5aaeb6053f3e94c9b9a09f33669435e7ef1beaed"))
# '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed'
safe_eth_native.is_checksum_address("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed")
# True
safe_eth_native.is_checksum_address("0x5aaeb6053f3e94c9b9a09f33669435e7ef1beaed")
# False
safe_eth_native.to_checksum_address("0x1234")
# ValueError: Expected 20 bytes or a 40 characters hex address

# ecrecover of a 65 bytes `r || s || v` signature over a 32 bytes hash
message_hash = bytes.fromhex("18c547e4f7b0f325ad1e56f57e26c745b09a3e503d86e00e5255ff7f715d3d1c")
signature = bytes.fromhex(
    "73b1693892219d736caba55bdb67216e485557ea6b6af75f37096c9aa6a5a75f"
    "eeb940b1d03b21e36b0e47e79769f095fe2ab855bd91e3a38756b7d75a9c4549"
    "1c"
)
r = int.from_bytes(signature[:32], "big")
s = int.from_bytes(signature[32:64], "big")
v = signature[64]
signer = safe_eth_native.ecrecover(message_hash, v, r, s)  # 20 bytes
safe_eth_native.to_checksum_address(signer)
# '0xa94f5374Fce5edBC8E2a8697C15331677e6EbF0B'
safe_eth_native.ecrecover(message_hash, 29, r, s)  # `v` must be 27 or 28
# None

# P-256 (passkey) signature over a sha256 digest, as the P256VERIFY precompile
message_hash = int.from_bytes(hashlib.sha256(b"sample").digest(), "big")
safe_eth_native.p256_verify(
    message_hash,
    0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716,  # r
    0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8,  # s
    0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6,  # public key x
    0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299,  # public key y
)
# True
```

## Wheels

Platforms: Linux (glibc 2.28+ and musl) x86_64 and aarch64, macOS x86_64 and arm64, and
Windows x86_64. For each one:

- One `abi3` wheel for CPython 3.11 and newer, 3.15 included
- One wheel per free-threaded CPython version, 3.14t and 3.15t, as `abi3` wheels do not load
  on free-threaded builds. The module runs without the GIL: importing it does not enable the
  GIL again

Other platforms and Python versions build from the sdist, which needs a Rust toolchain and a
C compiler.

## Development

From the root of the safe-eth-py repository, `uv sync --group dev --all-extras --frozen` builds the
extension and installs it in the safe-eth-py environment, and `pytest native/tests` runs
its tests. uv rebuilds it when a file in `src/` changes.

The tests compare every function with reference implementations (eth-keys, eth-utils,
pycryptodome) and run the vectors of the Keccak team,
Wycheproof, EIP-55, and the test suites of go-ethereum, eth-keys, eth-utils, coincurve and
libsecp256k1. See
[`tests/vectors`](https://github.com/safe-global/safe-eth-py/blob/main/native/tests/vectors/README.md)
for their sources. CI runs them on every wheel. The musl ones are tested in Alpine with
Python 3.14 only, so the free-threaded musl wheels are built but not tested.

## Releasing

Bump `version` in `Cargo.toml`, then push a `native-v<version>` tag on a commit of `main`. Push
only the tag: a GitHub release would also run the safe-eth-py release workflow, for nothing.
The `Native extension` workflow builds the wheels and the sdist and publishes them to PyPI
with the `PYPI_SAFE_ETH_NATIVE_TOKEN` repository secret.
