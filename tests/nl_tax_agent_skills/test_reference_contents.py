"""Long workflow references keep a Contents list that matches their headings.

The runtime contract tells agents to find a section through a file's Contents
list and read that section in full, so a list that drifts from the headings
hides a section. Hash-pinned reviewed knowledge notes, output templates, and
generated source projections are excluded: their bytes are fixed by review or
by a generator.
"""

import pathlib
import re
import unittest


SKILLS = pathlib.Path(__file__).resolve().parents[2] / "plugins/nl-tax-agent-skills/skills"
LONG_FILE_LINES = 100
EXCLUDED_PARTS = {"knowledge", "templates", "source-projections"}
CONTENTS_HEADINGS = {"## Contents", "## Table of contents"}


def reference_files():
    for path in sorted(SKILLS.rglob("*.md")):
        if path.name == "SKILL.md" or EXCLUDED_PARTS & set(path.relative_to(SKILLS).parts):
            continue
        yield path


def headings(lines, level):
    marker = "#" * level + " "
    found, fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence and line.startswith(marker):
            found.append(line[len(marker):].strip())
    return found


def contents_entries(lines):
    """Return (level, entries) for the file's Contents list, or (None, None)."""
    for index, line in enumerate(lines):
        if line.strip() in CONTENTS_HEADINGS or line.strip() == "Contents:":
            level = 2 if line.startswith("## ") else 3
            entries = []
            for item in lines[index + 1:]:
                if item.startswith("- "):
                    entries.append(item[2:].strip())
                elif entries and not item.strip():
                    break
                elif item.strip():
                    break
            return level, entries
    return None, None


class ReferenceContentsTests(unittest.TestCase):
    def test_long_references_have_a_contents_list_matching_their_headings(self):
        checked = 0
        for path in reference_files():
            lines = path.read_text(encoding="utf-8").split("\n")
            if len(lines) <= LONG_FILE_LINES:
                continue
            checked += 1
            with self.subTest(file=str(path.relative_to(SKILLS))):
                level, entries = contents_entries(lines)
                self.assertIsNotNone(level, "missing Contents list")
                expected = [
                    heading
                    for heading in headings(lines, level)
                    if heading not in {"Contents", "Table of contents"}
                ]
                self.assertEqual(entries, expected)
        self.assertGreaterEqual(checked, 40)


if __name__ == "__main__":
    unittest.main()
