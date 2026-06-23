#!/usr/bin/env python3
"""Policy and field-map coverage for Box 2 workflow support."""

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR_SCRIPT = ROOT / "skills/nl-tax-field-mapper/scripts/validate_field_map.py"


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
    # ME-24 sensitive scan: spaced IBAN in value, elfproef BSN in notes.
    # ------------------------------------------------------------------
    def test_spaced_iban_in_value_is_rejected(self):
        field = {
            "field_id": "box3.rekening",
            "value": "NL91 ABNA 0417 1643 00",
            "source": {"type": "evidence", "evidence_id": "ev1"},
        }
        errors = []
        self.validator.validate_sensitive_field_values("box3.rekening", field, errors)
        self.assertTrue(any("iban" in e.lower() for e in errors))

    def test_elfproef_bsn_in_notes_is_rejected(self):
        # 123456782 satisfies the Dutch BSN elfproef.
        field = {
            "field_id": "box1.note",
            "notes": ["client mentioned 123456782 in chat"],
            "source": {"type": "user_chat", "quote": "x"},
        }
        errors = []
        self.validator.validate_sensitive_field_values("box1.note", field, errors)
        self.assertTrue(any("bsn" in e.lower() for e in errors))

    def test_non_bsn_nine_digits_not_flagged(self):
        # An arbitrary 9-digit number that fails elfproef must not be flagged.
        field = {
            "field_id": "box1.note",
            "notes": ["invoice 123456789 paid"],
            "source": {"type": "estimate"},
        }
        errors = []
        self.validator.validate_sensitive_field_values("box1.note", field, errors)
        self.assertEqual([], errors)

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
