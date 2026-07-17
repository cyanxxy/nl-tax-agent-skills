#!/usr/bin/env python3
"""Regression coverage for the agent-driven conversational contracts."""

import importlib.util
import pathlib
import unittest


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)


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
        annual = read_text(
            "skills/nl-tax-annual-return/reference/annual-flow.md"
        )
        for text in (shared, annual):
            self.assertIn("sections.evidence.subsections.user_chat_values", text)
        self.assertIn(
            "reference/annual-flow.md",
            read_text("skills/nl-tax-annual-return/SKILL.md"),
        )
        self.assertIn("never simultaneously", shared)

    def test_provisional_owner_restores_chat_loop_and_exact_generation_gate(self):
        skill = read_text(
            "skills/nl-tax-provisional-assessment/SKILL.md"
        )
        flow = read_text(
            "skills/nl-tax-provisional-assessment/reference/provisional-flow.md"
        )
        for phrase in (
            "After every user reply",
            "source: user_chat",
            "stated_at",
            "sections.evidence.subsections.user_chat_values.answered",
            "workspace/shared/missing-info.md",
            "same `session-progress.yaml` write",
        ):
            self.assertIn(phrase, flow)
        for status in ("not_started", "in_progress", "complete", "chat_only", "deferred"):
            self.assertIn(f"`{status}`", skill)
        self.assertIn("`box2` and `winst_forecast` are always gate members", skill)
        self.assertIn("profile fact or user\nanswer", skill)

    def test_box1_helper_returns_questions_to_owner_only(self):
        for relative in (
            "skills/nl-tax-box1-home/reference/box1-2025.md",
            "skills/nl-tax-box1-home/reference/own-home-2025.md",
        ):
            text = read_text(relative)
            with self.subTest(relative=relative):
                self.assertNotIn("workspace/shared/review-questions.md", text)
                self.assertIn("owning workflow", " ".join(text.split()))

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

    def test_completed_intake_does_not_compete_with_active_workflow(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        description = intake.split("---", 2)[1]

        self.assertIn("Do not use", description)
        self.assertIn("after intake is complete", description)
        self.assertIn("intake is no longer an active skill", intake)

    def test_phase_gate_stops_credit_preloading(self):
        skill = read_text("skills/nl-tax-annual-return/SKILL.md")
        flow = read_text("skills/nl-tax-annual-return/reference/annual-flow.md")
        deductions = read_text(
            "skills/nl-tax-annual-return/reference/phases/05-deductions.md"
        )
        credits = read_text(
            "skills/nl-tax-annual-return/reference/phases/05-5-credits.md"
        )

        self.assertIn("never preload\nPhase N+2", skill)
        self.assertIn("Phase N+2 cannot be loaded", flow)
        self.assertIn("do not\nload Phase 5.5", deductions)
        self.assertIn("Never preload this phase", credits)

    def test_taxpayer_turns_do_not_scan_package_or_eval_surfaces(self):
        runtime = read_text("skills/_shared/runtime-contract.md")

        for phrase in (
            "resource allowlist",
            "package-wide `rg --files`",
            "Never read `.eval/`",
            "do not load intake resources again",
        ):
            self.assertIn(phrase, runtime)

    def test_savings_only_box3_does_not_request_year_end_bank_balance(self):
        phase = read_text(
            "skills/nl-tax-annual-return/reference/phases/04-box3.md"
        )
        helper = read_text("skills/nl-tax-box3/SKILL.md")
        annual_reference = read_text(
            "skills/nl-tax-box3/reference/box3-annual-2025.md"
        )
        actual_reference = read_text(
            "skills/nl-tax-box3/reference/box3-actual-2025.md"
        )
        checklist = read_text(
            "skills/_shared/knowledge/years/2025/annual/evidence-checklist.md"
        )

        for label, text in {
            "phase": phase,
            "helper": helper,
            "annual_reference": annual_reference,
            "actual_reference": actual_reference,
            "checklist": checklist,
        }.items():
            with self.subTest(document=label):
                flattened = " ".join(text.split())
                self.assertIn("31 December", flattened)
                self.assertIn("interest", flattened.lower())
        self.assertNotIn(
            "Collect values for the same categories on 31 December 2025", phase
        )
        self.assertNotIn(
            "need BOTH 1 January AND 31 December positions", annual_reference
        )
        self.assertNotIn(
            "balances on 1 January 2025 and 31 December 2025", checklist
        )

    def test_provisional_change_warns_before_first_questions(self):
        canonical = (
            "Prepare and verify the complete dataset; the change form "
            "requires all applicable categories, not only the changed item."
        )
        skill = " ".join(
            read_text("skills/nl-tax-provisional-assessment/SKILL.md").split()
        )
        flow = " ".join(
            read_text(
                "skills/nl-tax-provisional-assessment/reference/provisional-flow.md"
            ).split()
        )
        change = " ".join(
            read_text(
                "skills/nl-tax-provisional-assessment/reference/subflows/change.md"
            ).split()
        )

        for text in (skill, flow, change):
            self.assertIn(canonical, text)
        self.assertIn("If intake state is absent", skill)
        self.assertIn("as soon as intake records the change candidate", skill)
        self.assertIn("with valid intake state", flow)
        self.assertIn("without replaying completed setup", flow)
        self.assertIn("before baseline or intake follow-up questions", change)

    def test_workflow_owns_chat_without_evidence_index_requirement(self):
        indexer = read_text("skills/nl-tax-evidence-indexer/SKILL.md")
        preflight = read_text(
            "skills/nl-tax-annual-return/reference/phases/01-preflight.md"
        )
        self.assertIn("Do not invoke this indexer solely", indexer)
        self.assertIn("pure chat collection does not require", indexer)
        self.assertIn("absence of an evidence index", preflight)

    def test_rollup_precedes_mapping_and_regeneration_resets_confirmation(self):
        annual = read_text(
            "skills/nl-tax-annual-return/reference/phases/10-assembly.md"
        )
        annual_flat = " ".join(annual.split())
        before_mapper = annual.index("Before mapping")
        invoke_mapper = annual.index("Then\ninvoke `nl-tax-field-mapper`")
        self.assertLess(before_mapper, invoke_mapper)
        self.assertIn("reset the `confirm` subsection", annual_flat)
        self.assertIn("fresh contextual confirmation", annual_flat)
        self.assertIn("immediately preceding scoped question", annual_flat)
        self.assertIn("Never require an exact phrase", annual_flat)
        self.assertNotIn("exact generation phrase", annual_flat)
        self.assertIn(
            "reference/phases/10-assembly.md",
            read_text("skills/nl-tax-annual-return/SKILL.md"),
        )

    def test_workpack_and_checklist_confirmation_is_semantic(self):
        annual = read_text(
            "skills/nl-tax-annual-return/reference/phases/10-assembly.md"
        ).lower()
        provisional = read_text(
            "skills/nl-tax-provisional-assessment/SKILL.md"
        ).lower()
        mapper = read_text("skills/nl-tax-field-mapper/reference/mapper-flow.md").lower()

        for text in (annual, provisional):
            self.assertIn("immediate", text)
            self.assertIn("go ahead", text)
            self.assertTrue(
                "never require exact" in text
                or "never require an exact phrase" in text
                or "no exact wording" in text
                or "no magic phrase" in text
            )
        self.assertIn("offer", mapper)
        self.assertIn("checklist", mapper)
        self.assertIn("unambiguous affirmative reply", mapper)
        self.assertIn("do not create it solely because", mapper)

    def test_confirmed_workpack_authorizes_companion_map(self):
        mapper = read_text("skills/nl-tax-field-mapper/SKILL.md")
        self.assertIn("no second mapping request is needed", mapper)

    def test_mapper_loads_only_its_local_conversation_contract(self):
        skill = read_text("skills/nl-tax-field-mapper/SKILL.md")
        flow = read_text("skills/nl-tax-field-mapper/reference/mapper-flow.md")
        combined = f"{skill}\n{flow}"

        self.assertNotIn("interactive-elicitation.md", combined)
        self.assertIn("do not replay intake or impose a fixed", flow)

    def test_mapper_review_flags_use_case_sensitive_agent_judgment(self):
        principles = read_text(
            "skills/nl-tax-field-mapper/reference/mapping-principles.md"
        )

        self.assertIn("not as a decision engine", principles)
        self.assertIn("There is no universal euro amount", principles)
        self.assertNotIn("EUR 5,000", principles)
        self.assertNotIn("more than 20%", principles)
        self.assertNotIn("Confidence is below 0.7", principles)

    def test_internal_orchestration_is_invisible(self):
        runtime = read_text("skills/_shared/runtime-contract.md")
        intake = read_text("skills/nl-tax-intake/SKILL.md")
        mapper = read_text("skills/nl-tax-field-mapper/SKILL.md")
        self.assertIn("Invisible orchestration", runtime)
        self.assertIn("Never mention internal skill names", intake)
        self.assertIn("never announce", mapper)

    def test_subagent_reviews_preserve_one_agent_owned_workflow(self):
        runtime = read_text("skills/_shared/runtime-contract.md")
        annual = read_text("skills/nl-tax-annual-return/SKILL.md")
        provisional = read_text("skills/nl-tax-provisional-assessment/SKILL.md")
        elicitation = read_text(
            "skills/_shared/knowledge/methods/interactive-elicitation.md"
        )
        runtime_flat = " ".join(runtime.split())
        self.assertIn("only writer, user-question asker", runtime)
        self.assertIn("never a second tax workflow", runtime_flat)
        self.assertIn("public official sources", runtime)
        self.assertIn("only read/research capabilities", runtime_flat)
        self.assertIn("Never grant Bash, Write, Edit", runtime)
        self.assertIn("connectors, MCP tools", runtime)
        self.assertIn("returns that request to the owner", runtime_flat)
        self.assertIn("do the review inline instead", runtime_flat)
        self.assertNotIn("run the plugin's optional mechanical checks", runtime_flat)
        self.assertIn("sole writer", " ".join(annual.split()))
        self.assertIn("sole writer", " ".join(provisional.split()))
        self.assertIn(
            "one active owning workflow and one canonical-state writer",
            elicitation,
        )

    def test_progress_files_record_state_without_owning_the_dialogue(self):
        runtime = read_text("skills/_shared/runtime-contract.md")
        runtime_flat = " ".join(runtime.split())
        elicitation = read_text(
            "skills/_shared/knowledge/methods/interactive-elicitation.md"
        )
        contributing = (ROOT.parents[1] / "CONTRIBUTING.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("conversation ledger, not a workflow executor", runtime)
        self.assertIn("do not choose the next question", runtime_flat)
        self.assertIn("conversation ledger, not a\nstate machine", elicitation)
        self.assertIn("installed mechanical helpers", contributing)
        self.assertNotIn("small deterministic helpers", contributing)

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
