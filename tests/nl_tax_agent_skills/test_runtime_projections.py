#!/usr/bin/env python3
"""Lossless-projection contracts for reviewed portal-flow source notes."""

import hashlib
import importlib.util
import pathlib
import sys
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
PLUGIN = REPO / "plugins/nl-tax-agent-skills"
BUILDER_PATH = (
    REPO
    / "tools/nl_tax_agent_skills/source_maintenance/scripts/build_runtime_projections.py"
)


def load_builder():
    spec = importlib.util.spec_from_file_location("runtime_projection_builder", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RuntimeProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_builder()

    def test_checked_in_projections_are_current_and_lossless(self):
        for config in self.builder.PROJECTIONS:
            source = self.builder.KNOWLEDGE / config.source_name
            projection = self.builder.OUTPUT / config.output_name
            source_text = source.read_text(encoding="utf-8")
            projected_text = projection.read_text(encoding="utf-8")
            with self.subTest(projection=config.output_name):
                self.assertEqual(projected_text, self.builder.render_projection(config))
                projected_body = projected_text[projected_text.index("## Rule\n") :]
                self.assertEqual(
                    self.builder.strip_human_subjects(projected_body),
                    self.builder.reviewed_body(source_text, source),
                )
                self.assertIn(
                    hashlib.sha256(source.read_bytes()).hexdigest(),
                    projected_text,
                )
                self.assertNotIn("review_status:", projected_text)

    def test_projection_builder_targets_only_the_runtime_projection_directory(self):
        expected = {
            "request-flow-human.md",
            "change-flow-human.md",
            "stopzetten-flow-human.md",
        }
        self.assertEqual(
            {config.output_name for config in self.builder.PROJECTIONS},
            expected,
        )
        self.assertEqual(
            self.builder.OUTPUT,
            PLUGIN
            / "skills/nl-tax-provisional-assessment/reference/source-projections",
        )


if __name__ == "__main__":
    unittest.main()
