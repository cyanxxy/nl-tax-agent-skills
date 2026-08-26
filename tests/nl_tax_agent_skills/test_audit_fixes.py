#!/usr/bin/env python3
"""Regression tests for fixes from the full-codebase audit."""

import contextlib
import hashlib
import io
import importlib.util
import os
import pathlib
import subprocess
import sys
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


def provisional_field(field_id, source, notes=None):
    field = {
        "field_id": field_id,
        "label": "Neutral label",
        "source": source,
        "confidence": 0.9,
        "manual_review_required": False,
    }
    if notes is not None:
        field["notes"] = notes
    return field


class FieldMapWerkelijkScanTests(unittest.TestCase):
    """The provisional werkelijk-rendement guard must also scan quotes and notes."""

    def setUp(self):
        self.module = load_module(
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
            "validate_field_map_werkelijk_scan",
        )

    def assert_critical(self, field):
        errors, _ = self.module.validate(
            {
                "field_map_version": "1.1",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [field],
                "missing_fields": [],
            }
        )
        self.assertTrue(
            any("werkelijk rendement field in provisional map" in error for error in errors),
            errors,
        )

    def test_flags_werkelijk_in_source_quote(self):
        self.assert_critical(
            provisional_field(
                "box3.banktegoeden_totaal",
                {
                    "type": "user_chat",
                    "quote": "use my werkelijk rendement of 2400 euro",
                    "stated_at": "2026-06-01",
                },
            )
        )

    def test_flags_werkelijk_in_notes(self):
        self.assert_critical(
            provisional_field(
                "box3.overige_bezittingen_totaal",
                {"type": "baseline", "baseline_ref": "va-2026-01"},
                notes="taxpayer asked to switch to actual return next year",
            )
        )

    def test_clean_provisional_field_passes_the_guard(self):
        errors, _ = self.module.validate(
            {
                "field_map_version": "1.1",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    provisional_field(
                        "box3.banktegoeden_totaal",
                        {
                            "type": "user_chat",
                            "quote": "about 50000 in savings",
                            "stated_at": "2026-06-01",
                        },
                    )
                ],
                "missing_fields": [],
            }
        )
        self.assertFalse(
            any("werkelijk rendement" in error for error in errors),
            errors,
        )


class BuildSnapshotsReviewStatusTests(unittest.TestCase):
    """build_snapshots must never promote a snapshot to reviewed on its own."""

    SCRIPT = ROOT / "../../tools/nl_tax_agent_skills/source_maintenance/scripts/build_snapshots.py"

    def run_build(self, project_root):
        register = project_root / "skills" / "_shared" / "source-register.yaml"
        return subprocess.run(
            [sys.executable, str(self.SCRIPT), str(register)],
            capture_output=True,
            text=True,
            check=False,
        )

    def make_project(
        self,
        tmp,
        snapshot_text,
        metadata_text=None,
        with_repository_metadata=True,
    ):
        repo_root = pathlib.Path(tmp)
        if with_repository_metadata:
            project_root = repo_root / "plugins" / "nl-tax-agent-skills"
            metadata_root = (
                repo_root
                / "tools"
                / "nl_tax_agent_skills"
                / "source_maintenance"
                / "metadata"
            )
            metadata_root.mkdir(parents=True)
        else:
            project_root = repo_root / "nl-tax-agent-skills"
            metadata_root = None
        (project_root / ".claude-plugin").mkdir(parents=True)
        knowledge = project_root / "skills" / "_shared" / "knowledge"
        knowledge.mkdir(parents=True)
        (knowledge / "note.md").write_text(snapshot_text, encoding="utf-8")
        if metadata_text is not None:
            target = (
                metadata_root / "_snapshot-metadata.yaml"
                if metadata_root is not None
                else knowledge / "_snapshot-metadata.yaml"
            )
            target.write_text(
                metadata_text, encoding="utf-8"
            )
        (project_root / "skills" / "_shared" / "source-register.yaml").write_text(
            "sources:\n"
            "  - id: test_source\n"
            "    url: \"https://www.belastingdienst.nl/test\"\n"
            "    snapshot_path: \"skills/_shared/knowledge/note.md\"\n",
            encoding="utf-8",
        )
        return project_root

    def load_metadata(self, project_root):
        import yaml

        meta_path = (
            project_root.parents[1]
            / "tools"
            / "nl_tax_agent_skills"
            / "source_maintenance"
            / "metadata"
            / "_snapshot-metadata.yaml"
        )
        with meta_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)

    def test_unchanged_snapshot_keeps_needs_review(self):
        snapshot_text = "# Rule note\n\nsome content\n"
        current_hash = hashlib.sha256(snapshot_text.encode("utf-8")).hexdigest()
        metadata_text = (
            "metadata_version: '1.1'\n"
            "sources:\n"
            "  test_source:\n"
            "    source_id: test_source\n"
            "    reviewed_note_hash_recorded_at: '2026-05-01T00:00:00+00:00'\n"
            "    source_url: 'https://www.belastingdienst.nl/test'\n"
            f"    reviewed_note_hash_sha256: {current_hash}\n"
            "    review_status: needs_review\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self.make_project(tmp, snapshot_text, metadata_text)
            result = self.run_build(project_root)
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = self.load_metadata(project_root)
            self.assertEqual(
                metadata["sources"]["test_source"]["review_status"], "needs_review"
            )

    def test_unchanged_snapshot_keeps_reviewed(self):
        snapshot_text = "# Rule note\n\nreviewed content\n"
        current_hash = hashlib.sha256(snapshot_text.encode("utf-8")).hexdigest()
        metadata_text = (
            "metadata_version: '1.1'\n"
            "sources:\n"
            "  test_source:\n"
            "    source_id: test_source\n"
            "    reviewed_note_hash_recorded_at: '2026-05-01T00:00:00+00:00'\n"
            "    source_url: 'https://www.belastingdienst.nl/test'\n"
            f"    reviewed_note_hash_sha256: {current_hash}\n"
            "    review_status: reviewed\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self.make_project(tmp, snapshot_text, metadata_text)
            result = self.run_build(project_root)
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = self.load_metadata(project_root)
            self.assertEqual(
                metadata["sources"]["test_source"]["review_status"], "reviewed"
            )

    def test_new_snapshot_entry_defaults_to_needs_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self.make_project(tmp, "# Rule note\n\nnew content\n")
            result = self.run_build(project_root)
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = self.load_metadata(project_root)
            self.assertEqual(
                metadata["sources"]["test_source"]["review_status"], "needs_review"
            )

    def test_changed_reviewed_note_is_demoted_for_human_review(self):
        metadata_text = (
            "metadata_version: '1.1'\n"
            "sources:\n"
            "  test_source:\n"
            "    source_id: test_source\n"
            "    reviewed_note_hash_recorded_at: '2026-05-01T00:00:00+00:00'\n"
            "    source_url: 'https://www.belastingdienst.nl/test'\n"
            "    reviewed_note_hash_sha256: stale\n"
            "    review_status: reviewed\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self.make_project(
                tmp, "# Rule note\n\nchanged content\n", metadata_text
            )
            result = self.run_build(project_root)
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = self.load_metadata(project_root)
            self.assertEqual(
                metadata["sources"]["test_source"]["review_status"], "needs_review"
            )

    def test_missing_repository_metadata_root_fails_without_runtime_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self.make_project(
                tmp,
                "# Rule note\n\nnew content\n",
                with_repository_metadata=False,
            )
            runtime_metadata = (
                project_root
                / "skills"
                / "_shared"
                / "knowledge"
                / "_snapshot-metadata.yaml"
            )

            result = self.run_build(project_root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("repository-only snapshot metadata", result.stderr)
            self.assertFalse(runtime_metadata.exists())


class PlanSourceRefreshCliTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py",
            "plan_source_refresh_cli",
        )

    def test_parse_cli_args_exits_on_missing_scope(self):
        # Regression: the length check must inspect the argv parameter,
        # not the interpreter-level sys.argv of the calling process.
        # Capture the usage text so suite output stays clean.
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.module.parse_cli_args(["plan_source_refresh.py"])

    def test_parse_cli_args_parses_scope_year_and_fetch_flag(self):
        scope, year, fetch_flag = self.module.parse_cli_args(
            ["plan_source_refresh.py", "provisional", "2026", "--fetch"]
        )
        self.assertEqual(scope, "provisional")
        self.assertEqual(year, 2026)
        self.assertTrue(fetch_flag)

    def test_allowed_domains_match_source_register_validator(self):
        validator = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_source_register.py",
            "validate_source_register_domains",
        )
        self.assertEqual(self.module.ALLOWED_DOMAINS, validator.ALLOWED_DOMAINS)


class SourceRegisterValidatorRobustnessTests(unittest.TestCase):
    def test_empty_register_reports_error_instead_of_crashing(self):
        module = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_source_register.py",
            "validate_source_register_empty",
        )
        with tempfile.NamedTemporaryFile(
            "w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as handle:
            handle.write("# empty register\n")
            path = handle.name
        try:
            errors, _ = module.validate(path)
        finally:
            os.unlink(path)
        self.assertTrue(
            any("empty or could not be parsed" in error for error in errors),
            errors,
        )


class KnowledgePackUnknownSourceTests(unittest.TestCase):
    def test_unknown_source_id_is_collected_as_error(self):
        module = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py",
            "validate_knowledge_pack_unknown_refs",
        )
        with tempfile.TemporaryDirectory() as tmp:
            project_root = pathlib.Path(tmp)
            knowledge_dir = project_root / "knowledge"
            knowledge_dir.mkdir()
            (knowledge_dir / "note.md").write_text(
                "# Rule note\n\n"
                "source_ids: nonexistent_source\n"
                "status: active\n"
                "review_status: reviewed\n",
                encoding="utf-8",
            )
            (
                _unreferenced,
                _review_markers,
                _workflow_errors,
                unknown_reference_errors,
            ) = module.collect_knowledge_file_errors(
                str(knowledge_dir),
                str(project_root / "missing-skills-dir"),
                str(project_root),
                {"registered_source"},
            )
        self.assertIn(
            ("knowledge/note.md", "nonexistent_source"),
            [
                (rel.replace(os.sep, "/"), source_id)
                for rel, source_id in unknown_reference_errors
            ],
        )


if __name__ == "__main__":
    unittest.main()
