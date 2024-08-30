from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from nextcord import Color, Embed

from fazbot.bot.view._base_view import BaseView
from fazbot.bot.view._custom_embed import CustomEmbed
from fazbot.bot.view._view_utils import ViewUtils

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazbot.bot.bot import Bot
    from fazutil.db.fazdb.model.player_info import PlayerInfo


class ActivityView(BaseView):

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
        embed = await self._get_embed()
        await self._interaction.send(embed=embed)

    async def _get_embed(self) -> Embed:
        begin_ts = int(self._period_begin.timestamp())
        end_ts = int(self._period_end.timestamp())
        assert self._interaction.user

        embed = CustomEmbed(
            self._interaction,
            title=f"Player Activity ({self._player.latest_username})",
            color=Color.teal(),
        )
        time_period = await self._repo.get_playtime_between_period(
            self._player.uuid, self._period_begin, self._period_end
        )
        embed.description = f"`Playtime : ` {ViewUtils.format_timedelta(time_period)}"
        embed.description += f"\n`Period   : ` <t:{begin_ts}:R> to <t:{end_ts}:R>"
        embed.finalize()
        return embed
