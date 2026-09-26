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


def flattened(relative_path):
    return " ".join(read_plugin(relative_path).split())


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
        annual_template = flattened("skills/nl-tax-annual-return/templates/annual-workpack.md")
        self.assertIn("`queued_workflow` holds the queued 2026 subflow value", annual_template)

    def test_intake_records_both_but_activates_annual_only_and_writes_nothing(self):
        runtime = flattened("skills/nl-tax-shared-resources/runtime-contract.md")
        intake = flattened("skills/nl-tax-intake/SKILL.md")
        intake_flow = flattened("skills/nl-tax-intake/reference/intake-flow.md")
        filing_paths = flattened("skills/nl-tax-intake/reference/filing-paths.md")

        self.assertIn("carry the provisional subflow as the queued workflow", intake)
        self.assertIn("without a new activation phrase", intake)
        self.assertIn("It is never final-generation confirmation for either workpack", intake)
        self.assertIn("Both workflows requested", read_plugin("skills/nl-tax-intake/reference/intake-flow.md"))
        self.assertIn("records it as `queued_workflow`", intake_flow)
        self.assertIn("without asking for a new activation phrase", filing_paths)
        self.assertIn("`queued_workflow: provisional_2026_<subflow>`", runtime)
        self.assertIn("A queued workflow is intent, not a second active owner", runtime)
        self.assertIn(
            "do not load provisional resources or collect provisional figures while annual is active",
            runtime,
        )
        self.assertNotIn("Edit(", read_plugin("skills/nl-tax-intake/SKILL.md").split("---", 2)[1])

    def test_annual_handoff_requires_generated_and_mapped_workpack(self):
        runtime = flattened("skills/nl-tax-shared-resources/runtime-contract.md")
        assembly = flattened("skills/nl-tax-annual-return/reference/phases/10-assembly.md")
        annual_skill = flattened("skills/nl-tax-annual-return/SKILL.md")

        self.assertIn(
            "annual workpack has been generated and mapped with every field-map check passing",
            runtime,
        )
        self.assertIn("never partially switch ownership", runtime)
        self.assertIn("intentionally `draft`", runtime)
        self.assertIn("do not partially hand off", assembly)
        self.assertIn("annual stays the active workflow and 2026 stays queued", assembly)
        self.assertIn("leave the annual workpack unchanged", assembly)
        self.assertIn("record the queued 2026 subflow as `queued_workflow`", annual_skill)
        self.assertIn("after the annual workpack is generated and mapped", annual_skill.lower())

    def test_handoff_needs_no_reactivation_but_keeps_generation_gates_separate(self):
        runtime = flattened("skills/nl-tax-shared-resources/runtime-contract.md")
        intake_skill = flattened("skills/nl-tax-intake/SKILL.md")
        annual_skill = flattened("skills/nl-tax-annual-return/SKILL.md")
        provisional_skill = flattened("skills/nl-tax-provisional-assessment/SKILL.md")

        for text in (runtime, intake_skill, annual_skill, provisional_skill):
            with self.subTest(document=text[:80]):
                self.assertIn("activation phrase", text)

        self.assertIn("without another activation phrase", provisional_skill)
        self.assertIn("it does not authorize final generation", provisional_skill)
        self.assertIn("does not authorize final provisional artifact generation", runtime)
        self.assertIn("does not replace the later 2026 final-generation confirmation", annual_skill)
        self.assertIn("Never require exact wording", provisional_skill)
        self.assertIn("reuse the opening preparation request as final consent", provisional_skill)

    def test_each_workflow_keeps_its_own_file_with_its_own_consent(self):
        runtime = flattened("skills/nl-tax-shared-resources/runtime-contract.md")
        provisional_skill = flattened("skills/nl-tax-provisional-assessment/SKILL.md")
        annual_skill = flattened("skills/nl-tax-annual-return/SKILL.md")
        assembly = flattened("skills/nl-tax-annual-return/reference/phases/10-assembly.md")

        self.assertIn("Provisional starts its own file only with consent", runtime)
        self.assertIn(
            "Consent given for the annual file extends to the provisional file only if the user said so",
            runtime,
        )
        self.assertIn(
            "Consent to save the annual file covers this file only if the user said so",
            provisional_skill,
        )
        self.assertIn("Never write the provisional workpack or any other file", annual_skill)
        self.assertIn("Never write the annual workpack or any other file", provisional_skill)
        self.assertIn("A consent given earlier for the annual file extends to the 2026 file only if the user said so", assembly)

    def test_handoff_suppresses_the_ambiguous_annual_checklist_question(self):
        assembly = flattened(
            "skills/nl-tax-annual-return/reference/phases/10-assembly.md"
        ).lower()
        mapper_skill = flattened("skills/nl-tax-field-mapper/SKILL.md").lower()
        mapper_flow = flattened(
            "skills/nl-tax-field-mapper/reference/mapper-flow.md"
        ).lower()

        self.assertIn("do not ask an annual-checklist question at the handoff", assembly)
        self.assertIn("make the next actual question a 2026-subflow question", assembly)
        self.assertIn("never reinterpret it as annual-checklist authorization", assembly)
        for mapper in (mapper_skill, mapper_flow):
            with self.subTest(mapper=mapper[:80]):
                self.assertIn("provisional 2026", mapper)
                self.assertIn("`queued`", mapper)
                self.assertIn("non-question", mapper)
                self.assertIn("bare", mapper)
                self.assertIn("checklist", mapper)

        fixture = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
        handoff = fixture["expected_conversation"]["after_complete_annual_mapping"]
        self.assertIs(handoff["annual_checklist_question_suppressed"], True)
        self.assertIs(handoff["annual_checklist_availability_is_non_question"], True)
        self.assertIs(handoff["bare_yes_activates_annual_checklist"], False)
        self.assertEqual(handoff["first_question_owner"], "provisional_2026_request")

    def test_owner_contracts_keep_year_specific_facts_separate(self):
        runtime = flattened("skills/nl-tax-shared-resources/runtime-contract.md")
        provisional = flattened("skills/nl-tax-provisional-assessment/SKILL.md")
        assembly = flattened("skills/nl-tax-annual-return/reference/phases/10-assembly.md")

        self.assertIn("never copy an annual amount into provisional facts automatically", runtime)
        self.assertIn("Never copy an annual amount into 2026 facts", assembly)
        self.assertIn("Do not copy annual actuals into provisional facts", provisional)
        self.assertIn("Leave the annual workpack and the completed annual work exactly as handed off", provisional)

    def test_source_ledgers_do_not_union_annual_and_provisional_ids(self):
        runtime = flattened("skills/nl-tax-shared-resources/runtime-contract.md")
        annual_output = flattened(
            "skills/nl-tax-annual-return/reference/annual-output-contract.md"
        )
        provisional_output = flattened(
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        )

        self.assertIn("never a union of both", runtime)
        self.assertIn("the provisional list starts empty", runtime)
        self.assertIn("Never include the other workflow's IDs", runtime)
        self.assertIn("do not include provisional IDs", annual_output)
        self.assertIn("Do not copy IDs from the annual workflow", provisional_output)
        self.assertIn("MUST equal Appendix A `sources_loaded`", provisional_output)

    def test_structural_fixture_covers_each_transition_and_is_wired(self):
        fixture = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
        dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        conversation = fixture["expected_conversation"]

        self.assertIn("prepare both", fixture["user_request"]["text"].lower())
        self.assertIn("do not make me use a slash command", fixture["user_request"]["text"])

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
