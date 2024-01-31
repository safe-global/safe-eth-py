import time

from eth_typing import ChecksumAddress


def get_totp():
    return int(time.time()) // 3600


def get_delegate_message(cls, delegate_address: ChecksumAddress) -> str:
    totp = get_totp()
    return delegate_address + str(totp)


def get_remove_transaction_message(
    safe_address: ChecksumAddress, safe_tx_hash: bytes, chain_id: int
):
    remove_transaction_message = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "DeleteRequest": [
                {"name": "safeTxHash", "type": "bytes32"},
                {"name": "totp", "type": "uint256"},
            ],
        },
        "primaryType": "DeleteRequest",
        "domain": {
            "name": "Safe Transaction Service",
            "version": "1.0",
            "chainId": chain_id,
            "verifyingContract": safe_address,
        },
        "message": {
            "safeTxHash": safe_tx_hash,
            "totp": get_totp(),
        },
    }
    return remove_transaction_message
