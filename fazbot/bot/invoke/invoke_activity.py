from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from nextcord import Color, Embed

from fazutil.db.fazdb.model.player_activity_history import PlayerActivityHistory

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
        self._repo = self._bot.fazdb_db.player_activity_history_repository

    @override
    async def run(self) -> None:
        player_activities = await self._repo.select_between_period(
            self._player.uuid, self._period_begin, self._period_end
        )
        embed = await self._get_embed(player_activities)
        await self._interaction.send(embed=embed)

    async def _get_embed(
        self, player_activities: Sequence[PlayerActivityHistory]
    ) -> Embed:
        begin_ts = int(self._period_begin.timestamp())
        end_ts = int(self._period_end.timestamp())
        assert self._interaction.user
        embed = Embed(
            title=f"Player Activity ({self._player.latest_username})",
            color=Color.teal(),
        )
        embed.set_author(
            name=self._interaction.user.display_name,
            icon_url=self._interaction.user.display_avatar.url,
        )
        time_period = self._repo.get_activity_time(
            player_activities, self._period_begin, self._period_end
        )
        embed.description = f"Playtime (<t:{begin_ts}:R>, <t:{end_ts}:R>): `{self._format_time_delta(time_period)}`"
        return embed

    def _format_time_delta(self, timedelta: timedelta) -> str:
        total_seconds = int(timedelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        formatted_time = f"{hours}h {minutes}m"
        return formatted_time
