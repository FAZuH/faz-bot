from typing import Any

import nextcord

from fazcord.bot.cog._cog_base import CogBase
from fazcord.bot.errors import UnauthorizedLocationException
from fazcord.bot.view.help_view import HelpView


class HelpCog(CogBase):
    @nextcord.slash_command(name="help", description="Help command")
    async def _help(self, interaction: nextcord.Interaction[Any]) -> None:
        if not interaction.guild:
            raise UnauthorizedLocationException(
                "You can only use this command in a guild channel."
            )

        cmds = list(interaction.guild.get_application_commands())
        await HelpView(self._bot, interaction, cmds).run()
