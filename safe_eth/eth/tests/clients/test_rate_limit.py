import asyncio
import unittest

from safe_eth.eth.clients.rate_limiter import get_client_rate_limited


class TestRateLimit(unittest.IsolatedAsyncioTestCase):
    async def _make_request(self, rate_limited):
        """Helper to fetch the status code of a request."""
        try:
            async with await rate_limited.get(
                "https://safe-transaction-sepolia.safe.global/api/v1/about", timeout=5
            ) as response:
                return response
        except asyncio.TimeoutError:
            return None

    async def test_rate_limiter(self):
        rate_limited = get_client_rate_limited(
            "https://safe-transaction-sepolia.safe.global/", 5
        )
        tasks = [self._make_request(rate_limited) for _ in range(20)]
        responses = await asyncio.gather(*tasks)
        self.assertEqual(len(responses), 20)
        for response in responses:
            self.assertEqual(response.status, 200)  # Check the status code
            self.assertTrue(response.ok)
