from datetime import datetime
from typing import override
import unittest

from fazutil.api import WynnApi


class TestApiEndpoint(unittest.IsolatedAsyncioTestCase):
    """Test if API request works, and if it stores the response properly"""

    @override
    async def asyncSetUp(self) -> None:
        self._api = WynnApi()

    async def test_guild_get(self) -> None:
        """Test if API endpoint 'guild' works, and if it stores the response
        properly
        """
        async with self._api as api:
            response = await api.guild.get("Avicia")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.name, "Avicia")
        self.assertAlmostEqual(
            response.headers.expires.to_datetime().timestamp(),
            datetime.now().timestamp(),
            delta=500,
        )

    async def test_guild_prefix_get(self) -> None:
        """Test if API endpoint 'guild' works by a guild prefix, and if it
        stores the response properly
        """
        async with self._api as api:
            response = await api.guild.get_from_prefix("AVO")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.prefix, "AVO")
        self.assertAlmostEqual(
            response.headers.expires.to_datetime().timestamp(),
            datetime.now().timestamp(),
            delta=500,
        )

    async def test_player(self) -> None:
        """Test if API endpoint 'player' works, and if it stores the response
        properly"""
        async with self._api as api:
            response = await api.player.get_full_stats("FAZuH")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.username, "FAZuH")
        self.assertAlmostEqual(
            response.headers.expires.to_datetime().timestamp(),
            datetime.now().timestamp(),
            delta=500,
        )

    async def test_online_players(self) -> None:
        """Test if API endpoint 'player' works, and if it stores the response
        properly
        """
        async with self._api as api:
            response = await api.player.get_online_uuids()
        self.assertIsNotNone(response.body)
        self.assertAlmostEqual(
            response.headers.expires.to_datetime().timestamp(),
            datetime.now().timestamp(),
            delta=500,
        )

    @override
    async def asyncTearDown(self) -> None:
        await self._api.close()
