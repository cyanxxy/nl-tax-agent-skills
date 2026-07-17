#!/usr/bin/env python3
"""Contracts for one-request annual-2025 to provisional-2026 sequencing."""

import pathlib
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
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


def read_plugin(relative_path):
    return (PLUGIN_ROOT / relative_path).read_text(encoding="utf-8")


def load_plugin_yaml(relative_path):
    return yaml.safe_load(read_plugin(relative_path))


def flattened(relative_path):
    return " ".join(read_plugin(relative_path).split())


class DualWorkflowHandoffTests(unittest.TestCase):
    def test_templates_represent_one_active_and_one_queued_workflow(self):
        profile = load_plugin_yaml("skills/nl-tax-intake/templates/taxpayer-profile.yaml")
        progress = load_plugin_yaml("skills/_shared/templates/session-progress.yaml")
        profile_text = read_plugin("skills/nl-tax-intake/templates/taxpayer-profile.yaml")
        progress_text = read_plugin("skills/_shared/templates/session-progress.yaml")

        self.assertEqual(
            set(profile["workflows"]), {"annual_2025", "provisional_2026"}
        )
        self.assertIs(profile["workflows"]["annual_2025"]["requested"], False)
        self.assertIs(profile["workflows"]["provisional_2026"]["requested"], False)
        self.assertIn("not_started | queued | in_progress | complete", profile_text)
        self.assertIn("exactly one current candidate", progress_text)
        self.assertIn("a queued workflow is not active", progress_text)
        self.assertIn("subflow", progress["sections"]["provisional_2026"])
        self.assertEqual(
            set(progress["sources_loaded_by_workflow"]),
            {"annual_2025", "provisional_2026"},
        )
        self.assertEqual(progress["sources_loaded"], [])

    def test_intake_records_both_but_activates_annual_only(self):
        runtime = flattened("skills/_shared/runtime-contract.md")
        intake = flattened("skills/nl-tax-intake/reference/intake-flow.md")
        filing_paths = flattened("skills/nl-tax-intake/reference/filing-paths.md")

        for text in (runtime, intake):
            with self.subTest(document=text[:80]):
                self.assertIn("workflows.annual_2025.requested", text)
                self.assertIn("workflows.provisional_2026.requested", text)
                self.assertIn("status `queued`", text)
                self.assertIn("active_workflow: annual_2025", text)
                self.assertIn("active_skill: nl-tax-annual-return", text)
                self.assertIn("sections.provisional_2026.subflow", text)

        self.assertIn("Keep the provisional section `not_started`", runtime)
        self.assertIn("A queued workflow is saved intent, not a second active owner", intake)
        self.assertIn("queue provisional 2026", filing_paths)
        self.assertIn("queue `change`, not `stopzetten`", intake)

    def test_annual_handoff_is_atomic_and_requires_complete_validated_outputs(self):
        runtime = flattened("skills/_shared/runtime-contract.md")
        assembly = flattened(
            "skills/nl-tax-annual-return/reference/phases/10-assembly.md"
        )

        for text in (runtime, assembly):
            with self.subTest(document=text[:80]):
                self.assertIn("workflows.annual_2025.status: complete", text)
                self.assertIn("workflows.provisional_2026.status: in_progress", text)
                self.assertIn("provisional_2026_<subflow>", text)
                self.assertIn("active_skill: nl-tax-provisional-assessment", text)
                self.assertIn("Preserve", text)

        self.assertIn("workpack and field map have been written and validated", runtime)
        self.assertIn("annual rollup remains `in_progress`", runtime)
        self.assertIn("intentionally `draft`", runtime)
        self.assertIn("Never partially switch ownership", runtime)
        self.assertIn("field map fails validation", assembly)
        self.assertIn("keep `active_workflow: annual_2025`", assembly)
        self.assertIn("`updated_at` values in the same write", assembly)

    def test_handoff_needs_no_reactivation_but_keeps_generation_gates_separate(self):
        runtime = flattened("skills/_shared/runtime-contract.md")
        intake_skill = flattened("skills/nl-tax-intake/SKILL.md")
        annual_skill = flattened("skills/nl-tax-annual-return/SKILL.md")
        provisional_skill = flattened("skills/nl-tax-provisional-assessment/SKILL.md")

        for text in (runtime, intake_skill, annual_skill, provisional_skill):
            with self.subTest(document=text[:80]):
                self.assertIn("activation phrase", text)

        self.assertIn("without another activation phrase", provisional_skill)
        self.assertIn("does not authorize final provisional artifact generation", runtime)
        self.assertIn("does not replace the later provisional final-generation confirmation", annual_skill)
        self.assertIn("Never require exact wording", provisional_skill)
        self.assertIn("reuse the opening preparation request as final consent", provisional_skill)

    def test_owner_contracts_preserve_year_specific_state_and_artifacts(self):
        runtime = flattened("skills/_shared/runtime-contract.md")
        annual = flattened("skills/nl-tax-annual-return/SKILL.md")
        provisional = flattened("skills/nl-tax-provisional-assessment/SKILL.md")

        self.assertIn("never copy an annual amount into provisional state automatically", runtime)
        self.assertIn("Never write `workspace/provisional/**`", annual)
        self.assertIn("Never write `workspace/annual/**`", provisional)
        self.assertIn("Leave the completed annual section", provisional)
        self.assertIn("Do not copy annual actuals into provisional state", provisional)
        self.assertIn("preserve `workflows.annual_2025.status: complete`", provisional)

    def test_source_ledgers_do_not_union_annual_and_provisional_ids(self):
        runtime = flattened("skills/_shared/runtime-contract.md")
        annual_output = flattened(
            "skills/nl-tax-annual-return/reference/annual-output-contract.md"
        )
        provisional_output = flattened(
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        )
        assembly = flattened(
            "skills/nl-tax-annual-return/reference/phases/10-assembly.md"
        )

        self.assertIn("sources_loaded_by_workflow.annual_2025", runtime)
        self.assertIn("sources_loaded_by_workflow.provisional_2026", runtime)
        self.assertIn("exact mirror of the active workflow's list", runtime)
        self.assertIn("never as a union", runtime)
        self.assertIn("older progress file", runtime)
        self.assertIn("sources_loaded_by_workflow.annual_2025", annual_output)
        self.assertIn(
            "sources_loaded_by_workflow.provisional_2026", provisional_output
        )
        self.assertIn("set the top-level `sources_loaded` mirror", assembly)

    def test_structural_fixture_covers_each_transition_and_is_wired(self):
        fixture = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
        dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        expected = fixture["expected_state"]

        intake = expected["after_intake"]
        self.assertIn("prepare both", fixture["user_request"]["text"].lower())
        self.assertIn("do not make me use a slash command", fixture["user_request"]["text"])
        self.assertEqual(intake["session"]["active_workflow"], "annual_2025")
        self.assertEqual(
            intake["profile"]["provisional_2026"]["status"], "queued"
        )

        handoff = expected["after_complete_annual_mapping"]
        self.assertEqual(
            handoff["session"]["active_workflow"], "provisional_2026_request"
        )
        self.assertEqual(
            handoff["session"]["active_skill"], "nl-tax-provisional-assessment"
        )
        self.assertFalse(handoff["requires_new_activation_phrase"])
        self.assertFalse(handoff["provisional_generation_confirmed"])
        self.assertTrue(handoff["annual_artifacts_preserved"])
        self.assertEqual(
            handoff["session"]["sources_loaded_by_workflow"]["annual_2025"],
            ["annual_source_id"],
        )
        self.assertEqual(
            handoff["session"]["sources_loaded_by_workflow"]["provisional_2026"],
            [],
        )
        self.assertEqual(handoff["session"]["sources_loaded"], [])
        self.assertEqual(
            handoff["workpack_source_sections"]["annual_2025"],
            handoff["session"]["sources_loaded_by_workflow"]["annual_2025"],
        )
        self.assertIsNone(
            handoff["workpack_source_sections"]["provisional_2026"]
        )

        finished = expected["after_complete_provisional_mapping"]
        self.assertEqual(finished["profile"]["annual_2025"]["status"], "complete")
        self.assertEqual(
            finished["profile"]["provisional_2026"]["status"], "complete"
        )
        self.assertEqual(finished["session"]["active_skill"], "")
        self.assertEqual(
            finished["session"]["sources_loaded"],
            ["provisional_source_id"],
        )
        for workflow in ("annual_2025", "provisional_2026"):
            with self.subTest(workflow=workflow):
                self.assertEqual(
                    finished["workpack_source_sections"][workflow],
                    finished["session"]["sources_loaded_by_workflow"][workflow],
                )
        self.assertNotIn(
            "provisional_source_id",
            finished["workpack_source_sections"]["annual_2025"],
        )
        self.assertNotIn(
            "annual_source_id",
            finished["workpack_source_sections"]["provisional_2026"],
        )

        cases = {case["id"]: case for case in dataset["cases"]}
        case = cases["annual_then_provisional_request"]
        self.assertEqual(
            case["fixture"],
            "evals/nl-tax-agent-skills/fixtures/annual/dual-workflow-handoff.yaml",
        )
        self.assertIn("annual_then_provisional_request", dataset["contract_default_cases"])
        self.assertIn(
            "workspace/annual/2025/field-map.yaml", case["expected_files"]
        )
        self.assertIn(
            "workspace/provisional/2026/field-map.yaml", case["expected_files"]
        )
        self.assertEqual(
            case["source_ledger_check"]["session_path"],
            "workspace/shared/session-progress.yaml",
        )
        self.assertEqual(
            {rule["workflow"] for rule in case["source_ledger_check"]["workpacks"]},
            {"annual_2025", "provisional_2026"},
        )


if __name__ == "__main__":
    unittest.main()
