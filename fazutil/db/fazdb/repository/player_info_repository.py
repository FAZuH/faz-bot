from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import select

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.player_info import PlayerInfo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class PlayerInfoRepository(BaseRepository[PlayerInfo, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, PlayerInfo)

    async def get_player(
        self, username_or_uuid: str | bytes, *, session: AsyncSession | None = None
    ) -> PlayerInfo | None:
        model = self.model
        if isinstance(username_or_uuid, str):
            try:
                uuid = UUID(hex=username_or_uuid)
                stmt = select(model).where(model.uuid == uuid.bytes).limit(1)
            except ValueError:
                stmt = (
                    select(model)
                    .where(model.latest_username == username_or_uuid)
                    .limit(1)
                )
        else:
            stmt = select(model).where(model.uuid == username_or_uuid).limit(1)
        async with self._database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalar_one_or_none()
