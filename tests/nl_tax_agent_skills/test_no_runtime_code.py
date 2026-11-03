#!/usr/bin/env python3
"""The installed plugin ships no executable code and pre-approves no shell.

Every runtime check is an agent checklist. Repository-only graders and source
maintenance scripts live under tools/ and are never installed.
"""

import pathlib
import re
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
SKILLS_ROOT = PLUGIN_ROOT / "skills"

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

    def test_skills_pre_approve_no_shell_and_only_workspace_writes(self):
        for skill in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            tools = skill_frontmatter(skill).get("allowed-tools") or []
            with self.subTest(skill=skill.parent.name):
                for tool in tools:
                    self.assertFalse(tool.startswith("Bash"), tool)
                    # Claude Code never consults Write(path) rules; Edit rules
                    # cover every built-in tool that creates or changes files.
                    self.assertFalse(tool.startswith("Write"), tool)
                    if tool.startswith("Edit"):
                        self.assertEqual(tool, "Edit(./workspace/**)")

    def test_readme_names_no_bundled_image_paths(self):
        # The directory scan holds a plugin whose README names bundled images
        # outside Markdown image syntax (UNREAD_ASSET_REFERENCED).
        readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotRegex(readme, r"\b[\w/.-]+\.(png|jpe?g|gif|webp|svg)\b")

    def test_shared_templates_record_an_agent_check(self):
        templates = ("skills/nl-tax-field-mapper/templates/field-map-template.yaml",)
        for relative in templates:
            data = yaml.safe_load((PLUGIN_ROOT / relative).read_text(encoding="utf-8"))
            with self.subTest(relative=relative):
                self.assertEqual(data["check_performed_by"], "checked_by_agent")

if __name__ == "__main__":
    unittest.main()
