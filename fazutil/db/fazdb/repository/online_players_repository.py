from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.online_players import OnlinePlayers

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazutil.db.base_mysql_database import BaseMySQLDatabase


class OnlinePlayersRepository(BaseRepository[OnlinePlayers, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, OnlinePlayers)

    async def update(
        self, entities: list[OnlinePlayers], *, session: AsyncSession | None = None
    ) -> None:
        # TODO: confirm this works properly
        async with self.database.must_enter_async_session(session) as s:
            await self.truncate(session=s)
            await self.insert(entities, session=s)
