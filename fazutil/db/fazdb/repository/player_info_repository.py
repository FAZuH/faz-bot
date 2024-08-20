from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import text

from ...base_repository import BaseRepository
from ..model import PlayerInfo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ...base_mysql_database import BaseMySQLDatabase


class PlayerInfoRepository(BaseRepository[PlayerInfo, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, PlayerInfo)

    async def is_exist_player(
        self, username_or_uuid: str, *, session: AsyncSession | None = None
    ) -> bool | None:
        sql = """
            SELECT EXISTS(
                SELECT 1
                FROM your_table_name
                WHERE uuid = :username_or_uuid
                   OR latest_username = :username_or_uuid
            ) AS record_exists;
        """
        params = {"username_or_uuid": username_or_uuid}
        async with self._database.must_enter_async_session(session) as session:
            res = await session.execute(text(sql), params)
            row = res.fetchone()
            ret = row["record_exists"] == 1  # type: ignore
        return ret
