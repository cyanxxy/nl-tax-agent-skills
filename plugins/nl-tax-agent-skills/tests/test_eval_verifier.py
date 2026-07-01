#!/usr/bin/env python3
"""Tests for offline benchmark workspace verification."""

import importlib.util
import pathlib
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]

# The offline eval verifier lives in the dev repo under evals/ but is not part of
# the shipped plugin package. When this test module runs from a standalone plugin
# copy, evals/ is absent — skip rather than error on the missing file.
VERIFIER_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/verify_offline_workspace.py"


def load_module(relative_path, name):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(
    VERIFIER_PATH.is_file(),
    f"offline eval verifier not present ({VERIFIER_PATH}) — standalone package run",
)
class OfflineVerifierTests(unittest.TestCase):
    def test_offline_verifier_validates_generated_field_maps(self):
        verifier = load_module(
            "evals/nl-tax-agent-skills/verify_offline_workspace.py",
            "verify_offline_workspace_field_maps",
        )

        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp)
            field_map = workspace / "workspace/annual/2025/field-map.yaml"
            field_map.parent.mkdir(parents=True)
            field_map.write_text(
                "\n".join(
                    [
                        'field_map_version: "1.1"',
                        "workflow: annual_return",
                        "tax_year: 2026",
                        "fields:",
                        "  - field_id: personal.naam",
                        "    label: Naam",
                        "    source:",
                        "      type: baseline",
                        "    confidence: 0.9",
                        "    manual_review_required: false",
                        "missing_fields:",
                        "  - field_id: personal.bsn",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            errors = verifier.verify_case(
                workspace,
                {"global": {"plugin_root": "plugins/nl-tax-agent-skills"}},
                {
                    "id": "annual_bad_year",
                    "expected_files": ["workspace/annual/2025/field-map.yaml"],
                },
            )

        self.assertTrue(
            any("field-map validation failed" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("Unsupported workflow/tax_year combination" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
