from eth_account import Account
from eth_account.messages import encode_defunct
import requests
import json
from eip712_structs import make_domain
from eip712_structs import Address, Boolean, Bytes, String, Uint
from eip712_structs import EIP712Struct
from eth_typing import HexStr
from hexbytes import HexBytes

from gnosis.eth import EthereumNetwork, EthereumClient, EthereumNetworkNotSupported

try:
    from functools import cache
except ImportError:
    from functools import lru_cache
    cache = lru_cache(maxsize=None)


stablecoins = {
    "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83": 6,  # USDC
    "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d": 18,  # wxDAI
    "0x4ECaBa5870353805a9F068101A40E0f32ed605C6": 6,  # USDT
}

weth = '0xc778417E063141139Fce010982780140Aa0cD5Ab'
dai = '0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa'


class Order(EIP712Struct):
    sellToken = Address()
    buyToken = Address()
    receiver = Address()
    sellAmount = Uint(256)
    buyAmount = Uint(256)
    validTo = Uint(32)
    appData = Bytes(32)
    feeAmount = Uint(256)
    kind = String()  # `sell` or `buy`
    partiallyFillable = Boolean()
    sellTokenBalance = String()  # `erc20`, `external` or `internal`
    buyTokenBalance = String()  # `erc20` or `internal`


class GnosisProtocolAPI:
    settlement_contract_addresses = {
        EthereumNetwork.MAINNET: '0x9008D19f58AAbD9eD0D60971565AA8510560ab41',
        EthereumNetwork.RINKEBY: '0x9008D19f58AAbD9eD0D60971565AA8510560ab41',
        EthereumNetwork.XDAI: '0x9008D19f58AAbD9eD0D60971565AA8510560ab41',
    }

    api_base_urls = {
        EthereumNetwork.MAINNET: 'https://protocol-mainnet.gnosis.io/api/v1/',
        EthereumNetwork.RINKEBY: 'https://protocol-rinkeby.gnosis.io/api/v1/',
        EthereumNetwork.XDAI: 'https://protocol-xdai.gnosis.io/api/v1/',
    }

    def __init__(self, ethereum_client: EthereumClient):
        self.network = ethereum_client.get_network()
        if self.network not in self.api_base_urls:
            raise EthereumNetworkNotSupported(f'{self.network.name} network not supported by Gnosis Protocol')
        self.ethereum_client = ethereum_client
        self.w3 = ethereum_client.w3
        self.domain_separator = self.build_domain_separator(self.network)
        self.base_url = self.api_base_urls[self.network]

    @classmethod
    def build_domain_separator(cls, ethereum_network: EthereumNetwork):
        return make_domain(
            name='Gnosis Protocol',
            version='v2',
            chainId=str(ethereum_network.value),
            verifyingContract=cls.settlement_contract_addresses[ethereum_network]
        )

    def get_fee(self, order: Order) -> int:
        if order['kind'] == 'sell':
            amount = order['sellAmount']
        else:
            amount = order['buyAmount']
        url = self.base_url + f'fee?sellToken={order["sellToken"]}&buyToken={order["buyToken"]}' \
                              f'&amount={amount}&kind={order["kind"]}'
        result = requests.get(url).json()
        if 'amount' in result:
            return int(result['amount'])
        else:
            return 0

    def place_order(self, order: Order, private_key: HexStr) -> str:
        order['feeAmount'] = self.get_fee(order)
        signable_bytes = order.signable_bytes(self.domain_separator)
        signable_hash = self.w3.keccak(signable_bytes)
        message = encode_defunct(primitive=signable_hash)
        signed_message = self.w3.eth.account.sign_message(message, private_key=private_key)

        data_json = {
            'sellToken': order['sellToken'].lower(),
            'buyToken': order['buyToken'].lower(),
            'sellAmount': str(order['sellAmount']),
            'buyAmount': str(order['buyAmount']),
            'validTo': order['validTo'],
            'appData': HexBytes(order['appData']).hex() if isinstance(order['appData'], bytes) else order['appData'],
            'feeAmount': str(order['feeAmount']),
            'kind': order['kind'],
            'partiallyFillable': order['partiallyFillable'],
            'signature': signed_message.signature.hex(),
            'signingScheme': 'ethsign',
            'from': Account.from_key(private_key).address,
        }
        print(data_json)
        url = self.base_url + "orders"
        r = requests.post(url, json=data_json)
        if r.ok:
            return r.json()
        else:
            raise ValueError(f'Error placing order - {r.status_code} - {r.content}')

