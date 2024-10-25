from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Sequence, override

from nextcord import Color, Embed
from sortedcontainers import SortedList
from tabulate import tabulate

from fazcord.bot.view._base_pagination_view import BasePaginationView
from fazcord.bot.view._pagination_embed import PaginationEmbed
from fazcord.bot.view._view_utils import ViewUtils
from fazutil.db.fazdb.model.player_activity_history import PlayerActivityHistory

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazcord.bot.bot import Bot
    from fazutil.db.fazdb.model.guild_info import GuildInfo


class HistoryGuildActivityView(BasePaginationView):
    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        guild: GuildInfo,
        period_begin: datetime,
        period_end: datetime,
    ) -> None:
        super().__init__(bot, interaction, timeout=120)
        self._guild = guild
        self._period_begin = period_begin
        self._period_end = period_end

        self._activity_res: SortedList = SortedList()

    @override
    async def run(self) -> None:
        await self._guild.awaitable_attrs.members
        members = self._guild.members
        repo = self._bot.fazdb_db.player_activity_history

        for player in members:
            entities = await repo.get_activities_between_period(
                player.uuid, self._period_begin, self._period_end
            )
            playtime = self._get_activity_time(
                entities, self._period_begin, self._period_end
            )
            activity_result = self.ActivityResult(player.latest_username, playtime)
            if activity_result.playtime.total_seconds() < 60:
                continue
            self._activity_res.add(activity_result)

        self._embed = PaginationEmbed(
            self._interaction,
            self._activity_res,
            title="Guild Members Activity",
            color=Color.teal(),
        )
        await self._interaction.send(embed=self._get_embed_page(1), view=self)

    def _get_embed_page(self, page: int = 1) -> Embed:
        begin_ts = int(self._period_begin.timestamp())
        end_ts = int(self._period_end.timestamp())
        embed = self._embed.get_base()
        results = embed.get_items(page)

        embed.description = f"`Guild  : `{self._guild.name}\n"
        embed.description += f"`Period : `<t:{begin_ts}:R> to <t:{end_ts}:R>"
        if len(results) == 0:
            embed.description = (
                "```ml\nNo guild members were recorded online at this time period.\n```"
            )
        else:
            embed.description += (
                "\n```ml\n"
                + tabulate(
                    [
                        [n, res.username, res.playtime_string]  # type: ignore
                        for n, res in enumerate(reversed(results), 1)
                    ],
                    headers=["No", "Username", "Activity"],
                    tablefmt="github",
                )
                + "\n```"
            )

        embed.finalize()
        return embed

    @staticmethod
    def _get_activity_time(
        entities: Sequence[PlayerActivityHistory],
        period_begin: datetime,
        period_end: datetime,
    ) -> timedelta:
        res = 0
        begin_ts = period_begin.timestamp()
        end_ts = period_end.timestamp()
        for e in entities:
            on_ts = e.logon_datetime.timestamp()
            off_ts = e.logoff_datetime.timestamp()
            on = begin_ts if on_ts <= begin_ts else on_ts
            off = end_ts if off_ts >= end_ts else off_ts
            res += off - on
        ret = timedelta(seconds=res)
        return ret

    class ActivityResult:
        def __init__(self, username: str, playtime: timedelta) -> None:
            self._username = username
            self._playtime = playtime
            self._playtime_string = ViewUtils.format_timedelta(playtime)

        @property
        def username(self) -> str:
            return self._username

        @property
        def playtime(self) -> timedelta:
            return self._playtime

        @property
        def playtime_string(self) -> str:
            return self._playtime_string

        def __lt__(self, other: int) -> bool:
            if isinstance(other, HistoryGuildActivityView.ActivityResult):
                return self.playtime < other.playtime
            return NotImplemented

        def __eq__(self, other: object) -> bool:
            if isinstance(other, HistoryGuildActivityView.ActivityResult):
                return self.playtime == other.playtime
            return NotImplemented
