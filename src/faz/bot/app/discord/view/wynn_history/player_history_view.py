from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, override, TYPE_CHECKING
from uuid import UUID

from nextcord.ui import StringSelect

from faz.bot.app.discord.embed.director.player_history_embed_director import (
    PlayerHistoryEmbedDirector,
)
from faz.bot.app.discord.select.player_history_data_option import PlayerHistoryDataOption
from faz.bot.app.discord.select.player_history_data_select import PlayerHistoryDataSelect
from faz.bot.app.discord.view._base_pagination_view import BasePaginationView

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.player_info import PlayerInfo
    from nextcord import Interaction

    from faz.bot.app.discord.bot.bot import Bot


class PlayerHistoryView(BasePaginationView):
    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        player: PlayerInfo,
        period_begin: datetime,
        period_end: datetime,
    ) -> None:
        super().__init__(bot, interaction)
        self._player = player
        self._period_begin = period_begin
        self._period_end = period_end

        self._character_labels: dict[str, str] = {}

        self._embed_director = PlayerHistoryEmbedDirector(
            self,
            self._player,
            self._period_begin,
            self._period_end,
            self._character_labels,
        )

        self._selected_character: str | None = None
        self._selected_data: PlayerHistoryDataOption = PlayerHistoryDataOption.ALL

        self._data_select = PlayerHistoryDataSelect(self._id_select_callback)

    @override
    async def run(self) -> None:
        """Initial method to setup and run the view."""
        self.add_item(self._data_select)
        await self._add_character_select()

        await self._embed_director.setup()
        self.set_embed_director_options()
        await self._initial_send_message()

    async def _add_character_select(self) -> None:
        """Helper method to add character selection during setup."""
        self._character_select = StringSelect(placeholder="Select character")
        self._character_select.callback = self._character_select_callback
        self._character_select.add_option(label="Total", value="total")

        await self._player.awaitable_attrs.characters
        ch_counter = defaultdict(int)
        for ch in self._player.characters:
            ch_hists = await self.bot.fazwynn_db.character_history.select_between_period(
                ch.character_uuid, self._period_begin, self._period_end
            )
            if len(ch_hists) == 0:
                continue
            ch_counter[ch.type] += 1
            # select ch_hist with max datetime
            latest_ch_hist = max(ch_hists, key=lambda x: x.datetime)
            total_level = latest_ch_hist.get_total_level()
            label = f"{ch.type}{ch_counter[ch.type]} (Lv. {total_level})"
            uuid = str(UUID(bytes=ch.character_uuid))
            self._character_select.add_option(label=label, value=uuid)
            self._character_labels[uuid] = label

        if len(self._character_select.options) == 0:
            self._character_select.placeholder = "No character"
            self._character_select.disabled = True

        self.add_item(self._character_select)

    async def _id_select_callback(self, interaction: Interaction) -> None:
        """Callback for data selection."""
        # Length of values is always 1
        self._selected_data = self._data_select.get_selected_option()
        self.set_embed_director_options()
        await self._edit_message_page(interaction)

    async def _character_select_callback(self, interaction: Interaction) -> None:
        """Callback for character selection."""
        # Length of values is always 1
        self._selected_character = self._character_select.values[0]
        if self._selected_character.lower() == "total":
            self._selected_character = None
        self.set_embed_director_options()
        await self._edit_message_page(interaction)

    def set_embed_director_options(self) -> None:
        self.embed_director.set_options(self._selected_data, self._selected_character)

    @property
    @override
    def embed_director(self) -> PlayerHistoryEmbedDirector:
        return self._embed_director
