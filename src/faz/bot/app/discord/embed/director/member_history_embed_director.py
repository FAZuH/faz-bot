from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import override, Self, TYPE_CHECKING
from uuid import UUID

from nextcord import Embed
import pandas as pd

from faz.bot.app.discord.embed.builder.description_builder import DescriptionBuilder
from faz.bot.app.discord.embed.builder.field_pagination_embed_builder import (
    FieldPaginationEmbedBuilder,
)
from faz.bot.app.discord.embed.builder.member_history_field_builder import MemberHistoryFieldBuilder
from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.player_info import PlayerInfo

    from faz.bot.app.discord.select.member_history_data_option import MemberHistoryDataOption
    from faz.bot.app.discord.select.member_history_mode_option import MemberHistoryModeOption
    from faz.bot.app.discord.view.wynn_history.member_history_view import MemberHistoryView


class MemberHistoryEmbedDirector(BasePaginationEmbedDirector):
    def __init__(
        self,
        view: MemberHistoryView,
        player: PlayerInfo,
        period_begin: datetime,
        period_end: datetime,
    ) -> None:
        self._period_begin = period_begin
        self._period_end = period_end
        self._player = player

        begin_ts = int(period_begin.timestamp())
        end_ts = int(period_end.timestamp())

        self._desc_builder = DescriptionBuilder().set_builder_initial_lines(
            [("Period", f"<t:{begin_ts}:R> to <t:{end_ts}:R>")]
        )
        self._embed_builder = FieldPaginationEmbedBuilder(
            view.interaction, items_per_page=4
        ).set_builder_initial_embed(Embed(title=f"Member History ({self._player.latest_username})"))
        self.field_builder = MemberHistoryFieldBuilder()

        self._db = view.bot.app.create_fazwynn_db()

    @override
    async def setup(self) -> None:
        await self._player.awaitable_attrs.characters
        self._fetch_data()
        await self._setup_character_lables()
        self.field_builder.set_data(self._char_df, self._member_df).set_character_labels(
            self._character_labels
        )

    def set_options(self, data: MemberHistoryDataOption, mode: MemberHistoryModeOption) -> Self:
        self._data = data
        self._mode = mode
        return self

    @override
    def construct(self) -> Embed:
        data = self._data
        mode = self._mode
        fields = self.field_builder.set_data_option(data).set_mode_option(mode).build()
        desc = (
            self._desc_builder.reset()
            .add_line("Data", data.value)
            .add_line("Mode", mode.value)
            .build()
        )
        embed = self.prepare_default().set_description(desc).set_builder_items(fields).build()
        return embed

    def _fetch_data(self) -> None:
        self._char_df = pd.DataFrame()

        for ch in self._player.characters:
            df_char_ = self._db.character_history.select_between_period_as_dataframe(
                ch.character_uuid, self._period_begin, self._period_end
            )
            if df_char_.empty:
                continue
            self._char_df = pd.concat([self._char_df, df_char_])

        self._member_df = self._db.guild_member_history.select_between_period_as_dataframe(
            self._player.uuid, self._period_begin, self._period_end
        )

    async def _setup_character_lables(self) -> None:
        ch_counter = defaultdict(int)
        self._character_labels = {}
        for ch in self._player.characters:
            ch_hists = await self._db.character_history.select_between_period(
                ch.character_uuid, self._period_begin, self._period_end
            )
            if len(ch_hists) == 0:
                continue

            ch_counter[ch.type] += 1

            latest_ch_hist = max(ch_hists, key=lambda x: x.datetime)
            total_level = latest_ch_hist.get_total_level()

            label = f"{ch.type}{ch_counter[ch.type]} (Lv. {total_level})"
            uuid = str(UUID(bytes=ch.character_uuid))

            self._character_labels[uuid] = label

    @property
    @override
    def embed_builder(self) -> FieldPaginationEmbedBuilder:
        return self._embed_builder
