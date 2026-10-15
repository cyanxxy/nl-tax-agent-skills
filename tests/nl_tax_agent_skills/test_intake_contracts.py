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


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


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
    def test_resume_record_schema_and_chat_only_gate_match_templates(self):
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

    def test_manual_review_route_is_terminal_and_conversation_only(self):
        # The 0.3 profile template and its intake_status ledger are retired.
        self.assertFalse((ROOT / "skills/nl-tax-intake/templates").exists())

    def test_supported_blocked_candidates_are_reachable_from_intake(self):
        supported = load_supported_workflows()

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

    def test_resume_record_tracks_annual_and_provisional_winst(self):
        annual = resume_record(ANNUAL_TEMPLATE)
        provisional = resume_record(PROVISIONAL_TEMPLATE)

        self.assertEqual(annual["workflow"], "annual_2025")
        self.assertEqual(annual["tax_year"], 2025)
        self.assertIn("winst", annual["sections"])
        self.assertEqual(provisional["tax_year"], 2026)
        self.assertIn("winst_forecast", provisional["sections"])

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

        self.assertNotIn("Edit(", intake.split("---", 2)[1])

    def test_legacy_ledgers_are_never_read_or_migrated(self):
        for retired in (
            "skills/nl-tax-shared-resources/templates",
            "skills/nl-tax-intake/templates/taxpayer-profile.yaml",
        ):
            with self.subTest(retired=retired):
                self.assertFalse((ROOT / retired).exists())


if __name__ == "__main__":
    unittest.main()
