from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable

import dateparser

from fazcord.bot.errors import BadArgument, ParseFailure
from fazutil.db.fazdb.model.guild_info import GuildInfo
from fazutil.db.fazdb.model.player_info import PlayerInfo

if TYPE_CHECKING:
    from nextcord import Client, Guild, Interaction, PartialMessageable, Thread, User
    from nextcord.abc import GuildChannel, PrivateChannel
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazcord.bot.bot import Bot

    type Channel = GuildChannel | Thread | PrivateChannel | PartialMessageable


class Utils:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def add_to_db(
        self,
        interaction: Interaction[Any],
        channel: Channel,
        session: AsyncSession,
    ) -> None:
        intr = interaction
        assert intr.user
        db = self._bot.fazcord_db
        guild_repo = db.discord_guild_repository
        channel_repo = db.discord_channel_repository
        user_repo = db.discord_user_repository
        await guild_repo.insert(
            guild_repo.model(guild_id=channel.guild.id, guild_name=channel.guild.name),  # type: ignore
            session=session,
            replace_on_duplicate=True,
            columns_to_replace=["guild_name"],
        )
        await channel_repo.insert(
            channel_repo.model(
                channel_id=channel.id,
                channel_name=channel.name,  # type: ignore
                guild_id=channel.guild.id,  # type: ignore
            ),
            session=session,
            replace_on_duplicate=True,
            columns_to_replace=["channel_name"],
        )
        await user_repo.insert(
            user_repo.model(user_id=intr.user.id, username=intr.user.display_name),
            session=session,
            replace_on_duplicate=True,
            columns_to_replace=["username"],
        )

    async def must_get_wynn_guild(self, guild: str) -> GuildInfo:
        guild_info = await self._bot.fazdb_db.guild_info_repository.get_guild(guild)
        if not guild_info:
            raise BadArgument(
                f"Guild not found (reason: Can't find guild with name or uuid {guild})"
            )
        return guild_info

    async def must_get_wynn_player(self, player: str) -> PlayerInfo:
        player_info = await self._bot.fazdb_db.player_info_repository.get_player(player)
        if not player_info:
            raise BadArgument(
                f"Player not found (reason: Can't find player with username or uuid {player})"
            )
        return player_info

    async def must_get_channel(self, channel_id: Any) -> Channel:
        channel = await self.must_get_id(self._bot.client.get_channel, channel_id)
        return channel

    async def must_get_sendable_channel(self, channel_id: Any) -> Channel:
        channel = await self.must_get_id(self._bot.client.get_channel, channel_id)
        if not hasattr(channel, "send"):
            raise ParseFailure(
                f"Channel with id {channel_id} does not support sending messages."
            )
        return channel

    async def must_get_guild(self, guild_id: Any) -> Guild:
        guild = await self.must_get_id(self._bot.client.get_guild, guild_id)
        return guild

    async def must_get_user(self, user_id: Any) -> User:
        user = await self.must_get_id(self._bot.client.get_user, user_id)
        return user

    @staticmethod
    async def must_get_id[T](get_strategy: Callable[[int], T | None], id_: Any) -> T:
        try:
            parsed_id = int(id_)
        except ParseFailure as exc:
            raise ParseFailure(f"Failed parsing {id_} into an integer.") from exc
        if not (ret := get_strategy(parsed_id)):
            raise ParseFailure(f"Failed getting object from ID {id_}")
        return ret

    @staticmethod
    def must_parse_date_string(datestr: str) -> datetime:
        date = dateparser.parse(datestr)
        if not date:
            raise ParseFailure(f"Failed parsing date string {datestr}")
        return date
