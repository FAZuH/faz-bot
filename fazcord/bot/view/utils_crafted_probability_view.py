from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, override

from nextcord import ButtonStyle, Embed, Interaction
from nextcord.ui import Button, button

from fazcord.bot.view._base_view import BaseView
from fazcord.bot.view._custom_embed import CustomEmbed
from fazutil.wynn.crafted_roll_probability import CraftedRollProbability
from fazutil.cache_util import CacheUtil

if TYPE_CHECKING:
    from fazcord.bot.bot import Bot


class UtilsCraftedProbabilityView(BaseView):
    _THUMBNAIL_URL = "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Crafting_Table_JE4_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20191229083528"

    def __init__(
        self, bot: Bot, interaction: Interaction[Any], craftutil: CraftedRollProbability
    ) -> None:
        super().__init__(bot, interaction)
        self._craftutil = craftutil
        self._cache = CacheUtil()
        self._cache.register(
            self,
            [
                self._get_craftprobs_embed,
                self._get_atleast_embed,
                self._get_atmost_embed,
            ],
        )

    @override
    async def run(self) -> None:
        embed = self._get_craftprobs_embed()
        await self._interaction.send(
            embed=embed,
            view=self,
        )

    def _get_base_embed(self) -> CustomEmbed:
        embed = CustomEmbed(
            self._interaction,
            title="Crafteds Probabilites Calculator",
            color=8894804,
            thumbnail_url=self._THUMBNAIL_URL,
        )
        # Embed descriptions
        embed_desc = ["Ingredients:"]
        for i, ing in enumerate(self._craftutil.ingredients, start=1):
            ing_info = (
                f"- `[{i}]`: {ing.min_value} to {ing.max_value}"  # -[nth]: min to max
            )
            ing_info += (
                f", {ing.boost}% boost" if ing.boost != 0 else ""
            )  # Add boost to info if exist
            embed_desc.append(ing_info)
        embed.description = "\n".join(embed_desc)
        return embed

    def _get_craftprobs_embed(self) -> Embed:
        embed = self._get_base_embed()
        embed_fields_values = ""
        is_first_embed = True
        for value, probability in self._craftutil.roll_pmfs.items():
            one_in_n = round(Decimal(1 / probability), 2)
            result = f"Roll: **{value}**, Chance: **{probability * 100:.2f}%** (1 in {one_in_n:,})"
            if len(embed_fields_values + f"{result}\n") > 1024:
                embed.add_field(
                    name="Probabilities" if is_first_embed else "",
                    value=embed_fields_values,
                    inline=False,
                )
                embed_fields_values = ""
                is_first_embed = False
            embed_fields_values += f"{result}\n"
        embed.add_field(
            name="Probabilities" if is_first_embed else "",
            value=embed_fields_values,
            inline=False,
        )
        embed.finalize()
        return embed

    def _get_atleast_embed(self) -> Embed:
        embed = self._get_base_embed()
        field_value = ""
        cmlr_prob = 1
        is_first_embed = True
        for val, prob in self._craftutil.roll_pmfs.items():
            one_in_n = round(Decimal(1 / cmlr_prob), 2)
            line = f"Roll: **atleast {val}**, Chance: **{cmlr_prob * 100:.2f}%** (1 in {one_in_n:,})"
            if len(field_value + f"{line}\n") > 1024:
                embed.add_field(
                    name="Probabilities" if is_first_embed else "",
                    value=field_value,
                    inline=False,
                )
                field_value = ""
                is_first_embed = False
            cmlr_prob -= prob
            field_value += f"{line}\n"
        embed.add_field(
            name="Probabilities" if is_first_embed else "",
            value=field_value,
            inline=False,
        )
        embed.finalize()
        return embed

    def _get_atmost_embed(self) -> Embed:
        embed = self._get_base_embed()
        field_value = ""
        cml_prob = 0
        is_first_embed = True
        for val, prob in self._craftutil.roll_pmfs.items():
            cml_prob += prob
            one_in_n = round(Decimal(1 / cml_prob), 2)
            line = f"Roll: **atmost {val}**, Chance: **{cml_prob * 100:.2f}%** (1 in {one_in_n:,})"
            if len(field_value + f"{line}\n") > 1024:
                embed.add_field(
                    name="Probabilities" if is_first_embed else "",
                    value=field_value,
                    inline=False,
                )
                field_value = ""
                is_first_embed = False
            field_value += f"{line}\n"
        embed.add_field(
            name="Probabilities" if is_first_embed else "",
            value=field_value,
            inline=False,
        )
        embed.finalize()
        return embed

    @button(label="Distribution", style=ButtonStyle.green, emoji="🎲", disabled=True)
    async def button_distribution(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await self._do_button(button, interaction, self._get_craftprobs_embed)

    @button(label="Atleast", style=ButtonStyle.green, emoji="📉")
    async def button_atleast(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await self._do_button(button, interaction, self._get_atleast_embed)

    @button(label="Atmost", style=ButtonStyle.green, emoji="📈")
    async def button_atmost(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await self._do_button(button, interaction, self._get_atmost_embed)

    async def _do_button(
        self,
        button: Button[Any],
        interaction: Interaction[Any],
        embed_strategy: Callable[[], Embed] | None = None,
    ) -> None:
        await interaction.response.defer()
        self._click_button(button)
        embed = embed_strategy() if embed_strategy else None
        await interaction.edit_original_message(embed=embed, view=self)
