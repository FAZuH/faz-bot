from decimal import Decimal
from unittest import TestCase

from fazutil.wynn.crafted_util import CraftedUtil
from fazutil.wynn.ingredient_field import IngredientField


class TestCraftedUtil(TestCase):
    # 1. All positive
    # 2. Negative boost
    # 3. Negative min_value
    # 4. Negative max_value
    # 5. All negative

    def test_12lq(self) -> None:
        # Prepare
        ing1 = IngredientField(1, 2, 50)
        ing2 = IngredientField(1, 2, 50)
        ing3 = IngredientField(1, 2, 50)
        ing4 = IngredientField(1, 2, 50)
        craftedutil = CraftedUtil([ing1, ing2, ing3, ing4])

        # Assert
        self.assertEqual(4, craftedutil.crafted_roll_min)
        self.assertEqual(12, craftedutil.crafted_roll_max)
        self.assertEqual([ing1, ing2, ing3, ing4], craftedutil.ingredients)
        self.assertAlmostEqual(Decimal(0.060), craftedutil.craft_probs[4], delta=0.001)
        self.assertAlmostEqual(Decimal(0.245), craftedutil.craft_probs[6], delta=0.001)
        self.assertAlmostEqual(Decimal(0.375), craftedutil.craft_probs[8], delta=0.001)
        self.assertAlmostEqual(Decimal(0.255), craftedutil.craft_probs[10], delta=0.001)
        self.assertAlmostEqual(Decimal(0.065), craftedutil.craft_probs[12], delta=0.001)

    def test_negative_boost(self) -> None:
        # Prepare
        ing1 = IngredientField(0, 10, -500)
        craftedutil = CraftedUtil([ing1])

        # Assert
        self.assertEqual(-40, float(craftedutil.crafted_roll_min))
        self.assertEqual(0, float(craftedutil.crafted_roll_max))

    def test_negative_min_value(self) -> None:
        # Prepare
        ing1 = IngredientField(-10, 0, 50)
        craftedutil = CraftedUtil([ing1])

        # Assert
        self.assertEqual(-15, float(craftedutil.crafted_roll_min))
        self.assertEqual(0, float(craftedutil.crafted_roll_max))

    def test_negative_max_value(self) -> None:
        # Prepare
        ing1 = IngredientField(-20, -10, 50)
        craftedutil = CraftedUtil([ing1])

        # Assert
        self.assertEqual(-30, float(craftedutil.crafted_roll_min))
        self.assertEqual(-15, float(craftedutil.crafted_roll_max))

    def test_all_negative(self) -> None:
        # Prepare
        ing1 = IngredientField(-20, -10, -500)
        craftedutil = CraftedUtil([ing1])

        # Assert
        self.assertEqual(40, float(craftedutil.crafted_roll_min))
        self.assertEqual(80, float(craftedutil.crafted_roll_max))

    def test_distributions(self) -> None:
        # Prepare
        ing1 = IngredientField(0, 1)
        ing2 = IngredientField(0, 2)
        ing3 = IngredientField(0, 3)
        ing4 = IngredientField(0, 4)
        ing5 = IngredientField(0, 5)
        craft1 = CraftedUtil([ing1])
        craft2 = CraftedUtil([ing2])
        craft3 = CraftedUtil([ing3])
        craft4 = CraftedUtil([ing4])
        craft5 = CraftedUtil([ing5])

        # Assert
        def check(craft: CraftedUtil, expected: list[float]) -> None:
            for i in range(len(expected)):
                self.assertAlmostEqual(
                    expected[i], float(craft.craft_probs[i]), delta=0.001
                )

        check(craft1, [0.5049505, 0.4950495])
        check(craft2, [0.25742574, 0.48514851, 0.25742574])
        check(craft3, [0.16831683, 0.32673267, 0.33663366, 0.16831683])
        check(craft4, [0.12871287, 0.24752475, 0.24752475, 0.24752475, 0.12871287])
        check(
            craft5,
            [0.10891089, 0.18811881, 0.20792079, 0.18811881, 0.20792079, 0.0990099],
        )
