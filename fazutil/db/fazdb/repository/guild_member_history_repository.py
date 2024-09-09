from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.guild_member_history import GuildMemberHistory

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class GuildMemberHistoryRepository(BaseRepository[GuildMemberHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildMemberHistory)
