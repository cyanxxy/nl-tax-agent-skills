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

import yaml


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)
REPO_ROOT = ROOT.parents[1]
VALIDATOR_SCRIPT = ROOT / "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py"


def read_text(relative_path):
    path = ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    if relative_path in {
        "skills/nl-tax-provisional-assessment/SKILL.md",
        "skills/nl-tax-provisional-assessment/reference/provisional-flow.md",
    }:
        index_path = (
            ROOT
            / "skills/nl-tax-provisional-assessment/reference/provisional-flow.md"
        )
        index = index_path.read_text(encoding="utf-8")
        links = re.findall(r"\]\((subflows/[^)]+\.md)\)", index)
        text += "\n" + index + "\n".join(
            (index_path.parent / link).read_text(encoding="utf-8")
            for link in links
        )
    return text


def read_repo_text(relative_path):
    return (ROOT.parents[1] / relative_path).read_text(encoding="utf-8")


def skill_frontmatter(skill_name):
    text = read_text(f"skills/{skill_name}/SKILL.md")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing YAML frontmatter: {skill_name}")
    _, block, _ = text.split("---", 2)
    return yaml.safe_load(block)


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PolicyAndFieldMapTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_module(
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
            "validate_field_map_policy",
        )

    def test_manual_checklist_has_exact_validator_check_ids(self):
        principles = read_text(
            "skills/nl-tax-field-mapper/reference/mapping-principles.md"
        )
        manual_ids = set(
            re.findall(r"^- \[[ xX]\] `([^`]+)`", principles, re.MULTILINE)
        )

        self.assertEqual(set(self.validator.CHECK_IDS), manual_ids)

    def test_check_trail_accepts_only_agent_or_script(self):
        base = {
            "field_map_version": "1.1",
            "workflow": "provisional_assessment",
            "tax_year": 2026,
            "fields": [],
            "missing_fields": [{"field_id": "box1.geschat_loon"}],
        }
        for trail in ("checked_by_agent", "checked_by_script"):
            data = dict(base, check_performed_by=trail)
            errors, _ = self.validator.validate(data)
            self.assertFalse(any("check_performed_by" in e for e in errors), errors)

        errors, _ = self.validator.validate(
            dict(base, check_performed_by="checked_by_human")
        )
        self.assertTrue(any("check_performed_by" in e for e in errors), errors)

        errors, _ = self.validator.validate(base)
        self.assertTrue(any("check_performed_by" in e for e in errors), errors)

    def test_field_map_validator_accepts_annual_and_provisional_box2_fields(self):
        annual_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "annual_return",
                "tax_year": 2025,
                "check_performed_by": "checked_by_agent",
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
                        "source": {
                            "type": "user_chat",
                            "quote": "Use 60% for me and 40% for my partner",
                            "stated_at": "2026-07-17",
                        },
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
                "check_performed_by": "checked_by_agent",
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
                        "source": {
                            "type": "user_chat",
                            "quote": "Keep the 50/50 split",
                            "stated_at": "2026-07-17",
                        },
                        "confidence": 0.7,
                        "manual_review_required": True,
                    },
                ],
            }
        )

        self.assertEqual([], annual_errors)
        self.assertEqual([], provisional_errors)

    def test_partner_allocation_requires_explicit_taxpayer_choice(self):
        base_field = {
            "field_id": "partner.verdeling_box3_grondslag",
            "label": "Verdeling grondslag sparen en beleggen",
            "value": 60,
            "confidence": 0.8,
            "manual_review_required": True,
        }
        base = {
            "field_map_version": "1.1",
            "workflow": "annual_return",
            "tax_year": 2025,
            "fields": [],
            "missing_fields": [],
        }

        unconfirmed = dict(base)
        unconfirmed["fields"] = [
            dict(base_field, source={"type": "calculated", "calculated_from": []})
        ]
        errors, _ = self.validator.validate(unconfirmed)
        self.assertTrue(
            any("explicit taxpayer choice" in error.lower() for error in errors),
            errors,
        )

        confirmed = dict(base)
        confirmed["fields"] = [
            dict(
                base_field,
                source={
                    "type": "user_chat",
                    "quote": "Use a 60/40 split",
                    "stated_at": "2026-07-17",
                },
            )
        ]
        errors, _ = self.validator.validate(confirmed)
        self.assertFalse(
            any("explicit taxpayer choice" in error.lower() for error in errors),
            errors,
        )

    def test_partner_allocation_detection_accepts_canonical_id_orders(self):
        allocation_ids = (
            "partner.verdeling_box3_grondslag",
            "partner.allocation_box3",
            "partner.box3_allocation",
            "partner.toedeling_eigenwoning",
        )
        for field_id in allocation_ids:
            with self.subTest(field_id=field_id):
                errors, _ = self.validator.validate(
                    {
                        "field_map_version": "1.1",
                        "workflow": "annual_return",
                        "tax_year": 2025,
                        "check_performed_by": "checked_by_agent",
                        "fields": [
                            {
                                "field_id": field_id,
                                "label": "Partner scenario",
                                "value": 60,
                                "source": {
                                    "type": "calculated",
                                    "calculated_from": ["scenario_a"],
                                },
                                "confidence": 0.9,
                                "manual_review_required": True,
                            }
                        ],
                        "missing_fields": [],
                    }
                )
                self.assertTrue(
                    any("explicit taxpayer choice" in error.lower() for error in errors),
                    errors,
                )

    def test_partner_allocation_detection_uses_whole_tokens_and_namespace(self):
        benign_ids = (
            "partner.reallocation_note",
            "partner.relationship_status",
            "taxpayer.partner_allocation_note",
        )
        for field_id in benign_ids:
            with self.subTest(field_id=field_id):
                errors, _ = self.validator.validate(
                    {
                        "field_map_version": "1.1",
                        "workflow": "annual_return",
                        "tax_year": 2025,
                        "check_performed_by": "checked_by_agent",
                        "fields": [
                            {
                                "field_id": field_id,
                                "label": "Benign partner metadata",
                                "value": "reviewed",
                                "source": {"type": "estimate"},
                                "confidence": 0.9,
                                "manual_review_required": True,
                            }
                        ],
                        "missing_fields": [],
                    }
                )
                self.assertFalse(
                    any("explicit taxpayer choice" in error.lower() for error in errors),
                    errors,
                )

    def test_provisional_expected_profit_requires_provenance_and_manual_review(self):
        valid_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "check_performed_by": "checked_by_agent",
                "fields": [
                    {
                        "field_id": "onderneming.geschatte_winst",
                        "label": "Geschatte winst uit onderneming",
                        "value": 48000,
                        "source": {
                            "type": "user_chat",
                            "quote": "I expect EUR 48,000 profit",
                            "stated_at": "2026-07-11",
                        },
                        "manual_review_required": True,
                    }
                ],
                "missing_fields": [],
            }
        )
        invalid_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "onderneming.geschatte_winst",
                        "label": "Geschatte winst uit onderneming",
                        "value": 48000,
                        "source": {"type": "estimate"},
                        "manual_review_required": False,
                    }
                ],
                "missing_fields": [],
            }
        )

        self.assertEqual([], valid_errors)
        self.assertTrue(any("provenance" in e.lower() for e in invalid_errors), invalid_errors)
        self.assertTrue(any("manual review" in e.lower() for e in invalid_errors), invalid_errors)

    def test_provisional_expected_profit_does_not_bypass_deduction_guard(self):
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "onderneming.geschatte_winst",
                        "label": "Geschatte winst uit onderneming",
                        "value": 48000,
                        "notes": "Includes ondernemersaftrek",
                        "source": {
                            "type": "user_chat",
                            "quote": "EUR 48,000",
                            "stated_at": "2026-07-11",
                        },
                        "manual_review_required": True,
                    }
                ],
                "missing_fields": [],
            }
        )

        self.assertTrue(any("deduction" in error.lower() for error in errors), errors)

    def test_provisional_expected_profit_requires_complete_concrete_provenance(self):
        incomplete_sources = (
            {"type": "user_chat", "quote": "EUR 48,000"},
            {"type": "baseline"},
            {"type": "evidence"},
        )
        for source in incomplete_sources:
            errors, _ = self.validator.validate(
                {
                    "field_map_version": "1.0",
                    "workflow": "provisional_assessment",
                    "tax_year": 2026,
                    "fields": [
                        {
                            "field_id": "onderneming.geschatte_winst",
                            "label": "Geschatte winst uit onderneming",
                            "value": 48000,
                            "source": source,
                            "manual_review_required": True,
                        }
                    ],
                    "missing_fields": [],
                }
            )
            with self.subTest(source=source):
                self.assertTrue(any("provenance" in error.lower() for error in errors), errors)

    def test_field_map_validator_does_not_require_portal_prefilled_personal_fields(self):
        annual_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.1",
                "workflow": "annual_return",
                "tax_year": 2025,
                "check_performed_by": "checked_by_agent",
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
                "check_performed_by": "checked_by_agent",
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

    @unittest.skipUnless(
        (REPO_ROOT / ".gitignore").is_file(),
        "dev-repo .gitignore not present",
    )
    def test_repo_hygiene_ignores_identifier_artifact_files(self):
        gitignore = read_repo_text(".gitignore")

        self.assertIn("*.bsn", gitignore)
        self.assertIn("*.iban", gitignore)

    def test_field_map_validator_rejects_authenticated_portal_actions_everywhere(self):
        cases = (
            ("browser_session", "Browser session"),
            ("chrome_control", "Chrome control"),
            ("computer_use", "Computer use"),
            ("screen_interaction", "Screen interaction"),
            ("login", "Portal login"),
            ("authentication", "Portal authentication"),
            ("logged_in", "Logged in"),
            ("log_into", "Log into Mijn Belastingdienst"),
            ("inloggen", "Inloggen"),
            ("digid", "DigiD"),
            ("form_filling", "Form filling"),
            ("form_entry", "Form entry"),
            ("enter_values", "Enter values"),
            ("invullen", "Formulier invullen"),
            ("click_submit", "Click submit"),
            ("signature", "Signature"),
            ("signing", "Signing"),
            ("ondertekenen", "Ondertekenen"),
            ("verzenden", "Verzenden"),
            ("sending", "Sending"),
            ("submitting", "Submitting"),
            ("submission_confirmation", "Submission confirmation"),
        )

        for location in ("fields", "missing_fields"):
            for token, label in cases:
                with self.subTest(location=location, token=token):
                    row = {"field_id": f"portal.{token}", "label": label}
                    if location == "fields":
                        row.update(
                            {
                                "value": True,
                                "source": {"type": "estimate"},
                                "confidence": 0.9,
                                "manual_review_required": False,
                            }
                        )
                    else:
                        row.update(
                            {
                                "reason": f"Need {label}",
                                "blocking": True,
                            }
                        )
                    data = {
                        "field_map_version": "1.1",
                        "workflow": "annual_return",
                        "tax_year": 2025,
                        "fields": [row] if location == "fields" else [],
                        "missing_fields": [row] if location == "missing_fields" else [],
                    }
                    errors, _ = self.validator.validate(data)
                    self.assertTrue(
                        any(
                            "authenticated-portal action field" in error.lower()
                            and f"portal.{token}" in error
                            for error in errors
                        ),
                        errors,
                    )

    def test_portal_action_matching_uses_whole_tokens(self):
        data = {
            "field_map_version": "1.1",
            "workflow": "annual_return",
            "tax_year": 2025,
            "fields": [
                {
                    "field_id": "workflow.assigned_category",
                    "label": "Assigned review category",
                    "value": "manual",
                    "source": {"type": "estimate"},
                    "confidence": 0.9,
                    "manual_review_required": True,
                }
            ],
            "missing_fields": [],
        }

        errors, _ = self.validator.validate(data)
        self.assertFalse(
            any("authenticated-portal action field" in error.lower() for error in errors),
            errors,
        )

    def test_field_map_validator_rejects_automation_metadata_keys_everywhere(self):
        cases = (
            "selector",
            "selectors",
            "portal_selector_hint",
            "css_selector",
            "css-selector",
            "cssSelector",
            "CSSSelector",
            "xpath",
            "x_path",
            "xPath",
            "XPath",
            "DOMLocator",
            "dom_locator",
            "browserLocator",
            "browser-locator",
            "element_locator",
            "locators",
        )

        for location in ("fields", "missing_fields"):
            for metadata_key in cases:
                with self.subTest(location=location, metadata_key=metadata_key):
                    row = {
                        "field_id": "box1.tax_amount",
                        "label": "Tax amount",
                        metadata_key: "#tax-amount",
                    }
                    if location == "fields":
                        row.update(
                            {
                                "value": 100,
                                "source": {"type": "estimate"},
                                "confidence": 0.9,
                                "manual_review_required": False,
                            }
                        )
                    else:
                        row.update({"reason": "Amount is unknown", "blocking": True})
                    data = {
                        "field_map_version": "1.1",
                        "workflow": "annual_return",
                        "tax_year": 2025,
                        "check_performed_by": "checked_by_agent",
                        "fields": [row] if location == "fields" else [],
                        "missing_fields": [row] if location == "missing_fields" else [],
                    }

                    errors, _ = self.validator.validate(data)
                    self.assertTrue(
                        any(
                            "automation metadata key" in error.lower()
                            and location in error
                            and metadata_key in error
                            for error in errors
                        ),
                        errors,
                    )

    def test_field_map_validator_rejects_nested_automation_metadata_keys(self):
        for location in ("fields", "missing_fields"):
            with self.subTest(location=location):
                row = {
                    "field_id": "box1.tax_amount",
                    "label": "Tax amount",
                    "presentation": {
                        "targets": [{"browserLocator": "#tax-amount"}]
                    },
                }
                if location == "fields":
                    row.update(
                        {
                            "value": 100,
                            "source": {"type": "estimate"},
                            "confidence": 0.9,
                            "manual_review_required": False,
                        }
                    )
                else:
                    row.update({"reason": "Amount is unknown", "blocking": True})
                data = {
                    "field_map_version": "1.1",
                    "workflow": "annual_return",
                    "tax_year": 2025,
                    "check_performed_by": "checked_by_agent",
                    "fields": [row] if location == "fields" else [],
                    "missing_fields": [row] if location == "missing_fields" else [],
                }

                errors, _ = self.validator.validate(data)
                self.assertTrue(
                    any(
                        "automation metadata key" in error.lower()
                        and "presentation.targets.[0].browserLocator" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_automation_metadata_key_matching_avoids_benign_near_matches(self):
        data = {
            "field_map_version": "1.1",
            "workflow": "annual_return",
            "tax_year": 2025,
            "check_performed_by": "checked_by_agent",
            "fields": [
                {
                    "field_id": "workflow.review_category",
                    "label": "Review category",
                    "value": "manual",
                    "source": {"type": "estimate"},
                    "confidence": 0.9,
                    "manual_review_required": True,
                    "selected_scenario": "A",
                    "selection_reason": "Taxpayer choice",
                    "document_location": "uploads/source.pdf",
                    "browser_compatibility": "not applicable",
                    "xpathology_note": "benign whole-token near match",
                    "selectorate_status": "benign whole-token near match",
                }
            ],
            "missing_fields": [],
        }

        errors, _ = self.validator.validate(data)
        self.assertFalse(
            any("automation metadata key" in error.lower() for error in errors),
            errors,
        )

    def test_shared_evidence_types_use_canonical_beschikking_tokens(self):
        self.assertFalse((ROOT / "skills/nl-tax-evidence-indexer").exists())

    def test_provisional_generation_gate_tracks_box2_in_resume_record(self):
        template = read_text(
            "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md"
        )
        appendix = template.split("## Appendix A — Resume record", 1)[1]
        record = yaml.safe_load(appendix.split("```yaml\n", 1)[1].split("\n```", 1)[0])

        self.assertIn("box2", record["sections"])
        self.assertIn("winst_forecast", record["sections"])

    def test_stopzetten_contract_has_structured_body_date_gate_and_redirect_state(self):
        template = read_text(
            "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md"
        )

        self.assertIn("## Stopzetten outcome", template)

    def test_provisional_box3_explanatory_note_allowed_but_collection_fields_forbidden(self):
        allowed_errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "check_performed_by": "checked_by_agent",
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

        self.assertEqual([], allowed_errors)
        self.assertTrue(any("werkelijk rendement" in error.lower() for error in rejected_errors))

    def test_annual_output_contract_has_all_required_sections(self):
        # 0.4 R4: the workpack section order, after the title/STATUS banner.
        required_sections = [
            "How to use this file",
            "Contents",
            "Scope",
            "Unsupported-case checks",
            "Taxpayer profile summary",
            "Documents and sources",
            "Sources used",
            "Filing status and late-filing exposure",
            "Income notes",
            "Winst uit onderneming notes",
            "Own-home notes",
            "Box 2 notes",
            "Box 3 notes",
            "Deductions notes",
            "Credits screening",
            "Fiscal partner notes",
            "Open questions",
            "Missing information",
            "Assumptions",
            "User-stated values index",
            "Field map summary",
            "Manual-entry checklist",
            "Human review checklist",
            "Not submission advice",
            "Appendix A — Resume record",
            "Appendix B — Field map",
        ]

        self.assertEqual(len(required_sections), 26)

        template = read_text("skills/nl-tax-annual-return/templates/annual-workpack.md")
        headings = re.findall(r"(?m)^## (.+?)\s*$", template)
        self.assertEqual(headings, required_sections)

    def test_helpers_return_results_without_persisting_artifacts(self):
        helper_paths = (
            "skills/nl-tax-box1-home/SKILL.md",
            "skills/nl-tax-box2/SKILL.md",
            "skills/nl-tax-box3/SKILL.md",
            "skills/nl-tax-winst/SKILL.md",
            "skills/nl-tax-partner-deductions/SKILL.md",
        )

        for helper_path in helper_paths:
            helper = read_text(helper_path)
            with self.subTest(helper_path=helper_path):
                self.assertNotIn("  - Write", helper)
                self.assertNotIn("  - Edit", helper)

    def test_plugin_has_only_unique_skill_discovery_names(self):
        self.assertFalse((ROOT / "commands").exists())
        skill_paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
        names = [skill_frontmatter(path.parent.name)["name"] for path in skill_paths]

        # 0.4: eleven skills plus the hidden nl-tax-shared-resources package.
        self.assertEqual(len(names), 19)
        self.assertEqual(len(set(names)), 19)
        self.assertEqual(
            set(names),
            {
                "nl-tax-annual-return",
                "nl-tax-box1-home",
                "nl-tax-box2",
                "nl-tax-box3",
                "nl-tax-field-mapper",
                "nl-tax-intake",
                "nl-tax-knowledge",
                "nl-tax-partner-deductions",
                "nl-tax-provisional-assessment",
                "nl-tax-shared-resources",
                "nl-tax-submit-companion",
                "nl-tax-winst",
                "nl-tax-vat-return",
                "nl-tax-vat-correction",
                "nl-tax-vat-adjustments",
    "nl-tax-annual-return-2026",
    "nl-tax-icp",
    "nl-tax-oss",
    "nl-tax-international-return",
            },
        )

    def test_public_skills_retain_exact_argument_hints(self):
        expected = {
            "nl-tax-annual-return": "[2025] [confirm]",
            "nl-tax-field-mapper": "[annual|provisional|vat|vat-correction|icp|oss|international] [year] [period|form]",
            "nl-tax-intake": "[annual|international|request|change|review|stopzetten|vat|vat-correction|icp|oss]",
            "nl-tax-provisional-assessment": (
                "[2026] [request|change|review|stopzetten|confirm]"
            ),
            "nl-tax-submit-companion": "[annual|provisional|international|vat|vat-correction|icp|oss] [2025|2026] [identity]",
        }

        actual = {
            name: skill_frontmatter(name).get("argument-hint") for name in expected
        }
        self.assertEqual(actual, expected)

    # ------------------------------------------------------------------
    # CR-04 readiness: a map with zero populated fields is never "ready",
    # and the validator must not announce "No issues found." for it.
    # ------------------------------------------------------------------
    def test_all_missing_map_is_not_ready_and_not_announced_clean(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "check_performed_by": "checked_by_agent",
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

    def test_missing_field_id_returns_validation_error_instead_of_crashing(self):
        data = {
            "field_map_version": "1.1",
            "workflow": "annual_return",
            "tax_year": 2025,
            "check_performed_by": "checked_by_agent",
            "fields": [
                {
                    "label": "Malformed chat field",
                    "value": "x",
                    "source": {
                        "type": "user_chat",
                        "quote": "x",
                        "stated_at": "2026-07-16",
                    },
                    "manual_review_required": False,
                },
                {
                    "field_id": "personal.naam",
                    "label": "Naam",
                    "value": "Jan",
                    "source": {
                        "type": "user_chat",
                        "quote": "Jan",
                        "stated_at": "2026-07-16",
                    },
                    "manual_review_required": False,
                },
            ],
            "user_chat_values_index": [
                {
                    "field_id": "personal.naam",
                    "value": "Jan",
                    "quote": "Jan",
                    "stated_at": "2026-07-16",
                }
            ],
            "missing_fields": [
                {"field_id": "personal.adres"},
                {"field_id": "personal.geboortedatum"},
                {"field_id": "box1.loon"},
                {"field_id": "box1.loonheffing"},
            ],
        }

        errors, _ = self.validator.validate(data)

        self.assertIn(
            "fields[0] requires a non-empty string field_id",
            errors,
        )

    def test_review_ready_map_requires_every_user_chat_index_row(self):
        field_specs = (
            ("personal.naam", "Jan"),
            ("personal.adres", "Straat 1"),
            ("personal.geboortedatum", "1980-01-01"),
            ("box1.loon", 50000),
            ("box1.loonheffing", 12000),
        )
        data = {
            "field_map_version": "1.1",
            "workflow": "annual_return",
            "tax_year": 2025,
            "readiness": "review_ready",
            "check_performed_by": "checked_by_agent",
            "fields": [
                {
                    "field_id": field_id,
                    "label": field_id,
                    "value": value,
                    "source": {
                        "type": "user_chat",
                        "quote": str(value),
                        "stated_at": "2026-07-16",
                    },
                    "manual_review_required": False,
                }
                for field_id, value in field_specs
            ],
            "missing_fields": [],
        }

        errors, warnings = self.validator.validate(data)

        self.assertTrue(
            any(
                error
                == "user_chat field missing from user_chat_values_index: personal.naam"
                for error in errors
            ),
            errors,
        )
        self.assertFalse(
            any("missing from user_chat_values_index" in warning for warning in warnings),
            warnings,
        )
        with tempfile.TemporaryDirectory() as tmp:
            field_map = pathlib.Path(tmp) / "field-map.yaml"
            field_map.write_text(yaml.safe_dump(data), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_SCRIPT), "--require-ready", str(field_map)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("missing from user_chat_values_index", result.stdout)

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
    def test_review_ready_declaration_errors_when_not_ready(self):
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
        errors, warnings = self.validator.validate(data)
        self.assertTrue(any("review_ready" in error for error in errors), errors)
        self.assertEqual([], warnings)

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
    # CR-04 end-to-end: main() reports undeclared/blocked readiness, suppresses
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
            check_performed_by: checked_by_agent
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
        self.assertIn("UNDECLARED_OR_BLOCKED", result.stdout)
        self.assertNotIn("No issues found.", result.stdout)
        # Default exit semantics unchanged: no errors -> exit 0.
        self.assertEqual(0, result.returncode)

        strict = self._run_validator(yaml_text, "--strict")
        self.assertIn("UNDECLARED_OR_BLOCKED", strict.stdout)
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


def _field_map_grader():
    return load_module(
        "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
        "field_map_grader_identity_tests",
    )


def _samples():
    spec = importlib.util.spec_from_file_location(
        "workpack_samples_for_field_map_identity",
        pathlib.Path(__file__).resolve().parent / "workpack_samples.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _vat_map(workflow="vat_return", notes=()):
    values = {
        "vat.1a.turnover": 10000, "vat.1a.vat": 2100, "vat.1b.vat": 0, "vat.1c.vat": 0,
        "vat.1d.vat": 0, "vat.2a.vat": 0, "vat.4a.vat": 0, "vat.4b.turnover": 1000,
        "vat.4b.vat": 210, "vat.5a.vat": 2310, "vat.5b.vat": 735, "vat.total.balance": 1575,
    }
    internal = {"vat.5a.vat", "vat.total.balance"}
    return {
        "field_map_version": "1.1", "workflow": workflow, "tax_year": 2026, "period": "Q3",
        "created_at": "2026-10-02T08:00:00Z", "updated_at": "2026-10-02T08:00:00Z",
        "readiness": "draft", "check_performed_by": "checked_by_agent", "missing_fields": [],
        "user_chat_values_index": [], "notes": list(notes),
        "fields": [
            {"field_id": fid, "label": fid, "value": amount,
             "entry_mode": "internal_routing" if fid in internal else "manual_entry",
             "source": {"type": "evidence", "evidence_id": "ev_001"},
             "confidence": 0.9, "manual_review_required": True, "notes": []}
            for fid, amount in values.items()
        ],
    }


class FieldMapIdentityAndYearTests(unittest.TestCase):
    """PYT-09, PYT-10 and PYT-12 regressions in the repository field-map grader."""

    @classmethod
    def setUpClass(cls):
        cls.grader = _field_map_grader()
        cls.samples = _samples()

    def test_annual_2025_map_mislabelled_2026_names_the_year_slip(self):
        data = dict(self.samples.ANNUAL_FIELD_MAP, tax_year=2026)
        errors, _ = self.grader.validate(data)
        self.assertTrue(
            any(
                "annual_return tax_year 2026 map uses annual 2025 field ids box1.loon, box1.loonheffing"
                in error and "check tax_year" in error
                for error in errors
            ),
            errors,
        )
        # The per-field errors stay, so nothing is hidden.
        self.assertTrue(any("annual_2026: unsupported field_id box1.loon" in e for e in errors), errors)
        # A real annual 2026 map with annual2026. ids never gets the year-slip error.
        real = dict(self.samples.ANNUAL_FIELD_MAP, tax_year=2026, fields=[{
            "field_id": "annual2026.box1.wage", "label": "wage", "value": 100,
            "entry_mode": "internal_routing", "source": {"type": "evidence", "evidence_id": "ev_001"},
            "confidence": 0.9, "manual_review_required": True, "notes": [],
        }])
        errors, _ = self.grader.validate(real)
        self.assertFalse(any("year slip" in e or "uses annual 2025 field ids" in e for e in errors), errors)

    def test_identity_keys_belong_only_to_their_workflows(self):
        annual = dict(self.samples.ANNUAL_FIELD_MAP, period="Q3", scheme="union", return_form="migration")
        errors, warnings = self.grader.validate(annual)
        for key in ("period", "scheme", "return_form"):
            with self.subTest(key=key):
                self.assertIn(f"annual_return map must not carry identity key {key}", errors)
        self.assertFalse(any("Unknown top-level key" in warning for warning in warnings), warnings)

        provisional = dict(self.samples.PROVISIONAL_FIELD_MAP, period="Q1")
        self.assertIn(
            "provisional_assessment map must not carry identity key period",
            self.grader.validate(provisional)[0],
        )

        vat = dict(_vat_map(), scheme="ioss", return_form="nonresident")
        errors, _ = self.grader.validate(vat)
        self.assertIn("vat_return map must not carry identity key scheme", errors)
        self.assertIn("vat_return map must not carry identity key return_form", errors)
        errors, warnings = self.grader.validate(_vat_map())
        self.assertFalse(any("identity key" in error for error in errors), errors)
        self.assertFalse(any("Unknown top-level key" in warning for warning in warnings), warnings)

    def test_vat_coverage_notes_are_cross_checked_against_mapped_rows(self):
        data = _vat_map(notes=[
            "vat_rubric_coverage:1e=applicable_mapped; F:ev_001",
            "vat_rubric_coverage:1a=not_applicable_sourced; F:ev_001",
        ])
        readiness = self.grader.assess_readiness(
            data["fields"], data["missing_fields"], "vat_return", 2026, notes=data["notes"]
        )
        blockers = " | ".join(readiness["blockers"])
        self.assertIn("applicable_mapped has no mapped field: 1e", blockers)
        self.assertIn("not_applicable_sourced also has a mapped field: 1a", blockers)
        self.assertFalse(readiness["ready"])

    def test_vat_coverage_needs_leading_provenance(self):
        data = _vat_map(notes=["vat_rubric_coverage:1e=not_applicable_sourced; TODO: U: ask user"])
        readiness = self.grader.assess_readiness(
            data["fields"], data["missing_fields"], "vat_return", 2026, notes=data["notes"]
        )
        self.assertTrue(
            any("inapplicable rubric has no provenance: 1e" in blocker for blocker in readiness["blockers"]),
            readiness["blockers"],
        )


if __name__ == "__main__":
    unittest.main()
