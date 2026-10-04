#!/usr/bin/env python3
"""Reviewed-note provenance and legal-attribution contracts."""

import hashlib
import importlib.util
import pathlib
import unittest
from datetime import datetime, timezone

import yaml


PLUGIN = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)
REPO = PLUGIN.parents[1]
SKILLS = PLUGIN / "skills"
KNOWLEDGE = SKILLS / "nl-tax-shared-resources/knowledge"
REGISTER_PATH = SKILLS / "nl-tax-shared-resources/source-register.yaml"
METADATA = REPO / "tools/nl_tax_agent_skills/source_maintenance/metadata"
MAINTAINER_NOTES = REPO / "docs/maintainers/source-notes"


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class SourceProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register = load_yaml(REGISTER_PATH)
        cls.sources = {source["id"]: source for source in register["sources"]}

    def test_metadata_hashes_reviewed_notes(self):
        self.assertEqual(list(KNOWLEDGE.glob("**/_snapshot-metadata.yaml")), [])
        metadata_paths = sorted(METADATA.glob("**/_snapshot-metadata.yaml"))
        self.assertEqual(len(metadata_paths), 15)
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
                forbidden = {
                    "content_" + "hash_sha256",
                    "snapshot_" + "created_at",
                }
                if not required <= item.keys() or forbidden & item.keys():
                    violations.append(f"{source_id}: legacy or missing hash keys")
                source = self.sources.get(source_id, {})
                expected_status = "needs_review" if source.get("content_stage") == "draft_only" else "reviewed"
                if item.get("review_status") != expected_status:
                    violations.append(f"{source_id}: review_status is not {expected_status}")
        self.assertFalse(
            violations,
            f"{len(violations)} metadata violations; first 10: {violations[:10]}",
        )

    def test_reviewed_note_hash_matches_local_note(self):
        checked = 0
        for metadata_path in METADATA.glob("**/_snapshot-metadata.yaml"):
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

    def test_maintainer_note_hashes_remain_verified_outside_runtime(self):
        metadata_paths = sorted(
            MAINTAINER_NOTES.glob("**/_snapshot-metadata.yaml")
        )
        self.assertEqual(len(metadata_paths), 3)

        for metadata_path in metadata_paths:
            metadata = load_yaml(metadata_path)
            notes = [
                path
                for path in metadata_path.parent.glob("*.md")
                if path.name != "README.md"
            ]
            note_by_hash = {
                hashlib.sha256(path.read_bytes()).hexdigest(): path
                for path in notes
            }
            for source_id, item in metadata["sources"].items():
                with self.subTest(source_id=source_id):
                    self.assertEqual(item.get("review_status"), "reviewed")
                    digest = item.get("reviewed_note_hash_sha256")
                    self.assertIn(digest, note_by_hash)
                    note_text = note_by_hash[digest].read_text(encoding="utf-8")
                    self.assertIn(source_id, note_text)
                    self.assertTrue(item.get("source_url", "").startswith("https://"))

    def test_last_checked_is_documented_as_human_review(self):
        register_text = REGISTER_PATH.read_text(encoding="utf-8").lower()
        repository_docs = (
            (PLUGIN.parents[1] / "CONTRIBUTING.md").read_text(encoding="utf-8")
            + (
                PLUGIN.parents[1]
                / "tools/nl_tax_agent_skills/source_maintenance/README.md"
            ).read_text(encoding="utf-8")
        ).lower()
        combined = register_text + repository_docs
        self.assertIn("last_checked", register_text)
        self.assertIn("human review", combined)
        self.assertIn("reviewed_note_hash_sha256", combined)
        self.assertIn("local reviewed note", combined)
        self.assertRegex(
            combined,
            r"(?:not|never)[^\n]{0,100}remote (?:page )?bod",
        )

    def test_plan_report_separates_reachability_and_review(self):
        script_path = (
            PLUGIN.parents[1]
            / "tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py"
        )
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

    def _register_module(self):
        script_path = (
            REPO
            / "tools/nl_tax_agent_skills/source_maintenance/scripts/validate_source_register.py"
        )
        spec = importlib.util.spec_from_file_location("validate_source_register_prov", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_draft_sources_record_agent_research_never_human_review(self):
        drafts = {
            sid: source
            for sid, source in self.sources.items()
            if source.get("content_stage") == "draft_only"
        }
        self.assertGreater(len(drafts), 0)
        for sid, source in drafts.items():
            with self.subTest(source_id=sid):
                self.assertEqual(source.get("last_checked_kind"), "agent_source_research")
                self.assertIn("last_human_reviewed", source)
                self.assertIsNone(source["last_human_reviewed"])
                self.assertTrue(source.get("domain"), "draft entries name their domain")
        register_text = REGISTER_PATH.read_text(encoding="utf-8")
        self.assertIn("NEVER a review date", register_text)
        for field in ("content_stage", "workflow_family", "last_checked_kind", "last_human_reviewed"):
            self.assertIn(f"#   {field}", register_text)

    def test_provenance_validator_rejects_fabricated_draft_review(self):
        module = self._register_module()
        base = {
            "content_stage": "draft_only",
            "workflow_family": "vat",
            "last_checked_kind": "agent_source_research",
            "last_human_reviewed": None,
        }
        self.assertEqual(module.provenance_errors("ok", dict(base)), [])
        cases = {
            "review date on a draft": dict(base, last_human_reviewed="2026-10-02"),
            "missing last_checked_kind": {k: v for k, v in base.items() if k != "last_checked_kind"},
            "other last_checked_kind": dict(base, last_checked_kind="human_review"),
            "missing last_human_reviewed": {k: v for k, v in base.items() if k != "last_human_reviewed"},
        }
        for label, source in cases.items():
            with self.subTest(case=label):
                self.assertTrue(module.provenance_errors("bad", source))

    def test_provenance_validator_checks_promoted_sources(self):
        module = self._register_module()
        self.assertEqual(module.provenance_errors("legacy", {}), [])
        self.assertEqual(
            module.provenance_errors(
                "promoted",
                {"last_checked_kind": "human_review", "last_human_reviewed": "2026-10-01"},
            ),
            [],
        )
        self.assertTrue(
            module.provenance_errors("research", {"last_checked_kind": "agent_source_research"})
        )
        self.assertTrue(
            module.provenance_errors("nodate", {"last_human_reviewed": None})
        )
        self.assertTrue(
            module.provenance_errors("future", {"last_human_reviewed": "2999-01-01"})
        )

    def test_promoted_extension_source_needs_a_human_review_date(self):
        module = self._register_module()
        sid, draft = next(
            (sid, source)
            for sid, source in self.sources.items()
            if source.get("workflow_family") == "vat" and source.get("content_stage") == "draft_only"
        )
        promoted = {
            key: value
            for key, value in draft.items()
            if key not in {"content_stage", "last_checked_kind", "last_human_reviewed"}
        }
        promoted["review_status"] = "reviewed"
        errors = module.provenance_errors(sid, promoted)
        self.assertTrue(
            any("promoted vat source needs an ISO last_human_reviewed date" in error for error in errors),
            errors,
        )
        self.assertEqual(
            module.provenance_errors(sid, dict(promoted, last_human_reviewed="2026-10-01")), []
        )
        # No current register entry trips the promotion rule: every extension
        # family entry is still draft_only.
        for current_sid, source in self.sources.items():
            with self.subTest(source_id=current_sid):
                self.assertFalse(
                    [error for error in module.provenance_errors(current_sid, source) if "promoted" in error]
                )

    def test_draft_register_entry_with_review_date_fails_validation(self):
        import tempfile

        module = self._register_module()
        source = dict(self.sources["bd_vat_kor_conditions"])
        source["last_human_reviewed"] = "2026-10-02"
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / ".claude-plugin").mkdir()
            snapshot = root / source["snapshot_path"]
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("source_ids: bd_vat_kor_conditions\n", encoding="utf-8")
            register = root / "skills/nl-tax-shared-resources/source-register.yaml"
            register.write_text(yaml.safe_dump({"sources": [source]}), encoding="utf-8")
            errors, _ = module.validate(str(register))
        self.assertTrue(any("last_human_reviewed: null" in error for error in errors), errors)

    def test_plan_report_never_claims_review_for_draft_sources(self):
        script_path = (
            REPO / "tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py"
        )
        spec = importlib.util.spec_from_file_location("plan_source_refresh_draft", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        draft = self.sources["bd_vat_kor_conditions"]
        record = module.source_report_entry(draft, datetime.now(timezone.utc), PLUGIN, False)
        self.assertIsNone(record["last_human_reviewed"])
        self.assertEqual(record["public_research_checked_at"], str(draft["last_checked"]))
        promoted = {"id": "x", "last_checked": "2026-09-01", "last_human_reviewed": "2026-08-01"}
        self.assertEqual(module.human_review_date(promoted), "2026-08-01")

    def test_new_draft_sources_are_registered_with_metadata(self):
        expected = {
            "bd_vat_kor_conditions": "vat",
            "bd_vat_kor_withdrawal": "vat",
            "bd_zakelijk_login_machtigen": "vat",
            "law_uitvoeringsbeschikking_ob_1968": "vat-adjustments",
            "eu_vat_directive_oss_currency": "vat-cross-border",
            "bd_intl_partial_foreign_liability": "international",
            "bd_annual2026_box1_rates": "years/2026/annual",
            "bd_annual2026_partial_foreign_liability": "years/2026/annual",
        }
        for sid, metadata_dir in expected.items():
            with self.subTest(source_id=sid):
                source = self.sources[sid]
                self.assertEqual(source.get("content_stage"), "draft_only")
                metadata = load_yaml(METADATA / metadata_dir / "_snapshot-metadata.yaml")
                item = metadata["sources"][sid]
                self.assertEqual(item["review_status"], "needs_review")
                self.assertEqual(item["source_url"], source["url"])
        self.assertIn("nl-tax-icp", self.sources["bd_vat_icp"]["mandatory_for"])
        machtigen = self.sources["bd_machtigen_authorization"]["mandatory_for"]
        self.assertIn("nl-tax-international-return", machtigen)
        self.assertIn("nl-tax-annual-return-2026", machtigen)

    def test_staatscourant_sources_are_typed_as_decrees_or_regulations(self):
        decrees = {
            "bd_vat_bua_contribution_policy",
            "bd_vat_car_policy",
            "bd_vat_deduction_policy",
            "bd_vat_deduction_policy_amendment_2025",
            "bd_vat_deduction_policy_amendment_2026",
        }
        for sid, source in self.sources.items():
            if "zoek.officielebekendmakingen.nl" not in source.get("url", ""):
                continue
            with self.subTest(source_id=sid):
                expected = "official_doctrine" if sid in decrees else "law"
                self.assertEqual(source["source_type"], expected)
                self.assertIn("Stcrt.", source["title"])

    def test_domain_allowlists_agree(self):
        scripts = REPO / "tools/nl_tax_agent_skills/source_maintenance/scripts"
        domains = []
        for name in ("validate_source_register.py", "plan_source_refresh.py"):
            spec = importlib.util.spec_from_file_location(f"allow_{name[:-3]}", scripts / name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            domains.append(module.ALLOWED_DOMAINS)
        self.assertEqual(domains[0], domains[1])
        allowlist_doc = (
            REPO / "tools/nl_tax_agent_skills/source_maintenance/reference/official-domain-allowlist.md"
        ).read_text(encoding="utf-8")
        for domain in sorted(
            {source["url"].split("/")[2] for source in self.sources.values()}
            - {"belastingdienst.nl"}
        ):
            with self.subTest(domain=domain):
                self.assertIn(domain, domains[0])
                self.assertIn(f"`{domain}`", allowlist_doc)

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
