from __future__ import annotations

from datetime import timezone
from typing import Literal, override, TYPE_CHECKING

from nextcord import Colour
from nextcord import Embed

from faz.bot.app.discord.embed.builder.embed_builder import EmbedBuilder
from faz.bot.app.discord.embed.director._base_table_embed_director import BaseTableEmbedDirector
from faz.bot.app.discord.view._view_utils import ViewUtils

if TYPE_CHECKING:
    from faz.bot.app.discord.view.wynn_stat.worldlist_view import WorldlistView


class WorldlistEmbedDirector(BaseTableEmbedDirector):
    def __init__(self, view: WorldlistView, sort_by: Literal["player", "time"]) -> None:
        self._view = view
        self._interaction = view.interaction
        self._sort_by: Literal["player", "time"] = sort_by

        initial_embed = Embed(title="World List", color=Colour.dark_teal())
        self._embed_builder = EmbedBuilder(self._interaction, initial_embed)

        super().__init__(self._embed_builder, item_header=["#", "World", "Player Count", "Uptime"])

    @override
    async def setup(self) -> None:
        await self._fetch_data()
        self._parse_items()

    def _parse_items(self) -> None:
        worldlist = [
            [
                n,
                world.name,
                world.player_count,
                ViewUtils.format_timedelta(
                    self._interaction.created_at - world.time_created.replace(tzinfo=timezone.utc)
                ),
            ]
            for n, world in enumerate(self._worlds, start=1)
        ]
        self.set_items(worldlist)

    async def _fetch_data(self) -> None:
        self._worlds = await self._view.bot.fazwynn_db.worlds.get_worlds(self._sort_by)
