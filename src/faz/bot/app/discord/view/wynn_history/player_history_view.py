from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import TYPE_CHECKING, Any, override
from uuid import UUID

from nextcord.ui import StringSelect

from faz.bot.app.discord.view._base_pagination_view import BasePaginationView
from faz.bot.app.discord.embed.history_player_history_embed import (
    HistoryPlayerHistoryEmbed,
)
from faz.bot.app.discord.select.id_select import IdSelect
from faz.bot.app.discord.select.id_select_options import IdSelectOptions

if TYPE_CHECKING:
    from nextcord import Interaction

    from faz.bot.app.discord.bot.bot import Bot
    from faz.bot.database.fazwynn.model.player_info import PlayerInfo


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

        self._embed = HistoryPlayerHistoryEmbed(
            self,
            self._player,
            self._period_begin,
            self._period_end,
            self._character_labels,
        )

        self._selected_character: str | None = None
        self._selected_id: IdSelectOptions = IdSelectOptions.ALL

    @override
    async def run(self) -> None:
        """Initial method to setup and run the view."""
        await self._add_id_select()
        await self._add_character_select()

        await self._set_embed_fields()
        embed = self._get_embed_page()
        await self._interaction.send(embed=embed, view=self)

    async def _add_id_select(self) -> None:
        """Helper method to add ID selection during setup."""
        self._id_select = IdSelect(self._id_select_callback)
        self.add_item(self._id_select)

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
        """Callback for ID selection."""
        # Length of values is always 1
        self._selected_id = self._id_select.get_selected_option()
        await self._set_embed_fields()
        embed = self._get_embed_page()
        await interaction.edit(embed=embed, view=self)

    async def _character_select_callback(self, interaction: Interaction) -> None:
        """Callback for character selection."""
        # Length of values is always 1
        self._selected_character = self._character_select.values[0]
        if self._selected_character.lower() == "total":
            self._selected_character = None
        await self._set_embed_fields()
        embed = self._get_embed_page()
        await interaction.edit(embed=embed, view=self)

    async def _set_embed_fields(self) -> None:
        """Sets PaginationEmbed items with fields based on selected options."""
        fields = await self.embed.get_fields(self._selected_character, self._selected_id)
        self.embed.items = fields

    def _get_embed_page(self) -> HistoryPlayerHistoryEmbed:
        embed = self.embed.get_embed_page(self.embed.current_page)
        embed.description += "\n`Data   : ` "
        if self._selected_character is None:
            embed.description += "All characters"
        else:
            char_label = self._character_labels[self._selected_character]
            embed.description += char_label
        return embed

    @property
    @override
    def embed(self) -> HistoryPlayerHistoryEmbed:
        """The embed property."""
        return self._embed
