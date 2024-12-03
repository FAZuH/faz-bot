from typing import Callable, override, Self, Sequence

import pandas as pd

from faz.bot.app.discord.embed.builder._base_field_builder import BaseFieldBuilder
from faz.bot.app.discord.embed.embed_field import EmbedField
from faz.bot.app.discord.select.guild_history_data_options import GuildHistoryDataOption
from faz.bot.app.discord.select.guild_history_mode_options import GuildHistoryModeOptions


class GuildHistoryFieldBuilder(BaseFieldBuilder):
    def __init__(self) -> None:
        self._parsers: dict[
            GuildHistoryModeOptions | GuildHistoryDataOption,
            Callable[[], Sequence[EmbedField]],
        ] = {}

        self._parsers[GuildHistoryModeOptions.OVERALL] = self._parser_overall
        self._parsers[GuildHistoryDataOption.MEMBER_LIST] = self._parser_historical_member_list
        self._parsers[GuildHistoryDataOption.GUILD_LEVEL] = self._parser_historical_guild_level
        self._parsers[GuildHistoryDataOption.TERRITORIES] = self._parser_historical_territories

    def set_mode_option(self, mode: GuildHistoryModeOptions) -> Self:
        self._mode = mode
        return self

    def set_data_option(self, data: GuildHistoryDataOption) -> Self:
        self._data = data
        return self

    def set_data(self, player_df: pd.DataFrame, guild_df: pd.DataFrame) -> Self:
        self._player_df = player_df
        self._guild_df = guild_df
        return self

    @override
    def build(self) -> Sequence[EmbedField]:
        if self._mode == GuildHistoryModeOptions.OVERALL:
            parser = self._parsers[self._mode]
        else:
            parser = self._parsers[self._data]
        return parser()

    def _parser_overall(
        self,
    ) -> Sequence[EmbedField]:
        self._player_df.replace("", "None", inplace=True)
        self._guild_df.replace("", "None", inplace=True)
        ret: Sequence[EmbedField] = []
        if len(self._guild_df) == 0:
            return []
        earliest: pd.Series = self._guild_df.iloc[self._guild_df["datetime"].idxmin()]  # type: ignore
        latest: pd.Series = self._guild_df.iloc[self._guild_df["datetime"].idxmax()]  # type: ignore

        level1 = earliest["level"]
        level2 = latest["level"]

        if level1 != level2:
            self._add_embed_field(ret, "Level", f"{level1} -> {level2}")

        # HACK: This is inefficient
        lines_guild = {}
        lines_rank = {}
        for uuid in pd.unique(self._player_df["uuid"]):
            player = self._player_df[self._player_df["uuid"] == uuid]
            earliest_: pd.Series = player.iloc[player["datetime"].idxmin()]  # type: ignore
            latest_: pd.Series = player.iloc[player["datetime"].idxmax()]  # type: ignore

            username = latest_["username"]

            guild1 = earliest_["guild_name"]
            guild2 = latest_["guild_name"]

            if guild1 != guild2:
                lines_guild[username] = f"{guild1} -> {guild2}"

            rank1 = earliest_["guild_rank"]
            rank2 = latest_["guild_rank"]

            if rank1 != rank2:
                lines_rank[username] = f"{rank1} -> {rank2}"

        if not len(lines_guild) == 0:
            label_space = self._get_max_key_length(lines_guild)
            desc = "\n".join(
                self._diff_str_or_blank(value, label, label_space)
                for label, value in lines_guild.items()
            )
            self._add_embed_field(ret, "", desc)

        if not len(lines_rank) == 0:
            label_space = self._get_max_key_length(lines_rank)
            desc = "\n".join(
                self._diff_str_or_blank(value, label, label_space)
                for label, value in lines_rank.items()
            )
            self._add_embed_field(ret, "", desc)
        return ret

    def _parser_historical_member_list(
        self,
    ) -> Sequence[EmbedField]:
        """
        Assumption:
        - player_df is sorted by `datetime` column, ascending
        """
        self._player_df.replace("", "None", inplace=True)
        self._guild_df.replace("", "None", inplace=True)
        lines = []
        prev_value = None
        for uuid in pd.unique(self._player_df["uuid"]):
            player = self._player_df[self._player_df["uuid"] == uuid]
            lines.append(f"**{player.iloc[-1]["username"]}**")
            new_lines = []
            for _, row in player.iterrows():
                if row["guild_name"] == "None":
                    val = "None"
                else:
                    val = f"{row['guild_name']} ({row['guild_rank']})"
                if prev_value == val:
                    continue
                prev_value = val
                formatted_ts = self._get_formatted_timestamp(row)
                line = f"{formatted_ts}: {val}"
                new_lines.append(line)
            if len(new_lines) < 2:
                lines.pop()
                continue
            lines.extend(new_lines)
        desc = "\n".join(lines)
        ret = []
        self._add_embed_field(ret, "Member List", desc)
        return ret

    def _parser_historical_guild_level(
        self,
    ) -> Sequence[EmbedField]:
        self._player_df.replace("", "None", inplace=True)
        self._guild_df.replace("", "None", inplace=True)
        lines = []
        prev_value = None
        for _, row in self._guild_df.iterrows():
            value = row["level"]
            if prev_value == value:
                continue
            prev_value = value
            formatted_ts = self._get_formatted_timestamp(row)
            line = f"{formatted_ts}: {value}"
            lines.append(line)
        desc = "\n".join(lines)
        ret = []
        self._add_embed_field(ret, "Guild Level", desc)
        return ret

    def _parser_historical_territories(
        self,
    ) -> Sequence[EmbedField]:
        """dungeon_completions, quest_completions, raid_completions"""
        return [EmbedField("", value="UNIMPLEMENTED")]
