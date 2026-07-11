#!/usr/bin/env python3
"""Reviewed-note provenance and legal-attribution contracts."""

import hashlib
import importlib.util
import pathlib
import unittest
from datetime import datetime, timezone

import yaml


PLUGIN = pathlib.Path(__file__).resolve().parents[1]
SKILLS = PLUGIN / "skills"
KNOWLEDGE = SKILLS / "_shared/knowledge"
REGISTER_PATH = SKILLS / "_shared/source-register.yaml"


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class SourceProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register = load_yaml(REGISTER_PATH)
        cls.sources = {source["id"]: source for source in register["sources"]}

    def test_metadata_hashes_reviewed_notes(self):
        metadata_paths = sorted(KNOWLEDGE.glob("**/_snapshot-metadata.yaml"))
        self.assertEqual(len(metadata_paths), 13)
        violations = []
        for metadata_path in metadata_paths:
            metadata = load_yaml(metadata_path)
            if metadata.get("metadata_version") != "1.1":
                violations.append(f"{metadata_path}: metadata_version is not 1.1")
            if "snapshot_metadata_version" in metadata:
                violations.append(f"{metadata_path}: legacy metadata version key")
            for source_id, item in metadata["sources"].items():
                required = {
                    "reviewed_note_hash_sha256",
                    "reviewed_note_hash_recorded_at",
                }
                forbidden = {"content_hash_sha256", "snapshot_created_at"}
                if not required <= item.keys() or forbidden & item.keys():
                    violations.append(f"{source_id}: legacy or missing hash keys")
                if item.get("review_status") != "reviewed":
                    violations.append(f"{source_id}: review_status is not reviewed")
        self.assertFalse(
            violations,
            f"{len(violations)} metadata violations; first 10: {violations[:10]}",
        )

    def test_reviewed_note_hash_matches_local_note(self):
        checked = 0
        for metadata_path in KNOWLEDGE.glob("**/_snapshot-metadata.yaml"):
            metadata = load_yaml(metadata_path)
            for source_id, item in metadata["sources"].items():
                if "reviewed_note_hash_sha256" not in item:
                    continue
                checked += 1
                with self.subTest(source_id=source_id):
                    source = self.sources[source_id]
                    note_path = PLUGIN / source["snapshot_path"]
                    digest = hashlib.sha256(note_path.read_bytes()).hexdigest()
                    self.assertEqual(item.get("reviewed_note_hash_sha256"), digest)
        self.assertGreater(checked, 0, "no reviewed-note hashes were available to verify")

    def test_last_checked_is_documented_as_human_review(self):
        register_text = REGISTER_PATH.read_text(encoding="utf-8").lower()
        shared_readme = (
            SKILLS / "_shared/README.md"
        ).read_text(encoding="utf-8").lower()
        combined = register_text + shared_readme
        self.assertIn("last_checked", register_text)
        self.assertIn("human review", combined)
        self.assertIn("reviewed_note_hash_sha256", combined)
        self.assertIn("local reviewed note", combined)
        self.assertRegex(
            combined,
            r"(?:not|never)[^\n]{0,100}remote (?:page )?bod",
        )

    def test_plan_report_separates_reachability_and_review(self):
        script_path = SKILLS / "nl-tax-source-refresh/scripts/plan_source_refresh.py"
        spec = importlib.util.spec_from_file_location("plan_source_refresh", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        source = next(iter(self.sources.values()))
        record = module.source_report_entry(
            source, datetime.now(timezone.utc), PLUGIN, False
        )
        expected = {
            "url_reachability": "not_checked",
            "reachability_checked_at": None,
            "last_retrieved_at": None,
            "last_human_reviewed": str(source["last_checked"]),
            "reviewed_note_path": source["snapshot_path"],
        }
        for field, value in expected.items():
            with self.subTest(field=field):
                self.assertEqual(record.get(field), value)
        note_path = PLUGIN / source["snapshot_path"]
        self.assertEqual(
            record.get("reviewed_note_hash_sha256"),
            hashlib.sha256(note_path.read_bytes()).hexdigest(),
        )

    def test_own_home_attribution_names_wet_ib_article_3_112(self):
        wet_ib = (
            KNOWLEDGE / "laws/wet-inkomstenbelasting-2001.md"
        ).read_text(encoding="utf-8").lower()
        besluit = (
            KNOWLEDGE / "laws/uitvoeringsbesluit-inkomstenbelasting-2001.md"
        ).read_text(encoding="utf-8").lower()
        self.assertIn("3.112", wet_ib)
        self.assertNotIn("eigenwoningforfait percentages are defined", besluit)

    def test_business_retention_attribution_names_awr_article_52(self):
        awr_path = KNOWLEDGE / "laws/algemene-wet-inzake-rijksbelastingen.md"
        self.assertTrue(awr_path.is_file())
        awr = awr_path.read_text(encoding="utf-8").lower()
        self.assertIn("awr", awr)
        self.assertTrue("article 52" in awr or "artikel 52" in awr)
        source_ids = {
            source_id
            for source_id, source in self.sources.items()
            if source["snapshot_path"].endswith(
                "laws/algemene-wet-inzake-rijksbelastingen.md"
            )
        }
        self.assertTrue(source_ids)
        winst_note = (
            KNOWLEDGE / "years/2025/entrepreneur/winst-en-kosten.md"
        ).read_text(encoding="utf-8")
        self.assertTrue(any(source_id in winst_note for source_id in source_ids))
        regeling = (
            KNOWLEDGE / "laws/uitvoeringsregeling-inkomstenbelasting-2001.md"
        ).read_text(encoding="utf-8").lower()
        self.assertNotIn("specifies retention periods", regeling)


if __name__ == "__main__":
    unittest.main()
