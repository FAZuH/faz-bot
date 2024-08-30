from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from nextcord import ButtonStyle, Embed, Interaction
from nextcord.ui import Button, button

from fazcord.bot.view._base_view import BaseView

if TYPE_CHECKING:
    from fazcord.bot.view._pagination_embed import PaginationEmbed


class BasePaginationView(BaseView, ABC):

    _embed: PaginationEmbed

    @button(style=ButtonStyle.blurple, emoji="⏮️")
    async def first_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page = 1
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="◀️")
    async def previous_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page -= 1
        if self._embed.current_page == 0:
            self._embed.current_page = self._embed.page_count
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.red, emoji="⏹️")
    async def stop_(self, button: Button[Any], interaction: Interaction[Any]) -> None:
        await self.on_timeout()

    @button(style=ButtonStyle.blurple, emoji="▶️")
    async def next_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page += 1
        if self._embed.current_page == (self._embed.page_count + 1):
            self._embed.current_page = 1
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="⏭️")
    async def last_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page = self._embed.page_count
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @abstractmethod
    def _get_embed_page(self, page: int) -> Embed: ...
