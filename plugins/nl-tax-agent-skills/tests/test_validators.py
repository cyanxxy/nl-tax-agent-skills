#!/usr/bin/env python3
"""Smoke tests for deterministic NL tax helper validators."""

import importlib.util
import pathlib
import json
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
        errors, _ = module.validate_allocations(
            [
                {
                    "item": "employment income",
                    "total": 100,
                    "partner1_share": 50,
                    "partner2_share": 50,
                    "allocatable": False,
                }
            ]
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
                "--banktegoeden",
                "150000",
                "--overige",
                "275000",
                "--schulden",
                "100000",
            ],
            text=True,
        )
        data = json.loads(output)

        self.assertNotIn("werkelijk_rendement", data)
        self.assertEqual(
            data["box3_provisional_actual_return_note"],
            "Werkelijk rendement is not part of provisional 2026.",
        )

    def test_box3_classifier_recognizes_official_bank_asset_edge_cases(self):
        module = load_module(
            "skills/nl-tax-box3/scripts/classify_box3_assets.py",
            "classify_box3_assets_edge_cases",
        )
        cases = [
            {"name": "Aandeel reservefonds VvE", "type_hint": "", "value": 900},
            {"name": "Premiedepot hypotheek", "type_hint": "", "value": 1200},
            {"name": "Derdengeldenrekening notaris", "type_hint": "", "value": 5000},
        ]

        for case in cases:
            with self.subTest(case=case["name"]):
                category, _, _ = module.classify_asset(case)
                self.assertEqual(category, "banktegoeden")

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


if __name__ == "__main__":
    unittest.main()
