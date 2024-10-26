from decimal import Decimal
from unittest import TestCase

from fazutil.wynn.crafted_roll_probability import CraftedRollProbability
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
        craftedutil = CraftedRollProbability([ing1, ing2, ing3, ing4])

        # Assert
        self.assertEqual(4, craftedutil.min_roll)
        self.assertEqual(12, craftedutil.max_roll)
        self.assertEqual([ing1, ing2, ing3, ing4], craftedutil.ingredients)
        self.assertAlmostEqual(Decimal(0.060), craftedutil.roll_pmfs[4], delta=0.001)
        self.assertAlmostEqual(Decimal(0.245), craftedutil.roll_pmfs[6], delta=0.001)
        self.assertAlmostEqual(Decimal(0.375), craftedutil.roll_pmfs[8], delta=0.001)
        self.assertAlmostEqual(Decimal(0.255), craftedutil.roll_pmfs[10], delta=0.001)
        self.assertAlmostEqual(Decimal(0.065), craftedutil.roll_pmfs[12], delta=0.001)

    def test_negative_boost(self) -> None:
        # Prepare
        ing1 = IngredientField(0, 10, -500)
        craftedutil = CraftedRollProbability([ing1])

        # Assert
        self.assertEqual(-40, float(craftedutil.min_roll))
        self.assertEqual(0, float(craftedutil.max_roll))

    def test_negative_min_value(self) -> None:
        # Prepare
        ing1 = IngredientField(-10, 0, 50)
        craftedutil = CraftedRollProbability([ing1])

        # Assert
        self.assertEqual(-15, float(craftedutil.min_roll))
        self.assertEqual(0, float(craftedutil.max_roll))

    def test_negative_max_value(self) -> None:
        # Prepare
        ing1 = IngredientField(-20, -10, 50)
        craftedutil = CraftedRollProbability([ing1])

        # Assert
        self.assertEqual(-30, float(craftedutil.min_roll))
        self.assertEqual(-15, float(craftedutil.max_roll))

    def test_all_negative(self) -> None:
        # Prepare
        ing1 = IngredientField(-20, -10, -500)
        craftedutil = CraftedRollProbability([ing1])

        # Assert
        self.assertEqual(40, float(craftedutil.min_roll))
        self.assertEqual(80, float(craftedutil.max_roll))

    def test_distributions(self) -> None:
        # Prepare
        ing1 = IngredientField(0, 1)
        ing2 = IngredientField(0, 2)
        ing3 = IngredientField(0, 3)
        ing4 = IngredientField(0, 4)
        ing5 = IngredientField(0, 5)
        craft1 = CraftedRollProbability([ing1])
        craft2 = CraftedRollProbability([ing2])
        craft3 = CraftedRollProbability([ing3])
        craft4 = CraftedRollProbability([ing4])
        craft5 = CraftedRollProbability([ing5])

        # Assert
        def check(craft: CraftedRollProbability, expected: list[float]) -> None:
            for i in range(len(expected)):
                self.assertAlmostEqual(
                    expected[i], float(craft.roll_pmfs[i]), delta=0.001
                )

        check(craft1, [0.5049505, 0.4950495])
        check(craft2, [0.25742574, 0.48514851, 0.25742574])
        check(craft3, [0.16831683, 0.32673267, 0.33663366, 0.16831683])
        check(craft4, [0.12871287, 0.24752475, 0.24752475, 0.24752475, 0.12871287])
        check(
            craft5,
            [0.10891089, 0.18811881, 0.20792079, 0.18811881, 0.20792079, 0.0990099],
        )
