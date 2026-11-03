#!/usr/bin/env python3
"""Smoke tests for optional mechanical NL tax helper validators."""

import importlib.util
import pathlib
import tempfile
import unittest


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidatorSmokeTests(unittest.TestCase):
    def test_field_map_rejects_empty_fields_and_empty_missing_fields(self):
        module = load_module(
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
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
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
            "validate_field_map_workflow_year",
        )

        cases = [
            ("annual_return", 2027),
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
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
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
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
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
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
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

    def test_knowledge_validator_reports_missing_snapshot_metadata(self):
        module = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_missing_metadata",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            snapshot = root / "skills/nl-tax-shared-resources/knowledge/example.md"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("source_id: source_one\nstatus: active\n", encoding="utf-8")

            errors = module.collect_snapshot_metadata_errors(
                [
                    {
                        "id": "source_one",
                        "snapshot_path": "skills/nl-tax-shared-resources/knowledge/example.md",
                        "url": "https://www.belastingdienst.nl/example",
                    }
                ],
                str(root),
            )

        self.assertTrue(any(error[0] == "source_one" and "missing" in error[1] for error in errors))

    def test_knowledge_validator_reports_stale_snapshot_hash(self):
        module = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_stale_metadata",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            snapshot = root / "skills/nl-tax-shared-resources/knowledge/example.md"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("source_id: source_one\nstatus: active\n", encoding="utf-8")
            metadata = snapshot.parent / "_snapshot-metadata.yaml"
            metadata.write_text(
                "\n".join(
                    [
                        "metadata_version: '1.1'",
                        "sources:",
                        "  source_one:",
                        "    reviewed_note_hash_sha256: stale",
                        "    review_status: reviewed",
                        "    reviewed_note_hash_recorded_at: '2026-01-01T00:00:00+00:00'",
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
                        "snapshot_path": "skills/nl-tax-shared-resources/knowledge/example.md",
                        "url": "https://www.belastingdienst.nl/example",
                    }
                ],
                str(root),
            )

        self.assertTrue(any(error[0] == "source_one" and "hash mismatch" in error[1] for error in errors))

    def test_knowledge_validator_reports_snapshot_missing_its_registered_source_id(self):
        module = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_missing_source_id",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            snapshot = root / "skills/nl-tax-shared-resources/knowledge/example.md"
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
                        "metadata_version: '1.1'",
                        "sources:",
                        "  source_one:",
                        f"    reviewed_note_hash_sha256: {digest}",
                        "    review_status: reviewed",
                        "    reviewed_note_hash_recorded_at: '2026-01-01T00:00:00+00:00'",
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
                        "snapshot_path": "skills/nl-tax-shared-resources/knowledge/example.md",
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
