from __future__ import annotations

from typing import Any, override, TYPE_CHECKING

from nextcord import BaseApplicationCommand
from nextcord import Colour
from nextcord import Embed
from nextcord import Interaction

from faz.bot.app.discord.embed.builder.embed_builder import EmbedBuilder
from faz.bot.app.discord.embed.director._base_field_embed_director import BaseFieldEmbedDirector
from faz.bot.app.discord.embed.embed_field import EmbedField
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
        self._bot = bot
        self._interaction = interaction
        self._commands = commands

        self._embed_director = _HelpEmbedDirector(self)
        super().__init__(bot, interaction, self._embed_director)

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


class _HelpEmbedDirector(BaseFieldEmbedDirector):
    def __init__(self, view: HelpView) -> None:
        self._view = view
        self._commands = view._commands

        initial_embed = Embed(title="Commands List", colour=Colour.dark_blue()).set_footer(
            text="[text] means optional. <text> means required"
        )
        self._embed_builder = EmbedBuilder(view.interaction, initial_embed=initial_embed)

        super().__init__(self._embed_builder, items_per_page=5)

    @override
    async def setup(self) -> None:
        items = [
            EmbedField(
                name=f"/{cmd.qualified_name}",
                value=cmd.description or "No brief description given",
                inline=False,
            )
            for cmd in self._commands
        ]
        self.set_items(items)
