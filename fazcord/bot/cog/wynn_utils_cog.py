import re
from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from typing import Any

import nextcord
from nextcord import Interaction

from fazcord.bot.cog._cog_base import CogBase
from fazcord.bot.errors import BadArgument
from fazcord.bot.view.convert_emerald_view import ConvertEmeraldView
from fazcord.bot.view.crafted_probability_view import CraftedProbabilityView
from fazcord.bot.view.ingredient_probability_view import IngredientProbabilityView
from fazcord.wynn.crafted_util import CraftedUtil
from fazcord.wynn.ingredient_field import IngredientField


class WynnUtilsCog(CogBase):
    INGSTR_DEFAULT = "0,0,0"

    @nextcord.slash_command()
    async def utils(self, intr: Interaction[Any]) -> None: ...

    @utils.subcommand()
    async def crafted_probability(
        self,
        interaction: Interaction[Any],
        ingredient1: str = INGSTR_DEFAULT,
        ingredient2: str = INGSTR_DEFAULT,
        ingredient3: str = INGSTR_DEFAULT,
        ingredient4: str = INGSTR_DEFAULT,
        ingredient5: str = INGSTR_DEFAULT,
        ingredient6: str = INGSTR_DEFAULT,
    ) -> None:
        """Computes crafted roll probabilities.

        Args:
            ingredient1 (str, optional): min,max[,efficiency]
            ingredient2 (str, optional): min,max[,efficiency]
            ingredient3 (str, optional): min,max[,efficiency]
            ingredient4 (str, optional): min,max[,efficiency]
            ingredient5 (str, optional): min,max[,efficiency]
            ingredient6 (str, optional): min,max[,efficiency]
        """
        await CraftedProbabilityView(
            self._bot,
            interaction,
            CraftedUtil(
                self._parse_ings_str(
                    ingredient1,
                    ingredient2,
                    ingredient3,
                    ingredient4,
                    ingredient5,
                    ingredient6,
                )
            ),
        ).run()

    @utils.subcommand()
    async def convert_emerald(
        self, interaction: Interaction[Any], emerald_string: str = ""
    ) -> None:
        """Converts input emeralds into common emerald units.

        Args:
            emerald_string (str, optional): Examples: "2x 1stx 1le 1eb 1e", "2.5stx 100.5le 100.2eb", "1/3x 1000eb".
        """
        await ConvertEmeraldView(self._bot, interaction, emerald_string).run()

    @utils.subcommand()
    async def ingredient_probability(
        self,
        interaction: Interaction[Any],
        base_chance: str,
        loot_bonus: int = 0,
        loot_quality: int = 0,
    ) -> None:
        """Computes boosted ingredient drop probability after loot bonus and loot quality.

        Args:
            base_chance (str): Ingredient base drop chance (Supported format: 1.2%, 1.2/100).
            loot_bonus (int, optional): Loot bonus value. Defaults to 0.
            loot_quality (int, optional): Loot quality value. Defaults to 0.
        """
        parsed_base_chande = self._parse_base_chance(base_chance)
        await IngredientProbabilityView(
            self._bot, interaction, parsed_base_chande, loot_bonus, loot_quality
        ).run()

    def _parse_ings_str(self, *ing_strs: str) -> Sequence[IngredientField]:
        res: list[IngredientField] = []
        for ing_str in ing_strs:
            if ing_str == self.INGSTR_DEFAULT:
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
        try:
            ret = Decimal(base_chance)
        except InvalidOperation as exc:
            raise BadArgument(f"Failed parsing base chance: {exc}") from exc
        return ret
