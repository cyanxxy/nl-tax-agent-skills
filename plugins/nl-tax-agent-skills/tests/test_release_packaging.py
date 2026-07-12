#!/usr/bin/env python3
"""Release-package contracts for the current cross-host release."""

import json
import pathlib
import unittest

import yaml


REPO = pathlib.Path(__file__).resolve().parents[3]
PLUGIN = REPO / "plugins" / "nl-tax-agent-skills"
SKILLS = PLUGIN / "skills"
REPOSITORY_URL = "https://github.com/cyanxxy/nl-tax-agent-skills"

ARGUMENT_HINTS = {
    "nl-tax-annual-return": "[2025] [confirm]",
    "nl-tax-evidence-indexer": "[path-to-upload-folder]",
    "nl-tax-field-mapper": "[annual|provisional] [year]",
    "nl-tax-intake": "[annual|request|change|review|stopzetten]",
    "nl-tax-provisional-assessment": (
        "[2026] [request|change|review|stopzetten|confirm]"
    ),
    "nl-tax-source-refresh": "[annual|provisional|box3|all] [year]",
    "nl-tax-submit-companion": "[annual|provisional] [2025|2026]",
}

PUBLIC_OPENAI_SKILLS = {
    "nl-tax-annual-return",
    "nl-tax-evidence-indexer",
    "nl-tax-field-mapper",
    "nl-tax-intake",
    "nl-tax-provisional-assessment",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing YAML frontmatter: {path}")
    _, block, _ = text.split("---", 2)
    return yaml.safe_load(block)


class ReleasePackagingTests(unittest.TestCase):
    def test_no_legacy_commands(self):
        self.assertFalse((PLUGIN / "commands").exists())

    def test_exactly_12_workflow_skills_plus_hidden_shared_resources(self):
        paths = list(SKILLS.glob("*/SKILL.md"))
        names = [frontmatter(path)["name"] for path in paths]
        workflow_names = [
            frontmatter(path)["name"] for path in paths if path.parent.name != "_shared"
        ]
        self.assertEqual(len(workflow_names), 12)
        self.assertEqual(len(names), 13)
        self.assertEqual(len(set(names)), 13)
        shared = frontmatter(SKILLS / "_shared/SKILL.md")
        self.assertFalse(shared["user-invocable"])
        self.assertTrue(shared["disable-model-invocation"])

    def test_seven_public_skills_have_exact_argument_hints(self):
        actual = {
            skill_name: frontmatter(SKILLS / skill_name / "SKILL.md").get(
                "argument-hint"
            )
            for skill_name in ARGUMENT_HINTS
        }
        self.assertEqual(actual, ARGUMENT_HINTS)

    def test_manifest_versions_and_metadata(self):
        claude = load_json(PLUGIN / ".claude-plugin/plugin.json")
        codex = load_json(PLUGIN / ".codex-plugin/plugin.json")
        self.assertEqual(claude["version"], "0.1.9")
        self.assertEqual(codex["version"], "0.1.9")
        self.assertEqual(claude["displayName"], "NL Tax Agent Skills")
        self.assertEqual(claude["homepage"], REPOSITORY_URL)
        self.assertEqual(claude["repository"], REPOSITORY_URL)
        self.assertEqual(codex["homepage"], REPOSITORY_URL + "#readme")
        self.assertEqual(codex["repository"], REPOSITORY_URL)
        self.assertIn("Cowork-first, cross-platform", claude["description"])
        self.assertIn("Cowork-first, cross-platform", codex["description"])
        self.assertIn("Claude Cowork", codex["interface"]["longDescription"])
        self.assertIn("ChatGPT Work", codex["interface"]["longDescription"])
        self.assertEqual(len(codex["interface"]["defaultPrompt"]), 3)

    def test_every_skill_loads_the_cross_runtime_contract(self):
        contract = SKILLS / "_shared/runtime-contract.md"
        self.assertTrue(contract.is_file())
        contract_text = contract.read_text(encoding="utf-8")
        for required in (
            "ChatGPT Work on web or mobile",
            "ChatGPT Work or Codex on desktop",
            "Python and shell access are accelerators only",
            "Never depend on a vendor-specific environment variable",
        ):
            self.assertIn(required, contract_text)

        for path in SKILLS.glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                if path.parent.name != "_shared":
                    self.assertIn("../_shared/runtime-contract.md", text)
                self.assertNotIn("${CLAUDE_", text)
                self.assertNotIn("in Cowork's isolated VM", text)
                self.assertNotIn("requires Claude Code", text)
                self.assertNotIn("host file tools", text)

    def test_public_skills_have_openai_interface_metadata(self):
        for skill_name in PUBLIC_OPENAI_SKILLS:
            with self.subTest(skill=skill_name):
                path = SKILLS / skill_name / "agents/openai.yaml"
                self.assertTrue(path.is_file())
                metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
                interface = metadata["interface"]
                self.assertTrue(interface["display_name"])
                self.assertTrue(interface["short_description"])
                self.assertTrue(interface["default_prompt"])
                self.assertTrue(metadata["policy"]["allow_implicit_invocation"])
                for icon_key in ("icon_small", "icon_large"):
                    icon_path = (path.parent.parent / interface[icon_key]).resolve()
                    self.assertTrue(icon_path.is_file(), icon_path)

    def test_openai_submission_pack_has_exact_reviewer_case_counts(self):
        submission = REPO / "submission/openai"
        cases = yaml.safe_load(
            (submission / "test-cases.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(len(cases["positive"]), 5)
        self.assertEqual(len(cases["negative"]), 3)
        self.assertEqual(
            len({case["id"] for case in cases["positive"] + cases["negative"]}),
            8,
        )
        self.assertTrue((submission / "README.md").is_file())
        self.assertTrue((submission / "release-notes.md").is_file())

    def test_only_the_retained_icon_is_packaged(self):
        asset_names = {
            path.name for path in (PLUGIN / "assets").iterdir() if path.is_file()
        }
        self.assertEqual(asset_names, {"icon.png"})
        codex = load_json(PLUGIN / ".codex-plugin/plugin.json")
        self.assertEqual(codex["interface"]["composerIcon"], "./assets/icon.png")
        self.assertEqual(codex["interface"]["logo"], "./assets/icon.png")

    def test_user_docs_keep_python_optional(self):
        user_doc_paths = (
            REPO / "README.md",
            PLUGIN / "README.md",
        )
        for path in user_doc_paths:
            with self.subTest(path=path.relative_to(REPO)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("python is optional", text.lower())
                self.assertNotIn("Python 3." + "8", text)

    def test_public_readme_has_actionable_codex_install_steps(self):
        text = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "codex plugin marketplace add cyanxxy/nl-tax-agent-skills --ref main",
            text,
        )
        self.assertIn(
            "codex plugin add nl-tax-agent-skills@nl-tax-agent-skills-local",
            text,
        )
        self.assertIn("codex plugin list", text)

    def test_maintainer_docs_require_python_3_10(self):
        maintainer_doc_paths = (
            REPO / "CONTRIBUTING.md",
            REPO / "evals/nl-tax-agent-skills/README.md",
        )
        for path in maintainer_doc_paths:
            with self.subTest(path=path.relative_to(REPO)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("Python 3.10+", text)
                self.assertIn("python is optional", text.lower())
                self.assertNotIn("Python 3." + "8", text)

    def test_contributor_docs_have_no_current_0_1_2_example(self):
        text = (REPO / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertNotIn("currently `0.1." + "2`", text)
        self.assertNotIn('"version": "0.1.2"', text)

    def test_release_docs_include_future_tag_guard_without_claiming_tag(self):
        text = (REPO / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn(
            'test "$(git tag --list \'nl-tax-agent-skills--v0.1.9\')" = ""',
            text,
        )
        self.assertIn("claude plugin tag plugins/nl-tax-agent-skills", text)
        self.assertIn("git tag --list 'nl-tax-agent-skills--v0.1.9'", text)

    def test_contributor_architecture_docs_match_artifact_ownership(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        contributing = (REPO / "CONTRIBUTING.md").read_text(encoding="utf-8")

        self.assertNotIn("background helpers → workspace/shared/", readme)
        self.assertNotIn("background helper notes", contributing)
        self.assertNotIn("field-map.yaml                # nl-tax-field-mapper input", contributing)
        self.assertIn("canonical nl-tax-field-mapper output", contributing)
        self.assertIn(
            "background helpers return facts/questions without persisting files",
            contributing,
        )
        self.assertIn("field mapper alone writes canonical", contributing)


if __name__ == "__main__":
    unittest.main()
