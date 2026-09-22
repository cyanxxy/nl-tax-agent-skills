#!/usr/bin/env python3
"""Knowledge-base access contracts for agents that read skills on demand."""

import pathlib
import re
import unittest

import yaml


REPO = pathlib.Path(__file__).resolve().parents[2]
SKILLS = REPO / "plugins" / "nl-tax-agent-skills" / "skills"
SHARED = SKILLS / "nl-tax-shared-resources"
KNOWLEDGE = SHARED / "knowledge"
INDEX = SHARED / "knowledge-index.md"
HELPERS = (
    "nl-tax-box1-home",
    "nl-tax-box2",
    "nl-tax-box3",
    "nl-tax-winst",
    "nl-tax-partner-deductions",
)
INDEX_ROW = re.compile(r"^\| (.+?) \| (.+?) \| `(\.\./[^`]+)` \|$")


def frontmatter(path):
    _, block, _ = path.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(block)


def index_rows():
    rows = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        match = INDEX_ROW.match(line)
        if match and match.group(1) != "Topic":
            rows.append(match.groups())
    return rows


def skill_documents():
    for skill in sorted(SKILLS.iterdir()):
        if not (skill / "SKILL.md").is_file():
            continue
        yield skill / "SKILL.md"
        yield from sorted((skill / "reference").glob("**/*.md"))


class KnowledgeBaseAccessTests(unittest.TestCase):
    def test_every_skill_folder_matches_its_skill_name(self):
        for path in SKILLS.glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                name = frontmatter(path)["name"]
                self.assertEqual(name, path.parent.name)
                self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_index_links_every_knowledge_note_and_every_link_resolves(self):
        linked = set()
        for _, _, relative in index_rows():
            target = (SKILLS / "nl-tax-knowledge" / relative).resolve()
            with self.subTest(path=relative):
                self.assertTrue(target.is_file())
            linked.add(target)
        index_text = INDEX.read_text(encoding="utf-8")
        for note in KNOWLEDGE.glob("**/*.md"):
            relative = note.relative_to(KNOWLEDGE).as_posix()
            with self.subTest(note=relative):
                if note.name in {"request-flow.md", "change-flow.md", "stopzetten-flow.md"}:
                    # Reached through its human-subject runtime projection.
                    continue
                if relative.startswith("methods/"):
                    # Conversation contract, named in the index but not a rule row.
                    self.assertIn(f"knowledge/{relative}", index_text)
                    continue
                self.assertIn(note.resolve(), linked)

    def test_index_points_portal_flows_at_human_subject_projections(self):
        paths = [relative for _, _, relative in index_rows()]
        for flow in ("request", "change", "stopzetten"):
            with self.subTest(flow=flow):
                self.assertIn(
                    "../nl-tax-provisional-assessment/reference/"
                    f"source-projections/{flow}-flow-human.md",
                    paths,
                )
                self.assertFalse(
                    any(p.endswith(f"/provisional/{flow}-flow.md") for p in paths)
                )

    def test_index_key_terms_occur_in_the_linked_note(self):
        for _, terms, relative in index_rows():
            text = (SKILLS / "nl-tax-knowledge" / relative).read_text(
                encoding="utf-8"
            ).lower()
            for term in (t.strip() for t in terms.split(",")):
                with self.subTest(path=relative, term=term):
                    self.assertIn(term.lower(), text)

    def test_skill_documents_use_skill_relative_shared_paths(self):
        bare = re.compile(r"(?<![./A-Za-z0-9_-])(?:_shared|nl-tax-shared-resources)/")
        for path in skill_documents():
            if path.parent == SHARED:
                continue
            with self.subTest(path=str(path.relative_to(SKILLS))):
                self.assertIsNone(bare.search(path.read_text(encoding="utf-8")))

    def test_owning_workflows_name_helper_skill_paths(self):
        flows = (
            SKILLS / "nl-tax-annual-return/reference/annual-flow.md",
            SKILLS / "nl-tax-provisional-assessment/reference/provisional-flow.md",
        )
        for flow in flows:
            text = flow.read_text(encoding="utf-8")
            for helper in HELPERS:
                with self.subTest(flow=flow.name, helper=helper):
                    self.assertIn(f"`../{helper}/SKILL.md`", text)

    def test_runtime_contract_allows_index_lookup_and_scoped_search(self):
        contract = " ".join(
            (SHARED / "runtime-contract.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("../nl-tax-shared-resources/knowledge-index.md", contract)
        self.assertIn("inside `../nl-tax-shared-resources/knowledge/` is allowed", contract)
        self.assertIn("helper `SKILL.md` path named by the owning workflow", contract)
        self.assertIn("installed incompletely", contract)

    def test_knowledge_skill_is_a_discoverable_read_only_lookup(self):
        path = SKILLS / "nl-tax-knowledge" / "SKILL.md"
        metadata = frontmatter(path)
        body = " ".join(path.read_text(encoding="utf-8").split())
        openai = yaml.safe_load(
            (SKILLS / "nl-tax-knowledge/agents/openai.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(metadata["allowed-tools"]), {"Read", "Glob", "Grep"})
        self.assertNotIn("user-invocable", metadata)
        self.assertNotIn("disable-model-invocation", metadata)
        self.assertTrue(openai["policy"]["allow_implicit_invocation"])
        for keyword in ("2025", "2026", "voorlopige aanslag", "eigen woning"):
            self.assertIn(keyword, metadata["description"])
        self.assertIn("../nl-tax-shared-resources/knowledge-index.md", body)
        self.assertIn("not model memory", body)
        self.assertIn("Do not read the complete register", body)
        self.assertIn(
            "Werkelijk rendement may become relevant when filing the annual 2026 "
            "return in 2027.",
            body,
        )
        self.assertIn("never creates or updates `workspace/` files", body)

    def test_intake_routes_rule_questions_to_the_index(self):
        intake = (SKILLS / "nl-tax-intake/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("nl-tax-knowledge", frontmatter(SKILLS / "nl-tax-intake/SKILL.md")["description"])
        self.assertIn("../nl-tax-shared-resources/knowledge-index.md", intake)

    def test_knowledge_note_headers_use_uniform_keys(self):
        for note in KNOWLEDGE.glob("**/*.md"):
            header = note.read_text(encoding="utf-8").split("\n## ", 1)[0]
            with self.subTest(note=str(note.relative_to(KNOWLEDGE))):
                self.assertNotRegex(header, r"(?m)^source_id:")
                self.assertNotRegex(header, r"(?m)^tax_years:")
                self.assertRegex(header, r"(?m)^tax_year: ")
                self.assertRegex(header, r"(?m)^workflow: ")


if __name__ == "__main__":
    unittest.main()
