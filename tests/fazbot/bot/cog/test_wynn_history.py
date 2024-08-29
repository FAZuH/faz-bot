import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from fazbot.bot.cog.wynn_history import WynnHistory
from fazbot.bot.errors import BadArgument


class TestWynnHistory(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.mock_intr = MagicMock()
        self.mock_intr.created_at = datetime.now()
        self.mock_bot = MagicMock()

    async def test_activity_raises_badargument_nonexisting_guild(self) -> None:
        # Prepare
        self.mock_bot.fazdb_db.player_info_repository.get_player = AsyncMock(
            return_value=None
        )
        # Act, Assert
        with self.assertRaises(BadArgument):
            wynn_history = WynnHistory(self.mock_bot)
            await wynn_history.activity(self.mock_intr, "a", "a")

    @patch("fazbot.bot.cog.wynn_history.ActivityView", autospec=True)
    async def test_activity_past_n_hour(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_player = MagicMock()
        self.mock_bot.fazdb_db.player_info_repository.get_player = AsyncMock(
            return_value=mock_player
        )
        wynn_history = WynnHistory(self.mock_bot)
        # Act
        await wynn_history.activity(self.mock_intr, "a", "10")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        mock_invoke.assert_called_once_with(
            self.mock_bot,
            self.mock_intr,
            mock_player,
            self.mock_intr.created_at - timedelta(hours=10),
            self.mock_intr.created_at,
        )

    @patch("fazbot.bot.cog.wynn_history.ActivityView", autospec=True)
    async def test_activity_time_range(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_player = MagicMock()
        self.mock_bot.fazdb_db.player_info_repository.get_player = AsyncMock(
            return_value=mock_player
        )
        wynn_history = WynnHistory(self.mock_bot)
        # Act
        await wynn_history.activity(self.mock_intr, "a", "2 days ago - 1 days ago")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        call_args = mock_invoke.call_args[0]
        begin = call_args[3].timestamp()
        end = call_args[4].timestamp()
        self.assertAlmostEqual(
            (self.mock_intr.created_at - timedelta(days=2)).timestamp(), begin, delta=5
        )
        self.assertAlmostEqual(
            (self.mock_intr.created_at - timedelta(days=1)).timestamp(), end, delta=5
        )

    async def test_guild_activity_raises_badargument_nonexisting_guild(self) -> None:
        # Prepare
        self.mock_bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=None
        )
        # Act, Assert
        with self.assertRaises(BadArgument):
            wynn_history = WynnHistory(self.mock_bot)
            await wynn_history.guild_activity(self.mock_intr, "a", "a")

    @patch("fazbot.bot.cog.wynn_history.GuildActivityView", autospec=True)
    async def test_guild_activity_past_n_hour(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_guild = MagicMock()
        self.mock_bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=mock_guild
        )
        wynn_history = WynnHistory(self.mock_bot)
        # Act
        await wynn_history.guild_activity(self.mock_intr, "a", "10")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        mock_invoke.assert_called_once_with(
            self.mock_bot,
            self.mock_intr,
            mock_guild,
            self.mock_intr.created_at - timedelta(hours=10),
            self.mock_intr.created_at,
        )

    @patch("fazbot.bot.cog.wynn_history.GuildActivityView", autospec=True)
    async def test_guild_activity_time_range(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_guild = MagicMock()
        self.mock_bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=mock_guild
        )
        wynn_history = WynnHistory(self.mock_bot)
        # Act
        await wynn_history.guild_activity(
            self.mock_intr, "a", "2 days ago - 1 days ago"
        )
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        call_args = mock_invoke.call_args[0]
        begin = call_args[3].timestamp()
        end = call_args[4].timestamp()
        self.assertAlmostEqual(
            (self.mock_intr.created_at - timedelta(days=2)).timestamp(), begin, delta=5
        )
        self.assertAlmostEqual(
            (self.mock_intr.created_at - timedelta(days=1)).timestamp(), end, delta=5
        )

    async def asyncTearDown(self) -> None:
        return await super().asyncTearDown()
