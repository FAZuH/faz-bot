from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any, TYPE_CHECKING

from nextcord import ButtonStyle
from nextcord import Interaction
from nextcord.ui import Button

from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)
from faz.bot.app.discord.view._base_view import BaseView

if TYPE_CHECKING:
    from faz.bot.app.discord.bot.bot import Bot
    from faz.bot.app.discord.embed.builder.pagination_embed_builder import PaginationEmbedBuilder


class BasePaginationView[T](BaseView, ABC):
    """Base class for pagination views in a Discord bot using Nextcord.

    This class provides a base structure for pagination views that allow users to navigate
    through multiple pages of an embed message. It includes buttons for first, previous,
    next, last, and stop controls.

    Attributes:
        _embed (PaginationEmbed): The embed object that represents the paginated content.
    """

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        *,
        timeout: float | None = 180,
        auto_defer: bool = True,
        prevent_update: bool = True,
    ) -> None:
        super().__init__(
            bot, interaction, timeout=timeout, auto_defer=auto_defer, prevent_update=prevent_update
        )
        self._buttons_added = False

        self._first_page_button = Button(style=ButtonStyle.blurple, emoji="⏮️")
        self._first_page_button.callback = self.first_page_callback
        self._previous_page_button = Button(style=ButtonStyle.blurple, emoji="◀️")
        self._previous_page_button.callback = self.previous_page_callback
        self._stop_button = Button(style=ButtonStyle.red, emoji="⏹️")
        self._stop_button.callback = self.stop_callback
        self._next_page_button = Button(style=ButtonStyle.blurple, emoji="▶️")
        self._next_page_button.callback = self.next_page_callback
        self._last_page_button = Button(style=ButtonStyle.blurple, emoji="⏭️")
        self._last_page_button.callback = self.last_page_callback

    def _add_navigation_buttons(self) -> None:
        """Adds page navigation buttons to the view. Does not add if page count is less than 2."""
        if not self.embed_builder.page_count > 1:
            return
        if self._buttons_added:
            return
        self.add_item(self._first_page_button)
        self.add_item(self._previous_page_button)
        self.add_item(self._stop_button)
        self.add_item(self._next_page_button)
        self.add_item(self._last_page_button)
        self._buttons_added = True

    def _remove_navigation_buttons(self) -> None:
        """Adds page navigation buttons to the view."""
        if not self._buttons_added:
            return
        self.remove_item(self._first_page_button)
        self.remove_item(self._previous_page_button)
        self.remove_item(self._stop_button)
        self.remove_item(self._next_page_button)
        self.remove_item(self._last_page_button)
        self._buttons_added = False

    async def first_page_callback(self, interaction: Interaction[Any]) -> None:
        """Handles the callback for the 'First Page' button.

        This method sets the embed to the first page and updates the message.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        new_page = 1
        await self._edit_message_page(interaction, new_page)

    async def previous_page_callback(self, interaction: Interaction[Any]) -> None:
        """Handles the callback for the 'Previous Page' button.

        This method navigates to the previous page of the embed. If the current page
        is the first page, it loops around to the last page.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        curr_page = self.embed_builder.current_page
        new_page = self.embed_builder.page_count if curr_page == 1 else curr_page - 1
        await self._edit_message_page(interaction, new_page)

    async def stop_callback(self, interaction: Interaction[Any]) -> None:
        """Handles the callback for the 'Stop' button.

        This method stops the pagination by calling the `on_timeout` method, which
        effectively disables the view.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await self.on_timeout()

    async def next_page_callback(self, interaction: Interaction[Any]) -> None:
        """Handles the callback for the 'Next Page' button.

        This method navigates to the next page of the embed. If the current page is
        the last page, it loops around to the first page.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        curr_page = self.embed_builder.current_page
        new_page = 1 if curr_page == self.embed_builder.page_count else curr_page + 1
        await self._edit_message_page(interaction, new_page)

    async def last_page_callback(self, interaction: Interaction[Any]) -> None:
        """Handles the callback for the 'Last Page' button.

        This method sets the embed to the last page and updates the message.

        Args:
            button (Button[Any]): The button instance that triggered the callback.
            interaction (Interaction[Any]): The interaction object from Discord.
        """
        await interaction.response.defer()
        new_page = self.embed_builder.page_count
        await self._edit_message_page(interaction, new_page)

    async def _initial_send_message(self) -> None:
        """Add page navigation buttons and send the initial message with the embed."""
        embed = self.embed_director.construct_page(1)
        self._add_navigation_buttons()
        await self.interaction.send(embed=embed, view=self)

    async def _edit_message_page(self, interaction: Interaction[Any], new_page: int = 1) -> None:
        """Set the embed builder to a new page, construct an embed, and edit the message with the new embed."""
        embed = self.embed_director.construct_page(new_page)
        self._add_navigation_buttons()
        await interaction.edit(embed=embed, view=self)

    @property
    @abstractmethod
    def embed_director(self) -> BasePaginationEmbedDirector: ...

    @property
    def embed_builder(self) -> PaginationEmbedBuilder:
        return self.embed_director.embed_builder
