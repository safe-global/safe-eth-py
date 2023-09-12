import os
import random
from logging import getLogger

from gnosis.eth.constants import SECPK1_N

logger = getLogger(__name__)


def generate_salt_nonce() -> int:
    return random.getrandbits(256) - 1


def generate_valid_s() -> int:
    while True:
        s = int(os.urandom(30).hex(), 16)
        if s <= (SECPK1_N // 2):
            return s
