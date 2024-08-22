from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Sized, override

from nextcord import (
    ApplicationCommandOption,
    BaseApplicationCommand,
    ButtonStyle,
    Colour,
    Embed,
    Interaction,
)
from nextcord.ui import Button, button

from fazbot.bot.view._base_view import BaseView

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

        self._items_per_page = 5
        self._page_count = 0

    @override
    async def run(self) -> None:
        self._page_count = self._get_embed_total_pages(self._commands)
        embed = self._get_embed_page(self._commands, 1)
        await self._interaction.send(embed=embed, view=self)

    def _get_embed_page(
        self, commands: list[BaseApplicationCommand], page: int
    ) -> Embed:
        """Generates embed page for page nth-page"""
        embed = Embed(
            title=f"Commands List : Page [{page}/{self._page_count}]",
            color=Colour.dark_blue(),
            timestamp=datetime.now(),
        )
        embed.set_footer(text="[text] means optional. <text> means required")

        min_idx = self._items_per_page * (page - 1)
        max_idx = self._items_per_page * page
        for cmd in commands[min_idx:max_idx]:
            parameter_msg = self._get_parameters(cmd.options)
            embed.add_field(
                name=f"/{cmd.qualified_name}{parameter_msg}",
                value=cmd.description or "No brief description given",
                inline=False,
            )
        return embed

    def _get_embed_total_pages(self, commands: Sized) -> int:
        return (len(commands) - 1) // self._items_per_page + 1

    def _get_parameters(self, parameters: dict[str, ApplicationCommandOption]) -> str:
        if not parameters:
            # NOTE: case no params
            return ""
        msglist: list[str] = []
        for name, p in parameters.items():
            # NOTE: case param disp name, param description
            p_msg = f"{name}: {p.description}"
            # NOTE: case param isrequired
            p_msg = f"<{p_msg}>" if p.required else f"[{p_msg}]"
            msglist.append(p_msg)
        msg = ", ".join(msglist)
        return f" `{msg}`"

    @button(style=ButtonStyle.blurple, emoji="⏮️")
    async def first_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        self._current_page = 1
        self._embed_content = self._get_embed_page(self._commands, self._current_page)
        await interaction.response.edit_message(embed=self._embed_content)

    @button(style=ButtonStyle.blurple, emoji="◀️")
    async def previous_page_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        self._current_page -= 1
        if self._current_page == 0:
            self._current_page = self._page_count
        self._embed_content = self._get_embed_page(self._commands, self._current_page)
        await interaction.response.edit_message(embed=self._embed_content)

    @button(style=ButtonStyle.red, emoji="⏹️")
    async def stop_(self, button: Button[Any], interaction: Interaction[Any]) -> None:
        await self.on_timeout()

    @button(style=ButtonStyle.blurple, emoji="▶️")
    async def next_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        self._current_page += 1
        if self._current_page == (self._page_count + 1):
            self._current_page = 1
        self._embed_content = self._get_embed_page(self._commands, self._current_page)
        await interaction.response.edit_message(embed=self._embed_content)

    @button(style=ButtonStyle.blurple, emoji="⏭️")
    async def last_page(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        self._current_page = self._page_count
        self._embed_content = self._get_embed_page(self._commands, self._current_page)
        await interaction.response.edit_message(embed=self._embed_content)
