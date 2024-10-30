from typing import override
from fazutil.db.base_mysql_database import BaseMySQLDatabase
from fazutil.db.fazwynn.model.base_fazwynn_model import BaseFazwynnModel
from fazutil.db.fazwynn.repository.character_history_repository import (
    CharacterHistoryRepository,
)
from fazutil.db.fazwynn.repository.character_info_repository import (
    CharacterInfoRepository,
)
from fazutil.db.fazwynn.repository.fazdb_uptime_repository import FazdbUptimeRepository
from fazutil.db.fazwynn.repository.guild_history_repository import (
    GuildHistoryRepository,
)
from fazutil.db.fazwynn.repository.guild_info_repository import GuildInfoRepository
from fazutil.db.fazwynn.repository.guild_member_history_repository import (
    GuildMemberHistoryRepository,
)
from fazutil.db.fazwynn.repository.online_players_repository import (
    OnlinePlayersRepository,
)
from fazutil.db.fazwynn.repository.player_activity_history_repository import (
    PlayerActivityHistoryRepository,
)
from fazutil.db.fazwynn.repository.player_history_repository import (
    PlayerHistoryRepository,
)
from fazutil.db.fazwynn.repository.player_info_repository import PlayerInfoRepository
from fazutil.db.fazwynn.repository.worlds_repository import WorldsRepository


class FazwynnDatabase(BaseMySQLDatabase):
    def __init__(
        self, user: str, password: str, host: str, port: int, database: str
    ) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseFazwynnModel()

        self._character_history_repository = CharacterHistoryRepository(self)
        self._character_info_repository = CharacterInfoRepository(self)
        self._fazdb_uptime_repository = FazdbUptimeRepository(self)
        self._guild_history_repository = GuildHistoryRepository(self)
        self._guild_info_repository = GuildInfoRepository(self)
        self._guild_member_history_repository = GuildMemberHistoryRepository(self)
        self._online_players_repository = OnlinePlayersRepository(self)
        self._player_activity_history_repository = PlayerActivityHistoryRepository(self)
        self._player_history_repository = PlayerHistoryRepository(self)
        self._player_info_repository = PlayerInfoRepository(self)
        self._worlds_repository = WorldsRepository(self)

        self.repositories.extend(
            [
                self._character_history_repository,
                self._character_info_repository,
                self._fazdb_uptime_repository,
                self._guild_history_repository,
                self._guild_info_repository,
                self._guild_member_history_repository,
                self._online_players_repository,
                self._player_activity_history_repository,
                self._player_history_repository,
                self._player_info_repository,
                self._worlds_repository,
            ]
        )

    @property
    def character_history(self) -> CharacterHistoryRepository:
        return self._character_history_repository

    @property
    def character_info(self) -> CharacterInfoRepository:
        return self._character_info_repository

    @property
    def fazdb_uptime(self) -> FazdbUptimeRepository:
        return self._fazdb_uptime_repository

    @property
    def guild_history(self) -> GuildHistoryRepository:
        return self._guild_history_repository

    @property
    def guild_info(self) -> GuildInfoRepository:
        return self._guild_info_repository

    @property
    def guild_member_history(self) -> GuildMemberHistoryRepository:
        return self._guild_member_history_repository

    @property
    def online_players(self) -> OnlinePlayersRepository:
        return self._online_players_repository

    @property
    def player_activity_history(self) -> PlayerActivityHistoryRepository:
        return self._player_activity_history_repository

    @property
    def player_history(self) -> PlayerHistoryRepository:
        return self._player_history_repository

    @property
    def player_info(self) -> PlayerInfoRepository:
        return self._player_info_repository

    @property
    def worlds(self) -> WorldsRepository:
        return self._worlds_repository

    @property
    @override
    def base_model(self) -> BaseFazwynnModel:
        return self._base_model
