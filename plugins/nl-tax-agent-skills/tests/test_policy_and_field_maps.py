#!/usr/bin/env python3
"""Policy and field-map coverage for Box 2 workflow support."""

import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
VALIDATOR_SCRIPT = ROOT / "skills/nl-tax-field-mapper/scripts/validate_field_map.py"


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_repo_text(relative_path):
    return (ROOT.parents[1] / relative_path).read_text(encoding="utf-8")


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def section_text(relative_path, section_heading):
    content = read_text(relative_path)
    section_start = content.index(section_heading)
    next_heading = content.find("\n## ", section_start + len(section_heading))
    if next_heading == -1:
        return content[section_start:]
    return content[section_start:next_heading]


class PolicyAndFieldMapTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_policy",
        )

    def test_field_map_validator_accepts_annual_and_provisional_box2_fields(self):
        annual_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "annual_return",
                "tax_year": 2025,
                "missing_fields": [
                    {"field_id": "personal.bsn"},
                    {"field_id": "personal.naam"},
                    {"field_id": "personal.adres"},
                    {"field_id": "personal.geboortedatum"},
                    {"field_id": "box1.loon"},
                    {"field_id": "box1.loonheffing"},
                ],
                "fields": [
                    {
                        "field_id": "box2.has_aanmerkelijk_belang",
                        "label": "Aanmerkelijk belang",
                        "source": {"type": "evidence", "evidence_id": "ev_box2_001"},
                        "confidence": 0.9,
                        "manual_review_required": False,
                    },
                    {
                        "field_id": "box2.reguliere_voordelen_bruto",
                        "label": "Reguliere voordelen bruto",
                        "source": {"type": "evidence", "evidence_id": "ev_box2_002"},
                        "confidence": 0.9,
                        "manual_review_required": False,
                    },
                    {
                        "field_id": "partner.verdeling_box2_inkomen",
                        "label": "Verdeling Box 2 inkomen",
                        "source": {"type": "estimate"},
                        "confidence": 0.8,
                        "manual_review_required": True,
                    },
                ],
            }
        )
        provisional_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "missing_fields": [
                    {"field_id": "personal.bsn"},
                    {"field_id": "personal.adres"},
                ],
                "fields": [
                    {
                        "field_id": "box2.geschatte_reguliere_voordelen",
                        "label": "Geschatte reguliere voordelen",
                        "source": {"type": "estimate"},
                        "confidence": 0.8,
                        "manual_review_required": False,
                    },
                    {
                        "field_id": "box2.geschatte_vervreemdingsvoordelen",
                        "label": "Geschatte vervreemdingsvoordelen",
                        "source": {"type": "baseline"},
                        "confidence": 0.8,
                        "manual_review_required": False,
                    },
                    {
                        "field_id": "partner.verdeling_box2_inkomen",
                        "label": "Geschatte verdeling Box 2 inkomen",
                        "source": {"type": "estimate"},
                        "confidence": 0.7,
                        "manual_review_required": True,
                    },
                ],
            }
        )

        self.assertEqual([], annual_errors)
        self.assertEqual([], provisional_errors)

    def test_field_map_validator_does_not_require_portal_prefilled_personal_fields(self):
        annual_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.1",
                "workflow": "annual_return",
                "tax_year": 2025,
                "fields": [
                    {
                        "field_id": "box1.loon",
                        "label": "Loon",
                        "value": 64000,
                        "source": {"type": "evidence", "evidence_id": "ev_jaaropgaaf_001"},
                        "confidence": 0.95,
                        "manual_review_required": False,
                    },
                    {
                        "field_id": "box1.loonheffing",
                        "label": "Ingehouden loonheffing",
                        "value": 18000,
                        "source": {"type": "evidence", "evidence_id": "ev_jaaropgaaf_001"},
                        "confidence": 0.95,
                        "manual_review_required": False,
                    },
                ],
                "missing_fields": [],
            }
        )
        provisional_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.1",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box1.geschat_loon",
                        "label": "Geschat inkomen uit werk",
                        "value": 70000,
                        "source": {"type": "estimate"},
                        "confidence": 0.8,
                        "manual_review_required": False,
                    }
                ],
                "missing_fields": [],
            }
        )

        self.assertEqual([], annual_errors)
        self.assertEqual([], provisional_errors)

    def test_field_map_template_and_docs_require_explicit_tax_year(self):
        template = read_text("skills/nl-tax-field-mapper/templates/field-map-template.yaml")
        skill = read_text("skills/nl-tax-field-mapper/SKILL.md")

        self.assertNotIn("tax_year: null", template)
        self.assertIn("REQUIRED", template)
        self.assertIn("Set `tax_year` explicitly", skill)

    def test_field_mapper_documents_field_map_precedence_contract(self):
        skill = read_text("skills/nl-tax-field-mapper/SKILL.md")
        principles = read_text("skills/nl-tax-field-mapper/reference/mapping-principles.md")
        combined = f"{skill}\n{principles}"

        self.assertIn("most recently validated", combined)
        self.assertIn("authoritative", combined)

    @unittest.skipUnless(
        (pathlib.Path(__file__).resolve().parents[3] / ".gitignore").is_file(),
        "dev-repo .gitignore not present — standalone package run",
    )
    def test_repo_hygiene_ignores_identifier_artifact_files(self):
        gitignore = read_repo_text(".gitignore")

        self.assertIn("*.bsn", gitignore)
        self.assertIn("*.iban", gitignore)

    @unittest.skipUnless(
        (pathlib.Path(__file__).resolve().parents[3] / "CHANGELOG.md").is_file(),
        "dev-repo CHANGELOG.md not present — standalone package run",
    )
    def test_changelog_does_not_claim_removed_hygiene_rules_are_unchanged(self):
        changelog = read_repo_text("CHANGELOG.md")

        self.assertIsNone(
            re.search(r"BSN/credential hygiene rules\s+are\s+unchanged", changelog)
        )
        self.assertIn("host environment", changelog)

    def test_field_mapper_docs_match_validator_scope(self):
        principles = read_text("skills/nl-tax-field-mapper/reference/mapping-principles.md")

        self.assertNotIn("browser/login/submission", principles)
        self.assertIn("browser/session/submission", principles)

    def test_field_map_validator_rejects_portal_automation_and_submission_fields(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "fields": [
                {
                    "field_id": "portal.browser_session",
                    "label": "Browser session",
                    "source": {"type": "evidence"},
                    "confidence": 0.9,
                    "manual_review_required": False,
                },
                {
                    "field_id": "portal.submission_confirmation",
                    "label": "Submission confirmation",
                    "source": {"type": "evidence"},
                    "confidence": 0.9,
                    "manual_review_required": False,
                },
            ],
        }

        errors, _ = self.validator.validate(data)

        self.assertTrue(any("browser" in error.lower() for error in errors))
        self.assertTrue(any("submission" in error.lower() for error in errors))

    def test_evidence_indexer_uses_canonical_beschikking_tokens(self):
        skill = read_text("skills/nl-tax-evidence-indexer/SKILL.md")
        evidence_types = read_text(
            "skills/nl-tax-evidence-indexer/reference/evidence-types.md"
        )

        self.assertIn("`woz_beschikking`", skill)
        self.assertIn("`voorlopige_aanslag_beschikking`", skill)
        self.assertIn("`hypotheek_jaaroverzicht`", skill)
        self.assertIn("Use these canonical `evidence_type` tokens", evidence_types)
        self.assertNotIn("`WOZ-beschikking`", skill)
        self.assertNotIn("`beschikking-VA`", skill)

    def test_submission_checklist_stays_focused_without_paper_fallback(self):
        checklist = read_text(
            "skills/nl-tax-submit-companion/templates/manual-submission-checklist.md"
        )

        self.assertIn("Mijn Belastingdienst", checklist)
        self.assertNotIn("generic credential warning", checklist)
        self.assertNotIn("0800-0543", checklist)

    def test_provisional_generation_gate_tracks_box2_in_session_progress(self):
        skill = read_text("skills/nl-tax-provisional-assessment/SKILL.md")

        self.assertIn("provisional_2026.subsections.box2", skill)
        self.assertIn("older session-progress.yaml", skill)
        self.assertIn("generation gate", skill)

    def test_provisional_review_questions_template_is_concrete_and_wired(self):
        skill = read_text("skills/nl-tax-provisional-assessment/SKILL.md")
        contract = read_text(
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        )
        template = read_text(
            "skills/nl-tax-provisional-assessment/templates/review-questions.md"
        )

        self.assertIn("templates/review-questions.md", skill)
        self.assertIn("review-questions.md", contract)
        for required in (
            "provisional_2026_review",
            "Baseline field",
            "Current 2026 estimate",
            "Change status",
            "Recommended action",
        ):
            self.assertIn(required, template)

    def test_stopzetten_contract_has_structured_body_date_gate_and_redirect_state(self):
        skill = read_text("skills/nl-tax-provisional-assessment/SKILL.md")
        contract = read_text(
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        )
        template = read_text(
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md"
        )
        guidance = read_text(
            "skills/nl-tax-provisional-assessment/reference/stopzetten-guidance.md"
        )
        flow = read_text(
            "skills/_shared/knowledge/years/2026/provisional/stopzetten-flow.md"
        )

        combined = "\n".join([skill, contract, template, guidance, flow])
        self.assertIn("## Stopzetten outcome", template)
        self.assertIn("current date", combined)
        self.assertIn("do not generate a stopzetten checklist", combined)
        self.assertIn("provisional_2026.subflow: change", combined)
        self.assertIn("active_workflow: provisional_2026_change", combined)
        self.assertIn("copy the payment baseline", combined)

    def test_change_reentry_language_is_canonical_across_provisional_notes(self):
        canonical = (
            "enter ALL data again; omitted data defaults to zero because the new "
            "VA replaces the old one entirely"
        )
        for relative_path in (
            "skills/_shared/knowledge/years/2026/provisional/change-flow.md",
            "skills/_shared/knowledge/years/2026/provisional/refund-payment-timing.md",
        ):
            with self.subTest(path=relative_path):
                self.assertIn(canonical, read_text(relative_path))

    def test_submit_companion_lists_provisional_review_workflow(self):
        skill = read_text("skills/nl-tax-submit-companion/SKILL.md")
        checklist = read_text(
            "skills/nl-tax-submit-companion/templates/manual-submission-checklist.md"
        )

        self.assertIn("provisional_2026_review", checklist)
        self.assertIn("review-questions.md", skill)

    def test_provisional_rate_contract_uses_knowledge_placeholders(self):
        contract = read_text(
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        )

        self.assertNotIn("Box 3 tax at 36%", contract)
        self.assertIn("Box 3 tax at the rate from `box3-provisional.md`", contract)

    def test_provisional_box3_explanatory_note_allowed_but_collection_fields_forbidden(self):
        allowed_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "notes": [
                    "Werkelijk rendement is not part of provisional 2026."
                ],
                "missing_fields": [
                    {"field_id": "personal.bsn"},
                    {"field_id": "personal.adres"},
                ],
                "fields": [
                    {
                        "field_id": "box3.geschatte_banktegoeden",
                        "label": "Geschatte banktegoeden",
                        "source": {"type": "estimate"},
                        "confidence": 0.9,
                        "manual_review_required": False,
                    }
                ],
            }
        )
        rejected_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box3.actual_return_choice",
                        "label": "Choose actual return method",
                        "source": {"type": "estimate"},
                        "confidence": 0.9,
                        "manual_review_required": True,
                    }
                ],
            }
        )

        provisional_template = read_text(
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md"
        )
        provisional_field_map = read_text(
            "skills/nl-tax-field-mapper/reference/provisional-field-map.md"
        )
        provisional_text = f"{provisional_template}\n{provisional_field_map}".lower()

        self.assertEqual([], allowed_errors)
        self.assertTrue(any("werkelijk rendement" in error.lower() for error in rejected_errors))
        self.assertIn("werkelijk rendement is not part of provisional 2026", provisional_text)
        self.assertNotIn("collect werkelijk rendement", provisional_text)
        self.assertNotIn("choice between fictitious and actual return", provisional_text)
        self.assertNotIn("actual return method", provisional_text)

    def test_zorgkosten_and_lijfrente_templates_require_manual_review_without_sources(self):
        annual_flow = read_text("skills/nl-tax-annual-return/reference/annual-flow.md").lower()
        annual_template = read_text(
            "skills/nl-tax-annual-return/templates/annual-return-pack.md"
        ).lower()
        provisional_template = read_text(
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md"
        ).lower()

        self.assertIn("zorgkosten threshold manual review", annual_template)
        self.assertIn("lijfrente limit manual review", annual_template)
        self.assertIn("manual review", annual_flow)
        self.assertNotIn("**deductible zorgkosten (above drempel):** eur [amount]", annual_template)
        self.assertNotIn("**deductible lijfrentepremie:** eur [amount]", annual_template)
        self.assertNotIn("lijfrentepremie                       | eur", provisional_template)
        self.assertNotIn("specific care costs                   | eur", provisional_template)

    def test_provisional_box2_reference_uses_only_provisional_or_shared_sources(self):
        reference = read_text("skills/nl-tax-box2/reference/box2-provisional-2026.md")

        self.assertIn(
            "source_ids: bd_box2_rates_2025_2026, bd_box2_income_ab_guidance, bd_fisin_aanmerkelijk_belang_2026",
            reference,
        )
        self.assertNotIn("bd_fisin_aanmerkelijk_belang_2025", reference)

    def test_annual_skill_section_count_matches_contract(self):
        skill_sections = section_text(
            "skills/nl-tax-annual-return/SKILL.md",
            "## Sections in the workpack",
        )
        required_sections = [
            "Scope",
            "Unsupported-case checks",
            "Sources used",
            "Taxpayer profile summary",
            "Evidence summary",
            "Filing status and late-filing exposure",
            "Income notes",
            "Own-home notes",
            "Box 2 notes",
            "Box 3 notes",
            "Deductions notes",
            "Credits screening",
            "Fiscal partner notes",
            "Field map summary",
            "Missing information",
            "Assumptions",
            "User-stated values index",
            "Human review checklist",
            "Not submission advice",
        ]

        self.assertIn("requires 19 sections", skill_sections)
        self.assertNotIn("requires 16 sections", skill_sections)
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, skill_sections)

    def test_box2_helper_contract_names_notes_and_open_questions(self):
        annual_skill = read_text("skills/nl-tax-annual-return/SKILL.md")
        box2_skill = read_text("skills/nl-tax-box2/SKILL.md")
        combined = f"{annual_skill}\n{box2_skill}"

        self.assertIn("workspace/shared/box2-notes.md", combined)
        self.assertIn("workspace/shared/box2-open-questions.yaml", combined)
        self.assertIn("Read `workspace/shared/box2-notes.md`", annual_skill)
        self.assertIn("workspace/shared/box2-open-questions.yaml", annual_skill)

    def test_annual_helper_delegation_allows_inline_fallback(self):
        annual_skill = read_text("skills/nl-tax-annual-return/SKILL.md")
        box2_skill = read_text("skills/nl-tax-box2/SKILL.md")
        combined = f"{annual_skill}\n{box2_skill}"
        helper_paths = [
            "skills/nl-tax-box1-home/SKILL.md",
            "skills/nl-tax-box2/SKILL.md",
            "skills/nl-tax-box3/SKILL.md",
            "skills/nl-tax-partner-deductions/SKILL.md",
        ]

        self.assertIn("If no Skill/Task tool exists", annual_skill)
        self.assertIn("inline the helper's SKILL.md instructions", annual_skill)
        self.assertIn("write the helper-owned `workspace/shared/` files", annual_skill)
        self.assertIn("called through a Skill/Task tool or inlined by an owning workflow", combined)
        for helper_path in helper_paths:
            with self.subTest(helper_path=helper_path):
                self.assertIn(
                    "called through a Skill/Task tool or inlined by an owning workflow",
                    read_text(helper_path),
                )

    def test_annual_template_uses_knowledge_placeholders_for_rates(self):
        template = read_text("skills/nl-tax-annual-return/templates/annual-return-pack.md")

        forbidden_fixed_rate_text = [
            "5% -- Src: bd_belastingrente_overview",
            "49.50% - 37.48%",
            "Effective deduction rate for this portion: 37.48%",
            "76.667% in 2025",
            "Box 3 tax (at 36%)",
            "1.25x, max EUR 1,250 additional",
            "1% of drempelinkomen, min EUR 60",
            "10% of drempelinkomen",
        ]
        for text in forbidden_fixed_rate_text:
            with self.subTest(text=text):
                self.assertNotIn(text, template)

        self.assertIn("[rate from `late-filing.md`]", template)
        self.assertIn("[top bracket rate from `box1-rates.md`]", template)
        self.assertIn("[deduction-rate cap from `deductions.md`]", template)
        self.assertIn("[box 3 rate from `fictitious.md`]", template)

    def test_annual_template_clarifies_box2_disposal_costs_once(self):
        template = read_text("skills/nl-tax-annual-return/templates/annual-return-pack.md")

        self.assertIn("Do not subtract disposal costs from `box2.vervreemdingsprijs`", template)
        self.assertIn("Use `box2.vervreemdingskosten` only to derive net transfer price from gross proceeds", template)

    def test_box1_other_work_scope_is_manual_review_not_standard_support(self):
        annual_flow = read_text("skills/nl-tax-annual-return/reference/annual-flow.md").lower()
        annual_field_map = read_text(
            "skills/nl-tax-field-mapper/reference/annual-field-map.md"
        ).lower()

        self.assertNotIn("minor side business alongside employment may still be in scope", annual_flow)
        self.assertIn("manual review", annual_flow)
        self.assertIn("resultaat uit overige werkzaamheden", annual_field_map)
        self.assertIn("manual review only", annual_field_map)

    def test_field_mapper_skill_commands_use_python3(self):
        skill = read_text("skills/nl-tax-field-mapper/SKILL.md")

        self.assertIn("python3 ", skill)
        self.assertIn("validate_field_map.py", skill)
        self.assertIn("render_field_map.py", skill)
        self.assertNotIn("\npython ", skill)

    def test_source_refresh_docs_describe_fetch_as_plan_only(self):
        skill = read_text("skills/nl-tax-source-refresh/SKILL.md")
        command = read_text("commands/nl-tax-source-refresh.md")
        combined = f"{skill}\n{command}".lower()

        self.assertIn("plan", combined)
        self.assertIn("no live http", combined)
        self.assertNotIn("refresh or validate snapshots as requested", command)
        self.assertNotIn("run the scripts in `scripts/` to fetch, rebuild, and validate", skill)

    def test_public_workflow_docs_do_not_expose_run_modes(self):
        public_workflow_files = sorted(
            path
            for path in (ROOT / "skills").rglob("*")
            if path.is_file()
            and (
                path.name == "SKILL.md"
                or "reference" in path.relative_to(ROOT / "skills").parts
                or "templates" in path.relative_to(ROOT / "skills").parts
            )
        )
        forbidden_patterns = [
            r"mode:\s*(real|test)\b",
            r"real\s*/\s*test",
            r"real\s*\|\s*test",
            "TEST" + r"\s+RUN",
            r"\.test\.(md|ya?ml)\b",
            r"\bdry[- ]run\b",
            "dry" + r"_run",
            r"\breal run\b",
            r"\btest run\b",
            r"simulated\s+dry",
            r"mode marker",
            r"test\s+vs\s+real",
            r"test\s*,\s*demo\s*,\s*or\s*dry[- ]run",
        ]

        self.assertGreater(len(public_workflow_files), 20)
        for path in public_workflow_files:
            relative_path = path.relative_to(ROOT)
            content = path.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                with self.subTest(path=relative_path, pattern=pattern):
                    self.assertIsNone(
                        re.search(pattern, content, flags=re.IGNORECASE),
                        f"{relative_path} still contains removed run-mode language",
                    )

    def test_intake_screens_complex_box2_before_workflow_anchor(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")

        self.assertIn("complex Box 2", intake)
        self.assertIn("own BV", intake)
        self.assertIn("manual review", intake)
        self.assertIn("workflow-specific anchor", intake)

    def test_command_wrappers_do_not_prompt_skill_narration(self):
        command_files = sorted((ROOT / "commands").glob("nl-tax-*.md"))

        self.assertGreaterEqual(len(command_files), 7)
        for path in command_files:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("Use the bundled", content)
                self.assertNotIn("forwarding any arguments", content)
                self.assertIn("Do not tell the user", content)

    def test_manual_and_dev_only_command_wrappers_state_policy_in_body(self):
        source_refresh = read_text("commands/nl-tax-source-refresh.md")
        submit_companion = read_text("commands/nl-tax-submit-companion.md")

        self.assertIn("developer-only maintenance", source_refresh)
        self.assertIn("not a taxpayer workflow", source_refresh)
        self.assertIn("manual-only checklist", submit_companion)
        self.assertIn("only after the user explicitly asks", submit_companion)

    def test_user_facing_sections_hide_internal_setup_language(self):
        checks = [
            (
                "skills/nl-tax-intake/SKILL.md",
                "## Workspace location",
                ["On the first turn, also tell the user", "state its absolute path"],
            ),
            (
                "skills/nl-tax-intake/SKILL.md",
                "## After intake is complete",
                ["Which skill"],
            ),
            (
                "skills/nl-tax-intake/SKILL.md",
                "## Worked example",
                ["workspace folder", "profile.yaml", "session-progress.yaml"],
            ),
            (
                "skills/nl-tax-annual-return/SKILL.md",
                "## End-of-turn report",
                ["phase was covered", "chat_only", "indexed-file"],
            ),
            (
                "skills/nl-tax-provisional-assessment/SKILL.md",
                "## End-of-turn report",
                ["subflow and section"],
            ),
        ]

        for relative_path, heading, forbidden_terms in checks:
            section = section_text(relative_path, heading)
            for term in forbidden_terms:
                with self.subTest(path=relative_path, heading=heading, term=term):
                    self.assertNotIn(term, section)

    # ------------------------------------------------------------------
    # CR-04 readiness: a map with zero populated fields is never "ready",
    # and the validator must not announce "No issues found." for it.
    # ------------------------------------------------------------------
    def test_all_missing_map_is_not_ready_and_not_announced_clean(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "fields": [],
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
        }

        errors, warnings = self.validator.validate(data)
        readiness = self.validator._readiness_for(data)

        # No errors/warnings for a legitimate in-progress map (default semantics).
        self.assertEqual([], errors)
        # But it is NOT ready: zero populated fields and required refs outstanding.
        self.assertFalse(readiness["ready"])
        self.assertEqual(0, readiness["populated_count"])
        self.assertIn("box1.loon", readiness["required_unpopulated"])
        # BSN is identifier-class and excluded from required_unpopulated.
        self.assertNotIn("personal.bsn", readiness["required_unpopulated"])

        # The message-selection logic main() uses must NOT print "No issues found."
        announces_clean = not errors and not warnings and readiness["ready"]
        self.assertFalse(announces_clean)

    def test_assess_readiness_counts_only_sourced_populated_fields(self):
        # A populated field with usable provenance counts; required refs satisfied.
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
            {
                "field_id": "personal.naam",
                "value": "Jan Jansen",
                "source": {"type": "user_chat", "quote": "name"},
            },
            {
                "field_id": "personal.adres",
                "value": "Straat 1",
                "source": {"type": "user_chat", "quote": "addr"},
            },
            {
                "field_id": "personal.geboortedatum",
                "value": "1980-01-01",
                "source": {"type": "user_chat", "quote": "dob"},
            },
        ]
        readiness = self.validator.assess_readiness(fields, [], "annual_return", 2025)
        self.assertTrue(readiness["ready"])
        self.assertEqual(5, readiness["populated_count"])
        self.assertEqual([], readiness["required_unpopulated"])

    def test_assess_readiness_ME23_baseline_without_ref_not_populated(self):
        # ME-23: a populated baseline field lacking baseline_ref has no usable
        # provenance, so it does not count as populated.
        fields = [
            {
                "field_id": "box1.loon",
                "value": 50000,
                "source": {"type": "baseline"},  # no baseline_ref
            }
        ]
        readiness = self.validator.assess_readiness(fields, [], "annual_return", 2025)
        self.assertEqual(0, readiness["populated_count"])
        self.assertFalse(readiness["ready"])
        self.assertIn("box1.loon", readiness["required_unpopulated"])

        # With the ref present it counts as populated.
        fields[0]["source"]["baseline_ref"] = "prior_year_2024"
        readiness2 = self.validator.assess_readiness(fields, [], "annual_return", 2025)
        self.assertEqual(1, readiness2["populated_count"])

    # ------------------------------------------------------------------
    # ME-22 structural guards.
    # ------------------------------------------------------------------
    def test_root_not_a_mapping_is_rejected(self):
        errors, warnings = self.validator.validate(["not", "a", "mapping"])
        self.assertEqual(["Field map root must be a mapping"], errors)
        self.assertEqual([], warnings)

    def test_duplicate_field_id_is_rejected(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
            "fields": [
                {
                    "field_id": "box2.foo",
                    "label": "Foo",
                    "source": {"type": "estimate"},
                    "confidence": 0.5,
                    "manual_review_required": True,
                },
                {
                    "field_id": "box2.foo",
                    "label": "Foo again",
                    "source": {"type": "estimate"},
                    "confidence": 0.5,
                    "manual_review_required": True,
                },
            ],
        }
        errors, _ = self.validator.validate(data)
        self.assertTrue(any("Duplicate field_id: box2.foo" == e for e in errors))

    def test_fields_wrong_type_is_rejected(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "fields": {"not": "a list"},
            "missing_fields": [{"field_id": "personal.bsn"}],
        }
        errors, _ = self.validator.validate(data)
        self.assertTrue(any("fields must be a list" == e for e in errors))

    def test_non_dict_field_entry_is_skipped_with_error(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
            "fields": ["a bare string, not a mapping"],
        }
        errors, _ = self.validator.validate(data)
        self.assertTrue(any("must be a mapping" in e for e in errors))

    # ------------------------------------------------------------------
    # ME-35 non-finite numeric value.
    # ------------------------------------------------------------------
    def test_non_finite_value_is_rejected(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
            "fields": [
                {
                    "field_id": "box2.amount",
                    "label": "Amount",
                    "value": float("inf"),
                    "source": {"type": "estimate"},
                    "confidence": 0.5,
                    "manual_review_required": True,
                }
            ],
        }
        errors, _ = self.validator.validate(data)
        self.assertTrue(any("Non-finite" in e for e in errors))

    # ------------------------------------------------------------------
    # ME-30 readiness metadata.
    # ------------------------------------------------------------------
    def test_review_ready_declaration_warns_when_not_ready(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "readiness": "review_ready",
            "fields": [],
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
        }
        _, warnings = self.validator.validate(data)
        self.assertTrue(any("review_ready" in w for w in warnings))

    def test_invalid_readiness_value_is_rejected(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "readiness": "totally-ready",
            "missing_fields": [{"field_id": "personal.bsn"}],
        }
        errors, _ = self.validator.validate(data)
        self.assertTrue(any("Invalid readiness" in e for e in errors))

    # ------------------------------------------------------------------
    # ME-13 unknown source.type coverage in missing_fields.
    # ------------------------------------------------------------------
    def test_unknown_source_type_in_missing_fields_passes(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
                {"field_id": "box3.mystery"},
            ],
            "fields": [
                {
                    "field_id": "box3.mystery",
                    "label": "Mystery",
                    "value": None,
                    "source": {"type": "unknown"},
                    "manual_review_required": True,
                }
            ],
        }
        errors, _ = self.validator.validate(data)
        self.assertFalse(any("unknown" in e.lower() for e in errors))

    # ------------------------------------------------------------------
    # CR-04 end-to-end: main() prints NOT_READY_FOR_ENTRY, suppresses
    # "No issues found.", keeps default exit 0, and exits nonzero under --strict.
    # ------------------------------------------------------------------
    def _run_validator(self, yaml_text, *extra_args):
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML not available for main() subprocess test")
        with tempfile.NamedTemporaryFile(
            "w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as handle:
            handle.write(textwrap.dedent(yaml_text))
            tmp_path = handle.name
        try:
            return subprocess.run(
                [sys.executable, str(VALIDATOR_SCRIPT), *extra_args, tmp_path],
                capture_output=True,
                text=True,
            )
        finally:
            pathlib.Path(tmp_path).unlink(missing_ok=True)

    def test_main_all_missing_map_not_ready_no_clean_announcement(self):
        yaml_text = """
            field_map_version: "1.0"
            workflow: annual_return
            tax_year: 2025
            fields: []
            missing_fields:
              - field_id: personal.bsn
              - field_id: personal.naam
              - field_id: personal.adres
              - field_id: personal.geboortedatum
              - field_id: box1.loon
              - field_id: box1.loonheffing
        """
        result = self._run_validator(yaml_text)
        self.assertIn("NOT_READY_FOR_ENTRY", result.stdout)
        self.assertNotIn("No issues found.", result.stdout)
        # Default exit semantics unchanged: no errors -> exit 0.
        self.assertEqual(0, result.returncode)

        strict = self._run_validator(yaml_text, "--strict")
        self.assertIn("NOT_READY_FOR_ENTRY", strict.stdout)
        self.assertEqual(1, strict.returncode)

    def test_unknown_source_type_not_in_missing_fields_errors(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.naam"},
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
            "fields": [
                {
                    "field_id": "box3.mystery",
                    "label": "Mystery",
                    "value": None,
                    "source": {"type": "unknown"},
                    "manual_review_required": True,
                }
            ],
        }
        errors, _ = self.validator.validate(data)
        self.assertTrue(
            any("requires entry in missing_fields" in e for e in errors)
        )


if __name__ == "__main__":
    unittest.main()
