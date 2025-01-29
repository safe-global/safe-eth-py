import os
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import aiohttp
import requests
from eth_typing import ChecksumAddress

from .. import EthereumNetwork
from .contract_metadata import ContractMetadata


class BlockscoutClientException(Exception):
    pass


class BlockScoutConfigurationProblem(BlockscoutClientException):
    pass


class BlockscoutClient:
    NETWORK_WITH_URL = {
        EthereumNetwork.ACALA_NETWORK: "https://blockscout.acala.network/api/v2/",
        EthereumNetwork.ALEPH_ZERO_EVM: "https://evm-explorer.alephzero.org/api/v2/",
        EthereumNetwork.ARBITRUM_BLUEBERRY: "https://arb-blueberry.gelatoscout.com/api/v2/",
        EthereumNetwork.ARTHERA_MAINNET: "https://explorer.arthera.net/api/v2/",
        EthereumNetwork.ARTHERA_TESTNET: "https://explorer-test.arthera.net/api/v2/",
        EthereumNetwork.ASTAR_ZKEVM: "https://astar-zkevm.explorer.startale.com/api/v2/",
        EthereumNetwork.AURORIA_TESTNET: "https://auroria.explorer.stratisevm.com/api/v2/",
        EthereumNetwork.BAHAMUT: "https://api.ftnscan.com/api/v2/",
        EthereumNetwork.BOB_SEPOLIA: "https://bob-sepolia.explorer.gobob.xyz/api/v2/",
        EthereumNetwork.BITROCK_TESTNET: "https://testnetscan.bit-rock.io/api/v2/",
        EthereumNetwork.CONNEXT_SEPOLIA: "https://scan.testnet.everclear.org/api/v2/",
        EthereumNetwork.DODOCHAIN_TESTNET: "https://testnet-scan.dodochain.com/api/v2/",
        EthereumNetwork.EVERCLEAR_MAINNET: "https://scan.everclear.org/api/v2/",
        EthereumNetwork.EVMOS: "https://evm.evmos.org/api/v2/",
        EthereumNetwork.ETHERLINK_MAINNET: "https://explorer.etherlink.com/api/v2/",
        EthereumNetwork.EXSAT_MAINNET: "https://scan.exsat.network/api/v2/",
        EthereumNetwork.EXSAT_TESTNET: "https://scan-testnet.exsat.network/api/v2/",
        EthereumNetwork.FLARE_MAINNET: "https://flare-explorer.flare.network/api/v2/",
        EthereumNetwork.FLARE_TESTNET_COSTON2: "https://coston2-explorer.flare.network/api/v2/",
        EthereumNetwork.GAME7: "https://mainnet.game7.io/api/v2/",
        EthereumNetwork.GAME7_TESTNET: "https://testnet.game7.io/api/v2/",
        EthereumNetwork.GNOSIS: "https://gnosis.blockscout.com/api/v2/",
        EthereumNetwork.GNOSIS_CHIADO_TESTNET: "https://gnosis-chiado.blockscout.com/api/v2/",
        EthereumNetwork.GPT_MAINNET: "https://explorer.gptprotocol.io/api/v2/",
        EthereumNetwork.HAQQ_CHAIN_TESTNET: "https://explorer.testedge2.haqq.network/api/v2/",
        EthereumNetwork.HAQQ_NETWORK: "https://explorer.haqq.network/api/v2/",
        EthereumNetwork.HASHKEY_CHAIN: "https://explorer.hsk.xyz/api/v2/",
        EthereumNetwork.HASHKEY_CHAIN_TESTNET: "https://hashkeychain-testnet-explorer.alt.technology/api/v2/",
        EthereumNetwork.IOTA_EVM: "https://iota-evm.blockscout.com/api/v2/",
        EthereumNetwork.INK_SEPOLIA: "https://explorer-sepolia.inkonchain.com/api/v2/",
        EthereumNetwork.JAPAN_OPEN_CHAIN_MAINNET: "https://mainnet.japanopenchain.org/api/v2/",
        EthereumNetwork.JAPAN_OPEN_CHAIN_TESTNET: "https://explorer.testnet.japanopenchain.org/api/v2/",
        EthereumNetwork.KAIA_KAIROS_TESTNET: "https://baobab.scope.klaytn.com/api/v2/",
        EthereumNetwork.KAIA_MAINNET: "https://scope.klaytn.com/api/v2/",
        EthereumNetwork.KROMA: "https://blockscout.kroma.network/api/v2/",
        EthereumNetwork.KROMA_SEPOLIA: "https://blockscout.sepolia.kroma.network/api/v2/",
        EthereumNetwork.LINEA: "https://api-explorer.linea.build/api/v2/",
        EthereumNetwork.LISK: "https://blockscout.lisk.com/api/v2/",
        EthereumNetwork.LISK_SEPOLIA_TESTNET: "https://sepolia-blockscout.lisk.com/api/v2/",
        EthereumNetwork.LORENZO: "https://scan.lorenzo-protocol.xyz/api/v2/",
        EthereumNetwork.MANTLE: "https://explorer.mantle.xyz/api/v2/",
        EthereumNetwork.MANTLE_SEPOLIA_TESTNET: "https://explorer.sepolia.mantle.xyz/api/v2/",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz/api/v2/",
        EthereumNetwork.MANTLE_TESTNET: "https://explorer.testnet.mantle.xyz/api/v2/",
        EthereumNetwork.MANTA_PACIFIC_MAINNET: "https://pacific-explorer.manta.network/api/v2/",
        EthereumNetwork.METER_MAINNET: "https://scan.meter.io/api/v2/",
        EthereumNetwork.METER_TESTNET: "https://scan-warringstakes.meter.io/api/v2/",
        EthereumNetwork.MODE: "https://explorer.mode.network/api/v2/",
        EthereumNetwork.MODE_TESTNET: "https://sepolia.explorer.mode.network/api/v2/",
        EthereumNetwork.NAL_SEPOLIA_TESTNET: "https://testnet-scan.nal.network/api/v2/",
        EthereumNetwork.NEON_EVM_DEVNET: "https://neon-devnet.blockscout.com/api/v2/",
        EthereumNetwork.NEON_EVM_MAINNET: "https://neon.blockscout.com/api/v2/",
        EthereumNetwork.OP_CELESTIA_RASPBERRY: "https://opcelestia-raspberry.gelatoscout.com/api/v2/",
        EthereumNetwork.OP_SEPOLIA_TESTNET: "https://optimism-sepolia.blockscout.com/api/v2/",
        EthereumNetwork.PLUME_DEVNET: "https://test-explorer.plumenetwork.xyz/api/v2/",
        EthereumNetwork.PLUME_MAINNET: "https://phoenix-explorer.plumenetwork.xyz/api/v2/",
        EthereumNetwork.Q_MAINNET: "https://explorer.q.org/api/v2/",
        EthereumNetwork.Q_TESTNET: "https://explorer.qtestnet.org/api/v2/",
        EthereumNetwork.REDSTONE: "https://explorer.redstone.xyz/api/v2/",
        EthereumNetwork.RE_AL: "https://explorer.re.al/api/v2/",
        EthereumNetwork.REYA_NETWORK: "https://explorer.reya.network/api/v2/",
        EthereumNetwork.ROOTSTOCK_MAINNET: "https://rootstock.blockscout.com/api/v2/",
        EthereumNetwork.ROOTSTOCK_TESTNET: "https://rootstock-testnet.blockscout.com/api/v2/",
        EthereumNetwork.SAAKURU_MAINNET: "https://explorer.saakuru.network/api/v2/",
        EthereumNetwork.SNAXCHAIN: "https://explorer.snaxchain.io/api/v2/",
        EthereumNetwork.SONGBIRD_CANARY_NETWORK: "https://songbird-explorer.flare.network/api/v2/",
        EthereumNetwork.SONGBIRD_TESTNET_COSTON: "https://coston-explorer.flare.network/api/v2/",
        EthereumNetwork.STORY_ODYSSEY_TESTNET: "https://odyssey-testnet-explorer.storyscan.xyz/api/v2/",
        EthereumNetwork.SWELLCHAIN: "https://explorer.swellnetwork.io/api/v2/",
        EthereumNetwork.SWELLCHAIN_TESTNET: "https://swell-testnet-explorer.alt.technology/api/v2/",
        EthereumNetwork.TAIKO_HEKLA_L2: "https://blockscoutapi.hekla.taiko.xyz/api/v2/",
        EthereumNetwork.VANA_MOKSHA_TESTNET: "https://api.moksha.vanascan.io/api/v2/",
        EthereumNetwork.ZETACHAIN_TESTNET: "https://zetachain-athens-3.blockscout.com/api/v2/",
        EthereumNetwork.ZORA: "https://explorer.zora.energy/api/v2/",
        EthereumNetwork.ZORA_SEPOLIA_TESTNET: "https://sepolia.explorer.zora.energy/api/v2/",
    }

    def __init__(
        self,
        network: EthereumNetwork,
        request_timeout: int = int(
            os.environ.get("BLOCKSCOUT_CLIENT_REQUEST_TIMEOUT", 10)
        ),
    ):
        self.network = network
        self.api_url = self.NETWORK_WITH_URL.get(network, "")
        self.request_timeout = request_timeout
        if not self.api_url:
            raise BlockScoutConfigurationProblem(
                f"Network {network.name} - {network.value} not supported"
            )
        self.http_session = requests.Session()

    def build_url(self, path: str):
        return urljoin(self.api_url, path)

    def _do_request(self, url: str) -> Optional[Dict[str, Any]]:
        response = self.http_session.get(url, timeout=10)
        if not response.ok:
            return None

        return response.json()

    @staticmethod
    def _process_contract_metadata(
        contract_data: dict[str, Any]
    ) -> Optional[ContractMetadata]:
        """
        Return a ContractMetadata from BlockScout response

        :param contract_data:
        :return:
        """
        if abi := contract_data.get("abi"):
            name = contract_data["name"]
            implementations: list = contract_data.get("implementations", [])
            return ContractMetadata(
                name,
                abi,
                False,
                implementations[0]["address"] if implementations else None,
            )
        return None

    def get_contract_metadata(
        self, address: ChecksumAddress
    ) -> Optional[ContractMetadata]:
        contract_request = self.build_url(f"smart-contracts/{address}")
        contract_data = self._do_request(contract_request)
        if contract_data:
            return self._process_contract_metadata(contract_data)
        return None


class AsyncBlockscoutClient(BlockscoutClient):
    def __init__(
        self,
        network: EthereumNetwork,
        request_timeout: int = int(
            os.environ.get("BLOCKSCOUT_CLIENT_REQUEST_TIMEOUT", 10)
        ),
        max_requests: int = int(os.environ.get("BLOCKSCOUT_CLIENT_MAX_REQUESTS", 100)),
    ):
        super().__init__(network, request_timeout)
        # Limit simultaneous connections to the same host.
        self.async_session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit_per_host=max_requests)
        )

    async def _async_do_request(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Asynchronous version of _do_request
        """
        async with self.async_session.get(
            url, timeout=self.request_timeout
        ) as response:
            if not response.ok:
                return None

            return await response.json()

    async def async_get_contract_metadata(
        self, address: ChecksumAddress
    ) -> Optional[ContractMetadata]:
        contract_request = self.build_url(f"smart-contracts/{address}")
        contract_data = await self._async_do_request(contract_request)
        if contract_data:
            return self._process_contract_metadata(contract_data)
        return None
