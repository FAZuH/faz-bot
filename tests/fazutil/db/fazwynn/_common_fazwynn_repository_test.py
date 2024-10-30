from __future__ import annotations

from abc import ABC
from datetime import timedelta
from typing import TYPE_CHECKING, override
from uuid import UUID

from fazutil.db.fazwynn.fazwynn_database import FazwynnDatabase
from fazutil.db.fazwynn.model.character_history import CharacterHistory
from fazutil.db.fazwynn.model.character_info import CharacterInfo
from fazutil.db.fazwynn.model.fazdb_uptime import FazdbUptime
from fazutil.db.fazwynn.model.guild_history import GuildHistory
from fazutil.db.fazwynn.model.guild_info import GuildInfo
from fazutil.db.fazwynn.model.guild_member_history import GuildMemberHistory
from fazutil.db.fazwynn.model.online_players import OnlinePlayers
from fazutil.db.fazwynn.model.player_activity_history import PlayerActivityHistory
from fazutil.db.fazwynn.model.player_history import PlayerHistory
from fazutil.db.fazwynn.model.player_info import PlayerInfo
from fazutil.db.fazwynn.model.worlds import Worlds
from tests.fazutil.db.common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazutil.db.base_repository import BaseRepository


class CommonFazwynnRepositoryTest:
    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazwynnDatabase, R], ABC):
        @property
        @override
        def database_type(self) -> type[FazwynnDatabase]:
            return FazwynnDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "faz-wynn_test"

        @classmethod
        def _get_character_history_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = CharacterHistory(
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
                datetime=cls._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            del mock3.unique_id
            mock3.character_uuid = uuid2
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.level = 2
            return mock1, mock2, mock3, mock4, "level"

        @classmethod
        def _get_character_info_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = CharacterInfo(character_uuid=uuid1, uuid=uuid1, type="ARCHER")
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.character_uuid = uuid2
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.type = "ASSASSIN"
            return mock1, mock2, mock3, mock4, "type"

        @classmethod
        def _get_fazdb_uptime_mock_data(cls):
            mock1 = FazdbUptime(
                start_time=cls._get_mock_datetime().replace(day=1),
                stop_time=cls._get_mock_datetime().replace(day=2),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.start_time = cls._get_mock_datetime().replace(day=3, microsecond=0)
            mock4 = mock1.clone()
            mock4.stop_time = cls._get_mock_datetime().replace(day=3, microsecond=0)
            return mock1, mock2, mock3, mock4, "stop_time"

        @classmethod
        def _get_guild_history_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = GuildHistory(
                uuid=uuid1,
                level=1.0,
                territories=1,
                wars=1,
                member_total=1,
                online_members=1,
                datetime=cls._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            del mock3.unique_id
            mock3.uuid = uuid2
            mock3.datetime += timedelta(seconds=10)
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.level = 2.0
            return mock1, mock2, mock3, mock4, "level"

        @classmethod
        def _get_guild_info_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = GuildInfo(
                name="a", prefix="b", created=cls._get_mock_datetime(), uuid=uuid1
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.name = "b"
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.prefix = "c"
            return mock1, mock2, mock3, mock4, "prefix"

        @classmethod
        def _get_guild_member_history_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = GuildMemberHistory(
                uuid=uuid1,
                contributed=1,
                joined=cls._get_mock_datetime(),
                datetime=cls._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            del mock3.unique_id
            mock3.uuid = uuid2
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.contributed = 2
            return mock1, mock2, mock3, mock4, "contributed"

        @classmethod
        def _get_online_players_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = OnlinePlayers(uuid=uuid1, server="a")
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.server = "b"
            return mock1, mock2, mock3, mock4, "server"

        @classmethod
        def _get_player_activity_history_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = PlayerActivityHistory(
                uuid=uuid1,
                logon_datetime=cls._get_mock_datetime(),
                logoff_datetime=cls._get_mock_datetime().replace(day=1),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.logoff_datetime = cls._get_mock_datetime().replace(day=2)
            return mock1, mock2, mock3, mock4, "logoff_datetime"

        # def get_player_guild_history_mock_data(cls):
        #     repo = self.database.player_guild_history_repository
        #     model = repo.model

        @classmethod
        def _get_player_history_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = PlayerHistory(
                uuid=uuid1,
                username="a",
                support_rank="c",
                playtime=1.0,
                guild_name="d",
                guild_rank="OWNER",
                rank="CHAMPION",
                datetime=cls._get_mock_datetime(),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            del mock3.unique_id
            mock3 = mock3.clone()
            mock4 = mock1.clone()
            mock4.username = "b"
            return mock1, mock2, mock3, mock4, "username"

        @classmethod
        def _get_player_info_mock_data(cls):
            uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
            uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
            mock1 = PlayerInfo(
                uuid=uuid1, latest_username="a", first_join=cls._get_mock_datetime()
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.uuid = uuid2
            mock4 = mock1.clone()
            mock4.latest_username = "b"
            return mock1, mock2, mock3, mock4, "latest_username"

        @classmethod
        def _get_worlds_mock_data(cls):
            mock1 = Worlds(
                name="WC1",
                player_count=1,
                time_created=cls._get_mock_datetime().replace(day=1),
            )
            mock2 = mock1.clone()
            mock3 = mock1.clone()
            mock3.name = "WC2"
            mock4 = mock1.clone()
            mock4.player_count = 2
            # mock4.time_created = datetime.now().replace(microsecond=0)
            return mock1, mock2, mock3, mock4, "player_count"
