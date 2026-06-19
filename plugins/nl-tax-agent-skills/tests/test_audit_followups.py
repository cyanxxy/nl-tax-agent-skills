#!/usr/bin/env python3
"""Regression tests for the full-audit follow-up fixes.

Covers three guards added after the audit:
    - Cross-host invocation policy: every non-user-invocable skill ships an
      agents/openai.yaml with policy.allow_implicit_invocation: false.
    - Field-map BSN/IBAN deterministic guard.
    - The two marketplace.json files agree on plugin name and path.
"""

import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]          # plugins/nl-tax-agent-skills
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]     # repo root
SKILLS_DIR = ROOT / "skills"


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InvocationPolicyTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-source-refresh/scripts/validate_invocation_policy.py",
            "validate_invocation_policy",
        )

    def test_real_skills_pass(self):
        errors, checked = self.mod.collect_errors(str(SKILLS_DIR))
        self.assertEqual(errors, [], f"unexpected invocation-policy errors: {errors}")
        # All six background/manual-only skills must be detected and guarded.
        for name in (
            "nl-tax-box1-home",
            "nl-tax-box2",
            "nl-tax-box3",
            "nl-tax-partner-deductions",
            "nl-tax-source-refresh",
            "nl-tax-submit-companion",
        ):
            self.assertIn(name, checked)

    def test_missing_openai_yaml_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = pathlib.Path(tmp)
            helper = skills / "nl-tax-newhelper"
            helper.mkdir()
            (helper / "SKILL.md").write_text(
                "---\nname: nl-tax-newhelper\n"
                "description: helper\nuser-invocable: false\n---\nbody\n",
                encoding="utf-8",
            )
            errors, checked = self.mod.collect_errors(str(skills))
            self.assertIn("nl-tax-newhelper", checked)
            self.assertTrue(errors)
            self.assertEqual(errors[0][0], "nl-tax-newhelper")

    def test_disable_model_invocation_requires_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = pathlib.Path(tmp)
            helper = skills / "nl-tax-manual"
            (helper / "agents").mkdir(parents=True)
            (helper / "SKILL.md").write_text(
                "---\nname: nl-tax-manual\n"
                "description: manual\ndisable-model-invocation: true\n---\nbody\n",
                encoding="utf-8",
            )
            # Wrong policy value -> still fails.
            (helper / "agents" / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: true\n", encoding="utf-8"
            )
            errors, _ = self.mod.collect_errors(str(skills))
            self.assertTrue(errors)
            # Correct policy value -> passes.
            (helper / "agents" / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: false\n", encoding="utf-8"
            )
            errors, _ = self.mod.collect_errors(str(skills))
            self.assertEqual(errors, [])

    def test_user_invocable_skill_not_required_to_have_openai_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = pathlib.Path(tmp)
            entry = skills / "nl-tax-entry"
            entry.mkdir()
            (entry / "SKILL.md").write_text(
                "---\nname: nl-tax-entry\ndescription: entry point\n---\nbody\n",
                encoding="utf-8",
            )
            errors, checked = self.mod.collect_errors(str(skills))
            self.assertEqual(checked, [])
            self.assertEqual(errors, [])


class FieldMapCredentialGuardTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "skills/nl-tax-field-mapper/scripts/validate_field_map.py",
            "validate_field_map_guard",
        )

    def test_bsn_value_in_field_is_rejected(self):
        errors = []
        field = {
            "field_id": "personal.bsn",
            "label": "BSN",
            "value": "111222333",  # valid elfproef BSN
            "source": {"type": "user_chat", "quote": "my bsn is 111222333"},
        }
        self.mod.validate_field(field, 0, "annual_return", set(), errors, [])
        self.assertTrue(any("BSN" in e for e in errors), errors)

    def test_iban_value_in_quote_is_rejected(self):
        errors = []
        field = {
            "field_id": "box3.refund_account",
            "label": "Rekening",
            "value": "NL91ABNA0417164300",
            "source": {"type": "user_chat", "quote": "account NL91ABNA0417164300"},
        }
        self.mod.validate_field(field, 0, "annual_return", set(), errors, [])
        self.assertTrue(any("IBAN" in e for e in errors), errors)

    def test_elfproef_rejects_random_nine_digits(self):
        # A 9-digit number that fails the 11-test should NOT be flagged as a BSN.
        self.assertFalse(self.mod._passes_elfproef("123456789"))
        self.assertTrue(self.mod._passes_elfproef("111222333"))

    def test_bsn_placeholder_in_missing_fields_still_passes(self):
        # The established convention: personal.bsn lives in missing_fields with no
        # value. That path must remain valid (no credential error).
        data = {
            "field_map_version": "1.1",
            "workflow": "provisional_assessment",
            "tax_year": 2026,
            "fields": [
                {
                    "field_id": "box1.loon",
                    "label": "Loon",
                    "value": 45000,
                    "confidence": 0.9,
                    "manual_review_required": False,
                    "source": {"type": "estimate"},
                }
            ],
            "missing_fields": [
                {"field_id": "personal.bsn"},
                {"field_id": "personal.adres"},
            ],
        }
        errors, _ = self.mod.validate(data)
        self.assertFalse(
            any("BSN" in e or "IBAN" in e or "Credential" in e for e in errors),
            errors,
        )


class MarketplaceConsistencyTests(unittest.TestCase):
    @staticmethod
    def _plugin_entry(path):
        data = json.loads(path.read_text(encoding="utf-8"))
        plugins = data.get("plugins", [])
        assert plugins, f"no plugins in {path}"
        return plugins[0]

    @staticmethod
    def _source_path(entry):
        source = entry.get("source")
        if isinstance(source, str):
            return source
        if isinstance(source, dict):
            return source.get("path")
        return None

    def test_marketplaces_agree_on_name_and_path(self):
        claude = self._plugin_entry(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        agents = self._plugin_entry(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(claude.get("name"), agents.get("name"))
        self.assertEqual(self._source_path(claude), self._source_path(agents))
        self.assertEqual(claude.get("name"), "nl-tax-agent-skills")
        self.assertEqual(self._source_path(claude), "./plugins/nl-tax-agent-skills")


if __name__ == "__main__":
    unittest.main()
