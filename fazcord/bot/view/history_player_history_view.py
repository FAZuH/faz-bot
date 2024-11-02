from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from loguru import logger
from nextcord import Color, Embed, SelectOption
from nextcord.ui import StringSelect

from fazcord.bot.view._base_view import BaseView
from fazcord.bot.view._custom_embed import CustomEmbed
from fazcord.bot.view._id_select import IdSelect

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazcord.bot.bot import Bot
    from fazutil.db.fazwynn.model.player_info import PlayerInfo


class HistoryPlayerHistoryView(BaseView):

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

        begin_ts = int(self._period_begin.timestamp())
        end_ts = int(self._period_end.timestamp())
        self._base_embed = CustomEmbed(
            self._interaction,
            title=f"Player History ({self._player.latest_username})",
            description=f"`Period : ` <t:{begin_ts}:R> to <t:{end_ts}:R>\n\n",
            color=Color.teal(),
        )

        self._character_select = StringSelect(placeholder="Select character", row=0)
        self._character_select.callback = self.__character_select_callback
        self._id_select = IdSelect(view=self, callback=self.__id_select_callback, row=1)

    async def __character_select_callback(self, interaction: Interaction) -> None:
        # Assumption:
        #   - length of self._character_select.values is always 1
        self._selected = self._character_select.values[0]
        await interaction.send(f"selected_uuid={self._selected}")

    async def __id_select_callback(self, interaction: Interaction) -> None:
        self._selected = self._id_select.get_selected_option()
        await interaction.send(
            f"name={self._selected.name}, value={self._selected.value}"
        )

    async def __add_character_select(self) -> None:
        await self._player.awaitable_attrs.characters
        ch_counter = defaultdict(int)
        for ch in self._player.characters:
            ch_hists = (
                await self.bot.fazwynn_db.character_history.select_between_period(
                    ch.character_uuid, self._period_begin, self._period_end
                )
            )
            if len(ch_hists) == 0:
                continue
            ch_counter[ch.type] += 1
            # select ch_hist with max datetime
            latest_ch_hist = max(ch_hists, key=lambda x: x.datetime)
            total_level = latest_ch_hist.get_total_level()
            nth = ch_counter[ch.type]
            label = f"{ch.type}{nth} (Lv. {total_level})"
            self._character_select.add_option(label=label, value=str(ch.character_uuid))

        if len(self._character_select.options) == 0:
            self._character_select.placeholder = "No character"
            self._character_select.disabled = True

        self._character_select.callback = self.__character_select_callback
        self.add_item(self._character_select)

    @override
    async def run(self) -> None:
        await self.__add_character_select()
        embed = await self._get_embed()
        await self._interaction.send(embed=embed, view=self)

    async def _get_embed(self) -> Embed:
        # db = self._bot.fazwynn_db
        embed = self._base_embed.get_base()

        # player_hist = await db.player_history.select_between_period(self._player.uuid)

        #        player_hist = await db.player_history.select_between_period()
        #
        #        embed = self._base_embed.get_base()
        #        embed.description += "".join(  # type: ignore
        #            [
        #                self._diff_str_or_blank(diff[0], diff[1], label, max_label_length)
        #                for label, diff in d.items()
        #            ]
        #        )
        #            self._player.uuid, self._period_begin, self._period_end
        #        )
        #        p1, p2 = player_hist[0], player_hist[-1]
        #
        #        max_label_length = max(
        #            len(label) for label, data in d.items() if data[1] != data[0]
        #        )
        #        embed.description += "".join(  # type: ignore
        #            [
        #                self._diff_str_or_blank(diff[0], diff[1], label, max_label_length)
        #                for label, diff in d.items()
        #            ]
        #        )

        embed.finalize()
        return embed

    # def _diff_str_or_blank(
    #     self, before: Any, after: Any, label: str, label_space: int
    # ) -> str:
    #     fmt_num = lambda x: (
    #         f"{x:,}"
    #         if isinstance(x, int)
    #         else f"{x:,.2f}" if isinstance(x, (float, Decimal)) else x
    #     )
    #     if before != after:
    #         return f"`{label:{label_space}} : ` {fmt_num(before)} -> {fmt_num(after)}\n"
    #     return ""
