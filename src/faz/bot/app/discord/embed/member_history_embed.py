from __future__ import annotations
import asyncio

from collections import defaultdict
from datetime import datetime
from typing import override, Sequence, TYPE_CHECKING
from uuid import UUID

from nextcord import Colour
import pandas as pd

from faz.bot.app.discord.embed.embed_field import EmbedField
from faz.bot.app.discord.embed.pagination_embed import PaginationEmbed
from faz.bot.app.discord.series_parser.member_history_series_parser import MemberHistorySeriesParser

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.player_info import PlayerInfo

    from faz.bot.app.discord.select.member_history_data_option import MemberHistoryDataOption
    from faz.bot.app.discord.select.member_history_mode_option import MemberHistoryModeOption
    from faz.bot.app.discord.view.wynn_history.member_history_view import MemberHistoryView


class MemberHistoryEmbed(PaginationEmbed[EmbedField]):
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
        title = f"Member History ({player.latest_username})"
        desc = f"`Period : ` <t:{begin_ts}:R> to <t:{end_ts}:R>"
        super().__init__(
            view.interaction,
            items_per_page=4,
            title=title,
            description=desc,
            color=Colour.teal(),
        )

        self._db = view.bot.app.create_fazwynn_db()

    async def setup(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._fetch_data())
            tg.create_task(self._setup_parser())

    async def get_fields(
        self,
        data: MemberHistoryDataOption,
        mode: MemberHistoryModeOption,
    ) -> Sequence[EmbedField]:
        # Prepare
        fields: Sequence[EmbedField] = []
        parser = self._parsers.get_parser(data, mode)
        fields = parser(self._char_df, self._member_df)
        if not fields:
            return [
                EmbedField(
                    mode.value,
                    "No data found within the selected period of time.",
                )
            ]
        return fields

    @override
    def get_embed_page(self, page: int | None = None) -> MemberHistoryEmbed:
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

    async def _fetch_data(self) -> None:
        db = self._db
        player = self._player
        begin = self._period_begin
        end = self._period_end

        await player.awaitable_attrs.characters

        self._char_df = pd.DataFrame()

        for ch in self._player.characters:
            df_char_ = db.character_history.select_between_period_as_dataframe(
                ch.character_uuid, begin, end
            )
            if df_char_.empty:
                continue
            self._char_df = pd.concat([self._char_df, df_char_])

        self._member_df = db.guild_member_history.select_between_period_as_dataframe(
            player.uuid, begin, end
        )

    async def _setup_parser(self) -> None:
        db = self._db
        begin = self._period_begin
        end = self._period_end

        await self._player.awaitable_attrs.characters

        ch_counter = defaultdict(int)
        character_labels = {}
        for ch in self._player.characters:
            ch_hists = await db.character_history.select_between_period(
                ch.character_uuid, begin, end
            )
            if len(ch_hists) == 0:
                continue
            ch_counter[ch.type] += 1
            # select ch_hist with max datetime
            latest_ch_hist = max(ch_hists, key=lambda x: x.datetime)
            total_level = latest_ch_hist.get_total_level()
            label = f"{ch.type}{ch_counter[ch.type]} (Lv. {total_level})"
            uuid = str(UUID(bytes=ch.character_uuid))
            character_labels[uuid] = label

        self._parsers = MemberHistorySeriesParser(character_labels)
