import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, create_autospec, patch

from fazcord.bot._utils import Utils
from fazcord.bot.cog.wynn_history_cog import WynnHistoryCog


class TestWynnHistoryCog(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.intr = MagicMock()
        self.intr.response.defer = AsyncMock()
        self.intr.created_at = datetime.now()
        self.bot = MagicMock()
        self.utils = create_autospec(Utils, spec_set=True)
        self.bot.utils = self.utils

    @patch("fazcord.bot.cog.wynn_history_cog.ActivityView", autospec=True)
    async def test_activity_past_n_hour(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_player = MagicMock()
        mock_player.awaitable_attrs = self._mock_awaitable_attr()
        self.utils.must_get_wynn_player = AsyncMock(return_value=mock_player)
        wynn_history = WynnHistoryCog(self.bot)
        # Act
        await wynn_history.activity(self.intr, "a", "10")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        mock_invoke.assert_called_once_with(
            self.bot,
            self.intr,
            mock_player,
            self.intr.created_at - timedelta(hours=10),
            self.intr.created_at,
        )

    @patch("fazcord.bot.cog.wynn_history_cog.ActivityView", autospec=True)
    async def test_activity_time_range(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_player = MagicMock()
        mock_player.awaitable_attrs = self._mock_awaitable_attr()
        self.bot.fazdb_db.player_info_repository.get_player = AsyncMock(
            return_value=mock_player
        )
        wynn_history = WynnHistoryCog(self.bot)
        # Act
        await wynn_history.activity(self.intr, "a", "2 days ago - 1 days ago")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        call_args = mock_invoke.call_args[0]
        begin = call_args[3].timestamp()
        end = call_args[4].timestamp()
        self.assertAlmostEqual(
            (self.intr.created_at - timedelta(days=2)).timestamp(), begin, delta=5
        )
        self.assertAlmostEqual(
            (self.intr.created_at - timedelta(days=1)).timestamp(), end, delta=5
        )

    @patch("fazcord.bot.cog.wynn_history_cog.GuildActivityView", autospec=True)
    async def test_guild_activity_past_n_hour(self, mock_invoke: MagicMock) -> None:
        # Prepare
        mock_guild = MagicMock()
        mock_guild.awaitable_attrs.members = self._mock_awaitable_attr()
        self.utils.must_get_wynn_guild = AsyncMock(return_value=mock_guild)
        wynn_history = WynnHistoryCog(self.bot)
        # Act
        await wynn_history.guild_activity(self.intr, "a", "10")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        mock_invoke.assert_called_once_with(
            self.bot,
            self.intr,
            mock_guild,
            self.intr.created_at - timedelta(hours=10),
            self.intr.created_at,
        )

    @patch("fazcord.bot.cog.wynn_history_cog.GuildActivityView", autospec=True)
    async def test_guild_activity_time_range(self, mock_invoke: MagicMock) -> None:
        mock_guild = MagicMock()
        mock_guild.awaitable_attrs.members = self._mock_awaitable_attr()
        self.bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=mock_guild
        )
        wynn_history = WynnHistoryCog(self.bot)
        # Act
        await wynn_history.guild_activity(self.intr, "a", "2 days ago - 1 days ago")
        # Assert
        mock_invoke.return_value.run.assert_awaited_once()
        call_args = mock_invoke.call_args[0]
        begin = call_args[3].timestamp()
        end = call_args[4].timestamp()
        self.assertAlmostEqual(
            (self.intr.created_at - timedelta(days=2)).timestamp(), begin, delta=5
        )
        self.assertAlmostEqual(
            (self.intr.created_at - timedelta(days=1)).timestamp(), end, delta=5
        )

    async def _mock_awaitable_attr(self) -> None: ...

    async def asyncTearDown(self) -> None:
        return await super().asyncTearDown()
