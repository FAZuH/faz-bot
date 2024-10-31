from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from fazutil.wynn.ingredient_field import IngredientField


class CraftedRollProbability:
    def __init__(self, ingredients: Sequence[IngredientField]):
        self._ingredients = ingredients

        self._ing_prob_dists = []
        self._min_roll = np.int32(0)
        self._max_roll = np.int32(0)
        self._craft_probs = {}

        self._calculate_ingredient_probabilities()
        self._calculate_roll_probabilities()

    @property
    def min_roll(self) -> np.int32:
        assert isinstance(self._min_roll, np.number)
        return self._min_roll

    @property
    def max_roll(self) -> np.int32:
        assert isinstance(self._max_roll, np.number)
        return self._max_roll

    @property
    def roll_pmfs(self) -> dict[int, Decimal]:
        """Probability Mass Function of the crafted rolls"""
        assert isinstance(self._craft_probs, dict)
        return self._craft_probs

    @property
    def ingredients(self) -> Sequence[IngredientField]:
        return self._ingredients

    def _calculate_ingredient_probabilities(self):
        """Gets ingredient_rolls_list and ingredient_probDist_list from command arguments"""
        for ing in self._ingredients:
            ing_stat_eff = (ing.boost + 100) * 0.01

            # Calculate ingredient probability distribution
            ing_base_values = np.linspace(ing.min_value, ing.max_value, 101)
            ing_rolls_boosted = np.floor(
                np.round(ing_base_values) * ing_stat_eff
            ).astype(int)
            offset = -np.min(ing_rolls_boosted)  # Offset to ensure no negative indices
            ing_rolls_occurrences = np.bincount(ing_rolls_boosted + offset)
            ing_prob_dist = ing_rolls_occurrences / 101

            # Assign values into class attributes
            self._ing_prob_dists.append(ing_prob_dist)
            self._min_roll += np.min(ing_rolls_boosted)
            self._max_roll += np.max(ing_rolls_boosted)

    def _calculate_roll_probabilities(self):
        # Calculate crafted roll probabilities
        convolution = np.array([1])
        for prob_dist in self._ing_prob_dists:
            convolution = np.convolve(convolution, prob_dist)

        # Build craft_pmfs dictionary
        crafted_rolls = np.linspace(self.min_roll, self.max_roll, len(convolution))
        for roll, crafted_roll_chance in zip(crafted_rolls, convolution):
            if crafted_roll_chance == 0:
                continue
            self.roll_pmfs[int(roll)] = Decimal(crafted_roll_chance)
