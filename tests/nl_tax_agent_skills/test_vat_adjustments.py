"""Exact adjustment arithmetic invariants, independent of taxpayer eligibility."""

from decimal import Decimal
import importlib.util
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "vat_adjustment_arithmetic", REPO / "tools/nl_tax_agent_skills/vat_adjustments/adjustment_arithmetic.py")
MATH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATH)
D = Decimal


class VATAdjustmentArithmeticTests(unittest.TestCase):
    def test_car_window_uses_entrepreneur_first_use_and_year_boundary(self):
        self.assertEqual(MATH.car_fraction(2021, 2025, True), D("0.027"))
        self.assertEqual(MATH.car_fraction(2021, 2026, True), D("0.015"))
        self.assertEqual(MATH.car_fraction(2025, 2026, False), D("0.015"))

    def test_car_source_cap_uses_actual_deductions_without_second_split(self):
        cap = MATH.owned_car_cap("735", "3150", 2025, 2025, 2026)
        self.assertEqual(cap, D("1365"))
        result = MATH.car_forfait("75000", MATH.car_fraction(2025, 2026, True), 1, 1, "1", cap)
        self.assertEqual(result, {"uncapped": D("2025.000"), "adjustment": D("1365")})
        partial = MATH.car_forfait("45000", D("0.027"), 4, 12, "0.6", "2000")
        self.assertEqual(partial["adjustment"], D("243"))

    def test_time_apportioned_car_forfait_stays_exact_on_whole_euros(self):
        # 10000 x 0.027 x 4/12 = 90 exactly; a pre-divided share gave 89.999...
        self.assertEqual(MATH.car_forfait("10000", D("0.027"), 4, 12, "1", "100000")["adjustment"], D("90"))
        self.assertEqual(MATH.car_forfait("11000", D("0.027"), 4, 12, "1", "100000")["adjustment"], D("99"))
        self.assertEqual(MATH.car_forfait("10000", D("0.027"), 4, 12, "0.6", "100000")["adjustment"], D("54"))
        for available, year in ((13, 12), (0, 12), (D(4) / D(12), 1), ("4", 12)):
            with self.assertRaises(ValueError):
                MATH.car_forfait("10000", D("0.027"), available, year, "1", "100000")

    def test_no_purchase_component_after_window_or_without_deduction(self):
        self.assertEqual(MATH.owned_car_cap("840", "0", 2025, 2025, 2026), D("840"))
        self.assertEqual(MATH.owned_car_cap("735", "3150", 2020, 2020, 2026), D("735"))

    def test_car_caps_reject_unestablished_first_year_and_date_disagreement(self):
        for args in (("100", "2100", 2026, 2026, 2026), ("100", "2100", 2024, 2025, 2026)):
            with self.assertRaises(ValueError):
                MATH.owned_car_cap(*args)

    def test_actual_use_includes_confirmed_private_distance_in_component_share(self):
        self.assertEqual(MATH.actual_private_use("1500", "5000", "30000"), D("250"))
        for private, total in (("100", "0"), ("101", "100")):
            with self.assertRaises(ValueError):
                MATH.actual_private_use("1500", private, total)

    def test_deduction_fractions_have_separate_denominators_and_never_exceed_vat(self):
        self.assertEqual(MATH.accepted_deduction("2100", "0.8", "0.75"), D("1260.000"))
        self.assertEqual(MATH.accepted_deduction("2100", "1", "1"), D("2100"))
        with self.assertRaises(ValueError):
            MATH.accepted_deduction("2100", "1.1", "1")

    def test_year_end_delta_uses_prior_net_deduction_including_first_use_change(self):
        self.assertEqual(MATH.entitlement_delta("2100", "0.75", "1050"), D("525.00"))
        self.assertEqual(MATH.entitlement_delta("2100", "0.50", "1400"), D("-350.00"))
        with self.assertRaises(ValueError):
            MATH.entitlement_delta("2100", "0.75", "2101")

    def test_turnover_pro_rata_rounds_percentage_up_before_deduction(self):
        ratio = MATH.turnover_pro_rata("694", "1000")
        self.assertEqual(ratio, D("0.70"))
        self.assertEqual(MATH.accepted_deduction("1000", "1", ratio), D("700.00"))
        self.assertEqual(MATH.turnover_pro_rata("700", "1000"), D("0.70"))
        self.assertEqual(MATH.turnover_pro_rata("2", "3"), D("0.67"))
        self.assertEqual(MATH.turnover_pro_rata("70.000000000000000000000000000001", "100"), D("0.71"))
        self.assertEqual(MATH.turnover_pro_rata("0", "1000"), D(0))
        self.assertEqual(MATH.turnover_pro_rata("1000", "1000"), D(1))
        for numerator, denominator in (("1", "0"), ("1001", "1000")):
            with self.assertRaises(ValueError):
                MATH.turnover_pro_rata(numerator, denominator)
        # Confirmed actual-use keys retain their exact percentage instead.
        self.assertEqual(MATH.accepted_deduction("1000", "1", "0.694"), D("694.000"))

    def test_later_revision_tolerance_is_relative_not_ten_percentage_points(self):
        self.assertEqual(MATH.later_revision("84000", "0.65", "0.715", 10, 3), D(0))
        self.assertEqual(MATH.later_revision("84000", "0.65", "0.716", 10, 3), D("554.400"))
        self.assertEqual(MATH.later_revision("84000", "0.65", "0.85", 10, 3), D("1680.00"))
        self.assertEqual(MATH.later_revision("840", "0.55", "0.75", 5, 2), D("33.60"))
        self.assertEqual(MATH.later_revision("147000", "1", "0.30", 5, 2), D("-20580.00"))

    def test_revision_does_not_use_later_year_recipe_for_first_use_or_expired_window(self):
        for years, offset in ((5, 0), (5, 5), (10, 10), (4, 1)):
            with self.assertRaises(ValueError):
                MATH.later_revision("840", "0.55", "0.75", years, offset)
        self.assertEqual(MATH.later_revision("840", "0", "0.75", 5, 1), D("126.00"))

    def test_disposal_uses_remaining_bookyear_fraction_not_full_unspent_year(self):
        self.assertEqual(MATH.disposal_revision("105000", "1", "0", 51, 10, year_units=12), D("-44625.00"))
        self.assertEqual(MATH.disposal_revision("840", "0.55", "1", 2, 5), D("151.20"))

    def test_delivery_year_splits_into_elapsed_ordinary_part_and_one_time_remainder(self):
        # Property first used 2020, exempt sale on 1 October 2025: 9 of 12
        # months of the sale year are ordinary revision, 51 months are the
        # one-time remainder.
        remainder = MATH.disposal_revision("105000", "1", "0", 51, 10, year_units=12)
        unchanged_use = MATH.later_revision("105000", "1", "1", 10, 5, elapsed_units=9, year_units=12)
        self.assertEqual(unchanged_use + remainder, D("-44625"))
        half_exempt = MATH.later_revision("105000", "1", "0.5", 10, 5, elapsed_units=9, year_units=12)
        self.assertEqual(half_exempt, D("-3937.5"))
        self.assertEqual(half_exempt + remainder, D("-48562.5"))
        # A full-year annual share would revise the post-delivery 0.25 twice.
        full_year = MATH.later_revision("105000", "1", "0.5", 10, 5)
        self.assertEqual(full_year - half_exempt, D("-1312.5"))
        for elapsed, year in ((0, 12), (13, 12), ("9", 12), (9, 0)):
            with self.assertRaises(ValueError):
                MATH.later_revision("105000", "1", "0.5", 10, 5, elapsed_units=elapsed, year_units=year)
        for remaining, year in ((0, 12), (121, 12), ("51", 12)):
            with self.assertRaises(ValueError):
                MATH.disposal_revision("105000", "1", "0", remaining, 10, year_units=year)

    def test_month_splits_stay_exact_because_division_happens_last(self):
        # 2/12 and 10/12 are not terminating decimals; dividing first would
        # return -375.0000...01 and -8699.999...9.
        self.assertEqual(MATH.later_revision("45000", "1", "0.5", 10, 5, elapsed_units=2, year_units=12), D("-375"))
        self.assertEqual(MATH.disposal_revision("18000", "1", "0", 58, 10, year_units=12), D("-8700"))

    def test_bua_boundary_uses_gross_cost_even_with_large_contribution(self):
        self.assertEqual(MATH.bua_repayment("227", "47.67", "0"), D(0))
        self.assertEqual(MATH.bua_repayment("300", "63", "21"), D("42"))
        self.assertEqual(MATH.bua_repayment("300", "0", "21"), D(0))
        self.assertEqual(MATH.bua_repayment("300", "20", "21"), D(0))

    def test_individual_does_not_net_loss_and_splits_tax_from_inclusive_margin(self):
        result = MATH.individual_margin([("321", "200"), ("50", "100")], "0.21")
        self.assertEqual(result["vat"], D("21"))
        self.assertEqual(result["net_taxable_margin"], D("100"))
        self.assertEqual(result["gross_margin"], D("121"))

    def test_global_uses_period_purchases_and_unused_same_rate_loss(self):
        result = MATH.global_margin("40000", "25000", "10000", "0.21")
        self.assertEqual(result["gross_margin"], D("5000"))
        self.assertEqual(result["vat"], D("5000") * D("0.21") / D("1.21"))
        loss = MATH.global_margin("30000", "40000", "0", "0.21")
        self.assertEqual(loss["vat"], D(0))
        self.assertEqual(loss["negative_margin"], D("-10000"))

    def test_no_silent_zeros_locale_float_nan_or_boolean_amounts(self):
        for value in (None, True, "1,000.00", "NaN", "Infinity", "", 0.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    MATH.decimal(value)

    def test_component_labels_detect_duplicate_acquisition_or_correction(self):
        self.assertTrue(MATH.verify_unique_components(["asset_A.purchase_component", "asset_A.running_costs"]))
        with self.assertRaises(ValueError):
            MATH.verify_unique_components(["asset_A.purchase_component", "asset_A.purchase_component"])


if __name__ == "__main__":
    unittest.main()
