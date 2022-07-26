from .base import *  # noqa

INSTALLED_APPS += ("gnosis.eth.django.tests",)  # noqa

SECRET_KEY = "testtest"
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}

ETHEREUM_NODE_URL = "http://localhost:8545"
ETHEREUM_TEST_PRIVATE_KEY = "b0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773"  # Ganache account 9

# Ganache fixed seed keys (run ganache with -d)
SAFE_FUNDER_PRIVATE_KEY = (
    "4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"  # Ganache 0
)
SAFE_TX_SENDER_PRIVATE_KEY = (
    "6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"  # Ganache 1
)
SAFE_FUNDER_MAX_ETH = 0.1
SAFE_FUNDING_CONFIRMATIONS = 0
SAFE_GAS_PRICE = 1
SAFE_CONTRACT_ADDRESS = "0xaE32496491b53841efb51829d6f886387708F99B"
SAFE_V1_0_0_CONTRACT_ADDRESS = "0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A"
SAFE_V0_0_1_CONTRACT_ADDRESS = "0x8942595A2dC5181Df0465AF0D7be08c8f23C93af"
SAFE_PROXY_FACTORY_ADDRESS = "0x50e55Af101C777bA7A1d560a774A82eF002ced9F"
SAFE_VALID_CONTRACT_ADDRESSES = [SAFE_CONTRACT_ADDRESS]
