#!/usr/bin/env python3
"""0.4 conversation-first contracts (docs/maintainers/0.4-conversation-first-design.md).

Covers:
    - R3 write boundary: only the workpack writers carry
      ``Edit(./workspace/**)``; nothing lists Bash or Write; intake, knowledge,
      and the background helpers have no Edit rule.
    - R1/R8/R10: retired 0.3 runtime files are gone.
    - R4/R5/R7: both workpack templates carry the required headings in order,
      a parseable Appendix A resume record with the exact keys, and the
      ``not yet mapped`` / ``not requested`` placeholders.
    - R7 grader: validate_field_map.py / render_field_map.py accept a ``.md``
      workpack (Appendix B) and reject one that is ``not yet mapped``.
    - Review amendments: templates default ``save_consent`` to ``not_given``
      (A1), carry the grader's STALE line (A10), and keep the gap-table
      columns (A9).
"""

import importlib.util
import json
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

WRITERS = {
    "nl-tax-annual-return",
    "nl-tax-provisional-assessment",
    "nl-tax-field-mapper",
    "nl-tax-submit-companion",
    "nl-tax-vat-return",
    "nl-tax-vat-correction",
    "nl-tax-annual-return-2026",
    "nl-tax-icp",
    "nl-tax-oss",
    "nl-tax-international-return",

}
NON_WRITERS = {
    "nl-tax-intake",
    "nl-tax-knowledge",
    "nl-tax-box1-home",
    "nl-tax-box2",
    "nl-tax-box3",
    "nl-tax-partner-deductions",
    "nl-tax-winst",
    "nl-tax-vat-adjustments",
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


class SkillWriteBoundaryTests(unittest.TestCase):
    def test_skill_set_is_eleven_skills_plus_shared_resources(self):
        names = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(names, WRITERS | NON_WRITERS | {"nl-tax-shared-resources"})
        self.assertEqual(len(WRITERS | NON_WRITERS), 18)

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


class LegacyArtifactTests(unittest.TestCase):
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

    def test_resume_records_have_exact_r5_keys(self):
        release_version = json.loads(
            (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )["version"]
        for text, workflow, year, keys in (
            (self.annual, "annual_2025", 2025, ANNUAL_SECTION_KEYS),
            (self.provisional, "provisional_2026_request", 2026, PROVISIONAL_SECTION_KEYS),
        ):
            record = resume_record(text)
            with self.subTest(workflow=workflow):
                self.assertEqual(list(record), RESUME_RECORD_KEYS)
                self.assertEqual(record["workpack_format"], "nl-tax-workpack")
                self.assertEqual(record["workpack_version"], "2.0")
                self.assertEqual(record["plugin_version"], release_version)
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


class ReviewAmendmentTests(unittest.TestCase):
    """Binding review amendments A1-A12 of the 0.4 design."""

    # A1 ---------------------------------------------------------------------

    def test_templates_default_save_consent_to_not_given(self):
        for template in (ANNUAL_TEMPLATE, PROVISIONAL_TEMPLATE):
            text = template.read_text(encoding="utf-8")
            with self.subTest(template=template.name):
                self.assertEqual(resume_record(text)["save_consent"], "not_given")
                self.assertNotRegex(text, r"(?m)^save_consent:\s*given\b")

    # A10 --------------------------------------------------------------------

    def test_changed_fact_marks_map_and_checklist_stale(self):
        for template in (ANNUAL_TEMPLATE, PROVISIONAL_TEMPLATE):
            with self.subTest(template=template.name):
                self.assertIn(
                    "STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate before use.",
                    " ".join(section(template.read_text(encoding="utf-8"), "Field map summary").split()),
                )

    # A9 ---------------------------------------------------------------------

    def test_ids_chat_rows_and_identifier_rules_are_consistent(self):
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
