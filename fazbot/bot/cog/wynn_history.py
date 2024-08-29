from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import nextcord
from dateparser import parse
from nextcord import Interaction

from fazbot.bot.cog._cog_base import CogBase
from fazbot.bot.errors import BadArgument
from fazbot.bot.view.activity_view import ActivityView
from fazbot.bot.view.guild_activity_view import GuildActivityView


class WynnHistory(CogBase):

    # @nextcord.slash_command()
    # async def history(self, intr: Interaction[Any]) -> None: ...

    @nextcord.slash_command()
    async def activity(self, intr: Interaction[Any], player: str, period: str) -> None:
        """
        Shows player active time between the specified time period

        Args:
            player (str): The player username or UUID to check.
            period (str): The time period to check. Enter an integer to show active time past the last `n` hours,
                or enter a date-time range separated by '-' to specify a time range. Check
                dateparser.readthedocs.io for valid date-time formats. Max period is 6 months.

        Raises:
            BadArgument: If the player is not found or an error occurred in parsing period.
        """
        # `player` check
        player_info = await self._bot.fazdb_db.player_info_repository.get_player(player)
        if not player_info:
            raise BadArgument(
                f"Player not found (reason: Can't find player with username or uuid {player})"
            )
        # `period` check and parse
        period_begin, period_end = self.__parse_period(intr, period)
        invoke = ActivityView(self._bot, intr, player_info, period_begin, period_end)  # type: ignore
        await invoke.run()

    @nextcord.slash_command()
    async def guild_activity(
        self, intr: Interaction[Any], guild: str, period: str
    ) -> None:
        """
        Shows players' active time in a given guild between the specified time period

        Args:
            guild (str): The guild name or UUID to check.
            period (str): The time period to check. Enter an integer to show active time past the last `n` hours,
                or enter a date-time range separated by '-' to specify a time range. Check
                dateparser.readthedocs.io for valid date-time formats. Max period is 6 months.

        Raises:
            BadArgument: If the player is not found or an error occurred in parsing period.
        """
        # `guild` check
        guild_info = await self._bot.fazdb_db.guild_info_repository.get_guild(guild)
        if not guild_info:
            raise BadArgument(
                f"Guild not found (reason: Can't find guild with name or uuid {guild})"
            )
        period_begin, period_end = self.__parse_period(intr, period)
        await GuildActivityView(
            self._bot,
            intr,
            guild_info,
            period_begin,
            period_end,
        ).run()

    @staticmethod
    def __parse_period(
        intr: Interaction[Any], period: str
    ) -> tuple[datetime, datetime]:
        try:
            if "-" in period:
                left, right = period.split("-")
                period_begin = parse(left)
                period_end = parse(right)
                WynnHistory.__check_period(period_begin)
                WynnHistory.__check_period(period_end)
            else:
                period_begin = intr.created_at - timedelta(hours=float(period))
                period_end = intr.created_at
        except ValueError as exc:
            raise BadArgument(f"Can't parse period (reason: {exc})") from exc
        assert period_begin and period_end
        if period_begin - period_end > timedelta(days=182):
            raise BadArgument(
                "Can't parse period (reason: The period range cannot exceed 6 months.)"
            )
        return period_begin, period_end

    @staticmethod
    def __check_period(period: Any | None) -> None:
        if period is None:
            raise BadArgument(
                f"Can't parse period (reason: Failed interpreting {period} as a datetime)"
            )
