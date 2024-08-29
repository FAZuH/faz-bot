from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from fazbot.bot.cog._cog_base import CogBase
from fazbot.bot.cog.admin import Admin
from fazbot.bot.cog.help import Help
from fazbot.bot.cog.info import Info
from fazbot.bot.cog.wynn_analyze import WynnAnalyze
from fazbot.bot.cog.wynn_history import WynnHistory
from fazbot.bot.cog.wynn_stat import WynnStat
from fazbot.bot.cog.wynn_track import WynnTrack
from fazbot.bot.cog.wynn_utils import WynnUtils

if TYPE_CHECKING:
    from fazbot.bot.bot import Bot


class CogCore:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._cogs: list[CogBase] = []

        self.admin = Admin(bot)
        self.help = Help(bot)
        self.info = Info(bot)
        self.wynn_analyze = WynnAnalyze(bot)
        self.wynn_history = WynnHistory(bot)
        self.wynn_stat = WynnStat(bot)
        self.wynn_track = WynnTrack(bot)
        self.wynn_utils = WynnUtils(bot)

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
