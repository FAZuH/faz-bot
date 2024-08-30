from __future__ import annotations

from datetime import timezone
from typing import TYPE_CHECKING, Any, Literal, override

from nextcord import Color, Embed
from tabulate import tabulate

from fazcord.bot.view._base_pagination_view import BasePaginationView
from fazcord.bot.view._pagination_embed import PaginationEmbed
from fazcord.bot.view._view_utils import ViewUtils

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazcord.bot.bot import Bot


class WorldlistView(BasePaginationView):

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        sort_by: Literal["Player Count", "Time Created"],
    ) -> None:
        self._sort_by: Literal["player", "time"] = (
            "player" if sort_by == "Player Count" else "time"
        )
        super().__init__(bot, interaction)

    @override
    async def run(self):
        self._items = await self._bot.fazdb_db.worlds_repository.get_worlds(
            self._sort_by
        )
        self._embed = PaginationEmbed(
            self._interaction, self._items, title="World List", color=Color.dark_teal()
        )
        await self._interaction.send(embed=self._get_embed_page(1), view=self)

    @override
    def _get_embed_page(self, page: int) -> Embed:
        embed = self._embed.get_base()
        embed.current_page = page
        worlds = embed.get_items(page)
        worldlist = [
            [
                n,
                world.name,
                world.player_count,
                ViewUtils.format_timedelta(
                    self._interaction.created_at
                    - world.time_created.replace(tzinfo=timezone.utc)
                ),
            ]
            for n, world in enumerate(
                worlds, start=1 + embed.items_per_page * (embed.current_page - 1)
            )
        ]
        embed.description = (
            "```ml\n"
            + tabulate(
                worldlist,
                headers=["No", "World", "Players", "Uptime"],
                tablefmt="github",
            )
            + "\n```"
        )
        embed.finalize()
        return embed
