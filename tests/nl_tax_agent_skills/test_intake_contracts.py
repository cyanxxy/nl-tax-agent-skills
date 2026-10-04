#!/usr/bin/env python3
"""Contract coverage for intake routing and workpack resume-record semantics.

0.4 replaced the profile template and the session-progress ledger with the
conversation plus Appendix A (resume record) of the one consented workpack.
"""

import json
import pathlib
import re
import unittest

import yaml


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)
SUPPORTED_WORKFLOWS = (
    ROOT.parents[1]
    / "tools/nl_tax_agent_skills/source_maintenance/supported-workflows.yaml"
)
ANNUAL_TEMPLATE = "skills/nl-tax-annual-return/templates/annual-workpack.md"
PROVISIONAL_TEMPLATE = (
    "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md"
)
ELICITATION = (
    "skills/nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md"
)


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def compact(text):
    return " ".join(text.split())


def load_supported_workflows():
    return yaml.safe_load(SUPPORTED_WORKFLOWS.read_text(encoding="utf-8"))


def section(text, heading):
    marker = f"\n## {heading}\n"
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    return text[start:] if end == -1 else text[start:end]


def resume_record(relative_path):
    """Parse the one fenced yaml block of a template's Appendix A."""
    block = section(read_text(relative_path), "Appendix A — Resume record")
    blocks = re.findall(r"```yaml\n(.*?)\n```", block, re.DOTALL)
    assert len(blocks) == 1, blocks
    return yaml.safe_load(blocks[0])


REVIEW_READY_STATUSES = {"complete", "chat_only"}


def completed_annual_state():
    state = resume_record(ANNUAL_TEMPLATE)
    for entry in state["sections"].values():
        entry["status"] = "complete"
    return state


def completed_provisional_state():
    state = resume_record(PROVISIONAL_TEMPLATE)
    for entry in state["sections"].values():
        entry["status"] = "complete"
    return state


def readiness(state):
    """The R6 rollup: review_ready only when every section is complete or
    chat_only and no section still lists an open question."""
    sections = state["sections"].values()
    return (
        "review_ready"
        if all(
            item["status"] in REVIEW_READY_STATUSES and not item.get("open")
            for item in sections
        )
        else "draft"
    )


class IntakeContractTests(unittest.TestCase):
    def test_finite_choice_intake_prefers_return_capable_controls(self):
        runtime = read_text("skills/nl-tax-shared-resources/runtime-contract.md")
        contract = read_text("skills/nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md")
        intake = read_text("skills/nl-tax-intake/SKILL.md")

        for text in (runtime, contract, intake):
            with self.subTest(document=text[:40]):
                self.assertIn("return-capable", text)
                self.assertIn("same conversation", text)
        self.assertIn("Do not use a display-only visual", intake)
        self.assertIn("four-option limit", intake)
        self.assertIn("AskUserQuestion", intake)
        self.assertIn("a chat fact with `U:` provenance", compact(intake))
        self.assertIn("source: user_chat", runtime)

    def test_claude_host_rules_distinguish_cowork_from_claude_code(self):
        runtime = read_text("skills/nl-tax-shared-resources/runtime-contract.md")
        intake = read_text("skills/nl-tax-intake/SKILL.md")

        for text in (runtime, intake):
            with self.subTest(document=text[:40]):
                self.assertIn("Claude chat or Cowork", text)
                self.assertIn("Claude Code", text)
                self.assertIn("custom HTML visual", text)
                self.assertIn("not a guaranteed Cowork", text)
                self.assertIn("AskUserQuestion", text)
                self.assertIn("Codex", text)

    def test_resume_record_schema_and_chat_only_gate_match_templates(self):
        contract = read_text(ELICITATION)
        release_version = json.loads(read_text(".codex-plugin/plugin.json"))["version"]
        for template in (ANNUAL_TEMPLATE, PROVISIONAL_TEMPLATE):
            record = resume_record(template)
            with self.subTest(template=template):
                self.assertEqual(record["workpack_format"], "nl-tax-workpack")
                self.assertEqual(record["workpack_version"], "2.0")
                self.assertEqual(record["plugin_version"], release_version)
                self.assertIn(record["readiness"], {"draft", "review_ready"})
                self.assertIs(record["generation_confirmed"], False)
                for entry in record["sections"].values():
                    self.assertEqual(entry, {"status": "not_started", "open": []})
        self.assertIn('workpack_version: "2.0"', contract)
        self.assertNotIn("session_progress_version", contract)
        self.assertIn("not_started | in_progress | complete | chat_only | deferred", contract)
        self.assertIn("`complete`, `chat_only`, or `deferred`", compact(contract))

    def test_manual_review_route_is_terminal_and_conversation_only(self):
        intake = compact(read_text("skills/nl-tax-intake/SKILL.md"))
        flow = compact(read_text("skills/nl-tax-intake/reference/intake-flow.md"))

        self.assertIn("`manual_review`, `unsupported`, or a specific blocked label", intake)
        self.assertIn("prepare no workpack or partial calculation", intake)
        self.assertIn("| `manual_review` | Terminal:", flow)
        self.assertIn("complex Box 2", flow)
        self.assertIn(
            "Start no workflow, prepare no workpack or partial calculation, and "
            "write no file. The outcome lives only in the conversation.",
            flow,
        )
        # The 0.3 profile template and its intake_status ledger are retired.
        self.assertFalse((ROOT / "skills/nl-tax-intake/templates").exists())
        self.assertNotIn("intake_status", intake)

    def test_supported_blocked_candidates_are_reachable_from_intake(self):
        supported = load_supported_workflows()
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
            "annual_2025_deceased_f_form",
            "annual_2025_foreign_treaty_heavy",
        }

        self.assertTrue(expected.issubset(blocked_candidates), blocked_candidates)
        drafts = {wf["id"]: wf for wf in supported["draft_only_workflows"]}
        self.assertEqual(drafts["international_2025"]["maximum_readiness"], "draft")
        self.assertIn("nl-tax-international-return", intake_contract)
        for candidate in expected:
            with self.subTest(candidate=candidate):
                self.assertIn(candidate, intake_contract)

    def test_manual_review_is_terminal_supported_workflow_route(self):
        supported = load_supported_workflows()
        terminal_by_id = {
            workflow.get("id"): workflow
            for workflow in supported.get("terminal_workflows", [])
        }

        manual_review = terminal_by_id["manual_review"]
        self.assertEqual(manual_review["status"], "terminal_manual_review")
        self.assertIs(manual_review["may_prepare_workpack"], False)
        self.assertIn("manual_review", manual_review["profile_candidates"])
        # Terminal and blocked routes write nothing (0.4 design R1).
        self.assertEqual(manual_review["allowed_output"], "conversation_only")
        for group in ("terminal_workflows", "blocked_workflows"):
            for workflow in supported.get(group, []):
                with self.subTest(workflow=workflow["id"]):
                    self.assertEqual(workflow["allowed_output"], "conversation_only")
                    self.assertFalse(workflow.get("output_paths"))

    def test_aow_status_is_rule_derived_without_becoming_a_workflow_engine(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        household_section = compact(intake[intake.index("### Household composition") :])

        self.assertIn("reaches_during_year", household_section)
        self.assertIn("transition_month", household_section)
        self.assertIn("Keep 2025 and 2026 as separate entries", household_section)
        self.assertIn("calculated (`C:` from date of birth and tax year)", household_section)
        self.assertIn("do not create an assumption", household_section)
        # Each workflow's profile summary carries only its own year's AOW rows.
        annual = section(read_text(ANNUAL_TEMPLATE), "Taxpayer profile summary")
        provisional = section(read_text(PROVISIONAL_TEMPLATE), "Taxpayer profile summary")
        for who in ("person", "partner"):
            with self.subTest(who=who):
                self.assertIn(f"`{who}.aow_by_tax_year.2025.status`", annual)
                self.assertIn(f"`{who}.aow_by_tax_year.2025.transition_month`", annual)
                self.assertNotIn(f"{who}.aow_by_tax_year.2026", annual)
                self.assertIn(f"`{who}.aow_by_tax_year.2026.status`", provisional)
                self.assertIn(f"`{who}.aow_by_tax_year.2026.transition_month`", provisional)
                self.assertNotIn(f"{who}.aow_by_tax_year.2025", provisional)

    def test_intake_uses_a_conversation_ledger_not_a_decision_tree(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        filing_paths = read_text("skills/nl-tax-intake/reference/filing-paths.md")
        contract = read_text(
            "skills/nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md"
        )

        self.assertIn("conversational, not a fixed interview", intake)
        self.assertIn("let the conversation set the order", compact(intake))
        self.assertIn("not a fixed questionnaire or decision tree", filing_paths)
        self.assertIn("They are a record, not a state machine", compact(contract))
        self.assertNotIn("Decision Tree for Workflow Selection", filing_paths)

    def test_explicit_preparation_continues_without_internal_reactivation(self):
        runtime = read_text("skills/nl-tax-shared-resources/runtime-contract.md")
        intake = read_text("skills/nl-tax-intake/SKILL.md")

        self.assertIn("continue naturally", runtime)
        self.assertIn("continue directly in\nthe same conversation", intake)
        self.assertIn("do not\nrequire a second activation phrase", intake)

    def test_interactive_contract_aligns_draft_generation_with_output_contracts(self):
        contract = read_text("skills/nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md")

        self.assertNotIn('explicit "DRAFT - incomplete" markers', contract)
        self.assertIn("output contract", contract)

    def test_filing_paths_record_annual_2025_status_without_deciding_for_user(self):
        filing_paths = read_text("skills/nl-tax-intake/reference/filing-paths.md")

        self.assertIn("invitation letter", filing_paths)
        self.assertIn("no invitation", filing_paths)
        self.assertIn("14 July 2026", filing_paths)
        self.assertIn("filing_obligation_unresolved", filing_paths)
        self.assertIn("Do not infer scheme entitlement", filing_paths)
        self.assertNotIn("March-April 2026", filing_paths)

    def test_resume_record_tracks_annual_and_provisional_winst(self):
        annual = resume_record(ANNUAL_TEMPLATE)
        provisional = resume_record(PROVISIONAL_TEMPLATE)
        contract = compact(read_text(ELICITATION))

        self.assertEqual(annual["workflow"], "annual_2025")
        self.assertEqual(annual["tax_year"], 2025)
        self.assertIn("winst", annual["sections"])
        self.assertEqual(provisional["tax_year"], 2026)
        self.assertIn("winst_forecast", provisional["sections"])
        self.assertIn(
            "Annual `winst` and provisional `winst_forecast` are generation-gate members",
            contract,
        )

    def test_unfinished_winst_blocks_annual_review_readiness(self):
        state = completed_annual_state()
        self.assertEqual(readiness(state), "review_ready")
        state["sections"]["winst"]["status"] = "in_progress"

        self.assertEqual(readiness(state), "draft")

    def test_deferred_annual_subsection_keeps_draft_readiness(self):
        state = completed_annual_state()
        state["sections"]["box3_actual"]["status"] = "deferred"
        state["sections"]["box3_actual"]["open"] = ["Q007"]

        self.assertEqual(readiness(state), "draft")

    def test_open_question_keeps_draft_even_when_sections_are_complete(self):
        state = completed_annual_state()
        state["sections"]["box1"]["open"] = ["Q001"]

        self.assertEqual(readiness(state), "draft")

    def test_unfinished_winst_forecast_blocks_provisional_review_readiness(self):
        for unfinished_status in ("in_progress", "not_started"):
            state = completed_provisional_state()
            state["sections"]["winst_forecast"]["status"] = unfinished_status

            with self.subTest(status=unfinished_status):
                self.assertEqual(readiness(state), "draft")

    def test_intake_writes_nothing_and_the_owning_workflow_records_facts(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        flow = compact(read_text("skills/nl-tax-intake/reference/intake-flow.md"))
        annual = compact(read_text("skills/nl-tax-annual-return/SKILL.md"))
        provisional = compact(read_text("skills/nl-tax-provisional-assessment/SKILL.md"))

        self.assertIn("**Intake writes nothing.**", intake)
        self.assertNotIn("Edit(", intake.split("---", 2)[1])
        self.assertIn("Intake writes no file at any point.", flow)
        self.assertIn(
            "Intake writes nothing: no profile, ledger, missing-information, "
            "assumption, or workpack file.",
            flow,
        )
        self.assertIn("records these facts in its workpack's", compact(intake))
        self.assertIn("take intake's screened facts from this conversation", annual)
        self.assertIn("if intake is complete, never restart it", annual)
        self.assertIn("Never restart a completed intake", provisional)
        for workflow in (annual, provisional):
            with self.subTest(workflow=workflow[:40]):
                self.assertNotIn("require intake to create it", workflow)

    def test_legacy_ledgers_are_never_read_or_migrated(self):
        runtime = compact(read_text("skills/nl-tax-shared-resources/runtime-contract.md"))
        intake = compact(read_text("skills/nl-tax-intake/SKILL.md"))
        contract = read_text(ELICITATION)

        self.assertIn(
            "0.3 `workspace/` ledgers are not migrated: never read or write "
            "`profile.yaml`, `session-progress.yaml`, or `evidence-index.yaml`.",
            runtime,
        )
        self.assertIn(
            "0.3 ledgers (`profile.yaml`, `session-progress.yaml`, "
            "`evidence-index.yaml`) are never read or written.",
            intake,
        )
        self.assertNotIn("migrate older\nsession state in place", contract)
        self.assertIn("not applicable", contract)
        for retired in (
            "skills/nl-tax-shared-resources/templates",
            "skills/nl-tax-intake/templates/taxpayer-profile.yaml",
        ):
            with self.subTest(retired=retired):
                self.assertFalse((ROOT / retired).exists())


if __name__ == "__main__":
    unittest.main()
