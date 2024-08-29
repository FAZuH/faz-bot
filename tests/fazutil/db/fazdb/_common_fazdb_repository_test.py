from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, override
from uuid import UUID

from fazutil.db.fazdb.fazdb_database import FazdbDatabase
from tests.fazutil.db._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazutil.db.base_repository import BaseRepository


class CommonFazdbRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazdbDatabase, R], ABC):

        @property
        @override
        def database_type(self) -> type[FazdbDatabase]:
            return FazdbDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "faz-db_test"

        def _get_character_history_mock_data(self):
            repo = self.database.character_history_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(
                character_uuid=uuid1,
                level=1,
                xp=1,
                wars=1,
                playtime=1.0,
                mobs_killed=1,
                chests_found=1,
                logins=1,
                deaths=1,
                discoveries=1,
                hardcore=False,
                ultimate_ironman=False,
                ironman=False,
                craftsman=False,
                hunted=False,
                alchemism=1.0,
                armouring=1.0,
                cooking=1.0,
                jeweling=1.0,
                scribing=1.0,
                tailoring=1.0,
                weaponsmithing=1.0,
                woodworking=1.0,
                mining=1.0,
                woodcutting=1.0,
                farming=1.0,
                fishing=1.0,
                dungeon_completions=1,
                quest_completions=1,
                raid_completions=1,
                datetime=self._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            del mock3.unique_id
            mock3.character_uuid = uuid2
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.level = 2
            return mock1, mock2, mock3, mock4, "level"

        def _get_character_info_mock_data(self):
            repo = self.database.character_info_repository
            model = repo.model
            chuuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            chuuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            uuid = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea201").bytes
            mock1 = model(character_uuid=chuuid1, uuid=uuid, type="ARCHER")
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.character_uuid = chuuid2
            mock4 = mock1.clone()
            mock4.type = "ASSASSIN"
            return mock1, mock2, mock3, mock4, "type"

        def _get_fazdb_uptime_mock_data(self):
            repo = self.database.fazdb_uptime_repository
            model = repo.model
            mock1 = model(
                start_time=self._get_mock_datetime().replace(day=1),
                stop_time=self._get_mock_datetime().replace(day=2),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.start_time = self._get_mock_datetime().replace(day=3, microsecond=0)
            mock4 = mock1.clone()
            mock4.stop_time = self._get_mock_datetime().replace(day=3, microsecond=0)
            return mock1, mock2, mock3, mock4, "stop_time"

        def _get_guild_history_mock_data(self):
            repo = self.database.guild_history_repository
            model = repo.model
            mock1 = model(
                name="a",
                level=1.0,
                territories=1,
                wars=1,
                member_total=1,
                online_members=1,
                datetime=self._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            del mock3.unique_id
            mock3.name = "b"
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.level = 2.0
            return mock1, mock2, mock3, mock4, "level"

        def _get_guild_info_mock_data(self):
            repo = self.database.guild_info_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(
                name="a", prefix="b", created=self._get_mock_datetime(), uuid=uuid1
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.prefix = "c"
            return mock1, mock2, mock3, mock4, "prefix"

        def _get_guild_member_history_mock_data(self):
            repo = self.database.guild_member_history_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(
                uuid=uuid1,
                contributed=1,
                joined=self._get_mock_datetime(),
                datetime=self._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            del mock3.unique_id
            mock3.uuid = uuid2
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.contributed = 2
            return mock1, mock2, mock3, mock4, "contributed"

        def _get_online_players_mock_data(self):
            repo = self.database.online_players_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(uuid=uuid1, server="a")
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.server = "b"
            return mock1, mock2, mock3, mock4, "server"

        def _get_player_activity_history_mock_data(self):
            repo = self.database.player_activity_history_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(
                uuid=uuid1,
                logon_datetime=self._get_mock_datetime(),
                logoff_datetime=self._get_mock_datetime().replace(day=1),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.logoff_datetime = self._get_mock_datetime().replace(day=2)
            return mock1, mock2, mock3, mock4, "logoff_datetime"

        # def get_player_guild_history_mock_data(self):
        #     repo = self.database.player_guild_history_repository
        #     model = repo.model

        def _get_player_history_mock_data(self):
            repo = self.database.player_history_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(
                uuid=uuid1,
                username="a",
                support_rank="c",
                playtime=1.0,
                guild_name="d",
                guild_rank="OWNER",
                rank="CHAMPION",
                datetime=self._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            del mock3.unique_id
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.username = "b"
            return mock1, mock2, mock3, mock4, "username"

        def _get_player_info_mock_data(self):
            repo = self.database.player_info_repository
            model = repo.model
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = model(
                uuid=uuid1, latest_username="a", first_join=self._get_mock_datetime()
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.latest_username = "b"
            return mock1, mock2, mock3, mock4, "latest_username"

        def _get_worlds_mock_data(self):
            repo = self.database.worlds_repository
            model = repo.model
            mock1 = model(
                name="WC1",
                player_count=1,
                time_created=self._get_mock_datetime().replace(day=1),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.name = "WC2"
            mock4 = mock1.clone()
            mock4.player_count = 2
            # mock4.time_created = datetime.now().replace(microsecond=0)
            return mock1, mock2, mock3, mock4, "player_count"
