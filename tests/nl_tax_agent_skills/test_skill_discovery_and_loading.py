#!/usr/bin/env python3
"""Cowork intent discovery and progressive-loading contracts."""

import pathlib
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


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    _, block, _ = text.split("---", 2)
    return yaml.safe_load(block)


class SkillDiscoveryAndLoadingTests(unittest.TestCase):
    def test_only_conversation_owners_allow_native_structured_questions(self):
        owners = (
            "nl-tax-intake",
            "nl-tax-annual-return",
            "nl-tax-provisional-assessment",
            "nl-tax-field-mapper",
        )
        helpers = (
            "nl-tax-partner-deductions",
            "nl-tax-box1-home",
            "nl-tax-box2",
            "nl-tax-box3",
            "nl-tax-winst",
        )
        for skill_name in owners:
            with self.subTest(skill=skill_name):
                tools = frontmatter(SKILLS / skill_name / "SKILL.md")[
                    "allowed-tools"
                ]
                self.assertIn("AskUserQuestion", tools)
        for skill_name in helpers:
            with self.subTest(skill=skill_name):
                tools = frontmatter(SKILLS / skill_name / "SKILL.md")[
                    "allowed-tools"
                ]
                self.assertNotIn("AskUserQuestion", tools)

    def test_all_skill_descriptions_fit_claude_metadata_limit(self):
        for path in SKILLS.glob("*/SKILL.md"):
            description = frontmatter(path)["description"]
            with self.subTest(skill=path.parent.name):
                self.assertLessEqual(len(description), 200)

    def test_public_triggers_require_preparation_intent(self):
        intake = frontmatter(SKILLS / "nl-tax-intake/SKILL.md")[
            "description"
        ].lower()
        self.assertIn("explicitly wants", intake)
        self.assertIn("informational", intake)
        self.assertNotIn("mentions belastingaangifte", intake)
        # 0.4 (R10): documents are read inside the owning workflow; there is no
        # separate document-indexing entry point any more.
        self.assertFalse((SKILLS / "nl-tax-evidence-indexer").exists())

    def test_informational_questions_use_notes_without_creating_state(self):
        intake = read_skill("nl-tax-intake").lower()
        informational = intake.split(
            "## informational fast path", 1
        )[1].split("## user-facing boundary", 1)[0]
        for required in (
            "do not create or update",
            "source-register.yaml",
            "nl-tax-shared-resources/knowledge/",
            "not model memory",
            "do not read the complete register",
            "do not ask screening questions",
        ):
            self.assertIn(required, informational)
        self.assertLess(
            informational.index("nl-tax-shared-resources/knowledge/"),
            informational.index("source-register.yaml"),
        )

    def test_other_public_descriptions_use_explicit_user_intent(self):
        for skill_name in (
            "nl-tax-annual-return",
            "nl-tax-provisional-assessment",
            "nl-tax-field-mapper",
            "nl-tax-submit-companion",
        ):
            with self.subTest(skill=skill_name):
                description = frontmatter(SKILLS / skill_name / "SKILL.md")[
                    "description"
                ].lower()
                self.assertIn("explicitly", description)

    def test_submit_companion_uses_natural_language_activation(self):
        skill_path = SKILLS / "nl-tax-submit-companion/SKILL.md"
        metadata = frontmatter(skill_path)
        body = " ".join(
            skill_path.read_text(encoding="utf-8").lower().split()
        )
        openai = yaml.safe_load(
            (SKILLS / "nl-tax-submit-companion/agents/openai.yaml").read_text(
                encoding="utf-8"
            )
        )

        self.assertNotEqual(metadata.get("disable-model-invocation"), True)
        self.assertLessEqual(len(metadata["description"]), 200)
        self.assertIn("natural language", metadata["description"].lower())
        self.assertIn("checklist", metadata["description"].lower())
        self.assertIn("immediate checklist offer", metadata["description"].lower())
        self.assertIn("affirmative reply", body)
        self.assertIn("never require a slash command or magic phrase", body)
        self.assertIn("do not run merely because a field map exists", body)
        self.assertIn("not expected for `provisional_2026_review`", body)
        self.assertIn("or `provisional_2026_stopzetten`", body)
        self.assertIn("never report a missing field map as a blocker", body)
        self.assertIn("field-map rows only for annual", body)
        self.assertTrue(openai["policy"]["allow_implicit_invocation"])
        prompt = openai["interface"]["default_prompt"].lower()
        self.assertNotIn("$nl-tax-", prompt)
        self.assertNotIn("/nl-tax-", prompt)
        self.assertIn("any applicable field map", prompt)

    def test_large_output_files_load_only_at_consent_or_generation(self):
        annual = " ".join(read_skill("nl-tax-annual-return").lower().split())
        self.assertIn(
            "do not load `reference/annual-output-contract.md` during collection",
            annual,
        )
        self.assertIn(
            "phase 10 loads it, with the template, only after its generation gate opens",
            annual,
        )
        self.assertIn("on consent, load `templates/annual-workpack.md`", annual)

        provisional = " ".join(
            read_skill("nl-tax-provisional-assessment").lower().split()
        )
        self.assertIn(
            "load `templates/provisional-workpack.md` when the user consents to "
            "saving or at the generation gate, whichever comes first",
            provisional,
        )
        self.assertIn(
            "load `reference/provisional-output-contract.md` at final review",
            provisional,
        )
        for text in (annual, provisional):
            for retired in ("annual-return-pack.md", "provisional-pack.md"):
                self.assertNotIn(retired, text)

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

        # Provisional request/change hand off to the mapper by name; the mapper
        # entry surface names every bundled resource it loads, so nothing has
        # to enumerate the package.
        for name in ("request.md", "change.md"):
            subflow = (
                SKILLS / f"nl-tax-provisional-assessment/reference/subflows/{name}"
            ).read_text(encoding="utf-8")
            with self.subTest(subflow=name):
                self.assertIn("continue with `nl-tax-field-mapper`", subflow)
        mapper = read_skill("nl-tax-field-mapper")
        for path in MAPPER_PATHS:
            local = path.split("/", 1)[1]
            with self.subTest(mapper_resource=local):
                self.assertIn(local, mapper)
                self.assertTrue((SKILLS / path).is_file())


if __name__ == "__main__":
    unittest.main()
