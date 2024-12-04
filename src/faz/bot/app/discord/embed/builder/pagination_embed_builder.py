from __future__ import annotations

from typing import Any, override, Self, Sequence

from nextcord import Embed
from nextcord import Interaction

from faz.bot.app.discord.embed.builder.embed_builder import EmbedBuilder


class PaginationEmbedBuilder[T](EmbedBuilder):
    def __init__(
        self,
        interaction: Interaction[Any],
        items: Sequence[T] | None = None,
        items_per_page: int = 20,
    ) -> None:
        super().__init__(interaction)
        items = items or []
        self._items = items
        self._items_per_page = items_per_page
        self._current_page: int = 1

    def set_builder_items(self, items: Sequence[T]) -> Self:
        """Set pagination items for the builder."""
        self._items = items
        return self

    def set_builder_page(self, page: int) -> Self:
        """Set the current page for the builder.

        Args:
            page (int): Page number to set.

        Raises:
            ValueError: If the page number is invalid.

        Returns:
            Self: Returns self for method chaining.
        """
        if not self._check_page(page):
            raise ValueError(f"Invalid page number: {page}")
        self._current_page = page
        return self

    @override
    def build(self) -> Embed:
        self._add_page_field()
        return super().build()

    def get_items(self, page: int | None = None) -> Sequence[T]:
        """Get items from a specific page."""
        page = page or self._current_page
        if not self._check_page(page):
            raise ValueError(f"Invalid page number: {page}")
        l_idx = self.items_per_page * (page - 1)
        r_idx = self.items_per_page * page
        return self.items[l_idx:r_idx]

    def _add_page_field(self) -> Self:
        self._embed.add_field(
            name="Page",
            value=f"({self._current_page} / {self.page_count})",
            inline=False,
        )
        return self

    def _check_page(self, page: int) -> bool:
        """Check if the page number is valid.

        Args:
            page (int): Page number to check.

        Returns:
            bool: True if the page number is valid. False otherwise.
        """
        return 1 <= page <= self.page_count

    @property
    def current_page(self) -> int:
        return self._current_page

    @property
    def items(self) -> Sequence[T]:
        return self._items

    @property
    def items_per_page(self) -> int:
        return self._items_per_page

    @property
    def page_count(self) -> int:
        return max(1, -(-len(self._items) // self._items_per_page))
