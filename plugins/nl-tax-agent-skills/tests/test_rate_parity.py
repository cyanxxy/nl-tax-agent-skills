#!/usr/bin/env python3
"""Rate-parity tests (LO-03).

The deterministic calculator scripts duplicate rates/thresholds from the
canonical knowledge .md files (the knowledge pack is the source of truth).
These tests read the .md files, extract the numbers, and assert the Python
constants match. They are read-only on the calculators: if a value genuinely
mismatches, that is a real drift bug to fix in the calculator, not here.
"""

import importlib.util
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "skills" / "_shared" / "knowledge"


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
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
        self.assertEqual(self.module.PERC_BANKTEGOEDEN, 0.0137)
        self.assertEqual(self.module.PERC_OVERIGE_BEZITTINGEN, 0.0588)
        self.assertEqual(self.module.PERC_SCHULDEN, 0.0270)

    def test_tax_rate_matches_knowledge(self):
        self.assertIn(0.36, find_percentages(self.md))
        self.assertEqual(self.module.TAX_RATE, 0.36)

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
        self.assertEqual(self.module.PERC_BANKTEGOEDEN, 0.0128)
        self.assertEqual(self.module.PERC_OVERIGE_BEZITTINGEN, 0.0600)
        self.assertEqual(self.module.PERC_SCHULDEN, 0.0270)

    def test_return_percentages_match_rates_and_credits_note(self):
        pcts = find_percentages(self.rates_md)
        self.assertIn(0.0128, pcts)
        self.assertIn(0.06, pcts)
        self.assertIn(0.027, pcts)

    def test_tax_rate_matches_knowledge(self):
        self.assertIn(0.36, find_percentages(self.box3_md))
        self.assertIn(0.36, find_percentages(self.rates_md))
        self.assertEqual(self.module.TAX_RATE, 0.36)

    def test_heffingsvrij_matches_knowledge(self):
        self.assertIn(59_357, find_euros(self.box3_md))
        self.assertIn(59_357, find_euros(self.rates_md))
        self.assertEqual(self.module.HEFFINGSVRIJ_PER_PERSON, 59_357)


if __name__ == "__main__":
    unittest.main()
