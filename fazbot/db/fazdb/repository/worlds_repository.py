from __future__ import annotations
from typing import Any, Iterable, Literal, Sequence, TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import Worlds
from loguru import logger

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..._base_mysql_database import BaseMySQLDatabase


class WorldsRepository(BaseRepository[Worlds, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, Worlds)

    async def update_worlds(self, entity: Iterable[Worlds], *, session: AsyncSession | None = None) -> None:
        """Deletes worlds that's not up anymore, and updates player_count for worlds that's still up"""
        stmt = self.table.delete().where(self.model.name.not_in([e.name for e in entity]))
        async with self.database.enter_async_session() as session:
            await session.execute(stmt)
            await self.insert(entity, session=session, replace_on_duplicate=True, columns_to_replace=["player_count"])

    async def get_worlds(self, sortby: Literal["player", "time"]) -> Sequence[Worlds]:
        orderby_ = self.model.player_count if sortby == "player" else self.model.time_created
        # stmt = self.table.select().order_by(orderby_)
        stmt = self.table.select()
        async with self.database.enter_async_session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()
