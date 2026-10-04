#!/usr/bin/env python3
"""Offline eval verifier and hard-contract script for identity-scoped workpacks.

The draft-only extension workflows (VAT return, VAT correction, ICP, OSS,
international, annual 2026) write one consented file per exact identity. These
tests check that the offline verifier and the agentic hard-contract script
accept such a file only at its own path, with recorded consent, when the case
lists it, and that its source ledger follows the grader's workflow rule.
"""

import copy
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
VERIFIER_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/verify_offline_workspace.py"
DATASET_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
HARD_CONTRACTS = REPO_ROOT / "evals/nl-tax-agent-skills/agentic-workspace/.eval/verify-hard-contracts.sh"
Q1 = "workspace/nl-tax-vat-correction-2026-Q1-workpack.md"
Q2 = "workspace/nl-tax-vat-correction-2026-Q2-workpack.md"
VAT_Q3 = "workspace/nl-tax-vat-2026-Q3-workpack.md"
CORRECTION_SOURCES = ("bd_vat_corrections", "bd_vat_suppletie_explanation")
STATUSES = {
    "vat_scope": "complete",
    "vat_original": "in_progress",
    "vat_reconciliation": "not_started",
    "vat_correction_route": "not_started",
    "confirm": "not_started",
}


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


samples = load("tests/nl_tax_agent_skills/workpack_samples.py", "samples_for_offline_verifier_extended")


def correction_workpack(period, **kwargs):
    kwargs.setdefault("sources", CORRECTION_SOURCES)
    kwargs.setdefault("statuses", dict(STATUSES))
    return samples.build_workpack(
        "vat_correction",
        workflow=f"vat_correction_2026_{period}",
        documents=(("ev_001", "chat 2026-10-02", "user_chat", "2026", "taxpayer", "chat",
                    "original filed figures", "extracted"),),
        **kwargs,
    )


def write(root, relative, text):
    path = pathlib.Path(root) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@unittest.skipUnless(VERIFIER_PATH.is_file(), "offline eval verifier is repository-only")
class IdentityScopedOfflineVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verifier = load("evals/nl-tax-agent-skills/verify_offline_workspace.py", "verify_offline_extended")
        cls.dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        cls.cases = {case["id"]: case for case in cls.dataset["cases"]}
        cls.grader = samples.load_grader()

    def verify(self, root, case):
        return self.verifier.verify_case(pathlib.Path(root), self.dataset, case)

    def assertHas(self, errors, fragment):
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_dataset_mirrors_the_grader_paths_and_has_both_vat_owners(self):
        self.assertEqual(self.verifier.validate_dataset_paths(DATASET_PATH, self.dataset), [])
        templates = {
            kind: path
            for kind, path in self.grader.WORKPACK_PATHS.items()
            if kind not in {"annual", "provisional"}
        }
        self.assertEqual(self.dataset["global"]["identity_workpack_paths"], templates)
        skills = {case["skill"] for case in self.dataset["cases"]}
        self.assertTrue({"nl-tax-vat-return", "nl-tax-vat-correction"} <= skills)
        saved = self.cases["vat_correction_two_periods_saved"]
        self.assertEqual(saved["expected_files"], [Q1, Q2])
        self.assertEqual(
            {rule["workflow"] for rule in saved["workpacks"]},
            {"vat_correction_2026_Q1", "vat_correction_2026_Q2"},
        )
        self.assertEqual(self.cases["vat_return_reverse_charge_no_write"]["expected_files"],
                         ["workspace/eval/response.md"])

    def test_consented_two_period_save_passes(self):
        case = self.cases["vat_correction_two_periods_saved"]
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, Q1, correction_workpack("Q1"))
            write(tmp, Q2, correction_workpack("Q2"))
            self.assertEqual(self.verify(tmp, case), [])

    def test_save_without_recorded_consent_fails(self):
        case = self.cases["vat_correction_two_periods_saved"]
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, Q1, correction_workpack("Q1"))
            write(tmp, Q2, correction_workpack("Q2", save_consent="not_given"))
            errors = self.verify(tmp, case)
        self.assertHas(errors, "save_consent")

    def test_period_file_holding_another_period_fails(self):
        case = self.cases["vat_correction_two_periods_saved"]
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, Q1, correction_workpack("Q1"))
            write(tmp, Q2, correction_workpack("Q1"))
            errors = self.verify(tmp, case)
        self.assertHas(errors, "filename must match")
        self.assertHas(errors, "Appendix A workflow 'vat_correction_2026_Q1' != 'vat_correction_2026_Q2'")

    def test_period_file_naming_the_other_period_fails(self):
        case = self.cases["vat_correction_two_periods_saved"]
        crossed = correction_workpack("Q1").replace(
            "## Assumptions\n", f"## Assumptions\n\nQ2 lives in {Q2}\n", 1
        )
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, Q1, crossed)
            write(tmp, Q2, correction_workpack("Q2"))
            errors = self.verify(tmp, case)
        self.assertHas(errors, "mentions another vat_correction workpack path")

    def test_unlisted_or_combined_identity_files_fail(self):
        case = self.cases["vat_correction_two_periods_saved"]
        layouts = {
            VAT_Q3: "workpack written without this case's save consent",
            "workspace/nl-tax-vat-correction-2026-Y-workpack.md": "without this case's save consent",
            "workspace/nl-tax-vat-correction-2026-Q1-Q2-workpack.md": "workpack copy or variant",
            "workspace/nl-tax-vat-correction-2026-Q1-workpack-v2.md": "workpack copy or variant",
            "nl-tax-vat-correction-2026-Q1-workpack.md": "workpack copy outside workspace/",
        }
        for relative, fragment in layouts.items():
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as tmp:
                write(tmp, Q1, correction_workpack("Q1"))
                write(tmp, Q2, correction_workpack("Q2"))
                write(tmp, relative, "x\n")
                self.assertHas(self.verify(tmp, case), fragment)

    def test_no_write_vat_case_rejects_any_vat_file(self):
        case = self.cases["vat_return_reverse_charge_no_write"]
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "workspace/eval/response.md", "Prepared in chat only.\n")
            self.assertEqual(self.verify(tmp, case), [])
            write(tmp, VAT_Q3, samples.build_workpack("vat", sources=()))
            errors = self.verify(tmp, case)
        self.assertHas(errors, f"workpack written without this case's save consent: {VAT_Q3}")

    def test_unexpected_file_message_names_the_case_paths(self):
        case = self.cases["vat_correction_two_periods_saved"]
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, Q1, correction_workpack("Q1"))
            write(tmp, Q2, correction_workpack("Q2"))
            write(tmp, "workspace/field-map.yaml", "x\n")
            errors = self.verify(tmp, case)
        self.assertHas(errors, "the plugin may write only the case's consented workpack path(s)")
        self.assertHas(errors, Q1)

    def test_source_ledger_uses_the_grader_workflow_rule(self):
        case = self.cases["vat_correction_two_periods_saved"]
        for sources in (
            CORRECTION_SOURCES + ("bd_provisional_request_2026",),
            CORRECTION_SOURCES + ("bd_box1_rates_2025",),
        ):
            with self.subTest(sources=sources), tempfile.TemporaryDirectory() as tmp:
                write(tmp, Q1, correction_workpack("Q1", sources=sources))
                write(tmp, Q2, correction_workpack("Q2"))
                self.assertHas(self.verify(tmp, case), "cross-workflow union")

    def test_dataset_rejects_misplaced_or_undeclared_identity_paths(self):
        dataset = copy.deepcopy(self.dataset)
        case = next(c for c in dataset["cases"] if c["id"] == "vat_correction_two_periods_saved")
        case["workpacks"][0]["workflow"] = "vat_correction_2026_Q2"
        errors = self.verifier.validate_dataset_paths(DATASET_PATH, dataset)
        self.assertHas(errors, f"vat_correction_2026_Q2 belongs in {Q2}, not {Q1}")

        dataset = copy.deepcopy(self.dataset)
        case = next(c for c in dataset["cases"] if c["id"] == "vat_correction_two_periods_saved")
        case["expected_files"] = [Q1]
        errors = self.verifier.validate_dataset_paths(DATASET_PATH, dataset)
        self.assertHas(errors, f"workpack rule path '{Q2}' is not an expected file")

        dataset = copy.deepcopy(self.dataset)
        case = next(c for c in dataset["cases"] if c["id"] == "vat_correction_two_periods_saved")
        case["workpacks"][1]["presentation"] = "chat"
        errors = self.verifier.validate_dataset_paths(DATASET_PATH, dataset)
        self.assertHas(errors, "is a saved file, not a conversation rendering")

        dataset = copy.deepcopy(self.dataset)
        dataset["global"]["identity_workpack_paths"].pop("oss")
        errors = self.verifier.validate_dataset_paths(DATASET_PATH, dataset)
        self.assertHas(errors, "identity_workpack_paths must mirror")

    def test_grader_kinds_are_used_for_rules(self):
        for workflow, kind in (
            ("vat_2026_Q3", "vat"),
            ("vat_correction_2025_Y", "vat_correction"),
            ("icp_2026_M09", "icp"),
            ("oss_ioss_2026_M09", "oss"),
            ("international_2025_migration", "international"),
            ("annual_2026", "annual_2026"),
            ("annual_2025", "annual"),
            ("provisional_2026_review", "provisional"),
        ):
            with self.subTest(workflow=workflow):
                self.assertEqual(self.verifier._kind_for_workflow(workflow), kind)
        self.assertIsNone(self.verifier._kind_for_workflow("oss_ioss_2026_Q3"))


class IdentityScopedHardContractTests(unittest.TestCase):
    def run_script(self, root):
        return subprocess.run(["bash", str(HARD_CONTRACTS)], cwd=root, capture_output=True, text=True)

    def test_consented_identity_files_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, Q1, correction_workpack("Q1"))
            write(tmp, Q2, correction_workpack("Q2"))
            write(tmp, VAT_Q3, samples.build_workpack("vat", sources=()))
            result = self.run_script(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_identity_files_need_consent_own_workflow_and_no_cross_names(self):
        invalid = {
            "no consent": {Q1: correction_workpack("Q1", save_consent="not_given")},
            "wrong period in record": {Q1: correction_workpack("Q2")},
            "names the other period": {
                Q1: correction_workpack("Q1").replace(
                    "## Assumptions\n", f"## Assumptions\n\nSee {Q2}\n", 1
                )
            },
            "combined periods": {"workspace/nl-tax-vat-correction-2026-Q1-Q2-workpack.md": "x\n"},
            "unsupported year": {"workspace/nl-tax-vat-2024-Q3-workpack.md": "x\n"},
            "ioss quarter": {"workspace/nl-tax-oss-ioss-2026-Q3-workpack.md": "x\n"},
            "copy outside workspace": {"nl-tax-vat-2026-Q3-workpack.md": "x\n"},
        }
        for label, files in invalid.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                for relative, text in files.items():
                    write(tmp, relative, text)
                result = self.run_script(tmp)
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_annual_still_never_names_the_provisional_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(
                tmp,
                "workspace/nl-tax-annual-2025-workpack.md",
                samples.build_workpack("annual").replace(
                    "## Assumptions\n",
                    "## Assumptions\n\nSee workspace/nl-tax-provisional-2026-workpack.md\n",
                    1,
                ),
            )
            self.assertNotEqual(self.run_script(tmp).returncode, 0)


if __name__ == "__main__":
    unittest.main()
