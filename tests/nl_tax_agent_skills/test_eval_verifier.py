#!/usr/bin/env python3
"""Tests for the agentic benchmark and the 0.4 offline structural contracts."""

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
HERE = pathlib.Path(__file__).resolve().parent

# The offline eval verifier lives in the dev repo under evals/ but is not part of
# the shipped plugin package.
VERIFIER_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/verify_offline_workspace.py"
DATASET_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
ANNUAL = "workspace/nl-tax-annual-2025-workpack.md"
PROVISIONAL = "workspace/nl-tax-provisional-2026-workpack.md"
LEGACY_TREES = (
    "workspace/taxpayer/**",
    "workspace/shared/**",
    "workspace/annual/**",
    "workspace/provisional/**",
)


def load_module(relative_path, name):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_samples_spec = importlib.util.spec_from_file_location(
    "workpack_samples_for_eval_verifier", HERE / "workpack_samples.py"
)
samples = importlib.util.module_from_spec(_samples_spec)
_samples_spec.loader.exec_module(samples)


def write(root, relative, text="test\n"):
    path = pathlib.Path(root) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@unittest.skipUnless(
    VERIFIER_PATH.is_file(),
    f"offline eval verifier not present ({VERIFIER_PATH}) — standalone package run",
)
class OfflineDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        cls.cases = {case["id"]: case for case in cls.dataset["cases"]}
        cls.verifier = load_module(
            "evals/nl-tax-agent-skills/verify_offline_workspace.py", "verify_offline_dataset"
        )

    def _release_eval_surfaces(self):
        benchmark_path = REPO_ROOT / "evals/nl-tax-agent-skills/plugin-eval-benchmark.json"
        benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
        dataset_ids = set(self.cases)
        contract_ids = set(self.dataset["contract_default_cases"])
        return dataset_ids, contract_ids, benchmark

    def test_dataset_and_default_case_sets_are_equal(self):
        dataset_ids, contract_ids, _ = self._release_eval_surfaces()
        self.assertEqual(contract_ids, dataset_ids)

    def test_check_dataset_passes(self):
        errors = self.verifier.validate_dataset_paths(DATASET_PATH, self.dataset)
        self.assertEqual(errors, [])

    def test_workpack_paths_match_the_grader_and_the_spec(self):
        grader = samples.load_grader()
        self.assertEqual(
            self.dataset["global"]["workpack_paths"],
            {"annual_2025": ANNUAL, "provisional_2026": PROVISIONAL},
        )
        self.assertEqual(
            set(self.dataset["global"]["workpack_paths"].values()),
            set(grader.WORKPACK_PATHS.values()),
        )
        self.assertTrue(set(LEGACY_TREES) <= set(self.dataset["global"]["legacy_forbidden_paths"]))
        self.assertEqual(self.dataset["global"]["harness_output_globs"], ["workspace/eval/**"])
        self.assertEqual(
            self.dataset["global"]["forbidden_generated_output_regex"],
            [
                "(?i)wachtwoord\\s*[:=]\\s*\\S+",
                "(?i)password\\s*[:=]\\s*\\S+",
            ],
        )

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
        expected = {
            "annual_casual_informational_tax": "annual/casual-informational-tax.yaml",
            "annual_explicit_preparation": "annual/explicit-preparation.yaml",
            "annual_winst_resume": "annual/winst-resume.yaml",
            "annual_corrected_tax_behavior": "annual/corrected-tax-behavior.yaml",
            "annual_entrepreneur_zzp": "annual/entrepreneur-zzp.yaml",
            "provisional_entrepreneur_profit": "provisional/entrepreneur-profit.yaml",
            "annual_evidence_status": "annual/evidence-status.yaml",
            "annual_default_no_write": "annual/default-no-write.yaml",
            "annual_save_on_request": "annual/save-on-request.yaml",
            "provisional_resume_attached_workpack": "provisional/resume-attached-workpack.yaml",
            "annual_legacy_ledger_ignored": "annual/legacy-0-3-ledger.yaml",
            "annual_reconfirm_unseen_figure": "annual/reconfirm-unseen-figure.yaml",
        }
        for case_id, fixture in expected.items():
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, self.cases)
                self.assertEqual(
                    self.cases[case_id]["fixture"],
                    f"evals/nl-tax-agent-skills/fixtures/{fixture}",
                )

        entrepreneur = self.cases["annual_entrepreneur_zzp"]
        entrepreneur_map = next(
            rule
            for rule in entrepreneur["text_checks"]
            if rule["path"] == ANNUAL and rule["appendix"] == "B"
        )
        self.assertIn("readiness: review_ready", entrepreneur_map["all"])
        self.assertIn("onderneming.wv.", entrepreneur_map["all"])
        filing_ready_business_ids = {
            "onderneming.belastbare_winst",
            "onderneming.zelfstandigenaftrek",
            "onderneming.startersaftrek",
            "onderneming.ondernemersaftrek_totaal",
            "onderneming.mkb_winstvrijstelling",
            "onderneming.kleinschaligheidsinvesteringsaftrek",
        }
        self.assertTrue(filing_ready_business_ids <= set(entrepreneur_map["none"]))
        self.assertEqual(entrepreneur["workpacks"][0]["field_map"], "expected")
        self.assertEqual(entrepreneur["workpacks"][0]["readiness"], "review_ready")

        provisional = self.cases["provisional_entrepreneur_profit"]
        provisional_map = next(
            rule
            for rule in provisional["text_checks"]
            if rule["path"] == PROVISIONAL and rule["appendix"] == "B"
        )
        self.assertIn("onderneming.geschatte_winst", provisional_map["all"])
        for forbidden in ("zelfstandigenaftrek", "MKB-winstvrijstelling", "Zvw", "final tax"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, provisional_map["none"])

        evidence = self.cases["annual_evidence_status"]
        self.assertNotIn(
            "text_checks",
            evidence,
            "agent interpretation belongs in fixtures/rubrics, not exact Markdown checks",
        )
        self.assertEqual(
            set(evidence["workpacks"][0]["documents"]["statuses_present"]),
            {"extracted", "needs review"},
        )

    def test_new_0_4_cases_encode_the_file_rules(self):
        no_write = self.cases["annual_default_no_write"]
        self.assertFalse(
            {ANNUAL, PROVISIONAL} & set(no_write["expected_files"]),
            "a conversation without consent writes no workpack",
        )
        # A8: the capture is the conversation rendering, which has no Appendix A.
        self.assertEqual(no_write["workpacks"][0]["presentation"], "chat")
        self.assertNotIn("save_consent", no_write["workpacks"][0])
        self.assertTrue(no_write["workpacks"][0]["path"].startswith("workspace/eval/"))

        save = self.cases["annual_save_on_request"]
        self.assertEqual(save["expected_files"], [ANNUAL])
        self.assertTrue(save["workpacks"][0]["updated_after_created"])
        self.assertEqual(save["workpacks"][0]["field_map"], "not_yet_mapped")

        resume = self.cases["provisional_resume_attached_workpack"]
        self.assertEqual(resume["expected_files"], [PROVISIONAL])
        fixture = yaml.safe_load(
            (REPO_ROOT / resume["fixture"]).read_text(encoding="utf-8")
        )
        self.assertEqual(fixture["seed_files"][0]["path"], "uploads/nl-tax-provisional-2026-workpack.md")
        self.assertFalse(fixture["expected_conversation"]["reasks_answered_intake_questions"])

        legacy = self.cases["annual_legacy_ledger_ignored"]
        fixture = yaml.safe_load((REPO_ROOT / legacy["fixture"]).read_text(encoding="utf-8"))
        seeded = {seed["path"] for seed in fixture["seed_files"]}
        self.assertEqual(
            seeded,
            {
                "workspace/taxpayer/profile.yaml",
                "workspace/shared/session-progress.yaml",
                "workspace/taxpayer/evidence-index.yaml",
                "workspace/annual/2025/return-pack.md",
            },
        )
        self.assertEqual(
            legacy["workpacks"][0]["documents"]["document_contains_any"], ["return-pack"]
        )

        reconfirm = self.cases["annual_reconfirm_unseen_figure"]
        self.assertEqual(reconfirm["expected_files"], ["workspace/eval/response.md"])

    def test_no_case_expects_a_legacy_or_standalone_file(self):
        for case in self.dataset["cases"]:
            for relative in case.get("expected_files", []):
                with self.subTest(case=case["id"], path=relative):
                    self.assertTrue(
                        relative in {ANNUAL, PROVISIONAL}
                        or relative.startswith("workspace/eval/"),
                        relative,
                    )
                    for banned in (
                        "field-map.yaml",
                        "profile.yaml",
                        "session-progress",
                        "evidence-index",
                        "return-pack",
                        "provisional-pack",
                        "delta-summary",
                        "review-questions",
                        "checklist",
                    ):
                        self.assertNotIn(banned, relative)

    def test_every_saved_workpack_case_is_graded_with_its_own_workflow(self):
        for case in self.dataset["cases"]:
            rules = {rule["path"]: rule for rule in case.get("workpacks", [])}
            for relative in case.get("expected_files", []):
                if relative not in {ANNUAL, PROVISIONAL}:
                    continue
                with self.subTest(case=case["id"], path=relative):
                    rule = rules[relative]
                    if relative == ANNUAL:
                        self.assertEqual(rule["workflow"], "annual_2025")
                    else:
                        self.assertTrue(rule["workflow"].startswith("provisional_2026_"))
                    if rule["workflow"] in {
                        "provisional_2026_review",
                        "provisional_2026_stopzetten",
                    }:
                        self.assertNotEqual(rule.get("field_map"), "expected")

    def test_omitted_shipped_fixtures_are_wired_without_replacing_security_fixture(self):
        fixtures = {case["id"]: case["fixture"] for case in self.dataset["cases"]}

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

    def test_structural_dataset_contains_no_model_prompts_or_case_markers(self):
        self.assertNotIn("case_marker", self.dataset["global"])
        for case in self.dataset["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn("prompt", case)
                self.assertNotIn(
                    "workspace/eval/current-case.txt",
                    case.get("expected_files", []),
                )
                for rule in case.get("text_checks", []):
                    self.assertIn(
                        rule["appendix"],
                        {"A", "B"},
                        "structural contracts check YAML appendices, never Markdown prose",
                    )


@unittest.skipUnless(VERIFIER_PATH.is_file(), "offline eval verifier not present")
class OfflineVerifierBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verifier = load_module(
            "evals/nl-tax-agent-skills/verify_offline_workspace.py", "verify_offline_behavior"
        )
        cls.dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))

    def case(self, case_id):
        return next(case for case in self.dataset["cases"] if case["id"] == case_id)

    def verify(self, root, case):
        return self.verifier.verify_case(pathlib.Path(root), self.dataset, case)

    def test_default_no_write_accepts_only_harness_captures(self):
        case = self.case("annual_default_no_write")
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "workspace/eval/response.md", "Here is your workpack.\n")
            write(
                tmp,
                "workspace/eval/chat-workpack.md",
                samples.build_chat_rendering(
                    "annual",
                    statuses=samples.default_statuses("annual", "annual_2025", "complete"),
                    readiness="review_ready",
                    field_map=samples.ANNUAL_FIELD_MAP,
                ),
            )
            self.assertEqual(self.verify(tmp, case), [])

            # A12: after mapping, the conversation rendering keeps the summary.
            write(
                tmp,
                "workspace/eval/chat-workpack.md",
                samples.remove_section(
                    samples.build_chat_rendering(
                        "annual",
                        statuses=samples.default_statuses("annual", "annual_2025", "complete"),
                        readiness="review_ready",
                        field_map=samples.ANNUAL_FIELD_MAP,
                    ),
                    "Field map summary",
                ),
            )
            errors = self.verify(tmp, case)
            self.assertTrue(
                any("'## Field map summary' is required" in error for error in errors), errors
            )

            # A8: a rendering that prints the YAML appendices or fill notes fails.
            write(
                tmp,
                "workspace/eval/chat-workpack.md",
                samples.build_workpack("annual", save_consent="not_given"),
            )
            errors = self.verify(tmp, case)
            self.assertTrue(any("never shows '## Appendix A" in error for error in errors), errors)
            self.assertTrue(any("never prints a YAML block" in error for error in errors), errors)
            self.assertTrue(any("template fill note" in error for error in errors), errors)
            write(
                tmp,
                "workspace/eval/chat-workpack.md",
                samples.build_chat_rendering(
                    "annual",
                    statuses=samples.default_statuses("annual", "annual_2025", "complete"),
                    readiness="review_ready",
                ),
            )

            write(tmp, ANNUAL, samples.build_workpack("annual"))
            errors = self.verify(tmp, case)
            self.assertTrue(
                any("without this case's save consent" in error for error in errors), errors
            )

    def test_stale_checklist_case_accepts_only_a_regenerated_consistent_map(self):
        case = self.case("annual_stale_checklist_after_correction")
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses.update(box1="complete", confirm="complete")
        corrected = yaml.safe_load(yaml.safe_dump(samples.ANNUAL_FIELD_MAP))
        corrected["fields"][0]["value"] = 51400
        new_rows = (("1", "Loon", "EUR 51.400", "ev_001", "box1.loon"),)
        old_rows = (("1", "Loon", "EUR 48,250", "ev_001", "box1.loon"),)
        with tempfile.TemporaryDirectory() as tmp:
            write(
                tmp,
                ANNUAL,
                samples.build_workpack(
                    "annual", field_map=corrected, statuses=statuses, checklist_rows=new_rows
                ),
            )
            self.assertEqual(self.verify(tmp, case), [])

            # The checklist still shows the pre-correction salary.
            write(
                tmp,
                ANNUAL,
                samples.build_workpack(
                    "annual", field_map=corrected, statuses=statuses, checklist_rows=old_rows
                ),
            )
            errors = self.verify(tmp, case)
            self.assertTrue(
                any("shows box1.loon = 'EUR 48,250' but Appendix B holds 51400" in error for error in errors),
                errors,
            )

            # Left stale at the end: valid as a workpack, but this case ends regenerated.
            stale = samples.build_workpack(
                "annual",
                field_map=samples.ANNUAL_FIELD_MAP,
                statuses={**statuses, "confirm": "not_started"},
                checklist_rows=old_rows,
                stale=("fiscaal loon", "2026-09-22"),
            )
            self.assertEqual(samples.load_grader().validate_workpack_text(stale, expected_kind="annual").errors, [])
            write(tmp, ANNUAL, stale)
            errors = self.verify(tmp, case)
            self.assertTrue(any("generation_confirmed False != True" in error for error in errors), errors)
            self.assertTrue(any("missing required text: '51400'" in error for error in errors), errors)

    def test_legacy_and_unexpected_files_are_rejected(self):
        case = self.case("annual_simple_resident")
        layouts = {
            "workspace/annual/2025/return-pack.md": "legacy 0.3 path written",
            "workspace/taxpayer/profile.yaml": "legacy 0.3 path written",
            "workspace/shared/session-progress.yaml": "legacy 0.3 path written",
            "workspace/provisional/2026/field-map.yaml": "legacy 0.3 path written",
            "workspace/field-map.yaml": "unexpected file under workspace/",
            "workspace/manual-entry-checklist.md": "unexpected file under workspace/",
            "workspace/nl-tax-annual-2025-workpack-v2.md": "workpack copy or variant",
            "backup/workspace/nl-tax-annual-2025-workpack.md": "second workspace tree",
            PROVISIONAL: "without this case's save consent",
        }
        for relative, fragment in layouts.items():
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as tmp:
                write(tmp, ANNUAL, samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP))
                write(tmp, relative, samples.build_workpack("provisional") if relative == PROVISIONAL else "x\n")
                errors = self.verify(tmp, {**case, "text_checks": [], "workpacks": [
                    {"path": ANNUAL, "workflow": "annual_2025", "field_map": "expected"}
                ]})
                self.assertTrue(any(fragment in error for error in errors), errors)

    def test_saved_workpack_is_graded_and_field_map_checked(self):
        case = {
            "id": "annual_bad_year",
            "expected_files": [ANNUAL],
            "workpacks": [{"path": ANNUAL, "workflow": "annual_2025", "field_map": "expected"}],
        }
        wrong_year = dict(samples.ANNUAL_FIELD_MAP, tax_year=2026)
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual", field_map=wrong_year))
            errors = self.verify(tmp, case)
        self.assertTrue(any("field-map validation failed" in error for error in errors), errors)
        self.assertTrue(
            any("Unsupported workflow/tax_year combination" in error for error in errors),
            errors,
        )
        self.assertTrue(any("Appendix B tax_year must be 2025" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual"))
            errors = self.verify(tmp, case)
        self.assertTrue(any("expected an Appendix B field map" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP))
            self.assertEqual(self.verify(tmp, case), [])

    def test_saved_file_must_record_consent(self):
        case = {
            "id": "consent",
            "expected_files": [ANNUAL],
            "workpacks": [{"path": ANNUAL, "workflow": "annual_2025"}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual", save_consent="not_given"))
            errors = self.verify(tmp, case)
        self.assertTrue(any("save_consent: given" in error for error in errors), errors)

    def test_resume_record_expectations_are_enforced(self):
        case = self.case("annual_save_on_request")
        statuses = samples.default_statuses("annual", "annual_2025")
        statuses.update(filing_status="complete", box1="complete", box3_peildatum="chat_only")
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual", statuses=statuses))
            self.assertEqual(self.verify(tmp, case), [])
            write(
                tmp,
                ANNUAL,
                samples.build_workpack(
                    "annual",
                    statuses=statuses,
                    created_at="2026-09-20T10:00:00Z",
                    updated_at="2026-09-20T10:00:00Z",
                ),
            )
            errors = self.verify(tmp, case)
            self.assertTrue(any("kept current" in error for error in errors), errors)
            statuses["box3_peildatum"] = "not_started"
            write(tmp, ANNUAL, samples.build_workpack("annual", statuses=statuses))
            errors = self.verify(tmp, case)
            self.assertTrue(any("sections.box3_peildatum.status" in error for error in errors), errors)

    def test_seeded_files_must_stay_byte_identical(self):
        case = self.case("annual_legacy_ledger_ignored")
        fixture = yaml.safe_load((REPO_ROOT / case["fixture"]).read_text(encoding="utf-8"))
        rows = (
            ("ev_001", "0.3 return-pack.md", "other", "2025", "taxpayer", "Income notes",
             "fiscaal loon: EUR 45,000", "extracted"),
        )
        with tempfile.TemporaryDirectory() as tmp:
            for seed in fixture["seed_files"]:
                target = pathlib.Path(tmp) / seed["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO_ROOT / seed["from"], target)
            write(tmp, ANNUAL, samples.build_workpack("annual", documents=rows))
            self.assertEqual(self.verify(tmp, case), [])

            ledger = pathlib.Path(tmp) / "workspace/shared/session-progress.yaml"
            ledger.write_text(ledger.read_text(encoding="utf-8") + "touched: true\n", encoding="utf-8")
            errors = self.verify(tmp, case)
            self.assertTrue(any("seeded file changed" in error for error in errors), errors)
            ledger.unlink()
            errors = self.verify(tmp, case)
            self.assertTrue(any("seeded file missing" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as tmp:
            for seed in fixture["seed_files"]:
                target = pathlib.Path(tmp) / seed["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO_ROOT / seed["from"], target)
            write(tmp, ANNUAL, samples.build_workpack("annual"))
            write(tmp, "workspace/taxpayer/evidence-index-v2.yaml", "x: 1\n")
            errors = self.verify(tmp, case)
            self.assertTrue(any("names no document matching" in error for error in errors), errors)
            self.assertTrue(any("legacy 0.3 path written" in error for error in errors), errors)

    def test_offline_verifier_enforces_workflow_scoped_source_ledgers(self):
        case = {
            "id": "dual_sources",
            "expected_files": [ANNUAL, PROVISIONAL],
            "workpacks": [
                {"path": ANNUAL, "workflow": "annual_2025"},
                {"path": PROVISIONAL, "workflow": "provisional_2026_request"},
            ],
            "source_ledger_check": {"workpacks": [ANNUAL, PROVISIONAL]},
        }
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual", queued_workflow="provisional_2026_request"))
            write(tmp, PROVISIONAL, samples.build_workpack("provisional"))
            self.assertEqual(self.verify(tmp, case), [])

            write(
                tmp,
                PROVISIONAL,
                samples.build_workpack(
                    "provisional",
                    sources=("bd_box1_rates_2026", "bd_box1_rates_2025", "bd_box3_2025_calc"),
                ),
            )
            errors = self.verify(tmp, case)
            self.assertTrue(any("cross-workflow union" in error for error in errors), errors)

            mismatched = samples.build_workpack("annual").replace(
                "- bd_jaaropgaaf_fields_2025\n", "", 1
            )
            write(tmp, ANNUAL, mismatched)
            errors = self.verify(tmp, case)
            self.assertTrue(any("Sources used" in error for error in errors), errors)

    def test_generated_output_regex_still_rejects_credentials(self):
        case = self.case("annual_casual_informational_tax")
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "workspace/eval/response.md", "DigiD wachtwoord: hunter2\n")
            errors = self.verify(tmp, case)
        self.assertTrue(any("forbidden generated-output regex" in error for error in errors), errors)

    def test_appendix_text_checks_target_yaml_only(self):
        case = {
            "id": "appendix",
            "expected_files": [ANNUAL],
            "workpacks": [{"path": ANNUAL, "workflow": "annual_2025"}],
            "text_checks": [
                {"path": ANNUAL, "appendix": "A", "all": ["workflow: annual_2025"], "none": ["provisional_2026"]},
                {"path": ANNUAL, "appendix": "B", "all": ["annual_return"]},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual"))
            errors = self.verify(tmp, case)
            self.assertTrue(any("no single Appendix B yaml block" in error for error in errors), errors)
            self.assertFalse(any("Appendix A missing" in error for error in errors), errors)
            write(tmp, ANNUAL, samples.build_workpack("annual", field_map=samples.ANNUAL_FIELD_MAP))
            self.assertEqual(self.verify(tmp, case), [])


class AgenticSurfaceTests(unittest.TestCase):
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
            "cowork-save-and-resume",
            "cowork-stale-checklist-after-correction",
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

    def test_cowork_criteria_assume_no_written_state(self):
        eval_root = REPO_ROOT / "evals/claude"
        for criteria in eval_root.glob("cowork-*/graders/criteria.md"):
            text = criteria.read_text(encoding="utf-8")
            with self.subTest(case=criteria.parent.parent.name):
                for stale in (
                    "local workpack",
                    "field-map.yaml",
                    "session-progress",
                    "profile.yaml",
                    "evidence index",
                    "canonical artifact",
                    "annual field map have validated",
                ):
                    self.assertNotIn(stale, text)

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

        def run(root):
            return subprocess.run(["bash", str(script)], cwd=root, capture_output=True, text=True)

        with tempfile.TemporaryDirectory() as tmp:
            clean = run(tmp)
            self.assertEqual(clean.returncode, 0, clean.stderr)

        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, ANNUAL, samples.build_workpack("annual", queued_workflow="provisional_2026_request"))
            write(tmp, PROVISIONAL, samples.build_workpack("provisional"))
            valid = run(tmp)
            self.assertEqual(valid.returncode, 0, valid.stderr)

        invalid_layouts = {
            "case marker": {"workspace/eval/current-case.txt": "x\n"},
            "0.3 annual tree": {"workspace/annual/2025/return-pack.md": "x\n"},
            "0.3 profile ledger": {"workspace/taxpayer/profile.yaml": "x\n"},
            "0.3 session ledger": {"workspace/shared/session-progress.yaml": "x\n"},
            "standalone field map": {"workspace/field-map.yaml": "x\n"},
            "helper-owned note": {"workspace/shared/box2-notes.md": "x\n"},
            "workpack variant": {
                "workspace/nl-tax-annual-2025-workpack-2026-09-20.md": "x\n"
            },
            "second workspace tree": {
                "copy/workspace/nl-tax-annual-2025-workpack.md": "x\n"
            },
            "workpack copy outside workspace": {"nl-tax-annual-2025-workpack.md": "x\n"},
            "saved without consent": {
                ANNUAL: samples.build_workpack("annual", save_consent="not_given")
            },
            "annual file holds provisional workflow": {
                ANNUAL: samples.build_workpack("provisional")
            },
            "annual names provisional file": {
                ANNUAL: samples.build_workpack("annual").replace(
                    "## Assumptions\n",
                    "## Assumptions\n\nSee workspace/nl-tax-provisional-2026-workpack.md\n",
                    1,
                )
            },
            "provisional collects werkelijk rendement": {
                PROVISIONAL: samples.build_workpack("provisional").replace(
                    "## Assumptions\n",
                    "## Assumptions\n\nWerkelijk rendement 2026: EUR 900\n",
                    1,
                )
            },
        }
        for label, files in invalid_layouts.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                for relative, text in files.items():
                    write(tmp, relative, text)
                result = run(tmp)
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_new_cowork_graders_cover_handoff_generation_and_save_gates(self):
        eval_root = REPO_ROOT / "evals/claude"
        dual_prompt = (
            eval_root / "cowork-dual-workflow-handoff/prompt.md"
        ).read_text(encoding="utf-8")
        dual_criteria = (
            eval_root / "cowork-dual-workflow-handoff/graders/criteria.md"
        ).read_text(encoding="utf-8")
        dual_criteria_flat = " ".join(dual_criteria.split())
        entrepreneur_criteria = " ".join(
            (
                eval_root / "cowork-provisional-entrepreneur-profit/graders/criteria.md"
            ).read_text(encoding="utf-8").split()
        )
        save_resume = " ".join(
            (eval_root / "cowork-save-and-resume/graders/criteria.md")
            .read_text(encoding="utf-8")
            .split()
        )
        save_prompt = (eval_root / "cowork-save-and-resume/prompt.md").read_text(encoding="utf-8")

        self.assertIn("prepare both", dual_prompt.lower())
        for required in (
            "sole owning workflow",
            "queued intent",
            "without a new activation phrase",
            "must not authorize provisional generation",
            "own immediate, contextual confirmation",
            "writes no file",
            "own save consent",
        ):
            with self.subTest(required=required):
                self.assertIn(required, dual_criteria_flat)
        self.assertIn("not final-generation consent", entrepreneur_criteria)
        self.assertIn("must not claim", entrepreneur_criteria)
        self.assertIn("immediate, scoped natural-language confirmation", entrepreneur_criteria)
        self.assertIn("writes no file", entrepreneur_criteria)

        self.assertIn("workpack_format: nl-tax-workpack", save_prompt)
        for required in (
            "Appendix A",
            "must not re-ask",
            "first section",
            "workspace/nl-tax-annual-2025-workpack.md",
            "never a copy",
            "re-confirm",
        ):
            with self.subTest(required=required):
                self.assertIn(required, save_resume)


if __name__ == "__main__":
    unittest.main()
