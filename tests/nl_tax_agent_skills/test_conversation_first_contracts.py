#!/usr/bin/env python3
"""0.4 conversation-first contracts (docs/maintainers/0.4-conversation-first-design.md).

Covers:
    - R3 write boundary: only the two owning workflows, the field mapper, and
      the submit companion carry ``Edit(./workspace/**)``; nothing lists Bash or
      Write; intake, knowledge, and the background helpers have no Edit rule.
    - R1/R8/R10: no runtime skill file names a retired 0.3 artifact, except the
      sentences saying 0.3 ledgers are never read and older packs are ordinary
      source documents.
    - R4/R5/R7: both workpack templates carry the required headings in order,
      a parseable Appendix A resume record with the exact keys, and the
      ``not yet mapped`` / ``not requested`` placeholders.
    - R2/R9: the owning workflows state the fixed path, nothing-by-default save
      consent, and their critical boundaries on the first screen.
    - R7 grader: validate_field_map.py / render_field_map.py accept a ``.md``
      workpack (Appendix B) and reject one that is ``not yet mapped``.
    - Review amendments A1-A12: session-scoped consent (templates default to
      ``not_given``; writers check the conversation, not the file), the
      replace-or-keep question, the first save carrying everything, mapper-owned
      gap rows, one yes/no question per reply, offer frequency and
      ``queued_workflow`` clearing, non-persistent folders, presentation that
      never writes, consistent IDs and identifier rules, stale map/checklist
      markers after a changed fact (A10), no hidden unsaved map (A11), and the
      Field map summary as the checked surface (A12).
"""

import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
SKILLS = PLUGIN / "skills"
FIELD_MAPPER_TOOLS = REPO_ROOT / "tools" / "nl_tax_agent_skills" / "field_mapper"
VALIDATOR = FIELD_MAPPER_TOOLS / "validate_field_map.py"
RENDERER = FIELD_MAPPER_TOOLS / "render_field_map.py"

ANNUAL_TEMPLATE = SKILLS / "nl-tax-annual-return/templates/annual-workpack.md"
PROVISIONAL_TEMPLATE = (
    SKILLS / "nl-tax-provisional-assessment/templates/provisional-workpack.md"
)
ANNUAL_PATH = "workspace/nl-tax-annual-2025-workpack.md"
PROVISIONAL_PATH = "workspace/nl-tax-provisional-2026-workpack.md"

WRITERS = {
    "nl-tax-annual-return",
    "nl-tax-provisional-assessment",
    "nl-tax-field-mapper",
    "nl-tax-submit-companion",
}
NON_WRITERS = {
    "nl-tax-intake",
    "nl-tax-knowledge",
    "nl-tax-box1-home",
    "nl-tax-box2",
    "nl-tax-box3",
    "nl-tax-partner-deductions",
    "nl-tax-winst",
}

RESUME_RECORD_KEYS = [
    "workpack_format",
    "workpack_version",
    "plugin_version",
    "workflow",
    "tax_year",
    "created_at",
    "updated_at",
    "save_consent",
    "readiness",
    "generation_confirmed",
    "queued_workflow",
    "sections",
    "sources_loaded",
]
ANNUAL_SECTION_KEYS = [
    "filing_status",
    "box1",
    "winst",
    "eigen_woning",
    "box2",
    "box3_peildatum",
    "box3_actual",
    "deductions",
    "credits_screening",
    "partner_allocation",
    "confirm",
]
PROVISIONAL_SECTION_KEYS = [
    "baseline",
    "income_employment",
    "income_pension_benefit",
    "income_other",
    "winst_forecast",
    "deductions",
    "box2",
    "box3_peildatum",
    "partner_allocation",
    "stopzetten_direction",
    "confirm",
]

# R4 headings shared by both workflows, in order. The workflow's own tax
# sections sit between "Sources used" and "Open questions".
R4_LEADING = [
    "How to use this file",
    "Contents",
    "Scope",
    "Unsupported-case checks",
    "Taxpayer profile summary",
    "Documents and sources",
    "Sources used",
]
R4_TRAILING = [
    "Open questions",
    "Missing information",
    "Assumptions",
    "User-stated values index",
    "Field map summary",
    "Manual-entry checklist",
    "Human review checklist",
    "Not submission advice",
    "Appendix A — Resume record",
    "Appendix B — Field map",
]
ANNUAL_TAX_SECTIONS = [
    "Filing status and late-filing exposure",
    "Income notes",
    "Winst uit onderneming notes",
    "Own-home notes",
    "Box 2 notes",
    "Box 3 notes",
    "Deductions notes",
    "Credits screening",
    "Fiscal partner notes",
]
PROVISIONAL_TAX_SECTIONS = [
    "Existing baseline, if any",
    "Current-year estimates",
    "Delta summary",
    "Review questions",
    "Stopzetten outcome",
    "Income estimate",
    "Winst uit onderneming forecast",
    "Own-home estimate",
    "Box 2 provisional estimate",
    "Box 3 provisional estimate",
    "Deductions estimate",
    "Change subflow — full re-entry reminder",
]


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}


def headings(text):
    return re.findall(r"(?m)^## (.+?)\s*$", text)


def section(text, heading):
    marker = f"\n## {heading}\n"
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    return text[start:] if end == -1 else text[start:end]


def content_lines(body):
    """Lines of a section outside bracketed fill notes and blank lines."""
    without_notes = re.sub(r"\[[^\]]*\]", "", body, flags=re.DOTALL)
    return [line.strip() for line in without_notes.splitlines() if line.strip()]


def resume_record(text):
    blocks = re.findall(
        r"```yaml\n(.*?)\n```", section(text, "Appendix A — Resume record"), re.DOTALL
    )
    assert len(blocks) == 1, blocks
    return yaml.safe_load(blocks[0])


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_files():
    for path in sorted(SKILLS.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            yield path
    yield from sorted((PLUGIN / "agents").glob("*.md"))


def sentences(text):
    flat = " ".join(text.split())
    return re.split(r"(?<=[.!?])\s+(?=[-*`A-Z0-9])", flat)


class SkillWriteBoundaryTests(unittest.TestCase):
    def test_skill_set_is_eleven_skills_plus_shared_resources(self):
        names = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(names, WRITERS | NON_WRITERS | {"nl-tax-shared-resources"})
        self.assertEqual(len(WRITERS | NON_WRITERS), 11)

    def test_only_workpack_writers_carry_the_workspace_edit_rule(self):
        for skill in sorted(WRITERS | NON_WRITERS | {"nl-tax-shared-resources"}):
            tools = frontmatter(SKILLS / skill / "SKILL.md").get("allowed-tools") or []
            with self.subTest(skill=skill):
                for tool in tools:
                    self.assertFalse(tool.startswith("Bash"), tool)
                    self.assertFalse(tool.startswith("Write"), tool)
                edits = [tool for tool in tools if tool.startswith("Edit")]
                if skill in WRITERS:
                    self.assertEqual(edits, ["Edit(./workspace/**)"])
                else:
                    self.assertEqual(edits, [])

    def test_specialist_reviewer_agent_never_writes(self):
        tools = frontmatter(PLUGIN / "agents/nl-tax-specialist-reviewer.md")["tools"]
        listed = {tool.strip() for tool in str(tools).split(",")}
        self.assertEqual(listed, {"Read", "Grep", "Glob", "WebSearch", "WebFetch"})

    def test_writers_name_only_their_own_workpack_sections(self):
        mapper = " ".join((SKILLS / "nl-tax-field-mapper/SKILL.md").read_text(encoding="utf-8").split())
        companion = " ".join(
            (SKILLS / "nl-tax-submit-companion/SKILL.md").read_text(encoding="utf-8").split()
        )
        runtime = " ".join(
            (SKILLS / "nl-tax-shared-resources/runtime-contract.md").read_text(encoding="utf-8").split()
        )
        for text in (mapper, companion, runtime):
            self.assertIn(f"`{ANNUAL_PATH}`", text)
            self.assertIn(f"`{PROVISIONAL_PATH}`", text)
        self.assertIn(
            "write the `## Field map summary` section and `## Appendix B — Field map`",
            mapper,
        )
        self.assertIn("Edit only those two sections", mapper)
        self.assertIn("into the `## Manual-entry checklist` section", companion)
        self.assertIn("Edit only that section", companion)
        self.assertIn("Without save consent, write nothing.", companion)
        self.assertIn("Each writer edits only its own sections.", runtime)
        self.assertIn("The plugin never deletes files.", runtime)


class LegacyArtifactTests(unittest.TestCase):
    # Retired 0.3 runtime artifacts (0.4 design R1, R3, R8, R10).
    RETIRED = {
        "workspace_root": r"workspace_root",
        "workspace/annual/": r"workspace/annual/",
        "workspace/shared/": r"workspace/shared/",
        "workspace/taxpayer/": r"workspace/taxpayer/",
        "missing-info.md": r"(?<![\w-])missing-info\.md",
        "assumptions.md": r"(?<![\w-])assumptions\.md",
        "field-map.yaml": r"(?<![\w-])field-map\.yaml",
        "notes/<section>": r"(?<![\w-])notes/",
        "uploads/ or evidence/": r"(?:^|[\s`(\"'])(?:uploads|evidence)/",
        "nl-tax-evidence-indexer": r"nl-tax-evidence-indexer",
    }
    LEDGERS = ("profile.yaml", "session-progress.yaml", "evidence-index.yaml")
    OLD_PACKS = ("return-pack.md", "provisional-pack.md")

    def test_runtime_files_name_no_retired_artifact(self):
        contract = SKILLS / "nl-tax-annual-return/reference/annual-output-contract.md"
        for path in runtime_files():
            text = path.read_text(encoding="utf-8")
            if path == contract:
                # The annual self-check lists the provisional path as a
                # forbidden cross-contamination token; that is not a use.
                cross = text.split("### Cross-contamination", 1)[1].split("\n### ", 1)[0]
                text = text.replace(cross, "")
            relative = path.relative_to(PLUGIN)
            for label, pattern in self.RETIRED.items():
                with self.subTest(path=str(relative), artifact=label):
                    self.assertIsNone(re.search(pattern, text, re.MULTILINE))
            with self.subTest(path=str(relative), artifact="workspace/provisional/"):
                self.assertNotIn("workspace/provisional/", text)

    def test_ledgers_and_old_packs_appear_only_as_never_read_or_source_documents(self):
        seen = {"ledger": 0, "pack": 0}
        for path in runtime_files():
            relative = str(path.relative_to(PLUGIN))
            for sentence in sentences(path.read_text(encoding="utf-8")):
                if any(name in sentence for name in self.LEDGERS):
                    seen["ledger"] += 1
                    with self.subTest(path=relative, sentence=sentence[:90]):
                        self.assertRegex(sentence, r"never read|not migrated|no automatic migration")
                if any(name in sentence for name in self.OLD_PACKS):
                    seen["pack"] += 1
                    with self.subTest(path=relative, sentence=sentence[:90]):
                        self.assertIn("ordinary source document", sentence)
        # The rule itself must stay stated where resumes happen.
        self.assertGreaterEqual(seen["ledger"], 3)
        self.assertGreaterEqual(seen["pack"], 3)

    def test_retired_runtime_files_are_gone(self):
        for relative in (
            "nl-tax-evidence-indexer",
            "nl-tax-shared-resources/templates",
            "nl-tax-intake/templates",
            "nl-tax-annual-return/templates/annual-return-pack.md",
            "nl-tax-provisional-assessment/templates/provisional-pack.md",
            "nl-tax-provisional-assessment/templates/delta-summary.md",
            "nl-tax-provisional-assessment/templates/review-questions.md",
            "nl-tax-submit-companion/templates/manual-submission-checklist.md",
        ):
            with self.subTest(relative=relative):
                self.assertFalse((SKILLS / relative).exists())
        for relative in (
            "nl-tax-shared-resources/reference/evidence-types.md",
            "nl-tax-shared-resources/reference/extraction-boundaries.md",
            "nl-tax-submit-companion/templates/manual-entry-checklist.md",
        ):
            with self.subTest(relative=relative):
                self.assertTrue((SKILLS / relative).is_file())


class WorkpackTemplateTests(unittest.TestCase):
    def setUp(self):
        self.annual = ANNUAL_TEMPLATE.read_text(encoding="utf-8")
        self.provisional = PROVISIONAL_TEMPLATE.read_text(encoding="utf-8")

    def test_annual_template_headings_follow_r4_order(self):
        self.assertTrue(self.annual.startswith("# "))
        self.assertIn("STATUS:", self.annual.split("\n## ", 1)[0])
        self.assertEqual(
            headings(self.annual), R4_LEADING + ANNUAL_TAX_SECTIONS + R4_TRAILING
        )

    def test_provisional_template_headings_follow_r4_and_its_contract(self):
        self.assertTrue(self.provisional.startswith("# "))
        self.assertIn("STATUS:", self.provisional.split("\n## ", 1)[0])
        found = headings(self.provisional)
        # The provisional output contract keeps the Subflow identifier right
        # after Contents; every other R4 heading keeps its order.
        self.assertTrue(found[2].startswith("Subflow: "), found[2])
        without_subflow = found[:2] + found[3:]
        self.assertEqual(
            without_subflow, R4_LEADING + PROVISIONAL_TAX_SECTIONS + R4_TRAILING
        )
        contract = (
            SKILLS / "nl-tax-provisional-assessment/reference/provisional-output-contract.md"
        ).read_text(encoding="utf-8")
        table = contract.split("## Required sections", 1)[1].split("\n---", 1)[0]
        rows = re.findall(r"(?m)^\| ([^|]+?)\s*\|", table)[1:]  # skip the header row
        expected = ["Title + STATUS banner"] + [
            "Subflow identifier" if h.startswith("Subflow: ") else h
            for h in found
        ]
        normalized = [
            "Existing baseline, if any" if row == "Existing baseline" else row
            for row in rows
        ]
        self.assertEqual(normalized, expected)

    def test_contents_lists_match_the_headings(self):
        for text in (self.annual, self.provisional):
            listed = [
                line[2:].strip()
                for line in section(text, "Contents").splitlines()
                if line.startswith("- ")
            ]
            found = [
                "Subflow" if h.startswith("Subflow: ") else h
                for h in headings(text)
                if h != "Contents"
            ]
            found = found[1:]  # "How to use this file" precedes Contents
            listed = ["Subflow" if item.startswith("Subflow: ") else item for item in listed]
            with self.subTest(template=text[:40]):
                self.assertEqual(listed, found)

    def test_resume_records_have_exact_r5_keys(self):
        for text, workflow, year, keys in (
            (self.annual, "annual_2025", 2025, ANNUAL_SECTION_KEYS),
            (self.provisional, "provisional_2026_request", 2026, PROVISIONAL_SECTION_KEYS),
        ):
            record = resume_record(text)
            with self.subTest(workflow=workflow):
                self.assertEqual(list(record), RESUME_RECORD_KEYS)
                self.assertEqual(record["workpack_format"], "nl-tax-workpack")
                self.assertEqual(record["workpack_version"], "2.0")
                self.assertEqual(record["plugin_version"], "0.4.0")
                self.assertEqual(record["workflow"], workflow)
                self.assertEqual(record["tax_year"], year)
                self.assertIn(record["save_consent"], {"given", "not_given"})
                self.assertEqual(record["readiness"], "draft")
                self.assertIs(record["generation_confirmed"], False)
                self.assertIsNone(record["queued_workflow"])
                self.assertEqual(record["sources_loaded"], [])
                self.assertEqual(list(record["sections"]), keys)
                for entry in record["sections"].values():
                    self.assertEqual(entry, {"status": "not_started", "open": []})

    def test_flow_section_tables_match_the_resume_record_keys(self):
        for flow, keys in (
            ("nl-tax-annual-return/reference/annual-flow.md", ANNUAL_SECTION_KEYS),
            ("nl-tax-provisional-assessment/reference/provisional-flow.md", PROVISIONAL_SECTION_KEYS),
        ):
            text = (SKILLS / flow).read_text(encoding="utf-8")
            table = text.split("Section", 1)[1]
            found = re.findall(r"(?m)^\| `([a-z0-9_]+)` \|", table)
            with self.subTest(flow=flow):
                self.assertEqual(found, keys)
        elicitation = " ".join(
            (SKILLS / "nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertIn("# annual keys: " + ", ".join(ANNUAL_SECTION_KEYS[:6]), elicitation)
        self.assertIn("# provisional keys: " + ", ".join(PROVISIONAL_SECTION_KEYS[:3]), elicitation)

    def test_mapper_and_companion_sections_hold_their_placeholders(self):
        for text in (self.annual, self.provisional):
            with self.subTest(template=text[:40]):
                self.assertEqual(
                    content_lines(section(text, "Appendix B — Field map")), ["not yet mapped"]
                )
                self.assertEqual(
                    content_lines(section(text, "Field map summary")), ["not yet mapped"]
                )
                self.assertEqual(
                    content_lines(section(text, "Manual-entry checklist")), ["not requested"]
                )
                self.assertNotIn("```", section(text, "Appendix B — Field map"))

    def test_profile_summary_is_a_keyed_provenance_table_without_identifiers(self):
        for text in (self.annual, self.provisional):
            profile = section(text, "Taxpayer profile summary")
            rows = [line for line in profile.splitlines() if line.startswith("|")]
            with self.subTest(template=text[:40]):
                self.assertEqual(rows[0].replace(" ", ""), "|Key|Value|Src|")
                self.assertTrue(set(rows[1]) <= {"|", "-", " "})
                self.assertGreater(len(rows), 10)
                for row in rows[2:]:
                    cells = [cell.strip() for cell in row.strip("|").split("|")]
                    self.assertEqual(len(cells), 3, row)
                    self.assertRegex(cells[0], r"^`[a-z0-9_.]+`$")
                    self.assertTrue(cells[2], row)
                    self.assertNotRegex(cells[0].lower(), r"bsn|iban|naam|name|adres")
                self.assertIn("No name, BSN, or IBAN is needed", " ".join(profile.split()))

    def test_documents_and_sources_rows_use_ev_ids_without_hashes(self):
        for text in (self.annual, self.provisional):
            documents = section(text, "Documents and sources")
            header = next(line for line in documents.splitlines() if line.startswith("|"))
            cells = [cell.strip() for cell in header.strip("|").split("|")]
            with self.subTest(template=text[:40]):
                self.assertEqual(cells[0], "ID")
                self.assertEqual(len(cells), 8)
                self.assertTrue(cells[1].startswith("Document"))
                self.assertEqual(
                    cells[2:], ["Type", "Tax year", "Owner", "Location", "Values taken", "Status"]
                )
                self.assertIn("| ev_001 |", documents)
                self.assertIn("no file hashes", " ".join(documents.lower().split()))
                self.assertNotIn("sha256", documents.lower())

    def test_how_to_use_file_has_three_lines(self):
        for text in (self.annual, self.provisional):
            bullets = [
                line for line in section(text, "How to use this file").splitlines()
                if line.startswith("- ")
            ]
            joined = " ".join(bullets).lower()
            with self.subTest(template=text[:40]):
                self.assertEqual(len(bullets), 3)
                self.assertIn("your own working file", joined)
                self.assertIn("attach", joined)
                self.assertIn("mijn belastingdienst", joined)

    def test_provisional_box3_section_is_fictitious_only(self):
        box3 = section(self.provisional, "Box 3 provisional estimate")
        self.assertIn("Werkelijk rendement is not part of provisional 2026.", box3)
        without_note = box3.replace("Werkelijk rendement is not part of provisional 2026.", "")
        self.assertNotIn("werkelijk", without_note.lower())
        self.assertNotIn("actual return", without_note.lower())


class OwningWorkflowFirstScreenTests(unittest.TestCase):
    FIRST_SCREEN_LINES = 60

    def first_screen(self, skill):
        lines = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").splitlines()
        return " ".join(" ".join(lines[: self.FIRST_SCREEN_LINES]).split())

    def body(self, skill):
        return " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())

    def test_annual_first_screen_carries_the_critical_boundaries(self):
        head = self.first_screen("nl-tax-annual-return")
        for phrase in (
            "## Critical boundaries",
            "**Human-only portal.**",
            "never log in",
            "DigiD details, passwords, codes, or sessions",
            "Do not collect a BSN, IBAN, or names",
            "**Nothing is written by default.**",
            "clearly consents to saving",
            f"`{ANNUAL_PATH}`",
            "Never write the provisional workpack or any other file",
            "**Annual 2025 only.**",
            "never copy an annual amount into 2026 facts",
            "Annual Box 3 collects fictitious and actual-return data",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, head)

    def test_provisional_first_screen_carries_the_critical_boundaries(self):
        head = self.first_screen("nl-tax-provisional-assessment")
        for phrase in (
            "## Critical boundaries",
            "**Human-only portal.**",
            "Never log in",
            "BSN, DigiD details, passwords, codes, or sessions",
            "**Nothing is written by default.**",
            f"`{PROVISIONAL_PATH}`",
            "only after the user consents to saving",
            "Never write the annual workpack or any other file",
            "**Annual and provisional stay separate.**",
            "**Box 3 is fictitious-only.**",
            "Werkelijk rendement may become relevant when filing the annual 2026 return in 2027.",
            "**Stopzetten is only for a monthly refund.**",
            "**A change is a full re-entry.**",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, head)

    def test_owning_workflows_make_the_consented_save_offer(self):
        offer = (
            "This can take a few sessions. Want me to keep your workpack as one "
            "file in your working folder so you can pick up later? Otherwise "
            "everything stays in this conversation."
        )
        for skill, path in (
            ("nl-tax-annual-return", ANNUAL_PATH),
            ("nl-tax-provisional-assessment", PROVISIONAL_PATH),
        ):
            body = self.body(skill)
            with self.subTest(skill=skill):
                self.assertIn(offer, body)
                self.assertIn('("save my workpack", "keep a file", "bewaar")', body)
                self.assertIn("Offer each point at most once", body)
                self.assertIn("don't ask again", body)
                self.assertIn("`save_consent: given`", body)
                self.assertIn("stop saving", body)
                self.assertIn("Never delete files", body)
                self.assertIn("-v2", body)
                self.assertIn("no writable working folder", body)
                self.assertIn(path, body)
        # A file found at the fixed path is used only after one confirmation.
        annual = self.body("nl-tax-annual-return")
        resume = " ".join(
            (SKILLS / "nl-tax-provisional-assessment/reference/resume-contract.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertIn("I found your saved 2025 workpack, last updated <date>. Continue from it?", annual)
        self.assertIn("I found your saved 2026 workpack, last updated <date>. Continue from it?", resume)
        self.assertIn("load `reference/resume-contract.md` before asking anything else",
                      self.body("nl-tax-provisional-assessment"))

    def test_every_skill_puts_the_portal_and_write_boundary_on_the_first_screen(self):
        for skill in sorted(WRITERS | NON_WRITERS):
            head = self.first_screen(skill).lower()
            with self.subTest(skill=skill):
                self.assertIn("never log in", head)
                self.assertIn("claude in chrome", head)
                self.assertRegex(head, r"bsn|credential")
                self.assertRegex(
                    head,
                    r"writes nothing|nothing is written by default|write nothing",
                )

    def test_every_recap_and_compaction_rule_is_present(self):
        for skill in ("nl-tax-annual-return", "nl-tax-provisional-assessment"):
            body = self.body(skill)
            with self.subTest(skill=skill):
                self.assertIn("Confirmed so far", body)
                self.assertIn("no longer visible verbatim", body)
                self.assertIn("never reconstruct an amount from memory or a summary", body)


def flat(relative):
    """Whitespace-normalized text of a plugin file under ``skills/``."""
    return " ".join((SKILLS / relative).read_text(encoding="utf-8").split())


def flat_repo(relative):
    return " ".join((REPO_ROOT / relative).read_text(encoding="utf-8").split())


class ReviewAmendmentTests(unittest.TestCase):
    """Binding review amendments A1-A12 of the 0.4 design."""

    RUNTIME = "nl-tax-shared-resources/runtime-contract.md"
    ANNUAL_SKILL = "nl-tax-annual-return/SKILL.md"
    ASSEMBLY = "nl-tax-annual-return/reference/phases/10-assembly.md"
    PROVISIONAL_SKILL = "nl-tax-provisional-assessment/SKILL.md"
    MAPPER_SKILL = "nl-tax-field-mapper/SKILL.md"
    MAPPER_FLOW = "nl-tax-field-mapper/reference/mapper-flow.md"
    COMPANION_SKILL = "nl-tax-submit-companion/SKILL.md"
    REPLACE_OR_KEEP = (
        "Replace that older file with this one, or keep it and stay in this "
        "conversation only?"
    )

    # A1 ---------------------------------------------------------------------

    def test_templates_default_save_consent_to_not_given(self):
        for template in (ANNUAL_TEMPLATE, PROVISIONAL_TEMPLATE):
            text = template.read_text(encoding="utf-8")
            with self.subTest(template=template.name):
                self.assertEqual(resume_record(text)["save_consent"], "not_given")
                self.assertNotRegex(text, r"(?m)^save_consent:\s*given\b")
                appendix = " ".join(section(text, "Appendix A — Resume record").split())
                self.assertIn("never an authorization to write", appendix)
        elicitation = flat("nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md")
        self.assertIn("save_consent: not_given", elicitation)
        contract = flat("nl-tax-provisional-assessment/reference/provisional-output-contract.md")
        self.assertNotIn("`save_consent: given`,", contract)
        self.assertIn("defaults to `not_given` in the template", contract)

    def test_mapper_and_companion_check_consent_in_the_conversation_not_the_file(self):
        for relative in (self.MAPPER_SKILL, self.MAPPER_FLOW, self.COMPANION_SKILL):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertRegex(
                    text,
                    r"[Cc]onsent is (?:session-scoped and )?checked in the conversation, "
                    r"(?:never|not) (?:in )?the file",
                )
                self.assertIn("is a record, not an authorization", text)
                self.assertIn("while save consent is active in this conversation", text)
                self.assertNotIn("When the saved workpack records `save_consent: given`", text)
                # A found file is never read before the owner's confirm-once step.
                self.assertIn("confirm-once step", text)
                self.assertIn("I found your saved 2025 workpack, last updated <date>. Continue from it?", text)
        runtime = flat(self.RUNTIME)
        self.assertIn("**Consent is session-scoped.**", runtime)
        self.assertIn("checks this conversation, not the file", runtime)
        self.assertIn(
            "never read a file found at the fixed path unless the user has confirmed it", runtime
        )
        for relative in (self.ANNUAL_SKILL, self.PROVISIONAL_SKILL):
            with self.subTest(file=relative):
                self.assertIn("check the conversation, never the file's `save_consent`", flat(relative))

    # A2 ---------------------------------------------------------------------

    def test_runtime_contract_asks_replace_or_keep_before_overwriting(self):
        runtime = flat(self.RUNTIME)
        self.assertIn("**Never overwrite silently.**", runtime)
        self.assertIn(
            "If a file already exists at the fixed path and the user did not resume it in "
            "this conversation, consent to save includes one short question",
            runtime,
        )
        self.assertIn(self.REPLACE_OR_KEEP, runtime)
        self.assertIn("Never merge into that file.", runtime)
        for relative in (
            self.ANNUAL_SKILL,
            self.PROVISIONAL_SKILL,
            "nl-tax-provisional-assessment/reference/resume-contract.md",
            "nl-tax-intake/reference/intake-flow.md",
        ):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertIn(self.REPLACE_OR_KEEP, text)
                self.assertNotIn("If the file exists, update it in place", text)
                self.assertNotIn("may want to move or rename the old file", text)

    # A3 ---------------------------------------------------------------------

    def test_first_save_writes_everything_established_so_far(self):
        runtime = flat(self.RUNTIME)
        self.assertIn("**The first save writes everything established so far:**", runtime)
        self.assertIn("A download delivered at generation is produced after mapping", runtime)
        self.assertIn(
            "the first save writes the whole workpack from the facts and provenance recorded in this conversation",
            flat(self.ASSEMBLY),
        )
        self.assertIn(
            "owning workflow's first save carries this checklist into the file only when each of its "
            "values matches the map rebuilt for that save",
            flat(self.COMPANION_SKILL),
        )

    # A10 --------------------------------------------------------------------

    STALE_LINE = "STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate before use."
    PROVISIONAL_FLOW = "nl-tax-provisional-assessment/reference/provisional-flow.md"
    PROVISIONAL_CONTRACT = "nl-tax-provisional-assessment/reference/provisional-output-contract.md"
    ANNUAL_CONTRACT = "nl-tax-annual-return/reference/annual-output-contract.md"
    CHECKLIST_TEMPLATE = "nl-tax-submit-companion/templates/manual-entry-checklist.md"

    def test_changed_fact_marks_map_and_checklist_stale(self):
        for relative in (
            self.RUNTIME,
            self.ASSEMBLY,
            self.ANNUAL_SKILL,
            self.ANNUAL_CONTRACT,
            self.PROVISIONAL_SKILL,
            self.PROVISIONAL_FLOW,
            self.PROVISIONAL_CONTRACT,
            self.MAPPER_SKILL,
            self.MAPPER_FLOW,
            self.COMPANION_SKILL,
            "nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md",
        ):
            with self.subTest(file=relative):
                self.assertIn(self.STALE_LINE, flat(relative))
        for relative in (self.ASSEMBLY, self.PROVISIONAL_SKILL):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertIn("generation_confirmed", text)
                self.assertIn("Field map summary", text)
                self.assertIn("Appendix B", text)
                self.assertIn("Manual-entry checklist", text)
                self.assertIn("only edit this skill makes in the mapper's and", text)
                self.assertIn("only regeneration clears", text.lower())
        self.assertNotIn("tell the user the workpack and any field map need regenerating", flat(self.PROVISIONAL_SKILL))
        self.assertNotIn("tell the user that the saved field map and any checklist predate", flat(self.ASSEMBLY))
        runtime = flat(self.RUNTIME)
        self.assertIn("### Stale outputs after a change", runtime)
        self.assertIn("A stale marker is valid only while `generation_confirmed` is `false`.", runtime)
        self.assertIn("The one exception is the stale line", runtime)
        for template in (ANNUAL_TEMPLATE, PROVISIONAL_TEMPLATE):
            with self.subTest(template=template.name):
                self.assertIn(
                    "STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate before use.",
                    " ".join(section(template.read_text(encoding="utf-8"), "Field map summary").split()),
                )

    def test_companion_blocks_on_unconfirmed_or_stale_map(self):
        companion = flat(self.COMPANION_SKILL)
        self.assertIn("## Stale map: blocker first", companion)
        self.assertIn(
            "When `generation_confirmed` is `false` or any stale marker remains, that is a blocker "
            "that only regeneration clears",
            companion,
        )
        self.assertIn("Never copy a value from a stale map or checklist", companion)
        self.assertIn("with no steps and no values to enter. Write nothing to the file.", companion)
        self.assertIn("a stale map or unconfirmed workpack", companion)
        checklist = flat(self.CHECKLIST_TEMPLATE)
        self.assertIn("If `generation_confirmed` is false", checklist)
        self.assertIn("list only the stale blocker", checklist)
        self.assertIn("no steps, and no values until regeneration re-runs the field mapper", checklist)
        self.assertIn("Never copy a value from a stale map", checklist)

    # A11 --------------------------------------------------------------------

    def test_mapper_rebuilds_from_recorded_facts_and_keeps_no_hidden_map(self):
        for relative in (
            self.RUNTIME,
            self.ASSEMBLY,
            self.ANNUAL_SKILL,
            self.ANNUAL_CONTRACT,
            self.PROVISIONAL_SKILL,
            self.PROVISIONAL_CONTRACT,
            self.MAPPER_SKILL,
            self.MAPPER_FLOW,
        ):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertIn("An unsaved field map is not state", text)
                self.assertRegex(text, r"rebuilds? (?:the|every|each) (?:map|entry)")
                self.assertIn("recorded facts", text)
                self.assertIn("FM-* check", text)
                for retired in (
                    "writes this table, the YAML",
                    "carries this table and YAML into the file",
                    "including any Field map summary, Appendix B, and Manual-entry checklist already in the conversation",
                    "including a field map summary, Appendix B, and checklist that already exist",
                    "carried over exactly as the field mapper and the submit companion composed",
                    "or the map composed earlier in this conversation), update it",
                ):
                    self.assertNotIn(retired, text)
        for relative in (self.MAPPER_SKILL, self.MAPPER_FLOW):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertIn("re-confirm", text)
                self.assertIn("not visible verbatim in the conversation or the saved workpack", text)
        self.assertIn("**No hidden map.** An unsaved field map is not state.", flat(self.RUNTIME))
        flow = flat(self.MAPPER_FLOW)
        self.assertIn("a map composed earlier in this conversation, or a stale map, is never an input", flow)

    # A12 --------------------------------------------------------------------

    def test_summary_is_the_checked_surface(self):
        for relative in (
            self.RUNTIME,
            self.ANNUAL_CONTRACT,
            self.PROVISIONAL_CONTRACT,
            self.MAPPER_FLOW,
            self.MAPPER_SKILL,
        ):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertIn("checked surface", text)
                self.assertIn("`MISSING - enter manually` row with its Q-ID", text)
        self.assertIn("the rendering always states the map's state", flat(self.RUNTIME))

    # A4 ---------------------------------------------------------------------

    def test_field_mapper_owns_its_gap_rows(self):
        mapper = flat(self.MAPPER_SKILL)
        flow = flat(self.MAPPER_FLOW)
        self.assertIn("adds its own row to `## Open questions` (continuing the Q001 numbering)", mapper)
        self.assertIn("The mapper owns these gap rows.", flow)
        self.assertNotIn("belong to the owning workflow", flow)
        for text in (mapper, flow):
            self.assertIn("`sections.<key>.open`", text)
        for relative in (
            self.RUNTIME,
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-provisional-assessment/reference/provisional-output-contract.md",
        ):
            with self.subTest(file=relative):
                self.assertRegex(flat(relative), r"(?:mapper's own gap rows|its own gap rows)")
        contributing = flat_repo("CONTRIBUTING.md")
        self.assertIn("plus its own gap rows in `## Open questions` and `## Missing information`", contributing)

    # A5 ---------------------------------------------------------------------

    def test_one_yes_no_question_per_reply(self):
        runtime = flat(self.RUNTIME)
        self.assertIn("### One yes/no question per reply", runtime)
        self.assertIn(
            "Never put two yes/no offers, or a question plus an offer, in the same reply", runtime
        )
        assembly = flat(self.ASSEMBLY)
        self.assertIn("Ask one yes/no question per reply", assembly)
        self.assertIn("never add the save offer or the checklist offer to this reply", assembly)
        self.assertNotIn("two-part offer", assembly)
        provisional = flat(self.PROVISIONAL_SKILL)
        self.assertIn("Ask one yes/no question per reply", provisional)
        self.assertIn("never add the save offer or the checklist offer to it", provisional)
        self.assertNotIn("offer to save if the user has not opted in, and ask whether", provisional)
        for relative in (
            self.ANNUAL_SKILL,
            self.PROVISIONAL_SKILL,
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-provisional-assessment/reference/provisional-flow.md",
        ):
            with self.subTest(file=relative):
                self.assertIn("before the first collection question", flat(relative))
        for relative in (self.MAPPER_SKILL, self.MAPPER_FLOW):
            with self.subTest(file=relative):
                self.assertIn("the checklist offer comes in the reply after that", flat(relative))
        elicitation = flat("nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md")
        self.assertNotIn("this is also the last natural point to offer it", elicitation)

    # A6 ---------------------------------------------------------------------

    def test_handoff_offer_counts_once_and_clears_queued_workflow(self):
        runtime = flat(self.RUNTIME)
        assembly = flat(self.ASSEMBLY)
        provisional = flat(self.PROVISIONAL_SKILL)
        self.assertIn("also counts as the provisional workflow-start offer", runtime)
        self.assertIn("also counts as the 2026 workflow-start offer", assembly)
        self.assertIn("counts as this workflow's start offer; do not repeat it", provisional)
        self.assertIn("When provisional collection starts, `queued_workflow` is cleared", runtime)
        self.assertIn("When 2026 collection starts, `queued_workflow` is cleared", assembly)
        self.assertNotIn("has neither opted in nor declined", assembly)
        self.assertIn('an earlier "no" does not suppress this point', assembly)

    # A7 ---------------------------------------------------------------------

    def test_non_persistent_folders_also_get_a_download(self):
        for relative in (self.RUNTIME, self.ANNUAL_SKILL, self.PROVISIONAL_SKILL):
            with self.subTest(file=relative):
                self.assertIn("may not outlast the session", flat(relative))
        privacy = flat_repo("PRIVACY.md")
        self.assertIn("the file lives in the host's task storage", privacy)
        self.assertIn("the download is the copy you keep", privacy)

    # A8 ---------------------------------------------------------------------

    def test_presentation_never_writes_and_chat_shows_no_yaml(self):
        runtime = flat(self.RUNTIME)
        self.assertIn("Presentation never writes.", runtime)
        self.assertIn("Creating a downloadable file counts as saving", runtime)
        self.assertIn("no Appendix A or Appendix B YAML", runtime)
        self.assertIn("`F:ev_003 (jaaropgaaf ING 2025)`", runtime)
        for relative in (
            self.ANNUAL_SKILL,
            self.ASSEMBLY,
            self.PROVISIONAL_SKILL,
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-provisional-assessment/reference/provisional-output-contract.md",
        ):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertRegex(text, r"counts as saving")
                self.assertNotIn("document or artifact surface", text)
                self.assertNotIn("deliver it as a downloadable file or document instead", text)
        for relative in (self.MAPPER_SKILL, self.MAPPER_FLOW):
            text = flat(relative)
            with self.subTest(file=relative):
                self.assertIn("never printed in chat", text)
                self.assertNotIn("keep the YAML in the conversation only", text)
                self.assertNotIn("the YAML stays in the conversation", text)

    # A9 ---------------------------------------------------------------------

    def test_ids_chat_rows_and_identifier_rules_are_consistent(self):
        stray_ids = re.compile(r"(?<![\w-])(?:Q|M|A)\d{1,2}(?![\d\w])|(?<![\w])ev_\d{1,2}(?!\d)")
        for path in runtime_files():
            if "/knowledge/" in path.as_posix():
                continue  # reviewed source notes are not workpack instructions
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(PLUGIN))):
                self.assertIsNone(stray_ids.search(text))
        self.assertIn("| Eigen woning | WOZ-waarde | eigenwoning.woz_waarde | MISSING - enter manually | Q007 |",
                      flat(self.MAPPER_FLOW))
        for relative in (
            "nl-tax-shared-resources/reference/extraction-boundaries.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-provisional-assessment/reference/provisional-flow.md",
        ):
            with self.subTest(file=relative):
                self.assertIn("chat YYYY-MM-DD", flat(relative))
        self.assertNotIn("chat statement", PROVISIONAL_TEMPLATE.read_text(encoding="utf-8"))

        # The provisional gap tables carry the annual columns.
        provisional = PROVISIONAL_TEMPLATE.read_text(encoding="utf-8")
        annual = ANNUAL_TEMPLATE.read_text(encoding="utf-8")
        for heading, expected in (
            ("Open questions", ["Q-ID", "Section", "Question", "Blocking", "Status"]),
            ("Missing information", ["M-ID", "Description", "Workpack row", "Q-ID", "How to resolve"]),
            ("Assumptions", ["A-ID", "Description", "Accepted by taxpayer", "Impact if incorrect", "Resolution"]),
        ):
            for text in (annual, provisional):
                header = next(
                    line for line in section(text, heading).splitlines() if line.startswith("|")
                )
                with self.subTest(section=heading, template=text[:30]):
                    self.assertEqual([cell.strip() for cell in header.strip("|").split("|")], expected)
            self.assertIn('[U:"<short quote>" (<YYYY-MM-DD>)]', section(provisional, "Assumptions"))

        # Reference numbers are never recorded.
        boundaries = flat("nl-tax-shared-resources/reference/extraction-boundaries.md")
        self.assertNotIn("policy numbers |", boundaries)
        self.assertNotIn("kenmerk: BL/12345", boundaries)
        self.assertIn("Policy, contract, or aanslag numbers", boundaries)
        self.assertIn("A provider name plus tax year identifies a document", boundaries)
        evidence = flat("nl-tax-shared-resources/reference/evidence-types.md")
        self.assertNotRegex(evidence, r"Typical fields:[^.]*polisnummer,")
        for relative in ("nl-tax-box1-home/SKILL.md", "nl-tax-winst/SKILL.md"):
            with self.subTest(file=relative):
                self.assertIn("policy, contract, or aanslag number", flat(relative))
        privacy = flat_repo("PRIVACY.md")
        self.assertIn(
            "The workpack never records a full BSN, IBAN, policy, contract, or aanslag number",
            privacy,
        )

    # Finding 8 / R13 --------------------------------------------------------

    def test_provisional_business_scope_and_baseline_readiness(self):
        checks = " ".join(section(PROVISIONAL_TEMPLATE.read_text(encoding="utf-8"), "Unsupported-case checks").split())
        self.assertIn("non-business individual or recognised IB business form", checks)
        self.assertNotIn("eenmanszaak/ZZP with an expected-profit forecast only", checks)
        self.assertNotIn("If any of the first four checks", checks)
        self.assertIn("is **not** a whole-case exclusion and does not stop this workpack", checks)
        delta = flat("nl-tax-provisional-assessment/reference/delta-rules.md")
        self.assertIn("This is a non-blocking note", delta)
        self.assertNotIn("List the unavailable baseline fields under Missing information", delta)
        change = flat("nl-tax-provisional-assessment/reference/subflows/change.md")
        self.assertNotIn("list unavailable baseline fields under `Missing information`", change)
        self.assertIn(
            "Baseline fields unavailable:",
            section(PROVISIONAL_TEMPLATE.read_text(encoding="utf-8"), "Delta summary"),
        )


class FieldMapWorkpackGraderTests(unittest.TestCase):
    ANNUAL_MAP = """```yaml
field_map_version: "1.1"
workflow: annual_return
tax_year: 2025
created_at: "2026-09-26T10:00:00Z"
updated_at: "2026-09-26T10:00:00Z"
readiness: draft
check_performed_by: checked_by_agent
fields:
  - field_id: box1.loon
    label: "Loon"
    value: 45000
    source: {type: evidence, evidence_id: ev_001}
    confidence: 0.95
    manual_review_required: false
  - field_id: box1.loonheffing
    label: "Loonheffing"
    value: 12000
    source: {type: evidence, evidence_id: ev_001}
    confidence: 0.95
    manual_review_required: false
missing_fields: []
user_chat_values_index: []
notes: []
```"""

    PROVISIONAL_WERKELIJK_MAP = """```yaml
field_map_version: "1.1"
workflow: provisional_assessment
tax_year: 2026
readiness: draft
check_performed_by: checked_by_agent
fields:
  - field_id: box3.werkelijk_rendement
    label: "Werkelijk rendement"
    value: 1200
    source: {type: estimate}
    confidence: 0.5
    manual_review_required: true
missing_fields: []
```"""

    @classmethod
    def setUpClass(cls):
        cls.validator = load_module(VALIDATOR, "validate_field_map_workpack_tests")
        cls.renderer = load_module(RENDERER, "render_field_map_workpack_tests")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def with_appendix_b(template_path, body):
        text = template_path.read_text(encoding="utf-8")
        head, marker, _ = text.partition("## Appendix B — Field map")
        assert marker
        return f"{head}{marker}\n\n{body}\n"

    def write(self, name, text):
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_tool(self, tool, *args):
        return subprocess.run(
            [sys.executable, str(tool), *map(str, args)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=60,
        )

    def test_mapped_workpack_validates_through_the_cli(self):
        path = self.write(
            "nl-tax-annual-2025-workpack.md",
            self.with_appendix_b(ANNUAL_TEMPLATE, self.ANNUAL_MAP),
        )
        result = self.run_tool(VALIDATOR, path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALIDATION PASSED", result.stdout)
        self.assertIn("READINESS: DRAFT", result.stdout)
        # A draft never passes the strict readiness gate.
        strict = self.run_tool(VALIDATOR, "--require-ready", path)
        self.assertEqual(strict.returncode, 1, strict.stdout)

    def test_unmapped_template_reports_no_field_map(self):
        for template in (ANNUAL_TEMPLATE, PROVISIONAL_TEMPLATE):
            with self.subTest(template=template.name):
                result = self.run_tool(VALIDATOR, template)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("VALIDATION FAILED", result.stdout)
                self.assertIn("no field map in workpack", result.stdout)
                self.assertIn("not yet mapped", result.stdout)
                rendered = self.run_tool(RENDERER, template)
                self.assertEqual(rendered.returncode, 1)
                self.assertIn("no field map in workpack", rendered.stderr)

    def test_policy_checks_apply_to_the_extracted_map(self):
        path = self.write(
            "nl-tax-provisional-2026-workpack.md",
            self.with_appendix_b(PROVISIONAL_TEMPLATE, self.PROVISIONAL_WERKELIJK_MAP),
        )
        result = self.run_tool(VALIDATOR, path)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("werkelijk rendement", result.stdout.lower())

    def test_renderer_renders_the_appendix_b_map(self):
        path = self.write(
            "nl-tax-annual-2025-workpack.md",
            self.with_appendix_b(ANNUAL_TEMPLATE, self.ANNUAL_MAP),
        )
        result = self.run_tool(RENDERER, path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Field Map — annual_return 2025", result.stdout)
        self.assertIn("| Loon | 45000 | evidence |", result.stdout)

    def test_extraction_rejects_malformed_appendix_b(self):
        extract = self.validator.extract_workpack_field_map
        error = self.validator.WorkpackFieldMapError
        base = ANNUAL_TEMPLATE.read_text(encoding="utf-8")
        head = base.partition("## Appendix B — Field map")[0]
        cases = {
            "missing section": head,
            "two yaml blocks": head + "## Appendix B — Field map\n\n"
            + self.ANNUAL_MAP + "\n\n" + self.ANNUAL_MAP + "\n",
            "no yaml block": head + "## Appendix B — Field map\n\nsee above\n",
            "unclosed fence": head + "## Appendix B — Field map\n\n```yaml\nworkflow: x\n",
            "duplicate section": base + "\n## Appendix B — Field map\n\nnot yet mapped\n",
        }
        for label, text in cases.items():
            with self.subTest(case=label):
                with self.assertRaises(error):
                    extract(text)

    def test_extraction_ignores_headings_and_yaml_outside_appendix_b(self):
        # Appendix A's yaml block and a "## " line inside a fence must not be
        # mistaken for the field map or a section boundary.
        body = self.ANNUAL_MAP.replace(
            "notes: []", "notes:\n  - \"## not a heading\""
        )
        text = self.with_appendix_b(ANNUAL_TEMPLATE, body)
        yaml_text, warnings = self.validator.extract_workpack_field_map(text)
        data = yaml.safe_load(yaml_text)
        self.assertEqual(data["workflow"], "annual_return")
        self.assertEqual(data["notes"], ["## not a heading"])
        self.assertEqual(warnings, [])

    def test_standalone_yaml_input_is_unchanged(self):
        path = self.write(
            "field-map.yaml",
            self.ANNUAL_MAP.removeprefix("```yaml\n").removesuffix("```"),
        )
        data, warnings = self.validator.load_field_map(str(path))
        self.assertEqual(data["tax_year"], 2025)
        self.assertEqual(warnings, [])
        self.assertEqual(self.validator.load_yaml(str(path)), data)
        errors, _ = self.validator.validate(data)
        self.assertEqual(errors, [])
        self.assertEqual(
            self.validator.CHECK_IDS,
            (
                "FM-METADATA",
                "FM-WORKFLOW-YEAR",
                "FM-STRUCTURE",
                "FM-SOURCE",
                "FM-CONFIDENCE-FINITE",
                "FM-REFERENCE-COVERAGE",
                "FM-MISSING-STRUCTURE",
                "FM-PROVISIONAL-METHOD",
            ),
        )

    def test_leftover_placeholder_next_to_a_map_is_a_warning(self):
        text = self.with_appendix_b(
            ANNUAL_TEMPLATE, "not yet mapped\n\n" + self.ANNUAL_MAP
        )
        _, warnings = self.validator.extract_workpack_field_map(text)
        self.assertTrue(any("not yet mapped" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
