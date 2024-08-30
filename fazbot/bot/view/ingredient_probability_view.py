from __future__ import annotations

import re
from decimal import Decimal
from typing import TYPE_CHECKING, Any, override

from nextcord import Embed, Interaction

from fazbot.bot.errors import BadArgument
from fazbot.bot.view._base_view import BaseView
from fazbot.bot.view._custom_embed import CustomEmbed
from fazbot.wynn.ingredient_util import IngredientUtil

if TYPE_CHECKING:
    from fazbot.bot.bot import Bot


class IngredientProbabilityView(BaseView):

    _THUMBNAIL_URL = "https://www.wynndata.tk/assets/images/items/v4//ingredients/heads/50d8ba53402f4cb0455067d068973b3d.png"

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        base_chance: str,
        loot_bonus: int,
        loot_quality: int,
    ) -> None:
        super().__init__(bot, interaction)
        self._base_chance = self._parse_base_chance(base_chance)
        self._loot_bonus = loot_bonus
        self._loot_quality = loot_quality

        self._ing_util = IngredientUtil(
            self._base_chance, self._loot_quality, self._loot_bonus
        )

    @override
    async def run(self) -> None:
        embed = self._get_embed(self._ing_util)
        await self._interaction.send(embed=embed)

    def _get_embed(self, ing_util: IngredientUtil) -> Embed:
        one_in_n = 1 / ing_util.boosted_probability
        embed = CustomEmbed(
            self._interaction,
            title="Ingredient Chance Calculator",
            color=472931,
            thumbnail_url=self._THUMBNAIL_URL,
        )
        embed.description = (
            f"` Drop Chance  :` **{ing_util.base_probability:.2%}**\n"
            f"` Loot Bonus   :` **{ing_util.loot_bonus}%**\n"
            f"` Loot Quality :` **{ing_util.loot_quality}%**\n"
            f"` Loot Boost   :` **{ing_util.loot_boost}%**"
        )
        embed.add_field(
            name="Boosted Drop Chance",
            value=f"**{ing_util.boosted_probability:.2%}** OR **1 in {one_in_n:.2f}** mobs",
        )
        embed.finalize()
        return embed

    def _parse_base_chance(self, base_chance: str) -> Decimal:
        if base_chance.endswith("%"):
            return Decimal(base_chance[:-1]) / 100
        if "/" in base_chance:
            match = re.match(r"^(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)$", base_chance)
            if match:
                numerator = float(match.group(1))
                denominator = float(match.group(2))
                return Decimal(numerator) / Decimal(denominator)
            raise BadArgument("Invalid format: .")
        return Decimal(base_chance)
