from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Sequence, override
from uuid import UUID

import pandas as pd
from faz.bot.database.fazwynn.model.player_info import PlayerInfo
from nextcord import Colour

from faz.bot.app.discord.bot.errors import ApplicationException
from faz.bot.app.discord.embed.embed_field import EmbedField
from faz.bot.app.discord.embed.pagination_embed import PaginationEmbed
from faz.bot.app.discord.select.player_history_id_options import (
    PlayerHistoryIdOptions,
    PlayerHistoryIdOptionsType,
)
from faz.bot.app.discord.series_parser.player_history_series_parser import PlayerHistorySeriesParser

if TYPE_CHECKING:
    from faz.bot.app.discord.view.wynn_history.player_history_view import PlayerHistoryView


class PlayerHistoryEmbed(PaginationEmbed[EmbedField]):
    def __init__(
        self,
        view: PlayerHistoryView,
        player: PlayerInfo,
        period_begin: datetime,
        period_end: datetime,
        character_labels: dict[str, str],
    ) -> None:
        self._period_begin = period_begin
        self._period_end = period_end
        self._player = player
        begin_ts = int(period_begin.timestamp())
        end_ts = int(period_end.timestamp())
        title = f"Player History ({player.latest_username})"
        desc = f"`Period : ` <t:{begin_ts}:R> to <t:{end_ts}:R>"
        super().__init__(
            view.interaction,
            items_per_page=4,
            title=title,
            description=desc,
            color=Colour.teal(),
        )
        self._db = view.bot.app.create_fazwynn_db()
        self._parsers = PlayerHistorySeriesParser(character_labels)

    async def get_fields(
        self, character_uuid: str | None, id: PlayerHistoryIdOptions
    ) -> Sequence[EmbedField]:
        # Prepare
        db = self._db
        await self._player.awaitable_attrs.characters
        player_hist = db.player_history.select_between_period_as_dataframe(
            self._player.uuid, self._period_begin, self._period_end
        )
        df_char = pd.DataFrame()

        # Data: Total or Character
        if character_uuid is None:
            # Combine all characters data into df_character
            for ch in self._player.characters:
                df_char_ = db.character_history.select_between_period_as_dataframe(
                    ch.character_uuid, self._period_begin, self._period_end
                )
                if df_char_.empty:
                    continue
                df_char = pd.concat([df_char, df_char_])
        else:
            df_char = db.character_history.select_between_period_as_dataframe(
                UUID(character_uuid).bytes, self._period_begin, self._period_end
            )

        # Id type: Categorical, Numerical, or All
        #
        # Categorical for Total
        # Numerical for Total, Character
        # All for Total, Character
        type_ = id.type
        if type_ == PlayerHistoryIdOptionsType.CATEGORICAL:
            fields = self._get_fields_categorical(player_hist, id)
        elif type_ == PlayerHistoryIdOptionsType.NUMERICAL:
            fields = self._get_fields_numerical(player_hist, df_char, id)
        elif type_ == PlayerHistoryIdOptionsType.ALL:
            fields = self._get_fields_numerical(player_hist, df_char, id)
        else:
            raise ApplicationException("This should not happen")

        return fields

    def _get_fields_categorical(
        self, player_history: pd.DataFrame, id: PlayerHistoryIdOptions
    ) -> Sequence[EmbedField]:
        parser = self._parsers.get_categorical_parser(id)
        fields = parser(player_history)
        if not fields:
            return [self._get_no_data_field(id)]
        return fields

    def _get_fields_numerical(
        self,
        player_history: pd.DataFrame,
        character_history: pd.DataFrame,
        id: PlayerHistoryIdOptions,
    ) -> Sequence[EmbedField]:
        parser = self._parsers.get_numerical_parser(id)
        fields = parser(player_history, character_history)
        if not fields:
            return [self._get_no_data_field(id)]
        return fields

    def _get_no_data_field(self, id: PlayerHistoryIdOptions) -> EmbedField:
        ret = EmbedField(
            id.value.value,
            "No data found within the selected period of time.",
        )
        return ret

    @override
    def get_embed_page(self, page: int) -> PlayerHistoryEmbed:
        """Build specific page of the PaginationEmbed."""
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
