#!/usr/bin/env python3
"""Regression tests for the full-audit follow-up fixes.

Covers:
    - Cross-host invocation policy: every non-user-invocable skill ships an
      agents/openai.yaml with policy.allow_implicit_invocation: false.
    - Field-map identifier-placeholder convention (BSN/IBAN live in
      missing_fields without a value; the portal pre-fills them).
    - The two marketplace.json files agree on plugin name and path.
"""

import importlib.util
import json
import pathlib
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
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
            "../../tools/nl_tax_agent_skills/source_maintenance/scripts/validate_invocation_policy.py",
            "validate_invocation_policy",
        )

    def test_real_skills_pass(self):
        errors, checked = self.mod.collect_errors(str(SKILLS_DIR))
        self.assertEqual(errors, [], f"unexpected invocation-policy errors: {errors}")
        # Only the hidden shared skill and background helpers are guarded.
        self.assertEqual(
            set(checked),
            {
                "nl-tax-shared-resources",
                "nl-tax-box1-home",
                "nl-tax-box2",
                "nl-tax-box3",
                "nl-tax-partner-deductions",
                "nl-tax-winst",
            },
        )
        for name in (
            "nl-tax-box1-home",
            "nl-tax-box2",
            "nl-tax-box3",
            "nl-tax-partner-deductions",
            "nl-tax-winst",
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


class FieldMapIdentifierPlaceholderTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module(
            "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py",
            "validate_field_map_guard",
        )

    def test_bsn_placeholder_in_missing_fields_still_passes(self):
        # The established convention: personal.bsn lives in missing_fields with no
        # value (the portal pre-fills it). That path must remain valid.
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
            any("bsn" in e.lower() or "iban" in e.lower() for e in errors),
            errors,
        )


class MarketplaceConsistencyTests(unittest.TestCase):
    @staticmethod
    def _plugin_entry(path):
        data = json.loads(path.read_text(encoding="utf-8"))
        plugins = data.get("plugins", [])
        if not plugins:
            raise AssertionError(f"no plugins in {path}")
        return plugins[0]

    @staticmethod
    def _source_path(entry):
        source = entry.get("source")
        if isinstance(source, str):
            return source
        if isinstance(source, dict):
            return source.get("path")
        return None

    @unittest.skipUnless(
        (REPO_ROOT / ".claude-plugin" / "marketplace.json").is_file()
        and (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").is_file(),
        "dev-repo marketplace manifests not present — standalone package run",
    )
    def test_marketplaces_agree_on_name_path_and_description(self):
        claude_marketplace_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        claude_marketplace = json.loads(
            claude_marketplace_path.read_text(encoding="utf-8")
        )
        claude = self._plugin_entry(claude_marketplace_path)
        agents = self._plugin_entry(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
        canonical = json.loads(
            (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )["description"]
        self.assertEqual(claude.get("name"), agents.get("name"))
        self.assertEqual(self._source_path(claude), self._source_path(agents))
        self.assertEqual(claude.get("name"), "nl-tax-agent-skills")
        self.assertEqual(self._source_path(claude), "./plugins/nl-tax-agent-skills")
        self.assertEqual(claude.get("description"), canonical)
        self.assertEqual(agents.get("description"), canonical)
        self.assertIn(
            "Conversational, source-traceable",
            claude_marketplace.get("description", ""),
        )


if __name__ == "__main__":
    unittest.main()
