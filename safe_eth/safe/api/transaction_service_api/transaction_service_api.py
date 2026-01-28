import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

from eth_typing import ChecksumAddress, Hash32, HexStr
from eth_utils import to_checksum_address
from hexbytes import HexBytes

from safe_eth.eth import EthereumClient, EthereumNetwork
from safe_eth.eth.eip712 import eip712_encode_hash
from safe_eth.safe import SafeTx
from safe_eth.util.util import to_0x_hex_str

from ..base_api import SafeAPIException, SafeBaseAPI
from .entities import Balance, DataDecoded, DelegateUser, Message, Transaction
from .transaction_service_messages import get_delegate_message
from .transaction_service_tx import TransactionServiceTx

logger = logging.getLogger(__name__)


class ApiSafeTxHashNotMatchingException(SafeAPIException):
    pass


class TransactionServiceApi(SafeBaseAPI):
    NETWORK_SHORTNAME = {
        EthereumNetwork.ARBITRUM_ONE: "arb1",
        EthereumNetwork.AURORA_MAINNET: "aurora",
        EthereumNetwork.AVALANCHE_C_CHAIN: "avax",
        EthereumNetwork.BASE: "base",
        EthereumNetwork.BASE_SEPOLIA_TESTNET: "basesep",
        EthereumNetwork.BERACHAIN: "berachain",
        EthereumNetwork.BLAST: "blastmainnet",
        EthereumNetwork.BNB_SMART_CHAIN_MAINNET: "bnb",
        EthereumNetwork.CELO_MAINNET: "celo",
        EthereumNetwork.GNOSIS: "gno",
        EthereumNetwork.GNOSIS_CHIADO_TESTNET: "chi",
        EthereumNetwork.HEMI_NETWORK: "hemi",
        EthereumNetwork.INK: "ink",
        EthereumNetwork.KATANA_MAINNET: "katana",
        EthereumNetwork.LENS: "lens",
        EthereumNetwork.LINEA: "linea",
        EthereumNetwork.MAINNET: "eth",
        EthereumNetwork.MANTLE: "mantle",
        EthereumNetwork.OPTIMISM: "oeth",
        EthereumNetwork.POLYGON: "pol",
        EthereumNetwork.POLYGON_ZKEVM: "zkevm",
        EthereumNetwork.SCROLL: "scr",
        EthereumNetwork.SEPOLIA: "sep",
        EthereumNetwork.SONIC_MAINNET: "sonic",
        EthereumNetwork.UNICHAIN: "unichain",
        EthereumNetwork.WORLD_CHAIN: "wc",
        EthereumNetwork.X_LAYER_MAINNET: "okb",
        EthereumNetwork.ZKSYNC_MAINNET: "zksync",
        EthereumNetwork.PLASMA_MAINNET: "plasma",
    }
    TRANSACTION_SERVICE_BASE_URL = "https://api.safe.global/tx-service"

    def __init__(
        self,
        network: EthereumNetwork,
        ethereum_client: Optional[EthereumClient] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = os.environ.get("SAFE_TRANSACTION_SERVICE_API_KEY"),
        request_timeout: int = int(
            os.environ.get("SAFE_TRANSACTION_SERVICE_REQUEST_TIMEOUT", 10)
        ),
    ):
        super().__init__(network, ethereum_client, base_url, api_key, request_timeout)

    def _get_url_by_network(self, network: EthereumNetwork) -> Optional[str]:
        network_short_name = self.NETWORK_SHORTNAME.get(network)
        if not network_short_name:
            return None
        return f"{self.TRANSACTION_SERVICE_BASE_URL}/{network_short_name}"

    @classmethod
    def data_decoded_to_text(cls, data_decoded: Dict[str, Any]) -> Optional[str]:
        """
        Decoded data decoded to text
        :param data_decoded:
        :return:
        """
        if not data_decoded:
            return None

        method = data_decoded["method"]
        parameters = data_decoded.get("parameters", [])
        text = ""
        for (
            parameter
        ) in parameters:  # Multisend or executeTransaction from another Safe
            if "decodedValue" in parameter:
                text += (
                    method
                    + ":\n - "
                    + "\n - ".join(
                        [
                            decoded_text
                            for decoded_value in parameter.get("decodedValue", {})
                            if (
                                decoded_text := cls.data_decoded_to_text(
                                    decoded_value.get("decodedData", {})
                                )
                            )
                            is not None
                        ]
                    )
                    + "\n"
                )
        if text:
            return text.strip()
        else:
            return (
                method
                + ": "
                + ",".join([str(parameter["value"]) for parameter in parameters])
            )

    @classmethod
    def parse_signatures(cls, raw_tx: Transaction) -> Optional[bytes]:
        """
        Parse signatures in `confirmations` list to build a valid signature (owners must be sorted lexicographically)

        :param raw_tx:
        :return: Valid signature with signatures sorted lexicographically
        """
        if raw_tx["signatures"]:
            # Tx was executed and signatures field is populated
            return HexBytes(raw_tx["signatures"])
        elif raw_tx["confirmations"]:
            # Parse offchain transactions
            return b"".join(
                [
                    HexBytes(confirmation["signature"])
                    for confirmation in sorted(
                        raw_tx["confirmations"], key=lambda x: int(x["owner"], 16)
                    )
                    if confirmation["signatureType"] == "EOA"
                ]
            )
        return None

    def create_delegate_message_hash(self, delegate_address: ChecksumAddress) -> Hash32:
        return eip712_encode_hash(
            get_delegate_message(delegate_address, self.network.value)
        )

    def _build_transaction_service_tx(
        self, safe_tx_hash: Union[bytes, HexStr], tx_raw: Transaction
    ) -> TransactionServiceTx:
        signatures = self.parse_signatures(tx_raw)
        safe_tx = TransactionServiceTx(
            to_checksum_address(tx_raw["proposer"]) if tx_raw["proposer"] else None,
            self.ethereum_client,
            tx_raw["safe"],
            tx_raw["to"],
            int(tx_raw["value"]),
            HexBytes(tx_raw["data"]) if tx_raw["data"] else b"",
            int(tx_raw["operation"]),
            int(tx_raw["safeTxGas"]),
            int(tx_raw["baseGas"]),
            int(tx_raw["gasPrice"]),
            tx_raw["gasToken"],
            tx_raw["refundReceiver"],
            signatures=signatures if signatures else b"",
            safe_nonce=int(tx_raw["nonce"]),
            chain_id=self.network.value,
        )
        safe_tx.tx_hash = (
            HexBytes(tx_raw["transactionHash"]) if tx_raw["transactionHash"] else None
        )

        if safe_tx.safe_tx_hash != HexBytes(safe_tx_hash):
            raise ApiSafeTxHashNotMatchingException(
                f"API safe-tx-hash: {to_0x_hex_str(HexBytes(safe_tx_hash))} doesn't match the calculated safe-tx-hash: {to_0x_hex_str(HexBytes(safe_tx.safe_tx_hash))}"
            )

        return safe_tx

    def get_balances(self, safe_address: ChecksumAddress) -> List[Balance]:
        """

        :param safe_address:
        :return: a list of balances for provided Safe
        """
        response = self._get_request(f"/api/v1/safes/{safe_address}/balances/")
        if not response.ok:
            raise SafeAPIException(f"Cannot get balances: {response.content!r}")
        return response.json()

    def get_safe_transaction(
        self, safe_tx_hash: Union[bytes, HexStr]
    ) -> Tuple[TransactionServiceTx, Optional[HexBytes]]:
        """
        :param safe_tx_hash:
        :return: SafeTx and `tx-hash` if transaction was executed
        """
        safe_tx_hash_str = to_0x_hex_str(HexBytes(safe_tx_hash))
        response = self._get_request(
            f"/api/v2/multisig-transactions/{safe_tx_hash_str}/"
        )
        if not response.ok:
            raise SafeAPIException(
                f"Cannot get transaction with safe-tx-hash={safe_tx_hash_str}: {response.content!r}"
            )

        if not self.ethereum_client:
            logger.warning(
                "EthereumClient should be defined to get a executable SafeTx"
            )

        result = response.json()
        safe_tx = self._build_transaction_service_tx(safe_tx_hash, result)

        return safe_tx, HexBytes(safe_tx.tx_hash) if safe_tx.tx_hash else None

    def get_transactions(
        self, safe_address: ChecksumAddress, **kwargs: Dict[str, Union[str, int, bool]]
    ) -> List[Transaction]:
        """

        :param safe_address:
        :return: a list of transactions for provided Safe
        """
        url = f"/api/v2/safes/{safe_address}/multisig-transactions/"

        if kwargs:
            query_string = urlencode(
                {key: str(value) for key, value in kwargs.items() if value is not None}
            )
            url += "?" + query_string

        response = self._get_request(url)
        if not response.ok:
            raise SafeAPIException(f"Cannot get transactions: {response.content!r}")

        transactions = response.json().get("results", [])

        if safe_tx_hash_arg := kwargs.get("safe_tx_hash", None):
            # Validation that the calculated safe_tx_hash is the same as the safe_tx_hash provided for filter.
            safe_tx_hash = HexBytes(str(safe_tx_hash_arg))
            [
                self._build_transaction_service_tx(safe_tx_hash, tx)
                for tx in transactions
            ]

        return transactions

    def get_delegates(self, safe_address: ChecksumAddress) -> List[DelegateUser]:
        """

        :param safe_address:
        :return: a list of delegates for provided Safe
        """
        response = self._get_request(f"/api/v2/delegates/?safe={safe_address}")
        if not response.ok:
            raise SafeAPIException(f"Cannot get delegates: {response.content!r}")
        return response.json().get("results", [])

    def get_safes_for_owner(
        self, owner_address: ChecksumAddress
    ) -> List[ChecksumAddress]:
        """

        :param owner_address:
        :return: a List of Safe addresses which the owner_address is an owner
        """
        response = self._get_request(f"/api/v1/owners/{owner_address}/safes/")
        if not response.ok:
            raise SafeAPIException(f"Cannot get delegates: {response.content!r}")
        return response.json().get("safes", [])

    def post_signatures(self, safe_tx_hash: bytes, signatures: bytes) -> bool:
        """
        Create a new confirmation with provided signature for the given safe_tx_hash
        :param safe_tx_hash:
        :param signatures:
        :return: True if new confirmation was created
        """
        safe_tx_hash_str = to_0x_hex_str(safe_tx_hash)
        response = self._post_request(
            f"/api/v1/multisig-transactions/{safe_tx_hash_str}/confirmations/",
            payload={"signature": to_0x_hex_str(signatures)},
        )
        if not response.ok:
            raise SafeAPIException(
                f"Cannot post signatures for tx with safe-tx-hash={safe_tx_hash_str}: {response.content!r}"
            )
        return True

    def add_delegate(
        self,
        delegate_address: ChecksumAddress,
        delegator_address: ChecksumAddress,
        label: str,
        signature: bytes,
        safe_address: Optional[ChecksumAddress] = None,
    ) -> bool:
        add_payload = {
            "delegate": delegate_address,
            "delegator": delegator_address,
            "signature": to_0x_hex_str(HexBytes(signature)),
            "label": label,
        }
        if safe_address:
            add_payload["safe"] = safe_address
        response = self._post_request("/api/v2/delegates/", add_payload)
        if not response.ok:
            raise SafeAPIException(f"Cannot add delegate: {response.content!r}")
        return True

    def remove_delegate(
        self,
        delegate_address: ChecksumAddress,
        delegator_address: ChecksumAddress,
        signature: bytes,
        safe_address: Optional[ChecksumAddress] = None,
    ) -> bool:
        """
        Deletes a delegated user

        :param delegator_address:
        :param delegate_address:
        :param signature: Signature of a hash of an eip712 message.
        :param safe_address: If specified, a delegate is removed for a delegator for the specific safe.
            Otherwise, the delegate is deleted in a global form.
        :return:
        """
        remove_payload = {
            "delegator": delegator_address,
            "signature": to_0x_hex_str(HexBytes(signature)),
        }
        if safe_address:
            remove_payload["safe"] = safe_address
        response = self._delete_request(
            f"/api/v2/delegates/{delegate_address}/",
            remove_payload,
        )
        if not response.ok:
            raise SafeAPIException(f"Cannot remove delegate: {response.content!r}")
        return True

    def post_transaction(self, safe_tx: SafeTx) -> bool:
        random_sender = "0x0000000000000000000000000000000000000002"
        sender = safe_tx.sorted_signers[0] if safe_tx.sorted_signers else random_sender
        data = {
            "to": safe_tx.to,
            "value": safe_tx.value,
            "data": to_0x_hex_str(safe_tx.data) if safe_tx.data else None,
            "operation": safe_tx.operation,
            "gasToken": safe_tx.gas_token,
            "safeTxGas": safe_tx.safe_tx_gas,
            "baseGas": safe_tx.base_gas,
            "gasPrice": safe_tx.gas_price,
            "refundReceiver": safe_tx.refund_receiver,
            "nonce": safe_tx.safe_nonce,
            "contractTransactionHash": to_0x_hex_str(safe_tx.safe_tx_hash),
            "sender": sender,
            "signature": safe_tx.signatures.hex() if safe_tx.signatures else None,
            "origin": "Safe-CLI",
        }
        response = self._post_request(
            f"/api/v2/safes/{safe_tx.safe_address}/multisig-transactions/", data
        )
        if not response.ok:
            raise SafeAPIException(f"Error posting transaction: {response.content!r}")
        return True

    def delete_transaction(self, safe_tx_hash: str, signature: str) -> bool:
        """

        :param safe_tx_hash: hash of eip712 see in transaction_service_messages.py generate_remove_transaction_message function
        :param signature: signature of safe_tx_hash by transaction proposer
        :return:
        """
        payload = {"safeTxHash": safe_tx_hash, "signature": signature}
        response = self._delete_request(
            f"/api/v2/multisig-transactions/{safe_tx_hash}/", payload
        )
        if not response.ok:
            raise SafeAPIException(f"Error deleting transaction: {response.content!r}")
        return True

    def post_message(
        self,
        safe_address: ChecksumAddress,
        message: Union[str, Dict],
        signature: bytes,
        safe_app_id: Optional[int] = 0,
    ) -> bool:
        """
        Create safe message on transaction service for provided Safe address

        :param safe_address:
        :param message: If str it will be encoded using EIP191, and if it's a dictionary it will be encoded using EIP712
        :param signature:
        :return:
        """
        payload = {
            "message": message,
            "safeAppId": safe_app_id,
            "signature": to_0x_hex_str(signature),
        }
        response = self._post_request(
            f"/api/v1/safes/{safe_address}/messages/", payload
        )
        if not response.ok:
            raise SafeAPIException(f"Error posting message: {response.content!r}")
        return True

    def get_message(self, safe_message_hash: bytes) -> Message:
        """

        :param safe_message_hash:
        :return: Safe message for provided Safe message hash
        """
        response = self._get_request(
            f"/api/v1/messages/{to_0x_hex_str(safe_message_hash)}/"
        )
        if not response.ok:
            raise SafeAPIException(f"Cannot get messages: {response.content!r}")
        return response.json()

    def get_messages(self, safe_address: ChecksumAddress) -> List[Message]:
        """

        :param safe_address:
        :return: list of messages for provided Safe address
        """
        response = self._get_request(f"/api/v1/safes/{safe_address}/messages/")
        if not response.ok:
            raise SafeAPIException(f"Cannot get messages: {response.content!r}")
        return response.json().get("results", [])

    def post_message_signature(
        self, safe_message_hash: bytes, signature: bytes
    ) -> bool:
        """
        Add a new confirmation for provided Safe message hash

        :param safe_message_hash:
        :param signature:
        :return:
        """
        payload = {"signature": to_0x_hex_str(signature)}
        response = self._post_request(
            f"/api/v1/messages/{to_0x_hex_str(safe_message_hash)}/signatures/",
            payload,
        )
        if not response.ok:
            raise SafeAPIException(
                f"Error posting message signature: {response.content!r}"
            )
        return True

    def decode_data(
        self, data: Union[bytes, HexStr], to_address: Optional[ChecksumAddress] = None
    ) -> DataDecoded:
        """
        Retrieve decoded information using tx service internal ABI information given the tx data.

        :param data: tx data as a 0x prefixed hexadecimal string.
        :param to_address: address of the contract. This will be used in case of more than one function identifiers matching.
        :return:
        """
        payload = {"data": to_0x_hex_str(HexBytes(data))}
        if to_address:
            payload["to"] = to_address
        response = self._post_request("/api/v1/data-decoder/", payload)
        if not response.ok:
            raise SafeAPIException(f"Cannot decode tx data: {response.content!r}")
        return response.json()
