Safe-eth-py (previously known as Gnosis-py)
###########################################

.. class:: no-web no-pdf

|ci| |coveralls| |python| |django| |pipy| |readthedocs| |black|

Safe-eth-py includes a set of libraries to work with Ethereum and relevant Ethereum projects:
  - `EthereumClient`, a wrapper over Web3.py `Web3` client including utilities to deal with ERC20/721
    tokens and tracing.
  - `Gnosis Safe <https://github.com/safe-global/safe-contracts>`_ classes and utilities.
  - Price oracles for `Uniswap`, `Kyber`...
  - Django serializers, models and utils.

Quick start
-----------

Just run ``pip install safe-eth-py`` or add it to your **requirements.txt**

If you want django ethereum utils (models, serializers, filters...) you need to run
``pip install safe-eth-py[django]``

If you have issues building **coincurve** maybe
`you are missing some libraries <https://ofek.dev/coincurve/install/#source>`_


Contributing to safe-eth-py
---------------------------
Clone the repo, then to set it up:

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements-dev.txt
    pre-commit install -f

Ethereum utils
--------------
gnosis.eth
~~~~~~~~~~~~~~~~~~~~
- ``class EthereumClient (ethereum_node_url: str)``: Class to connect and do operations
  with an ethereum node. Uses web3 and raw rpc calls for things not supported in web3.
  Only ``http/https`` urls are supported for the node url.

``EthereumClient`` has some utils that improve a lot performance using Ethereum nodes, like
the possibility of doing ``batch_calls`` (a single request making read-only calls to multiple contracts):

.. code-block:: python

  from gnosis.eth import EthereumClient
  from gnosis.eth.contracts import get_erc721_contract
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  erc721_contract = get_erc721_contract(self.w3, token_address)
  name, symbol = ethereum_client.batch_call([
                      erc721_contract.functions.name(),
                      erc721_contract.functions.symbol(),
                  ])

If you want to use the underlying `web3.py <https://github.com/ethereum/web3.py>`_ library:

.. code-block:: python

  from gnosis.eth import EthereumClient
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  ethereum_client.w3.eth.get_block(57)


gnosis.eth.constants
~~~~~~~~~~~~~~~~~~~~
- ``NULL_ADDRESS (0x000...0)``: Solidity ``address(0)``.
- ``SENTINEL_ADDRESS (0x000...1)``: Used for Gnosis Safe's linked lists (modules, owners...).
- Maximum and minimum values for `R`, `S` and `V` in ethereum signatures.

gnosis.eth.oracles
~~~~~~~~~~~~~~~~~~

Price oracles for Uniswap, UniswapV2, Kyber, SushiSwap, Aave, Balancer, Curve, Mooniswap, Yearn...
Example:

.. code-block:: python

  from gnosis.eth import EthereumClient
  from gnosis.eth.oracles import UniswapV2Oracle
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  uniswap_oracle = UniswapV2Oracle(ethereum_client)
  gno_token_mainnet_address = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
  weth_token_mainnet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
  price = uniswap_oracle.get_price(gno_token_mainnet_address, uniswap_oracle.weth_address)



gnosis.eth.utils
~~~~~~~~~~~~~~~~

Contains utils for ethereum operations:

- ``get_eth_address_with_key() -> Tuple[str, bytes]``: Returns a tuple of a valid public ethereum checksumed
  address with the private key.
- ``mk_contract_address_2(from_: Union[str, bytes], salt: Union[str, bytes], init_code: [str, bytes]) -> str``:
  Calculates the address of a new contract created using the new CREATE2 opcode.

Ethereum django (REST) utils
----------------------------
Django utils are available under ``gnosis.eth.django``.
You can find a set of helpers for working with Ethereum using Django and Django Rest framework.

It includes:

- **gnosis.eth.django.filters**: EthereumAddressFilter.
- **gnosis.eth.django.models**: Model fields (Ethereum address, Ethereum big integer field).
- **gnosis.eth.django.serializers**: Serializer fields (Ethereum address field, hexadecimal field).
- **gnosis.eth.django.validators**: Ethereum related validators.
- **gnosis.safe.serializers**: Serializers for Gnosis Safe (signature, transaction...).
- All the tests are written using Django Test suite.

Contributors
------------
`See contributors <https://github.com/safe-global/safe-eth-py/graphs/contributors>`_

.. |ci| image:: https://github.com/safe-global/safe-eth-py/workflows/Python%20CI/badge.svg?branch=master
    :alt: Github Actions CI build

.. |coveralls| image:: https://coveralls.io/repos/github/safe-global/safe-eth-py/badge.svg?branch=master
    :target: https://coveralls.io/github/safe-global/safe-eth-py?branch=master
    :alt: Coveralls

.. |python| image:: https://img.shields.io/badge/Python-3.9-blue.svg
    :alt: Python 3.9

.. |django| image:: https://img.shields.io/badge/Django-2-blue.svg
    :alt: Django 2.2

.. |pipy| image:: https://badge.fury.io/py/safe-eth-py.svg
    :target: https://badge.fury.io/py/safe-eth-py
    :alt: Pypi package

.. |readthedocs| image:: https://readthedocs.org/projects/safe-eth-py/badge/?version=latest
    :target: https://safe-eth-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
