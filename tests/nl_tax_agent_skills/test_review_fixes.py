#!/usr/bin/env python3
"""Regression tests for fixes from the 2026-07 Python code review."""

import importlib.util
import pathlib
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"


def load_module(relative_path, name):
    module_path = PLUGIN_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    # Register before exec so module-level dataclasses resolve on Python 3.12+.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class InvocationPolicyFrontmatterTests(unittest.TestCase):
    """validate_invocation_policy must fail closed on odd frontmatter."""

    def setUp(self):
        self.mod = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_invocation_policy.py",
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


class PlanSourceRefreshUrlAllowlistTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py",
            "plan_source_refresh_review",
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


class FieldMapWerkelijkScanTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
            "validate_field_map_review",
        )

    def _base_map(self, **overrides):
        data = {
            "field_map_version": "1.0",
            "workflow": "provisional_assessment",
            "tax_year": 2026,
            "check_performed_by": "checked_by_agent",
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


class EvalVerifierGlobEscapeTests(unittest.TestCase):
    VERIFIER = REPO_ROOT / "evals/nl-tax-agent-skills/verify_offline_workspace.py"

    @unittest.skipUnless(VERIFIER.is_file(), "offline eval verifier not present")
    def test_workspace_path_with_glob_metacharacters(self):
        spec = importlib.util.spec_from_file_location("verify_offline_ws_review", self.VERIFIER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "run [2026]"
            target = workspace / "workspace"
            target.mkdir(parents=True)
            (target / "nl-tax-annual-2025-workpack.md").write_text(
                "# Annual workpack\n", encoding="utf-8"
            )
            matches = mod.glob_matches(workspace, "workspace/nl-tax-*-workpack.md")
        self.assertEqual(len(matches), 1, matches)


if __name__ == "__main__":
    unittest.main()
