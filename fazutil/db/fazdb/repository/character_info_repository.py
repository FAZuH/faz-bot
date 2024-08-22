from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.character_info import CharacterInfo

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class CharacterInfoRepository(BaseRepository[CharacterInfo, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, CharacterInfo)
