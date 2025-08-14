import asyncio
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
        self._waiters = []  # List of tasks that are waiting for a connection
        self.loop = asyncio.get_event_loop()
        self._schedule_next_release_connections()  # Schedule first release connections

    async def get(self, *args, **kwargs):
        await self._wait_for_available_conn()
        return self.client.get(*args, **kwargs)

    async def post(self, *args, **kwargs):
        await self._wait_for_available_conn()
        return self.client.post(*args, **kwargs)

    def _wakeup_waiters(self):
        """
        Unblock tasks waiting for connections
        """
        while self.available_conns > 0 and self._waiters:
            future = self._waiters.pop(0)
            future.set_result(None)  # Release await
            self.available_conns -= 1

    async def _wait_for_available_conn(self):
        if self.available_conns < 1:
            future = asyncio.Future()
            self._waiters.append(future)
            await future
        else:
            self.available_conns -= 1

    def _release_available_conns(self):
        """
        Release new connections
        """
        self.available_conns += self.rate - self.available_conns
        self._wakeup_waiters()
        self._schedule_next_release_connections()

    def _schedule_next_release_connections(self):
        """
        Schedule next release connections
        """
        self.loop.call_later(1, self._release_available_conns)


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
