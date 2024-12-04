from abc import ABC
from typing import override, Sequence

from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)
from faz.bot.app.discord.embed.embed_field import EmbedField


class BaseFieldEmbedDirector(BasePaginationEmbedDirector[EmbedField], ABC):
    @override
    def _process_page_items(self, items: Sequence[EmbedField]) -> None:
        self.embed_builder.add_fields(items)
