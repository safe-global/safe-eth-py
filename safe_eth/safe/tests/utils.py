import random


def generate_salt_nonce() -> int:
    return random.getrandbits(256) - 1
