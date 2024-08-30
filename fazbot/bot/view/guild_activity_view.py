from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from nextcord import Button, ButtonStyle, Color, Embed
from nextcord.ui import Button, button
from sortedcontainers import SortedList
from tabulate import tabulate

from fazbot.bot.view._base_view import BaseView
from fazbot.bot.view._custom_embed import CustomEmbed
from fazbot.bot.view._view_utils import ViewUtils

if TYPE_CHECKING:
    from datetime import timedelta

    from nextcord import Interaction

    from fazbot.bot.bot import Bot
    from fazutil.db.fazdb.model.guild_info import GuildInfo


class GuildActivityView(BaseView):

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

        self._current_page = 1
        self._items_per_page = 20
        self._page_count: int
        self._activity_res: SortedList = SortedList()

    @override
    async def run(self) -> None:
        await self._guild.awaitable_attrs.members
        members = self._guild.members
        repo = self._bot.fazdb_db.player_activity_history_repository
        for player in members:
            playtime = await repo.get_playtime_between_period(
                player.uuid, self._period_begin, self._period_end
            )
            activity_result = self.ActivityResult(player.latest_username, playtime)
            if activity_result.playtime_seconds < 60:
                continue
            self._activity_res.add(activity_result)
        self._page_count = len(self._activity_res) // self._items_per_page
        embed = self._get_embed_page(1)
        await self._interaction.send(embed=embed, view=self)

    def _get_embed_page(self, page: int) -> Embed:
        begin_ts = int(self._period_begin.timestamp())
        end_ts = int(self._period_end.timestamp())
        embed = CustomEmbed(
            self._interaction,
            title=f"Guild Members Activity ",
            color=Color.teal(),
        )
        embed.description = f"`Guild:  `{self._guild.name})\n`Period: `<t:{begin_ts}:R>, <t:{end_ts}:R>`"
        left_index = self._items_per_page * (page - 1)
        right_index = self._items_per_page * page
        results = self._activity_res[left_index:right_index]
        embed.description = (
            "```ml\n"
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
        embed.add_field(name="Page", value=f"{page} / {self._page_count}", inline=False)
        return embed

    @button(style=ButtonStyle.blurple, emoji="⏮️")
    async def first_page_callback(
        self, button: Button, interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._current_page = 1
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="◀️")
    async def previous_page_callback(
        self, button: Button, interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._current_page -= 1
        if self._current_page == 0:
            self._current_page = self._page_count
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.red, emoji="⏹️")
    async def stop_(self, button: Button, interaction: Interaction[Any]) -> None:
        await self.on_timeout()

    @button(style=ButtonStyle.blurple, emoji="▶️")
    async def next_page(self, button: Button, interaction: Interaction[Any]) -> None:
        await interaction.response.defer()
        self._current_page += 1
        if self._current_page == (self._page_count + 1):
            self._current_page = 1
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="⏭️")
    async def last_page(self, button: Button, interaction: Interaction[Any]) -> None:
        await interaction.response.defer()
        self._current_page = self._page_count
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    class ActivityResult:

        def __init__(self, username: str, playtime: timedelta) -> None:
            self._username = username
            self._playtime_seconds = playtime.total_seconds()
            self._playtime_string = ViewUtils.format_timedelta(playtime)

        @property
        def username(self) -> str:
            return self._username

        @property
        def playtime_seconds(self) -> float:
            return self._playtime_seconds

        @property
        def playtime_string(self) -> str:
            return self._playtime_string

        def __lt__(self, other: int) -> bool:
            if isinstance(other, GuildActivityView.ActivityResult):
                return self.playtime_seconds < other.playtime_seconds
            return NotImplemented

        def __eq__(self, other: object) -> bool:
            if isinstance(other, GuildActivityView.ActivityResult):
                return self.playtime_seconds == other.playtime_seconds
            return NotImplemented
