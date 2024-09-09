from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import nextcord
from dateparser import parse
from nextcord import Interaction, slash_command

from fazcord.bot.cog._cog_base import CogBase
from fazcord.bot.errors import BadArgument, ParseFailure
from fazcord.bot.view.activity_view import ActivityView
from fazcord.bot.view.guild_activity_view import GuildActivityView
from fazcord.bot.view.player_history_view import PlayerHistoryView


class WynnHistoryCog(CogBase):
    """Shows statistics from historical Wynncraft data."""

    @nextcord.slash_command()
    async def history(self, intr: Interaction[Any]) -> None: ...

    @history.subcommand()
    async def player_activity(
        self, intr: Interaction[Any], player: str, period: str
    ) -> None:
        """Shows player active time between the specified time period

        Args:
            player (str): The player username or UUID to check.
            period (str): The time period to check. Enter an integer to show active time past the last `n` hours,
                or enter a date-time range separated by '--' to specify a time range. Check
                dateparser.readthedocs.io for valid date-time formats. Max period is 6 months.

        Raises:
            BadArgument: If the player is not found.
            ParseFailure: If the period failed to be parsed
        """
        player_info = await self._bot.utils.must_get_wynn_player(player)
        period_begin, period_end = self._parse_period(intr, period)
        invoke = ActivityView(self._bot, intr, player_info, period_begin, period_end)
        await invoke.run()

    @history.subcommand()
    async def guild_activity(
        self, intr: Interaction[Any], guild: str, period: str
    ) -> None:
        """Shows players' active time in a given guild between the specified time period

        Args:
            guild (str): The guild name or UUID to check.
            period (str): The time period to check. Enter an integer to show active time past the last `n` hours,
                or enter a date-time range separated by '--' to specify a time range. Check
                dateparser.readthedocs.io for valid date-time formats. Max period is 6 months.

        Raises:
            BadArgument: If the player is not found.
            ParseFailure: If the period failed to be parsed
        """
        await intr.response.defer()
        guild_info = await self._bot.utils.must_get_wynn_guild(guild)
        period_begin, period_end = self._parse_period(intr, period)
        await GuildActivityView(
            self._bot,
            intr,
            guild_info,
            period_begin,
            period_end,
        ).run()

    @history.subcommand()
    async def player_history(
        self, intr: Interaction[Any], player: str, period: str
    ) -> None:
        """Show stat differences of a player between a time period.

        Args:
            player (str): The player username or UUID to check.
            period (str): The time period to check. Enter an integer to show active time past the last `n` hours,
                or enter a date-time range separated by '-' to specify a time range. Check
                dateparser.readthedocs.io for valid date-time formats. Max period is 6 months.

        Raises:
            BadArgument: If the player is not found.
            ParseFailure: If the period failed to be parsed
        """
        await intr.response.defer()
        player_info = await self._bot.utils.must_get_wynn_player(player)
        period_begin, period_end = self._parse_period(intr, period)
        await PlayerHistoryView(
            self._bot, intr, player_info, period_begin, period_end
        ).run()

    # @slash_command()
    # async def guild_history(
    #     self, intr: Interaction[Any], guild: str, period: str
    # ) -> None: ...

    # @slash_command()
    # async def member_history(
    #     self, intr: Interaction[Any], player: str, period: str
    # ) -> None: ...

    @staticmethod
    def _parse_period(intr: Interaction[Any], period: str) -> tuple[datetime, datetime]:
        try:
            if "--" in period:
                left, right = period.split("--")
                period_begin = parse(left)
                period_end = parse(right)
                WynnHistoryCog._check_period(period_begin)
                WynnHistoryCog._check_period(period_end)
            else:
                period_begin = intr.created_at - timedelta(hours=float(period))
                period_end = intr.created_at
        except ValueError as exc:
            raise ParseFailure(f"Can't parse period (reason: {exc})") from exc
        assert period_begin and period_end
        if period_end - period_begin > timedelta(days=182):
            raise BadArgument(
                "Can't parse period (reason: Period range cannot exceed 6 months.)"
            )
        return period_begin, period_end

    @staticmethod
    def _check_period(period: Any | None) -> None:
        if period is None:
            raise ParseFailure(
                f"Can't parse period (reason: Failed interpreting {period} as a datetime)"
            )
