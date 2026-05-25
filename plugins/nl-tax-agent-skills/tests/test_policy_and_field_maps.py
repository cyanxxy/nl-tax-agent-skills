#!/usr/bin/env python3
"""Policy and field-map coverage for Box 2 workflow support."""

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
                {
                    "field_id": "security.digid_username",
                    "label": "DigiD login username",
                    "source": {"type": "evidence"},
                    "confidence": 0.9,
                    "manual_review_required": False,
                },
            ],
        }

        errors, _ = self.validator.validate(data)

        self.assertTrue(any("browser" in error.lower() for error in errors))
        self.assertTrue(any("submission" in error.lower() for error in errors))
        self.assertTrue(any("credential/login" in error.lower() for error in errors))

    def test_no_digid_policy_keeps_online_machtigen_boundary_and_no_paper_fallback(self):
        policy = read_text("skills/nl-tax-submit-companion/reference/no-digid-policy.md")
        checklist = read_text(
            "skills/nl-tax-submit-companion/templates/manual-submission-checklist.md"
        )
        combined = f"{policy}\n{checklist}"

        self.assertIn("online Mijn Belastingdienst", policy)
        self.assertIn("DigiD Machtigen", combined)
        self.assertIn("does **NOT** collect, store, or use DigiD credentials", policy)
        self.assertIn("Paper filing is outside the supported online workflow", policy)
        self.assertNotIn("0800-0543", combined)
        self.assertNotIn("DigiD is required for **ALL** submission paths", policy)

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

    def test_intake_screens_complex_box2_before_workflow_anchor(self):
        intake = read_text("skills/nl-tax-intake/SKILL.md")

        self.assertIn("complex Box 2", intake)
        self.assertIn("own BV", intake)
        self.assertIn("manual review", intake)
        self.assertIn("workflow-specific anchor", intake)


if __name__ == "__main__":
    unittest.main()
