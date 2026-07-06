#!/usr/bin/env python3
"""Coverage for the entrepreneur (winst uit onderneming) annual-2025 unlock.

Verifies the eenmanszaak / ZZP unlock is wired end to end: knowledge pack,
source register, workflow gate, the new nl-tax-winst helper, the annual
workflow contract, the field map, intake routing, and the provisional guard.
"""

import importlib.util
import pathlib
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
    return (ROOT / relative_path).read_text(encoding="utf-8")


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
                self.assertEqual(len(entry["content_hash_sha256"]), 64)

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
        self.assertIn("## Must NOT write to", skill)
        self.assertIn("workspace/annual/**", skill)
        self.assertIn("workspace/provisional/**", skill)
        self.assertIn("workspace/shared/winst-notes.md", skill)

    def test_winst_helper_has_invocation_policy(self):
        policy = load_yaml("skills/nl-tax-winst/agents/openai.yaml")
        self.assertIs(policy["policy"]["allow_implicit_invocation"], False)

    def test_winst_helper_is_annual_only(self):
        skill = read_text("skills/nl-tax-winst/SKILL.md").lower()
        # The helper must explicitly forbid the provisional/voorlopige-aanslag use,
        # not merely mention the words — so the annual-only boundary can't regress
        # to a bare token match.
        self.assertIn("annual 2025 only", skill)
        self.assertIn("never prepare winst uit onderneming for", skill)


class AnnualWorkflowTests(unittest.TestCase):
    def test_annual_skill_delegates_to_winst_helper(self):
        skill = read_text("skills/nl-tax-annual-return/SKILL.md")
        self.assertIn("nl-tax-winst", skill)
        self.assertIn("workspace/shared/winst-notes.md", skill)
        self.assertIn("Winst uit onderneming notes", skill)
        self.assertIn("requires 20 sections", skill)

    def test_annual_flow_has_winst_phase(self):
        flow = read_text("skills/nl-tax-annual-return/reference/annual-flow.md")
        self.assertIn("Phase 2A — Winst uit onderneming compilation", flow)
        self.assertIn("business.has_onderneming", flow)

    def test_output_contract_has_winst_requirements(self):
        contract = read_text("skills/nl-tax-annual-return/reference/annual-output-contract.md")
        self.assertIn("Winst uit onderneming requirements", contract)
        self.assertIn("onderneming.belastbare_winst", contract)
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
        self.assertIn("`onderneming.belastbare_winst`", ref)
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

    def test_validator_accepts_annual_onderneming_field(self):
        # The onderneming.* field itself must not be rejected (no portal-automation
        # or werkelijk-rendement false positive). Reference-coverage errors for
        # unrelated required box1 fields are expected in a deliberately minimal map
        # and are not what this test asserts.
        errors, _ = self.validator.validate(
            {
                "field_map_version": "1.0",
                "workflow": "annual_return",
                "tax_year": 2025,
                "fields": [
                    {
                        "field_id": "onderneming.belastbare_winst",
                        "label": "Belastbare winst uit onderneming",
                        "value": 30000,
                        "source": {"type": "calculated", "calculated_from": ["onderneming.omzet"]},
                    }
                ],
                "missing_fields": [],
            }
        )
        self.assertFalse(
            [e for e in errors if "onderneming" in e.lower()],
            f"onderneming field wrongly rejected: {errors}",
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

    def test_provisional_map_allows_plain_business_profit_estimate(self):
        # A plain estimate of expected business profit IS allowed in provisional,
        # as long as it carries no annual onderneming.* prefix or deduction term.
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
                    }
                ],
                "missing_fields": [],
            }
        )
        self.assertFalse(
            [e for e in errors if "entrepreneur" in e.lower()],
            f"plain business-profit estimate wrongly rejected: {errors}",
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

    def test_provisional_forbids_winst(self):
        skill = read_text("skills/nl-tax-provisional-assessment/SKILL.md")
        # The provisional flow must explicitly refuse winst uit onderneming and must
        # not delegate to the annual-only winst helper.
        self.assertIn("Do not prepare winst uit onderneming", skill)
        self.assertIn("entrepreneur unlock is annual 2025 only", skill)
        self.assertNotIn("nl-tax-winst helper", skill)

    def test_evidence_types_have_business_category(self):
        types = read_text("skills/nl-tax-evidence-indexer/reference/evidence-types.md")
        self.assertIn("Business / Enterprise", types)
        for token in ("winst_verlies_rekening", "balans", "urenadministratie", "factuur"):
            with self.subTest(token=token):
                self.assertIn(token, types)


if __name__ == "__main__":
    unittest.main()
