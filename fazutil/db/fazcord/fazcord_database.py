from fazutil.db.base_mysql_database import BaseMySQLDatabase
from fazutil.db.fazcord.model.base_fazcord_model import BaseFazcordModel
from fazutil.db.fazcord.repository.discord_channel_repository import (
    DiscordChannelRepository,
)
from fazutil.db.fazcord.repository.discord_guild_repository import (
    DiscordGuildRepository,
)
from fazutil.db.fazcord.repository.discord_user_repository import DiscordUserRepository
from fazutil.db.fazcord.repository.track_entry_association_repository import (
    TrackEntryAssociationRepository,
)
from fazutil.db.fazcord.repository.track_entry_repository import TrackEntryRepository
from fazutil.db.fazcord.repository.whitelist_group_repository import (
    WhitelistGroupRepository,
)


class FazcordDatabase(BaseMySQLDatabase):

    def __init__(
        self, user: str, password: str, host: str, port: int, database: str
    ) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseFazcordModel()

        self._discord_channel_repository = DiscordChannelRepository(self)
        self._discord_guild_repository = DiscordGuildRepository(self)
        self._discord_user_repository = DiscordUserRepository(self)
        self._track_entry_association_repository = TrackEntryAssociationRepository(self)
        self._track_entry_repository = TrackEntryRepository(self)
        self._whitelist_group_repository = WhitelistGroupRepository(self)
        self.repositories.append(self.whitelist_group_repository)

    @property
    def discord_channel_repository(self) -> DiscordChannelRepository:
        return self._discord_channel_repository

    @property
    def discord_guild_repository(self) -> DiscordGuildRepository:
        return self._discord_guild_repository

    @property
    def discord_user_repository(self) -> DiscordUserRepository:
        return self._discord_user_repository

    @property
    def track_entry_association_repository(self) -> TrackEntryAssociationRepository:
        return self._track_entry_association_repository

    @property
    def track_entry_repository(self) -> TrackEntryRepository:
        return self._track_entry_repository

    @property
    def whitelist_group_repository(self) -> WhitelistGroupRepository:
        return self._whitelist_group_repository

    @property
    def base_model(self) -> BaseFazcordModel:
        return self._base_model
