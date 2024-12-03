from __future__ import annotations

from typing import Self, override, TYPE_CHECKING

from nextcord import Embed
import pandas as pd

from faz.bot.app.discord.embed.builder.custom_description_builder import CustomDescriptionBuilder
from faz.bot.app.discord.embed.builder.field_pagination_embed_builder import (
    FieldPaginationEmbedBuilder,
)
from faz.bot.app.discord.embed.builder.guild_history_field_builder import GuildHistoryFieldBuilder
from faz.bot.app.discord.embed.director._base_pagination_embed_director import (
    BasePaginationEmbedDirector,
)

if TYPE_CHECKING:
    from datetime import datetime

    from faz.bot.database.fazwynn.model.guild_info import GuildInfo

    from faz.bot.app.discord.select.guild_history_data_options import GuildHistoryDataOption
    from faz.bot.app.discord.select.guild_history_mode_options import GuildHistoryModeOptions
    from faz.bot.app.discord.view.wynn_history.guild_history_view import GuildHistoryView


class GuildHistoryEmbedDirector(BasePaginationEmbedDirector):
    def __init__(
        self,
        view: GuildHistoryView,
        guild: GuildInfo,
        period_begin: datetime,
        period_end: datetime,
    ) -> None:
        self._period_begin = period_begin
        self._period_end = period_end
        self._guild = guild

        begin_ts = int(period_begin.timestamp())
        end_ts = int(period_end.timestamp())

        self._desc_builder = CustomDescriptionBuilder().set_builder_initial_lines(
            [("Period", f"<t:{begin_ts}:R> to <t:{end_ts}:R>")]
        )
        self._embed_builder = FieldPaginationEmbedBuilder(
            view.interaction, items_per_page=4
        ).set_builder_initial_embed(Embed(title=f"Guild History ({guild.name})"))
        self.field_builder = GuildHistoryFieldBuilder()

        self._db = view.bot.app.create_fazwynn_db()

    @override
    async def setup(self) -> None:
        await self._fetch_data()
        self.field_builder.set_data(self._player_df, self._guild_df)

    def set_options(self, data: GuildHistoryDataOption, mode: GuildHistoryModeOptions) -> Self:
        self._data = data
        self._mode = mode
        return self

    @override
    def construct(self) -> Embed:
        data = self._data
        mode = self._mode
        fields = self.field_builder.set_data_option(data).set_mode_option(mode).build()
        desc = self._desc_builder.reset().add_line("Data", data.value).add_line("Mode", mode.value).build()
        embed = self.prepare_default().set_description(desc).set_builder_items(fields).build()
        return embed

    async def _fetch_data(self) -> None:
        await self._guild.awaitable_attrs.members

        self._player_df = pd.DataFrame()
        for member in self._guild.members:
            player_df_: pd.DataFrame = self._db.player_history.select_between_period_as_dataframe(
                member.uuid, self._period_begin, self._period_end
            )
            if player_df_.empty:
                continue
            self._player_df = pd.concat([self._player_df, player_df_])

        self._guild_df = self._db.guild_history.select_between_period_as_dataframe(
            self._guild.uuid, self._period_begin, self._period_end
        )

    @property
    @override
    def embed_builder(self) -> FieldPaginationEmbedBuilder:
        return self._embed_builder
