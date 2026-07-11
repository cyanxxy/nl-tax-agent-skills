#!/usr/bin/env python3
"""Regression tests for fixes from the 2026-07 Python code review."""

import importlib.util
import pathlib
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
PLUGIN_ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(relative_path, name):
    module_path = PLUGIN_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    # Register before exec so module-level dataclasses resolve on Python 3.12+.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CoerceScalarDutchThousandsTests(unittest.TestCase):
    """classify_box3_assets: '50.000' must be fifty thousand, not fifty."""

    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-box3/scripts/classify_box3_assets.py",
            "classify_box3_assets_review",
        )

    def test_dot_thousands_parse_before_float(self):
        self.assertEqual(self.mod._coerce_scalar("50.000"), 50_000)
        self.assertEqual(self.mod._coerce_scalar("1.234.567"), 1_234_567)

    def test_comma_thousands_and_dutch_decimal_comma(self):
        self.assertEqual(self.mod._coerce_scalar("50,000"), 50_000)
        self.assertEqual(self.mod._coerce_scalar("50.000,50"), 50_000.5)
        self.assertEqual(self.mod._coerce_scalar("50000,50"), 50_000.5)

    def test_plain_numbers_still_parse(self):
        self.assertEqual(self.mod._coerce_scalar("50"), 50)
        self.assertEqual(self.mod._coerce_scalar("50.5"), 50.5)
        self.assertEqual(self.mod._coerce_scalar("-3.25"), -3.25)

    def test_non_numeric_text_unchanged(self):
        self.assertEqual(self.mod._coerce_scalar("spaarrekening"), "spaarrekening")


class InvocationPolicyFrontmatterTests(unittest.TestCase):
    """validate_invocation_policy must fail closed on odd frontmatter."""

    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_invocation_policy.py",
            "validate_invocation_policy_review",
        )

    def _write_skill(self, tmp, name, skill_md, openai_yaml=None):
        skill_dir = pathlib.Path(tmp) / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
        if openai_yaml is not None:
            agents = skill_dir / "agents"
            agents.mkdir()
            (agents / "openai.yaml").write_text(openai_yaml, encoding="utf-8")
        return skill_dir

    def test_triple_dash_inside_value_does_not_truncate_frontmatter(self):
        skill_md = (
            "---\n"
            'description: "helper --- background use only"\n'
            "disable-model-invocation: true\n"
            "---\n"
            "# Body\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            self._write_skill(tmp, "helper-a", skill_md)
            errors, checked = self.mod.collect_errors(tmp)
        # The skill must still be RECOGNIZED as non-user-invocable (fail
        # closed) and flagged for its missing openai.yaml.
        self.assertIn("helper-a", checked)
        self.assertTrue(any(name == "helper-a" for name, _ in errors))

    def test_invalid_yaml_frontmatter_is_an_error_not_a_skip(self):
        skill_md = "---\ndescription: [unclosed\n---\n# Body\n"
        with tempfile.TemporaryDirectory() as tmp:
            self._write_skill(tmp, "helper-b", skill_md)
            errors, _ = self.mod.collect_errors(tmp)
        self.assertTrue(
            any(name == "helper-b" and "frontmatter" in reason for name, reason in errors),
            errors,
        )

    def test_compliant_helper_passes(self):
        skill_md = "---\nuser-invocable: false\n---\n# Body\n"
        openai_yaml = "policy:\n  allow_implicit_invocation: false\n"
        with tempfile.TemporaryDirectory() as tmp:
            self._write_skill(tmp, "helper-c", skill_md, openai_yaml)
            errors, checked = self.mod.collect_errors(tmp)
        self.assertEqual(errors, [])
        self.assertEqual(checked, ["helper-c"])


class FetchSourcesUrlAllowlistTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-source-refresh/scripts/fetch_sources.py",
            "fetch_sources_review",
        )

    def test_userinfo_trick_is_rejected(self):
        self.assertFalse(
            self.mod.is_url_allowed("https://www.belastingdienst.nl:pw@evil.com/x")
        )
        self.assertFalse(
            self.mod.is_url_allowed("https://www.belastingdienst.nl@evil.com/x")
        )

    def test_non_https_scheme_is_rejected(self):
        self.assertFalse(self.mod.is_url_allowed("http://www.belastingdienst.nl/a"))

    def test_allowed_https_url_passes(self):
        self.assertTrue(self.mod.is_url_allowed("https://www.belastingdienst.nl/a"))


class Box2InputHardeningTests(unittest.TestCase):
    def setUp(self):
        self.calc = load_module(
            "skills/nl-tax-box2/scripts/calculate_box2_tax.py",
            "calculate_box2_tax_review",
        )

    def test_nan_and_inf_raise_clean_value_error(self):
        for bad in (float("nan"), float("inf"), "-inf"):
            with self.subTest(bad=bad):
                result = self.calc.calculate_from_payload(
                    {
                        "workflow": "annual_2025",
                        "tax_year": 2025,
                        "substantial_interest_pct": 10,
                        "resident_full_year": True,
                        "standard_ab_case": True,
                        "regular_benefits": bad,
                        "disposal_benefit": 0,
                        "loss_setoff": 0,
                    }
                )
                self.assertTrue(result["errors"])
                self.assertIsNone(result["result"])

    def test_unknown_payload_key_is_flagged(self):
        result = self.calc.calculate_from_payload(
            {
                "workflow": "annual_2025",
                "tax_year": 2025,
                "substantial_interest_pct": 10,
                "resident_full_year": True,
                "standard_ab_case": True,
                "regular_benefit": 10_000,
            }  # typo'd key
        )
        self.assertTrue(
            any("regular_benefit" in error for error in result.get("errors", [])),
            result.get("errors"),
        )

    def test_explicit_zero_disposal_price_matches_calculator_presence_rule(self):
        # {"disposal_price": 0, "gross_disposal_price": X} computes fine in the
        # calculator, so the validator must not reject it as "not both".
        payload = {
            "workflow": "annual_2025",
            "tax_year": 2025,
            "substantial_interest_pct": 100,
            "disposal_price": 0,
            "gross_disposal_price": 50_000,
            "acquisition_price": 20_000,
        }
        payload.update(
            {
                "resident_full_year": True,
                "standard_ab_case": True,
            }
        )
        result = self.calc.calculate_from_payload(payload)
        self.assertNotIn(
            "provide either disposal_price or gross_disposal_price, not both",
            result["errors"],
        )


class FieldMapWerkelijkScanTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_review",
        )

    def _base_map(self, **overrides):
        data = {
            "field_map_version": "1.0",
            "workflow": "provisional_assessment",
            "tax_year": 2026,
            "fields": [
                {
                    "field_id": "box3.geschatte_banktegoeden",
                    "label": "Geschatte banktegoeden",
                    "source": {"type": "estimate"},
                    "confidence": 0.9,
                    "manual_review_required": False,
                }
            ],
            "missing_fields": [{"field_id": "personal.bsn"}],
        }
        data.update(overrides)
        return data

    def test_werkelijk_in_missing_fields_is_critical(self):
        errors, _ = self.mod.validate(
            self._base_map(
                missing_fields=[
                    {
                        "field_id": "box3.werkelijk_rendement",
                        "reason": "ask user for actual return",
                    }
                ]
            )
        )
        self.assertTrue(
            any("werkelijk" in error.lower() and "missing_fields" in error for error in errors),
            errors,
        )

    def test_collection_instruction_in_top_level_notes_is_critical(self):
        errors, _ = self.mod.validate(
            self._base_map(notes=["Collect werkelijk rendement statements from the bank."])
        )
        self.assertTrue(
            any("top-level notes" in error for error in errors),
            errors,
        )

    def test_explanatory_top_level_note_stays_allowed(self):
        errors, _ = self.mod.validate(
            self._base_map(notes=["Werkelijk rendement is not part of provisional 2026."])
        )
        self.assertEqual(errors, [])

    def test_confidence_bounds_are_enforced(self):
        base = self._base_map()
        base["fields"][0]["confidence"] = 1.5
        errors, _ = self.mod.validate(base)
        self.assertTrue(any("Confidence out of range" in error for error in errors), errors)

        base = self._base_map()
        base["fields"][0]["confidence"] = "high"
        errors, _ = self.mod.validate(base)
        self.assertTrue(any("Confidence must be a number" in error for error in errors), errors)


class Box1NanGuardTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-box1-home/scripts/validate_own_home_inputs.py",
            "validate_own_home_inputs_review",
        )

    def test_nan_cli_value_exits_cleanly(self):
        import contextlib
        import io

        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.mod._parse_value("--mortgage-interest", "nan", float)

    def test_no_deductible_costs_means_no_tariefsaanpassing(self):
        # With zero aftrekbare kosten there is nothing for the rate
        # adjustment to correct, regardless of income.
        applies, amount, _ = self.mod.calculate_tariefsaanpassing(
            deductible_costs=0.0,
            belastbaar_inkomen=200_000,
            tax_year=2026,
        )
        self.assertFalse(applies)
        self.assertEqual(amount, 0.0)

    def test_official_hillen_example_2026_still_applies_tariefsaanpassing(self):
        # Belastingdienst Hillen example: grondslag = 80,141 + 3,500 - 78,426
        # capped at the gross aftrekbare kosten 3,500 -> 3,500 x 0.1194 =
        # 417.90 — the adjustment applies even though Hillen leaves a
        # positive eigen-woning result.
        applies, amount, _ = self.mod.calculate_tariefsaanpassing(
            deductible_costs=3_500,
            belastbaar_inkomen=80_141,
            tax_year=2026,
        )
        self.assertTrue(applies)
        self.assertEqual(amount, 417.90)

    def test_tariefsaanpassing_2025_parameters_compute(self):
        # 2025 branch: threshold 76,817 / cap 37.48% -> rate diff 12.02%.
        applies, amount, _ = self.mod.calculate_tariefsaanpassing(
            deductible_costs=5_000,
            belastbaar_inkomen=150_000,
            tax_year=2025,
        )
        self.assertTrue(applies)
        self.assertEqual(amount, 601.00)  # 5000 x 0.1202, exact in Decimal


class EvalVerifierGlobEscapeTests(unittest.TestCase):
    VERIFIER = REPO_ROOT / "evals/nl-tax-agent-skills/verify_offline_workspace.py"

    @unittest.skipUnless(VERIFIER.is_file(), "offline eval verifier not present")
    def test_workspace_path_with_glob_metacharacters(self):
        spec = importlib.util.spec_from_file_location("verify_offline_ws_review", self.VERIFIER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "run [2026]"
            target = workspace / "workspace/annual/2025"
            target.mkdir(parents=True)
            (target / "field-map.yaml").write_text("workflow: annual_return\n", encoding="utf-8")
            matches = mod.glob_matches(workspace, "workspace/annual/*/field-map.yaml")
        self.assertEqual(len(matches), 1, matches)


if __name__ == "__main__":
    unittest.main()
