#!/usr/bin/env python3
"""Regression tests for deterministic Box 1 / own-home helper behavior."""

import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load():
    return load_module(
        "skills/nl-tax-box1-home/scripts/validate_own_home_inputs.py",
        "validate_own_home_inputs",
    )


class Box1OwnHomeTests(unittest.TestCase):
    # --- Hillenregeling golden cases (verified ground truth) ---
    # Each case is tagged with its tax_year because the remaining-benefit
    # percentage phases out year over year, and ROUND_HALF_UP rounding to whole
    # euros is what the Belastingdienst applies.
    def test_hillenregeling_2026_4000_3500(self):
        module = _load()
        applies, correction, remaining = module.calculate_hillenregeling(
            eigenwoningforfait=4_000,
            mortgage_interest=3_500,
            tax_year=2026,
        )
        # excess 500 x 0.71867 = 359.335 -> 359 (ROUND_HALF_UP)
        self.assertTrue(applies)
        self.assertEqual(correction, 359)
        self.assertAlmostEqual(remaining, 0.71867)

    def test_hillenregeling_2026_1200_1000(self):
        module = _load()
        applies, correction, remaining = module.calculate_hillenregeling(
            eigenwoningforfait=1_200,
            mortgage_interest=1_000,
            tax_year=2026,
        )
        # excess 200 x 0.71867 = 143.734 -> 144 (ROUND_HALF_UP)
        self.assertTrue(applies)
        self.assertEqual(correction, 144)
        self.assertAlmostEqual(remaining, 0.71867)

    def test_hillenregeling_2025_1200_1000_half_up(self):
        module = _load()
        applies, correction, remaining = module.calculate_hillenregeling(
            eigenwoningforfait=1_200,
            mortgage_interest=1_000,
            tax_year=2025,
        )
        # excess 200 x 0.76667 = 153.334 -> 153 (ROUND_HALF_UP, not 154)
        self.assertTrue(applies)
        self.assertEqual(correction, 153)
        self.assertAlmostEqual(remaining, 0.76667)

    # --- Tariefsaanpassing golden case (statutory capped grondslag) ---
    def test_tariefsaanpassing_official_grondslag_2026(self):
        module = _load()
        # belastbaar (AFTER eigen-woning result) = 80141, deductible = 3500.
        # income without deduction = 80141 + 3500 = 83641 > 78426 -> applies.
        # grondslag = min(3500, 83641 - 78426 = 5215) = 3500   (art. 2.10 lid 2 cap)
        # adjustment = round(3500 x (0.4950 - 0.3756), 2) = 417.90
        # (The correction can never exceed rate_diff x deducted costs = 417.90.)
        applies, adjustment, warnings = module.calculate_tariefsaanpassing(
            mortgage_interest=3_500,
            belastbaar_inkomen=80_141,
            tax_year=2026,
        )
        self.assertTrue(applies)
        self.assertEqual(adjustment, 417.90)
        self.assertTrue(any("capped at" in warning for warning in warnings))

    def test_tariefsaanpassing_capped_at_deducted_costs_high_income(self):
        module = _load()
        # Very high income: the cap binds, so adjustment = rate_diff x deductible,
        # never the (much larger) income-over-drempel amount.
        applies, adjustment, _ = module.calculate_tariefsaanpassing(
            mortgage_interest=4_000,
            belastbaar_inkomen=200_000,
            tax_year=2026,
        )
        self.assertTrue(applies)
        self.assertEqual(adjustment, 477.60)  # 4000 x 0.1194

    def test_tariefsaanpassing_applies_on_income_without_deduction(self):
        module = _load()
        # belastbaar 76000 is BELOW the 78426 drempel, but income WITHOUT the
        # deduction (76000 + 4000 = 80000) exceeds it, so the rule still applies.
        # grondslag = min(4000, 80000 - 78426 = 1574) = 1574 -> 187.94.
        applies, adjustment, _ = module.calculate_tariefsaanpassing(
            mortgage_interest=4_000,
            belastbaar_inkomen=76_000,
            tax_year=2026,
        )
        self.assertTrue(applies)
        self.assertEqual(adjustment, 187.94)

    def test_tariefsaanpassing_not_applicable_below_threshold(self):
        module = _load()
        # income without deduction = 50000 + 3500 = 53500 < 78426 -> no adjustment.
        applies, adjustment, _ = module.calculate_tariefsaanpassing(
            mortgage_interest=3_500,
            belastbaar_inkomen=50_000,
            tax_year=2026,
        )
        self.assertFalse(applies)
        self.assertEqual(adjustment, 0.0)

    # --- End-to-end main()-style ordering test ---
    def test_end_to_end_hillen_before_tariefsaanpassing_2026(self):
        module = _load()

        income_before_ew = 80_000.0  # box 1 income BEFORE the eigen-woning result
        forfait = 4_000.0
        interest = 3_500.0
        tax_year = 2026

        # Same call order as main(): Hillen first, then tariefsaanpassing.
        hillen_applies, hillen_correction, _ = module.calculate_hillenregeling(
            forfait, interest, tax_year
        )
        self.assertTrue(hillen_applies)
        self.assertEqual(hillen_correction, 359)

        net_after_hillen = round((forfait - hillen_correction) - interest)
        self.assertEqual(net_after_hillen, 141)

        belastbaar = income_before_ew + net_after_hillen
        self.assertEqual(belastbaar, 80_141)

        ta_applies, ta_amount, _ = module.calculate_tariefsaanpassing(
            interest, belastbaar, tax_year
        )
        self.assertTrue(ta_applies)
        # grondslag capped at the deducted costs: min(3500, 80141+3500-78426=5215)
        # = 3500 -> 3500 x 0.1194 = 417.90 (statutory ceiling).
        self.assertEqual(ta_amount, 417.90)

    # --- Renamed field (mortgage_regime_post2013) ---
    def test_mortgage_regime_field_name(self):
        module = _load()
        result = module.OwnHomeResult(
            tax_year=2026,
            woz_value=400_000.0,
            ownership_share_pct=100,
            eigenwoningforfait=1_400,
            mortgage_interest=3_500.0,
            mortgage_start_year=2018,
            mortgage_regime_post2013=True,
            net_eigen_woning=-2_100,
            tariefsaanpassing_applies=False,
            tariefsaanpassing_amount=0.0,
            hillenregeling_applies=False,
            hillenregeling_correction=0,
            hillenregeling_remaining_pct=0.71867,
            net_after_hillen=-2_100,
        )
        self.assertTrue(result.mortgage_regime_post2013)
        self.assertIn("mortgage_regime_post2013", result.to_dict())
        self.assertNotIn("mortgage_qualifies_post2013", result.to_dict())


if __name__ == "__main__":
    unittest.main()
