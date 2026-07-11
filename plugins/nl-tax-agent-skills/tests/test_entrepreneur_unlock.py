#!/usr/bin/env python3
"""Coverage for the entrepreneur (winst uit onderneming) annual-2025 unlock.

Verifies the eenmanszaak / ZZP unlock is wired end to end: knowledge pack,
source register, workflow gate, the new nl-tax-winst helper, the annual
workflow contract, the field map, intake routing, and the provisional guard.
"""

import importlib.util
import pathlib
import re
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]

ENTREPRENEUR_DIR = ROOT / "skills/_shared/knowledge/years/2025/entrepreneur"
ENTREPRENEUR_NOTES = [
    "ondernemer-criteria.md",
    "ondernemersaftrek.md",
    "mkb-winstvrijstelling.md",
    "investeringsaftrek.md",
    "winst-en-kosten.md",
    "entrepreneur-aangifte.md",
]
ENTREPRENEUR_SOURCE_IDS = {
    "bd_ondernemer_criteria_2025",
    "bd_ondernemerscheck_2025",
    "bd_urencriterium_2025",
    "bd_ondernemersaftrek_2025",
    "bd_zelfstandigenaftrek_2025",
    "bd_startersaftrek_2025",
    "bd_startersaftrek_ao_2025",
    "bd_meewerkaftrek_2025",
    "bd_stakingsaftrek_2025",
    "bd_so_aftrek_2025",
    "bd_mkb_winstvrijstelling_2025",
    "bd_kia_2025",
    "bd_eia_2025",
    "bd_eia_mia_vamil_2025",
    "bd_zakelijke_kosten_2025",
    "bd_beperkt_aftrekbare_kosten_2025",
    "bd_werkruimte_2025",
    "bd_privevervoermiddel_2025",
    "bd_oudedagsreserve_2025",
    "bd_administratie_bewaren_2025",
    "bd_aangifte_ondernemers_2025",
    "bd_ondernemer_cijfers_aangifte_2025",
    "bd_ondernemer_voorbereiden_2025",
}


def read_text(relative_path):
    path = ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    if relative_path == "skills/nl-tax-annual-return/reference/annual-flow.md":
        links = re.findall(r"\]\((phases/[^)]+\.md)\)", text)
        text += "\n".join(
            (path.parent / link).read_text(encoding="utf-8") for link in links
        )
    elif relative_path == "skills/nl-tax-provisional-assessment/SKILL.md":
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


def load_yaml(relative_path):
    return yaml.safe_load(read_text(relative_path))


def load_module(relative_path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KnowledgePackTests(unittest.TestCase):
    def test_entrepreneur_notes_exist_and_are_reviewed(self):
        for note in ENTREPRENEUR_NOTES:
            path = ENTREPRENEUR_DIR / note
            with self.subTest(note=note):
                self.assertTrue(path.is_file(), f"missing {note}")
                text = path.read_text(encoding="utf-8")
                self.assertIn("workflow: annual_return", text)
                self.assertIn("tax_year: 2025", text)
                self.assertIn("review_status: reviewed", text)

    def test_snapshot_metadata_covers_all_entrepreneur_sources(self):
        meta = yaml.safe_load((ENTREPRENEUR_DIR / "_snapshot-metadata.yaml").read_text())
        self.assertEqual(set(meta["sources"].keys()), ENTREPRENEUR_SOURCE_IDS)
        for sid, entry in meta["sources"].items():
            with self.subTest(source=sid):
                self.assertEqual(entry["review_status"], "reviewed")
                self.assertEqual(len(entry["reviewed_note_hash_sha256"]), 64)

    def test_key_2025_amounts_present_in_notes(self):
        # Adversarially verified 2025 figures (belastingdienst.nl / wetten.overheid.nl).
        ondernemersaftrek = (ENTREPRENEUR_DIR / "ondernemersaftrek.md").read_text()
        self.assertIn("EUR 2,470", ondernemersaftrek)   # zelfstandigenaftrek 2025
        self.assertIn("EUR 2,123", ondernemersaftrek)   # startersaftrek 2025
        self.assertIn("EUR 15,738", ondernemersaftrek)  # S&O-aftrek base 2025
        self.assertIn("EUR 3,630", ondernemersaftrek)   # stakingsaftrek 2025
        mkb = (ENTREPRENEUR_DIR / "mkb-winstvrijstelling.md").read_text()
        self.assertIn("12.7%", mkb)                     # MKB-winstvrijstelling 2025
        criteria = (ENTREPRENEUR_DIR / "ondernemer-criteria.md").read_text()
        self.assertIn("1,225 hours", criteria)          # urencriterium


class SourceRegisterTests(unittest.TestCase):
    def setUp(self):
        self.register = load_yaml("skills/_shared/source-register.yaml")
        self.by_id = {s["id"]: s for s in self.register["sources"]}

    def test_all_entrepreneur_sources_registered(self):
        self.assertTrue(ENTREPRENEUR_SOURCE_IDS.issubset(self.by_id.keys()))

    def test_entrepreneur_sources_are_annual_2025_and_mandatory(self):
        for sid in ENTREPRENEUR_SOURCE_IDS:
            src = self.by_id[sid]
            with self.subTest(source=sid):
                self.assertEqual(src["workflow"], "annual_return")
                self.assertEqual(src["tax_year"], 2025)
                self.assertIn("entrepreneur/", src["snapshot_path"])
                self.assertIn("nl-tax-annual-return", src["mandatory_for"])
                self.assertIn("nl-tax-winst", src["mandatory_for"])


class WorkflowGateTests(unittest.TestCase):
    def setUp(self):
        self.workflows = load_yaml("skills/_shared/supported-workflows.yaml")
        self.annual = next(
            w for w in self.workflows["active_workflows"] if w["id"] == "annual_2025"
        )

    def test_entrepreneur_dir_in_annual_knowledge_dirs(self):
        self.assertIn(
            "skills/_shared/knowledge/years/2025/entrepreneur",
            self.annual["knowledge_dirs"],
        )

    def test_entrepreneur_sources_required_by_annual(self):
        self.assertTrue(
            ENTREPRENEUR_SOURCE_IDS.issubset(set(self.annual["required_source_ids"]))
        )

    def test_complex_business_roadmap_still_blocked(self):
        blocked = {w["id"]: w for w in self.workflows["blocked_workflows"]}
        entry = blocked["annual_2025_entrepreneurs_roadmap"]
        self.assertEqual(entry["status"], "blocked_pending_official_sources")
        self.assertIs(entry["may_prepare_workpack"], False)
        self.assertEqual(entry["case_scope"], "complex_business_profit")
        self.assertIn("annual_2025_entrepreneurs", entry["profile_candidates"])

    def test_validators_know_the_winst_helper(self):
        reg = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_source_register.py",
            "vsr_entrepreneur",
        )
        self.assertIn("nl-tax-winst", reg.VALID_SKILL_NAMES)
        sw = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py",
            "vsw_entrepreneur",
        )
        hints = dict(sw.KNOWLEDGE_SKILL_HINTS)
        self.assertEqual(hints.get("entrepreneur"), "nl-tax-winst")


class WinstHelperTests(unittest.TestCase):
    def test_winst_helper_is_internal_and_bounded(self):
        skill = read_text("skills/nl-tax-winst/SKILL.md")
        self.assertIn("user-invocable: false", skill)
        self.assertIn("called through a Skill/Task tool or inlined by an owning workflow", skill)
        self.assertIn("Return structured facts and open questions", skill)
        self.assertIn("Do not\npersist any final artifact", skill)
        self.assertNotIn("  - Write\n", skill)
        self.assertNotIn("  - Edit\n", skill)
        normalized = " ".join(skill.lower().split())
        self.assertIn("the annual workflow owns persistence in annual mode", normalized)
        self.assertIn("the provisional workflow owns persistence in provisional mode", normalized)
        self.assertIn("the helper owns no persisted artifact", normalized)

    def test_winst_helper_has_invocation_policy(self):
        policy = load_yaml("skills/nl-tax-winst/agents/openai.yaml")
        self.assertIs(policy["policy"]["allow_implicit_invocation"], False)

    def test_winst_helper_has_bounded_annual_and_provisional_modes(self):
        skill = read_text("skills/nl-tax-winst/SKILL.md").lower()
        self.assertIn("preparation-only", skill)
        self.assertIn("finalized profit-and-loss", skill)
        self.assertIn("finalized balance", skill)
        self.assertIn("provisional 2026", skill)
        self.assertIn("expected-profit forecast", skill)
        self.assertNotIn("calculate final taxable business profit", skill)

    def test_winst_helper_loads_only_the_active_mode(self):
        skill = read_text("skills/nl-tax-winst/SKILL.md").lower()
        annual = skill.split("for **annual 2025 preparation-only**", 1)[1].split(
            "for **provisional 2026 expected-profit forecast**", 1
        )[0]
        provisional = skill.split(
            "for **provisional 2026 expected-profit forecast**", 1
        )[1].split("there are no bundled calculators", 1)[0]
        self.assertIn("years/2025/entrepreneur", annual)
        self.assertNotIn("winst-2026-provisional", annual)
        self.assertIn("winst-2026-provisional", provisional)
        self.assertNotIn("years/2025/entrepreneur", provisional)
        self.assertIn("do not load the annual 2025", provisional)
        self.assertIn("or `reference/winst-2025.md`", provisional)


class AnnualWorkflowTests(unittest.TestCase):
    def test_annual_skill_delegates_to_winst_helper(self):
        skill = read_text("skills/nl-tax-annual-return/SKILL.md")
        self.assertIn("nl-tax-winst", skill)
        self.assertIn("persist the returned facts and open questions", skill)
        self.assertIn("resume compatibility only", skill)
        self.assertIn("Winst uit onderneming notes", skill)
        self.assertIn("requires 20 sections", skill)

    def test_annual_flow_has_winst_phase(self):
        flow = read_text("skills/nl-tax-annual-return/reference/annual-flow.md")
        self.assertIn("Phase 2A — Winst uit onderneming preparation-only", flow)
        self.assertIn("business.has_onderneming", flow)

    def test_output_contract_has_winst_requirements(self):
        contract = read_text("skills/nl-tax-annual-return/reference/annual-output-contract.md")
        self.assertIn("Winst uit onderneming requirements", contract)
        self.assertIn("profit-and-loss", contract.lower())
        self.assertIn("balance", contract.lower())
        self.assertIn("preparation-only", contract.lower())
        self.assertNotIn("calculate final taxable business profit", contract.lower())
        self.assertIn("business.has_onderneming: no", contract)

    def test_template_has_winst_section_and_hook(self):
        template = read_text("skills/nl-tax-annual-return/templates/annual-return-pack.md")
        self.assertIn("## Winst uit onderneming notes", template)
        self.assertIn("business.has_onderneming: no", template)


class FieldMapTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "vfm_entrepreneur",
        )

    def test_reference_has_onderneming_section_never_required(self):
        ref = read_text("skills/nl-tax-field-mapper/reference/annual-field-map.md")
        self.assertIn("## Winst uit onderneming", ref)
        self.assertIn("business-section schema review", ref)
        self.assertNotIn("`onderneming.belastbare_winst`", ref)
        # required_reference_fields() must find no onderneming.* row marked required.
        required = self.validator.required_reference_fields(
            ROOT / "skills/nl-tax-field-mapper/reference/annual-field-map.md"
        )
        self.assertFalse(
            [f for f in required if f.startswith("onderneming.")],
            "onderneming.* rows must be conditional/optional, never required",
        )

    def test_renderer_groups_onderneming_fields(self):
        renderer = load_module(
            "skills/nl-tax-field-mapper/scripts/render_field_map.py",
            "rfm_entrepreneur",
        )
        self.assertEqual(
            renderer.infer_section("onderneming.belastbare_winst"),
            "Winst uit onderneming",
        )

    def test_annual_entrepreneur_map_stays_draft_with_business_blocker(self):
        data = {
            "field_map_version": "1.0",
            "workflow": "annual_return",
            "tax_year": 2025,
            "readiness": "draft",
            "fields": [
                {
                    "field_id": "business.has_onderneming",
                    "label": "Heeft onderneming",
                    "value": True,
                    "source": {"type": "user_chat", "quote": "yes", "stated_at": "2026-07-11"},
                    "manual_review_required": True,
                }
            ],
            "missing_fields": [],
        }
        errors, _ = self.validator.validate(data)
        readiness = self.validator.assess_readiness(
            data["fields"], data["missing_fields"], "annual_return", 2025
        )
        self.assertFalse([e for e in errors if "business-section" in e.lower()])
        self.assertFalse(readiness["ready"])
        self.assertIn("business-section schema review", readiness["blockers"])

    def test_annual_business_routing_requires_boolean_and_cannot_bypass_blocker(self):
        for value in ("true", "yes", 1):
            field = {
                "field_id": "business.has_onderneming",
                "label": "Heeft onderneming",
                "value": value,
                "source": {"type": "user_chat", "quote": str(value), "stated_at": "2026-07-11"},
                "manual_review_required": True,
            }
            errors, _ = self.validator.validate(
                {
                    "field_map_version": "1.0",
                    "workflow": "annual_return",
                    "tax_year": 2025,
                    "readiness": "draft",
                    "fields": [field],
                    "missing_fields": [
                        {"field_id": "box1.loon"},
                        {"field_id": "box1.loonheffing"},
                    ],
                }
            )
            readiness = self.validator.assess_readiness(
                [field], [], "annual_return", 2025
            )
            with self.subTest(value=value):
                self.assertTrue(any("boolean" in error.lower() for error in errors), errors)
                self.assertIn("business-section schema review", readiness["blockers"])

    def test_annual_business_boolean_true_blocks_and_false_does_not(self):
        def readiness_for(value):
            return self.validator.assess_readiness(
                [
                    {
                        "field_id": "business.has_onderneming",
                        "value": value,
                        "source": {"type": "user_chat", "quote": str(value), "stated_at": "2026-07-11"},
                    }
                ],
                [],
                "annual_return",
                2025,
            )

        self.assertIn("business-section schema review", readiness_for(True)["blockers"])
        self.assertEqual([], readiness_for(False)["blockers"])

    def test_annual_entrepreneur_map_cannot_claim_review_ready(self):
        errors, warnings = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "annual_return",
                "tax_year": 2025,
                "check_performed_by": "checked_by_agent",
                "readiness": "review_ready",
                "fields": [
                    {
                        "field_id": "business.has_onderneming",
                        "label": "Heeft onderneming",
                        "value": True,
                        "source": {"type": "user_chat", "quote": "yes", "stated_at": "2026-07-11"},
                        "manual_review_required": True,
                    }
                ],
                "missing_fields": [
                    {"field_id": "box1.loon"},
                    {"field_id": "box1.loonheffing"},
                ],
            }
        )
        self.assertFalse(errors)
        self.assertTrue(
            any("review_ready" in warning and "business-section" in warning for warning in warnings),
            warnings,
        )

    def test_provisional_map_rejects_entrepreneur_deductions(self):
        # winst deductions are annual-only; a provisional map must hard-reject them.
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "onderneming.zelfstandigenaftrek",
                        "label": "Zelfstandigenaftrek",
                        "value": 2470,
                        "source": {"type": "estimate"},
                    }
                ],
                "missing_fields": [],
            }
        )
        self.assertTrue(
            any("entrepreneur" in e.lower() for e in errors),
            f"provisional map should reject entrepreneur deductions: {errors}",
        )

    def test_provisional_map_allows_expected_business_profit_field(self):
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "onderneming.geschatte_winst",
                        "label": "Geschatte winst uit onderneming",
                        "value": 40000,
                        "source": {"type": "user_chat", "quote": "EUR 40,000", "stated_at": "2026-07-11"},
                        "manual_review_required": True,
                    }
                ],
                "missing_fields": [],
            }
        )
        self.assertFalse(
            [e for e in errors if "entrepreneur" in e.lower()],
            f"expected-profit field wrongly rejected: {errors}",
        )

    def test_provisional_expected_profit_rejects_embedded_annual_deduction(self):
        for contaminated_key, contaminated_value in (
            ("label", "Geschatte winst met zelfstandigenaftrek"),
            ("notes", "Apply ondernemersaftrek before entry"),
            ("quote", "EUR 40,000 after zelfstandigenaftrek"),
        ):
            field = {
                "field_id": "onderneming.geschatte_winst",
                "label": "Geschatte winst uit onderneming",
                "value": 40000,
                "source": {
                    "type": "user_chat",
                    "quote": "EUR 40,000",
                    "stated_at": "2026-07-11",
                },
                "manual_review_required": True,
            }
            if contaminated_key == "quote":
                field["source"]["quote"] = contaminated_value
            else:
                field[contaminated_key] = contaminated_value
            errors, _ = self.validator.validate(
                {
                    "field_map_version": "1.0",
                    "workflow": "provisional_assessment",
                    "tax_year": 2026,
                    "fields": [field],
                    "missing_fields": [],
                }
            )
            with self.subTest(contaminated_key=contaminated_key):
                self.assertTrue(
                    any("deduction" in error.lower() for error in errors), errors
                )

    def test_provisional_map_rejects_generic_other_income_business_substitution(self):
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box1.geschat_overig_inkomen",
                        "label": "Geschatte winst uit onderneming",
                        "value": 40000,
                        "source": {"type": "estimate"},
                        "manual_review_required": True,
                    }
                ],
                "missing_fields": [],
            }
        )
        self.assertTrue(any("dedicated expected-profit" in e.lower() for e in errors), errors)

    def test_provisional_business_profit_substitution_is_rejected_for_any_field(self):
        cases = (
            ("custom.forecast", "Winst uit onderneming", "", "EUR 40,000"),
            ("income.ondernemingswinst", "Forecast", "", "EUR 40,000"),
            ("custom.forecast", "Forecast", "business-profit for 2026", "EUR 40,000"),
            ("custom.forecast", "Forecast", "", "enterprise_profit EUR 40,000"),
            ("custom.forecast", "Self-employment income", "", "EUR 40,000"),
        )
        for field_id, label, notes, quote in cases:
            errors, _ = self.validator.validate(
                {
                    "field_map_version": "1.0",
                    "workflow": "provisional_assessment",
                    "tax_year": 2026,
                    "fields": [
                        {
                            "field_id": field_id,
                            "label": label,
                            "notes": notes,
                            "value": 40000,
                            "source": {"type": "user_chat", "quote": quote, "stated_at": "2026-07-11"},
                            "manual_review_required": True,
                        }
                    ],
                    "missing_fields": [],
                }
            )
            with self.subTest(field_id=field_id, label=label, notes=notes, quote=quote):
                self.assertTrue(
                    any("onderneming.geschatte_winst" in error for error in errors), errors
                )

    def test_provisional_unrelated_other_income_remains_allowed(self):
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box1.geschat_overig_inkomen",
                        "label": "Estimated rental income",
                        "value": 1200,
                        "source": {"type": "user_chat", "quote": "EUR 1,200 rent", "stated_at": "2026-07-11"},
                        "manual_review_required": True,
                    }
                ],
                "missing_fields": [],
            }
        )
        self.assertFalse(
            [error for error in errors if "onderneming.geschatte_winst" in error], errors
        )

    def test_provisional_missing_business_forecast_uses_dedicated_field(self):
        rejected, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [],
                "missing_fields": [
                    {
                        "field_id": "custom.self_employment_income",
                        "label": "Self-employment income forecast",
                    }
                ],
            }
        )
        allowed, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [],
                "missing_fields": [
                    {
                        "field_id": "onderneming.geschatte_winst",
                        "label": "Geschatte winst uit onderneming",
                    }
                ],
            }
        )
        self.assertTrue(
            any("onderneming.geschatte_winst" in error for error in rejected), rejected
        )
        self.assertFalse(
            [error for error in allowed if "entrepreneur" in error.lower()], allowed
        )

    def test_provisional_missing_expected_profit_rejects_deduction_contamination(self):
        for key, value in (
            ("label", "Expected profit after zelfstandigenaftrek"),
            ("reason", "Need forecast after ondernemersaftrek"),
            ("notes", "Apply KIA before supplying this amount"),
        ):
            missing = {
                "field_id": "onderneming.geschatte_winst",
                "label": "Geschatte winst uit onderneming",
            }
            missing[key] = value
            errors, _ = self.validator.validate(
                {
                    "field_map_version": "1.0",
                    "workflow": "provisional_assessment",
                    "tax_year": 2026,
                    "fields": [],
                    "missing_fields": [missing],
                }
            )
            with self.subTest(key=key):
                self.assertTrue(
                    any("deduction" in error.lower() for error in errors), errors
                )

    def test_provisional_map_rejects_bare_kia_token(self):
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box1.geschat_overig_inkomen",
                        "label": "KIA",
                        "value": 1200,
                        "source": {"type": "estimate"},
                    }
                ],
                "missing_fields": [],
            }
        )

        self.assertTrue(
            any("entrepreneur" in e.lower() for e in errors),
            f"provisional map should reject bare KIA token: {errors}",
        )

    def test_provisional_map_allows_kia_inside_unrelated_word(self):
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "provisional_assessment",
                "tax_year": 2026,
                "fields": [
                    {
                        "field_id": "box1.geschat_overig_inkomen",
                        "label": "Skialessen vergoeding",
                        "value": 250,
                        "source": {"type": "estimate"},
                    }
                ],
                "missing_fields": [],
            }
        )

        self.assertFalse(
            [e for e in errors if "entrepreneur" in e.lower()],
            f"unrelated word containing kia wrongly rejected: {errors}",
        )


class IntakeAndProvisionalTests(unittest.TestCase):
    def test_intake_supports_eenmanszaak(self):
        skill = read_text("skills/nl-tax-intake/SKILL.md")
        unsupported = read_text("skills/nl-tax-intake/reference/unsupported-cases.md")
        self.assertIn("business.has_onderneming", skill)
        self.assertIn("eenmanszaak", skill.lower())
        # The blocked candidate stays reachable for complex business forms.
        self.assertIn("annual_2025_entrepreneurs", skill)
        self.assertIn("annual_2025_entrepreneurs", unsupported)
        self.assertIn("eenmanszaak", unsupported.lower())

    def test_profile_template_has_business_section(self):
        profile = load_yaml("skills/nl-tax-intake/templates/taxpayer-profile.yaml")
        self.assertIn("business", profile)
        self.assertIn("has_onderneming", profile["business"])
        self.assertIn("complex_business_screening", profile["routing"])

    def test_provisional_supports_only_sourced_expected_profit(self):
        skill = read_text("skills/nl-tax-provisional-assessment/SKILL.md")
        reference = read_text("skills/nl-tax-winst/reference/winst-2026-provisional.md")
        business_section = read_text(
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        )
        self.assertIn("nl-tax-winst", skill)
        self.assertIn("`onderneming.geschatte_winst`", reference)
        self.assertIn("manual review", reference.lower())
        self.assertNotIn("`box1.geschat_overig_inkomen`", business_section)
        for forbidden in ("zelfstandigenaftrek", "mkb-winstvrijstelling", "zvw", "cessation profit", "final tax"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, reference.lower())

    def test_evidence_types_have_business_category(self):
        types = read_text("skills/nl-tax-evidence-indexer/reference/evidence-types.md")
        self.assertIn("Business / Enterprise", types)
        for token in ("winst_verlies_rekening", "balans", "urenadministratie", "factuur"):
            with self.subTest(token=token):
                self.assertIn(token, types)


if __name__ == "__main__":
    unittest.main()
