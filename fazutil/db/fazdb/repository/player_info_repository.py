from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import select

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazdb.model.player_info import PlayerInfo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazutil.db.fazdb.fazdb_database import FazdbDatabase


class PlayerInfoRepository(BaseRepository[PlayerInfo, Any]):
    def __init__(self, database: FazdbDatabase) -> None:
        self._database = database
        super().__init__(database, PlayerInfo)

    async def safe_insert(
        self,
        entity: Iterable[PlayerInfo] | PlayerInfo,
        *,
        session: None | AsyncSession = None,
        ignore_on_duplicate: bool = False,
        replace_on_duplicate: bool = False,
        columns_to_replace: Iterable[str] | None = None,
    ) -> None:
        """Safely inserts one or more `PlayerInfo` entities into the database.

        This method first checks if the guild associated with the player exists. If not, it adds a dummy guild entry
        with minimal information. After ensuring the guild exists, it proceeds to insert the `PlayerInfo` entities.

        Args:
            entity (Union[Iterable[PlayerInfo], PlayerInfo]): An entity or an iterable of `PlayerInfo` entities to be inserted into the database.
            session (AsyncSession, optional): An optional SQLAlchemy async session to use for the database connection. If not provided, a new session will be created.
            ignore_on_duplicate (bool, optional): Whether to ignore duplicate entries. Defaults to `False`.
            replace_on_duplicate (bool, optional): Whether to replace duplicate entries. Defaults to `False`. Note that `ignore_on_duplicate` and `replace_on_duplicate` cannot both be `True`.
            columns_to_replace (Union[Iterable[str], None], optional): List of columns to replace if a duplicate entry is found. If `None`, all non-primary key columns will be replaced.

        Raises:
            ValueError: If both `ignore_on_duplicate` and `replace_on_duplicate` are set to `True`.
        """
        guild_repo = self._database.guild_info_repository
        guild_model = guild_repo.model
        to_insert_guild = [
            # NOTE: illegal guild name. Still select-able if someone deliberately searches
            #   for guild with name '-' with the app, though the impact is minimal.
            guild_model(uuid=e.guild_uuid, name="-", prefix="-", created=datetime.now())
            for e in self._ensure_iterable(entity)
            if e.guild_uuid is not None
        ]
        if to_insert_guild:
            await guild_repo.insert(to_insert_guild, ignore_on_duplicate=True)
        await self.insert(
            entity,
            session=session,
            ignore_on_duplicate=ignore_on_duplicate,
            replace_on_duplicate=replace_on_duplicate,
            columns_to_replace=columns_to_replace,
        )

    async def get_player(
        self, username_or_uuid: str | bytes, *, session: AsyncSession | None = None
    ) -> PlayerInfo | None:
        """
        Retrieves a player record based on a username or UUID.

        Args:
            username_or_uuid (Union[str, bytes]): The player's username or UUID. If a string is provided, it will be treated as a UUID if it is in a valid UUID format; otherwise, it will be treated as a username.
            session (AsyncSession, optional): An optional SQLAlchemy async session to use for the query. If not provided, a new session will be created.

        Returns:
            PlayerInfo | None: The player record if found; otherwise, `None`.
        """
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
