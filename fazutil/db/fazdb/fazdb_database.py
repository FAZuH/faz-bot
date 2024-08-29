from fazutil.db.base_mysql_database import BaseMySQLDatabase
from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel
from fazutil.db.fazdb.repository.character_history_repository import (
    CharacterHistoryRepository,
)
from fazutil.db.fazdb.repository.character_info_repository import (
    CharacterInfoRepository,
)
from fazutil.db.fazdb.repository.fazdb_uptime_repository import FazdbUptimeRepository
from fazutil.db.fazdb.repository.guild_history_repository import GuildHistoryRepository
from fazutil.db.fazdb.repository.guild_info_repository import GuildInfoRepository
from fazutil.db.fazdb.repository.guild_member_history_repository import (
    GuildMemberHistoryRepository,
)
from fazutil.db.fazdb.repository.online_players_repository import (
    OnlinePlayersRepository,
)
from fazutil.db.fazdb.repository.player_activity_history_repository import (
    PlayerActivityHistoryRepository,
)
from fazutil.db.fazdb.repository.player_history_repository import (
    PlayerHistoryRepository,
)
from fazutil.db.fazdb.repository.player_info_repository import PlayerInfoRepository
from fazutil.db.fazdb.repository.worlds_repository import WorldsRepository


class FazdbDatabase(BaseMySQLDatabase):

    def __init__(
        self, user: str, password: str, host: str, port: int, database: str
    ) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseFazdbModel()

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
    def character_history_repository(self) -> CharacterHistoryRepository:
        return self._character_history_repository

    @property
    def character_info_repository(self) -> CharacterInfoRepository:
        return self._character_info_repository

    @property
    def fazdb_uptime_repository(self) -> FazdbUptimeRepository:
        return self._fazdb_uptime_repository

    @property
    def guild_history_repository(self) -> GuildHistoryRepository:
        return self._guild_history_repository

    @property
    def guild_info_repository(self) -> GuildInfoRepository:
        return self._guild_info_repository

    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryRepository:
        return self._guild_member_history_repository

    @property
    def online_players_repository(self) -> OnlinePlayersRepository:
        return self._online_players_repository

    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryRepository:
        return self._player_activity_history_repository

    @property
    def player_history_repository(self) -> PlayerHistoryRepository:
        return self._player_history_repository

    @property
    def player_info_repository(self) -> PlayerInfoRepository:
        return self._player_info_repository

    @property
    def worlds_repository(self) -> WorldsRepository:
        return self._worlds_repository

    @property
    def base_model(self) -> BaseFazdbModel:
        return self._base_model
