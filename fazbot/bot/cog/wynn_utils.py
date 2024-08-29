from typing import Any

import nextcord
from nextcord import Interaction

from fazbot.bot.cog._cog_base import CogBase
from fazbot.bot.view.convert_emerald_view import ConvertEmeraldView
from fazbot.bot.view.crafted_probability_view import CraftedProbabilityView
from fazbot.bot.view.ingredient_probability_view import IngredientProbabilityView


class WynnUtils(CogBase):

    @nextcord.slash_command(name="crafted_probability")
    async def crafted_probability(
        self,
        interaction: Interaction[Any],
        ingredient1: str = CraftedProbabilityView.INGSTR_DEFAULT,
        ingredient2: str = CraftedProbabilityView.INGSTR_DEFAULT,
        ingredient3: str = CraftedProbabilityView.INGSTR_DEFAULT,
        ingredient4: str = CraftedProbabilityView.INGSTR_DEFAULT,
        ingredient5: str = CraftedProbabilityView.INGSTR_DEFAULT,
        ingredient6: str = CraftedProbabilityView.INGSTR_DEFAULT,
    ) -> None:
        """
        Computes crafted roll probabilities.

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
            [
                ingredient1,
                ingredient2,
                ingredient3,
                ingredient4,
                ingredient5,
                ingredient6,
            ],
        ).run()

    @nextcord.slash_command(name="convert_emerald")
    async def convert_emerald(
        self, interaction: Interaction[Any], emerald_string: str = ""
    ) -> None:
        """
        Converts input emeralds into common emerald units.

        Args:
            emerald_string (str, optional): Examples: "2x 1stx 1le 1eb 1e", "2.5stx 100.5le 100.2eb", "1/3x 1000eb".

        """
        await ConvertEmeraldView(self._bot, interaction, emerald_string).run()

    @nextcord.slash_command(name="ingredient_probability")
    async def ingredient_probability(
        self,
        interaction: Interaction[Any],
        base_chance: str,
        loot_bonus: int = 0,
        loot_quality: int = 0,
    ) -> None:
        """
        Computes boosted ingredient drop probability after loot bonus and loot quality.

        Args:
            base_chance (str): Ingredient base drop chance (Supported format: 1.2%, 1.2/100).
            loot_bonus (int, optional): Loot bonus value. Defaults to 0.
            loot_quality (int, optional): Loot quality value. Defaults to 0.

        """
        await IngredientProbabilityView(
            self._bot, interaction, base_chance, loot_bonus, loot_quality
        ).run()
