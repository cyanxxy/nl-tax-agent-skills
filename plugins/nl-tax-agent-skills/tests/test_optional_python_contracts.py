#!/usr/bin/env python3
"""Contracts for the plugin's optional, mechanical Python helpers."""

import pathlib
import unittest

import yaml


PLUGIN_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_ROOT = PLUGIN_ROOT / "skills"


EXPECTED_SCRIPT_GROUPS = {
    "inventory_hash": {
        "nl-tax-evidence-indexer/scripts/index_evidence.py",
    },
    "field_map": {
        "nl-tax-field-mapper/scripts/validate_field_map.py",
        "nl-tax-field-mapper/scripts/render_field_map.py",
    },
    "arithmetic": {
        "nl-tax-box1-home/scripts/validate_own_home_inputs.py",
        "nl-tax-box2/scripts/calculate_box2_tax.py",
        "nl-tax-box3/scripts/compare_box3_annual_2025.py",
        "nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
        "nl-tax-partner-deductions/scripts/validate_allocation.py",
    },
    "developer_consistency": {
        "nl-tax-source-refresh/scripts/build_snapshots.py",
        "nl-tax-source-refresh/scripts/plan_source_refresh.py",
        "nl-tax-source-refresh/scripts/validate_invocation_policy.py",
        "nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
        "nl-tax-source-refresh/scripts/validate_source_register.py",
        "nl-tax-source-refresh/scripts/validate_supported_workflows.py",
    },
}


class OptionalPythonContractTests(unittest.TestCase):
    def test_exact_optional_python_inventory(self):
        actual = {
            str(path.relative_to(SKILLS_ROOT))
            for path in SKILLS_ROOT.glob("*/scripts/*.py")
        }
        expected = set().union(*EXPECTED_SCRIPT_GROUPS.values())

        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 14)

    def test_retired_heuristics_have_no_runtime_references(self):
        retired = {
            "summarize_" + "box1_inputs.py",
            "summarize_" + "box2_inputs.py",
            "validate_" + "box2_inputs.py",
            "classify_" + "box3_assets.py",
            "fetch_" + "sources.py",
        }
        shipped = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILLS_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py"}
        )

        for name in retired:
            with self.subTest(name=name):
                self.assertFalse(
                    name in shipped,
                    f"retired helper is still shipped or referenced: {name}",
                )

    def test_runtime_docs_make_python_optional(self):
        for relative in ("README.md", "skills/nl-tax-intake/SKILL.md"):
            text = (PLUGIN_ROOT / relative).read_text(encoding="utf-8").lower()
            with self.subTest(relative=relative):
                self.assertIn("python is optional", text)
                self.assertIn("do not ask", text)
                self.assertIn("install python", text)

    def test_shared_templates_record_who_performed_the_check(self):
        templates = (
            "skills/nl-tax-evidence-indexer/templates/evidence-index.yaml",
            "skills/nl-tax-field-mapper/templates/field-map-template.yaml",
        )
        allowed = {"checked_by_agent", "checked_by_script"}

        for relative in templates:
            data = yaml.safe_load((PLUGIN_ROOT / relative).read_text(encoding="utf-8"))
            with self.subTest(relative=relative):
                self.assertIn("check_performed_by", data)
                self.assertIn(data["check_performed_by"], allowed)


if __name__ == "__main__":
    unittest.main()
