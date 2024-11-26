from typing import Any

import nextcord

from faz.bot.app.discord.cog._base_cog import CogBase
from faz.bot.app.discord.bot.errors import UnauthorizedLocationException
from faz.bot.app.discord.view.help_view import HelpView


class HelpCog(CogBase):
    @nextcord.slash_command(name="help", description="Help command")
    async def _help(self, interaction: nextcord.Interaction[Any]) -> None:
        if not interaction.guild:
            raise UnauthorizedLocationException(
                "You can only use this command in a discord channel."
            )

        cmds = list(interaction.guild.get_application_commands())
        await HelpView(self._bot, interaction, cmds).run()
