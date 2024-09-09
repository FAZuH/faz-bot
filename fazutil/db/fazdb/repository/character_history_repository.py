from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.character_history import CharacterHistory

if TYPE_CHECKING:
    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class CharacterHistoryRepository(BaseRepository[CharacterHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, CharacterHistory)

    async def select_between_period(
        self,
        character_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
        *,
        session: AsyncSession | None = None,
    ) -> Sequence[CharacterHistory]:
        """Selects records for a given player within a specified period.

        This method queries the `PlayerHistory` model for records where the `datetime`
        field is within the specified period (`period_begin` to `period_end`) and
        matches the given player's UUID. The results are sorted by the `datetime` field
        in ascending order.

        Args:
            player_uuid (bytes): The UUID of the player as a byte string.
            period_begin (datetime): The start of the period to filter records.
            period_end (datetime): The end of the period to filter records.
            session (AsyncSession | None, optional): An optional asynchronous session
                to use for the database query. If not provided, a new session is created
                internally.

        Returns:
            Sequence[PlayerHistory]: A sequence of `PlayerHistory` objects matching the
            specified criteria, sorted by `datetime` in ascending order.
        """
        model = self.model
        stmt = (
            select(model)
            .where(
                and_(
                    model.datetime >= period_begin,
                    model.datetime <= period_end,
                    model.character_uuid == character_uuid,
                )
            )
            .order_by(self.model.datetime)
        )
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalars().all()
