#!/usr/bin/env python3
"""Smoke tests for deterministic NL tax helper validators."""

import importlib.util
import pathlib
import json
import math
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidatorSmokeTests(unittest.TestCase):
    def test_field_map_rejects_empty_fields_and_empty_missing_fields(self):
        module = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_empty",
        )

        errors, _ = module.validate(
            {
                "field_map_version": "1.1",
                "workflow": "annual_return",
                "tax_year": 2025,
                "fields": [],
                "missing_fields": [],
            }
        )

        self.assertTrue(any("fields" in error and "missing_fields" in error for error in errors))

    def test_field_map_rejects_unsupported_workflow_year_combinations(self):
        module = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_workflow_year",
        )

        cases = [
            ("annual_return", 2026),
            ("provisional_assessment", 2025),
            ("annual", 2025),
        ]
        for workflow, tax_year in cases:
            with self.subTest(workflow=workflow, tax_year=tax_year):
                errors, _ = module.validate(
                    {
                        "field_map_version": "1.1",
                        "workflow": workflow,
                        "tax_year": tax_year,
                        "fields": [
                            {
                                "field_id": "personal.naam",
                                "label": "Naam",
                                "source": {"type": "baseline"},
                                "confidence": 0.9,
                                "manual_review_required": False,
                            }
                        ],
                        "missing_fields": [
                            {"field_id": "personal.bsn"},
                        ],
                    }
                )

                self.assertTrue(
                    any("Unsupported workflow/tax_year combination" in error for error in errors),
                    errors,
                )

    def test_field_map_requires_required_reference_fields_to_be_represented(self):
        module = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_required_reference_fields",
        )

        errors, _ = module.validate(
            {
                "field_map_version": "1.1",
                "workflow": "annual_return",
                "tax_year": 2025,
                "fields": [
                    {
                        "field_id": "personal.naam",
                        "label": "Naam",
                        "source": {"type": "baseline"},
                        "confidence": 0.9,
                        "manual_review_required": False,
                    }
                ],
                "missing_fields": [
                    {"field_id": "personal.bsn"},
                    {"field_id": "personal.adres"},
                    {"field_id": "personal.geboortedatum"},
                    {"field_id": "box1.loon"},
                ],
            }
        )

        self.assertTrue(any("box1.loonheffing" in error for error in errors), errors)

    def test_field_map_accepts_required_reference_fields_in_fields_or_missing_fields(self):
        module = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_required_reference_fields_valid",
        )

        errors, _ = module.validate(
            {
                "field_map_version": "1.1",
                "workflow": "annual_return",
                "tax_year": 2025,
                "fields": [
                    {
                        "field_id": "box1.loon",
                        "label": "Loon",
                        "source": {"type": "evidence", "evidence_id": "ev_001"},
                        "confidence": 0.9,
                        "manual_review_required": False,
                    }
                ],
                "missing_fields": [
                    {"field_id": "personal.bsn"},
                    {"field_id": "personal.naam"},
                    {"field_id": "personal.adres"},
                    {"field_id": "personal.geboortedatum"},
                    {"field_id": "box1.loonheffing"},
                ],
            }
        )

        self.assertFalse([error for error in errors if "Required reference field" in error], errors)

    def test_provisional_field_map_rejects_actual_return_field(self):
        module = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map",
        )
        errors, _ = module.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box3_werkelijk_rendement",
                        "label": "Werkelijk rendement",
                        "source": {"type": "estimate"},
                        "confidence": 0.9,
                        "manual_review_required": True,
                    }
                ],
            }
        )
        self.assertTrue(any("werkelijk rendement" in error for error in errors))

    def test_allocation_validator_rejects_split_non_allocatable_income(self):
        module = load_module(
            "skills/nl-tax-partner-deductions/scripts/validate_allocation.py",
            "validate_allocation",
        )
        errors = module.validate(
            {
                "has_fiscal_partner": True,
                "items": [
                    {
                        "name": "employment income",
                        "allocatable": False,
                        "taxpayer_pct": 50,
                        "partner_pct": 50,
                    }
                ],
            }
        )
        self.assertTrue(any("non-allocatable" in error for error in errors))

    def test_annual_box3_matches_official_2025_mixed_example(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
            "compare_box3_annual_2025",
        )
        result = module.calculate_fictitious_box3(
            banktegoeden=150_000,
            overige=275_000,
            schulden=100_000,
            heffingsvrij=0,
            has_partner=False,
        )
        self.assertEqual(result["aandeel_in_rendementsgrondslag"], 82.45)
        self.assertEqual(result["box3_inkomen"], 12_885)
        self.assertEqual(result["box3_belasting"], 4_638)

    def test_annual_box3_partner_allocation_matches_official_2025_example(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
            "compare_box3_annual_2025_partner",
        )
        result = module.calculate_fictitious_box3(
            banktegoeden=150_000,
            overige=275_000,
            schulden=100_000,
            heffingsvrij=0,
            has_partner=True,
            allocation_pct=50,
            partner_full_year_confirmed=True,
        )
        self.assertEqual(result["aandeel_in_rendementsgrondslag"], 32.65)
        self.assertEqual(result["box3_inkomen"], 5_135)
        self.assertEqual(result["box3_belasting"], 1_848)

    def test_provisional_box3_uses_official_2026_three_decimal_share_rule(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
            "summarize_box3_provisional_2026",
        )
        result = module.calculate_provisional_fictitious(
            banktegoeden=150_000,
            overige=275_000,
            schulden=100_000,
            heffingsvrij=0,
            has_partner=False,
        )
        self.assertEqual(result["aandeel_in_rendementsgrondslag"], 81.947)
        self.assertEqual(result["box3_inkomen"], 12_966)
        self.assertEqual(result["box3_belasting"], 4_667)

    def test_provisional_box3_partner_allocation_uses_official_2026_three_decimal_share_rule(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
            "summarize_box3_provisional_2026_partner",
        )
        result = module.calculate_provisional_fictitious(
            banktegoeden=150_000,
            overige=275_000,
            schulden=100_000,
            heffingsvrij=0,
            has_partner=True,
            allocation_pct=50,
            partner_full_year_confirmed=True,
        )
        self.assertEqual(result["aandeel_in_rendementsgrondslag"], 32.154)
        self.assertEqual(result["box3_inkomen"], 5_120)
        self.assertEqual(result["box3_belasting"], 1_843)

    def test_provisional_box3_output_has_only_allowed_actual_return_note(self):
        script = ROOT / "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py"
        output = subprocess.check_output(
            [
                sys.executable,
                str(script),
                "--rows-json",
                json.dumps(
                    [
                        {
                            "id": "bank",
                            "category": "banktegoeden",
                            "status": "accepted",
                            "value": 150000,
                            "provenance": "F:bank",
                        },
                        {
                            "id": "assets",
                            "category": "overige_bezittingen",
                            "status": "accepted",
                            "value": 275000,
                            "provenance": "F:assets",
                        },
                        {
                            "id": "debts",
                            "category": "schulden",
                            "status": "accepted",
                            "value": 100000,
                            "provenance": "F:debts",
                        },
                    ]
                ),
            ],
            text=True,
        )
        data = json.loads(output)

        self.assertNotIn("werkelijk_rendement", data)
        self.assertEqual(
            data["box3_provisional_actual_return_note"],
            "Werkelijk rendement is not part of provisional 2026.",
        )

    def test_only_accepted_rows_enter_annual_trusted_totals(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
            "compare_box3_annual_2025_rows",
        )
        rows = [
            {
                "id": "a",
                "category": "banktegoeden",
                "status": "accepted",
                "value": 1000,
                "provenance": "F:bank-2025",
            },
            {
                "id": "b",
                "category": "banktegoeden",
                "status": "manual_review",
                "value": 9000,
                "provenance": "U:loan",
            },
            {
                "id": "c",
                "category": "unknown",
                "status": "accepted",
                "value": 5000,
                "provenance": "F:mystery",
            },
            {
                "id": "d",
                "category": "banktegoeden",
                "status": "accepted",
                "value": -100,
                "provenance": "F:bad",
            },
            {
                "id": "e",
                "category": "overige_bezittingen",
                "status": "accepted",
                "value": 2500,
                "provenance": "",
            },
        ]

        output = module.normalize_classified_rows(rows)
        self.assertEqual(output["trusted_totals"]["banktegoeden"], 1000)
        self.assertEqual(output["trusted_totals"]["overige_bezittingen"], 0)
        self.assertEqual(output["trusted_totals"]["schulden"], 0)
        self.assertEqual(
            {row["id"] for row in output["rejected_rows"]},
            {"b", "c", "d", "e"},
        )
        for row in output["rejected_rows"]:
            self.assertTrue(row["rejection_reasons"])

    def test_provisional_row_normalizer_matches_annual_contract(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
            "summarize_box3_provisional_2026_rows",
        )
        rows = [
            {
                "id": "bank",
                "category": "banktegoeden",
                "status": "accepted",
                "value": "1200.50",
                "provenance": "A:confirmed-estimate",
            },
            {
                "id": "loan",
                "description": "Loan to friend",
                "category": "unknown",
                "status": "manual_review",
                "value": 10_000,
                "provenance": "U:loan-to-friend",
            },
            {
                "id": "nan",
                "category": "schulden",
                "status": "accepted",
                "value": float("nan"),
                "provenance": "F:bad",
            },
        ]

        output = module.normalize_classified_rows(rows)
        self.assertEqual(output["trusted_totals"]["banktegoeden"], 1200.5)
        self.assertEqual(
            {row["id"] for row in output["rejected_rows"]},
            {"loan", "nan"},
        )

    def test_box3_row_normalizers_reject_float_and_total_overflow(self):
        modules = [
            (
                "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
                "compare_box3_annual_2025_overflow",
            ),
            (
                "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
                "summarize_box3_provisional_2026_overflow",
            ),
        ]
        rows = [
            {
                "id": "too-large",
                "category": "overige_bezittingen",
                "status": "accepted",
                "value": "1e400",
                "provenance": "F:huge",
            },
            {
                "id": "first",
                "category": "banktegoeden",
                "status": "accepted",
                "value": "1e308",
                "provenance": "F:first",
            },
            {
                "id": "total-overflow",
                "category": "banktegoeden",
                "status": "accepted",
                "value": "1e308",
                "provenance": "F:second",
            },
        ]

        for relative_path, module_name in modules:
            with self.subTest(path=relative_path):
                module = load_module(relative_path, module_name)
                output = module.normalize_classified_rows(rows)
                self.assertEqual(
                    {row["id"] for row in output["rejected_rows"]},
                    {"too-large", "total-overflow"},
                )
                self.assertEqual(
                    [row["id"] for row in output["accepted_rows"]],
                    ["first"],
                )
                self.assertTrue(
                    all(
                        math.isfinite(value)
                        for value in output["trusted_totals"].values()
                    )
                )
                self.assertTrue(
                    all(
                        math.isfinite(row["value"])
                        for row in output["accepted_rows"]
                    )
                )

    def test_knowledge_validator_reports_missing_snapshot_metadata(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_missing_metadata",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            snapshot = root / "skills/_shared/knowledge/example.md"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("source_id: source_one\nstatus: active\n", encoding="utf-8")

            errors = module.collect_snapshot_metadata_errors(
                [
                    {
                        "id": "source_one",
                        "snapshot_path": "skills/_shared/knowledge/example.md",
                        "url": "https://www.belastingdienst.nl/example",
                    }
                ],
                str(root),
            )

        self.assertTrue(any(error[0] == "source_one" and "missing" in error[1] for error in errors))

    def test_knowledge_validator_reports_stale_snapshot_hash(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_stale_metadata",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            snapshot = root / "skills/_shared/knowledge/example.md"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("source_id: source_one\nstatus: active\n", encoding="utf-8")
            metadata = snapshot.parent / "_snapshot-metadata.yaml"
            metadata.write_text(
                "\n".join(
                    [
                        "snapshot_metadata_version: '1.0'",
                        "sources:",
                        "  source_one:",
                        "    content_hash_sha256: stale",
                        "    review_status: reviewed",
                        "    snapshot_created_at: '2026-01-01T00:00:00+00:00'",
                        "    source_id: source_one",
                        "    source_url: https://www.belastingdienst.nl/example",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            errors = module.collect_snapshot_metadata_errors(
                [
                    {
                        "id": "source_one",
                        "snapshot_path": "skills/_shared/knowledge/example.md",
                        "url": "https://www.belastingdienst.nl/example",
                    }
                ],
                str(root),
            )

        self.assertTrue(any(error[0] == "source_one" and "hash mismatch" in error[1] for error in errors))

    def test_knowledge_validator_reports_snapshot_missing_its_registered_source_id(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_missing_source_id",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            snapshot = root / "skills/_shared/knowledge/example.md"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text(
                "source_id: different_source\nstatus: active\nreview_status: reviewed\n",
                encoding="utf-8",
            )
            digest = module.compute_sha256(str(snapshot))
            metadata = snapshot.parent / "_snapshot-metadata.yaml"
            metadata.write_text(
                "\n".join(
                    [
                        "snapshot_metadata_version: '1.0'",
                        "sources:",
                        "  source_one:",
                        f"    content_hash_sha256: {digest}",
                        "    review_status: reviewed",
                        "    snapshot_created_at: '2026-01-01T00:00:00+00:00'",
                        "    source_id: source_one",
                        "    source_url: https://www.belastingdienst.nl/example",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            errors = module.collect_snapshot_metadata_errors(
                [
                    {
                        "id": "source_one",
                        "snapshot_path": "skills/_shared/knowledge/example.md",
                        "url": "https://www.belastingdienst.nl/example",
                    }
                ],
                str(root),
            )

        self.assertTrue(
            any(
                error[0] == "source_one"
                and "snapshot does not reference source_id" in error[1]
                for error in errors
            ),
            errors,
        )


class Box3InputHardeningTests(unittest.TestCase):
    def _compare_module(self):
        return load_module(
            "skills/nl-tax-box3/scripts/compare_box3_annual_2025.py",
            "compare_box3_annual_2025_hardening",
        )

    def _provisional_module(self):
        return load_module(
            "skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
            "summarize_box3_provisional_2026_hardening",
        )

    def test_annual_negative_amount_raises(self):
        module = self._compare_module()
        with self.assertRaises(ValueError):
            module.calculate_fictitious_box3(
                banktegoeden=-1,
                overige=275_000,
                schulden=100_000,
                heffingsvrij=0,
                has_partner=False,
            )

    def test_annual_nan_and_inf_amount_raise(self):
        module = self._compare_module()
        for bad in (float("nan"), float("inf")):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    module.calculate_fictitious_box3(
                        banktegoeden=bad,
                        overige=275_000,
                        schulden=100_000,
                        heffingsvrij=0,
                        has_partner=False,
                    )

    def test_provisional_negative_amount_raises(self):
        module = self._provisional_module()
        with self.assertRaises(ValueError):
            module.calculate_provisional_fictitious(
                banktegoeden=150_000,
                overige=-5,
                schulden=100_000,
                heffingsvrij=0,
                has_partner=False,
            )

    def test_provisional_nan_and_inf_amount_raise(self):
        module = self._provisional_module()
        for bad in (float("nan"), float("inf")):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    module.calculate_provisional_fictitious(
                        banktegoeden=150_000,
                        overige=275_000,
                        schulden=bad,
                        heffingsvrij=0,
                        has_partner=False,
                    )

    def test_annual_allocation_pct_out_of_range_raises(self):
        module = self._compare_module()
        for pct in (-5, 150):
            with self.subTest(pct=pct):
                with self.assertRaises(ValueError):
                    module.calculate_fictitious_box3(
                        banktegoeden=150_000,
                        overige=275_000,
                        schulden=100_000,
                        heffingsvrij=0,
                        has_partner=True,
                        allocation_pct=pct,
                        partner_full_year_confirmed=True,
                    )

    def test_provisional_allocation_pct_out_of_range_raises(self):
        module = self._provisional_module()
        for pct in (-5, 150):
            with self.subTest(pct=pct):
                with self.assertRaises(ValueError):
                    module.calculate_provisional_fictitious(
                        banktegoeden=150_000,
                        overige=275_000,
                        schulden=100_000,
                        heffingsvrij=0,
                        has_partner=True,
                        allocation_pct=pct,
                        partner_full_year_confirmed=True,
                    )

    def test_annual_partner_without_full_year_confirmation_raises(self):
        module = self._compare_module()
        with self.assertRaises(ValueError):
            module.calculate_fictitious_box3(
                banktegoeden=150_000,
                overige=275_000,
                schulden=100_000,
                heffingsvrij=0,
                has_partner=True,
                allocation_pct=50,
            )

    def test_annual_negative_allocated_actual_return_floors_to_zero(self):
        module = self._compare_module()
        result = module.compare_tax_methods(
            {"box3_belasting": 1_000},
            -25_000,
        )
        self.assertEqual(result["actual_return_for_tax"], 0)
        self.assertEqual(result["tax_at_actual"], 0)


class AllocationHardeningTests(unittest.TestCase):
    def _module(self):
        return load_module(
            "skills/nl-tax-partner-deductions/scripts/validate_allocation.py",
            "validate_allocation_hardening",
        )

    def test_partner_and_allocatable_require_real_booleans(self):
        module = self._module()
        for bad in ("false", "true", 0, 1, None):
            with self.subTest(field="has_fiscal_partner", bad=bad):
                errors = module.validate({"has_fiscal_partner": bad, "items": []})
                self.assertTrue(errors)

            with self.subTest(field="allocatable", bad=bad):
                errors = module.validate(
                    {
                        "has_fiscal_partner": True,
                        "items": [
                            {
                                "name": "Box 3 base",
                                "allocatable": bad,
                                "taxpayer_pct": 50,
                                "partner_pct": 50,
                            }
                        ],
                    }
                )
                self.assertTrue(errors)

    def test_item_name_does_not_decide_allocatability(self):
        module = self._module()
        payload = {
            "has_fiscal_partner": True,
            "items": [
                {
                    "name": "employment income",
                    "allocatable": True,
                    "taxpayer_pct": 50,
                    "partner_pct": 50,
                }
            ],
        }
        self.assertFalse(module.validate(payload))

    def test_wrapped_payload_and_explicit_row_fields_are_required(self):
        module = self._module()
        self.assertTrue(module.validate([]))
        self.assertTrue(module.validate({"has_fiscal_partner": True, "items": [{}]}))

    def test_percentage_string_does_not_crash_and_reports_error(self):
        module = self._module()
        errors = module.validate(
            {
                "has_fiscal_partner": True,
                "items": [
                    {
                        "name": "Box 3 base",
                        "allocatable": True,
                        "taxpayer_pct": "50",
                        "partner_pct": 50,
                    }
                ],
            }
        )
        self.assertTrue(any("real finite number" in e for e in errors), errors)

    def test_nan_and_inf_are_rejected(self):
        module = self._module()
        for bad in (float("nan"), float("inf")):
            with self.subTest(bad=bad):
                errors = module.validate(
                    {
                        "has_fiscal_partner": True,
                        "items": [
                            {
                                "name": "Box 3 base",
                                "allocatable": True,
                                "taxpayer_pct": bad,
                                "partner_pct": 0,
                            }
                        ],
                    }
                )
                self.assertTrue(
                    any("real finite number" in e for e in errors), errors
                )

    def test_percentages_must_be_in_range_and_sum_to_100(self):
        module = self._module()
        for taxpayer_pct, partner_pct in ((-1, 101), (101, -1), (60, 30)):
            with self.subTest(taxpayer_pct=taxpayer_pct, partner_pct=partner_pct):
                errors = module.validate(
                    {
                        "has_fiscal_partner": True,
                        "items": [
                            {
                                "name": "Box 3 base",
                                "allocatable": True,
                                "taxpayer_pct": taxpayer_pct,
                                "partner_pct": partner_pct,
                            }
                        ],
                    }
                )
                self.assertTrue(errors)

    def test_partner_percentage_without_partner_is_rejected(self):
        module = self._module()
        errors = module.validate(
            {
                "has_fiscal_partner": False,
                "items": [
                    {
                        "name": "Box 3 base",
                        "allocatable": True,
                        "taxpayer_pct": 60,
                        "partner_pct": 40,
                    }
                ],
            }
        )
        self.assertTrue(any("no fiscal partner asserted" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
