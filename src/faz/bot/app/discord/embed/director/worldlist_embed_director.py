from __future__ import annotations

from datetime import timezone
from typing import Literal, override, TYPE_CHECKING

from discord import Colour
from nextcord import Embed
from tabulate import tabulate

from faz.bot.app.discord.embed.builder.pagination_embed_builder import PaginationEmbedBuilder
from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)
from faz.bot.app.discord.view._view_utils import ViewUtils

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.worlds import Worlds

    from faz.bot.app.discord.view.wynn_stat.worldlist_view import WorldlistView


class WorldlistEmbedDirector(BasePaginationEmbedDirector):
    def __init__(self, view: WorldlistView, sort_by: Literal["player", "time"]) -> None:
        self._view = view
        self._interaction = view.interaction
        self._sort_by: Literal["player", "time"] = sort_by

        self._embed_builder = PaginationEmbedBuilder(
            self._interaction,
        ).set_builder_initial_embed(Embed(title="World List"))

    @override
    async def setup(self) -> None:
        await self._fetch_data()
        self.embed_builder.set_builder_items(self._worlds)

    @override
    def construct(self) -> Embed:
        builder = self.prepare_default()
        worldlist = [
            [
                n,
                world.name,
                world.player_count,
                ViewUtils.format_timedelta(
                    self._interaction.created_at - world.time_created.replace(tzinfo=timezone.utc)
                ),
            ]
            for n, world in enumerate(
                builder.get_items(), start=1 + builder.items_per_page * (builder.current_page - 1)
            )
        ]
        desc = (
            "```ml\n"
            + tabulate(
                worldlist,
                headers=["No", "World", "Players", "Uptime"],
                tablefmt="github",
            )
            + "\n```"
        )
        embed = builder.set_description(desc).set_colour(Colour.dark_teal()).build()
        return embed

    async def _fetch_data(self) -> None:
        self._worlds = await self._view.bot.fazwynn_db.worlds.get_worlds(self._sort_by)

    @property
    @override
    def embed_builder(self) -> PaginationEmbedBuilder[Worlds]:
        return self._embed_builder
