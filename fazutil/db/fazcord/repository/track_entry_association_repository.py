from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazcord.model.track_entry_association import TrackEntryAssociation

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class TrackEntryAssociationRepository(BaseRepository[TrackEntryAssociation, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, TrackEntryAssociation)
