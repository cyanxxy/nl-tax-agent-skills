#!/usr/bin/env python3
"""Focused tests for workflow/source-register coupling."""

import importlib.util
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkflowSourceValidationTests(unittest.TestCase):
    def test_active_workflow_missing_mandatory_box2_source_fails_validation(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py",
            "validate_supported_workflows_missing_box2",
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / ".codex-plugin").mkdir()
            shared = root / "skills/_shared"
            (shared / "knowledge/years/2025/annual").mkdir(parents=True)
            (shared / "knowledge/years/2025/box2").mkdir(parents=True)

            supported = shared / "supported-workflows.yaml"
            supported.write_text(
                """
version: 1
active_workflows:
  - id: annual_2025
    workflow: annual_return
    tax_year: 2025
    status: active
    profile_candidates:
      - annual_2025
    knowledge_dirs:
      - skills/_shared/knowledge/years/2025/annual
      - skills/_shared/knowledge/years/2025/box2
    output_paths:
      - workspace/annual/2025/return-pack.md
    required_source_ids:
      - bd_annual_test
blocked_workflows: []
""",
                encoding="utf-8",
            )
            register = shared / "source-register.yaml"
            register.write_text(
                """
sources:
  - id: bd_annual_test
    title: Annual test source
    url: https://www.belastingdienst.nl/example
    source_type: official_guidance
    workflow: annual_return
    tax_year: 2025
    snapshot_path: skills/_shared/knowledge/years/2025/annual/test.md
    last_checked: "2026-01-01"
    freshness_policy: check annually
    owner: tax-content
    mandatory_for:
      - nl-tax-annual-return
  - id: bd_box2_rates_test
    title: Box 2 rates test source
    url: https://www.belastingdienst.nl/box2
    source_type: official_rates
    workflow: annual_return
    tax_year: 2025
    snapshot_path: skills/_shared/knowledge/years/2025/box2/box2-rates.md
    last_checked: "2026-01-01"
    freshness_policy: check annually
    owner: tax-content
    mandatory_for:
      - nl-tax-box2
""",
                encoding="utf-8",
            )

            errors, _ = module.validate(str(supported), str(register))

        self.assertTrue(
            any("mandatory" in error and "bd_box2_rates_test" in error for error in errors),
            errors,
        )

    def test_source_register_accepts_box2_mandatory_skill(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_source_register.py",
            "validate_source_register_box2",
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / ".codex-plugin").mkdir()
            snapshot = root / "skills/_shared/knowledge/years/2025/box2/box2-rates.md"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("source_id: bd_box2_rates_test\n", encoding="utf-8")
            register = root / "skills/_shared/source-register.yaml"
            register.write_text(
                """
sources:
  - id: bd_box2_rates_test
    title: Box 2 rates test source
    url: https://www.belastingdienst.nl/box2
    source_type: official_rates
    snapshot_path: skills/_shared/knowledge/years/2025/box2/box2-rates.md
    last_checked: "2026-01-01"
    freshness_policy: check annually
    owner: tax-content
    mandatory_for:
      - nl-tax-box2
""",
                encoding="utf-8",
            )

            errors, warnings = module.validate(str(register))

        self.assertEqual(errors, [])
        self.assertFalse(any("unknown skill" in warning for warning in warnings), warnings)

    def test_blocked_roadmap_workflows_remain_blocked_without_source_ids(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py",
            "validate_supported_workflows_blocked_roadmap",
        )
        config = module.load_yaml_or_json(str(ROOT / "skills/_shared/supported-workflows.yaml"))
        blocked_by_id = {
            workflow.get("id"): workflow
            for workflow in config.get("blocked_workflows", [])
        }

        expected_ids = {
            "annual_2025_entrepreneurs_roadmap",
            "annual_2025_nonresidents_c_form_roadmap",
            "annual_2025_migration_m_form_roadmap",
            "annual_2025_deceased_f_form_roadmap",
            "annual_2025_foreign_treaty_heavy_roadmap",
            "annual_2027",
            "provisional_2027",
        }

        self.assertTrue(expected_ids.issubset(blocked_by_id), blocked_by_id.keys())
        for workflow_id in expected_ids:
            with self.subTest(workflow_id=workflow_id):
                workflow = blocked_by_id[workflow_id]
                self.assertEqual(workflow.get("status"), "blocked_pending_official_sources")
                self.assertIs(workflow.get("may_prepare_workpack"), False)
                self.assertNotIn("required_source_ids", workflow)

    def test_scoped_blocked_workflow_can_share_active_workflow_year(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py",
            "validate_supported_workflows_scoped_blocked",
        )

        active_pairs = {("annual_return", 2025)}
        blocked = {
            "id": "annual_2025_entrepreneurs_roadmap",
            "workflow": "annual_return",
            "tax_year": 2025,
            "status": "blocked_pending_official_sources",
            "may_prepare_workpack": False,
            "profile_candidates": ["annual_2025_entrepreneurs"],
            "allowed_output": "workspace/shared/missing-info.md",
            "reason": "Entrepreneur workflows need dedicated official sources.",
            "unlock_condition": "Add reviewed entrepreneur sources and tests.",
        }

        errors, warnings = module.validate_blocked_workflow(blocked, set(), active_pairs)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
