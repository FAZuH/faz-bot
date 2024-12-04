from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from faz.bot.app.discord.embed.builder.pagination_embed_builder import PaginationEmbedBuilder

if TYPE_CHECKING:
    from nextcord import Embed


class BasePaginationEmbedDirector(ABC):
    @abstractmethod
    async def setup(self) -> None: ...

    def prepare_default(self) -> PaginationEmbedBuilder:
        """Prepare the default embed for the director.

        Returns:
            Embed: The default embed.
        """
        builder = self.embed_builder.reset_embed()
        return builder

    def construct(self) -> Embed:
        """Construct an embed page.

        Args:
            page (int | None, optional): Page of the embed to construct. Defaults to None.

        Returns:
            Embed: Constructed embed.
        """
        embed = self.prepare_default().build()
        return embed

    def construct_page(self, page: int) -> Embed:
        """Construct an embed page.

        Args:
            page (int): Page of the embed to construct.

        Returns:
            Embed: Constructed embed.
        """
        self.embed_builder.set_builder_page(page)
        return self.construct()

    @property
    @abstractmethod
    def embed_builder(self) -> PaginationEmbedBuilder:
        """Pagination embed builder."""
        ...
