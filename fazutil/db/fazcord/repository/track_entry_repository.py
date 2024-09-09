from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fazutil.db.base_repository import BaseRepository
from fazutil.db.fazcord.model.track_entry import TrackEntry

if TYPE_CHECKING:
    from fazutil.db.fazcord.fazcord_database import FazcordDatabase


class TrackEntryRepository(BaseRepository[TrackEntry, Any]):
    def __init__(self, database: FazcordDatabase) -> None:
        super().__init__(database, TrackEntry)
        self._database = database

    async def toggle(
        self,
        channel_id: int,
        *,
        session: AsyncSession | None = None,
    ) -> bool:
        # stmt = (
        #     update(self.model)
        #     .values(enabled=lambda: not self.model.enabled)  # Toggle the boolean column
        #     .where(self.model.channel_id == channel_id)
        # )
        async with self.database.must_enter_async_session(session) as ses:
            res = await self.select_by_channel_id(channel_id, session=ses)
            if res is None:
                raise ValueError(
                    f"Cannot find track_entry entry with channel id: {channel_id}"
                )
            res.enabled = not res.enabled
            await ses.commit()
            return res.enabled

    async def select_by_channel_id(
        self, channel_id: int, *, session: AsyncSession | None = None
    ) -> TrackEntry | None:
        stmt = select(self.model).where(self.model.channel_id == channel_id)
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalars().one_or_none()

    async def select_by_guild_id(
        self, guild_id, *, session: AsyncSession | None = None
    ) -> Sequence[TrackEntry]:
        channel_model = self._database.discord_channel.model
        guild_model = self._database.discord_guild.model
        stmt = (
            select(self.model)
            .join(channel_model, TrackEntry.channel_id == channel_model.channel_id)
            .join(guild_model, channel_model.guild_id == guild_model.guild_id)
            .where(guild_model.guild_id == guild_id)
        )
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalars().all()
