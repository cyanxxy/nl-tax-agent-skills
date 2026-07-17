#!/usr/bin/env python3
"""Focused tests for the optional mechanical Box 2 arithmetic check."""

import importlib.util
import pathlib
import unittest


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)


def valid_annual_payload(**overrides):
    payload = {
        "workflow": "annual_2025",
        "tax_year": 2025,
        "substantial_interest_pct": "10",
        "resident_full_year": True,
        "standard_ab_case": True,
        "regular_benefits": "10000",
        "disposal_benefit": "0",
        "loss_setoff": "0",
    }
    payload.update(overrides)
    return payload


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Box2HelperTests(unittest.TestCase):
    def test_payload_entrypoint_is_the_only_public_full_calculation_api(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_public_api",
        )
        self.assertTrue(callable(module.calculate_from_payload))
        self.assertFalse(hasattr(module, "calculate_box2_tax"))

    def test_2025_bracket_calculation_splits_lower_and_upper_income(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_2025",
        )

        result = module._calculate_box2_tax(
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

        result = module._calculate_box2_tax(
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

        result = module._calculate_box2_tax(
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

        result = module._calculate_box2_tax(
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

        result = module._calculate_box2_tax(
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

        result = module._calculate_box2_tax(
            tax_year=2025,
            regular_benefits=1_000,
            regular_costs=2_000,
        )

        self.assertEqual(result["taxable_income"], -1_000.0)
        self.assertEqual(result["gross_tax"], 0.0)
        self.assertEqual(result["loss"]["current_year_loss"], 1_000.0)
        self.assertIn("box2_loss", result["manual_review_flags"])

    def test_allocation_without_full_year_fiscal_partner_is_not_standard_case(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_partner_unconfirmed_validation",
        )

        result = module.calculate_from_payload(
            valid_annual_payload(
                **{
                    "regular_benefits": 100_000,
                    "partner_allocation": {
                        "taxpayer_pct": 40,
                        "partner_pct": 60,
                    },
                }
            )
        )

        self.assertIsNone(result["result"])
        self.assertTrue(result["normalized"]["manual_review_required"])
        self.assertIn(
            "partner_status_unconfirmed",
            result["normalized"]["manual_review_flags"],
        )

    def test_calculator_skips_partner_split_without_full_year_fiscal_partner(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_partner_unconfirmed",
        )

        output = module.calculate_from_payload(
            valid_annual_payload(
                **{
                    "regular_benefits": 100_000,
                    "partner_allocation": {
                        "taxpayer_pct": 40,
                        "partner_pct": 60,
                    },
                }
            )
        )

        self.assertIsNone(output["result"])
        self.assertIn(
            "partner_status_unconfirmed",
            output["normalized"]["manual_review_flags"],
        )

    def test_calculator_emits_partner_split_when_full_year_fiscal_partner_true(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_partner_confirmed",
        )

        output = module.calculate_from_payload(
            valid_annual_payload(
                **{
                    "regular_benefits": 100_000,
                    "full_year_fiscal_partner": True,
                    "partner_allocation": {
                        "taxpayer_pct": 40,
                        "partner_pct": 60,
                    },
                }
            )
        )
        result = output["result"]

        self.assertEqual(output["errors"], [])
        self.assertIn("partner_allocation", result)
        self.assertNotIn("partner_allocation_skipped", result)
        self.assertEqual(
            result["partner_allocation"]["taxpayer"]["taxable_income"], 40_000.0
        )
        self.assertEqual(
            result["partner_allocation"]["partner"]["taxable_income"], 60_000.0
        )

    def test_integrated_validator_flags_unsupported_complex_markers_for_manual_review(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_complex",
        )

        result = module.calculate_from_payload(
            valid_annual_payload(
                **{
                    "substantial_interest_pct": 5,
                    "regular_benefits": 0,
                    "complex_markers": {
                        "valuation_dispute": True,
                        "emigration": True,
                    },
                }
            )
        )

        self.assertIsNone(result["result"])
        self.assertTrue(result["normalized"]["manual_review_required"])
        self.assertIn("valuation_dispute", result["normalized"]["manual_review_flags"])
        self.assertIn("emigration", result["normalized"]["manual_review_flags"])

    def test_payload_validation_cannot_be_bypassed(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_integrated_validation",
        )
        for patch in (
            {"substantial_interest_pct": ""},
            {"resident_full_year": "true"},
            {"standard_ab_case": False},
            {"workflow": "provisional_2026", "tax_year": 2025},
        ):
            with self.subTest(patch=patch):
                output = module.calculate_from_payload(valid_annual_payload(**patch))
                self.assertTrue(output["errors"])
                self.assertIsNone(output["result"])

    def test_loss_setoff_blocks_until_reviewed(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_loss_review",
        )
        blocked = module.calculate_from_payload(valid_annual_payload(loss_setoff="500"))
        self.assertIsNone(blocked["result"])

        reviewed = module.calculate_from_payload(
            valid_annual_payload(
                loss_setoff="500",
                loss_setoff_reviewed=True,
                loss_setoff_source="2025 assessment loss statement",
            )
        )
        self.assertFalse(reviewed["errors"])
        self.assertIsNotNone(reviewed["result"])
        self.assertNotIn(
            "loss_setoff_manual_review",
            reviewed["result"]["manual_review_flags"],
        )

    def test_unknown_amount_key_is_rejected(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_unknown_key",
        )
        output = module.calculate_from_payload(
            valid_annual_payload(regluar_benefits="10000")
        )
        self.assertTrue(any("unknown" in item.lower() for item in output["errors"]))

    def test_large_amounts_never_crash_decimal_or_emit_nonfinite_json(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_large_amounts",
        )

        representable = module.calculate_from_payload(
            valid_annual_payload(regular_benefits="1e100")
        )
        self.assertEqual(representable["errors"], [])
        self.assertIsNotNone(representable["result"])

        too_large = module.calculate_from_payload(
            valid_annual_payload(regular_benefits="1e1000")
        )
        self.assertTrue(too_large["errors"])
        self.assertIsNone(too_large["result"])

        aggregate_overflow = module.calculate_from_payload(
            valid_annual_payload(
                regular_benefits="1e308",
                disposal_benefit="1e308",
            )
        )
        self.assertTrue(aggregate_overflow["errors"])
        self.assertIsNone(aggregate_overflow["result"])

    def test_integrated_output_records_script_check(self):
        module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_check_trail",
        )
        output = module.calculate_from_payload(valid_annual_payload())
        self.assertEqual(output["check_performed_by"], "checked_by_script")


if __name__ == "__main__":
    unittest.main()
