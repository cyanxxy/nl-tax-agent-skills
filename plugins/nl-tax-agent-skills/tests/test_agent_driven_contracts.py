#!/usr/bin/env python3
"""Regression coverage for the agent-driven conversational contracts."""

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_validator():
    path = ROOT / "skills/nl-tax-field-mapper/scripts/validate_field_map.py"
    spec = importlib.util.spec_from_file_location("agent_driven_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentDrivenContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_complete_box3_chat_inputs_are_not_deferred(self):
        paths = [
            "skills/nl-tax-annual-return/reference/annual-output-contract.md",
            "skills/nl-tax-annual-return/reference/phases/04-box3.md",
            "skills/nl-tax-box3/reference/box3-annual-2025.md",
            "skills/nl-tax-annual-return/templates/annual-return-pack.md",
        ]
        for path in paths:
            text = read_text(path)
            with self.subTest(path=path):
                self.assertIn("chat_only", text)
                self.assertNotIn("all required actual-return evidence", text)
                self.assertNotIn("complete evidence", text)

    def test_declining_optional_box3_comparison_is_complete(self):
        paths = [
            "skills/nl-tax-annual-return/reference/annual-output-contract.md",
            "skills/nl-tax-annual-return/reference/phases/04-box3.md",
            "skills/nl-tax-box3/reference/box3-annual-2025.md",
            "skills/nl-tax-annual-return/templates/annual-return-pack.md",
        ]
        for path in paths:
            text = " ".join(read_text(path).split())
            with self.subTest(path=path):
                self.assertIn("not supplied by choice", text)
                self.assertIn("complete", text)

    def test_wajong_requires_a_dedicated_answer(self):
        phase = read_text(
            "skills/nl-tax-annual-return/reference/phases/05-5-credits.md"
        )
        output = read_text(
            "skills/nl-tax-annual-return/reference/annual-output-contract.md"
        )
        for text in (phase, output):
            self.assertIn("annual.credits.young_disabled_status", text)
            self.assertIn("broad", text)
            self.assertIn("ouderenkorting", text)
        self.assertIn("Do not mark credits screening", phase)

    def test_chat_values_update_evidence_ledger(self):
        shared = read_text(
            "skills/_shared/knowledge/methods/interactive-elicitation.md"
        )
        annual = read_text("skills/nl-tax-annual-return/SKILL.md")
        for text in (shared, annual):
            self.assertIn("sections.evidence.subsections.user_chat_values", text)
        self.assertIn("never simultaneously", shared)

    def test_aow_screen_uses_calculated_provenance(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        aow = read_text("skills/_shared/knowledge/aow/aow-leeftijd.md")
        profile = read_text(
            "skills/nl-tax-intake/templates/taxpayer-profile.yaml"
        )
        for text in (intake, aow, profile):
            self.assertIn("calculated", text)
        self.assertNotIn("AOW-age status derived from DOB", intake)

    def test_preflight_does_not_preload_irrelevant_sources(self):
        preflight = read_text(
            "skills/nl-tax-annual-return/reference/phases/01-preflight.md"
        )
        filing = read_text(
            "skills/nl-tax-annual-return/reference/phases/01-5-filing-status.md"
        )
        self.assertIn("Do **not** load any file", preflight)
        self.assertNotIn("Load every file in this list", preflight)
        self.assertIn("An on-time case must not", filing)
        self.assertIn("stale-check", filing)
        self.assertIn("bare label", filing)

    def test_workflow_owns_chat_without_evidence_index_requirement(self):
        indexer = read_text("skills/nl-tax-evidence-indexer/SKILL.md")
        preflight = read_text(
            "skills/nl-tax-annual-return/reference/phases/01-preflight.md"
        )
        self.assertIn("Do not invoke this indexer solely", indexer)
        self.assertIn("pure chat collection does not require", indexer)
        self.assertIn("absence of an evidence index", preflight)

    def test_rollup_precedes_mapping_and_regeneration_resets_confirmation(self):
        annual = read_text("skills/nl-tax-annual-return/SKILL.md")
        annual_flat = " ".join(annual.split())
        before_mapper = annual.index("Before invoking the mapper")
        invoke_mapper = annual.index("After the confirmed workpack is written")
        self.assertLess(before_mapper, invoke_mapper)
        self.assertIn("reset the `confirm` subsection", annual_flat)
        self.assertIn("fresh exact generation phrase", annual_flat)

    def test_confirmed_workpack_authorizes_companion_map(self):
        mapper = read_text("skills/nl-tax-field-mapper/SKILL.md")
        self.assertIn("no second mapping request is needed", mapper)

    def test_internal_orchestration_is_invisible(self):
        runtime = read_text("skills/_shared/runtime-contract.md")
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        mapper = read_text("skills/nl-tax-field-mapper/SKILL.md")
        self.assertIn("Invisible orchestration", runtime)
        self.assertIn("Never mention internal skill names", intake)
        self.assertIn("never announce", mapper)

    def test_failed_commands_and_speculative_paths_are_forbidden(self):
        runtime = read_text("skills/_shared/runtime-contract.md")
        annual = read_text("skills/nl-tax-annual-return/SKILL.md")
        runtime_flat = " ".join(runtime.split())
        plugin_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "skills").rglob("*.md")
        )
        self.assertIn("A nonzero exit is never a successful check", runtime_flat)
        self.assertIn(
            "Do not assume the taxpayer workspace is a Git repository",
            runtime_flat,
        )
        self.assertIn("Do not probe speculative template names", annual)
        self.assertNotIn("return-pack-template.md", plugin_text)

    def test_agent_declared_draft_cannot_be_promoted(self):
        fields = [
            {
                "field_id": "box1.loon",
                "value": 50000,
                "source": {"type": "evidence", "evidence_id": "ev1"},
            },
            {
                "field_id": "box1.loonheffing",
                "value": 12000,
                "source": {"type": "evidence", "evidence_id": "ev2"},
            },
        ]
        result = self.validator._readiness_for(
            {
                "workflow": "annual_return",
                "tax_year": 2025,
                "readiness": "draft",
                "fields": fields,
                "missing_fields": [],
            }
        )
        self.assertTrue(result["structurally_ready"])
        self.assertFalse(result["ready"])
        self.assertEqual("draft", result["declared"])


if __name__ == "__main__":
    unittest.main()
