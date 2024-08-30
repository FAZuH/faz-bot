from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any, Literal, override

from nextcord import ButtonStyle, Color, Embed
from nextcord.ui import Button, button
from tabulate import tabulate

from fazbot.bot.view._base_view import BaseView
from fazbot.bot.view._custom_embed import CustomEmbed
from fazbot.bot.view._view_utils import ViewUtils

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazbot.bot.bot import Bot


class WorldlistView(BaseView):

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        sort_by: Literal["Player Count", "Time Created"],
    ) -> None:
        self._sort_by: Literal["player", "time"] = (
            "player" if sort_by == "Player Count" else "time"
        )
        super().__init__(bot, interaction)
        self._current_page = 1
        self._items_per_page = 20
        self._page_count: int

    @override
    async def run(self):
        self._worlds = await self._bot.fazdb_db.worlds_repository.get_worlds(
            self._sort_by
        )
        self._page_count = len(self._worlds) // self._items_per_page + 1
        await self._interaction.send(embed=self._get_embed_page(1), view=self)

    def _get_embed_page(self, page: int) -> Embed:
        embed = CustomEmbed(
            self._interaction, title="World List", color=Color.dark_teal()
        )
        intr = self._interaction
        assert intr.user

        left_index = self._items_per_page * (page - 1)
        right_index = self._items_per_page * page

        worlds = self._worlds[left_index:right_index]
        worldlist = [
            [
                n,
                w.name,
                w.player_count,
                ViewUtils.format_timedelta(intr.created_at - w.time_created),
            ]
            for n, w in enumerate(worlds, start=1)
        ]
        embed.description = (
            "```ml\n"
            + tabulate(
                worldlist,
                headers=["No", "World", "Players", "Uptime"],
                tablefmt="github",
            )
            + "\n```"
        )
        embed.add_field(name="Page", value=f"{page} / {self._page_count}", inline=False)
        embed.finalize()
        return embed

    @staticmethod
    def _timedelta_to_string(td: timedelta) -> str:
        hours, remainder = divmod(int(td.total_seconds()), 3600)
        minutes = remainder // 60
        ret = (str(hours) + "h " if hours > 0 else "") + str(minutes) + "m"
        return ret

    @button(style=ButtonStyle.blurple, emoji="⏮️")
    async def first_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._current_page = 1
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="◀️")
    async def previous_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._current_page -= 1
        if self._current_page == 0:
            self._current_page = self._page_count
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.red, emoji="⏹️")
    async def stop_(self, button: Button[Any], interaction: Interaction[Any]) -> None:
        await self.on_timeout()

    @button(style=ButtonStyle.blurple, emoji="▶️")
    async def next_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._current_page += 1
        if self._current_page == (self._page_count + 1):
            self._current_page = 1
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="⏭️")
    async def last_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._current_page = self._page_count
        embed = self._get_embed_page(self._current_page)
        await interaction.edit_original_message(embed=embed)
