from typing import Any

import nextcord

from fazcord.cog._base_cog import CogBase
from fazcord.bot.errors import UnauthorizedLocationException
from fazcord.view.help_view import HelpView


class HelpCog(CogBase):
    @nextcord.slash_command(name="help", description="Help command")
    async def _help(self, interaction: nextcord.Interaction[Any]) -> None:
        if not interaction.guild:
            raise UnauthorizedLocationException(
                "You can only use this command in a discord channel."
            )

        cmds = list(interaction.guild.get_application_commands())
        await HelpView(self._bot, interaction, cmds).run()
