from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, override

from ._invoke import Invoke

from nextcord import ButtonStyle, Color, Embed
from nextcord.ui import Button, View, button

if TYPE_CHECKING:
    from nextcord import Interaction
    from .. import Bot


class InvokeWorldlist(Invoke):

    def __init__(self, bot: Bot, interaction: Interaction[Any], sort_by: Literal["Player Count", "Time Created"]) -> None:
        self._sort_by: Literal["player", "time"] = "player" if sort_by == "Player Count" else "time"
        super().__init__(bot, interaction) 

    async def run(self):
        self._worlds = await self._bot.fazdb_db.worlds_repository.get_worlds(self._sort_by)
        self._items_per_page = 10
        self._page_count = len(self._worlds) // self._items_per_page + 1
        await self._interaction.send(embed=self._get_embed_page(1))
        self._view = self._View(self)

    def _get_embed_page(self, page: int) -> Embed:
        embed = Embed(title="World List", color=Color.dark_teal())
        intr = self._interaction
        assert intr.user

        left_index = self._items_per_page * (page - 1)
        right_index = self._items_per_page * page

        worlds = self._worlds[left_index:right_index]
        longest_len_world = max(len(w.name) for w in worlds)
        worldlist_strs = '\n'.join(
            f"` {w.name:<{longest_len_world}} `: {w.player_count:<5} | <t:{int(w.time_created.timestamp())}:R>"
            for w in worlds
        )
        embed.description = worldlist_strs

        embed.set_author(name=intr.user.display_name, icon_url=intr.user.display_avatar.url)
        embed.add_field(name="Timestamp", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=False)
        return embed
        
    class _View(View):
        def __init__(self, cmd: InvokeWorldlist):
            super().__init__(timeout=60)
            self._cmd = cmd
            self._embed_pages = 1

        @override
        async def on_timeout(self) -> None:
            for item in self.children:
                self.remove_item(item)
            await self._cmd._interaction.edit_original_message(view=self)

        @button(style=ButtonStyle.blurple, emoji="⏮️")
        async def first_page_callback(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            self._current_page = 1
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.response.edit_message(embed=embed)

        @button(style=ButtonStyle.blurple, emoji="◀️")
        async def previous_page_callback(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            self._current_page -= 1
            if self._current_page == 0:
                self._current_page = self._embed_pages
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.response.edit_message(embed=embed)

        @button(style=ButtonStyle.red, emoji="⏹️")
        async def stop_(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            await self.on_timeout()

        @button(style=ButtonStyle.blurple, emoji="▶️")
        async def next_page(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            self._current_page += 1
            if self._current_page == (self._embed_pages + 1):
                self._current_page = 1
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.response.edit_message(embed=embed)

        @button(style=ButtonStyle.blurple, emoji="⏭️")
        async def last_page(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            self._current_page = self._embed_pages
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.response.edit_message(embed=embed)
