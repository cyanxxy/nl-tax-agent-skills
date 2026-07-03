#!/usr/bin/env python3
"""Shape checks for the eval fixtures under skills/_shared/eval-fixtures/.

Fixtures are consumed by humans and by the offline eval harness, so they must
share one minimal schema: identifying metadata, a workflow label drawn from the
intake routing vocabulary, and explicit expectations (either an
``expected_behavior`` list or an ``acceptance_criteria`` list; both may be
present).
"""

import pathlib
import unittest

import yaml


FIXTURES_DIR = (
    pathlib.Path(__file__).resolve().parents[1]
    / "skills"
    / "_shared"
    / "eval-fixtures"
)

# Workflow labels: the intake routing vocabulary (annual_2025 plus the four
# provisional subflows), and the two non-taxpayer harness labels used by the
# security fixtures (intake boundary tests and source maintenance tests).
ALLOWED_WORKFLOWS = {
    "annual_2025",
    "provisional_2026_request",
    "provisional_2026_change",
    "provisional_2026_review",
    "provisional_2026_stopzetten",
    "intake",
    "maintenance",
}

REQUIRED_KEYS = ("fixture_id", "fixture_version", "scenario", "workflow")


def iter_fixture_paths():
    return sorted(FIXTURES_DIR.glob("*/*.yaml"))


class FixtureSchemaTests(unittest.TestCase):
    def test_fixtures_exist(self):
        self.assertTrue(iter_fixture_paths(), f"no fixtures under {FIXTURES_DIR}")

    def test_required_keys_present(self):
        for path in iter_fixture_paths():
            with self.subTest(fixture=path.name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                for key in REQUIRED_KEYS:
                    self.assertIn(key, data, f"{path} missing {key}")

    def test_workflow_label_is_known(self):
        for path in iter_fixture_paths():
            with self.subTest(fixture=path.name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertIn(
                    data.get("workflow"),
                    ALLOWED_WORKFLOWS,
                    f"{path} uses unknown workflow label {data.get('workflow')!r}",
                )

    def test_expectations_present(self):
        for path in iter_fixture_paths():
            with self.subTest(fixture=path.name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                has_behavior = bool(data.get("expected_behavior"))
                has_criteria = bool(data.get("acceptance_criteria"))
                self.assertTrue(
                    has_behavior or has_criteria,
                    f"{path} declares neither expected_behavior nor acceptance_criteria",
                )

    def test_fixture_ids_unique(self):
        # Note: fixture_id follows eval_<scope>_<slug> and is NOT required to
        # match the filename; only uniqueness is enforced.
        seen = {}
        for path in iter_fixture_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            fixture_id = data.get("fixture_id")
            self.assertNotIn(fixture_id, seen, f"duplicate fixture_id {fixture_id}")
            seen[fixture_id] = path


if __name__ == "__main__":
    unittest.main()
