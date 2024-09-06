from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from nextcord import ButtonStyle, Embed, Interaction
from nextcord.ui import Button, button

from fazcord.bot.view._base_view import BaseView

if TYPE_CHECKING:
    from fazcord.bot.view._pagination_embed import PaginationEmbed


class BasePaginationView(BaseView, ABC):
    """Base class for pagination views in a Discord bot using Nextcord.

    This class provides a base structure for pagination views that allow users to navigate
    through multiple pages of an embed message. It includes buttons for first, previous,
    next, last, and stop controls.

    Attributes:
        _embed (PaginationEmbed): The embed object that represents the paginated content.
    """

    _embed: PaginationEmbed

    @button(style=ButtonStyle.blurple, emoji="⏮️")
    async def first_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        """Handles the callback for the 'First Page' button.

        This method sets the embed to the first page and updates the message.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        self._embed.current_page = 1
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="◀️")
    async def previous_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        """Handles the callback for the 'Previous Page' button.

        This method navigates to the previous page of the embed. If the current page
        is the first page, it loops around to the last page.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        self._embed.current_page -= 1
        if self._embed.current_page == 0:
            self._embed.current_page = self._embed.page_count
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.red, emoji="⏹️")
    async def stop_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        """Handles the callback for the 'Stop' button.

        This method stops the pagination by calling the `on_timeout` method, which
        effectively disables the view.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await self.on_timeout()

    @button(style=ButtonStyle.blurple, emoji="▶️")
    async def next_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        """Handles the callback for the 'Next Page' button.

        This method navigates to the next page of the embed. If the current page is
        the last page, it loops around to the first page.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        self._embed.current_page += 1
        if self._embed.current_page == (self._embed.page_count + 1):
            self._embed.current_page = 1
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="⏭️")
    async def last_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        """Handles the callback for the 'Last Page' button.

        This method sets the embed to the last page and updates the message.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        self._embed.current_page = self._embed.page_count
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @abstractmethod
    def _get_embed_page(self, page: int) -> Embed:
        """Abstract method to get the embed for a specific page.

        This method must be implemented in subclasses to define how the embed content
        is generated for each page.

        Args:
            page (int): The page number to generate the embed for.

        Returns:
            Embed: The generated embed for the specified page.
        """
        ...
