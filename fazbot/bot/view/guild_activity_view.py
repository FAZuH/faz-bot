from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from nextcord import Button, ButtonStyle, Color, Embed
from nextcord.ui import Button, button
from tabulate import tabulate

from fazbot.bot.view._base_view import BaseView

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

    @override
    async def run(self) -> None:
        await self._guild.awaitable_attrs.members
        members = self._guild.members
        repo = self._bot.fazdb_db.player_activity_history_repository
        self._activity_res: list[GuildActivityView.ActivityResult] = [
            self.ActivityResult(
                member.latest_username,
                await repo.get_playtime_between_period(
                    member.uuid, self._period_begin, self._period_end
                ),
            )
            for member in members
        ]
        self._page_count = len(self._activity_res) // self._items_per_page
        embed = self._get_embed_page(1)
        await self._interaction.send(embed=embed)

    def _get_embed_page(self, page: int) -> Embed:
        begin_ts = int(self._period_begin.timestamp())
        end_ts = int(self._period_end.timestamp())
        intr = self._interaction
        assert intr.user
        embed = Embed(
            title=f"Guild Members Activity ",
            color=Color.teal(),
        )
        embed.description = f"`Guild:  `{self._guild.name})\n`Period: `<t:{begin_ts}:R>, <t:{end_ts}:R>`"
        embed.set_author(
            name=intr.user.display_name,
            icon_url=intr.user.display_avatar.url,
        )
        left_index = self._items_per_page * (page - 1)
        right_index = self._items_per_page * page
        results = self._activity_res[left_index:right_index]
        embed.description = (
            "```ml\n"
            + tabulate(
                [[res.username, res.playtime] for res in results],
                headers=["Username", "Activity"],
                tablefmt="github",
            )
            + "\n```"
        )
        embed.set_author(
            name=intr.user.display_name, icon_url=intr.user.display_avatar.url
        )
        embed.add_field(
            name="Timestamp",
            value=f"<t:{int(intr.created_at.timestamp())}:F>",
            inline=False,
        )
        embed.add_field(name="Page", value=f"{page} / {self._page_count}", inline=False)
        return embed

    def _format_time_delta(self, timedelta: timedelta) -> str:
        total_seconds = int(timedelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        formatted_time = f"{hours}h {minutes}m"
        return formatted_time

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
            self._username: str = username
            self._playtime: str = self.__format_time_delta(playtime)

        @property
        def username(self) -> str:
            return self._username

        @property
        def playtime(self) -> str:
            return self._playtime

        def __format_time_delta(self, timedelta: timedelta) -> str:
            total_seconds = int(timedelta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            formatted_time = f"{hours}h {minutes}m"
            return formatted_time
