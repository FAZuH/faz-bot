from __future__ import annotations

from datetime import datetime
from typing import Any, override, TYPE_CHECKING

from faz.bot.app.discord.embed.director.guild_history_embed_director import (
    GuildHistoryEmbedDirector,
)
from faz.bot.app.discord.select.guild_history_data_options import GuildHistoryDataOption
from faz.bot.app.discord.select.guild_history_data_select import GuildHistoryDataSelect
from faz.bot.app.discord.select.guild_history_mode_options import GuildHistoryModeOptions
from faz.bot.app.discord.select.guild_history_mode_select import GuildHistoryModeSelect
from faz.bot.app.discord.view._base_pagination_view import BasePaginationView

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.guild_info import GuildInfo
    from nextcord import Interaction

    from faz.bot.app.discord.bot.bot import Bot


class GuildHistoryView(BasePaginationView):
    """View for history guild_history command.

    ## Data

    - Member list
    - Guild level
    - Territories (Future)

    ## Command parameters

    - guild: str
    - period: str

    ## Further options

    - Mode (StringSelect)
        - Overall: Earliest vs latest
        - Historical: Show stat for each data point

    - Data (StringSelect) (For Historical mode)
        - Member list
        - Guild level
        - Territories (Future)
    """

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        guild: GuildInfo,
        period_begin: datetime,
        period_end: datetime,
    ) -> None:
        super().__init__(bot, interaction)
        self._guild = guild
        self._period_begin = period_begin
        self._period_end = period_end

        self._options: str | None = None
        self._selected_mode: GuildHistoryModeOptions = GuildHistoryModeOptions.OVERALL
        self._selected_data: GuildHistoryDataOption = GuildHistoryDataOption.MEMBER_LIST

        self._mode_select = GuildHistoryModeSelect(self._mode_select_callback)
        self._data_select = GuildHistoryDataSelect(self._data_select_callback)

        self._embed_director = GuildHistoryEmbedDirector(
            self,
            guild,
            period_begin,
            period_end,
        )

    @override
    async def run(self) -> None:
        """Initial method to setup and run the view."""
        self.add_item(self._mode_select)

        await self.embed_director.setup()
        self.set_embed_director_options()
        await self._initial_send_message()

    async def _mode_select_callback(self, interaction: Interaction[Any]) -> None:
        """Callback for mode selection."""
        # Length of values is always 1
        self._selected_mode = self._mode_select.get_selected_option()
        if self._selected_mode == GuildHistoryModeOptions.OVERALL:
            self.remove_item(self._data_select)
        elif self._data_select not in self.children:
            self.add_item(self._data_select)
        self.set_embed_director_options()
        await self._edit_message_page(interaction)

    async def _data_select_callback(self, interaction: Interaction[Any]) -> None:
        """Callback for data selection."""
        # Length of values is always 1
        self._selected_data = self._data_select.get_selected_option()
        self.set_embed_director_options()
        await self._edit_message_page(interaction)

    def set_embed_director_options(self) -> None:
        self.embed_director.set_options(self._selected_data, self._selected_mode)
    
    @property
    @override
    def embed_director(self) -> GuildHistoryEmbedDirector:
        return self._embed_director
