#!/usr/bin/env python3
"""Release-package contracts for the current Cowork-first release."""

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

    def test_exactly_12_unique_skills(self):
        names = [frontmatter(path)["name"] for path in SKILLS.glob("*/SKILL.md")]
        self.assertEqual(len(names), 12)
        self.assertEqual(len(set(names)), 12)

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
        self.assertEqual(claude["version"], "0.1.8")
        self.assertEqual(codex["version"], "0.1.8")
        self.assertEqual(claude["displayName"], "NL Tax Agent Skills")
        self.assertEqual(claude["homepage"], REPOSITORY_URL)
        self.assertEqual(claude["repository"], REPOSITORY_URL)

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
            'test "$(git tag --list \'nl-tax-agent-skills--v0.1.8\')" = ""',
            text,
        )
        self.assertIn("claude plugin tag plugins/nl-tax-agent-skills", text)
        self.assertIn("git tag --list 'nl-tax-agent-skills--v0.1.8'", text)

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
