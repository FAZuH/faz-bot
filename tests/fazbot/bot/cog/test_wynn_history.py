from __future__ import annotations

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import UUID

from fazbot.app.properties import Properties
from fazbot.bot.cog.wynn_history import WynnHistory
from fazbot.bot.errors import BadArgument
from fazutil.db.fazdb.fazdb_database import FazdbDatabase
from fazutil.db.fazdb.model.guild_info import GuildInfo
from fazutil.db.fazdb.model.player_info import PlayerInfo


class TestWynnHistory(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        with patch("nextcord.interactions.Interaction", autospec=True) as mock_intr:
            self.mock_intr = mock_intr
            self.mock_intr.created_at = datetime.now()
        with patch("fazbot.bot.bot.Bot") as mock_bot:
            self.mock_bot = mock_bot
        p = Properties()
        p.setup()
        self.db = FazdbDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            f"{p.FAZDB_DB_NAME}_test",
        )
        self.db.drop_all()
        self.mock_bot.fazdb_db = self.db
        dummy_guild = self._get_dummy_guild_info()
        await self.db.guild_info_repository.create_table()
        await self.db.player_info_repository.create_table()
        await self.db.guild_info_repository.insert(dummy_guild)

    async def test_activity_raises_badargument_nonexisting_player(self) -> None:
        # Act, Assert
        with self.assertRaises(BadArgument):
            wynn_history = WynnHistory(self.mock_bot)
            await wynn_history.activity(self.mock_intr, "a", "a")

    # @patch("fazbot.bot.invoke.invoke_activity.InvokeActivity")
    async def test_activity_past_n_hour(self) -> None:
        # Prepare
        dummy = self._get_dummy_player_info()
        await self.db.player_info_repository.insert(dummy)
        with patch("fazbot.bot.invoke.invoke_activity.InvokeActivity.run") as mock_run:
            wynn_history = WynnHistory(self.mock_bot)
            # Act
            await wynn_history.activity(self.mock_intr, "a", "10")
            # Assert
            mock_run.assert_awaited_once()
        # TODO: patch by class doesn't patch InvokeActivity for some reason
        # mock_invoke_instance = mock_invoke.return_value
        # mock_invoke_instance.run = AsyncMock()
        # wynn_history = WynnHistory(self.mock_bot)
        # # Act
        # await wynn_history.activity(self.mock_intr, "a", "10")
        # # Assert
        # mock_invoke_instance.run.assert_awaited_once()
        # mock_invoke_instance.assert_called_once_with(
        #     self.mock_bot,
        #     self.mock_intr,
        #     dummy,
        #     self.mock_intr.created_at - timedelta(hours=10),
        # )

    @unittest.skip("Skip until test_activity_past_n_hour is fixed")
    async def test_activity_time_range(self, mock_intr: MagicMock) -> None:
        pass

    async def asyncTearDown(self) -> None:
        await self.db.async_engine.dispose()
        return await super().asyncTearDown()

    def _get_dummy_player_info(self) -> PlayerInfo:
        model = self.db.player_info_repository.model
        uuid = UUID(int=1).bytes
        dummy = model(
            uuid=uuid,
            latest_username="a",
            first_join=datetime.now(),
            guild_uuid=uuid,
        )
        return dummy

    def _get_dummy_guild_info(self) -> GuildInfo:
        model = self.db.guild_info_repository.model
        uuid = UUID(int=1).bytes
        dummy = model(
            uuid=uuid,
            name="a",
            prefix="ABC",
            created=datetime.now(),
        )
        return dummy

    @staticmethod
    def _get_mock_user() -> MagicMock:
        ret = MagicMock()
        ret.id = 1
        return ret
