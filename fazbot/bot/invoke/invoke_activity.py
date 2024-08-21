from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from nextcord import Color, Embed

from ..invoke._invoke import Invoke

if TYPE_CHECKING:
    from datetime import timedelta

    from nextcord import Interaction

    from fazutil.db.fazdb.model import PlayerInfo

    from ..bot import Bot


class InvokeActivity(Invoke):

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        player: PlayerInfo,
        period_begin: datetime,
        period_end: datetime,
    ) -> None:
        super().__init__(bot, interaction)
        self._player = player
        self._period_begin = period_begin
        self._period_end = period_end

    @override
    async def run(self) -> None:
        embed = await self._get_embed()
        await self._interaction.send(embed=embed)

    async def _get_embed(self) -> Embed:
        begin = self._period_begin
        begin_ts = int(begin.timestamp())
        end = self._period_end
        end_ts = int(end.timestamp())
        assert self._interaction.user
        repo = self._bot.fazdb_db.player_activity_history_repository

        player_activities = await repo.select_between_period(
            self._player.uuid, begin, end
        )
        embed = Embed(
            title=f"Player Activity ({self._player.latest_username})",
            color=Color.teal(),
        )
        embed.set_author(
            name=self._interaction.user.display_name,
            icon_url=self._interaction.user.display_avatar.url,
        )
        time_period = repo.get_activity_time(player_activities, begin, end)
        embed.description = f"Playtime (<t:{begin_ts}:R>, <t:{end_ts}:R>): `{self._format_time_delta(time_period)}`"
        return embed

    def _format_time_delta(self, timedelta: timedelta) -> str:
        total_seconds = int(timedelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        formatted_time = f"{hours}h {minutes}m"
        return formatted_time
