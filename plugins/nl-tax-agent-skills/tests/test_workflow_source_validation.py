#!/usr/bin/env python3
"""Focused tests for workflow/source-register coupling."""

import hashlib
import importlib.util
import pathlib
import tempfile
import unittest
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent.parent


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
        self.assertFalse(
            any("unknown skill" in msg for msg in errors + warnings),
            (errors, warnings),
        )

    def test_provisional_2026_box2_note_is_registered_and_metadata_covered(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_box2_2026_note",
        )
        register = module.load_yaml_or_json(str(ROOT / "skills/_shared/source-register.yaml"))
        sources = register.get("sources", [])
        source_by_id = {source.get("id"): source for source in sources}

        source = source_by_id.get("bd_box2_provisional_2026")

        self.assertIsNotNone(source)
        self.assertEqual(
            source.get("snapshot_path"),
            "skills/_shared/knowledge/years/2026/provisional/box2.md",
        )
        self.assertEqual(source.get("workflow"), "provisional_assessment")
        self.assertEqual(source.get("tax_year"), 2026)
        self.assertIn("nl-tax-box2", source.get("mandatory_for", []))
        self.assertEqual(module.collect_snapshot_metadata_errors([source], str(ROOT)), [])

    def test_source_register_documents_snapshot_path_base_conventions(self):
        register = (ROOT / "skills/_shared/source-register.yaml").read_text(
            encoding="utf-8"
        )
        refresh_skill = (ROOT / "skills/nl-tax-source-refresh/SKILL.md").read_text(
            encoding="utf-8"
        )
        combined = f"{register}\n{refresh_skill}"

        self.assertIn("repo root", combined)
        self.assertIn("skill-relative", combined)
        self.assertIn("_shared/", combined)

    def test_box3_examples_have_direct_register_coverage(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_box3_examples",
        )
        register = module.load_yaml_or_json(str(ROOT / "skills/_shared/source-register.yaml"))
        sources = register.get("sources", [])
        matching = [
            source for source in sources
            if source.get("snapshot_path") == "skills/_shared/knowledge/years/2025/box3/examples.md"
        ]

        self.assertEqual(len(matching), 1)
        self.assertEqual(module.collect_snapshot_metadata_errors(matching, str(ROOT)), [])

    def test_fetch_flag_reports_refresh_plan_without_live_fetch_language(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/fetch_sources.py",
            "fetch_sources_plan_only",
        )
        source = {
            "id": "bd_stale_test",
            "title": "Stale test source",
            "url": "https://www.belastingdienst.nl/example",
            "source_type": "official_guidance",
            "last_checked": "2025-01-01",
            "snapshot_path": "skills/_shared/knowledge/years/2026/provisional/box2.md",
        }

        report = module.build_report(
            [source],
            [source],
            datetime(2026, 5, 25, tzinfo=timezone.utc),
            str(ROOT),
            str(ROOT / "skills/_shared/source-register.yaml"),
            "all",
            None,
            True,
        )
        entry = report["sources_checked"][0]

        self.assertEqual(report["report_type"], "source_refresh_plan")
        self.assertTrue(report["refresh_plan_requested"])
        self.assertNotIn("dry" + "_run", report)
        self.assertNotIn("mode", report)
        self.assertEqual(report["operation"], "plan_only_no_live_http")
        self.assertEqual(entry["refresh_action"], "PLAN_REFRESH (plan-only -- no live HTTP)")
        self.assertNotIn("fetch_action", entry)
        self.assertEqual(entry["staleness_threshold_days"], 180)
        self.assertEqual(entry["expires_on"], "2025-06-30")
        self.assertGreater(entry["age_days"], entry["staleness_threshold_days"])

    @unittest.skipUnless(
        (REPO_ROOT / "CHANGELOG.md").is_file(),
        "dev-repo CHANGELOG.md not present — standalone package run",
    )
    def test_changelog_notes_source_refresh_report_schema_change(self):
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

        self.assertIn("source-refresh report schema", changelog.lower())
        self.assertIn("dry_run", changelog)
        self.assertIn("mode", changelog)
        self.assertIn("refresh_plan_requested", changelog)
        self.assertIn("operation", changelog)

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

    def test_terminal_workflows_are_validated_for_shape(self):
        module = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py",
            "validate_supported_workflows_terminal",
        )
        config = module.load_yaml_or_json(str(ROOT / "skills/_shared/supported-workflows.yaml"))
        terminal_by_id = {
            workflow.get("id"): workflow
            for workflow in config.get("terminal_workflows", [])
        }
        # The shipped terminal entries are well-formed.
        for workflow_id in ("manual_review", "unsupported"):
            with self.subTest(workflow_id=workflow_id):
                self.assertIn(workflow_id, terminal_by_id)
                errors, _ = module.validate_terminal_workflow(
                    terminal_by_id[workflow_id], set()
                )
                self.assertEqual(errors, [])

        # A typo in the load-bearing fields is now caught, not silently ignored.
        bad = {
            "id": "manual_review",
            "status": "terminal_manual_review",
            "may_prepare_workpack": True,
            "allowed_output": "workspace/annual/2025/return-pack.md",
            "profile_candidates": ["manual_review"],
        }
        errors, _ = module.validate_terminal_workflow(bad, set())
        self.assertTrue(any("may_prepare_workpack" in e for e in errors), errors)
        self.assertTrue(any("workspace/shared/" in e for e in errors), errors)

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
