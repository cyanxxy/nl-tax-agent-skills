#!/usr/bin/env python3
"""Contracts for one-request annual-2025 to provisional-2026 sequencing (0.4 R11).

Annual runs first; the 2026 request is carried as ``queued_workflow`` in the
annual resume record (and in the conversation); after the annual workpack is
generated and mapped, provisional collection continues without a new
activation phrase; each workflow keeps its own file, only with its own save
consent, and its own final-generation confirmation.
"""

import importlib.util
import pathlib
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
PLUGIN_ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
FIXTURE_PATH = (
    REPO_ROOT
    / "evals"
    / "nl-tax-agent-skills"
    / "fixtures"
    / "annual"
    / "dual-workflow-handoff.yaml"
)
DATASET_PATH = REPO_ROOT / "evals" / "nl-tax-agent-skills" / "offline-dataset.yaml"
ANNUAL = "workspace/nl-tax-annual-2025-workpack.md"
PROVISIONAL = "workspace/nl-tax-provisional-2026-workpack.md"

_spec = importlib.util.spec_from_file_location("workpack_samples_for_dual", HERE / "workpack_samples.py")
samples = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(samples)


def read_plugin(relative_path):
    return (PLUGIN_ROOT / relative_path).read_text(encoding="utf-8")


def appendix_a(relative_path):
    grader = samples.load_grader()
    record, errors = grader.resume_record_block(read_plugin(relative_path))
    assert not errors, errors
    return record


class DualWorkflowHandoffTests(unittest.TestCase):
    def test_templates_carry_one_queued_workflow_slot_in_the_annual_record(self):
        annual = appendix_a("skills/nl-tax-annual-return/templates/annual-workpack.md")
        provisional = appendix_a(
            "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md"
        )
        self.assertIn("queued_workflow", annual)
        self.assertIsNone(annual["queued_workflow"])
        self.assertIsNone(provisional["queued_workflow"])
        self.assertEqual(annual["workflow"], "annual_2025")
        self.assertTrue(provisional["workflow"].startswith("provisional_2026_"))
        self.assertEqual(annual["sources_loaded"], [])
        self.assertEqual(provisional["sources_loaded"], [])

    def test_intake_records_both_but_activates_annual_only_and_writes_nothing(self):
        self.assertNotIn("Edit(", read_plugin("skills/nl-tax-intake/SKILL.md").split("---", 2)[1])

    def test_handoff_suppresses_the_ambiguous_annual_checklist_question(self):
        fixture = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
        handoff = fixture["expected_conversation"]["after_complete_annual_mapping"]
        self.assertIs(handoff["annual_checklist_question_suppressed"], True)
        self.assertIs(handoff["annual_checklist_availability_is_non_question"], True)
        self.assertIs(handoff["bare_yes_activates_annual_checklist"], False)
        self.assertEqual(handoff["first_question_owner"], "provisional_2026_request")

    def test_structural_fixture_covers_each_transition_and_is_wired(self):
        fixture = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
        dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        conversation = fixture["expected_conversation"]

        intake = conversation["after_intake"]
        self.assertEqual(intake["active_workflow"], "annual_2025")
        self.assertEqual(intake["queued_workflow"], "provisional_2026_request")
        self.assertFalse(intake["provisional_resources_loaded"])
        self.assertFalse(intake["provisional_facts_collected"])
        self.assertEqual(intake["files_written"], [])

        handoff = conversation["after_complete_annual_mapping"]
        self.assertEqual(handoff["active_workflow"], "provisional_2026_request")
        self.assertFalse(handoff["requires_new_activation_phrase"])
        self.assertFalse(handoff["provisional_generation_confirmed"])
        # A6: the handoff clears queued_workflow and changes nothing else.
        self.assertEqual(handoff["annual_workpack_change_at_handoff"], "queued_workflow_cleared")
        self.assertTrue(handoff["provisional_file_consent_asked_once"])
        self.assertTrue(handoff["one_yes_no_question_per_reply"])
        self.assertIsNone(handoff["annual_resume_record"]["queued_workflow"])
        self.assertEqual(handoff["annual_resume_record"]["sources_loaded"], ["annual_source_id"])
        self.assertEqual(handoff["provisional_sources_loaded"], [])

        finished = conversation["after_complete_provisional_mapping"]
        self.assertEqual(finished["files_written"], [ANNUAL, PROVISIONAL])
        self.assertEqual(finished["annual_resume_record"]["sources_loaded"], ["annual_source_id"])
        self.assertEqual(
            finished["provisional_resume_record"]["sources_loaded"], ["provisional_source_id"]
        )
        self.assertIsNone(finished["provisional_resume_record"]["queued_workflow"])
        self.assertIsNone(finished["annual_resume_record"]["queued_workflow"])
        self.assertNotIn(
            "provisional_source_id", finished["annual_resume_record"]["sources_loaded"]
        )
        self.assertNotIn(
            "annual_source_id", finished["provisional_resume_record"]["sources_loaded"]
        )
        self.assertTrue(conversation["invariants"]["annual_and_provisional_save_consent_are_separate"])

        self.assertEqual(fixture["saving"]["annual_2025"]["consent"], "given")
        self.assertEqual(fixture["saving"]["provisional_2026"]["consent"], "given")
        self.assertTrue(fixture["saving"]["provisional_2026"]["asked_separately"])
        self.assertEqual(fixture["expected_outputs"]["files_created"], [ANNUAL, PROVISIONAL])

        cases = {case["id"]: case for case in dataset["cases"]}
        case = cases["annual_then_provisional_request"]
        self.assertEqual(
            case["fixture"],
            "evals/nl-tax-agent-skills/fixtures/annual/dual-workflow-handoff.yaml",
        )
        self.assertIn("annual_then_provisional_request", dataset["contract_default_cases"])
        self.assertEqual(case["expected_files"], [ANNUAL, PROVISIONAL])
        rules = {rule["path"]: rule for rule in case["workpacks"]}
        self.assertEqual(rules[ANNUAL]["workflow"], "annual_2025")
        self.assertIsNone(rules[ANNUAL]["queued_workflow"])
        self.assertEqual(rules[PROVISIONAL]["workflow"], "provisional_2026_request")
        self.assertIsNone(rules[PROVISIONAL]["queued_workflow"])
        for rule in rules.values():
            self.assertEqual(rule["field_map"], "expected")
            self.assertTrue(rule["generation_confirmed"])
        self.assertEqual(case["source_ledger_check"]["workpacks"], [ANNUAL, PROVISIONAL])


class DualWorkflowGraderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grader = samples.load_grader()

    def grade(self, text, kind):
        return self.grader.validate_workpack_text(text, expected_kind=kind, expect_saved=True)

    def test_a_queued_annual_record_and_a_separate_provisional_file_pass(self):
        annual = samples.build_workpack(
            "annual",
            readiness="review_ready",
            queued_workflow="provisional_2026_request",
            field_map=samples.ANNUAL_FIELD_MAP,
        )
        provisional = samples.build_workpack("provisional", field_map=samples.PROVISIONAL_FIELD_MAP)
        self.assertEqual(self.grade(annual, "annual").errors, [])
        self.assertEqual(self.grade(provisional, "provisional").errors, [])

    def test_the_grader_rejects_merged_or_crossed_workflows(self):
        crossed_sources = samples.build_workpack(
            "annual",
            queued_workflow="provisional_2026_request",
            sources=("bd_box1_rates_2025", "bd_provisional_request_2026"),
        )
        self.assertTrue(
            any("source ledgers never mix workflows" in error for error in self.grade(crossed_sources, "annual").errors)
        )
        queued_in_provisional = samples.build_workpack(
            "provisional", queued_workflow="provisional_2026_request"
        )
        self.assertTrue(
            any(
                "queued_workflow must be null in a provisional workpack" in error
                for error in self.grade(queued_in_provisional, "provisional").errors
            )
        )
        combined = samples.build_workpack("annual").replace(
            "## Assumptions\n",
            "## Assumptions\n\nThe 2026 part lives in workspace/nl-tax-provisional-2026-workpack.md.\n",
            1,
        )
        self.assertTrue(
            any("mentions the provisional workpack path" in error for error in self.grade(combined, "annual").errors)
        )
        wrong_file = samples.build_workpack("provisional")
        self.assertTrue(
            any("does not belong in the annual workpack" in error for error in self.grade(wrong_file, "annual").errors)
        )


if __name__ == "__main__":
    unittest.main()
