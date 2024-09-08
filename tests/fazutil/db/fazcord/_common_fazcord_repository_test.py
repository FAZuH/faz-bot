from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, override

from fazutil.db.fazcord.fazcord_database import FazcordDatabase
from tests.fazutil.db._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazutil.db.base_repository import BaseRepository


class CommonFazcordRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazcordDatabase, R], ABC):

        @property
        @override
        def database_type(self) -> type[FazcordDatabase]:
            return FazcordDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "faz-cord_test"

        # Create Table Order
        # await self.database.discord_guild_repository.create_table()
        # await self.database.discord_user_repository.create_table()
        # await self.database.discord_channel_repository.create_table()
        # await self.database.track_entry_repository.create_table()
        # await self.database.track_entry_association_repository.create_table()
        # await self.database.whitelist_group_repository.create_table()

        def _get_discord_channel_mock_data(self):
            model = self.database.discord_channel_repository.model
            mock_data1 = model(channel_id=1, channel_name="a", guild_id=1)
            mock_data2 = mock_data1.clone()
            mock_data3 = mock_data1.clone()
            mock_data3.channel_id = 2
            mock_data4 = mock_data1.clone()
            mock_data4.channel_name = "b"
            return (mock_data1, mock_data2, mock_data3, mock_data4, "channel_name")

        def _get_discord_guild_mock_data(self):
            model = self.database.discord_guild_repository.model
            mock_data1 = model(guild_id=1, guild_name="a")
            mock_data2 = mock_data1.clone()
            mock_data3 = mock_data1.clone()
            mock_data3.guild_id = 2
            mock_data4 = mock_data1.clone()
            mock_data4.guild_name = "b"
            return (mock_data1, mock_data2, mock_data3, mock_data4, "guild_name")

        def _get_discord_user_mock_data(self):
            model = self.database.discord_user_repository.model
            mock_data1 = model(user_id=1, username="a")
            mock_data2 = mock_data1.clone()
            mock_data3 = mock_data1.clone()
            mock_data3.user_id = 2
            mock_data4 = mock_data1.clone()
            mock_data4.username = "b"
            return (mock_data1, mock_data2, mock_data3, mock_data4, "username")

        def _get_track_entry_association_mock_data(self):
            model = self.database.track_entry_association_repository.model
            mock_data1 = model(
                id=1,
                track_entry_id=1,
                associated_value=b"a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            )
            mock_data2 = mock_data1.clone()
            mock_data3 = mock_data1.clone()
            mock_data3.id = 2
            mock_data3.track_entry_id = 2
            mock_data4 = mock_data1.clone()
            mock_data4.associated_value = (
                b"b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            )
            return (mock_data1, mock_data2, mock_data3, mock_data4, "associated_value")

        def _get_track_entry_mock_data(self):
            model = self.database.track_entry_repository.model
            mock_data1 = model(
                id=1,
                channel_id=1,
                created_by=1,
                created_on=self._get_mock_datetime(),
                type="GUILD",
                enabled=False,
            )
            mock_data2 = mock_data1.clone()
            mock_data3 = mock_data1.clone()
            mock_data3.id = 2
            mock_data3.channel_id = 2
            mock_data4 = mock_data1.clone()
            mock_data4.type = "PLAYER"
            return (mock_data1, mock_data2, mock_data3, mock_data4, "type")

        def _get_whitelist_group_mock_data(self):
            model = self.database.whitelist_group_repository.model
            mock_data1 = model(
                id=1,
                type="a",
                reason="a",
                from_=self._get_mock_datetime(),
                until=self._get_mock_datetime(),
            )
            mock_data2 = mock_data1.clone()
            mock_data3 = mock_data1.clone()
            mock_data3.id = 2
            mock_data4 = mock_data1.clone()
            mock_data4.reason = "b"
            return (mock_data1, mock_data2, mock_data3, mock_data4, "reason")
