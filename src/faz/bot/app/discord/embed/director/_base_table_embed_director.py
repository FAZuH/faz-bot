from abc import ABC
from typing import Any, Iterable, override, Sequence

from tabulate import TableFormat
from tabulate import tabulate

from faz.bot.app.discord.embed.builder.embed_builder import EmbedBuilder
from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)


class BaseTableEmbedDirector(BasePaginationEmbedDirector[Iterable[Any]], ABC):
    def __init__(
        self,
        embed_builder: EmbedBuilder,
        *,
        items: Sequence[Iterable[str]] | None = None,
        items_per_page: int = 20,
        item_header: Sequence[str],
        table_format: str | TableFormat = "github",
    ) -> None:
        super().__init__(embed_builder, items=items, items_per_page=items_per_page)
        self.item_header = item_header
        self.table_format = table_format

    @override
    def _process_page_items(self, items: Sequence[Iterable[Any]]) -> None:
        desc = (
            "```ml\n"
            + tabulate(
                items,
                headers=self.item_header,
                tablefmt=self.table_format,
            )
            + "\n```"
        )
        self.embed_builder.set_description(desc)
