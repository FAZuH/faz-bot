from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazbot.model.discord_user import DiscordUser

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class DiscordUserRepository(BaseRepository[DiscordUser, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, DiscordUser)
