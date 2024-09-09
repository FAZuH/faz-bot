from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.player_history import PlayerHistory

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class PlayerHistoryRepository(BaseRepository[PlayerHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, PlayerHistory)
