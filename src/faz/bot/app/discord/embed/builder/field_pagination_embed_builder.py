from typing import Any, override, Self, Sequence

from nextcord import Embed
from nextcord import Interaction

from faz.bot.app.discord.embed.builder.pagination_embed_builder import PaginationEmbedBuilder
from faz.bot.app.discord.embed.embed_field import EmbedField


class FieldPaginationEmbedBuilder(PaginationEmbedBuilder[EmbedField]):
    def __init__(
        self,
        interaction: Interaction[Any],
        items: Sequence[EmbedField] | None = None,
        items_per_page: int = 20,
    ) -> None:
        super().__init__(
            interaction,
            items,
            items_per_page,
        )

    @override
    def build(self) -> Embed:
        fields = self.get_items()

        if len(fields) == 0:
            self._add_empty_field("")
        else:
            for field in fields:
                self._embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=field.inline,
                )
        return super().build()

    def _add_empty_field(self, name: str, inline: bool = False) -> Self:
        self._embed.add_field(name=name, value="```No data found.\n```", inline=inline)
        return self
