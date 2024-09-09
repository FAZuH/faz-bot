from typing import Any, Literal

import nextcord
from nextcord import Interaction

from fazcord.bot.cog._cog_base import CogBase
from fazcord.bot.view.stat_worldlist_view import StatWorldlistView


class WynnStatCog(CogBase):
    """Shows statistics from most recent Wynncraft data."""

    @nextcord.slash_command()
    async def stats(self, intr: Interaction[Any]) -> None: ...

    @stats.subcommand(name="worldlist")
    async def worldlist(
        self,
        interaction: Interaction[Any],
        sort_by: Literal["Player Count", "Time Created"] = "Time Created",
    ) -> None:
        """
        Shows a list of active worlds, showing player count and world uptime.

        Args:
            sort_by (Literal["Player Count", "Time Created"], optional): The criteria to sort the worlds by.
                Can be either "Player Count" or "Time Created". Defaults to "Time Created".
        """
        await StatWorldlistView(self._bot, interaction, sort_by).run()

    # @nextcord.slash_command(name="player")
    # async def player(self, interaction: Interaction[Any]) -> None:
    #     return

    # @nextcord.slash_command(name="player_guilds")
    # async def player_guilds(self, interaction: Interaction[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="guild")
    # async def guild(self, interaction: Interaction[Any], guild: str) -> None:
    #     return

    # @nextcord.slash_command(name="guild_member")
    # async def guild_member(self, interaction: Interaction[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="find_hunteds")
    # async def find_hunteds(self, interaction: Interaction[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="find_returned")
    # async def find_returned(self, interaction: Interaction[Any], player: str) -> None:
    #     return
