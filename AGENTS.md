# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`safe-eth-py` is a Python library (published to PyPI as `safe-eth-py`, previously `gnosis-py`), not a
service. It provides `EthereumClient`, a wrapper over `web3.py` with ERC20/ERC721/tracing/batching
helpers, the `Safe` contract classes and Safe transaction/signature handling, price oracles, clients
for external services (Etherscan, Blockscout, Sourcify, ENS, CowSwap, Safe Transaction Service) and
an optional Django layer.

It is a shared dependency of the Safe Python backends, so any public API change ripples into
`safe-transaction-service`, `safe-queue-service`, `safe-auth-service`, `safe-decoder-service` and
`safe-cli`. Check the consumers before renaming or changing the signature of anything exported.

## Team and Project Context

- **Team**: Platform
- **Repository**: `safe-global/safe-eth-py`

### Linear Guidelines

- Create issues under team **Platform** with the `eth-py` and `Backend` labels
- Use `add-new-address` for new chain address issues (that flow is automated, see below)
- Add PR links as issue attachments/links
- Branches follow the Linear name: `uxio/pla-<number>-<slug>`. Plain `feat/<scope>`, `fix/<scope>`,
  `chore/<scope>` branches are also used for work without an issue

## Development Setup

### Initial Setup
```bash
uv sync --group dev --all-extras --frozen
source .venv/bin/activate
pre-commit install -f
```

`--all-extras` pulls the `django` extra, which the test suite needs. `uv.lock` is the source of
truth: always sync `--frozen`, run `uv lock` after editing `pyproject.toml` and commit both.
`[tool.uv] exclude-newer = "7 days"` rejects packages published in the last 7 days, so a brand new
release cannot be locked yet.

### Running Tests

Tests need Postgres (Django test database) and a ganache node on `localhost:8545` started with the
fixed mnemonic (`-d`), because the test mixins deploy Safe and Multicall contracts on it:

```bash
docker compose up -d db ganache

# Run all tests
pytest

# Run a single test file
pytest safe_eth/safe/tests/test_safe.py

# Run a specific test
pytest safe_eth/safe/tests/test_safe.py::TestSafe::test_estimate_tx_gas

# Run with coverage
coverage run --source=safe_eth -m pytest -rxXs
coverage report

# compose up + pytest + compose down
./run_tests.sh
```

`DJANGO_SETTINGS_MODULE=config.settings.test` is set automatically by `pytest-env`
(`[tool.pytest_env]` in `pyproject.toml`), so plain `pytest` works. The `config/` package exists only
to run the Django part of the suite and is not shipped in the wheel.

### Linting and Type Checking
```bash
pre-commit run --all-files   # isort, black, flake8, mypy — this is what CI runs
mypy safe_eth
```

### Building the Docs
```bash
./build_docs.sh   # sphinx-apidoc + make html, output in docs/build
```

## Architecture

### `safe_eth.eth` — node access

`EthereumClient` wraps `web3.py` and composes domain managers, all built in its `__init__`:

- `.erc20` (`Erc20Manager`), `.erc721` (`Erc721Manager`), `.tracing` (`TracingManager`),
  `.batch_call_manager` (`BatchCallManager`) — all subclasses of `EthereumClientManager`
- `.multicall` (`Multicall`), deployed per chain or from `safe_eth/eth/multicall.py` addresses

New node-level features belong in a manager, not on the client itself. `async_ethereum_client.py`
mirrors the sync client for async callers; a feature added to one usually has to be added to both.

Performance rules that hold across the codebase:
- Prefer `batch_call` / multicall over N sequential RPC calls
- Prefer `fast_to_checksum_address` / `fast_is_checksum_address` / `fast_keccak`
  (`safe_eth/eth/utils.py`, pysha3-backed and `lru_cache`d) over the `Web3` equivalents

### Contracts are loaded from bundled ABIs

`safe_eth/eth/contracts/__init__.py` holds a `contracts` dict mapping a name to a JSON file under
`abis/`, and generates the `get_<name>_contract(w3, address)` functions dynamically with `setattr` at
import time. The module also declares typed stubs for those generated functions so mypy sees them.
Deployed-bytecode getters (`get_proxy_1_3_0_deployed_bytecode`, …) are `@cache`d and written by hand.

### `safe_eth.safe` — Safe protocol logic

`Safe.__new__` is a factory: `Safe(address, ethereum_client)` detects the deployed version over RPC
(or takes `version=` to skip the lookup) and returns the matching subclass from `_version_class_map()`
— `SafeV001`, `SafeV100`, `SafeV111`, `SafeV120`, `SafeV130`, `SafeV141`, `SafeV150`. Version specific
behaviour goes in the subclass, shared behaviour in `Safe`, and `SafeCompatibilityAdapter` holds what
1.4.1 and 1.5.0 share. `proxy_factory.py` and `compatibility_fallback_handler.py` use the same
version-subclass pattern.

Every contract wrapper extends `ContractBase` (`safe_eth/eth/contracts/contract_base.py`), which
requires a `get_contract_fn()` returning one of the generated contract getters and exposes a
`cached_property contract`.

Other core modules:
- `safe_tx.py`: builds, hashes (EIP-712) and signs Safe transactions
- `safe_signature.py`: parses the packed signature blob into `SafeSignature` / `SafeSignatureAsync`
  objects by `SafeSignatureType` (EOA, ETH_SIGN, APPROVED_HASH, CONTRACT_SIGNATURE/EIP-1271, SECP256R1)
- `multi_send.py`, `safe_create2_tx.py`, `safe_creator.py`, `p256.py`
- `account_abstraction/safe_operation.py` on top of `safe_eth/eth/account_abstraction/` (ERC-4337
  user operations and bundler client)

### External service clients

`safe_eth/eth/clients/` (Etherscan v2, Blockscout, Sourcify, ENS, CowSwap) and `safe_eth/safe/api/`
(Transaction Service API on `base_api.py`). Several have both sync and async variants. `oracles/`
holds the price oracles (Uniswap v2/v3, Kyber, SushiSwap, Curve, Superfluid…).

### Optional Django layer

`safe_eth/eth/django/` (model fields, serializers, filters, validators, forms) and
`safe_eth/safe/serializers.py` are only importable with the `django` extra. Keep Django imports out
of the core modules. Where a value can come from Django settings or the environment, Django settings
win when Django is installed — see `get_auto_ethereum_client` and
`EthereumTestCaseMixin.get_ethereum_test_account`.

### Generated data files — do not hand-edit

- `safe_eth/safe/safe_deployments.py`: generated from the `safe-deployments` repo by
  `scripts/generators/generate_safe_deployments.py`
- `safe_eth/eth/ethereum_network.py` (the `EthereumNetwork` enum, ~2000 chains) and the multicall
  addresses: `scripts/generators/generate_chains_list.py` and `generate_chains_info_from_viem.py`
- `safe_eth/safe/addresses.py`: per chain, `MASTER_COPIES` as `(address, deployment block, version)`
  and `PROXY_FACTORIES` as `(address, deployment block)`. Updated by the add-new-address workflow

## Configuration

The library reads everything from environment variables, all optional. `README.rst` has the canonical
list with defaults; the groups are:

- **RPC client**: `ETHEREUM_NODE_URL` (ignored under Django, which uses `settings.ETHEREUM_NODE_URL`),
  `ETHEREUM_RPC_TIMEOUT`, `ETHEREUM_RPC_SLOW_TIMEOUT`, `ETHEREUM_RPC_RETRY_COUNT`,
  `ETHEREUM_RPC_BATCH_REQUEST_MAX_SIZE`
- **Caching**: `CACHE_KECCAK`, `CACHE_CHECKSUM_ADDRESS` (`lru_cache` sizes for the fast helpers)
- **Contract addresses**: `SAFE_SINGLETON_FACTORY_ADDRESS`, `SAFE_SIMULATE_TX_ACCESSOR_ADDRESS`, for
  chains where the deterministic address differs
- **Transaction Service**: `SAFE_TRANSACTION_SERVICE_API_KEY` (JWT from developer.safe.global),
  `SAFE_TRANSACTION_SERVICE_REQUEST_TIMEOUT`
- **Block explorer / source clients**: `ETHERSCAN_CLIENT_*`, `BLOCKSCOUT_CLIENT_*`, `SOURCIFY_*`,
  `ENS_CLIENT_REQUEST_TIMEOUT`. `ETHERSCAN_CLIENT_MAX_REQUESTS` and `BLOCKSCOUT_CLIENT_MAX_REQUESTS`
  only tune the async clients' pools. `SOURCIFY_CLIENT_MAX_REQUESTS` applies to both: the sync
  `SourcifyClient` passes it to `prepare_http_session` as `pool_maxsize`

Anything new added here must be documented in `README.rst`.

## Testing Strategy

Tests live next to the code they cover, in `tests/` packages inside each module
(`safe_eth/eth/tests/`, `safe_eth/safe/tests/`, `safe_eth/util/tests/`).

Base classes:
- `EthereumTestCaseMixin` (`safe_eth/eth/tests/ethereum_test_case.py`): sets up `ethereum_client`,
  `w3`, a funded `ethereum_test_account` and deploys Multicall. The client is cached across test
  classes, so do not mutate it
- `SafeTestCaseMixin` (`safe_eth/safe/tests/safe_test_case.py`): adds deployed singletons for Safe
  0.0.1, 1.0.0, 1.1.1, 1.3.0, 1.4.1 and 1.5.0, the 1.4.1 and 1.5.0 proxy factories, MultiSend and the
  fallback handlers, plus `deploy_test_safe*` helpers. `SafeV120` exists in `_version_class_map()`
  but has no fixture: 1.2.0 shipped with a bug, was replaced by 1.3.0 and never used in production

Conventions:
- Tests are `unittest`-style `TestCase` classes run under pytest, not bare pytest functions
- The async client tests (`test_async_ethereum_client.py`) subclass the sync test classes and swap in
  a proxy that drives the coroutines, so a sync test added there is covered on both clients
- Tests hitting a real network call `just_test_if_mainnet_node()` / `just_test_if_polygon_node()`
  (`safe_eth/eth/tests/utils.py`). An unset `ETHEREUM_MAINNET_NODE` / `ETHEREUM_POLYGON_NODE`
  `pytest.skip`s the module. A variable that is set but points at an unreachable node `pytest.fail`s,
  on a bad response or an `IOError`. Never make a test fail because a node is missing
- Other optional CI keys: `ETHEREUM_4337_BUNDLER_URL`, `ETHERSCAN_API_KEY`, `ENS_CLIENT_API_KEY`,
  `SAFE_TRANSACTION_SERVICE_API_KEY`
- Recorded API responses go in the `mocks/` package of the module being tested
- CI reruns failures 3 times (`--reruns 3 --reruns-delay 10`); network flakiness is expected
- All imports at the top of the file, never inside test functions

## Common Development Tasks

### GitHub Flow (Branching and PRs)

- Branch from `main` for every change, in a dedicated worktree
- Keep commits focused and atomic; commit subjects use `feat:`, `fix:`, `chore:` prefixes
- Open PRs against `main`; label with `breaking_change` or `dependencies` when relevant, since
  `.github/release.yml` builds the changelog from labels
- Link the PR to the Linear issue (Platform / `eth-py`)

### Adding a Contract ABI

1. Drop the compiled JSON (with `abi`, and `bytecode` if it will be deployed) in
   `safe_eth/eth/contracts/abis/`
2. Add the entry to the `contracts` dict in `safe_eth/eth/contracts/__init__.py`
3. Add the typed stub declaration for the generated `get_<name>_contract` so mypy sees it

### Supporting a New Safe Version

1. Add the ABI as above
2. Add the `SafeV<version>` subclass in `safe_eth/safe/safe.py` with its `get_contract_fn()`, and
   register it in `_version_class_map()`; update `_DEFAULT_VERSION` if it becomes the default
3. Do the same for `ProxyFactory` and the fallback handler when the version changes them
4. Deploy the new singleton in `SafeTestCaseMixin` and extend the version-specific test modules

### Adding Chain Addresses

Do not edit `safe_eth/safe/addresses.py` by hand. Users open an issue from the
`add_safe_address_new_chain.yml` template;
`.github/workflows/validate_new_address_issue_input_data.yml` validates the input and
`create_pr_with_new_address.yml` opens the PR, which the team reviews and merges.

### Updating Safe Deployments

Run `python scripts/generators/generate_safe_deployments.py` (clones `safe-deployments`, rewrites
`safe_eth/safe/safe_deployments.py`) and commit the regenerated file.

### Releasing

Bump `VERSION` in `safe_eth/__init__.py` in its own PR (hatch reads it as the package version), then
publish a GitHub release. The `publish` job in `.github/workflows/python.yml` runs `uv build` and
`uv publish` on the `released` event.

## Python Version

Supported: **3.10 to 3.13** (CI matrix). mypy targets 3.13. Do not use syntax or stdlib APIs newer
than 3.10.

## Code Quality Standards

- **Type hints required**: all functions must have complete annotations. The package ships `py.typed`
  and mypy runs over `safe_eth` in pre-commit with `check_untyped_defs`, `warn_unused_ignores`,
  `warn_redundant_casts`
- **reST style docstrings**: `:param x:` / `:return:`, matching the surrounding code and Sphinx
- **Formatting**: black and isort (profile `black`, with the custom section order
  `FUTURE, STDLIB, DJANGO, THIRDPARTY, SAFE_FOUNDATION, FIRSTPARTY, LOCALFOLDER`), flake8 with
  line length 88 (`E501` ignored, black decides)
- **Web3 types**: use `ChecksumAddress`, `HexBytes`, `HexStr` and the `web3.types` aliases instead of
  raw `str`/`bytes` for blockchain data
- **Exceptions**: raise the library's own exceptions from `safe_eth/eth/exceptions.py` and
  `safe_eth/safe/exceptions.py`; do not leak `web3`/`requests` exceptions to callers
- **Descriptive variable names in loops and comprehensions**: `for address in addresses`, not
  `for addr in addresses` or `for a in addrs`
- Update `README.rst` when adding a public feature or an environment variable

## Architectural Decisions and Design Rationale

### Version Dispatch in `Safe.__new__` Instead of `if version ==` Branches

**Decision**: `Safe(address, ethereum_client)` returns a version-specific subclass, chosen by a
factory in `__new__`.

**Rationale**:
- Safe contracts changed signatures across versions (1.0.0 to 1.5.0); branching inside each method
  would spread the version checks over the whole class
- Callers get one entry point and do not need to know the deployed version
- Passing `version=` skips the RPC lookup, which matters for the indexers calling this in a loop

**Implementation**: `_version_class_map()` maps the semantic version to the class,
`_default_version_class()` handles unknown versions.

### Sync and Async Clients Are Separate Implementations

**Decision**: `AsyncEthereumClient` mirrors `EthereumClient` rather than sharing a base with
sync/async variants of each method.

**Trade-off**: features must be added twice, but neither client pays for the other's abstraction, and
consumers that are fully sync (Django services) never import async machinery.

### Chain Data Is Generated, Not Fetched at Runtime

**Decision**: chain ids, multicall addresses and Safe deployment addresses are committed as Python
files generated from upstream sources, instead of being read from an API or JSON at runtime.

**Rationale**:
- The library must work offline and with no extra network call at import time
- The data is reviewable in the diff, so a wrong upstream address is caught in review
- Chain additions are frequent but mechanical, which is why they go through the issue-driven workflow
  instead of manual edits

### Fast Keccak and Checksum Helpers

**Decision**: `safe_eth/eth/utils.py` provides pysha3-backed, `lru_cache`d `fast_keccak`,
`fast_to_checksum_address` and `fast_is_checksum_address`, used everywhere instead of the `Web3`
equivalents.

**Rationale**: the indexers checksum millions of addresses; the cached implementation is
significantly faster, and the cache sizes are tunable with `CACHE_KECCAK` / `CACHE_CHECKSUM_ADDRESS`.
`safe_eth/eth/tests/test_keccak_performance.py` benchmarks it against `eth_utils` and `Web3` with
pytest-benchmark.

### Django Is an Optional Extra

**Decision**: Django code lives in dedicated modules behind the `django` extra, and the core never
imports Django at module level.

**Rationale**: `safe-cli` and library users install `safe-eth-py` without Django. Where both sources
exist, Django settings take precedence over environment variables, so a Django service configures
everything in one place.
