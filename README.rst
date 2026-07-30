Safe-eth-py (previously known as Gnosis-py)
###########################################

.. class:: no-web no-pdf

|ci| |coveralls| |python| |django| |pipy| |readthedocs| |black|

Safe-eth-py includes a set of libraries to work with Ethereum and relevant Ethereum projects:
  - `EthereumClient`, a wrapper over Web3.py `Web3` client including utilities to deal with ERC20/721
    tokens and tracing.
  - `Safe <https://github.com/safe-global/safe-smart-account>`_ classes and utilities.
  - Price oracles for `Uniswap`, `Kyber`...
  - Django serializers, models and utils.

Quick start
-----------

Just run ``uv add safe-eth-py``

If you want django ethereum utils (models, serializers, filters...) you need to run
``uv add safe-eth-py[django]``

If you have issues building **coincurve** maybe
`you are missing some libraries <https://ofek.dev/coincurve/install/#source>`_


Contributing to safe-eth-py
---------------------------
Clone the repo, then to set it up:

.. code-block:: bash

    uv sync --group dev --frozen
    source .venv/bin/activate
    pre-commit install -f

Add new address for new chains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to add Safe Smart Account support for a new chain you must `open a new issue <https://github.com/safe-global/safe-eth-py/issues/new?assignees=&labels=add-new-address&projects=&template=add_safe_address_new_chain.yml&title=%5BNew+chain%5D%3A+%7Bchain+name%7D>`_.

Once the issue is created or edited, an automatic validation will be executed and a **Pull Request** will be created if everything is ok. Finally, the Safe team will review and merge the automatic **Pull Request** generated from the issue.

Ethereum utils
--------------
safe_eth.eth
~~~~~~~~~~~~
- ``class EthereumClient (ethereum_node_url: str)``: Class to connect and do operations
  with an ethereum node. Uses web3 and raw rpc calls for things not supported in web3.
  Only ``http/https`` urls are supported for the node url.

``EthereumClient`` has some utils that improve a lot performance using Ethereum nodes, like
the possibility of doing ``batch_calls`` (a single request making read-only calls to multiple contracts):

.. code-block:: python

  from safe_eth.eth import EthereumClient
  from safe_eth.eth.contracts import get_erc721_contract
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  erc721_contract = get_erc721_contract(self.w3, token_address)
  name, symbol = ethereum_client.batch_call([
                      erc721_contract.functions.name(),
                      erc721_contract.functions.symbol(),
                  ])

If you want to use the underlying `web3.py <https://github.com/ethereum/web3.py>`_ library:

.. code-block:: python

  from safe_eth.eth import EthereumClient
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  ethereum_client.w3.eth.get_block(57)


safe_eth.eth.constants
~~~~~~~~~~~~~~~~~~~~~~
- ``NULL_ADDRESS (0x000...0)``: Solidity ``address(0)``.
- ``SENTINEL_ADDRESS (0x000...1)``: Used for Safe's linked lists (modules, owners...).
- Maximum and minimum values for `R`, `S` and `V` in ethereum signatures.

safe_eth.eth.oracles
~~~~~~~~~~~~~~~~~~~~
Price oracles for Uniswap, UniswapV2, Kyber, SushiSwap, Aave, Balancer, Curve, Mooniswap, Yearn...
Example:

.. code-block:: python

  from safe_eth.eth import EthereumClient
  from safe_eth.eth.oracles import UniswapV2Oracle
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  uniswap_oracle = UniswapV2Oracle(ethereum_client)
  gno_token_mainnet_address = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
  weth_token_mainnet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
  price = uniswap_oracle.get_price(gno_token_mainnet_address, uniswap_oracle.weth_address)



safe_eth.eth.utils
~~~~~~~~~~~~~~~~~~

Contains utils for ethereum operations:

- ``mk_contract_address_2(from_: Union[str, bytes], salt: Union[str, bytes], init_code: [str, bytes]) -> str``:
  Calculates the address of a new contract created using the new CREATE2 opcode.

Ethereum django (REST) utils
----------------------------
Django utils are available under ``safe_eth.eth.django``.
You can find a set of helpers for working with Ethereum using Django and Django Rest framework.

It includes:

- **safe_eth.eth.django.filters**: EthereumAddressFilter.
- **safe_eth.eth.django.models**: Model fields (Ethereum address, Ethereum big integer field).
- **safe_eth.eth.django.serializers**: Serializer fields (Ethereum address field, hexadecimal field).
- **safe_eth.eth.django.validators**: Ethereum related validators.
- **safe_eth.safe.serializers**: Serializers for Safe (signature, transaction...).
- All the tests are written using Django Test suite.


Safe APIs
--------------
safe_eth.safe.api
~~~~~~~~~~~~~~~~~
Interaction with the Safe Transaction Service API to manage Safes, transactions, delegates, and messages.

To use the default Transaction Service, you need an API key. You can set this API key either as an environment variable
or pass it directly to the constructor using the `api_key` parameter. To obtain your API key, create an account on the
Safe Developer Portal at https://developer.safe.global. Additionally, you can choose to use a custom service by setting
the `base_url` parameter, the API key may not be required.

.. code-block:: bash

 export SAFE_TRANSACTION_SERVICE_API_KEY=[api-key-jwt-token-value]

Example:

.. code-block:: python

    from safe_eth.eth import EthereumNetwork
    from safe_eth.safe.api import TransactionServiceApi

    transaction_service_api = TransactionServiceApi(EthereumNetwork.GNOSIS)
    transactions = transaction_service_api.get_transactions("0xAedF684C1c41B51CbD228116e11484425d2FACB9")

Environment variables
----------------------
Behaviour can be tuned with the following environment variables. All of them are optional and
fall back to the defaults shown below.

Ethereum RPC client
~~~~~~~~~~~~~~~~~~~~~
These are read when the module-level ``EthereumClient`` singleton (``safe_eth.eth.ethereum_client``
and its async counterpart) is instantiated.

- ``ETHEREUM_NODE_URL``: RPC node url used by the default ``EthereumClient`` singleton. No default
  (the singleton is not usable until it is set). **In a Django application this variable is
  ignored**: ``get_auto_ethereum_client`` / ``get_auto_async_ethereum_client`` read
  ``settings.ETHEREUM_NODE_URL`` instead, and that setting is required. The environment variable is
  only used as a fallback when Django is not installed.
- ``ETHEREUM_RPC_TIMEOUT``: Timeout (seconds) for regular RPC calls. Default ``10``.
- ``ETHEREUM_RPC_SLOW_TIMEOUT``: Timeout (seconds) for slow RPC calls (e.g. tracing). Default ``60``.
- ``ETHEREUM_RPC_RETRY_COUNT``: Number of retries for RPC calls. Default ``1``.
- ``ETHEREUM_RPC_BATCH_REQUEST_MAX_SIZE``: Maximum number of calls bundled in a single batch
  request. Default ``500``.

Caching
~~~~~~~
- ``CACHE_KECCAK``: ``lru_cache`` max size for keccak256 hashing. Default ``1024``.
- ``CACHE_CHECKSUM_ADDRESS``: ``lru_cache`` max size for checksummed address conversion. Default ``500000``.

Safe contract addresses
~~~~~~~~~~~~~~~~~~~~~~~~~
Override the default deterministic contract addresses (useful on chains where they were deployed
to a different address).

- ``SAFE_SINGLETON_FACTORY_ADDRESS``: `Safe singleton factory <https://github.com/safe-global/safe-singleton-factory>`_
  address. Default ``0x914d7Fec6aaC8cd542e72Bca78B30650d45643d7``.
- ``SAFE_SIMULATE_TX_ACCESSOR_ADDRESS``: ``SimulateTxAccessor`` contract address. Default
  ``0x3d4BA2E0884aa488718476ca2FB8Efc291A46199``.

Safe Transaction Service API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- ``SAFE_TRANSACTION_SERVICE_API_KEY``: API key (JWT) for the default Transaction Service. See
  `Safe APIs`_ above. No default.
- ``SAFE_TRANSACTION_SERVICE_REQUEST_TIMEOUT``: Request timeout (seconds). Default ``10``.

Block explorer and source verification clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``*_MAX_REQUESTS`` variables tune the connection pool of the async clients only; the
synchronous Etherscan and Blockscout clients do not pool connections and ignore them.

- ``ETHERSCAN_CLIENT_REQUEST_TIMEOUT``: Request timeout (seconds). Default ``10``.
- ``ETHERSCAN_CLIENT_MAX_REQUESTS``: Max pool size of concurrent requests (``AsyncEtherscanClientV2``
  only). Default ``100``.
- ``BLOCKSCOUT_CLIENT_REQUEST_TIMEOUT``: Request timeout (seconds). Default ``10``.
- ``BLOCKSCOUT_CLIENT_MAX_REQUESTS``: Max pool size of concurrent requests (``AsyncBlockscoutClient``
  only). Default ``100``.
- ``SOURCIFY_BASE_URL_API``: Sourcify API base url. Default ``https://sourcify.dev``.
- ``SOURCIFY_CLIENT_REQUEST_TIMEOUT``: Request timeout (seconds). Default ``10``.
- ``SOURCIFY_CLIENT_MAX_REQUESTS``: Max pool size of concurrent requests. Default ``100``.
- ``ENS_CLIENT_REQUEST_TIMEOUT``: ENS client request timeout (seconds). Default ``5``.

Contributors
------------
`See contributors <https://github.com/safe-global/safe-eth-py/graphs/contributors>`_

.. |ci| image:: https://github.com/safe-global/safe-eth-py/actions/workflows/python.yml/badge.svg
    :alt: Github Actions CI build

.. |coveralls| image:: https://coveralls.io/repos/github/safe-global/safe-eth-py/badge.svg
    :target: https://coveralls.io/github/safe-global/safe-eth-py

.. |python| image:: https://img.shields.io/badge/Python-3.13-blue.svg
    :alt: Python 3.13

.. |django| image:: https://img.shields.io/badge/Django-5-blue.svg
    :alt: Django 5

.. |pipy| image:: https://badge.fury.io/py/safe-eth-py.svg
    :target: https://badge.fury.io/py/safe-eth-py
    :alt: Pypi package

.. |readthedocs| image:: https://readthedocs.org/projects/safe-eth-py/badge/?version=latest
    :target: https://safe-eth-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
