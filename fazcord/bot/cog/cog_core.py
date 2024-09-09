from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from fazcord.bot.cog._cog_base import CogBase
from fazcord.bot.cog.admin_cog import AdminCog
from fazcord.bot.cog.help_cog import HelpCog
from fazcord.bot.cog.info_cog import InfoCog
from fazcord.bot.cog.wynn_analyze_cog import WynnAnalyzeCog
from fazcord.bot.cog.wynn_history_cog import WynnHistoryCog
from fazcord.bot.cog.wynn_stat_cog import WynnStatCog
from fazcord.bot.cog.wynn_track_cog import WynnTrackCog
from fazcord.bot.cog.wynn_utils_cog import WynnUtilsCog

if TYPE_CHECKING:
    from fazcord.bot.bot import Bot


class CogCore:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._cogs: list[CogBase] = []

        self.admin = AdminCog(bot)
        self.help = HelpCog(bot)
        self.info = InfoCog(bot)
        self.wynn_analyze = WynnAnalyzeCog(bot)
        self.wynn_history = WynnHistoryCog(bot)
        self.wynn_stat = WynnStatCog(bot)
        self.wynn_track = WynnTrackCog(bot)
        self.wynn_utils = WynnUtilsCog(bot)

        self._cogs.extend(
            [
                self.admin,
                self.help,
                self.info,
                self.wynn_analyze,
                self.wynn_history,
                self.wynn_stat,
                self.wynn_track,
                self.wynn_utils,
            ]
        )

    async def setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Intansiates all cogs and adds all application commands to the client.
        Should only be run once, that is, during start up"""
        for cog in self._cogs:
            cog.setup(whitelisted_guild_ids)
