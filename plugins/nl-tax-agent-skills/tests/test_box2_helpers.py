#!/usr/bin/env python3
"""Focused tests for deterministic Box 2 helper scripts."""

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Box2HelperTests(unittest.TestCase):
    def test_2025_bracket_calculation_splits_lower_and_upper_income(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_2025",
        )

        result = module.calculate_box2_tax(
            tax_year=2025,
            regular_benefits=100_000,
        )

        self.assertEqual(result["taxable_income"], 100_000.0)
        self.assertEqual(result["bracket_split"]["lower_bracket_income"], 67_804.0)
        self.assertEqual(result["bracket_split"]["upper_bracket_income"], 32_196.0)
        self.assertEqual(result["bracket_split"]["lower_bracket_tax"], 16_611.0)
        self.assertEqual(result["bracket_split"]["upper_bracket_tax"], 9_980.0)
        self.assertEqual(result["gross_tax"], 26_591.0)

    def test_dividend_only_2025_applies_withholding_credit(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_dividend",
        )

        result = module.calculate_box2_tax(
            tax_year=2025,
            regular_benefits=10_000,
            dividend_withholding_tax=1_500,
        )

        self.assertEqual(result["taxable_income"], 10_000.0)
        self.assertEqual(result["gross_tax"], 2_450.0)
        self.assertEqual(result["dividend_withholding_credit"], 1_500.0)
        self.assertEqual(result["net_payable_or_refund_indicative"], 950.0)

    def test_2026_bracket_split_uses_provisional_threshold(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_2026",
        )

        result = module.calculate_box2_tax(
            tax_year=2026,
            regular_benefits=70_000,
        )

        self.assertEqual(result["bracket_split"]["threshold"], 68_843.0)
        self.assertEqual(result["bracket_split"]["lower_bracket_income"], 68_843.0)
        self.assertEqual(result["bracket_split"]["upper_bracket_income"], 1_157.0)
        self.assertEqual(result["bracket_split"]["lower_bracket_tax"], 16_866.0)
        self.assertEqual(result["bracket_split"]["upper_bracket_tax"], 358.0)
        self.assertEqual(result["gross_tax"], 17_224.0)

    def test_share_sale_disposal_benefit_uses_net_transfer_price_without_double_deducting_costs(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_disposal",
        )

        result = module.calculate_box2_tax(
            tax_year=2025,
            disposal_price=120_000,
            acquisition_price=50_000,
            disposal_costs=5_000,
        )

        self.assertEqual(result["components"]["net_disposal_price"], 120_000.0)
        self.assertEqual(result["components"]["disposal_benefit"], 70_000.0)
        self.assertEqual(result["taxable_income"], 70_000.0)
        self.assertEqual(result["gross_tax"], 17_291.0)
        self.assertTrue(any("net transfer price" in warning for warning in result["warnings"]))

    def test_gross_disposal_price_derives_net_transfer_price_once(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_gross_disposal",
        )

        result = module.calculate_box2_tax(
            tax_year=2025,
            gross_disposal_price=120_000,
            acquisition_price=50_000,
            disposal_costs=5_000,
        )

        self.assertEqual(result["components"]["gross_disposal_price"], 120_000.0)
        self.assertEqual(result["components"]["net_disposal_price"], 115_000.0)
        self.assertEqual(result["components"]["disposal_benefit"], 65_000.0)
        self.assertEqual(result["taxable_income"], 65_000.0)
        self.assertEqual(result["gross_tax"], 15_925.0)

    def test_partner_allocation_validates_percentages_and_calculates_each_share(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_partner",
        )

        result = module.allocate_partner_box2(
            tax_year=2025,
            total_taxable_income=100_000,
            taxpayer_pct=40,
            partner_pct=60,
            dividend_withholding_tax=1_000,
        )

        self.assertEqual(result["taxpayer"]["taxable_income"], 40_000.0)
        self.assertEqual(result["taxpayer"]["gross_tax"], 9_800.0)
        self.assertEqual(result["taxpayer"]["dividend_withholding_credit"], 400.0)
        self.assertEqual(result["partner"]["taxable_income"], 60_000.0)
        self.assertEqual(result["partner"]["gross_tax"], 14_700.0)
        self.assertEqual(result["partner"]["dividend_withholding_credit"], 600.0)

        with self.assertRaises(ValueError):
            module.allocate_partner_box2(
                tax_year=2025,
                total_taxable_income=100_000,
                taxpayer_pct=60,
                partner_pct=30,
            )

    def test_loss_returns_zero_gross_tax_and_manual_review_data(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_loss",
        )

        result = module.calculate_box2_tax(
            tax_year=2025,
            regular_benefits=1_000,
            regular_costs=2_000,
        )

        self.assertEqual(result["taxable_income"], -1_000.0)
        self.assertEqual(result["gross_tax"], 0.0)
        self.assertEqual(result["loss"]["current_year_loss"], 1_000.0)
        self.assertIn("box2_loss", result["manual_review_flags"])

    def test_validator_flags_unsupported_complex_markers_for_manual_review(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/validate_box2_inputs.py",
            "validate_box2_inputs_complex",
        )

        result = module.validate_box2_input_payload(
            {
                "workflow": "annual_2025",
                "tax_year": 2025,
                "substantial_interest_pct": 5,
                "regular_benefits": 0,
                "complex_markers": {
                    "valuation_dispute": True,
                    "emigration": True,
                },
            }
        )

        self.assertEqual(result["errors"], [])
        self.assertFalse(result["supported_standard_case"])
        self.assertTrue(result["manual_review_required"])
        self.assertIn("valuation_dispute", result["manual_review_flags"])
        self.assertIn("emigration", result["manual_review_flags"])


if __name__ == "__main__":
    unittest.main()
