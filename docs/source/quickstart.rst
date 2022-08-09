Quick start
-----------

Just run ``pip install safe-eth-py`` or add it to your **requirements.txt**

If you want django ethereum utils (models, serializers, filters...) you need to run
``pip install safe-eth-py[django]``

If you have issues building **coincurve** maybe
`you are missing some libraries <https://ofek.dev/coincurve/install/#source>`_

Ethereum utils
--------------
gnosis.eth
~~~~~~~~~~
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

More optimal in case you want to call the same function in multiple contracts

.. code-block:: python

  from gnosis.eth import EthereumClient
  from gnosis.eth.contracts import get_erc20_contract
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  erc20_contract = get_erc20_contract(self.w3, token_address)
  my_account = '0xD0E03B027A367fED4fd0E7834a82CD8A73E76B45'
  name, symbol = ethereum_client.batch_call_same_function(
                      erc20_contract.functions.balanceOf(my_account),
                      ['0x6810e776880C02933D47DB1b9fc05908e5386b96', '0x6B175474E89094C44Da98b954EedeAC495271d0F']
                  )

If you want to use the underlying `web3.py <https://github.com/ethereum/web3.py>`_ library:

.. code-block:: python

  from gnosis.eth import EthereumClient
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  ethereum_client.w3.eth.get_block(57)


``EthereumClient`` supports `EIP1559 <https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md>`_ fees:

.. code-block:: python

  from gnosis.eth import TxSpeed
  base_fee, priority_fee = ethereum_client.estimate_fee_eip1559(tx_speed=TxSpeed.NORMAL)
  # If you want to convert a legacy tx to a EIP1559 one
  eip1559_tx = ethereum_client.set_eip1559_fees(legacy_tx, tx_speed=TxSpeed.NORMAL)


You can modify timeouts (in seconds) for the RPC endpoints by setting
`ETHEREUM_RPC_TIMEOUT` and `ETHEREUM_RPC_SLOW_TIMEOUT` as environment variables.

By default every RPC request will be retried `3` times. You can modify that by setting `ETHEREUM_RPC_RETRY_COUNT`.


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

Gnosis Products
---------------
Safe
~~~~
On ``gnosis.safe`` there're classes to work with `Gnosis Safe <https://safe.global/>`_

.. code-block:: python

  from gnosis.eth import EthereumClient
  from gnosis.safe import Safe
  safe_address = ''  # Fill with checksummed version of a Safe address
  ethereum_client = EthereumClient(ETHEREUM_NODE_URL)
  safe = Safe(safe_address, ethereum_client)
  safe_info = safe.retrieve_all_info()

To work with Multisig Transactions:

.. code-block:: python

  safe_tx = safe.build_multisig_tx(to, value, data, operation, safe_tx_gas, base_gas, gas_price, gas_token,
                                   refund_receiver, signatures, safe_nonce)
  safe_tx.sign(owner_1_private_key)
  safe_tx.sign(owner_2_private_key)
  safe_tx.call()  # Check it works
  safe_tx.execute(tx_sender_private_key)

Protocol
~~~~~~~~
On ``gnosis.protocol`` there're classes to work with `Gnosis Protocol v2 <https://docs.cowswap.app>`_

.. code-block:: python

  import time
  from gnosis.eth import EthereumNetwork
  from gnosis.protocol import Order, OrderKind, GnosisProtocolAPI

  account_address = ''  # Fill with checksummed version of a Gnosis Protocol user address
  account_private_key = ''  # Fill with private key of a user address
  gnosis_protocol_api = GnosisProtocolAPI(EthereumNetwork.RINKEBY)
  print(gnosis_protocol_api.get_trades(owner=account_address))
  buy_amount = gnosis_protocol_api.get_estimated_amount(base_token, quote_token, OrderKind.SELL, sell_amount)
  valid_to = int(time.time() + (24 * 60 * 60))  # Order valid for 1 day
  order = Order(
        sellToken=base_token,
        buyToken=buyToken,
        receiver=receiver,
        sellAmount=sell_amount,
        buyAmount=buy_amount,
        validTo=valid_to,  # timestamp
        appData=ipfs_hash,  # IPFS hash for metadata
        fee_amount=0,  # If set to `0` it will be autodetected
        kind='sell',  # `sell` or `buy`
        partiallyFillable=True,  # `True` or `False`
        sellTokenBalance='erc20',  # `erc20`, `external` or `internal`
        buyTokenBalance='erc20',  # `erc20` or `internal`
    )
  gnosis_protocol_api.place_order(order, account_private_key)
