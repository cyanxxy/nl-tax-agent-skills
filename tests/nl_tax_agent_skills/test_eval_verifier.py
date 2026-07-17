#!/usr/bin/env python3
"""Tests for the agentic benchmark and offline structural contracts."""

import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

# The offline eval verifier lives in the dev repo under evals/ but is not part of
# the shipped plugin package.
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
    def _release_eval_surfaces(self):
        dataset_path = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
        benchmark_path = (
            REPO_ROOT / "evals/nl-tax-agent-skills/plugin-eval-benchmark.json"
        )
        dataset = yaml.safe_load(dataset_path.read_text(encoding="utf-8"))
        benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))

        dataset_ids = {case["id"] for case in dataset["cases"]}
        contract_ids = set(dataset["contract_default_cases"])
        return dataset_ids, contract_ids, benchmark

    def test_dataset_and_default_case_sets_are_equal(self):
        dataset_ids, contract_ids, _ = self._release_eval_surfaces()
        self.assertEqual(contract_ids, dataset_ids)

    def test_agentic_benchmark_is_not_coupled_to_contract_fixtures(self):
        _, _, benchmark = self._release_eval_surfaces()
        scenarios = benchmark["scenarios"]
        self.assertEqual(len(scenarios), 5)
        self.assertTrue(all("datasetCaseId" not in scenario for scenario in scenarios))

        rendered_prompts = "\n".join(
            scenario["userInput"].lower() for scenario in scenarios
        )
        for forbidden in (
            "fixture",
            "current-case",
            "dataset case",
            "exact case",
            "expected file",
            "run offline",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, rendered_prompts)

        self.assertEqual(
            {scenario["rubricProfile"] for scenario in scenarios},
            {
                "informational",
                "annual_preparation",
                "provisional_change",
                "entrepreneur_winst",
                "unsupported_boundary",
            },
        )

    def test_behavioral_fixture_cases_are_wired_into_dataset(self):
        dataset_path = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
        dataset = yaml.safe_load(dataset_path.read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in dataset["cases"]}
        expected = {
            "annual_casual_informational_tax": "evals/nl-tax-agent-skills/fixtures/annual/casual-informational-tax.yaml",
            "annual_explicit_preparation": "evals/nl-tax-agent-skills/fixtures/annual/explicit-preparation.yaml",
            "annual_winst_resume": "evals/nl-tax-agent-skills/fixtures/annual/winst-resume.yaml",
            "annual_corrected_tax_behavior": "evals/nl-tax-agent-skills/fixtures/annual/corrected-tax-behavior.yaml",
            "annual_entrepreneur_zzp": "evals/nl-tax-agent-skills/fixtures/annual/entrepreneur-zzp.yaml",
            "provisional_entrepreneur_profit": "evals/nl-tax-agent-skills/fixtures/provisional/entrepreneur-profit.yaml",
            "annual_evidence_status": "evals/nl-tax-agent-skills/fixtures/annual/evidence-status.yaml",
        }

        self.assertTrue(expected.keys() <= cases.keys())
        for case_id, fixture in expected.items():
            with self.subTest(case_id=case_id):
                self.assertEqual(cases[case_id]["fixture"], fixture)

        entrepreneur = cases["annual_entrepreneur_zzp"]
        entrepreneur_map = next(
            rule
            for rule in entrepreneur["text_checks"]
            if rule["path"] == "workspace/annual/2025/field-map.yaml"
        )
        self.assertIn("readiness: draft", entrepreneur_map["all"])
        self.assertIn("business-section schema review", entrepreneur_map["all"])
        filing_ready_business_ids = {
            "onderneming.belastbare_winst",
            "onderneming.zelfstandigenaftrek",
            "onderneming.startersaftrek",
            "onderneming.ondernemersaftrek_totaal",
            "onderneming.mkb_winstvrijstelling",
            "onderneming.kleinschaligheidsinvesteringsaftrek",
        }
        self.assertTrue(
            filing_ready_business_ids <= set(entrepreneur_map["none"])
        )

        provisional = cases["provisional_entrepreneur_profit"]
        provisional_map = next(
            rule
            for rule in provisional["text_checks"]
            if rule["path"] == "workspace/provisional/2026/field-map.yaml"
        )
        self.assertIn("onderneming.geschatte_winst", provisional_map["all"])
        for forbidden in ("zelfstandigenaftrek", "MKB-winstvrijstelling", "Zvw", "final tax"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, provisional_map["none"])

        evidence = cases["annual_evidence_status"]
        self.assertNotIn(
            "text_checks",
            evidence,
            "agent interpretation belongs in fixtures/rubrics, not exact Markdown checks",
        )

    def test_omitted_shipped_fixtures_are_wired_without_replacing_security_fixture(self):
        dataset_path = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
        dataset = yaml.safe_load(dataset_path.read_text(encoding="utf-8"))
        fixtures = {case["id"]: case["fixture"] for case in dataset["cases"]}

        self.assertEqual(
            fixtures.get("provisional_stopzetten_payment_redirect"),
            "evals/nl-tax-agent-skills/fixtures/provisional/stopzetten-payment-redirect.yaml",
        )
        self.assertEqual(
            fixtures.get("security_source_staleness"),
            "evals/nl-tax-agent-skills/fixtures/security/source-staleness.yaml",
        )

        security_fixture = (
            REPO_ROOT
            / "evals/nl-tax-agent-skills/fixtures/security/source-staleness.yaml"
        )
        self.assertEqual(
            hashlib.sha256(security_fixture.read_bytes()).hexdigest(),
            "d71500efb2dc18db9490bf0ba30ef4cd21e222c8477c4b4f0f4d496b56a520b7",
        )

    def test_first_party_cowork_cases_use_native_prose_format(self):
        case_names = {
            "cowork-casual-tax-question",
            "cowork-explicit-annual-preparation",
            "cowork-annual-entrepreneur-boundary",
            "cowork-provisional-change",
            "cowork-unsupported-boundary",
            "cowork-natural-language-checklist",
            "cowork-refuse-portal-control",
            "cowork-corrected-tax-rules",
            "cowork-provisional-entrepreneur-profit",
            "cowork-dual-workflow-handoff",
        }
        eval_root = REPO_ROOT / "evals/claude"
        actual_case_names = {
            path.parent.name
            for path in eval_root.glob("cowork-*/prompt.md")
            if (path.parent / "graders/criteria.md").is_file()
        }
        self.assertEqual(actual_case_names, case_names)

        for case_name in case_names:
            with self.subTest(case=case_name):
                prompt = eval_root / case_name / "prompt.md"
                criteria = eval_root / case_name / "graders/criteria.md"
                self.assertTrue(prompt.is_file(), prompt)
                self.assertTrue(criteria.is_file(), criteria)
                self.assertIn('schema_version: "1.1"', prompt.read_text(encoding="utf-8"))
                self.assertIn("type: llm", criteria.read_text(encoding="utf-8"))

    def test_benchmark_contains_tax_specific_copy_only(self):
        benchmark_path = REPO_ROOT / "evals/nl-tax-agent-skills/plugin-eval-benchmark.json"
        benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
        rendered = json.dumps(benchmark)

        self.assertEqual(len(benchmark["scenarios"]), 5)
        self.assertEqual(
            benchmark["workspace"]["sourcePath"],
            "evals/nl-tax-agent-skills/agentic-workspace",
        )
        self.assertEqual(
            benchmark["verifiers"]["commands"],
            ["bash .eval/verify-hard-contracts.sh"],
        )
        workspace_seed = REPO_ROOT / benchmark["workspace"]["sourcePath"]
        self.assertTrue(
            (workspace_seed / ".eval/verify-hard-contracts.sh").is_file()
        )
        self.assertIn("Dutch tax", rendered)

    def test_agentic_rubric_is_weighted_and_allows_valid_variation(self):
        rubric_path = REPO_ROOT / "evals/nl-tax-agent-skills/agentic-rubric.json"
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))

        self.assertEqual(
            sum(dimension["weight"] for dimension in rubric["dimensions"]),
            100,
        )
        self.assertEqual(rubric["passThresholdPercent"], 80)
        self.assertGreaterEqual(len(rubric["hardFails"]), 4)
        instructions = " ".join(rubric["reviewInstructions"]).lower()
        self.assertIn("different wording", instructions)
        self.assertIn("do not require a case marker", instructions)

    def test_structural_dataset_contains_no_model_prompts_or_case_markers(self):
        dataset_path = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
        dataset = yaml.safe_load(dataset_path.read_text(encoding="utf-8"))

        self.assertNotIn("case_marker", dataset["global"])
        for case in dataset["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn("prompt", case)
                self.assertNotIn(
                    "workspace/eval/current-case.txt",
                    case.get("expected_files", []),
                )
                for rule in case.get("text_checks", []):
                    self.assertTrue(
                        rule["path"].endswith(".yaml"),
                        "structural contracts must not prescribe Markdown prose",
                    )

    def test_agentic_metric_pack_is_schema_compatible(self):
        root = REPO_ROOT / "evals/nl-tax-agent-skills"
        manifest = json.loads(
            (root / "agentic-metric-pack/manifest.json").read_text(encoding="utf-8")
        )

        self.assertEqual(manifest["supportedTargetKinds"], ["plugin"])
        self.assertEqual(
            manifest["command"], ["node", "./emit-agentic-design.js"]
        )

        node = shutil.which("node")
        if node is None:
            self.skipTest("Node is unavailable; metric-pack execution was not checked")
        emitted = subprocess.run(
            [node, str(root / "agentic-metric-pack/emit-agentic-design.js")],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(emitted.stdout)
        checks = result["checks"]
        self.assertEqual(len(checks), 5)
        self.assertTrue(all(check["status"] == "pass" for check in checks))

    def test_agentic_shell_verifier_checks_only_hard_artifact_boundaries(self):
        script = (
            REPO_ROOT
            / "evals/nl-tax-agent-skills/agentic-workspace/.eval/verify-hard-contracts.sh"
        )

        with tempfile.TemporaryDirectory() as tmp:
            clean = subprocess.run(
                ["bash", str(script)], cwd=tmp, capture_output=True, text=True
            )
            self.assertEqual(clean.returncode, 0, clean.stderr)

        invalid_layouts = {
            "case marker": ["workspace/eval/current-case.txt"],
            "mixed workflows": [
                "workspace/annual/2025/return-pack.md",
                "workspace/provisional/2026/provisional-pack.md",
            ],
            "noncanonical map": ["workspace/shared/field-map.yaml"],
            "helper-owned note": ["workspace/shared/box2-notes.md"],
        }
        for label, relative_paths in invalid_layouts.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                for relative_path in relative_paths:
                    path = root / relative_path
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("test\n", encoding="utf-8")
                result = subprocess.run(
                    ["bash", str(script)],
                    cwd=root,
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(result.returncode, 0, result.stdout)

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

    def test_offline_verifier_enforces_workflow_scoped_source_ledgers(self):
        verifier = load_module(
            "evals/nl-tax-agent-skills/verify_offline_workspace.py",
            "verify_offline_workspace_source_ledgers",
        )
        case = {
            "id": "dual_sources",
            "source_ledger_check": {
                "session_path": "workspace/shared/session-progress.yaml",
                "workpacks": [
                    {
                        "workflow": "annual_2025",
                        "path": "workspace/annual/2025/return-pack.md",
                    },
                    {
                        "workflow": "provisional_2026",
                        "path": "workspace/provisional/2026/provisional-pack.md",
                    },
                ],
            },
        }

        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp)
            session_path = workspace / "workspace/shared/session-progress.yaml"
            annual_path = workspace / "workspace/annual/2025/return-pack.md"
            provisional_path = (
                workspace / "workspace/provisional/2026/provisional-pack.md"
            )
            for path in (session_path, annual_path, provisional_path):
                path.parent.mkdir(parents=True, exist_ok=True)

            session_path.write_text(
                "\n".join(
                    [
                        "active_workflow: provisional_2026_request",
                        "sources_loaded: [provisional_source_id]",
                        "sources_loaded_by_workflow:",
                        "  annual_2025: [annual_source_id]",
                        "  provisional_2026: [provisional_source_id]",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            annual_path.write_text(
                "# Annual\n\n## Sources used\n\n- annual_source_id\n\n## Next\n",
                encoding="utf-8",
            )
            provisional_path.write_text(
                "# Provisional\n\n## Sources used\n\n- provisional_source_id\n\n## Next\n",
                encoding="utf-8",
            )

            self.assertEqual(verifier.verify_case(workspace, {}, case), [])

            session_path.write_text(
                session_path.read_text(encoding="utf-8").replace(
                    "sources_loaded: [provisional_source_id]",
                    "sources_loaded: [annual_source_id, provisional_source_id]",
                ),
                encoding="utf-8",
            )
            provisional_path.write_text(
                "# Provisional\n\n## Sources used\n\n"
                "- annual_source_id\n- provisional_source_id\n\n## Next\n",
                encoding="utf-8",
            )
            errors = verifier.verify_case(workspace, {}, case)

        self.assertTrue(any("must exactly mirror" in error for error in errors), errors)
        self.assertTrue(any("Sources used" in error for error in errors), errors)

    def test_new_cowork_graders_cover_handoff_and_generation_gates(self):
        eval_root = REPO_ROOT / "evals/claude"
        dual_prompt = (
            eval_root / "cowork-dual-workflow-handoff/prompt.md"
        ).read_text(encoding="utf-8")
        dual_criteria = (
            eval_root / "cowork-dual-workflow-handoff/graders/criteria.md"
        ).read_text(encoding="utf-8")
        dual_criteria_flat = " ".join(dual_criteria.split())
        entrepreneur_criteria = (
            eval_root
            / "cowork-provisional-entrepreneur-profit/graders/criteria.md"
        ).read_text(encoding="utf-8")

        self.assertIn("prepare both", dual_prompt.lower())
        for required in (
            "sole owning workflow",
            "queued intent",
            "without a new activation phrase",
            "must not authorize provisional generation",
            "own immediate, contextual confirmation",
        ):
            with self.subTest(required=required):
                self.assertIn(required, dual_criteria_flat)
        self.assertIn("not final-generation consent", entrepreneur_criteria)
        self.assertIn("must not claim", entrepreneur_criteria)
        self.assertIn("immediate, scoped natural-language confirmation", entrepreneur_criteria)


if __name__ == "__main__":
    unittest.main()
