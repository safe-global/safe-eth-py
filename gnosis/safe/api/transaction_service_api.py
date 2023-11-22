import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3

from gnosis.eth import EthereumNetwork
from gnosis.safe import SafeTx

from .base_api import SafeAPIException, SafeBaseAPI

logger = logging.getLogger(__name__)


class TransactionServiceApi(SafeBaseAPI):
    URL_BY_NETWORK = {
        EthereumNetwork.ARBITRUM_ONE: "https://safe-transaction-arbitrum.safe.global",
        EthereumNetwork.AURORA_MAINNET: "https://safe-transaction-aurora.safe.global",
        EthereumNetwork.AVALANCHE_C_CHAIN: "https://safe-transaction-avalanche.safe.global",
        EthereumNetwork.BASE_GOERLI_TESTNET: "https://safe-transaction-base-testnet.safe.global",
        EthereumNetwork.BASE_MAINNET: "https://safe-transaction-base.safe.global",
        EthereumNetwork.BINANCE_SMART_CHAIN_MAINNET: "https://safe-transaction-bsc.safe.global",
        EthereumNetwork.CELO_MAINNET: "https://safe-transaction-celo.safe.global",
        EthereumNetwork.GNOSIS: "https://safe-transaction-gnosis-chain.safe.global",
        EthereumNetwork.GOERLI: "https://safe-transaction-goerli.safe.global",
        EthereumNetwork.MAINNET: "https://safe-transaction-mainnet.safe.global",
        EthereumNetwork.OPTIMISM: "https://safe-transaction-optimism.safe.global",
        EthereumNetwork.POLYGON: "https://safe-transaction-polygon.safe.global",
        EthereumNetwork.POLYGON_ZKEVM: "https://safe-transaction-zkevm.safe.global",
        EthereumNetwork.SEPOLIA: "https://safe-transaction-sepolia.safe.global",
        EthereumNetwork.ZKSYNC_V2: "https://safe-transaction-zksync.safe.global",
    }

    @classmethod
    def create_delegate_message_hash(cls, delegate_address: ChecksumAddress) -> str:
        totp = int(time.time()) // 3600
        hash_to_sign = Web3.keccak(text=delegate_address + str(totp))
        return hash_to_sign

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
                            cls.data_decoded_to_text(
                                decoded_value.get("decodedData", {})
                            )
                            for decoded_value in parameter.get("decodedValue", {})
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
    def parse_signatures(cls, raw_tx: Dict[str, Any]) -> Optional[bytes]:
        """
        Parse signatures in `confirmations` list to build a valid signature (owners must be sorted lexicographically)

        :param raw_tx:
        :return: Valid signature with signatures sorted lexicographically
        """
        if raw_tx["signatures"]:
            # Tx was executed and signatures field is populated
            return raw_tx["signatures"]
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

    def get_balances(self, safe_address: str) -> List[Dict[str, Any]]:
        """

        :param safe_address:
        :return: a list of balances for provided Safe
        """
        response = self._get_request(f"/api/v1/safes/{safe_address}/balances/")
        if not response.ok:
            raise SafeAPIException(f"Cannot get balances: {response.content}")
        return response.json()

    def get_safe_transaction(
        self, safe_tx_hash: Union[bytes, HexStr]
    ) -> Tuple[SafeTx, Optional[HexBytes]]:
        """
        :param safe_tx_hash:
        :return: SafeTx and `tx-hash` if transaction was executed
        """
        safe_tx_hash = HexBytes(safe_tx_hash).hex()
        response = self._get_request(f"/api/v1/multisig-transactions/{safe_tx_hash}/")
        if not response.ok:
            raise SafeAPIException(
                f"Cannot get transaction with safe-tx-hash={safe_tx_hash}: {response.content}"
            )

        result = response.json()
        signatures = self.parse_signatures(result)
        if not self.ethereum_client:
            logger.warning(
                "EthereumClient should be defined to get a executable SafeTx"
            )
        safe_tx = SafeTx(
            self.ethereum_client,
            result["safe"],
            result["to"],
            int(result["value"]),
            HexBytes(result["data"]) if result["data"] else b"",
            int(result["operation"]),
            int(result["safeTxGas"]),
            int(result["baseGas"]),
            int(result["gasPrice"]),
            result["gasToken"],
            result["refundReceiver"],
            signatures=signatures if signatures else b"",
            safe_nonce=int(result["nonce"]),
            chain_id=self.network.value,
        )
        tx_hash = (
            HexBytes(result["transactionHash"]) if result["transactionHash"] else None
        )
        if tx_hash:
            safe_tx.tx_hash = tx_hash
        return safe_tx, tx_hash

    def get_transactions(self, safe_address: ChecksumAddress) -> List[Dict[str, Any]]:
        """

        :param safe_address:
        :return: a list of transactions for provided Safe
        """
        response = self._get_request(
            f"/api/v1/safes/{safe_address}/multisig-transactions/"
        )
        if not response.ok:
            raise SafeAPIException(f"Cannot get transactions: {response.content}")
        return response.json().get("results", [])

    def get_delegates(self, safe_address: ChecksumAddress) -> List[Dict[str, Any]]:
        """

        :param safe_address:
        :return: a list of delegates for provided Safe
        """
        response = self._get_request(f"/api/v1/delegates/?safe={safe_address}")
        if not response.ok:
            raise SafeAPIException(f"Cannot get delegates: {response.content}")
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
            raise SafeAPIException(f"Cannot get delegates: {response.content}")
        return response.json().get("safes", [])

    def post_signatures(self, safe_tx_hash: bytes, signatures: bytes) -> bool:
        """
        Create a new confirmation with provided signature for the given safe_tx_hash
        :param safe_tx_hash:
        :param signatures:
        :return: True if new confirmation was created
        """
        safe_tx_hash = HexBytes(safe_tx_hash).hex()
        response = self._post_request(
            f"/api/v1/multisig-transactions/{safe_tx_hash}/confirmations/",
            payload={"signature": HexBytes(signatures).hex()},
        )
        if not response.ok:
            raise SafeAPIException(
                f"Cannot post signatures for tx with safe-tx-hash={safe_tx_hash}: {response.content}"
            )
        return True

    def add_delegate(
        self,
        safe_address: ChecksumAddress,
        delegate_address: ChecksumAddress,
        label: str,
        signer_account: LocalAccount,
    ) -> bool:
        hash_to_sign = self.create_delegate_message_hash(delegate_address)
        signature = signer_account.signHash(hash_to_sign)
        add_payload = {
            "safe": safe_address,
            "delegate": delegate_address,
            "signature": signature.signature.hex(),
            "label": label,
        }
        response = self._post_request(
            f"/api/v1/safes/{safe_address}/delegates/", add_payload
        )
        if not response.ok:
            raise SafeAPIException(f"Cannot add delegate: {response.content}")
        return True

    def remove_delegate(
        self,
        safe_address: ChecksumAddress,
        delegate_address: ChecksumAddress,
        signer_account: LocalAccount,
    ) -> bool:
        hash_to_sign = self.create_delegate_message_hash(delegate_address)
        signature = signer_account.signHash(hash_to_sign)
        remove_payload = {"signature": signature.signature.hex()}
        response = self._delete_request(
            f"/api/v1/safes/{safe_address}/delegates/{delegate_address}/",
            remove_payload,
        )
        if not response.ok:
            raise SafeAPIException(f"Cannot remove delegate: {response.content}")
        return True

    def post_transaction(self, safe_tx: SafeTx) -> bool:
        random_sender = "0x0000000000000000000000000000000000000002"
        sender = safe_tx.sorted_signers[0] if safe_tx.sorted_signers else random_sender
        data = {
            "to": safe_tx.to,
            "value": safe_tx.value,
            "data": safe_tx.data.hex() if safe_tx.data else None,
            "operation": safe_tx.operation,
            "gasToken": safe_tx.gas_token,
            "safeTxGas": safe_tx.safe_tx_gas,
            "baseGas": safe_tx.base_gas,
            "gasPrice": safe_tx.gas_price,
            "refundReceiver": safe_tx.refund_receiver,
            "nonce": safe_tx.safe_nonce,
            "contractTransactionHash": safe_tx.safe_tx_hash.hex(),
            "sender": sender,
            "signature": safe_tx.signatures.hex() if safe_tx.signatures else None,
            "origin": "Safe-CLI",
        }
        response = self._post_request(
            f"/api/v1/safes/{safe_tx.safe_address}/multisig-transactions/", data
        )
        if not response.ok:
            raise SafeAPIException(f"Error posting transaction: {response.content}")
        return True
