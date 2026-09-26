#!/usr/bin/env python3
"""Contracts for the platform-specific OpenAI submission bundle (0.4)."""

import importlib.util
import pathlib
import shutil
import tempfile
import unittest
import zipfile

import yaml


REPO = pathlib.Path(__file__).resolve().parents[2]
BUILDER_PATH = REPO / "submission/openai/build_bundle.py"
TEST_CASES_PATH = REPO / "submission/openai/test-cases.yaml"
SOURCE_PLUGIN = REPO / "plugins/nl-tax-agent-skills"
RETIRED_SKILL = "nl-tax-evidence-indexer"
PUBLIC_SKILLS = {
    "nl-tax-annual-return",
    "nl-tax-field-mapper",
    "nl-tax-intake",
    "nl-tax-knowledge",
    "nl-tax-provisional-assessment",
    "nl-tax-submit-companion",
}
LEGACY_OUTPUTS = (
    "workspace/taxpayer",
    "workspace/shared",
    "workspace/annual",
    "workspace/provisional",
    "evidence-index",
    "field-map.yaml",
    "field-map-open-questions",
    "missing-info.md",
    "delta-summary.md",
    "return-pack.md",
    "provisional-pack.md",
)


def load_builder():
    spec = importlib.util.spec_from_file_location("openai_bundle_builder", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OpenAISubmissionBundleTests(unittest.TestCase):
    def test_source_allows_natural_language_checklist_invocation(self):
        for skill_name in ("nl-tax-submit-companion",):
            with self.subTest(skill=skill_name):
                skill = (
                    SOURCE_PLUGIN / "skills" / skill_name / "SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertNotIn("disable-model-invocation: true", skill)
                self.assertIn("natural language", skill.lower())
                policy = (
                    SOURCE_PLUGIN / "skills" / skill_name / "agents/openai.yaml"
                ).read_text(encoding="utf-8")
                self.assertIn("allow_implicit_invocation: true", policy)

    def test_builder_sanitizes_only_the_copied_openai_bundle(self):
        builder = load_builder()
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "nl-tax-agent-skills"
            zip_path = pathlib.Path(temporary) / "nl-tax-agent-skills.zip"
            built, archive, removed = builder.build_bundle(output, zip_path)

            self.assertGreater(removed, 2)
            self.assertTrue((built / ".codex-plugin/plugin.json").is_file())
            self.assertFalse((built / ".claude-plugin").exists())
            self.assertFalse((built / "agents").exists())
            self.assertFalse((built / "tests").exists())
            self.assertTrue(archive.is_file())

            claude_only_keys = (
                "allowed-tools",
                "argument-hint",
                "disable-model-invocation",
                "disable_model_invocation",
                "user-invocable",
            )
            for skill_path in built.glob("skills/*/SKILL.md"):
                copied_frontmatter = skill_path.read_text(encoding="utf-8").split(
                    "---", 2
                )[1]
                with self.subTest(skill=skill_path.parent.name):
                    for key in claude_only_keys:
                        self.assertNotIn(f"{key}:", copied_frontmatter)

            for skill_name in ("nl-tax-submit-companion",):
                with self.subTest(skill=skill_name):
                    copied = (built / "skills" / skill_name / "SKILL.md").read_text(
                        encoding="utf-8"
                    )
                    source = (
                        SOURCE_PLUGIN / "skills" / skill_name / "SKILL.md"
                    ).read_text(encoding="utf-8")
                    self.assertNotIn("disable-model-invocation: true", source)
                    self.assertIn("natural language", copied.lower())
                    copied_policy = (
                        built / "skills" / skill_name / "agents/openai.yaml"
                    ).read_text(encoding="utf-8")
                    self.assertIn("allow_implicit_invocation: true", copied_policy)

            with zipfile.ZipFile(archive) as bundle_zip:
                names = bundle_zip.namelist()
                self.assertTrue(
                    any(name.endswith("/.codex-plugin/plugin.json") for name in names)
                )
                self.assertFalse(any("/.claude-plugin/" in name for name in names))
                self.assertFalse(any(RETIRED_SKILL in name for name in names))
                self.assertFalse(any(name.endswith(".py") for name in names))

    def test_bundle_ships_the_0_4_workpack_templates_only(self):
        builder = load_builder()
        with tempfile.TemporaryDirectory() as temporary:
            built, _, _ = builder.build_bundle(
                pathlib.Path(temporary) / "nl-tax-agent-skills",
                pathlib.Path(temporary) / "bundle.zip",
            )
            self.assertFalse((built / "skills" / RETIRED_SKILL).exists())
            self.assertTrue(
                (built / "skills/nl-tax-annual-return/templates/annual-workpack.md").is_file()
            )
            self.assertTrue(
                (built / "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md").is_file()
            )
            for retired in (
                "skills/nl-tax-annual-return/templates/annual-return-pack.md",
                "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
                "skills/nl-tax-provisional-assessment/templates/delta-summary.md",
                "skills/nl-tax-intake/templates/taxpayer-profile.yaml",
                "skills/nl-tax-shared-resources/templates/session-progress.yaml",
                "skills/nl-tax-submit-companion/templates/manual-submission-checklist.md",
            ):
                with self.subTest(retired=retired):
                    self.assertFalse((built / retired).exists())
            policies = {
                path.parent.parent.name
                for path in built.glob("skills/*/agents/openai.yaml")
                if yaml.safe_load(path.read_text(encoding="utf-8"))["policy"][
                    "allow_implicit_invocation"
                ]
            }
            self.assertEqual(policies, PUBLIC_SKILLS)

    def test_builder_refuses_a_retired_or_incomplete_skill_directory(self):
        builder = load_builder()
        with tempfile.TemporaryDirectory() as temporary:
            skills = pathlib.Path(temporary) / "skills"
            shutil.copytree(SOURCE_PLUGIN / "skills" / "nl-tax-knowledge", skills / "nl-tax-knowledge")
            builder._assert_shippable_skills(skills)
            (skills / RETIRED_SKILL / "reference").mkdir(parents=True)
            (skills / RETIRED_SKILL / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "retired skill"):
                builder._assert_shippable_skills(skills)
            shutil.rmtree(skills / RETIRED_SKILL)
            (skills / "nl-tax-empty").mkdir()
            with self.assertRaisesRegex(ValueError, "without SKILL.md"):
                builder._assert_shippable_skills(skills)


class OpenAIReviewerCasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = yaml.safe_load(TEST_CASES_PATH.read_text(encoding="utf-8"))

    def test_case_counts_and_ids(self):
        positive, negative = self.cases["positive"], self.cases["negative"]
        self.assertEqual(len(positive), 5)
        self.assertEqual(len(negative), 3)
        self.assertEqual(len({case["id"] for case in positive + negative}), 8)
        self.assertNotIn("evidence_index_mixed_sources", {case["id"] for case in positive})

    def test_expected_skills_are_shipped_public_skills(self):
        for case in self.cases["positive"]:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["expected_skills"])
                for skill in case["expected_skills"]:
                    self.assertIn(skill, PUBLIC_SKILLS)
                    self.assertTrue((SOURCE_PLUGIN / "skills" / skill / "SKILL.md").is_file())
                self.assertTrue((REPO / case["fixture"]).is_file(), case["fixture"])

    def test_expected_results_follow_the_0_4_file_rules(self):
        rendered = yaml.safe_dump(self.cases)
        self.assertNotIn(RETIRED_SKILL, rendered)
        for legacy in LEGACY_OUTPUTS:
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, rendered)
        for case in self.cases["positive"]:
            text = " ".join(case["expected_result"]) + " " + " ".join(case["expected_behavior"])
            with self.subTest(case=case["id"]):
                for path in (
                    "workspace/nl-tax-annual-2025-workpack.md",
                    "workspace/nl-tax-provisional-2026-workpack.md",
                ):
                    if path in text:
                        self.assertIn("consent", text.lower())
        informational = next(
            case for case in self.cases["positive"] if case["id"] == "informational_supported_rule"
        )
        self.assertEqual(informational["expected_skills"], ["nl-tax-knowledge"])
        self.assertIn("no files written", " ".join(informational["expected_result"]))


if __name__ == "__main__":
    unittest.main()
