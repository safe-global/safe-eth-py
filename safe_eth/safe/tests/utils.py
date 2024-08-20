import os
import random

from safe_eth.eth.constants import SECPK1_N


def generate_salt_nonce() -> int:
    return random.getrandbits(256) - 1


def generate_valid_s() -> int:
    while True:
        s = int(os.urandom(30).hex(), 16)
        if s <= (SECPK1_N // 2):
            return s
