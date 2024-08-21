from __future__ import annotations

from datetime import timedelta
from typing import Any

import nextcord
from dateparser import parse
from nextcord import Interaction

from ..cog._cog_base import CogBase
from ..errors import BadArgument
from ..invoke import InvokeActivity


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

        await InvokeActivity(
            self._bot, intr, player_info, period_begin, period_end
        ).run()

    # @nextcord.slash_command(name="worldlist")
    # async def worldlist(
    #     self,
    #     interaction: Interaction[Any],
    #     sort_by: Literal["Player Count", "Time Created"] = "Time Created"
    # ) -> None:
    #     await InvokeWorldlist(self._bot, interaction, sort_by).run()
