#!/usr/bin/env python3
"""Cowork intent discovery and progressive-loading contracts."""

import pathlib
import unittest

import yaml


PLUGIN = pathlib.Path(__file__).resolve().parents[1]
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
    "nl-tax-field-mapper/scripts/validate_field_map.py",
)


def read_skill(skill_name):
    return (SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    _, block, _ = text.split("---", 2)
    return yaml.safe_load(block)


class SkillDiscoveryAndLoadingTests(unittest.TestCase):
    def test_all_skill_descriptions_fit_claude_metadata_limit(self):
        for path in SKILLS.glob("*/SKILL.md"):
            description = frontmatter(path)["description"]
            with self.subTest(skill=path.parent.name):
                self.assertLessEqual(len(description), 200)

    def test_public_triggers_require_preparation_intent(self):
        intake = frontmatter(SKILLS / "nl-tax-intake/SKILL.md")[
            "description"
        ].lower()
        evidence = frontmatter(SKILLS / "nl-tax-evidence-indexer/SKILL.md")[
            "description"
        ].lower()
        self.assertIn("explicitly wants", intake)
        self.assertIn("informational", intake)
        self.assertIn("explicitly wants", evidence)
        self.assertTrue("index" in evidence or "organiz" in evidence)
        self.assertNotIn("mentions belastingaangifte", intake)
        self.assertNotIn("mentions tax documents", evidence)

    def test_informational_questions_use_notes_without_creating_state(self):
        intake = read_skill("nl-tax-intake").lower()
        informational = intake.split(
            "## informational fast path", 1
        )[1].split("## user-facing boundary", 1)[0]
        for required in (
            "do not create or update",
            "source-register.yaml",
            "_shared/knowledge/",
            "not model memory",
            "do not read the complete register",
            "do not ask screening questions",
        ):
            self.assertIn(required, informational)
        self.assertLess(
            informational.index("_shared/knowledge/"),
            informational.index("source-register.yaml"),
        )

    def test_other_public_descriptions_use_explicit_user_intent(self):
        for skill_name in (
            "nl-tax-annual-return",
            "nl-tax-provisional-assessment",
            "nl-tax-field-mapper",
            "nl-tax-source-refresh",
            "nl-tax-submit-companion",
        ):
            with self.subTest(skill=skill_name):
                description = frontmatter(SKILLS / skill_name / "SKILL.md")[
                    "description"
                ].lower()
                self.assertIn("explicitly", description)

    def test_large_output_files_load_only_at_generation(self):
        for skill_name, template in (
            ("nl-tax-annual-return", "annual-return-pack.md"),
            ("nl-tax-provisional-assessment", "provisional-pack.md"),
        ):
            text = read_skill(skill_name).lower()
            self.assertIn(f"load `{template}` only after", text)

    def test_annual_phases_exist_and_are_linked_from_the_entry_surface(self):
        skill = read_skill("nl-tax-annual-return")
        index = (
            SKILLS / "nl-tax-annual-return/reference/annual-flow.md"
        ).read_text(encoding="utf-8")
        phases_dir = SKILLS / "nl-tax-annual-return/reference/phases"
        self.assertEqual(
            {path.name for path in phases_dir.glob("*.md")}, set(ANNUAL_PHASES)
        )
        positions = []
        for filename in ANNUAL_PHASES:
            with self.subTest(phase=filename):
                reference = f"reference/phases/{filename}"
                self.assertIn(reference, skill)
                index_reference = f"phases/{filename}"
                self.assertIn(index_reference, index)
                positions.append(index.index(index_reference))
        self.assertEqual(positions, sorted(positions))

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
        self.assertIn("exactly one", (skill + index).lower())

    def test_workflow_skills_use_explicit_sibling_mapper_paths(self):
        annual = read_skill("nl-tax-annual-return")
        provisional = read_skill("nl-tax-provisional-assessment")
        shared_paths = (
            MAPPER_PATHS[0],
            MAPPER_PATHS[1],
            MAPPER_PATHS[4],
        )
        for skill_name, text in (("annual", annual), ("provisional", provisional)):
            for path in shared_paths:
                with self.subTest(skill=skill_name, path=path):
                    self.assertIn(path, text)
        self.assertIn(MAPPER_PATHS[2], annual)
        self.assertIn(MAPPER_PATHS[3], provisional)


if __name__ == "__main__":
    unittest.main()
