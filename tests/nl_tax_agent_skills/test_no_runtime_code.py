#!/usr/bin/env python3
"""The installed plugin ships no executable code and pre-approves no shell.

Every runtime check is an agent checklist. The former optional helpers live
under tools/ as repository graders, next to the field-map validator.
"""

import pathlib
import re
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
TOOLS_ROOT = REPO_ROOT / "tools" / "nl_tax_agent_skills"

REPOSITORY_GRADERS = {
    "box1_home/validate_own_home_inputs.py",
    "box2/calculate_box2_tax.py",
    "box3/compare_box3_annual_2025.py",
    "box3/summarize_box3_provisional_2026.py",
    "evidence_indexer/index_evidence.py",
    "field_mapper/render_field_map.py",
    "field_mapper/validate_field_map.py",
    "partner_deductions/validate_allocation.py",
}

EXECUTABLE_SUFFIXES = {".py", ".sh", ".bash", ".js", ".mjs", ".ts", ".rb", ".pl"}


def skill_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}


class NoRuntimeCodeContractTests(unittest.TestCase):
    def test_plugin_ships_no_executable_code(self):
        shipped = sorted(
            str(path.relative_to(PLUGIN_ROOT))
            for path in PLUGIN_ROOT.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix in EXECUTABLE_SUFFIXES
        )
        self.assertEqual(shipped, [])
        self.assertEqual(list(SKILLS_ROOT.glob("*/scripts")), [])

    def test_former_helpers_are_repository_graders(self):
        for relative in sorted(REPOSITORY_GRADERS):
            with self.subTest(relative=relative):
                self.assertTrue((TOOLS_ROOT / relative).is_file())

    def test_developer_source_tools_are_not_runtime_scripts(self):
        source_tools = TOOLS_ROOT / "source_maintenance" / "scripts"
        scripts = {path.name for path in source_tools.glob("*.py")}
        self.assertEqual(len(scripts), 7)
        self.assertIn("build_runtime_projections.py", scripts)
        self.assertFalse((SKILLS_ROOT / "nl-tax-source-refresh").exists())

    def test_skills_pre_approve_no_shell_and_only_workspace_writes(self):
        for skill in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            tools = skill_frontmatter(skill).get("allowed-tools") or []
            with self.subTest(skill=skill.parent.name):
                for tool in tools:
                    self.assertFalse(tool.startswith("Bash"), tool)
                    if tool.split("(")[0] in {"Write", "Edit"}:
                        self.assertEqual(tool.split("(")[1:], ["./workspace/**)"])

    def test_runtime_docs_run_no_code(self):
        shipped = "\n".join(
            path.read_text(encoding="utf-8")
            for path in PLUGIN_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}
        )
        for phrase in ("python3 ", "scripts/", "checked_by_script"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, shipped)
        contract = (
            SKILLS_ROOT / "nl-tax-shared-resources" / "runtime-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("The plugin ships no scripts and needs no shell or Python", contract)

    def test_retired_heuristics_have_no_runtime_references(self):
        retired = {
            "summarize_" + "box1_inputs.py",
            "summarize_" + "box2_inputs.py",
            "validate_" + "box2_inputs.py",
            "classify_" + "box3_assets.py",
            "fetch_" + "sources.py",
        }
        shipped = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILLS_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}
        )
        for name in retired:
            with self.subTest(name=name):
                self.assertNotIn(name, shipped)

    def test_readme_names_no_bundled_image_paths(self):
        # The directory scan holds a plugin whose README names bundled images
        # outside Markdown image syntax (UNREAD_ASSET_REFERENCED).
        readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotRegex(readme, r"\b[\w/.-]+\.(png|jpe?g|gif|webp|svg)\b")

    def test_shared_templates_record_an_agent_check(self):
        templates = (
            "skills/nl-tax-evidence-indexer/templates/evidence-index.yaml",
            "skills/nl-tax-field-mapper/templates/field-map-template.yaml",
        )
        for relative in templates:
            data = yaml.safe_load((PLUGIN_ROOT / relative).read_text(encoding="utf-8"))
            with self.subTest(relative=relative):
                self.assertEqual(data["check_performed_by"], "checked_by_agent")


if __name__ == "__main__":
    unittest.main()
