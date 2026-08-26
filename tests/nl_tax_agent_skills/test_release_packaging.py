#!/usr/bin/env python3
"""Release-package contracts for the current cross-host release."""

import json
import pathlib
import unittest

import yaml


REPO = pathlib.Path(__file__).resolve().parents[2]
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
    "nl-tax-submit-companion": "[annual|provisional] [2025|2026]",
}

PUBLIC_OPENAI_SKILLS = {
    "nl-tax-annual-return",
    "nl-tax-evidence-indexer",
    "nl-tax-field-mapper",
    "nl-tax-intake",
    "nl-tax-provisional-assessment",
    "nl-tax-submit-companion",
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
    def test_runtime_plugin_excludes_repository_tests(self):
        self.assertFalse((PLUGIN / "tests").exists())

    def test_runtime_plugin_excludes_source_maintenance_and_eval_fixtures(self):
        self.assertFalse((SKILLS / "nl-tax-source-refresh").exists())
        self.assertFalse((SKILLS / "_shared/eval-fixtures").exists())
        self.assertFalse((SKILLS / "_shared/supported-workflows.yaml").exists())
        self.assertTrue(
            (
                REPO
                / "tools/nl_tax_agent_skills/source_maintenance/supported-workflows.yaml"
            ).is_file()
        )

    def test_runtime_plugin_excludes_maintainer_source_notes(self):
        knowledge = SKILLS / "_shared/knowledge"
        self.assertEqual(list(knowledge.glob("**/_snapshot-metadata.yaml")), [])
        for directory in ("platform", "compat"):
            with self.subTest(directory=directory):
                self.assertFalse((knowledge / directory).exists())
        self.assertFalse((knowledge / "methods/regelspraak.md").exists())

        maintainer_notes = REPO / "docs/maintainers/source-notes"
        self.assertTrue((maintainer_notes / "platform/agent-host-capabilities.md").is_file())
        self.assertTrue((maintainer_notes / "platform/claude-skills.md").is_file())
        self.assertTrue((maintainer_notes / "compat/odb-service-developers.md").is_file())
        self.assertTrue((maintainer_notes / "methodology/regelspraak.md").is_file())
        metadata = REPO / "tools/nl_tax_agent_skills/source_maintenance/metadata"
        self.assertEqual(len(list(metadata.glob("**/_snapshot-metadata.yaml"))), 10)

        runtime_registry = "\n".join(
            (
                (SKILLS / "_shared/source-register.yaml").read_text(encoding="utf-8"),
                (
                    REPO
                    / "tools/nl_tax_agent_skills/source_maintenance/supported-workflows.yaml"
                ).read_text(encoding="utf-8"),
            )
        )
        for source_id in (
            "openai_codex_subagents",
            "claude_plugins_cowork",
            "odb_service_developers",
            "regels_overheid_regelspraak",
        ):
            with self.subTest(source_id=source_id):
                self.assertNotIn(source_id, runtime_registry)

    def test_no_legacy_commands(self):
        self.assertFalse((PLUGIN / "commands").exists())

    def test_exactly_11_runtime_skills_plus_hidden_shared_resources(self):
        paths = list(SKILLS.glob("*/SKILL.md"))
        names = [frontmatter(path)["name"] for path in paths]
        workflow_names = [
            frontmatter(path)["name"] for path in paths if path.parent.name != "_shared"
        ]
        self.assertEqual(len(workflow_names), 11)
        self.assertEqual(len(names), 12)
        self.assertEqual(len(set(names)), 12)
        shared = frontmatter(SKILLS / "_shared/SKILL.md")
        self.assertFalse(shared["user-invocable"])
        self.assertTrue(shared["disable-model-invocation"])

    def test_six_public_skills_have_exact_argument_hints(self):
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
        self.assertEqual(claude["version"], "0.2.0")
        self.assertEqual(codex["version"], "0.2.0")
        self.assertEqual(claude["displayName"], "NL Tax Agent Skills")
        self.assertEqual(claude["homepage"], REPOSITORY_URL)
        self.assertEqual(claude["repository"], REPOSITORY_URL)
        self.assertEqual(codex["homepage"], REPOSITORY_URL + "#readme")
        self.assertEqual(codex["repository"], REPOSITORY_URL)
        self.assertIn("Conversational, source-traceable", claude["description"])
        self.assertEqual(claude["description"], codex["description"])
        self.assertIn("Claude Cowork", codex["interface"]["longDescription"])
        self.assertIn("ChatGPT Work", codex["interface"]["longDescription"])
        self.assertIn("Conversational", codex["interface"]["shortDescription"])
        self.assertNotIn("Step-by-step", codex["interface"]["shortDescription"])
        self.assertEqual(len(codex["interface"]["defaultPrompt"]), 3)

    def test_claude_package_has_one_specialist_reviewer_agent(self):
        claude = load_json(PLUGIN / ".claude-plugin/plugin.json")
        # Claude auto-discovers the default plugin-root agents/ directory. Its
        # manifest `agents` field is for custom agent file paths; pointing it
        # at the default directory is rejected by the current strict validator.
        self.assertNotIn("agents", claude)
        agent_paths = sorted((PLUGIN / "agents").glob("*.md"))
        self.assertEqual(
            [path.name for path in agent_paths],
            ["nl-tax-specialist-reviewer.md"],
        )
        metadata = frontmatter(agent_paths[0])
        self.assertEqual(metadata["name"], "nl-tax-specialist-reviewer")
        self.assertEqual(metadata["model"], "inherit")
        self.assertEqual(metadata["effort"], "high")
        self.assertEqual(metadata["maxTurns"], 12)
        self.assertEqual(
            {tool.strip() for tool in metadata["tools"].split(",")},
            {"Read", "Grep", "Glob", "WebSearch", "WebFetch"},
        )
        self.assertNotIn("disallowedTools", metadata)
        body = agent_paths[0].read_text(encoding="utf-8")
        self.assertIn("official sources", body)
        self.assertIn("outside the frontmatter\nallowlist", body)
        self.assertIn("Do not use Bash, Write, Edit, Agent", body)
        self.assertIn("connectors, MCP tools", body)
        self.assertIn("return that request to the owner", body)
        self.assertNotIn("run the plugin's optional mechanical validators", body)
        self.assertIn("Do not decide final readiness", body)
        self.assertIn("Do not write or mutate any file", body)

    def test_public_box3_copy_preserves_the_non_election_boundary(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        examples = (
            SKILLS / "_shared/knowledge/years/2025/box3/examples.md"
        ).read_text(encoding="utf-8")

        self.assertIn("informational comparison", readme)
        self.assertIn("not a tax-method election", readme)
        self.assertIn("uses the more favorable amount", readme)
        self.assertNotIn("comparison for the user to choose from", readme)
        self.assertIn("recommendation note", examples)
        runtime = (SKILLS / "_shared/runtime-contract.md").read_text(encoding="utf-8")
        self.assertIn("legacy “recommendation note” shorthand", runtime)
        self.assertIn("does not create a taxpayer method election", runtime)
        self.assertIn("Preserve\nthe reviewed source note byte-for-byte", runtime)

    def test_every_skill_loads_the_cross_runtime_contract(self):
        contract = SKILLS / "_shared/runtime-contract.md"
        self.assertTrue(contract.is_file())
        contract_text = contract.read_text(encoding="utf-8")
        for required in (
            "ChatGPT Work on web or mobile",
            "ChatGPT Work or Codex on desktop",
            "Python and shell access are accelerators only",
            "Never depend on a vendor-specific environment variable",
            "The owning conversational agent remains the only writer",
            "the user may ask for deadline reminders",
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
                self.assertNotIn("$nl-tax-", interface["default_prompt"])
                self.assertNotIn("/nl-tax-", interface["default_prompt"])
                self.assertTrue(metadata["policy"]["allow_implicit_invocation"])
                icon_values = [
                    interface.get(icon_key)
                    for icon_key in ("icon_small", "icon_large")
                ]
                self.assertEqual(bool(icon_values[0]), bool(icon_values[1]))
                for icon_value in filter(None, icon_values):
                    icon_path = (path.parent.parent / icon_value).resolve()
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
            'test "$(git tag --list \'nl-tax-agent-skills--v0.2.0\')" = ""',
            text,
        )
        self.assertIn("claude plugin tag plugins/nl-tax-agent-skills", text)
        self.assertIn("git tag --list 'nl-tax-agent-skills--v0.2.0'", text)

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
