from __future__ import annotations

from typing import Any, override, TYPE_CHECKING

from nextcord import BaseApplicationCommand
from nextcord import Colour
from nextcord import Embed
from nextcord import Interaction

from faz.bot.app.discord.embed.builder.pagination_embed_builder import PaginationEmbedBuilder
from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)
from faz.bot.app.discord.view._base_pagination_view import BasePaginationView

if TYPE_CHECKING:
    from faz.bot.app.discord.bot.bot import Bot


class HelpView(BasePaginationView):
    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        commands: list[BaseApplicationCommand],
    ) -> None:
        super().__init__(bot, interaction)
        self._commands = commands

        self._embed_builder: PaginationEmbedBuilder[BaseApplicationCommand] = (
            PaginationEmbedBuilder(
                self._interaction,
                items=commands,
                items_per_page=5,
            )
        )

    @override
    async def run(self) -> None:
        embed = self._get_embed()
        await self._interaction.send(embed=embed, view=self)

    # def _get_parameters(self, parameters: dict[str, ApplicationCommandOption]) -> str:
    #     if not parameters:
    #         # NOTE: case no params
    #         return ""
    #     msglist: list[str] = []
    #     for name, p in parameters.items():
    #         # NOTE: case param disp name, param description
    #         p_msg = f"{name}: {p.description}"
    #         # NOTE: case param isrequired
    #         p_msg = f"<{p_msg}>" if p.required else f"[{p_msg}]"
    #         msglist.append(p_msg)

    def _get_embed(self) -> Embed:
        builder = self._embed_builder
        for cmd in builder.get_items():
            builder.add_field(
                name=f"/{cmd.qualified_name}",
                value=cmd.description or "No brief description given",
                inline=False,
            )
        embed = (
            builder.set_footer(text="[text] means optional. <text> means required")
            .set_title("Commands List")
            .set_colour(Colour.dark_blue())
            .build()
        )
        return embed

    @property
    @override
    def embed_director(self) -> PaginationEmbedBuilder:
        return self._embed_builder


class _HelpEmbedDirector(BasePaginationEmbedDirector):
    def __init__(self, view: HelpView) -> None:
        self._view = view

    @override
    async def setup(self) -> None:
        pass

    @override
    def construct(self, page: int | None = None) -> Embed:
        if page:
            self._view.embed_builder.set_builder_page(page)
        embed = self._view._get_embed()
        return embed

    @property
    @override
    def embed_builder(self) -> PaginationEmbedBuilder:
        return self._view.embed_director
