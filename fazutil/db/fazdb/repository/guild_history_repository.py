from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.guild_history import GuildHistory

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class GuildHistoryRepository(BaseRepository[GuildHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildHistory)
