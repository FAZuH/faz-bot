from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, override

from nextcord import ButtonStyle, Color, Embed
from nextcord.ui import Button, button

from fazcord.bot.view._base_view import BaseView
from fazcord.bot.view._custom_embed import CustomEmbed
from fazutil.db.fazdb.model.character_history import CharacterHistory

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazcord.bot.bot import Bot
    from fazutil.db.fazdb.model.player_info import PlayerInfo


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

    @override
    async def run(self) -> None:
        self._embed = await self._get_embed()
        await self._interaction.send(embed=self._embed, view=self)

    @button(style=ButtonStyle.blurple, label="Total", disabled=True)
    async def default_button(self, button: Button[Any], intr: Interaction[Any]) -> None:
        embed = self._embed
        self._click_button(button)
        # HACK: Using intr returns error. Use self._interaction instead.
        await self._interaction.edit_original_message(embed=embed, view=self)

    async def _get_embed(self) -> Embed:
        db = self._bot.fazdb_db
        embed = self._base_embed.get_base()

        player_hist = await db.player_history.select_between_period(
            self._player.uuid, self._period_begin, self._period_end
        )
        p1, p2 = player_hist[0], player_hist[-1]

        d: dict[str, list[Any]] = {
            "Username": [p1.username, p2.username],
            "Rank": [p1.support_rank, p2.support_rank],
            "Playtime": [p1.playtime, p2.playtime],
            "Guild Name": [p1.guild_name, p2.guild_name],
            "Guild Rank": [p1.guild_rank, p2.guild_rank],
            "Level": [0, 0],
            "Xp": [0, 0],
            "Wars": [0, 0],
            "Mobs Killed": [0, 0],
            "Chests Found": [0, 0],
            "Logins": [0, 0],
            "Deaths": [0, 0],
            "Discoveries": [0, 0],
            "Alchemism": [Decimal(0), Decimal(0)],
            "Armouring": [Decimal(0), Decimal(0)],
            "Cooking": [Decimal(0), Decimal(0)],
            "Jeweling": [Decimal(0), Decimal(0)],
            "Scribing": [Decimal(0), Decimal(0)],
            "Tailoring": [Decimal(0), Decimal(0)],
            "Weaponsmithing": [Decimal(0), Decimal(0)],
            "Woodworking": [Decimal(0), Decimal(0)],
            "Mining": [Decimal(0), Decimal(0)],
            "Woodcutting": [Decimal(0), Decimal(0)],
            "Farming": [Decimal(0), Decimal(0)],
            "Fishing": [Decimal(0), Decimal(0)],
            "Dungeons": [0, 0],
            "Quests": [0, 0],
            "Raids": [0, 0],
        }
        chars = await db.character_info.select_from_player(self._player.uuid)
        charcount: dict[str, int] = defaultdict(int)
        for char in chars:
            res = await db.character_history.select_between_period(
                char.character_uuid, self._period_begin, self._period_end
            )
            reslen = len(res)
            if reslen < 2:
                continue
            else:
                c1, c2 = res[0], res[-1]
            type = char.type
            charcount[type] += 1
            d["Level"][0] += c1.level
            d["Level"][1] += c2.level
            d["Xp"][0] += c1.xp
            d["Xp"][1] += c2.xp
            d["Wars"][0] += c1.wars
            d["Wars"][1] += c2.wars
            d["Mobs Killed"][0] += c1.mobs_killed
            d["Mobs Killed"][1] += c2.mobs_killed
            d["Chests Found"][0] += c1.chests_found
            d["Chests Found"][1] += c2.chests_found
            d["Logins"][0] += c1.logins
            d["Logins"][1] += c2.logins
            d["Deaths"][0] += c1.deaths
            d["Deaths"][1] += c2.deaths
            d["Discoveries"][0] += c1.discoveries
            d["Discoveries"][1] += c2.discoveries
            d["Alchemism"][0] += c1.alchemism
            d["Alchemism"][1] += c2.alchemism
            d["Armouring"][0] += c1.armouring
            d["Armouring"][1] += c2.armouring
            d["Cooking"][0] += c1.cooking
            d["Cooking"][1] += c2.cooking
            d["Jeweling"][0] += c1.jeweling
            d["Jeweling"][1] += c2.jeweling
            d["Scribing"][0] += c1.scribing
            d["Scribing"][1] += c2.scribing
            d["Tailoring"][0] += c1.tailoring
            d["Tailoring"][1] += c2.tailoring
            d["Weaponsmithing"][0] += c1.weaponsmithing
            d["Weaponsmithing"][1] += c2.weaponsmithing
            d["Woodworking"][0] += c1.woodworking
            d["Woodworking"][1] += c2.woodworking
            d["Mining"][0] += c1.mining
            d["Mining"][1] += c2.mining
            d["Woodcutting"][0] += c1.woodcutting
            d["Woodcutting"][1] += c2.woodcutting
            d["Farming"][0] += c1.farming
            d["Farming"][1] += c2.farming
            d["Fishing"][0] += c1.fishing
            d["Fishing"][1] += c2.fishing
            d["Dungeons"][0] += c1.dungeon_completions
            d["Dungeons"][1] += c2.dungeon_completions
            d["Quests"][0] += c1.quest_completions
            d["Quests"][1] += c2.quest_completions
            d["Raids"][0] += c1.raid_completions
            d["Raids"][1] += c2.raid_completions
            self._add_character_difference_to_view(
                c1, c2, f"{char.type}{charcount[type]}"
            )

        max_label_length = max(
            len(label) for label, data in d.items() if data[1] != data[0]
        )
        embed.description += "".join(  # type: ignore
            [
                self._diff_str_or_blank(diff[0], diff[1], label, max_label_length)
                for label, diff in d.items()
            ]
        )

        embed.finalize()
        return embed

    def _diff_str_or_blank(
        self, before: Any, after: Any, label: str, label_space: int
    ) -> str:
        if before != after:
            formatted_label = f"`{label:{label_space}}:`"
            return f"{formatted_label} {before} -> {after}\n"
        return ""

    def _add_character_difference_to_view(
        self,
        character_before: CharacterHistory,
        character_after: CharacterHistory,
        label: str,
    ) -> None:
        c1 = character_before
        c2 = character_after
        d = {
            "Level": [c1.level, c2.level],
            "Xp": [c1.xp, c2.xp],
            "Wars": [c1.wars, c2.wars],
            "Mobs Killed": [c1.mobs_killed, c2.mobs_killed],
            "Playtime": [c1.playtime, c2.playtime],
            "Chests Found": [c1.chests_found, c2.chests_found],
            "Logins": [c1.logins, c2.logins],
            "Deaths": [c1.deaths, c2.deaths],
            "Discoveries": [c1.discoveries, c2.discoveries],
            "Alchemism": [c1.alchemism, c2.alchemism],
            "Armouring": [c1.armouring, c2.armouring],
            "Cooking": [c1.cooking, c2.cooking],
            "Jeweling": [c1.jeweling, c2.jeweling],
            "Scribing": [c1.scribing, c2.scribing],
            "Tailoring": [c1.tailoring, c2.tailoring],
            "Weaponsmithing": [c1.weaponsmithing, c2.weaponsmithing],
            "Woodworking": [c1.woodworking, c2.woodworking],
            "Mining": [c1.mining, c2.mining],
            "Woodcutting": [c1.woodcutting, c2.woodcutting],
            "Farming": [c1.farming, c2.farming],
            "Fishing": [c1.fishing, c2.fishing],
            "Dungeons": [c1.dungeon_completions, c2.dungeon_completions],
            "Quests": [c1.quest_completions, c2.quest_completions],
            "Raids": [c1.raid_completions, c2.raid_completions],
        }
        max_label_length = max(
            len(label) for label, data in d.items() if data[1] != data[0]
        )

        embed = self._base_embed.get_base()
        embed.description += "".join(  # type: ignore
            [
                self._diff_str_or_blank(diff[0], diff[1], label, max_label_length)
                for label, diff in d.items()
            ]
        )

        class _CharacterButton(Button):
            @override
            async def callback(self_, interaction: Interaction) -> None:
                await interaction.response.defer()
                self._click_button(self_)
                await interaction.edit_original_message(embed=embed, view=self)

        button = _CharacterButton(style=ButtonStyle.green, label=label.title())
        button._view = self  # type: ignore

        self.add_item(button)
