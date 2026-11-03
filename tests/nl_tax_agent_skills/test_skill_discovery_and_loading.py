#!/usr/bin/env python3
"""Cowork intent discovery and progressive-loading contracts."""

import importlib.util
import pathlib
import re
import unittest

import yaml


PLUGIN = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)
SKILLS = PLUGIN / "skills"

ANNUAL_PHASES = (
    "01-preflight.md",
    "01-5-filing-status.md",
    "02-income.md",
    "02a-winst.md",
    "03-own-home.md",
    "03a-box2.md",
    "04-box3.md",
    "05-deductions.md",
    "05-5-credits.md",
    "06-partner.md",
    "07-field-map.md",
    "08-missing-info.md",
    "09-review-questions.md",
    "10-assembly.md",
)
PROVISIONAL_SUBFLOWS = ("request.md", "change.md", "review.md", "stopzetten.md")
MAPPER_PATHS = (
    "nl-tax-field-mapper/templates/field-map-template.yaml",
    "nl-tax-field-mapper/reference/mapping-principles.md",
    "nl-tax-field-mapper/reference/annual-field-map.md",
    "nl-tax-field-mapper/reference/provisional-field-map.md",
    "nl-tax-field-mapper/reference/field-map-rules.yaml",
)


def read_skill(skill_name):
    return (SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8")


_frontmatter_spec = importlib.util.spec_from_file_location(
    "skill_frontmatter", pathlib.Path(__file__).with_name("skill_frontmatter.py")
)
_frontmatter_helpers = importlib.util.module_from_spec(_frontmatter_spec)
_frontmatter_spec.loader.exec_module(_frontmatter_helpers)
split_allowed_tools = _frontmatter_helpers.split_allowed_tools


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    _, block, _ = text.split("---", 2)
    return split_allowed_tools(yaml.safe_load(block))


def all_skill_frontmatter():
    return {
        path.parent.name: frontmatter(path) for path in SKILLS.glob("*/SKILL.md")
    }


def public_skills():
    """Every user-invocable skill (no `user-invocable: false`)."""
    return {
        name
        for name, metadata in all_skill_frontmatter().items()
        if metadata.get("user-invocable", True) is not False
    }


def conversation_owner_skills():
    """Workspace writers that hold the conversation, plus intake.

    The submit companion writes only its checklist section from an existing
    workpack and asks no structured questions, so it is not a conversation
    owner here.
    """
    owners = {
        name
        for name, metadata in all_skill_frontmatter().items()
        if "Edit(./workspace/**)" in (metadata.get("allowed-tools") or [])
    }
    return (owners | {"nl-tax-intake"}) - {"nl-tax-submit-companion"}


def background_helper_skills():
    """Every non-user-invocable skill except the hidden resource bundle."""
    return {
        name
        for name, metadata in all_skill_frontmatter().items()
        if metadata.get("user-invocable") is False
    } - {"nl-tax-shared-resources"}


class SkillDiscoveryAndLoadingTests(unittest.TestCase):
    def test_only_conversation_owners_allow_native_structured_questions(self):
        owners = conversation_owner_skills()
        helpers = background_helper_skills()
        # Derived sets must keep covering the original and the extended skills.
        self.assertTrue(
            {
                "nl-tax-intake",
                "nl-tax-annual-return",
                "nl-tax-provisional-assessment",
                "nl-tax-field-mapper",
                "nl-tax-vat-return",
                "nl-tax-vat-correction",
                "nl-tax-icp",
                "nl-tax-oss",
                "nl-tax-international-return",
                "nl-tax-annual-return-2026",
            }
            <= owners
        )
        self.assertTrue(
            {
                "nl-tax-partner-deductions",
                "nl-tax-box1-home",
                "nl-tax-box2",
                "nl-tax-box3",
                "nl-tax-winst",
                "nl-tax-vat-adjustments",
            }
            <= helpers
        )
        self.assertFalse(owners & helpers)
        for skill_name in sorted(owners):
            with self.subTest(skill=skill_name):
                tools = frontmatter(SKILLS / skill_name / "SKILL.md")[
                    "allowed-tools"
                ]
                self.assertIn("AskUserQuestion", tools)
        for skill_name in sorted(helpers):
            with self.subTest(skill=skill_name):
                tools = frontmatter(SKILLS / skill_name / "SKILL.md").get(
                    "allowed-tools", []
                )
                self.assertNotIn("AskUserQuestion", tools)
                # Helpers write nothing, so they never pre-approve any edit.
                self.assertFalse(
                    [tool for tool in tools if str(tool).startswith(("Edit", "Write"))]
                )

    def test_public_triggers_require_preparation_intent(self):
        # 0.4 (R10): documents are read inside the owning workflow; there is no
        # separate document-indexing entry point any more.
        self.assertFalse((SKILLS / "nl-tax-evidence-indexer").exists())

    def test_other_public_descriptions_use_explicit_user_intent(self):
        public = public_skills() - {"nl-tax-intake", "nl-tax-knowledge"}
        self.assertTrue(
            {
                "nl-tax-annual-return",
                "nl-tax-provisional-assessment",
                "nl-tax-field-mapper",
                "nl-tax-submit-companion",
                "nl-tax-vat-return",
                "nl-tax-vat-correction",
                "nl-tax-icp",
                "nl-tax-oss",
                "nl-tax-international-return",
                "nl-tax-annual-return-2026",
            }
            <= public
        )
        # Each preparation workflow triggers on a request to prepare, map, or
        # check off a workpack, and sends a question about how a rule works to
        # the knowledge skill, so a casual question starts no workflow.
        for name in sorted(public):
            description = all_skill_frontmatter()[name]["description"]
            with self.subTest(skill=name):
                self.assertIn("Use when", description)
                self.assertIn("nl-tax-knowledge", description)
                self.assertNotIn("explicitly", description)

    def test_helper_descriptions_require_an_active_owner(self):
        for name in sorted(background_helper_skills()):
            description = all_skill_frontmatter()[name]["description"]
            body = read_skill(name)
            with self.subTest(skill=name):
                self.assertIn("Use only when an active", description)
                self.assertIn("**Only inside an owning workflow.**", body)

    def test_allowed_tools_tokens_are_permission_rules(self):
        # Malformed tokens such as "Edit(" or "Read," would still be a string,
        # so check each space-separated token against the rule grammar.
        token = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\([^\s()]+\))?$")
        for path in SKILLS.glob("*/SKILL.md"):
            tools = frontmatter(path).get("allowed-tools") or []
            with self.subTest(skill=path.parent.name):
                for tool in tools:
                    self.assertRegex(tool, token)

    def test_allowed_tools_use_the_spec_space_separated_string(self):
        # agentskills.io defines `allowed-tools` as one space-separated string.
        for path in SKILLS.glob("*/SKILL.md"):
            _, block, _ = path.read_text(encoding="utf-8").split("---", 2)
            raw = yaml.safe_load(block).get("allowed-tools")
            if raw is None:
                continue
            with self.subTest(skill=path.parent.name):
                self.assertIsInstance(raw, str)
                self.assertTrue(raw.split())

    def test_submit_companion_uses_natural_language_activation(self):
        skill_path = SKILLS / "nl-tax-submit-companion/SKILL.md"
        metadata = frontmatter(skill_path)
        openai = yaml.safe_load(
            (SKILLS / "nl-tax-submit-companion/agents/openai.yaml").read_text(
                encoding="utf-8"
            )
        )

        self.assertNotEqual(metadata.get("disable-model-invocation"), True)
        self.assertTrue(openai["policy"]["allow_implicit_invocation"])

    def test_annual_phases_exist_and_are_linked_from_the_entry_surface(self):
        skill = read_skill("nl-tax-annual-return")
        index = (
            SKILLS / "nl-tax-annual-return/reference/annual-flow.md"
        ).read_text(encoding="utf-8")
        phases_dir = SKILLS / "nl-tax-annual-return/reference/phases"
        self.assertEqual(
            {path.name for path in phases_dir.glob("*.md")}, set(ANNUAL_PHASES)
        )
        for filename in ANNUAL_PHASES:
            with self.subTest(phase=filename):
                reference = f"reference/phases/{filename}"
                self.assertIn(reference, skill)
                index_reference = f"phases/{filename}"
                self.assertIn(index_reference, index)

    def test_provisional_subflows_exist_and_are_directly_selectable(self):
        skill = read_skill("nl-tax-provisional-assessment")
        index = (
            SKILLS
            / "nl-tax-provisional-assessment/reference/provisional-flow.md"
        ).read_text(encoding="utf-8")
        subflows_dir = SKILLS / "nl-tax-provisional-assessment/reference/subflows"
        self.assertEqual(
            {path.name for path in subflows_dir.glob("*.md")},
            set(PROVISIONAL_SUBFLOWS),
        )
        for filename in PROVISIONAL_SUBFLOWS:
            with self.subTest(subflow=filename):
                reference = f"reference/subflows/{filename}"
                self.assertIn(reference, skill)
                self.assertIn(f"subflows/{filename}", index)

    def test_workflow_skills_use_explicit_sibling_mapper_paths(self):
        annual_entry = read_skill("nl-tax-annual-return")
        provisional_entry = read_skill("nl-tax-provisional-assessment")
        annual = (
            SKILLS
            / "nl-tax-annual-return/reference/phases/10-assembly.md"
        ).read_text(encoding="utf-8")
        shared_paths = (
            MAPPER_PATHS[0],
            MAPPER_PATHS[1],
            MAPPER_PATHS[4],
        )
        for path in shared_paths + (MAPPER_PATHS[2],):
            with self.subTest(skill="annual", path=path):
                self.assertIn(path, annual)
        self.assertIn("reference/phases/10-assembly.md", annual_entry)
        self.assertIn("reference/subflows/request.md", provisional_entry)
        self.assertIn("reference/subflows/change.md", provisional_entry)

        # The mapper entry surface names every bundled resource it loads, so
        # nothing has to enumerate the package.
        mapper = read_skill("nl-tax-field-mapper")
        for path in MAPPER_PATHS:
            local = path.split("/", 1)[1]
            with self.subTest(mapper_resource=local):
                self.assertIn(local, mapper)
                self.assertTrue((SKILLS / path).is_file())


if __name__ == "__main__":
    unittest.main()
