#!/usr/bin/env python3
"""Reliability tests for optional mechanical tax arithmetic checks."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)


def load_module(relative_path: str, name: str):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Box1MechanicalReliabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module(
            "skills/nl-tax-box1-home/scripts/validate_own_home_inputs.py",
            "box1_mechanical_reliability",
        )

    def valid_payload(self, **overrides):
        payload = {
            "tax_year": 2025,
            "eigenwoningforfait": "4000",
            "mortgage_interest": "3500",
            "qualifying_financing_costs": "0",
            "periodic_erfpacht_opstal_beklemming": "0",
            "taxable_income": "80000",
        }
        payload.update(overrides)
        return payload

    def test_negative_box1_income_is_valid_context_for_rate_adjustment_check(self):
        result = self.module.validate(self.valid_payload(taxable_income="-10000"))

        self.assertEqual(result["errors"], [])
        adjustment = result["review_adjustments"]["tariefsaanpassing"]
        self.assertFalse(adjustment["applies"])
        self.assertEqual(adjustment["amount"], "0.00")

    def test_direct_arithmetic_apis_reject_nonfinite_inputs_cleanly(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            self.module.calculate_eigenwoningforfait(float("inf"), 2025)
        with self.assertRaisesRegex(ValueError, "finite"):
            self.module.calculate_tariefsaanpassing(float("nan"), 80_000, 2025)
        with self.assertRaisesRegex(ValueError, "finite"):
            self.module.calculate_hillenregeling(4_000, float("inf"), 2025)

    def test_direct_hillen_check_rejects_unreviewed_year(self):
        with self.assertRaisesRegex(ValueError, "No reviewed Hillenregeling"):
            self.module.calculate_hillenregeling(4_000, 3_500, 2024)


class Box2MechanicalReliabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "box2_mechanical_reliability",
        )

    def valid_payload(self, **overrides):
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

    def test_empty_or_ambiguous_allocation_input_is_not_silently_ignored(self):
        empty = self.module.calculate_from_payload(
            self.valid_payload(partner_allocation=[])
        )
        self.assertTrue(empty["errors"])
        self.assertIsNone(empty["result"])

        ambiguous = self.module.calculate_from_payload(
            self.valid_payload(
                partner_allocation={"taxpayer_pct": 50, "partner_pct": 50},
                allocation={"taxpayer_pct": 50, "partner_pct": 50},
                full_year_fiscal_partner=True,
            )
        )
        self.assertTrue(any("either" in error for error in ambiguous["errors"]))
        self.assertIsNone(ambiguous["result"])

    def test_invalid_partner_status_is_rejected_even_without_allocation(self):
        output = self.module.calculate_from_payload(
            self.valid_payload(full_year_fiscal_partner="true")
        )

        self.assertTrue(any("boolean" in error for error in output["errors"]))
        self.assertIsNone(output["result"])


class Box3MechanicalReliabilityTests(unittest.TestCase):
    ANNUAL = ROOT / "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py"
    PROVISIONAL = (
        ROOT / "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py"
    )

    @classmethod
    def setUpClass(cls):
        cls.annual = load_module(
            "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
            "box3_annual_mechanical_reliability",
        )
        cls.provisional = load_module(
            "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
            "box3_provisional_mechanical_reliability",
        )

    @staticmethod
    def accepted_rows(value="100000"):
        return [
            {
                "id": "bank",
                "category": "banktegoeden",
                "status": "accepted",
                "value": value,
                "provenance": "U:confirmed amount",
            }
        ]

    @staticmethod
    def rejected_rows():
        return [
            {
                "id": "unresolved",
                "category": "unknown",
                "status": "manual_review",
                "value": "1000",
                "provenance": "U:unresolved",
            }
        ]

    def test_manual_review_without_result_has_nonzero_cli_status(self):
        cases = (
            (self.ANNUAL, ["--actual_return", "0"]),
            (self.PROVISIONAL, []),
        )
        for script, extra in cases:
            with self.subTest(script=script.name):
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(script),
                        "--rows-json",
                        json.dumps(self.rejected_rows()),
                        *extra,
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 1, completed.stderr)
                output = json.loads(completed.stdout)
                self.assertTrue(output["manual_review_required"])
                self.assertIsNone(output["result"])

    def test_nonfinite_or_boolean_allocation_is_rejected_cleanly(self):
        cases = (
            (self.annual.validate_allocation_pct, float("nan")),
            (self.annual.validate_allocation_pct, True),
            (self.provisional.validate_allocation_pct, float("inf")),
            (self.provisional.validate_allocation_pct, False),
        )
        for validator, value in cases:
            with self.subTest(validator=validator.__module__, value=value):
                with self.assertRaises(ValueError):
                    validator(value)

    def test_large_finite_row_does_not_crash_or_emit_invalid_json(self):
        cases = (
            (self.ANNUAL, ["--actual_return", "0"], "box3_belasting"),
            (self.PROVISIONAL, [], "estimated_tax"),
        )
        for script, extra, result_key in cases:
            with self.subTest(script=script.name):
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(script),
                        "--rows-json",
                        json.dumps(self.accepted_rows("1e308")),
                        *extra,
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(completed.returncode, 0, completed.stderr)
                output = json.loads(completed.stdout)
                self.assertFalse(output["manual_review_required"])
                self.assertIsInstance(output[result_key], int)

    def test_provisional_output_labels_rounding_as_nonbinding_working_convention(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(self.PROVISIONAL),
                "--rows-json",
                json.dumps(self.accepted_rows()),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = json.loads(completed.stdout)
        self.assertEqual(
            output["share_percentage_rounding"]["working_convention"],
            "three_decimals",
        )
        self.assertEqual(
            output["share_percentage_rounding"]["published_examples_convention"],
            "two_decimals",
        )
        self.assertTrue(
            output["share_percentage_rounding"][
                "estimate_may_differ_due_to_rounding"
            ]
        )
        self.assertIn(
            "examples display two",
            output["share_percentage_rounding"]["official_instruction_note"],
        )
        self.assertIn("not a guaranteed portal result", output["rounding_note"])
        self.assertIn("beschikking", output["rounding_note"])


if __name__ == "__main__":
    unittest.main()
