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
        self._embed_director = _HelpEmbedDirector(self)

    @override
    async def run(self) -> None:
        await self._initial_send_message()

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

    @property
    @override
    def embed_director(self) -> BasePaginationEmbedDirector:
        return self._embed_director


class _HelpEmbedDirector(BasePaginationEmbedDirector):
    def __init__(self, view: HelpView) -> None:
        self._view = view
        self._embed_builder = PaginationEmbedBuilder(
            view.interaction,
            items=view._commands,
            items_per_page=5,
        )

    @override
    async def setup(self) -> None:
        pass

    @override
    def construct(self) -> Embed:
        builder = self.embed_builder
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
    def embed_builder(self) -> PaginationEmbedBuilder[BaseApplicationCommand]:
        return self._embed_builder
