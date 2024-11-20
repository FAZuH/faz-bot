from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Sequence, override
from uuid import UUID

import pandas as pd
from nextcord import Colour

from fazcord.bot.errors import ApplicationException
from fazcord.embed.embed_field import EmbedField
from fazcord.select.id_select_options import IdSelectOptions, IdSelectOptionsType
from fazcord.embed.pagination_embed import PaginationEmbed
from fazcord.series_parser.player_history_series_parser import PlayerHistorySeriesParser
from fazutil.db.fazwynn.model.player_info import PlayerInfo

if TYPE_CHECKING:
    from fazcord.view.history_player_history_view import HistoryPlayerHistoryView


class HistoryPlayerHistoryEmbed(PaginationEmbed[EmbedField]):

    def __init__(
        self,
        view: HistoryPlayerHistoryView,
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
        self, character_uuid: str | None, id: IdSelectOptions
    ) -> Sequence[EmbedField]:
        # Prepare
        db = self._db
        await self._player.awaitable_attrs.characters
        player_hist = db.player_history.select_between_period_as_dataframe(
            self._player.uuid, self._period_begin, self._period_end
        )
        character_hist = pd.DataFrame()

        # Data: Total or Character
        if character_uuid is None:
            # Combine all characters data into df_character
            for ch in self._player.characters:
                df_char_ = db.character_history.select_between_period_as_dataframe(
                    ch.character_uuid, self._period_begin, self._period_end
                )
                if len(df_char_) == 0:
                    continue
                character_hist = pd.concat([character_hist, df_char_])
        else:
            character_hist = db.character_history.select_between_period_as_dataframe(
                UUID(character_uuid).bytes, self._period_begin, self._period_end
            )

        # Id type: Categorical, Numerical, or All
        #
        # Categorical for Total
        # Numerical for Total, Character
        # All for Total, Character
        type_ = id.type
        if type_ == IdSelectOptionsType.CATEGORICAL:
            fields = self._get_fields_categorical(player_hist, id)
        elif type_ == IdSelectOptionsType.NUMERICAL:
            fields = self._get_fields_numerical(player_hist, character_hist, id)
        elif type_ == IdSelectOptionsType.ALL:
            fields = self._get_fields_numerical(player_hist, character_hist, id)
        else:
            raise ApplicationException("This should not happen")

        return fields

    def _get_fields_categorical(
        self, player_history: pd.DataFrame, id: IdSelectOptions
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
        id: IdSelectOptions,
    ) -> Sequence[EmbedField]:
        parser = self._parsers.get_numerical_parser(id)
        fields = parser(player_history, character_history)
        if not fields:
            return [self._get_no_data_field(id)]
        return fields

    def _get_no_data_field(self, id: IdSelectOptions) -> EmbedField:
        ret = EmbedField(
            id.value.value,
            "No data found within the selected period of time.",
        )
        return ret

    @override
    def get_embed_page(self, page: int) -> HistoryPlayerHistoryEmbed:
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
