import asyncio
import time
from functools import cache
from logging import getLogger

import aiohttp

logger = getLogger(__name__)


class RateLimiter:
    """
    Class to limit the number of requests per second
    """

    def __init__(self, client, rate):
        self.client = client
        self.rate = rate
        self.available_conns = rate  # Initialize available conns
        self.updated_at = time.monotonic()

    async def get(self, *args, **kwargs):
        await self._wait_for_available_conn()
        return self.client.get(*args, **kwargs)

    async def post(self, *args, **kwargs):
        await self._wait_for_available_conn()
        return self.client.post(*args, **kwargs)

    async def _wait_for_available_conn(self):
        while self.available_conns < 1:
            self._release_available_conns()
            await asyncio.sleep(0.1)
        self.available_conns -= 1

    def _release_available_conns(self):
        now = time.monotonic()
        time_since_update = now - self.updated_at
        if time_since_update >= 1:
            self.available_conns = self.rate
            self.updated_at = now


@cache
def get_client_rate_limited(host: str, rate: int) -> "RateLimiter":
    """
    Get a rate limited client by host
    Host parameter is just being used to store in cache different instance by host

    :param host:
    :param rate: number of requests allowed per second
    """
    logger.info(f"Initializing rate limiter for {host} by {rate}/s")
    async_session = aiohttp.ClientSession()
    return RateLimiter(async_session, rate)
