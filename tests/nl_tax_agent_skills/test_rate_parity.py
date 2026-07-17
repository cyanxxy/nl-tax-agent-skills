#!/usr/bin/env python3
"""Rate-parity tests (LO-03).

The optional mechanical arithmetic checks duplicate rates/thresholds from the
canonical knowledge .md files (the knowledge pack is the source of truth).
These tests read the .md files, extract the numbers, and assert the Python
constants match. They are read-only on the checks: if a value genuinely
mismatches, that is a real drift bug to fix in the helper, not here.
"""

import importlib.util
import io
import json
import pathlib
import re
import sys
import unittest
from contextlib import redirect_stdout


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)
KNOWLEDGE = ROOT / "skills" / "_shared" / "knowledge"


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    # Register before exec so @dataclass introspection (Python 3.12+) can resolve
    # the module via sys.modules[cls.__module__]; scripts with a module-level
    # dataclass (e.g. validate_own_home_inputs.OwnHomeResult) fail to load otherwise.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_md(relative_path):
    return (KNOWLEDGE / relative_path).read_text(encoding="utf-8")


def find_percentages(text):
    """Return the set of percentage values (as fractions) found in the text."""
    return {
        round(float(m) / 100, 6)
        for m in re.findall(r"(\d+(?:\.\d+)?)\s*%", text)
    }


def find_euros(text):
    """Return the set of integer EUR amounts found in the text.

    Handles both '67,804' (comma thousands) and 'EUR 57684' forms.
    """
    amounts = set()
    for m in re.findall(r"EUR\s*([\d.,]+)", text):
        cleaned = m.strip().rstrip(".").replace(",", "").replace(".", "")
        if cleaned.isdigit():
            amounts.add(int(cleaned))
    return amounts


class Box2RateParityTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_parity",
        )
        self.md = read_md("years/2025/box2/box2-rates.md")

    def test_thresholds_match_knowledge(self):
        euros = find_euros(self.md)
        self.assertIn(67_804, euros)
        self.assertIn(68_843, euros)
        self.assertEqual(int(self.module.BOX2_RATES[2025]["threshold"]), 67_804)
        self.assertEqual(int(self.module.BOX2_RATES[2026]["threshold"]), 68_843)

    def test_rates_match_knowledge(self):
        pcts = find_percentages(self.md)
        self.assertIn(0.245, pcts)
        self.assertIn(0.31, pcts)
        for year in (2025, 2026):
            self.assertEqual(float(self.module.BOX2_RATES[year]["lower_rate"]), 0.245)
            self.assertEqual(float(self.module.BOX2_RATES[year]["upper_rate"]), 0.31)


class Box3AnnualRateParityTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(
            "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
            "compare_box3_annual_2025_parity",
        )
        self.md = read_md("years/2025/box3/fictitious.md")

    def test_return_percentages_match_knowledge(self):
        pcts = find_percentages(self.md)
        self.assertIn(0.0137, pcts)
        self.assertIn(0.0588, pcts)
        self.assertIn(0.027, pcts)
        self.assertEqual(float(self.module.PERC_BANKTEGOEDEN), 0.0137)
        self.assertEqual(float(self.module.PERC_OVERIGE_BEZITTINGEN), 0.0588)
        self.assertEqual(float(self.module.PERC_SCHULDEN), 0.0270)

    def test_tax_rate_matches_knowledge(self):
        self.assertIn(0.36, find_percentages(self.md))
        self.assertEqual(float(self.module.TAX_RATE), 0.36)

    def test_heffingsvrij_matches_knowledge(self):
        self.assertIn(57_684, find_euros(self.md))
        self.assertEqual(self.module.HEFFINGSVRIJ_PER_PERSON, 57_684)


class Box3ProvisionalRateParityTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(
            "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
            "summarize_box3_provisional_2026_parity",
        )
        self.box3_md = read_md("years/2026/provisional/box3-provisional.md")
        self.rates_md = read_md("years/2026/provisional/rates-and-credits.md")

    def test_return_percentages_match_box3_provisional_note(self):
        pcts = find_percentages(self.box3_md)
        self.assertIn(0.0128, pcts)
        self.assertIn(0.06, pcts)
        self.assertIn(0.027, pcts)
        self.assertEqual(float(self.module.PERC_BANKTEGOEDEN), 0.0128)
        self.assertEqual(float(self.module.PERC_OVERIGE_BEZITTINGEN), 0.0600)
        self.assertEqual(float(self.module.PERC_SCHULDEN), 0.0270)

    def test_return_percentages_match_rates_and_credits_note(self):
        pcts = find_percentages(self.rates_md)
        self.assertIn(0.0128, pcts)
        self.assertIn(0.06, pcts)
        self.assertIn(0.027, pcts)

    def test_tax_rate_matches_knowledge(self):
        self.assertIn(0.36, find_percentages(self.box3_md))
        self.assertIn(0.36, find_percentages(self.rates_md))
        self.assertEqual(float(self.module.TAX_RATE), 0.36)

    def test_heffingsvrij_matches_knowledge(self):
        self.assertIn(59_357, find_euros(self.box3_md))
        self.assertIn(59_357, find_euros(self.rates_md))
        self.assertEqual(self.module.HEFFINGSVRIJ_PER_PERSON, 59_357)


class Box1OwnHomeRateParityTests(unittest.TestCase):
    """Guard the box1 eigenwoningforfait, Hillen, and tariefsaanpassing constants
    against their canonical knowledge notes (closes the audit 4.7c residual: the
    box2/box3 checks were parity-tested but box1's were not)."""

    def setUp(self):
        self.module = load_module(
            "skills/nl-tax-box1-home/scripts/validate_own_home_inputs.py",
            "validate_own_home_inputs_parity",
        )
        self.forfait_md = read_md("own-home/eigenwoningforfait.md")
        self.own_home_2025_md = read_md("years/2025/annual/own-home.md")
        self.own_home_2026_md = read_md("years/2026/provisional/own-home.md")

    def test_eigenwoningforfait_brackets_match_knowledge(self):
        pcts = find_percentages(self.forfait_md)
        euros = find_euros(self.forfait_md)
        for pct in (0.0010, 0.0020, 0.0025, 0.0035, 0.0235):
            self.assertIn(pct, pcts)
        for amount in (12_500, 25_000, 50_000, 75_000,
                       1_330_000, 4_655, 1_350_000, 4_725):
            self.assertIn(amount, euros)
        table = self.module.EIGENWONINGFORFAIT_TABLE
        self.assertEqual(
            [row[2] for row in table[2025]],
            [0.0, 0.0010, 0.0020, 0.0025, 0.0035, 0.0235],
        )
        self.assertEqual(table[2025][-1][0], 1_330_000)
        self.assertEqual(table[2025][-1][3], 4_655)
        self.assertEqual(
            [row[2] for row in table[2026]],
            [0.0, 0.0010, 0.0020, 0.0025, 0.0035, 0.0235],
        )
        self.assertEqual(table[2026][-1][0], 1_350_000)
        self.assertEqual(table[2026][-1][3], 4_725)

    def test_hillenregeling_remaining_matches_knowledge(self):
        pcts = find_percentages(self.forfait_md)
        self.assertIn(0.76667, pcts)
        self.assertIn(0.71867, pcts)
        self.assertEqual(float(self.module.HILLENREGELING_REMAINING[2025]), 0.76667)
        self.assertEqual(float(self.module.HILLENREGELING_REMAINING[2026]), 0.71867)

    def test_tariefsaanpassing_2025_matches_knowledge(self):
        pcts = find_percentages(self.own_home_2025_md)
        euros = find_euros(self.own_home_2025_md)
        self.assertIn(0.495, pcts)    # schijf 3 rate 49.50%
        self.assertIn(0.3748, pcts)   # 2025 cap 37.48%
        self.assertIn(76_817, euros)  # schijf 3 threshold
        ta = self.module.TARIEFSAANPASSING[2025]
        self.assertEqual(ta["schijf3_threshold"], 76_817)
        self.assertEqual(ta["schijf3_rate"], 0.4950)
        self.assertEqual(ta["cap_rate"], 0.3748)

    def test_tariefsaanpassing_2026_matches_knowledge(self):
        pcts = find_percentages(self.own_home_2026_md)
        euros = find_euros(self.own_home_2026_md)
        self.assertIn(0.3756, pcts)   # 2026 cap 37.56%
        self.assertIn(78_426, euros)  # schijf 3 threshold
        ta = self.module.TARIEFSAANPASSING[2026]
        self.assertEqual(ta["schijf3_threshold"], 78_426)
        self.assertEqual(ta["cap_rate"], 0.3756)
        # The schijf-3 IB rate (49.50%) is shared with 2025; the 2026 note states
        # it only implicitly (cap 37.56% + tariefsaanpassing 11.94%), so assert the
        # script constant directly rather than scanning the note for it.
        self.assertEqual(ta["schijf3_rate"], 0.4950)

    def test_cli_uses_the_same_explicit_amount_contract(self):
        output = io.StringIO()
        with redirect_stdout(output):
            status = self.module.main(
                [
                    "--tax-year", "2025",
                    "--eigenwoningforfait", "4000",
                    "--mortgage-interest", "3500",
                    "--qualifying-financing-costs", "300",
                    "--periodic-erfpacht-opstal-beklemming", "300",
                    "--taxable-income", "80000",
                ]
            )
        result = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(result, self.module.validate({
            "tax_year": 2025,
            "eigenwoningforfait": "4000",
            "mortgage_interest": "3500",
            "qualifying_financing_costs": "300",
            "periodic_erfpacht_opstal_beklemming": "300",
            "taxable_income": "80000",
        }))
        self.assertNotIn("woz_value", result)
        self.assertNotIn("mortgage_start_year", result)


if __name__ == "__main__":
    unittest.main()
