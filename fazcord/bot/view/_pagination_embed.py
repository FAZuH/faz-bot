from datetime import datetime
from typing import Any, Optional, Sequence, Union, override

from nextcord import Colour, Interaction
from nextcord.types.embed import EmbedType

from fazcord.bot.view._custom_embed import CustomEmbed


class PaginationEmbed[T](CustomEmbed):
    def __init__(
        self,
        interaction: Interaction[Any],
        items: Sequence[T],
        items_per_page: int = 20,
        *,
        thumbnail_url: Optional[str] = None,
        colour: Optional[Union[int, Colour]] = None,
        color: Optional[Union[int, Colour]] = None,
        title: Optional[Any] = None,
        type: EmbedType = "rich",
        url: Optional[Any] = None,
        description: Optional[Any] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(
            interaction,
            thumbnail_url=thumbnail_url,
            colour=colour,
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp,
        )
        self._memento = {
            "interaction": interaction,
            "items": items,
            "items_per_page": items_per_page,
            "thumbnail_url": thumbnail_url,
            "colour": colour,
            "color": color,
            "title": title,
            "type": type,
            "url": url,
            "description": description,
            "timestamp": timestamp,
        }
        self._items = items
        self._items_per_page = items_per_page
        self._page_count = self._get_page_count()
        self._current_page = 1

    def get_items(self, page: int) -> Sequence[T]:
        l_idx = self._items_per_page * (page - 1)
        r_idx = self._items_per_page * page
        return self._items[l_idx:r_idx]

    def add_page_field(self) -> None:
        self.add_field(
            name="Page",
            value=f"{self._current_page} / {self._page_count}",
            inline=False,
        )

    @override
    def finalize(self) -> None:
        super().finalize()
        self.add_page_field()

    @property
    def items(self) -> Sequence[T]:
        return self._items

    @property
    def items_per_page(self) -> int:
        return self._items_per_page

    @property
    def page_count(self) -> int:
        return self._page_count

    @property
    def current_page(self):
        return self._current_page

    @current_page.setter
    def current_page(self, value):
        self._current_page = value

    def _get_page_count(self) -> int:
        return -(-len(self._items) // self._items_per_page)
