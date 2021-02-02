Gnosis-py
############################

.. class:: no-web no-pdf

|ci| |coveralls| |python| |django| |pipy|

Gnosis-py includes a set of libraries to work with Ethereum and Gnosis projects:
- `EthereumClient`, a wrapper over Web3.py `Web3` client including utilities to deal with ERC20/721
  tokens and tracing.
- `Gnosis Safe <https://github.com/gnosis/safe-contracts>`_ classes and utilities.
- Price oracles for `Uniswap`, `Kyber`...
- Django serializers, models and utils.

Quick start
-----------

Just run ``pip install gnosis-py`` or add it to your **requirements.txt**

If you have issues building **coincurve** maybe
`you are missing some libraries <https://github.com/ofek/coincurve#installation>`_

Ethereum utils
--------------
gnosis.eth
~~~~~~~~~~~~~~~~~~~~
- ``class EthereumClient (ethereum_node_url: str)``: Class to connect and do operations
  with a ethereum node. Uses web3 and raw rpc calls for things not supported in web3.
  Only ``http/https`` urls are suppored for the node url.

gnosis.eth.constants
~~~~~~~~~~~~~~~~~~~~
- ``NULL_ADDRESS (0x000...0)``
- ``SENTINEL_ADDRESS (0x000...1)``
- Maximum an minimum values for `R`, `S` and `V` in ethereum signatures

gnosis.eth.utils
~~~~~~~~~~~~~~~~

Contains utils for ethereum operations:

- ``get_eth_address_with_key() -> Tuple[str, bytes]``: Returns a tuple of a valid public ethereum checksumed
  address with the private key.
- ``generate_address_2(from_: Union[str, bytes], salt: Union[str, bytes], init_code: [str, bytes]) -> str``:
  Calculates the address of a new contract created using the new CREATE2 opcode.

Ethereum django utils
---------------------
Now ``django-eth`` is part of this package, available under ``gnosis.eth.django``
You can find a set of helpers for working with Ethereum using Django and Django Rest framework.

It includes:

- Basic serializers (signature, transaction)
- Serializer fields (Ethereum address field, hexadecimal field)
- Model fields (Ethereum address, Ethereum big integer field)
- Utils for testing

Contributors
------------
- Denís Graña (denis@gnosis.pm)
- Giacomo Licari (giacomo.licari@gnosis.pm)
- Uxío Fuentefría (uxio@gnosis.pm)

.. |ci| image:: https://github.com/gnosis/gnosis-py/workflows/Python%20CI/badge.svg?branch=master
    :alt: Github Actions CI build

.. |coveralls| image:: https://coveralls.io/repos/github/gnosis/gnosis-py/badge.svg?branch=master
    :target: https://coveralls.io/github/gnosis/gnosis-py?branch=master
    :alt: Coveralls

.. |python| image:: https://img.shields.io/badge/Python-3.6-blue.svg
    :alt: Python 3.7

.. |django| image:: https://img.shields.io/badge/Django-2-blue.svg
    :alt: Django 2.2

.. |pipy| image:: https://badge.fury.io/py/gnosis-py.svg
    :target: https://badge.fury.io/py/gnosis-py
    :alt: Pypi package
