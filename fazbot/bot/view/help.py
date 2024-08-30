from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from nextcord import BaseApplicationCommand, ButtonStyle, Colour, Embed, Interaction
from nextcord.ui import Button, button

from fazbot.bot.view._base_view import BaseView
from fazbot.bot.view._pagination_embed import PaginationEmbed

if TYPE_CHECKING:
    from fazbot.bot.bot import Bot


class InvokeHelp(BaseView):

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        commands: list[BaseApplicationCommand],
    ) -> None:
        super().__init__(bot, interaction)
        self._commands = commands
        self._embed = PaginationEmbed(
            self._interaction,
            commands,
            5,
            title=f"Commands List",
            color=Colour.dark_blue(),
        )

    @override
    async def run(self) -> None:
        await self._interaction.send(embed=self._get_embed_page(1), view=self)

    def _get_embed_page(self, page: int) -> Embed:
        """Generates embed page for page nth-page"""
        # title=f"Commands List : Page [{page}/{self._page_count}]",
        embed = self._embed.get_base()
        embed.set_footer(text="[text] means optional. <text> means required")
        for cmd in embed.get_items(page):
            embed.add_field(
                name=f"/{cmd.qualified_name}",
                value=cmd.description or "No brief description given",
                inline=False,
            )
        embed.finalize()
        return embed

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
    #     msg = ", ".join(msglist)
    #     return f" `{msg}`"

    @button(style=ButtonStyle.blurple, emoji="⏮️")
    async def first_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page = 1
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="◀️")
    async def previous_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page -= 1
        if self._embed.current_page == 0:
            self._embed.current_page = self._embed.page_count
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.red, emoji="⏹️")
    async def stop_(self, button: Button[Any], interaction: Interaction[Any]) -> None:
        await self.on_timeout()

    @button(style=ButtonStyle.blurple, emoji="▶️")
    async def next_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page += 1
        if self._embed.current_page == (self._embed.page_count + 1):
            self._embed.current_page = 1
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)

    @button(style=ButtonStyle.blurple, emoji="⏭️")
    async def last_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await interaction.response.defer()
        self._embed.current_page = self._embed.page_count
        embed = self._get_embed_page(self._embed.current_page)
        await interaction.edit_original_message(embed=embed)
