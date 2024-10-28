from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncGenerator, Iterable

from loguru import logger
from nextcord import Colour, Interaction
from nextcord.ext import commands

from fazcord.bot.view._custom_embed import CustomEmbed

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fazcord.bot.bot import Bot
    from fazutil.db.fazcord.fazcord_database import FazcordDatabase
    from fazutil.db.fazdb.fazdb_database import FazdbDatabase


class CogBase(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self._bot = bot
        self._utils = self._bot.utils

    def setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Adds cog to the bot."""
        self._bot.client.add_cog(self)
        self._setup(whitelisted_guild_ids)

        logger.info(
            f"Added cog {self.__class__.__qualname__} "
            f"with {len(self.application_commands)} application commands"
        )

    async def _respond_successful(
        self, interaction: Interaction[Any], message: str
    ) -> None:
        embed = CustomEmbed(
            interaction, title="Success", description=message, color=Colour.dark_green()
        )
        embed.finalize()
        await interaction.send(embed=embed)

    @asynccontextmanager
    async def _enter_botdb_session(
        self,
    ) -> AsyncGenerator[tuple[FazcordDatabase, AsyncSession], None]:
        db = self._bot.fazcord_db
        async with db.enter_async_session() as session:
            yield db, session

    @asynccontextmanager
    async def _enter_fazdb_session(
        self,
    ) -> AsyncGenerator[tuple[FazdbDatabase, AsyncSession], None]:
        db = self._bot.fazdb_db
        async with db.enter_async_session() as session:
            yield db, session

    def _setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Method to run on cog setup.
        By default, this adds whitelisted_guild_ids into
        guild rollouts into all command in the cog."""
        for app_cmd in self.application_commands:
            for guild_id in whitelisted_guild_ids:
                app_cmd.add_guild_rollout(guild_id)
                # app_cmd.guild_ids.add(guild_id)
            self._bot.client.add_application_command(
                app_cmd, overwrite=True, use_rollout=True
            )
