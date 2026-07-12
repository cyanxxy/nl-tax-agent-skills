#!/usr/bin/env python3
"""Contracts for the platform-specific OpenAI submission bundle."""

import importlib.util
import pathlib
import tempfile
import unittest
import zipfile


REPO = pathlib.Path(__file__).resolve().parents[3]
BUILDER_PATH = REPO / "submission/openai/build_bundle.py"
SOURCE_PLUGIN = REPO / "plugins/nl-tax-agent-skills"


def load_builder():
    spec = importlib.util.spec_from_file_location("openai_bundle_builder", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OpenAISubmissionBundleTests(unittest.TestCase):
    def test_source_retains_exact_claude_invocation_guards(self):
        for skill_name in ("nl-tax-source-refresh", "nl-tax-submit-companion"):
            with self.subTest(skill=skill_name):
                skill = (
                    SOURCE_PLUGIN / "skills" / skill_name / "SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("disable-model-invocation: true", skill)
                policy = (
                    SOURCE_PLUGIN / "skills" / skill_name / "agents/openai.yaml"
                ).read_text(encoding="utf-8")
                self.assertIn("allow_implicit_invocation: false", policy)

    def test_builder_sanitizes_only_the_copied_openai_bundle(self):
        builder = load_builder()
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "nl-tax-agent-skills"
            zip_path = pathlib.Path(temporary) / "nl-tax-agent-skills.zip"
            built, archive, removed = builder.build_bundle(output, zip_path)

            self.assertGreater(removed, 2)
            self.assertTrue((built / ".codex-plugin/plugin.json").is_file())
            self.assertFalse((built / ".claude-plugin").exists())
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

            for skill_name in ("nl-tax-source-refresh", "nl-tax-submit-companion"):
                with self.subTest(skill=skill_name):
                    copied = (built / "skills" / skill_name / "SKILL.md").read_text(
                        encoding="utf-8"
                    )
                    source = (
                        SOURCE_PLUGIN / "skills" / skill_name / "SKILL.md"
                    ).read_text(encoding="utf-8")
                    self.assertIn("disable-model-invocation: true", source)

            with zipfile.ZipFile(archive) as bundle_zip:
                names = bundle_zip.namelist()
                self.assertTrue(
                    any(name.endswith("/.codex-plugin/plugin.json") for name in names)
                )
                self.assertFalse(any("/.claude-plugin/" in name for name in names))
