#!/usr/bin/env python3
"""Tests for the 0.4 workpack grader (tools/nl_tax_agent_skills/workpack).

Fixtures are built from the real plugin templates by ``workpack_samples.py``
and broken one contract at a time.
"""

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml


HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("workpack_samples_for_grader", HERE / "workpack_samples.py")
samples = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(samples)

REPO_ROOT = samples.REPO_ROOT
GRADER_PATH = samples.GRADER_PATH


class WorkpackGraderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grader = samples.load_grader()

    def grade(self, text, kind=None, expect_saved=True):
        return self.grader.validate_workpack_text(
            text, expected_kind=kind, expect_saved=expect_saved
        )

    def assertValid(self, text, kind=None, expect_saved=True):
        report = self.grade(text, kind, expect_saved)
        self.assertEqual(report.errors, [], "\n".join(report.errors))
        return report

    def assertError(self, text, fragment, kind=None, expect_saved=True):
        report = self.grade(text, kind, expect_saved)
        self.assertTrue(
            any(fragment in error for error in report.errors),
            f"expected an error containing {fragment!r}; got {report.errors}",
        )
        return report


class ValidSamplesTests(WorkpackGraderTestCase):
    def test_annual_draft_and_review_ready_samples_pass(self):
        self.assertValid(samples.build_workpack("annual"), "annual")
        report = self.assertValid(
            samples.build_workpack(
                "annual", readiness="review_ready", field_map=samples.ANNUAL_FIELD_MAP
            ),
            "annual",
        )
        self.assertEqual(report.field_map_state, "mapped")
        self.assertEqual(report.kind, "annual")

    def test_every_provisional_subflow_sample_passes(self):
        for subflow in ("request", "change", "review", "stopzetten"):
            with self.subTest(subflow=subflow):
                report = self.assertValid(
                    samples.build_workpack(
                        "provisional", workflow=f"provisional_2026_{subflow}"
                    ),
                    "provisional",
                )
                self.assertEqual(report.field_map_state, "not_yet_mapped")

    def test_mapped_samples_also_pass_the_field_map_grader(self):
        field_map_grader = samples.load_field_map_grader()
        for kind, field_map in (
            ("annual", samples.ANNUAL_FIELD_MAP),
            ("provisional", samples.PROVISIONAL_FIELD_MAP),
        ):
            with self.subTest(kind=kind):
                report = self.assertValid(
                    samples.build_workpack(kind, field_map=field_map), kind
                )
                errors, _ = field_map_grader.validate(report.field_map)
                self.assertEqual(errors, [])

    def test_conversation_only_workpack_records_not_given(self):
        text = samples.build_workpack("annual", save_consent="not_given")
        self.assertValid(text, "annual", expect_saved=False)
        self.assertError(text, "save_consent: given", "annual", expect_saved=True)

    def test_kind_is_inferred_from_appendix_a(self):
        report = self.assertValid(samples.build_workpack("provisional"))
        self.assertEqual(report.kind, "provisional")


class StructureTests(WorkpackGraderTestCase):
    def test_required_headings_come_from_the_templates(self):
        plugin_root = str(samples.PLUGIN_ROOT.resolve())
        for kind, template in samples.TEMPLATES.items():
            with self.subTest(kind=kind):
                headings = [
                    line[3:].strip()
                    for line in template.read_text(encoding="utf-8").splitlines()
                    if line.startswith("## ")
                ]
                specs = [display for display, _ in self.grader.template_headings(plugin_root, kind)]
                self.assertEqual(specs, headings)
                for required in (
                    "How to use this file",
                    "Taxpayer profile summary",
                    "Documents and sources",
                    "Sources used",
                    "Open questions",
                    "Missing information",
                    "Assumptions",
                    "Field map summary",
                    "Manual-entry checklist",
                    "Appendix A — Resume record",
                    "Appendix B — Field map",
                ):
                    self.assertIn(required, headings)

    def test_missing_section_is_rejected(self):
        text = samples.build_workpack("annual").replace(
            "## Missing information\n", "## Gaps\n", 1
        )
        self.assertError(text, "missing required section '## Missing information'")

    def test_out_of_order_section_is_rejected(self):
        text = samples.build_workpack("annual")
        start = text.index("## Scope\n")
        end = text.index("## Unsupported-case checks\n")
        scope = text[start:end]
        text = text[:start] + text[end:]
        insert_at = text.index("## Not submission advice\n")
        text = text[:insert_at] + scope + text[insert_at:]
        self.assertError(text, "out of order")

    def test_duplicate_section_is_rejected(self):
        text = samples.build_workpack("annual").replace(
            "## Assumptions\n", "## Assumptions\n\nNone.\n\n## Assumptions\n", 1
        )
        self.assertError(text, "appears 2 times")

    def test_dash_variants_in_appendix_headings_are_accepted(self):
        text = samples.build_workpack("annual").replace(
            "## Appendix A — Resume record", "## Appendix A - Resume record"
        )
        self.assertValid(text, "annual")

    def test_headings_inside_fences_do_not_split_sections(self):
        text = samples.build_workpack("annual").replace(
            "## Assumptions\n",
            "## Assumptions\n\n```text\n## Not a section\n```\n",
            1,
        )
        self.assertValid(text, "annual")

    def test_status_banner_must_match_readiness(self):
        draft = samples.build_workpack("annual")
        self.assertError(
            draft.replace("STATUS: DRAFT —", "STATUS: COMPLETE DRAFT FOR REVIEW —", 1),
            "readiness is draft but the STATUS banner is not DRAFT",
        )
        ready = samples.build_workpack("annual", readiness="review_ready")
        self.assertError(
            ready.replace("COMPLETE DRAFT FOR REVIEW", "DRAFT — 1 open section(s)", 1),
            "readiness is review_ready but the STATUS banner",
        )
        self.assertError(draft.replace("not for filing", "ready", 1), "not for filing")

    def test_unfilled_template_banner_is_rejected(self):
        template = samples.TEMPLATES["annual"].read_text(encoding="utf-8")
        banner = next(line for line in template.splitlines() if "STATUS:" in line)
        text = samples.build_workpack("annual")
        text = "\n".join(
            banner if line.startswith("> **STATUS:") else line for line in text.split("\n")
        )
        self.assertError(text, "both template alternatives")

    def test_provisional_subflow_heading_matches_workflow(self):
        text = samples.build_workpack("provisional", workflow="provisional_2026_change")
        self.assertError(
            text.replace("## Subflow: change", "## Subflow: request", 1),
            "does not match Appendix A workflow provisional_2026_change",
        )


class ResumeRecordTests(WorkpackGraderTestCase):
    def test_missing_and_unknown_keys_are_rejected(self):
        self.assertError(
            samples.build_workpack(
                "annual", record_overrides={"readiness": samples.DELETE}
            ),
            "missing key(s): readiness",
        )
        self.assertError(
            samples.build_workpack(
                "annual", record_overrides={"fiscaal_loon": 48250}
            ),
            "facts never live in the resume record",
        )

    def test_format_and_version(self):
        self.assertError(
            samples.build_workpack(
                "annual", record_overrides={"workpack_format": "nl-tax-ledger"}
            ),
            "workpack_format must be 'nl-tax-workpack'",
        )
        self.assertError(
            samples.build_workpack("annual", record_overrides={"workpack_version": "3.0"}),
            'workpack_version must be "2.x"',
        )
        unquoted = samples.build_workpack("annual").replace(
            "workpack_version: '2.0'", "workpack_version: 2.0"
        )
        report = self.assertValid(unquoted, "annual")
        self.assertTrue(any("quoted string" in warning for warning in report.warnings))

    def test_workflow_and_tax_year_are_paired(self):
        self.assertError(
            samples.build_workpack("annual", record_overrides={"tax_year": 2026}),
            "tax_year must be 2025",
        )
        self.assertError(
            samples.build_workpack("provisional", record_overrides={"tax_year": 2025}),
            "tax_year must be 2026",
        )
        provisional = samples.build_workpack("provisional")
        self.assertError(provisional, "does not belong in the annual workpack", kind="annual")

    def test_section_keys_are_exact_for_the_workflow(self):
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses["box1_home"] = "complete"
        self.assertError(
            samples.build_workpack("annual", statuses=statuses),
            "not used by annual_2025: box1_home",
        )
        statuses = samples.default_statuses("annual", "annual_2025")
        del statuses["box3_actual"]
        self.assertError(
            samples.build_workpack("annual", statuses=statuses),
            "sections missing key(s) for annual_2025: box3_actual",
        )
        request = samples.default_statuses("provisional", "provisional_2026_request")
        request["baseline"] = "complete"
        self.assertError(
            samples.build_workpack("provisional", statuses=request),
            "not used by provisional_2026_request: baseline",
        )
        stopzetten = samples.default_statuses("provisional", "provisional_2026_stopzetten")
        self.assertEqual(set(stopzetten), {"baseline", "stopzetten_direction", "confirm"})

    def test_change_may_keep_the_stopzetten_redirect_section(self):
        statuses = samples.default_statuses("provisional", "provisional_2026_change")
        statuses["stopzetten_direction"] = "complete"
        statuses["baseline"] = "in_progress"
        self.assertValid(
            samples.build_workpack(
                "provisional", workflow="provisional_2026_change", statuses=statuses
            ),
            "provisional",
        )

    def test_status_and_readiness_vocabulary(self):
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses["box1"] = "done"
        self.assertError(
            samples.build_workpack("annual", statuses=statuses),
            "sections.box1.status must be one of",
        )
        self.assertError(
            samples.build_workpack("annual", record_overrides={"readiness": "ready"}),
            "readiness must be one of",
        )
        self.assertError(
            samples.build_workpack("annual", record_overrides={"save_consent": "yes"}),
            "save_consent must be one of",
        )
        self.assertError(
            samples.build_workpack(
                "annual", record_overrides={"generation_confirmed": "no"}
            ),
            "generation_confirmed must be true or false",
        )

    def test_review_ready_requires_every_section_done_and_no_blocker(self):
        statuses = samples.default_statuses("annual", "annual_2025", "complete")
        statuses["box3_actual"] = "in_progress"
        self.assertError(
            samples.build_workpack("annual", readiness="review_ready", statuses=statuses),
            "not done: box3_actual",
        )
        statuses = samples.default_statuses("annual", "annual_2025", "complete")
        blocking = samples.build_workpack(
            "annual",
            readiness="review_ready",
            statuses=statuses,
            open_questions={"deductions": ["Q001"]},
            questions=(("Q001", "deductions", "Any gifts?", "yes"),),
        )
        self.assertError(blocking, "blocking open question(s): Q001")
        nonblocking = blocking.replace("| Any gifts? | yes |", "| Any gifts? | no |")
        self.assertValid(nonblocking, "annual")

    def test_open_question_ids_match_the_open_questions_table(self):
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses["box1"] = "deferred"
        self.assertError(
            samples.build_workpack(
                "annual", statuses=statuses, open_questions={"box1": ["Q001"]}
            ),
            "Q001 is open in Appendix A but has no row",
        )
        self.assertError(
            samples.build_workpack(
                "annual", questions=(("Q002", "box1", "Second employer?", "yes"),)
            ),
            "row Q002 is not listed in any Appendix A open list",
        )
        self.assertError(
            samples.build_workpack(
                "annual",
                statuses=statuses,
                open_questions={"box1": ["Q003"]},
                questions=(("Q003", "box2", "Shares?", "yes"),),
            ),
            "Q003 belongs to section 'box2'",
        )
        self.assertError(
            samples.build_workpack("annual", statuses=statuses),
            "sections.box1 is deferred but lists no open question",
        )

    def test_generation_confirmation_tracks_the_confirm_section(self):
        statuses = samples.default_statuses("annual", "annual_2025")
        self.assertError(
            samples.build_workpack(
                "annual", statuses=statuses, generation_confirmed=True
            ),
            "generation_confirmed is true but sections.confirm is not complete",
        )
        statuses["confirm"] = "complete"
        self.assertError(
            samples.build_workpack(
                "annual", statuses=statuses, generation_confirmed=False
            ),
            "sections.confirm is complete but generation_confirmed is false",
        )

    def test_queued_workflow_lives_only_in_the_annual_record(self):
        self.assertValid(
            samples.build_workpack("annual", queued_workflow="provisional_2026_change"),
            "annual",
        )
        self.assertError(
            samples.build_workpack("annual", queued_workflow="annual_2026"),
            "queued_workflow must be null or a provisional_2026_<subflow> value",
        )
        self.assertError(
            samples.build_workpack("provisional", queued_workflow="provisional_2026_change"),
            "queued_workflow must be null in a provisional workpack",
        )

    def test_saved_workpack_needs_ordered_timestamps(self):
        self.assertError(
            samples.build_workpack("annual", created_at=""),
            "created_at must be set in a saved workpack",
        )
        self.assertError(
            samples.build_workpack(
                "annual",
                created_at="2026-09-21T10:00:00Z",
                updated_at="2026-09-20T10:00:00Z",
            ),
            "updated_at is earlier than created_at",
        )
        self.assertError(
            samples.build_workpack("annual", updated_at="yesterday"),
            "updated_at must be an ISO 8601 timestamp",
        )


class SourcesAndDocumentsTests(WorkpackGraderTestCase):
    def test_sources_used_must_equal_sources_loaded(self):
        text = samples.build_workpack("annual").replace(
            "- bd_jaaropgaaf_fields_2025\n", "", 1
        )
        self.assertError(text, "must equal Appendix A sources_loaded")

    def test_sources_used_must_be_registered_and_workflow_scoped(self):
        self.assertError(
            samples.build_workpack("annual", sources=("bd_made_up_2025",)),
            "unregistered source_id bd_made_up_2025",
        )
        self.assertError(
            samples.build_workpack(
                "annual", sources=("bd_box1_rates_2025", "bd_box3_2026_provisional")
            ),
            "annual workpack lists bd_box3_2026_provisional, a provisional_assessment source",
        )
        self.assertError(
            samples.build_workpack(
                "provisional", sources=("bd_box1_rates_2026", "bd_box3_2025_calc")
            ),
            "provisional workpack lists bd_box3_2025_calc, a annual_return source",
        )
        text = samples.build_workpack("annual").replace(
            "- bd_box1_rates_2025\n", "- [source_id]\n- bd_box1_rates_2025\n", 1
        )
        self.assertError(text, "entry is not a source_id")

    def test_every_evidence_reference_has_a_documents_row(self):
        text = samples.build_workpack("annual").replace(
            "## Assumptions\n",
            "## Assumptions\n\nA001 rests on F:ev_002.\n",
            1,
        )
        self.assertError(text, "ev_002 is referenced but has no row")
        field_map = yaml.safe_load(yaml.safe_dump(samples.ANNUAL_FIELD_MAP))
        field_map["fields"][0]["source"]["evidence_id"] = "ev_007"
        self.assertError(
            samples.build_workpack("annual", field_map=field_map),
            "ev_007 is referenced but has no row",
        )
        field_map["fields"][0]["source"]["evidence_id"] = "jaaropgaaf-2025"
        self.assertError(
            samples.build_workpack("annual", field_map=field_map),
            "must name an ev_NNN row",
        )

    def test_documents_rows_use_the_status_vocabulary_and_no_hashes(self):
        row = list(samples.ANNUAL_DOCUMENTS[0])
        row[-1] = "reviewed"
        self.assertError(
            samples.build_workpack("annual", documents=(tuple(row),)),
            "status must be 'extracted' or 'needs review'",
        )
        row = list(samples.ANNUAL_DOCUMENTS[0])
        row[6] = "sha256 " + "a" * 64
        self.assertError(
            samples.build_workpack("annual", documents=(tuple(row),)),
            "contains a file hash",
        )
        duplicate = samples.ANNUAL_DOCUMENTS + samples.ANNUAL_DOCUMENTS
        self.assertError(
            samples.build_workpack("annual", documents=duplicate), "duplicate row ev_001"
        )
        needs_review = list(samples.ANNUAL_DOCUMENTS[0])
        needs_review[-1] = "needs review"
        self.assertValid(samples.build_workpack("annual", documents=(tuple(needs_review),)), "annual")


class PrivacyAndSeparationTests(WorkpackGraderTestCase):
    def _with_note(self, kind, note, **kwargs):
        return samples.build_workpack(kind, **kwargs).replace(
            "## Assumptions\n", f"## Assumptions\n\n{note}\n", 1
        )

    def test_bsn_like_numbers_are_rejected(self):
        self.assertError(self._with_note("annual", "BSN 123456782"), "BSN-like")
        self.assertError(self._with_note("annual", "BSN 1234.56.782"), "BSN-like")
        # Decimal amounts and longer digit runs are not BSN-like.
        self.assertValid(self._with_note("annual", "EUR 123456789.00 and 0612345678"), "annual")

    def test_ibans_are_rejected_but_masked_ones_pass(self):
        self.assertError(self._with_note("annual", "Refund to NL91 ABNA 0417 1643 00"), "IBAN-like")
        self.assertError(self._with_note("annual", "Account NL91ABNA0417164300"), "IBAN-like")
        self.assertError(
            self._with_note("provisional", "German account DE89370400440532013000"), "IBAN-like"
        )
        self.assertValid(self._with_note("annual", "Refund to NL91 ABNA **** **** 00"), "annual")

    def test_workpacks_never_name_the_other_workflow_file(self):
        self.assertError(
            self._with_note("annual", "See workspace/nl-tax-provisional-2026-workpack.md"),
            "mentions the provisional workpack path",
        )
        self.assertError(
            self._with_note("provisional", "See workspace/nl-tax-annual-2025-workpack.md"),
            "mentions the annual workpack path",
        )

    def test_provisional_workpack_never_collects_werkelijk_rendement(self):
        self.assertError(
            self._with_note("provisional", "Werkelijk rendement 2026: EUR 1,200 -- Src: U"),
            "fictitious-only",
        )
        self.assertError(
            self._with_note("provisional", "Actual return inputs requested."), "fictitious-only"
        )
        allowed = (
            "Werkelijk rendement may become relevant when filing the annual 2026 return in 2027."
        )
        self.assertValid(self._with_note("provisional", allowed), "provisional")
        text = samples.build_workpack("provisional").replace(
            "> Werkelijk rendement is not part of provisional 2026.", "", 1
        )
        self.assertError(text, "must include the note")
        # Review and stopzetten may carry a Box 3 section marked N/A.
        review = samples.build_workpack(
            "provisional", workflow="provisional_2026_review"
        ).replace("> Werkelijk rendement is not part of provisional 2026.", "", 1)
        self.assertValid(review, "provisional")

    def test_annual_workpack_may_collect_actual_return(self):
        self.assertValid(
            self._with_note("annual", "Werkelijk rendement data supplied: see Box 3 notes."),
            "annual",
        )


class FieldMapAppendixTests(WorkpackGraderTestCase):
    def test_appendix_b_is_placeholder_or_one_yaml_block(self):
        mapped = samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP)
        self.assertError(
            mapped.replace("## Appendix B — Field map\n", "## Appendix B — Field map\n\nnot yet mapped\n", 1),
            "holds both a field map and the 'not yet mapped' line",
        )
        block_start = mapped.index("## Appendix B — Field map")
        appendix = mapped[block_start:]
        doubled = mapped + "\n" + appendix[appendix.index("```yaml"):]
        self.assertError(doubled, "exactly one fenced yaml block (found 2)")
        empty = samples.build_workpack("annual").replace("\nnot yet mapped\n", "\n\n")
        self.assertError(empty, "must hold the literal line 'not yet mapped'")

    def test_review_and_stopzetten_never_hold_a_field_map(self):
        for subflow in ("review", "stopzetten"):
            with self.subTest(subflow=subflow):
                text = samples.build_workpack(
                    "provisional",
                    workflow=f"provisional_2026_{subflow}",
                    field_map=samples.PROVISIONAL_FIELD_MAP,
                )
                self.assertError(text, "never holds a field map")

    def test_field_map_workflow_year_and_readiness_match_the_workpack(self):
        self.assertError(
            samples.build_workpack("provisional", field_map=samples.ANNUAL_FIELD_MAP),
            "Appendix B workflow must be provisional_assessment",
        )
        wrong_year = dict(samples.ANNUAL_FIELD_MAP, tax_year=2026)
        self.assertError(
            samples.build_workpack("annual", field_map=wrong_year),
            "Appendix B tax_year must be 2025",
        )
        promoted = dict(samples.ANNUAL_FIELD_MAP, readiness="review_ready")
        self.assertError(
            samples.build_workpack("annual", field_map=promoted),
            "nothing promotes a draft",
        )

    def test_field_map_summary_agrees_with_appendix_b(self):
        mapped = samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP)
        summary_start = mapped.index("## Field map summary")
        summary_end = mapped.index("## Manual-entry checklist")
        stale = mapped[:summary_start] + "## Field map summary\n\nnot yet mapped\n\n" + mapped[summary_end:]
        self.assertError(stale, "still reads not yet mapped")
        unmapped = samples.build_workpack("annual")
        shown = unmapped.replace(
            "## Field map summary\n\nnot yet mapped\n",
            "## Field map summary\n\n| field_id | Value |\n|---|---|\n| box1.loon | 48250 |\n",
            1,
        )
        self.assertError(shown, "shows a map but Appendix B holds 'not yet mapped'")

    def test_field_map_pointers_resolve_inside_the_workpack(self):
        field_map = yaml.safe_load(yaml.safe_dump(samples.ANNUAL_FIELD_MAP))
        field_map["missing_fields"] = [
            {
                "field_id": "box3.bankrekeningen",
                "label": "Bankrekeningen",
                "reason": "statement not shared yet",
                "blocking": True,
                "open_question_id": "Q009",
            }
        ]
        self.assertError(
            samples.build_workpack("annual", field_map=field_map),
            "open_question_id 'Q009' has no row",
        )
        field_map = yaml.safe_load(yaml.safe_dump(samples.ANNUAL_FIELD_MAP))
        field_map["fields"][0]["source"]["profile_path"] = "partner.has_fiscal_partner"
        self.assertValid(samples.build_workpack("annual", field_map=field_map), "annual")
        field_map["fields"][0]["source"]["profile_path"] = "partner.spouse_name"
        self.assertError(
            samples.build_workpack("annual", field_map=field_map),
            "is not a row Key in '## Taxpayer profile summary'",
        )


def _copy(field_map):
    return yaml.safe_load(yaml.safe_dump(field_map))


def _replace_summary(text, new_body):
    return samples.replace_section(text, "Field map summary", new_body)


SUMMARY_HEADER = (
    "| Portal section | Portal label | field_id | Value to enter | Source | Review |\n"
    "|---|---|---|---|---|---|\n"
)


class FieldMapSummaryTests(WorkpackGraderTestCase):
    """Review amendment A12: the Field map summary is the checked surface."""

    def mapped(self, **kwargs):
        return samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP, **kwargs)

    def test_reported_case_wrong_salary_in_the_summary_is_rejected(self):
        text = self.mapped()
        broken = text.replace("| box1.loon | 48250 |", "| box1.loon | 1 |", 1)
        self.assertNotEqual(broken, text)
        self.assertError(broken, "shows box1.loon = '1' but Appendix B holds 48250", "annual")
        # The field-map grader alone still accepts the unchanged Appendix B.
        field_map_grader = samples.load_field_map_grader()
        errors, _ = field_map_grader.validate(self.grade(broken, "annual").field_map)
        self.assertEqual(errors, [])

    def test_reported_case_deleted_withholding_row_is_rejected(self):
        text = self.mapped()
        lines = [line for line in text.split("\n") if "| box1.loonheffing |" not in line]
        self.assertError(
            "\n".join(lines),
            "Appendix B manual_entry field box1.loonheffing is missing from '## Field map summary'",
            "annual",
        )

    def test_summary_must_hold_the_table_once_mapped(self):
        text = _replace_summary(self.mapped(), "Readiness: draft | Mapped from sources: 2")
        self.assertError(text, "must hold the summary table", "annual")
        wrong_columns = _replace_summary(
            self.mapped(),
            "| field_id | Value to enter |\n|---|---|\n| box1.loon | 48250 |\n| box1.loonheffing | 13100 |",
        )
        self.assertError(wrong_columns, "table must use the columns", "annual")

    def test_equal_values_pass_in_any_amount_format(self):
        for shown_loon, shown_heffing in (
            ("EUR 48,250", "€ 13.100"),
            ("48.250,00", "13,100.00"),
            ("€48 250", "`13100`"),
            ("**48250**", "EUR 13 100,-"),
        ):
            with self.subTest(loon=shown_loon):
                text = self.mapped().replace("| box1.loon | 48250 |", f"| box1.loon | {shown_loon} |", 1)
                text = text.replace("| box1.loonheffing | 13100 |", f"| box1.loonheffing | {shown_heffing} |", 1)
                self.assertValid(text, "annual")
        near_miss = self.mapped().replace("| box1.loon | 48250 |", "| box1.loon | 48,25 |", 1)
        self.assertError(near_miss, "shows box1.loon = '48,25'", "annual")

    def test_double_entry_rows_repeat_one_value(self):
        text = self.mapped()
        row = "| Box 1 | Loon | box1.loon | 48250 | mapped | check |"
        self.assertIn(row, text)
        twice = text.replace(row, row + "\n| Box 1 (screen 2) | Loon | box1.loon | 48,250 | mapped | check |", 1)
        self.assertValid(twice, "annual")
        differing = text.replace(row, row + "\n| Box 1 (screen 2) | Loon | box1.loon | 45,000 | mapped | check |", 1)
        self.assertError(differing, "shows box1.loon with different values", "annual")

    def test_missing_fields_appear_as_missing_rows_with_their_q_id(self):
        field_map = _copy(samples.ANNUAL_FIELD_MAP)
        field_map["missing_fields"] = [
            {
                "field_id": "box3.bankrekeningen",
                "label": "Bankrekeningen",
                "reason": "statement not shared yet",
                "blocking": True,
                "open_question_id": "Q001",
            }
        ]
        kwargs = dict(
            field_map=field_map,
            questions=(("Q001", "box3_peildatum", "Bank balance on 1 January 2025?", "yes"),),
            open_questions={"box3_peildatum": ["Q001"]},
        )
        text = samples.build_workpack("annual", **kwargs)
        self.assertIn("| box3.bankrekeningen | MISSING - enter manually | Q001 |", text)
        self.assertValid(text, "annual")
        self.assertValid(
            text.replace("MISSING - enter manually | Q001", "MISSING — enter manually | Q001", 1), "annual"
        )
        no_qid = text.replace("| MISSING - enter manually | Q001 |", "| MISSING - enter manually | ask |", 1)
        self.assertError(no_qid, "MISSING row box3.bankrekeningen must name its Q-ID Q001", "annual")
        dropped = "\n".join(
            line for line in text.split("\n") if "| box3.bankrekeningen |" not in line
        )
        self.assertError(
            dropped,
            "Appendix B missing field box3.bankrekeningen has no 'MISSING - enter manually' row",
            "annual",
        )
        filled = text.replace("| MISSING - enter manually | Q001 |", "| 0 | Q001 |", 1)
        self.assertError(filled, "shows box3.bankrekeningen = '0' but Appendix B has no value", "annual")

    def test_rows_must_name_appendix_b_portal_fields(self):
        text = self.mapped()
        extra = text.replace(
            "| box1.loonheffing | 13100 |",
            "| box1.loonheffing | 13100 | mapped | check |\n| Box 1 | Extra | box1.extra | 500",
            1,
        )
        self.assertError(extra, "row box1.extra is not a field in Appendix B", "annual")

        field_map = _copy(samples.ANNUAL_FIELD_MAP)
        field_map["fields"].append(
            {
                "field_id": "business.legal_form",
                "label": "Rechtsvorm",
                "entry_mode": "internal_routing",
                "value": "eenmanszaak",
                "source": {"type": "user_chat", "quote": "I have an eenmanszaak", "stated_at": "2026-09-20"},
                "confidence": 0.9,
                "manual_review_required": False,
                "notes": [],
            }
        )
        routed = samples.build_workpack("annual", field_map=field_map)
        self.assertNotIn("| business.legal_form |", routed)
        self.assertValid(routed, "annual")
        shown = routed.replace(
            "| box1.loonheffing | 13100 | mapped | check |",
            "| box1.loonheffing | 13100 | mapped | check |\n| Onderneming | Rechtsvorm | business.legal_form | eenmanszaak | chat | - |",
            1,
        )
        self.assertError(shown, "internal_routing record that is never a portal row", "annual")

    def test_summary_readiness_line_matches_appendix_b(self):
        text = self.mapped()
        table_start = text.index(SUMMARY_HEADER)
        with_line = text[:table_start] + "Readiness: draft | Mapped from sources: 2 | Missing: 0\n\n" + text[table_start:]
        self.assertValid(with_line, "annual")
        self.assertError(
            with_line.replace("Readiness: draft |", "Readiness: review_ready |", 1),
            "says Readiness: review_ready but Appendix B readiness is draft",
            "annual",
        )

    def test_value_normalization(self):
        normalize = self.grader.normalize_value
        self.assertEqual(normalize("EUR 48.250,00"), normalize(48250))
        self.assertEqual(normalize("48,250"), normalize("48250"))
        self.assertEqual(normalize("1,5"), normalize(1.5))
        self.assertEqual(normalize("0.125"), normalize("0,125"))
        self.assertEqual(normalize("-1.200"), normalize(-1200))
        self.assertEqual(normalize("Ja"), normalize(True))
        self.assertNotEqual(normalize("48,25"), normalize(48250))
        self.assertEqual(normalize("Hypotheek  ING"), normalize("hypotheek ing"))
        self.assertEqual(normalize("51,400 (check the pre-fill; correct if different)"), normalize(51400))
        self.assertEqual(normalize("nee (no business)"), normalize(False))
        self.assertEqual(normalize("see note (x)")[0], "text")


class StaleOutputTests(WorkpackGraderTestCase):
    """Review amendment A10: stale map and checklist after a changed fact."""

    FACT = ("fiscaal loon", "2026-09-22")
    OLD_ROWS = (("1", "Loon", "EUR 48,250", "ev_001", "box1.loon"),)

    def test_stale_workpack_with_unconfirmed_generation_is_valid(self):
        text = samples.build_workpack(
            "annual",
            field_map=samples.ANNUAL_FIELD_MAP,
            checklist_rows=self.OLD_ROWS,
            stale=self.FACT,
        )
        self.assertEqual(text.count("STALE — predates the change to fiscaal loon (2026-09-22)"), 3)
        report = self.assertValid(text, "annual")
        self.assertIs(report.resume_record["generation_confirmed"], False)

    def test_stale_marker_is_invalid_once_generation_is_confirmed(self):
        text = samples.build_workpack(
            "annual", field_map=samples.ANNUAL_FIELD_MAP, stale=self.FACT
        )
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses["confirm"] = "complete"
        confirmed = samples.build_workpack(
            "annual", field_map=samples.ANNUAL_FIELD_MAP, statuses=statuses
        )
        stale_line = samples.stale_marker(*self.FACT)
        leftover = confirmed.replace(
            "## Field map summary\n\n", "## Field map summary\n\n" + stale_line + "\n\n", 1
        )
        self.assertValid(text, "annual")
        self.assertError(leftover, "valid only while Appendix A generation_confirmed is false", "annual")

    def test_changed_fact_without_stale_markers_is_rejected(self):
        statuses = samples.default_statuses("annual", "annual_2025")
        unmarked = samples.build_workpack(
            "annual",
            field_map=samples.ANNUAL_FIELD_MAP,
            statuses=statuses,
            checklist_rows=self.OLD_ROWS,
        )
        report = self.assertError(unmarked, "must carry the line 'STALE", "annual")
        message = next(error for error in report.errors if "must carry the line" in error)
        for part in ("'## Field map summary'", "Appendix B", "'## Manual-entry checklist'"):
            self.assertIn(part, message)

        marked_map_only = samples.build_workpack(
            "annual", field_map=samples.ANNUAL_FIELD_MAP, stale=self.FACT
        )
        checklist = samples.replace_section(
            marked_map_only, "Manual-entry checklist", "### 4. Steps\n\n| Step | Portal label | Value to enter | Source | field_id |\n|---|---|---|---|---|\n| 1 | Loon | 48250 | ev_001 | box1.loon |"
        )
        self.assertError(checklist, "'## Manual-entry checklist' must carry the line", "annual")

    def test_malformed_stale_line_and_stale_without_map_are_rejected(self):
        text = samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP, stale=self.FACT)
        malformed = text.replace("; regenerate before use.", " - please redo", 1)
        self.assertError(malformed, "STALE line must read", "annual")
        unmapped = samples.build_workpack("annual").replace(
            "## Field map summary\n\nnot yet mapped",
            "## Field map summary\n\n" + samples.stale_marker(*self.FACT) + "\n\nnot yet mapped",
            1,
        )
        self.assertError(unmapped, "needs a field map in Appendix B", "annual")

    def test_stale_map_keeps_its_readiness_until_regeneration(self):
        ready_map = _copy(samples.ANNUAL_FIELD_MAP)
        ready_map["readiness"] = "review_ready"
        stale = samples.build_workpack("annual", field_map=ready_map, stale=self.FACT)
        self.assertValid(stale, "annual")
        statuses = samples.default_statuses("annual", "annual_2025")
        unmarked_draft = samples.build_workpack(
            "annual", field_map=ready_map, statuses=statuses, generation_confirmed=False
        )
        self.assertError(unmarked_draft, "nothing promotes a draft", "annual")

    def test_checklist_may_stay_stale_after_regeneration(self):
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses["confirm"] = "complete"
        regenerated = samples.build_workpack(
            "annual", field_map=samples.ANNUAL_FIELD_MAP, statuses=statuses
        )
        stale_checklist = samples.replace_section(
            regenerated,
            "Manual-entry checklist",
            samples.stale_marker(*self.FACT)
            + "\n\n### 4. Steps\n\n| Step | Portal label | Value to enter | Source | field_id |\n"
            "|---|---|---|---|---|\n| 1 | Loon | 48250 | ev_001 | box1.loon |",
        )
        self.assertValid(stale_checklist, "annual")

    def test_checklist_never_shows_a_value_the_current_map_lacks(self):
        corrected = _copy(samples.ANNUAL_FIELD_MAP)
        corrected["fields"][0]["value"] = 51400
        old_checklist = samples.build_workpack(
            "annual", field_map=corrected, checklist_rows=self.OLD_ROWS
        )
        self.assertError(
            old_checklist,
            "'## Manual-entry checklist' shows box1.loon = 'EUR 48,250' but Appendix B holds 51400",
            "annual",
        )
        rebuilt = samples.build_workpack(
            "annual",
            field_map=corrected,
            checklist_rows=(("1", "Loon", "EUR 51.400", "ev_001", "box1.loon"),),
        )
        self.assertValid(rebuilt, "annual")
        unknown_row = samples.build_workpack(
            "annual",
            field_map=corrected,
            checklist_rows=(("1", "Rente", "300", "ev_001", "box1.rente"),),
        )
        self.assertError(unknown_row, "'## Manual-entry checklist' row box1.rente is not a field in Appendix B", "annual")


class ChatFieldMapSummaryTests(WorkpackGraderTestCase):
    """A12 in chat mode: the rendering always states the map's state."""

    def chat(self, text, kind="annual"):
        return self.grader.validate_workpack_text(text, expected_kind=kind, presentation="chat")

    def assertChatValid(self, text, kind="annual"):
        report = self.chat(text, kind)
        self.assertEqual(report.errors, [], "\n".join(report.errors))

    def assertChatError(self, text, fragment, kind="annual"):
        errors = self.chat(text, kind).errors
        self.assertTrue(any(fragment in error for error in errors), f"{fragment!r} not in {errors}")

    def test_mapped_chat_rendering_passes(self):
        for kind, field_map in (
            ("annual", samples.ANNUAL_FIELD_MAP),
            ("provisional", samples.PROVISIONAL_FIELD_MAP),
        ):
            with self.subTest(kind=kind):
                self.assertChatValid(samples.build_chat_rendering(kind, field_map=field_map), kind)

    def test_reported_case_removed_summary_is_rejected(self):
        rendering = samples.build_chat_rendering("annual", field_map=samples.ANNUAL_FIELD_MAP)
        removed = samples.remove_section(rendering, "Field map summary")
        self.assertChatError(removed, "'## Field map summary' is required in the conversation rendering")
        unmapped = samples.remove_section(samples.build_chat_rendering("provisional"), "Field map summary")
        self.assertChatError(unmapped, "'## Field map summary' is required", "provisional")
        for subflow in ("review", "stopzetten"):
            with self.subTest(subflow=subflow):
                rendering = samples.build_chat_rendering(
                    "provisional", workflow=f"provisional_2026_{subflow}"
                )
                self.assertChatValid(samples.remove_section(rendering, "Field map summary"), "provisional")

    def test_mapped_state_markers_require_the_table(self):
        rendering = samples.build_chat_rendering("annual", field_map=samples.ANNUAL_FIELD_MAP)
        readiness_only = _replace_summary(rendering, "Readiness: draft | Mapped from sources: 2")
        self.assertChatError(readiness_only, "claims a field map")
        both = _replace_summary(rendering, "not yet mapped\n\n" + SUMMARY_HEADER + "| Box 1 | Loon | box1.loon | 48250 | ev_001 | check |")
        self.assertChatError(both, "holds both 'not yet mapped' and a mapped-state marker")
        empty = _replace_summary(rendering, "The map is ready.")
        self.assertChatError(empty, "must hold the summary table once mapping has run")
        no_qid = _replace_summary(
            rendering,
            SUMMARY_HEADER + "| Box 3 | Bankrekeningen | box3.bankrekeningen | MISSING - enter manually | ask later | Blocking |",
        )
        self.assertChatError(no_qid, "without its Q-ID")

    def test_chat_checklist_shows_the_summary_values_or_is_stale(self):
        old_rows = (("1", "Loon", "EUR 48,250", "ev_001", "box1.loon"),)
        corrected = _copy(samples.ANNUAL_FIELD_MAP)
        corrected["fields"][0]["value"] = 51400
        mismatch = samples.build_chat_rendering("annual", field_map=corrected, checklist_rows=old_rows)
        self.assertChatError(
            mismatch, "'## Manual-entry checklist' shows box1.loon = 'EUR 48,250' but '## Field map summary' holds '51400'"
        )
        stale = samples.build_chat_rendering(
            "annual",
            field_map=samples.ANNUAL_FIELD_MAP,
            checklist_rows=old_rows,
            stale=("fiscaal loon", "2026-09-22"),
        )
        self.assertChatValid(stale)
        unmarked = stale.replace(
            "## Manual-entry checklist\n\n" + samples.stale_marker("fiscaal loon", "2026-09-22"),
            "## Manual-entry checklist\n",
            1,
        )
        self.assertNotEqual(unmarked, stale)
        self.assertChatError(unmarked, "the manual-entry checklist built from it must carry the line")


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(GRADER_PATH), *args],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )

    def test_exit_codes_and_kind_inference_from_the_fixed_file_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            annual = folder / "nl-tax-annual-2025-workpack.md"
            annual.write_text(samples.build_workpack("annual"), encoding="utf-8")
            result = self.run_cli("--expect-saved", str(annual))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("WORKPACK VALID", result.stdout)

            misplaced = folder / "nl-tax-provisional-2026-workpack.md"
            misplaced.write_text(samples.build_workpack("annual"), encoding="utf-8")
            result = self.run_cli(str(misplaced))
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("WORKPACK INVALID", result.stdout)
            self.assertIn("does not belong in the provisional workpack", result.stdout)

            chat = folder / "chat-copy.md"
            chat.write_text(
                samples.build_workpack("annual", save_consent="not_given"), encoding="utf-8"
            )
            self.assertEqual(self.run_cli(str(chat)).returncode, 0)
            self.assertEqual(self.run_cli("--expect-saved", str(chat)).returncode, 1)

    def test_the_seeded_eval_workpacks_are_valid_saved_workpacks(self):
        seeds = sorted(
            (REPO_ROOT / "evals/nl-tax-agent-skills/fixtures/seeds").glob("*/nl-tax-*-workpack.md")
        )
        self.assertEqual(len(seeds), 2)
        result = self.run_cli("--expect-saved", *map(str, seeds))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_raw_templates_are_not_valid_workpacks(self):
        for kind, template in samples.TEMPLATES.items():
            with self.subTest(kind=kind):
                result = self.run_cli("--kind", kind, str(template))
                self.assertEqual(result.returncode, 1)
                self.assertIn("Sources used", result.stdout)


class ChatRenderingTests(WorkpackGraderTestCase):
    """Review amendment A8: the conversation shows only filled sections, no YAML."""

    def chat(self, text, kind):
        return self.grader.validate_workpack_text(text, expected_kind=kind, presentation="chat")

    def test_chat_renderings_of_both_templates_pass(self):
        for kind in ("annual", "provisional"):
            with self.subTest(kind=kind):
                report = self.chat(samples.build_chat_rendering(kind), kind)
                self.assertEqual(report.errors, [], "\n".join(report.errors))
                self.assertIsNone(report.resume_record)

    def test_appendices_yaml_and_fill_notes_never_appear_in_chat(self):
        full = samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP)
        errors = self.chat(full, "annual").errors
        self.assertTrue(any("never shows '## Appendix A" in error for error in errors), errors)
        self.assertTrue(any("never shows '## Appendix B" in error for error in errors), errors)
        self.assertTrue(any("never prints a YAML block" in error for error in errors), errors)
        self.assertTrue(any("template fill note" in error for error in errors), errors)

        rendering = samples.build_chat_rendering("annual")
        with_note = rendering.replace(
            "## Open questions\n", "## Open questions\n\n[Every question still awaiting ...]\n", 1
        )
        self.assertTrue(
            any("template fill note" in error for error in self.chat(with_note, "annual").errors)
        )

    def test_chat_mode_keeps_section_order_privacy_and_documents_checks(self):
        rendering = samples.build_chat_rendering("annual")
        missing = samples.remove_section(rendering, "Sources used")
        self.assertTrue(
            any(
                "missing required section '## Sources used'" in error
                for error in self.chat(missing, "annual").errors
            )
        )
        leaked = rendering.replace("## Assumptions\n", "## Assumptions\n\nBSN 123456782\n", 1)
        self.assertTrue(any("never record a BSN" in error for error in self.chat(leaked, "annual").errors))
        dangling = rendering.replace("## Assumptions\n", "## Assumptions\n\nSee F:ev_009.\n", 1)
        self.assertTrue(any("ev_009" in error for error in self.chat(dangling, "annual").errors))

    def test_a_rendering_is_never_a_saved_file(self):
        report = self.grader.validate_workpack_text(
            samples.build_chat_rendering("annual"),
            expected_kind="annual",
            expect_saved=True,
            presentation="chat",
        )
        self.assertTrue(any("never a saved workpack" in error for error in report.errors))

    def test_cli_chat_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "chat-workpack.md"
            path.write_text(samples.build_chat_rendering("provisional"), encoding="utf-8")
            command = [sys.executable, str(GRADER_PATH), "--kind", "provisional"]

            def run(*args):
                return subprocess.run(
                    command + list(args), capture_output=True, text=True, cwd=REPO_ROOT
                )

            ok = run("--chat", str(path))
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            self.assertEqual(run(str(path)).returncode, 1)
            self.assertEqual(run("--chat", "--expect-saved", str(path)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
