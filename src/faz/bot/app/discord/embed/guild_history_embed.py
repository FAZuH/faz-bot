from __future__ import annotations

from datetime import datetime
from typing import override, Sequence, TYPE_CHECKING

from nextcord import Colour
import pandas as pd

from faz.bot.app.discord.embed.embed_field import EmbedField
from faz.bot.app.discord.embed.pagination_embed import PaginationEmbed
from faz.bot.app.discord.select.guild_history_id_options import GuildHistoryIdOptions
from faz.bot.app.discord.series_parser.guild_history_series_parser import GuildHistorySeriesParser

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.guild_info import GuildInfo

    from faz.bot.app.discord.select.guild_history_mode_options import GuildHistoryModeOptions
    from faz.bot.app.discord.view.wynn_history.guild_history_view import GuildHistoryView


class GuildHistoryEmbed(PaginationEmbed[EmbedField]):
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
        title = f"Guild History ({guild.name})"
        desc = f"`Period : ` <t:{begin_ts}:R> to <t:{end_ts}:R>"
        super().__init__(
            view.interaction,
            items_per_page=4,
            title=title,
            description=desc,
            color=Colour.teal(),
        )
        self._db = view.bot.app.create_fazwynn_db()
        self._parsers = GuildHistorySeriesParser()

    async def get_fields(
        self, mode: GuildHistoryModeOptions | GuildHistoryIdOptions
    ) -> Sequence[EmbedField]:
        # Prepare
        db = self._db
        fields: Sequence[EmbedField] = []
        guild = self._guild
        begin = self._period_begin
        end = self._period_end

        await guild.awaitable_attrs.members

        guild_df = db.guild_history.select_between_period_as_dataframe(guild.uuid, begin, end)
        player_df = pd.DataFrame()

        for member in guild.members:
            player_df_: pd.DataFrame = db.player_history.select_between_period_as_dataframe(
                member.uuid, begin, end
            )
            if player_df_.empty:
                continue
            player_df = pd.concat([player_df, player_df_])

        parser = self._parsers.get_parser(mode)
        fields = parser(guild_df, player_df)
        if not fields:
            return [
                EmbedField(
                    mode.value,
                    "No data found within the selected period of time.",
                )
            ]
        return fields

    @override
    def get_embed_page(self, page: int | None = None) -> GuildHistoryEmbed:
        """Build specific page of the PaginationEmbed."""
        if page is None:
            page = self.current_page
        embed = self.get_base()
        fields = embed.get_items(page)

        if len(fields) == 0:
            embed.description = "```ml\nNo data found.\n```"
        else:
            for field in fields:
                embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=field.inline,
                )

        embed.finalize()
        return embed
