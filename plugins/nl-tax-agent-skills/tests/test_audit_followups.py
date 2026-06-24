#!/usr/bin/env python3
"""Regression tests for the full-audit follow-up fixes.

Covers three guards added after the audit:
    - Cross-host invocation policy: every non-user-invocable skill ships an
      agents/openai.yaml with policy.allow_implicit_invocation: false.
    - Field-map BSN/IBAN deterministic guard.
    - The two marketplace.json files agree on plugin name and path.
"""

import hashlib
import importlib.util
import json
import os
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]          # plugins/nl-tax-agent-skills
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]     # repo root
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
            "skills/nl-tax-source-refresh/scripts/validate_invocation_policy.py",
            "validate_invocation_policy",
        )

    def test_real_skills_pass(self):
        errors, checked = self.mod.collect_errors(str(SKILLS_DIR))
        self.assertEqual(errors, [], f"unexpected invocation-policy errors: {errors}")
        # All six background/manual-only skills must be detected and guarded.
        for name in (
            "nl-tax-box1-home",
            "nl-tax-box2",
            "nl-tax-box3",
            "nl-tax-partner-deductions",
            "nl-tax-source-refresh",
            "nl-tax-submit-companion",
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


class FieldMapCredentialGuardTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_guard",
        )

    def test_bsn_value_in_field_is_rejected(self):
        errors = []
        field = {
            "field_id": "personal.bsn",
            "label": "BSN",
            "value": "111222333",  # valid elfproef BSN
            "source": {"type": "user_chat", "quote": "my bsn is 111222333"},
        }
        self.mod.validate_field(field, 0, "annual_return", set(), errors, [])
        self.assertTrue(any("BSN" in e for e in errors), errors)

    def test_iban_value_in_quote_is_rejected(self):
        errors = []
        field = {
            "field_id": "box3.refund_account",
            "label": "Rekening",
            "value": "NL91ABNA0417164300",
            "source": {"type": "user_chat", "quote": "account NL91ABNA0417164300"},
        }
        self.mod.validate_field(field, 0, "annual_return", set(), errors, [])
        self.assertTrue(any("IBAN" in e for e in errors), errors)

    def test_elfproef_rejects_random_nine_digits(self):
        # A 9-digit number that fails the 11-test should NOT be flagged as a BSN.
        self.assertFalse(self.mod._passes_elfproef("123456789"))
        self.assertTrue(self.mod._passes_elfproef("111222333"))

    def test_bsn_placeholder_in_missing_fields_still_passes(self):
        # The established convention: personal.bsn lives in missing_fields with no
        # value. That path must remain valid (no credential error).
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
            any("BSN" in e or "IBAN" in e or "Credential" in e for e in errors),
            errors,
        )


class MarketplaceConsistencyTests(unittest.TestCase):
    @staticmethod
    def _plugin_entry(path):
        data = json.loads(path.read_text(encoding="utf-8"))
        plugins = data.get("plugins", [])
        assert plugins, f"no plugins in {path}"
        return plugins[0]

    @staticmethod
    def _source_path(entry):
        source = entry.get("source")
        if isinstance(source, str):
            return source
        if isinstance(source, dict):
            return source.get("path")
        return None

    def test_marketplaces_agree_on_name_and_path(self):
        claude = self._plugin_entry(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        agents = self._plugin_entry(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(claude.get("name"), agents.get("name"))
        self.assertEqual(self._source_path(claude), self._source_path(agents))
        self.assertEqual(claude.get("name"), "nl-tax-agent-skills")
        self.assertEqual(self._source_path(claude), "./plugins/nl-tax-agent-skills")


class EvidenceIndexerSecurityTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-evidence-indexer/scripts/index_evidence.py",
            "index_evidence",
        )

    def test_symlink_outside_dir_is_not_hashed_or_cataloged(self):
        with tempfile.TemporaryDirectory() as tmp:
            scanned = pathlib.Path(tmp) / "scanned"
            outside = pathlib.Path(tmp) / "outside"
            scanned.mkdir()
            outside.mkdir()

            # Secret content lives OUTSIDE the scanned directory.
            secret = outside / "secret.txt"
            secret_text = "TOP SECRET payroll data that must never be hashed"
            secret.write_text(secret_text, encoding="utf-8")
            secret_digest = hashlib.sha256(
                secret_text.encode("utf-8")
            ).hexdigest()

            # A symlink inside the scanned dir points at the outside secret.
            link = scanned / "link.txt"
            try:
                os.symlink(secret, link)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks not supported on this platform")

            entries = self.mod.scan_directory(str(scanned))

            # The out-of-dir content must NEVER appear as a hash.
            hashes = [e.get("file_sha256") for e in entries]
            self.assertNotIn(secret_digest, hashes)

            # The symlink itself may be cataloged as a skipped/failed item, but
            # never hashed or followed.
            for e in entries:
                if e.get("file_name") == "link.txt":
                    self.assertIsNone(e.get("file_sha256"))
                    self.assertEqual(e.get("extraction_status"), "failed")
                    self.assertTrue(
                        any("symlink" in n.lower() for n in e.get("notes", [])),
                        e.get("notes"),
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
            return
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

    def test_macro_spreadsheets_flagged_as_active_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            scanned = pathlib.Path(tmp)
            (scanned / "old.xls").write_bytes(b"\xd0\xcf\x11\xe0legacy")
            (scanned / "macro.xlsm").write_bytes(b"PK\x03\x04macro")
            entries = self.mod.scan_directory(str(scanned))
            macro_entries = [
                e for e in entries if e.get("file_name") in {"old.xls", "macro.xlsm"}
            ]
            self.assertEqual(len(macro_entries), 2, entries)
            for entry in macro_entries:
                with self.subTest(file_name=entry.get("file_name")):
                    self.assertTrue(entry.get("active_content_detected"))
                    self.assertTrue(entry.get("review_required"))
                    self.assertTrue(
                        any("macro" in n.lower() for n in entry.get("notes", [])),
                        entry.get("notes"),
                    )

            formatted = self.mod.format_output(entries, str(scanned))
            self.assertIn("active_content_count: 2", formatted)

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

if __name__ == "__main__":
    unittest.main()
