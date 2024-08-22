from __future__ import annotations

from datetime import timedelta
from typing import Any

import nextcord
from dateparser import parse
from nextcord import Interaction

from fazbot.bot.cog._cog_base import CogBase
from fazbot.bot.errors import BadArgument
from fazbot.bot.invoke.invoke_activity import InvokeActivity
from fazbot.bot.invoke.invoke_guild_activity import InvokeGuildActivity


class WynnHistory(CogBase):

    # @nextcord.slash_command()
    # async def history(self, intr: Interaction[Any]) -> None: ...

    @nextcord.slash_command()
    async def activity(self, intr: Interaction[Any], player: str, period: str) -> None:
        # `player` check
        player_info = await self._bot.fazdb_db.player_info_repository.get_player(player)
        if not player_info:
            raise BadArgument(
                f"Player not found (reason: Can't find player with username or uuid {player})"
            )
        # `period` check and parse
        try:
            if "-" in period:
                left, right = period.split("-")
                period_begin = parse(left)
                period_end = parse(right)
                assert period_begin and period_end
            else:
                period_begin = intr.created_at - timedelta(hours=float(period))
                period_end = intr.created_at
        except ValueError as exc:
            raise BadArgument(f"Can't parse period (reason: {exc})") from exc
        invoke = InvokeActivity(self._bot, intr, player_info, period_begin, period_end)
        await invoke.run()

    @nextcord.slash_command()
    async def guild_activity(
        self, intr: Interaction[Any], guild: str, period: str
    ) -> None:
        # `guild` check
        guild_info = await self._bot.fazdb_db.guild_info_repository.get_guild(guild)
        if not guild_info:
            raise BadArgument(
                f"Player not found (reason: Can't find guild with name or uuid {guild})"
            )
        # `period` check and parse
        try:
            if "-" in period:
                left, right = period.split("-")
                period_begin = parse(left)
                period_end = parse(right)
                assert period_begin and period_end
            else:
                period_begin = intr.created_at - timedelta(hours=float(period))
                period_end = intr.created_at
        except ValueError as exc:
            raise BadArgument(f"Can't parse period (reason: {exc})") from exc
        await InvokeGuildActivity(
            self._bot, intr, guild_info, period_begin, period_end
        ).run()
