from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, override

from nextcord import ButtonStyle, Embed, Interaction
from nextcord.ui import Button, button

from fazbot.bot.errors import BadArgument
from fazbot.bot.view._base_view import BaseView
from fazbot.bot.view._custom_embed import CustomEmbed
from fazbot.wynn.crafted_util import CraftedUtil
from fazbot.wynn.ingredient_field import IngredientField
from fazutil.util.cache_util import CacheUtil

if TYPE_CHECKING:
    from fazbot.bot.bot import Bot


class CraftedProbabilityView(BaseView):

    _THUMBNAIL_URL = "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Crafting_Table_JE4_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20191229083528"
    INGSTR_DEFAULT = "0,0,0"

    def __init__(
        self, bot: Bot, interaction: Interaction[Any], ing_strs: list[str]
    ) -> None:
        super().__init__(bot, interaction)
        self._ing_strs = ing_strs

        self._cache = CacheUtil()
        self._cache.register(
            self,
            [
                self._get_craftprobs_embed,
                self._get_atleast_embed,
                self._get_atmost_embed,
            ],
        )
        self._craftutil = CraftedUtil(self._parse_ings_str(ing_strs))

    @override
    async def run(self) -> None:
        embed = self._get_craftprobs_embed(self._craftutil)
        await self._interaction.send(
            embed=embed,
            view=self,
        )

    def _parse_ings_str(self, ing_strs: list[str]) -> list[IngredientField]:
        res: list[IngredientField] = []
        for ing_str in ing_strs:
            if ing_str == CraftedProbabilityView.INGSTR_DEFAULT:
                continue
            ing_str = ing_str.strip()
            ing_vals = ing_str.split(",")
            if len(ing_vals) not in {2, 3}:
                raise BadArgument(
                    f"Invalid format on {ing_str}. Value must be 'min,max[,efficiency]'"
                )
            try:
                parsed_ing_vals: list[int] = [int(v) for v in ing_vals]
            except ValueError as exc:
                raise BadArgument(
                    f"Failed parsing ingredient value on {ing_str}"
                ) from exc
            try:
                res.append(IngredientField(*parsed_ing_vals))
            except ValueError as e:
                raise BadArgument(e.args[0]) from e
        return res

    def _get_base_embed(self, craftutil: CraftedUtil) -> CustomEmbed:
        embed = CustomEmbed(
            self._interaction,
            title="Crafteds Probabilites Calculator",
            color=8894804,
            thumbnail_url=self._THUMBNAIL_URL,
        )
        # Embed descriptions
        embed_desc = ["Ingredients:"]
        for i, ing in enumerate(craftutil.ingredients, start=1):
            ing_info = (
                f"- `[{i}]`: {ing.min_value} to {ing.max_value}"  # -[nth]: min to max
            )
            ing_info += (
                f", {ing.boost}% boost" if ing.boost != 0 else ""
            )  # Add boost to info if exist
            embed_desc.append(ing_info)
        embed.description = "\n".join(embed_desc)
        return embed

    def _get_craftprobs_embed(self, craftutil: CraftedUtil) -> Embed:
        embed = self._get_base_embed(craftutil)
        embed_fields_values = ""
        is_first_embed = True
        for value, probability in craftutil.craft_probs.items():
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

    def _get_atleast_embed(self, craftutil: CraftedUtil) -> Embed:
        embed = self._get_base_embed(craftutil)
        field_value = ""
        cmlr_prob = 1
        is_first_embed = True
        for val, prob in craftutil.craft_probs.items():
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

    def _get_atmost_embed(self, craftutil: CraftedUtil) -> Embed:
        embed = self._get_base_embed(craftutil)
        field_value = ""
        cml_prob = 0
        is_first_embed = True
        for val, prob in craftutil.craft_probs.items():
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
    async def button_atmost_callback(
        self, button: Button[Any], interaction: Interaction[Any]
    ) -> None:
        await self._do_button(button, interaction, self._get_atmost_embed)

    async def _do_button(
        self,
        button: Button[Any],
        interaction: Interaction[Any],
        embed_strategy: Callable[[CraftedUtil], Embed] | None = None,
    ) -> None:
        await interaction.response.defer()
        self._click_button(button)
        embed = embed_strategy(self._craftutil) if embed_strategy else None
        await interaction.edit_original_message(embed=embed, view=self)

    def _click_button(self, button: Button[Any]) -> None:
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = False
        button.disabled = True
