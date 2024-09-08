from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable

import dateparser
from nextcord import PartialMessage

from fazcord.bot.errors import ParseFailure

if TYPE_CHECKING:
    from nextcord import Client, Guild, Interaction, PartialMessageable, Thread, User
    from nextcord.abc import GuildChannel, PrivateChannel
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazcord.bot.bot import Bot

    type Channel = GuildChannel | Thread | PrivateChannel | PartialMessageable


class Utils:

    @staticmethod
    async def add_to_db(
        bot: Bot,
        interaction: Interaction[Any],
        channel: Channel,
        session: AsyncSession,
    ) -> None:
        intr = interaction
        assert intr.user
        db = bot.fazcord_db
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
                channel_id=channel.id, channel_name=channel.name, guild_id=channel.guild.id  # type: ignore
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

    @staticmethod
    async def must_get_channel(client: Client, channel_id: Any) -> Channel:
        return await Utils.must_get_id(client.get_channel, channel_id)

    @staticmethod
    async def must_get_sendable_channel(client: Client, channel_id: Any) -> Channel:
        channel = await Utils.must_get_id(client.get_channel, channel_id)
        if not hasattr(channel, "send"):
            raise ParseFailure(
                f"Channel with id {channel_id} does not support sending messages."
            )
        return channel

    @staticmethod
    async def must_get_guild(client: Client, guild_id: Any) -> Guild:
        return await Utils.must_get_id(client.get_guild, guild_id)

    @staticmethod
    async def must_get_user(client: Client, user_id: Any) -> User:
        return await Utils.must_get_id(client.get_user, user_id)

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
