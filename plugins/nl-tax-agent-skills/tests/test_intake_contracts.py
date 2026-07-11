#!/usr/bin/env python3
"""Contract coverage for intake routing and session-progress semantics."""

import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_yaml(relative_path):
    return yaml.safe_load(read_text(relative_path))


TERMINAL_STATUSES = {"complete", "chat_only", "deferred"}


def completed_annual_state():
    state = load_yaml("skills/_shared/templates/session-progress.yaml")
    for subsection in state["sections"]["annual_2025"]["subsections"].values():
        subsection["status"] = "complete"
    return state


def completed_provisional_state():
    state = load_yaml("skills/_shared/templates/session-progress.yaml")
    for subsection in state["sections"]["provisional_2026"]["subsections"].values():
        subsection["status"] = "complete"
    return state


def readiness(state, workflow="annual_2025"):
    subsections = state["sections"][workflow]["subsections"].values()
    return (
        "review_ready"
        if all(item["status"] in TERMINAL_STATUSES for item in subsections)
        else "draft"
    )


class IntakeContractTests(unittest.TestCase):
    def test_session_progress_schema_version_and_chat_only_gate_match_template(self):
        template = load_yaml("skills/_shared/templates/session-progress.yaml")
        contract = read_text("skills/_shared/knowledge/methods/interactive-elicitation.md")

        self.assertEqual(template["session_progress_version"], "1.4")
        self.assertIn("Schema (v1.4", contract)
        self.assertIn("last_question_asked", template)
        self.assertIn("not_started | in_progress | complete | chat_only | deferred", contract)
        self.assertIn("`complete`, `chat_only`, or `deferred`", contract)

    def test_profile_template_represents_manual_review_terminal_route(self):
        profile = load_yaml("skills/nl-tax-intake/templates/taxpayer-profile.yaml")
        profile_text = read_text("skills/nl-tax-intake/templates/taxpayer-profile.yaml")
        intake = read_text("skills/nl-tax-intake/SKILL.md")

        self.assertIn("intake_status", profile)
        self.assertIn("manual_review", profile_text)
        self.assertIn("complex_box2_screening", profile_text)
        self.assertEqual(profile["manual_review"]["required"]["value"], False)
        self.assertIn("workflow_candidate: manual_review", intake)
        self.assertIn("intake_status: complete", intake)

    def test_supported_blocked_candidates_are_reachable_from_intake(self):
        supported = load_yaml("skills/_shared/supported-workflows.yaml")
        intake_contract = (
            read_text("skills/nl-tax-intake/SKILL.md")
            + "\n"
            + read_text("skills/nl-tax-intake/reference/unsupported-cases.md")
        )

        blocked_candidates = {
            candidate
            for workflow in supported["blocked_workflows"]
            for candidate in workflow.get("profile_candidates", [])
            if candidate.startswith("annual_2025_")
        }
        expected = {
            "annual_2025_entrepreneurs",
            "annual_2025_nonresident_c_form",
            "annual_2025_migration_m_form",
            "annual_2025_deceased_f_form",
            "annual_2025_foreign_treaty_heavy",
        }

        self.assertTrue(expected.issubset(blocked_candidates), blocked_candidates)
        for candidate in expected:
            with self.subTest(candidate=candidate):
                self.assertIn(candidate, intake_contract)

    def test_manual_review_is_terminal_supported_workflow_route(self):
        supported = load_yaml("skills/_shared/supported-workflows.yaml")
        terminal_by_id = {
            workflow.get("id"): workflow
            for workflow in supported.get("terminal_workflows", [])
        }

        manual_review = terminal_by_id["manual_review"]
        self.assertEqual(manual_review["status"], "terminal_manual_review")
        self.assertIs(manual_review["may_prepare_workpack"], False)
        self.assertIn("manual_review", manual_review["profile_candidates"])
        self.assertEqual(manual_review["allowed_output"], "workspace/shared/missing-info.md")

    def test_aow_assumption_requires_assumption_id(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        household_section = intake[intake.index("### Household composition") :]

        self.assertIn("aow_age_in_tax_year", household_section)
        self.assertIn("assumption_id", household_section)
        self.assertIn("assumptions.md", household_section)

    def test_interactive_contract_aligns_draft_generation_with_output_contracts(self):
        contract = read_text("skills/_shared/knowledge/methods/interactive-elicitation.md")

        self.assertNotIn('explicit "DRAFT - incomplete" markers', contract)
        self.assertIn("output contract", contract)

    def test_filing_paths_route_annual_2025_deadline_by_invitation_status(self):
        filing_paths = read_text("skills/nl-tax-intake/reference/filing-paths.md")

        self.assertIn("invitation letter", filing_paths)
        self.assertIn("no invitation", filing_paths)
        self.assertIn("14 July 2026", filing_paths)
        self.assertIn("do not invent a filing deadline", filing_paths)
        self.assertNotIn("March-April 2026", filing_paths)

    def test_session_tracks_annual_and_provisional_winst(self):
        state = load_yaml("skills/_shared/templates/session-progress.yaml")
        contract = read_text("skills/_shared/knowledge/methods/interactive-elicitation.md")

        self.assertEqual(state["session_progress_version"], "1.4")
        self.assertIn("winst", state["sections"]["annual_2025"]["subsections"])
        self.assertIn(
            "winst_forecast",
            state["sections"]["provisional_2026"]["subsections"],
        )
        self.assertIn("Schema (v1.4", contract)

    def test_unfinished_winst_blocks_annual_review_readiness(self):
        state = completed_annual_state()
        state["sections"]["annual_2025"]["subsections"]["winst"]["status"] = (
            "in_progress"
        )

        self.assertEqual(readiness(state), "draft")

    def test_unfinished_winst_forecast_blocks_provisional_review_readiness(self):
        for unfinished_status in ("in_progress", "not_started"):
            state = completed_provisional_state()
            state["sections"]["provisional_2026"]["subsections"][
                "winst_forecast"
            ]["status"] = unfinished_status

            with self.subTest(status=unfinished_status):
                self.assertEqual(readiness(state, "provisional_2026"), "draft")

    def test_intake_alone_creates_session_state(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        contract = read_text("skills/_shared/knowledge/methods/interactive-elicitation.md")
        annual = read_text("skills/nl-tax-annual-return/SKILL.md")
        provisional = read_text("skills/nl-tax-provisional-assessment/SKILL.md")

        self.assertIn("sole creator of `workspace/shared/session-progress.yaml`", intake)
        self.assertIn("Only `nl-tax-intake` creates", contract)
        for workflow in (annual, provisional):
            with self.subTest(workflow=workflow[:40]):
                self.assertIn("require intake to create it", workflow)
                self.assertNotIn("reconstruct it from `profile.yaml`", workflow)

    def test_schema_14_documents_legacy_resume_migration(self):
        contract = read_text("skills/_shared/knowledge/methods/interactive-elicitation.md")

        self.assertIn("migrate older\nsession state in place", contract)
        self.assertIn("annual_2025.subsections.winst", contract)
        self.assertIn("provisional_2026.subsections.winst_forecast", contract)
        self.assertIn("not applicable", contract)


if __name__ == "__main__":
    unittest.main()
