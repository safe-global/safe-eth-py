Quick start
-----------

Just run ``pip install gnosis-py`` or add it to your **requirements.txt**

If you want django ethereum utils (models, serializers, filters...) you need to run
``pip install gnosis-py[django]``

If you have issues building **coincurve** maybe
`you are missing some libraries <https://ofek.dev/coincurve/install/#source>`_

Ethereum utils
--------------
gnosis.eth
~~~~~~~~~~~~~~~~~~~~
- ``class EthereumClient (ethereum_node_url: str)``: Class to connect and do operations
  with a ethereum node. Uses web3 and raw rpc calls for things not supported in web3.
  Only ``http/https`` urls are suppored for the node url.

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
- Maximum an minimum values for `R`, `S` and `V` in ethereum signatures.

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
- ``generate_address_2(from_: Union[str, bytes], salt: Union[str, bytes], init_code: [str, bytes]) -> str``:
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