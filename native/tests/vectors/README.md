# Test vectors

Files are copied unchanged from their source.

| File | Source | License |
| --- | --- | --- |
| `keccak_256_short_msg_kat.txt` | `ShortMsgKAT_256.txt` of the Keccak team (original Keccak padding, the one Ethereum uses), as converted in [5afe/pysha3](https://github.com/5afe/pysha3/blob/0e64fdda072bf9adf6b2924f98c755c86291cb9a/vectors/keccak_256.txt) | Public domain (CC0) |
| `ecdsa_secp256k1_sha256_p1363_test.json`, `ecdsa_secp256k1_sha512_p1363_test.json`, `ecdsa_secp256r1_sha256_p1363_test.json`, `ecdsa_secp256r1_sha512_p1363_test.json` | [C2SP/wycheproof](https://github.com/C2SP/wycheproof/tree/65ca494727a52944c204441c860b039e6786b99b/testvectors_v1) | Apache License 2.0, copy in [`LICENSE-wycheproof`](LICENSE-wycheproof) |

`test_native_ecrecover.py` also has a few vectors inline, taken from:

| Vectors | Source | License |
| --- | --- | --- |
| `GETH_*`, unrecoverable key, `v` with high bits | [go-ethereum `ecRecover.json`](https://github.com/ethereum/go-ethereum/blob/a3cd8a040a4ffe04a7b455f11a6c049a9b29b1c5/core/vm/testdata/precompiles/ecRecover.json) | LGPL-3.0 |
| `ETH_KEYS_*`, point at infinity | [eth-keys tests](https://github.com/ethereum/eth-keys/tree/f6362996bf51aa65a081295df411a6e315940daf/tests/backends) | MIT |
| `COINCURVE_*` | [coincurve `tests/conftest.py`](https://github.com/ofek/coincurve/blob/2d11b1160c75ae8fd94fe8fe3f226aec176bf9bf/tests/conftest.py) | MIT or Apache-2.0 |
| `LIBSECP256K1_*`, (1, 1), (4, 4), (0, 1), (1, 0) | [libsecp256k1 recovery tests](https://github.com/bitcoin-core/secp256k1/blob/a1c2c87c90a7945044eca1b8d7469d323a00877e/src/modules/recovery/tests_impl.h) | MIT |
