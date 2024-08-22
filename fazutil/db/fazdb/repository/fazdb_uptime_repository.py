from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.fazdb_uptime import FazdbUptime

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class FazdbUptimeRepository(BaseRepository[FazdbUptime, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, FazdbUptime)
