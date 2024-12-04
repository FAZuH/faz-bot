from typing import Callable, override, Self, Sequence
from uuid import UUID

import pandas as pd

from faz.bot.app.discord.embed.builder._base_field_builder import BaseFieldBuilder
from faz.bot.app.discord.embed.embed_field import EmbedField
from faz.bot.app.discord.select.member_history_data_option import MemberHistoryDataOption
from faz.bot.app.discord.select.member_history_mode_option import MemberHistoryModeOption


class MemberHistoryFieldBuilder(BaseFieldBuilder):
    def __init__(self) -> None:
        self._historical_parsers: dict[
            MemberHistoryDataOption,
            Callable[[], Sequence[EmbedField]],
        ] = {}

        hist_prsr = self._historical_parsers
        hist_prsr[MemberHistoryDataOption.WARS] = self._parser_historical_wars
        hist_prsr[MemberHistoryDataOption.XP_CONTRIBUTION] = self._parser_historical_contributed

    def set_character_labels(self, character_labels: dict[str, str]) -> Self:
        self._character_labels = character_labels
        return self

    def set_mode_option(self, mode: MemberHistoryModeOption) -> Self:
        self._mode = mode
        return self

    def set_data_option(self, data: MemberHistoryDataOption) -> Self:
        self._data = data
        return self

    def set_data(self, char_df: pd.DataFrame, member_df: pd.DataFrame) -> Self:
        self._char_df = char_df
        self._member_df = member_df
        return self

    @override
    def build(self) -> Sequence[EmbedField]:
        if self._mode == MemberHistoryModeOption.OVERALL:
            parser = self._parser_overall
        elif self._mode == MemberHistoryModeOption.HISTORICAL:
            parser = self._historical_parsers[self._data]
        return parser()  # type: ignore

    def _parser_overall(
        self,
    ) -> Sequence[EmbedField]:
        ret: Sequence[EmbedField] = []

        lines = {}

        self._char_df.replace("", "None", inplace=True)
        self._member_df.replace("", "None", inplace=True)

        if len(self._char_df) == 0 and len(self._member_df) == 0:
            return ret

        total_war_count = 0
        for _, group in self._char_df.groupby("character_uuid"):
            sorted_group = group.sort_values("datetime")
            first_war = sorted_group.iloc[0]["wars"]
            last_war = sorted_group.iloc[-1]["wars"]
            total_war_count += last_war - first_war

        if total_war_count != 0:
            lines["Wars"] = f"+{total_war_count}"

        earliest_member = self._member_df.iloc[self._member_df["datetime"].idxmin()]  # type: ignore
        latest_member = self._member_df.iloc[self._member_df["datetime"].idxmax()]  # type: ignore

        xp1 = earliest_member["contributed"]
        xp2 = latest_member["contributed"]

        if xp1 != xp2:
            lines["XP Contributed"] = f"{xp1} -> {xp2}"

        label_space = self._get_max_key_length(lines)
        desc = "\n".join(
            [self._diff_str_or_blank(value, label, label_space) for label, value in lines.items()]
        )
        ret = []
        self._add_embed_field(ret, "Overall", desc)
        return ret

    def _parser_historical_wars(
        self,
    ) -> Sequence[EmbedField]:
        ret: Sequence[EmbedField] = []
        for chuuid, chlabel in self._character_labels.items():
            char = self._char_df[self._char_df["character_uuid"] == UUID(chuuid).bytes]
            lines: list[str] = []
            prev_value = None
            for _, row in char.iterrows():
                value = row["wars"]
                if prev_value == value:
                    continue
                prev_value = value
                timestamp = self._get_formatted_timestamp(row)
                line = f"{timestamp}: {value}"
                lines.append(line)
            if prev_value is None:
                continue
            desc = "\n".join(lines)
            self._add_embed_field(ret, chlabel, desc)
        return ret

    def _parser_historical_contributed(
        self,
    ) -> Sequence[EmbedField]:
        ret: Sequence[EmbedField] = []
        lines: list[str] = []
        prev_value = None
        for _, row in self._member_df.iterrows():
            value = row["contributed"]
            if prev_value == value:
                continue
            prev_value = value
            timestamp = self._get_formatted_timestamp(row)
            line = f"{timestamp}: {value}"
            lines.append(line)
            if prev_value is None:
                continue
        desc = "\n".join(lines)
        self._add_embed_field(ret, "XP Contributed", desc)
        return ret
