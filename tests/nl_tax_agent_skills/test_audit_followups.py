#!/usr/bin/env python3
"""Regression tests for the full-audit follow-up fixes.

Covers:
    - Cross-host invocation policy: every non-user-invocable skill ships an
      agents/openai.yaml with policy.allow_implicit_invocation: false.
    - Field-map identifier-placeholder convention (BSN/IBAN live in
      missing_fields without a value; the portal pre-fills them).
    - The two marketplace.json files agree on plugin name and path.
    - Evidence indexer cataloging: hash-failure handling and stable ids.
"""

import importlib.util
import json
import os
import pathlib
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
SKILLS_DIR = ROOT / "skills"


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InvocationPolicyTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_invocation_policy.py",
            "validate_invocation_policy",
        )

    def test_real_skills_pass(self):
        errors, checked = self.mod.collect_errors(str(SKILLS_DIR))
        self.assertEqual(errors, [], f"unexpected invocation-policy errors: {errors}")
        # Only the hidden shared skill and background helpers are guarded.
        self.assertEqual(
            set(checked),
            {
                "_shared",
                "nl-tax-box1-home",
                "nl-tax-box2",
                "nl-tax-box3",
                "nl-tax-partner-deductions",
                "nl-tax-winst",
            },
        )
        for name in (
            "nl-tax-box1-home",
            "nl-tax-box2",
            "nl-tax-box3",
            "nl-tax-partner-deductions",
            "nl-tax-winst",
        ):
            self.assertIn(name, checked)

    def test_missing_openai_yaml_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = pathlib.Path(tmp)
            helper = skills / "nl-tax-newhelper"
            helper.mkdir()
            (helper / "SKILL.md").write_text(
                "---\nname: nl-tax-newhelper\n"
                "description: helper\nuser-invocable: false\n---\nbody\n",
                encoding="utf-8",
            )
            errors, checked = self.mod.collect_errors(str(skills))
            self.assertIn("nl-tax-newhelper", checked)
            self.assertTrue(errors)
            self.assertEqual(errors[0][0], "nl-tax-newhelper")

    def test_disable_model_invocation_requires_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = pathlib.Path(tmp)
            helper = skills / "nl-tax-manual"
            (helper / "agents").mkdir(parents=True)
            (helper / "SKILL.md").write_text(
                "---\nname: nl-tax-manual\n"
                "description: manual\ndisable-model-invocation: true\n---\nbody\n",
                encoding="utf-8",
            )
            # Wrong policy value -> still fails.
            (helper / "agents" / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: true\n", encoding="utf-8"
            )
            errors, _ = self.mod.collect_errors(str(skills))
            self.assertTrue(errors)
            # Correct policy value -> passes.
            (helper / "agents" / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: false\n", encoding="utf-8"
            )
            errors, _ = self.mod.collect_errors(str(skills))
            self.assertEqual(errors, [])

    def test_user_invocable_skill_not_required_to_have_openai_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = pathlib.Path(tmp)
            entry = skills / "nl-tax-entry"
            entry.mkdir()
            (entry / "SKILL.md").write_text(
                "---\nname: nl-tax-entry\ndescription: entry point\n---\nbody\n",
                encoding="utf-8",
            )
            errors, checked = self.mod.collect_errors(str(skills))
            self.assertEqual(checked, [])
            self.assertEqual(errors, [])


class FieldMapIdentifierPlaceholderTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_guard",
        )

    def test_bsn_placeholder_in_missing_fields_still_passes(self):
        # The established convention: personal.bsn lives in missing_fields with no
        # value (the portal pre-fills it). That path must remain valid.
        data = {
            "field_map_version": "1.1",
            "workflow": "provisional_assessment",
            "tax_year": 2026,
            "fields": [
                {
                    "field_id": "box1.loon",
                    "label": "Loon",
                    "value": 45000,
                    "confidence": 0.9,
                    "manual_review_required": False,
                    "source": {"type": "estimate"},
                }
            ],
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.adres"},
            ],
        }
        errors, _ = self.mod.validate(data)
        self.assertFalse(
            any("bsn" in e.lower() or "iban" in e.lower() for e in errors),
            errors,
        )


class MarketplaceConsistencyTests(unittest.TestCase):
    @staticmethod
    def _plugin_entry(path):
        data = json.loads(path.read_text(encoding="utf-8"))
        plugins = data.get("plugins", [])
        if not plugins:
            raise AssertionError(f"no plugins in {path}")
        return plugins[0]

    @staticmethod
    def _source_path(entry):
        source = entry.get("source")
        if isinstance(source, str):
            return source
        if isinstance(source, dict):
            return source.get("path")
        return None

    @unittest.skipUnless(
        (REPO_ROOT / ".claude-plugin" / "marketplace.json").is_file()
        and (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").is_file(),
        "dev-repo marketplace manifests not present — standalone package run",
    )
    def test_marketplaces_agree_on_name_and_path(self):
        claude = self._plugin_entry(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        agents = self._plugin_entry(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(claude.get("name"), agents.get("name"))
        self.assertEqual(self._source_path(claude), self._source_path(agents))
        self.assertEqual(claude.get("name"), "nl-tax-agent-skills")
        self.assertEqual(self._source_path(claude), "./plugins/nl-tax-agent-skills")


class EvidenceIndexerTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-evidence-indexer/scripts/index_evidence.py",
            "index_evidence",
        )

    def test_hash_failure_yields_none_and_failed_status(self):
        # Unit-level: compute_sha256 returns None (never an error string) on a
        # missing/unreadable file.
        result = self.mod.compute_sha256("/nonexistent/path/does-not-exist.txt")
        self.assertIsNone(result)

        # Integration-level: an unreadable real file is cataloged with a None
        # hash and extraction_status "failed".
        if getattr(os, "geteuid", lambda: 1)() == 0:
            # Running as root bypasses chmod 000, so only assert the unit case.
            self.skipTest("running as root: chmod 000 does not block reads")
        with tempfile.TemporaryDirectory() as tmp:
            scanned = pathlib.Path(tmp)
            unreadable = scanned / "locked.txt"
            unreadable.write_text("cannot read me", encoding="utf-8")
            os.chmod(unreadable, 0o000)
            try:
                entries = self.mod.scan_directory(str(scanned))
            finally:
                os.chmod(unreadable, 0o600)

            locked = [e for e in entries if e.get("file_name") == "locked.txt"]
            self.assertEqual(len(locked), 1, entries)
            entry = locked[0]
            self.assertIsNone(entry.get("file_sha256"))
            self.assertEqual(entry.get("extraction_status"), "failed")
            self.assertTrue(entry.get("review_required"))

    def test_relative_file_path_and_stable_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            scanned = pathlib.Path(tmp)
            (scanned / "a.txt").write_text("alpha content", encoding="utf-8")
            (scanned / "b.txt").write_text("beta content", encoding="utf-8")
            entries = self.mod.scan_directory(str(scanned))
            for e in entries:
                # Paths are stored relative to the scanned directory.
                self.assertFalse(os.path.isabs(e["file_path"]), e["file_path"])
                # IDs are content-hash derived (ev_ + 10 hex chars).
                self.assertTrue(e["evidence_id"].startswith("ev_"))

            ids_before = {e["file_name"]: e["evidence_id"] for e in entries}
            # Deleting one file must not renumber the OTHER file's id.
            (scanned / "a.txt").unlink()
            entries2 = self.mod.scan_directory(str(scanned))
            ids_after = {e["file_name"]: e["evidence_id"] for e in entries2}
            self.assertEqual(ids_before["b.txt"], ids_after["b.txt"])

    def test_inventory_does_not_classify_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            (folder / "jaaropgaaf-2025.txt").write_text(
                "Jaaropgaaf 2025; loon 50000", encoding="utf-8"
            )

            entry = self.mod.index_directory(str(folder))[0]

            self.assertEqual(entry["evidence_type"], "")
            self.assertIsNone(entry["tax_year"])
            self.assertIsNone(entry["confidence"])
            self.assertIsNone(entry["owner"])
            self.assertEqual(entry["extraction_status"], "indexed_only")
            rendered = self.mod.format_output([entry], str(folder))
            self.assertIn("check_performed_by: checked_by_script", rendered)

if __name__ == "__main__":
    unittest.main()
