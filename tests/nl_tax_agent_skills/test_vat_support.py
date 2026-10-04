#!/usr/bin/env python3
"""VAT return arithmetic, period isolation, draft-source and workpack regressions."""

import copy
import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import date
from datetime import datetime, timezone

import yaml


REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "plugins/nl-tax-agent-skills"


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VAT = load("tools/nl_tax_agent_skills/vat/validate_vat.py", "vat_grader_test")
MAP = load("tools/nl_tax_agent_skills/field_mapper/validate_field_map.py", "vat_map_grader_test")
RENDER = load("tools/nl_tax_agent_skills/field_mapper/render_field_map.py", "vat_render_test")
SAMPLES = load("tests/nl_tax_agent_skills/workpack_samples.py", "vat_samples_test")
WORKPACK = SAMPLES.load_grader()
GATE = load("tools/nl_tax_agent_skills/source_maintenance/scripts/validate_supported_workflows.py", "vat_workflow_gate_test")
KNOWLEDGE = load("tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py", "vat_knowledge_gate_test")
REFRESH = load("tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py", "vat_refresh_report_test")


def vat_map(correction=False):
    values = {fid: 0 for fid in VAT.LIABILITY_IDS}
    values.update({"vat.1a.turnover": 10000, "vat.1a.vat": 2100,
                   "vat.4b.turnover": 1000, "vat.4b.vat": 210,
                   "vat.5a.vat": 2310, "vat.5b.vat": 735, "vat.total.balance": 1575})
    if correction:
        values.update({"vat.correction.previous_balance": 1450, "vat.correction.delta": 125})
    return {
        "field_map_version": "1.1", "workflow": "vat_correction" if correction else "vat_return",
        "tax_year": 2026, "period": "Q3", "created_at": "2026-10-02T08:00:00Z",
        "updated_at": "2026-10-02T08:00:00Z", "readiness": "draft",
        "check_performed_by": "checked_by_agent", "missing_fields": [],
        "user_chat_values_index": [],
        "notes": ["Source-content review remains open."]
        + (["vat_correction_route: suppletie"] if correction else []),
        "fields": [{"field_id": fid, "label": fid, "value": amount,
                    "entry_mode": "internal_routing" if fid in VAT.INTERNAL_IDS else "manual_entry",
                    "source": {"type": "evidence", "evidence_id": "ev_001"},
                    "confidence": 0.9, "manual_review_required": True, "notes": []}
                   for fid, amount in values.items()],
    }


def staged_plugin(root):
    """One explicitly staged source, never labelled human-reviewed."""
    plugin = root / "plugins/nl-tax-agent-skills"
    (plugin / ".codex-plugin").mkdir(parents=True)
    shared = plugin / "skills/nl-tax-shared-resources"
    note = shared / "knowledge/vat/test.md"
    note.parent.mkdir(parents=True)
    note.write_text("# VAT source draft\n\nreview_status: needs_review\nworkflow: all\nsource_id: bd_vat_test\n", encoding="utf-8")
    source = {"id": "bd_vat_test", "url": "https://www.belastingdienst.nl/example",
              "snapshot_path": "skills/nl-tax-shared-resources/knowledge/vat/test.md",
              "content_stage": "draft_only", "workflow_family": "vat", "mandatory_for": ["nl-tax-vat-return", "nl-tax-field-mapper"]}
    register = shared / "source-register.yaml"
    register.write_text(yaml.safe_dump({"sources": [source]}), encoding="utf-8")
    metadata_root = root / "tools/nl_tax_agent_skills/source_maintenance/metadata"
    metadata_path = metadata_root / "vat/_snapshot-metadata.yaml"
    metadata_path.parent.mkdir(parents=True)
    metadata = {"metadata_version": "1.1", "sources": {"bd_vat_test": {
        "reviewed_note_hash_sha256": hashlib.sha256(note.read_bytes()).hexdigest(),
        "reviewed_note_hash_recorded_at": "2026-10-02T08:00:00Z",
        "source_url": source["url"], "review_status": "needs_review"}}}
    metadata_path.write_text(yaml.safe_dump(metadata), encoding="utf-8")
    return plugin, note, source, register, metadata_root, metadata_path


class VatArithmeticTests(unittest.TestCase):
    def test_field_map_validator_accepts_draft_and_refuses_false_ready(self):
        data = vat_map(correction=True)
        errors, warnings = MAP.validate(data)
        self.assertEqual(errors, [])
        data["readiness"] = "review_ready"
        errors, warnings = MAP.validate(data)
        self.assertTrue(any("NOT ready" in error for error in errors))

    def test_sourced_inapplicable_rubrics_can_be_omitted_without_imputation(self):
        data = vat_map()
        zeros = {field["field_id"] for field in data["fields"] if field["value"] == 0}
        data["fields"] = [field for field in data["fields"] if field["field_id"] not in zeros]
        data["notes"] = [f"{VAT.COVERAGE_PREFIX}{fid.split('.')[1]}=not_applicable_sourced; F:ev_001" for fid in zeros]
        self.assertEqual(VAT.validate_map(data), [])
        next(field for field in data["fields"] if field["field_id"] == VAT.LIABILITY_TOTAL_ID)["value"] += 1
        self.assertTrue(any("5a mismatch" in error for error in VAT.validate_map(data)))
        data["notes"] = [note.split(";")[0] for note in data["notes"]]
        self.assertFalse(any("5a mismatch" in error for error in VAT.validate_map(data)), "a status without provenance never supplies a zero")

    def test_eu_purchase_liability_and_deduction_reconcile(self):
        data = vat_map()
        self.assertEqual(VAT.validate_map(data), [])
        data["fields"].append({"field_id": "vat.3b.turnover", "value": 8000})
        self.assertEqual(VAT.validate_map(data), [], "EU sales turnover must not add liability")

    def test_wrong_liability_balance_and_correction_delta_are_rejected(self):
        for fid in ("vat.5a.vat", "vat.total.balance", "vat.correction.delta"):
            data = vat_map(correction=True)
            next(field for field in data["fields"] if field["field_id"] == fid)["value"] += 1
            with self.subTest(field=fid):
                self.assertTrue(any("mismatch" in error for error in VAT.validate_map(data)))

    def test_correction_uses_full_revised_totals_not_delta_as_return(self):
        data = vat_map(correction=True)
        next(field for field in data["fields"] if field["field_id"] == "vat.5a.vat")["value"] = 125
        self.assertTrue(any("5a mismatch" in error for error in VAT.validate_map(data)))

    def test_fabricated_turnover_only_tax_fields_and_ib_rows_are_rejected(self):
        for fid in ("vat.1e.vat", "vat.3a.vat", "vat.3b.vat", "vat.3c.vat", "box1.loon", "vat.5c.balance"):
            data = vat_map()
            data["fields"].append({"field_id": fid, "value": 0})
            with self.subTest(field=fid):
                self.assertTrue(any("Unsupported VAT" in error for error in VAT.validate_map(data)))

    def test_no_rounding_or_zero_imputation_and_finite_values_required(self):
        for amount in (True, float("nan"), float("inf"), 735.49, "735,00"):
            data = vat_map()
            next(field for field in data["fields"] if field["field_id"] == "vat.5b.vat")["value"] = amount
            with self.subTest(value=amount):
                self.assertTrue(any("finite whole-euro" in error for error in VAT.validate_map(data)))
        data = vat_map()
        next(field for field in data["fields"] if field["field_id"] == "vat.4b.vat")["value"] = None
        self.assertFalse(any("5a mismatch" in error for error in VAT.validate_map(data)), "missing must never be treated as zero")

    def test_derived_balance_is_never_a_portal_row(self):
        data = vat_map()
        balance = next(field for field in data["fields"] if field["field_id"] == "vat.total.balance")
        balance["entry_mode"] = "manual_entry"
        self.assertTrue(any("internal_routing" in error for error in VAT.validate_map(data)))
        rendered = RENDER.render(vat_map(correction=True))
        self.assertNotIn("vat.total.balance", rendered)
        self.assertNotIn("vat.correction.delta", rendered)
        self.assertIn("**Period:** Q3", rendered)

    def test_correction_map_declares_one_route_and_only_suppletie_maps_prior_total(self):
        data = vat_map(correction=True)
        self.assertIn("vat_correction_route: suppletie", data["notes"])
        self.assertEqual(VAT.validate_map(data), [])
        data["notes"] = [note for note in data["notes"] if not note.startswith(VAT.ROUTE_PREFIX)]
        self.assertTrue(any("must declare vat_correction_route:" in error for error in VAT.validate_map(data)))
        data["notes"].append("vat_correction_route: next_month")
        self.assertTrue(any("Invalid vat_correction_route:" in error for error in VAT.validate_map(data)))
        data["notes"][-1] = "vat_correction_route: suppletie"
        data["notes"].append("vat_correction_route: next_return")
        self.assertTrue(any("more than one" in error for error in VAT.validate_map(data)))
        for route in ("next_return", "letter", "human_review"):
            data = vat_map(correction=True)
            data["notes"] = ["Source-content review remains open.", f"vat_correction_route: {route}"]
            with self.subTest(route=route):
                self.assertTrue(any("suppletie-only entry row" in error for error in VAT.validate_map(data)))
                data["fields"] = [f for f in data["fields"] if f["field_id"] != VAT.PREVIOUS_BALANCE_ID]
                self.assertFalse(any("suppletie-only" in error for error in VAT.validate_map(data)))
        self.assertEqual(VAT.validate_map(vat_map()), [], "a vat_return map needs no route note")

    def test_suppletie_prior_total_is_an_entry_row_not_internal(self):
        """'Totaalbedrag eerdere btw-aangifte over dit tijdvak' is a real form field."""
        self.assertNotIn("vat.correction.previous_balance", VAT.INTERNAL_IDS)
        self.assertIn("vat.correction.previous_balance", VAT.SUPPLETIE_ENTRY_IDS)
        data = vat_map(correction=True)
        self.assertEqual(VAT.validate_map(data), [])
        prior = next(field for field in data["fields"] if field["field_id"] == "vat.correction.previous_balance")
        self.assertEqual(prior["entry_mode"], "manual_entry")
        prior["entry_mode"] = "internal_routing"
        self.assertTrue(any("never mark it internal_routing" in error for error in VAT.validate_map(data)))
        data = vat_map()
        data["fields"].append({"field_id": "vat.correction.previous_balance", "value": 1450, "entry_mode": "manual_entry"})
        self.assertTrue(any("Unsupported VAT" in error for error in VAT.validate_map(data)), "a return map never carries the suppletie prior total")

    def test_period_names_and_resume_identity(self):
        for year in (2025, 2026):
            for period in ("Q1", "Q4", "M01", "M12", "Y"):
                self.assertEqual(VAT.parse_resume_identity(f"vat_{year}_{period}"), ("vat_return", year, period))
                self.assertNotEqual(VAT.workpack_path("vat_return", year, period), VAT.workpack_path("vat_correction", year, period))
        for workflow in ("vat_2027_Q1", "vat_2026_M00", "vat_2026_M13", "vat_2026_Q5", "vat_2026_../Q1",
                         "vat_\uff12\uff10\uff12\uff16_Q1", "vat_correction_\u0662\u0660\u0662\u0665_Q1"):
            self.assertIsNone(VAT.parse_resume_identity(workflow))
        self.assertNotEqual(VAT.workpack_path("vat_return", 2026, "Q1"), VAT.workpack_path("vat_return", 2026, "Q2"))


class VatCoverageAuditTests(unittest.TestCase):
    ALL = [str(rubric) for rubric in VAT.POLICY["turnover_rubrics"]] + ["5a", "5b"]

    def notes(self, **overrides):
        notes = {rubric: f"{VAT.COVERAGE_PREFIX}{rubric}=not_applicable_sourced; F:ev_001" for rubric in self.ALL}
        notes.update(overrides)
        return list(notes.values())

    def test_provenance_must_open_the_note(self):
        coverage = VAT.rubric_coverage([f"{VAT.COVERAGE_PREFIX}1b=not_applicable_sourced; TODO: U: ask user"])
        self.assertEqual(coverage["1b"], ("not_applicable_sourced", False))
        for provenance in ('F:ev_001', 'F:ev_001 (ledger p.2)', 'U:"no low-rate sales" (2026-10-02)'):
            with self.subTest(provenance=provenance):
                coverage = VAT.rubric_coverage([f"{VAT.COVERAGE_PREFIX}1b=not_applicable_sourced; {provenance}"])
                self.assertEqual(coverage["1b"], ("not_applicable_sourced", True))
        blockers = VAT.coverage_blockers(self.notes(**{"1b": f"{VAT.COVERAGE_PREFIX}1b=not_applicable_sourced; see U: later"}))
        self.assertTrue(any("no provenance: 1b" in blocker for blocker in blockers))

    def test_duplicate_declarations_are_reported_and_never_supply_a_zero(self):
        notes = self.notes() + [f"{VAT.COVERAGE_PREFIX}1a=applicable_mapped; F:ev_002"]
        self.assertEqual(VAT.rubric_coverage(notes)["1a"], ("duplicate", False))
        blockers = VAT.coverage_blockers(notes)
        self.assertTrue(any("declared more than once: 1a" in blocker for blocker in blockers))
        self.assertFalse(any("unresolved" in blocker for blocker in blockers))

    def test_declarations_are_cross_checked_against_mapped_fields(self):
        fields = [{"field_id": "vat.1a.turnover"}, {"field_id": "vat.1a.vat"}, {"field_id": "vat.5a.vat"}]
        notes = self.notes(**{"1a": f"{VAT.COVERAGE_PREFIX}1a=applicable_mapped; F:ev_001",
                              "5a": f"{VAT.COVERAGE_PREFIX}5a=applicable_mapped; F:ev_001",
                              "5b": f"{VAT.COVERAGE_PREFIX}5b=applicable_mapped; F:ev_001"})
        self.assertEqual(VAT.coverage_blockers(notes), [], "without fields only the declarations are audited")
        blockers = VAT.coverage_blockers(notes, fields)
        self.assertTrue(any("applicable_mapped has no mapped field: 5b" in blocker for blocker in blockers))
        self.assertEqual(VAT.coverage_blockers(notes, fields, missing_fields=[{"field_id": "vat.5b.vat"}]), [])
        fields.append({"field_id": "vat.1b.turnover"})
        blockers = VAT.coverage_blockers(notes, fields, missing_fields=[{"field_id": "vat.5b.vat"}])
        self.assertTrue(any("not_applicable_sourced also has a mapped field: 1b" in blocker for blocker in blockers))


class VatCorrectionContentTests(unittest.TestCase):
    """Decision D1 and the suppletie explanation stay consistent across owners."""

    KNOWLEDGE = PLUGIN / "skills/nl-tax-shared-resources/knowledge/vat"

    def test_corrections_note_keeps_sourced_branches(self):
        text = (self.KNOWLEDGE / "corrections.md").read_text(encoding="utf-8")
        for phrase in ("Totaalbedrag eerdere btw-aangifte over dit tijdvak",
                       "betalingskenmerk",
                       "never prepared under the `Y` period token",
                       "Central Liaison Office",
                       "within six weeks",
                       "may not be offset in the next return"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_whole_year_suppletie_is_never_prepared_under_y(self):
        for relative in ("nl-tax-vat-correction/SKILL.md",
                         "nl-tax-vat-correction/reference/vat-correction-flow.md",
                         "nl-tax-field-mapper/reference/vat-field-map.md"):
            with self.subTest(file=relative):
                text = " ".join((PLUGIN / "skills" / relative).read_text(encoding="utf-8").split())
                self.assertIn("whole-year suppletie", text)
                self.assertIn("`Y`", text)
                self.assertNotIn("Year-scope corrections need a complete", text)
                self.assertNotIn("until the sources and exact form are established", text)


class VatDraftSourceGateTests(unittest.TestCase):
    def test_public_source_research_is_never_reported_as_human_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin, note, source, register, metadata_root, metadata_path = staged_plugin(Path(tmp))
            source["last_checked"] = "2026-10-02"
            report = REFRESH.source_report_entry(source, datetime(2026, 10, 2, tzinfo=timezone.utc), str(plugin), False)
            self.assertIsNone(report["last_human_reviewed"])
            self.assertEqual(report["public_research_checked_at"], "2026-10-02")

    def test_staging_allows_unreviewed_metadata_only_with_explicit_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin, note, source, register, metadata_root, metadata_path = staged_plugin(Path(tmp))
            self.assertEqual(KNOWLEDGE.collect_snapshot_metadata_errors([source], str(plugin), str(metadata_root)), [])
            source.pop("content_stage")
            errors = KNOWLEDGE.collect_snapshot_metadata_errors([source], str(plugin), str(metadata_root))
            self.assertTrue(any("not reviewed" in error[1] for error in errors))

    def test_draft_source_review_gate_never_promotes_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin, note, source, register, metadata_root, metadata_path = staged_plugin(Path(tmp))
            self.assertTrue(VAT.review_blockers(plugin, "vat_return"))
            self.assertEqual(VAT.review_blockers(plugin, "annual_return"), [])
            source.pop("content_stage")
            register.write_text(yaml.safe_dump({"sources": [source]}), encoding="utf-8")
            self.assertTrue(VAT.review_blockers(plugin, "vat_return"), "deleting stage alone is not human review")
            note.write_text(note.read_text().replace("needs_review", "reviewed"), encoding="utf-8")
            self.assertTrue(VAT.review_blockers(plugin, "vat_return"), "changing note alone cannot bypass hash/metadata")

    def test_workflow_gate_requires_draft_ceiling_and_period_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin, note, source, register, metadata_root, metadata_path = staged_plugin(Path(tmp))
            workflow = {"id": "vat_2026", "workflow": "vat_return", "tax_year": 2026,
                        "status": "draft_only", "maximum_readiness": "draft", "may_prepare_workpack": True,
                        "profile_candidates": ["vat_2026_<period>"],
                        "knowledge_dirs": ["skills/nl-tax-shared-resources/knowledge/vat"],
                        "required_source_ids": ["bd_vat_test"],
                        "output_paths": ["workspace/nl-tax-vat-2026-{period}-workpack.md"]}
            config = {"last_reviewed": date.today().isoformat(), "draft_only_workflows": [workflow]}
            config_path = plugin / "supported-workflows.yaml"
            config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
            self.assertEqual(GATE.validate(str(config_path), str(register))[0], [])
            workflow["maximum_readiness"] = "review_ready"
            workflow["output_paths"] = ["workspace/nl-tax-vat-2026-workpack.md"]
            config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
            errors = GATE.validate(str(config_path), str(register))[0]
            self.assertTrue(any("maximum_readiness" in error for error in errors))
            self.assertTrue(any("one workpack file" in error for error in errors))

    def test_active_workflow_cannot_use_a_staged_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin, note, source, register, metadata_root, metadata_path = staged_plugin(Path(tmp))
            workflow = {"id": "vat_2026", "workflow": "vat_return", "tax_year": 2026,
                        "status": "active", "profile_candidates": ["vat_2026_<period>"],
                        "knowledge_dirs": ["skills/nl-tax-shared-resources/knowledge/vat"],
                        "required_source_ids": ["bd_vat_test"],
                        "output_paths": ["workspace/nl-tax-vat-2026-{period}-workpack.md"]}
            config_path = plugin / "supported-workflows.yaml"
            config_path.write_text(yaml.safe_dump({"last_reviewed": date.today().isoformat(), "active_workflows": [workflow]}), encoding="utf-8")
            self.assertTrue(any("active workflow cannot use draft-only" in error for error in GATE.validate(str(config_path), str(register))[0]))

    def test_family_rejects_vat_source_for_ib_even_after_future_review(self):
        source = {"workflow_family": "vat", "mandatory_for": ["nl-tax-field-mapper"]}
        self.assertFalse(GATE.source_scope_matches(source, "annual_return", 2025)[0])
        self.assertFalse(GATE.source_scope_matches(source, "provisional_assessment", 2026)[0])
        self.assertTrue(GATE.source_scope_matches(source, "vat_return", 2025)[0])

    def test_staged_sources_require_a_declared_draft_workflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin, note, source, register, metadata_root, metadata_path = staged_plugin(Path(tmp))
            config_path = plugin / "supported-workflows.yaml"
            config_path.write_text(yaml.safe_dump({"last_reviewed": date.today().isoformat()}), encoding="utf-8")
            self.assertTrue(any("no declared draft workflow owner" in error for error in GATE.validate(str(config_path), str(register))[0]))


class VatWorkpackTests(unittest.TestCase):
    def sample(self, kind="vat", field_map=None, **kwargs):
        return SAMPLES.build_workpack(kind, sources=(),
            documents=(("ev_001", "VAT control ledger Q3 2026", "vat_summary", "2026", "taxpayer", "summary", "explicit reviewed ledger totals and zero categories", "extracted"),),
            field_map=field_map, **kwargs)

    def test_draft_workpack_and_confirmation_are_accepted(self):
        report = WORKPACK.validate_workpack_text(self.sample(field_map=vat_map()), expect_saved=True)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.kind, "vat")

    def test_period_mismatch_is_rejected(self):
        data = vat_map()
        data["period"] = "Q2"
        report = WORKPACK.validate_workpack_text(self.sample(field_map=data))
        self.assertTrue(any("VAT period must match" in error for error in report.errors))

    def test_draft_source_workpack_cannot_be_declared_review_ready(self):
        report = WORKPACK.validate_workpack_text(self.sample(readiness="review_ready", field_map=vat_map()))
        self.assertTrue(any("VAT review_ready is blocked" in error for error in report.errors))

    def test_changed_fact_keeps_map_and_checklist_stale(self):
        # Draft-only VAT content never carries a manual-entry checklist, so the
        # stale marker is exercised on the map sections only.
        data = vat_map()
        text = self.sample(field_map=data, stale=("deductible input VAT", "2026-10-02"))
        self.assertEqual(WORKPACK.validate_workpack_text(text).errors, [])
        text = text.replace(SAMPLES.stale_marker("deductible input VAT", "2026-10-02"), "", 1)
        self.assertTrue(any("must carry the line" in error for error in WORKPACK.validate_workpack_text(text).errors))

    def test_save_consent_and_filename_match_the_period(self):
        text = self.sample(save_consent="not_given")
        self.assertTrue(any("save_consent: given" in error for error in WORKPACK.validate_workpack_text(text, expect_saved=True).errors))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nl-tax-vat-2026-Q2-workpack.md"
            path.write_text(self.sample(), encoding="utf-8")
            self.assertTrue(any("filename must match" in error for error in WORKPACK.validate_workpack_file(path).errors))


if __name__ == "__main__":
    unittest.main()
