from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import select

from ...base_repository import BaseRepository
from ..model import GuildInfo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from ...base_mysql_database import BaseMySQLDatabase


class GuildInfoRepository(BaseRepository[GuildInfo, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildInfo)

    async def get_guild(
        self, name_or_uuid: str | bytes, *, session: AsyncSession | None = None
    ) -> GuildInfo | None:
        model = self.model
        if isinstance(name_or_uuid, str):
            try:
                uuid = UUID(hex=name_or_uuid)
                stmt = select(model).where(model.uuid == uuid.bytes).limit(1)
            except ValueError:
                stmt = select(model).where(model.name == name_or_uuid).limit(1)
        else:
            stmt = select(model).where(model.uuid == name_or_uuid).limit(1)
        async with self._database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalar_one_or_none()
