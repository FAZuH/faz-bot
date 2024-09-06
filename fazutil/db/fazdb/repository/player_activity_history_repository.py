from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Sequence

from sqlalchemy import and_, select

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.player_activity_history import PlayerActivityHistory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class PlayerActivityHistoryRepository(
    BaseRepository[PlayerActivityHistory, tuple[bytes, datetime]]
):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, PlayerActivityHistory)

    async def get_activities_between_period(
        self,
        player_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
        *,
        session: AsyncSession | None = None,
    ) -> Sequence[PlayerActivityHistory]:
        model = self.model
        stmt = select(model).where(
            and_(
                model.logoff_datetime >= period_begin,
                model.logon_datetime <= period_end,
                model.uuid == player_uuid,
            )
        )
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalars().all()

    async def get_playtime_between_period(
        self,
        player_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
        *,
        session: AsyncSession | None = None,
    ) -> timedelta:
        model = self.model
        stmt = select(model).where(
            and_(
                model.logoff_datetime >= period_begin,
                model.logon_datetime <= period_end,
                model.uuid == player_uuid,
            )
        )
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            activities = res.scalars().all()
        return self.get_activity_time(activities, period_begin, period_end)

    @staticmethod
    def get_activity_time(
        entities: Sequence[PlayerActivityHistory],
        period_begin: datetime,
        period_end: datetime,
    ) -> timedelta:
        res = 0
        begin_ts = period_begin.timestamp()
        end_ts = period_end.timestamp()
        for e in entities:
            on_ts = e.logon_datetime.timestamp()
            off_ts = e.logoff_datetime.timestamp()
            on = begin_ts if on_ts <= begin_ts else on_ts
            off = end_ts if off_ts >= end_ts else off_ts
            res += off - on
        ret = timedelta(seconds=res)
        return ret
