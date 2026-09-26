#!/usr/bin/env python3
"""Shape checks for the eval fixtures under evals/nl-tax-agent-skills/fixtures/.

Fixtures are consumed by humans, LLM graders, and the structural contract
harness, so they share one minimal schema: identifying metadata, a workflow
label drawn from the intake routing vocabulary, and explicit expectations
(``expected_behavior`` and/or ``acceptance_criteria``). 0.4 adds the file
rules: a fixture creates files only through the save consent it declares, and
only the two fixed workpack paths; resume expectations use Appendix A resume
record terms, never 0.3 ledger terms.
"""

import importlib.util
import pathlib
import unittest

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES_DIR = (
    REPO_ROOT
    / "evals"
    / "nl-tax-agent-skills"
    / "fixtures"
)
SEEDS_DIR = FIXTURES_DIR / "seeds"
DATASET_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"
PLUGIN_ROOT = REPO_ROOT / "plugins/nl-tax-agent-skills"
GRADER_PATH = REPO_ROOT / "tools/nl_tax_agent_skills/workpack/validate_workpack.py"

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

WORKPACK_BY_FAMILY = {
    "annual_2025": "workspace/nl-tax-annual-2025-workpack.md",
    "provisional_2026": "workspace/nl-tax-provisional-2026-workpack.md",
}
CONSENT_VALUES = {"given", "declined", "pending"}
CONSENT_POINTS = {"workflow_start", "pause", "generation", "user_request", "resumed_file"}
STATUS_VALUES = {"not_started", "in_progress", "complete", "chat_only", "deferred"}
LEGACY_TERMS = (
    "session_progress_version",
    "sources_loaded_by_workflow",
    "active_skill",
    "evidence_index_version",
    "taxpayer_profile_version",
)


def iter_fixture_paths():
    return sorted(FIXTURES_DIR.glob("*/*.yaml"))


def load_fixture(relative_path):
    path = FIXTURES_DIR / relative_path
    if not path.is_file():
        raise AssertionError(f"required fixture does not exist: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_grader():
    spec = importlib.util.spec_from_file_location("validate_workpack_for_fixtures", GRADER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def family_for(workflow_key):
    return "annual_2025" if workflow_key.startswith("annual") else "provisional_2026"


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

    @unittest.skipUnless(
        DATASET_PATH.is_file(),
        "repo-only offline dataset is absent from standalone plugin package",
    )
    def test_shipped_fixture_paths_equal_dataset_fixture_paths(self):
        dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        shipped = {
            path.relative_to(FIXTURES_DIR.parents[2]).as_posix()
            for path in iter_fixture_paths()
        }
        referenced_paths = [case["fixture"] for case in dataset["cases"]]
        self.assertEqual(
            len(referenced_paths),
            len(set(referenced_paths)),
            "each dataset case must map to a unique shipped fixture",
        )
        self.assertEqual(set(referenced_paths), shipped)

    @unittest.skipUnless(
        DATASET_PATH.is_file(),
        "repo-only offline dataset is absent from standalone plugin package",
    )
    def test_dataset_case_ids_are_unique_and_equal_contract_cases(self):
        dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        case_ids = [case["id"] for case in dataset["cases"]]
        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertEqual(set(case_ids), set(dataset["contract_default_cases"]))

    @unittest.skipUnless(
        DATASET_PATH.is_file(),
        "repo-only offline dataset is absent from standalone plugin package",
    )
    def test_dataset_includes_payment_redirect_and_staleness_fixtures(self):
        dataset = yaml.safe_load(DATASET_PATH.read_text(encoding="utf-8"))
        fixtures = {case["id"]: case["fixture"] for case in dataset["cases"]}

        self.assertEqual(
            fixtures["provisional_stopzetten_payment_redirect"],
            "evals/nl-tax-agent-skills/fixtures/provisional/stopzetten-payment-redirect.yaml",
        )
        self.assertEqual(
            fixtures["security_source_staleness"],
            "evals/nl-tax-agent-skills/fixtures/security/source-staleness.yaml",
        )


class SaveConsentAndFileRuleTests(unittest.TestCase):
    """R1-R3: files appear only through declared consent, at fixed paths."""

    def test_files_created_are_only_the_fixed_workpacks_and_need_consent(self):
        for path in iter_fixture_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            outputs = data.get("expected_outputs") or {}
            created = outputs.get("files_created") or []
            saving = data.get("saving") or {}
            with self.subTest(fixture=path.name):
                for relative in created:
                    self.assertIn(relative, WORKPACK_BY_FAMILY.values())
                    family = next(
                        key for key, value in WORKPACK_BY_FAMILY.items() if value == relative
                    )
                    self.assertEqual(
                        (saving.get(family) or {}).get("consent"),
                        "given",
                        f"{path.name} creates {relative} without declared save consent",
                    )
                for family, state in saving.items():
                    self.assertIn(family, WORKPACK_BY_FAMILY)
                    self.assertIn(state.get("consent"), CONSENT_VALUES)
                    if state.get("consent") == "given":
                        self.assertIn(state.get("at"), CONSENT_POINTS)
                        self.assertIn(WORKPACK_BY_FAMILY[family], created)
                    else:
                        self.assertNotIn(WORKPACK_BY_FAMILY[family], created)
                for relative in outputs.get("files_not_created") or []:
                    self.assertNotIn(relative, created)

    def test_fixtures_use_resume_record_terms_not_0_3_ledgers(self):
        for path in iter_fixture_paths():
            if path.name == "legacy-0-3-ledger.yaml":
                continue  # describes the 0.3 seed on purpose
            text = path.read_text(encoding="utf-8")
            with self.subTest(fixture=path.name):
                for term in LEGACY_TERMS:
                    self.assertNotIn(term, text)
                for legacy_path in (
                    "workspace/taxpayer/",
                    "workspace/shared/",
                    "workspace/annual/",
                    "workspace/provisional/",
                    "field-map.yaml",
                    "evidence-index",
                ):
                    self.assertNotIn(legacy_path, text)

    def test_expected_resume_record_sections_exist_for_the_workflow(self):
        grader = load_grader()
        plugin_root = str(PLUGIN_ROOT.resolve())
        checked = 0
        for path in iter_fixture_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            record = data.get("expected_resume_record")
            if not record:
                continue
            workflow = record["workflow"]
            required, optional = grader.expected_section_keys(plugin_root, workflow)
            with self.subTest(fixture=path.name, workflow=workflow):
                self.assertEqual(record.get("tax_year"), 2025 if workflow == "annual_2025" else 2026)
                self.assertIn(record.get("save_consent"), {"given", "not_given"})
                for key, status in (record.get("sections") or {}).items():
                    self.assertIn(key, required | optional)
                    self.assertIn(status, STATUS_VALUES)
                checked += 1
        self.assertGreaterEqual(checked, 10)

    def test_no_write_fixtures_create_nothing(self):
        for relative in (
            "annual/casual-informational-tax.yaml",
            "annual/corrected-tax-behavior.yaml",
            "annual/explicit-preparation.yaml",
            "annual/default-no-write.yaml",
            "annual/reconfirm-unseen-figure.yaml",
            "security/out-of-scope.yaml",
            "security/complex-box2-review.yaml",
            "security/blocked-universal-roadmap-workflows.yaml",
        ):
            with self.subTest(fixture=relative):
                data = load_fixture(relative)
                outputs = data["expected_outputs"]
                self.assertEqual(outputs["files_created"], [])
                self.assertTrue(
                    set(WORKPACK_BY_FAMILY.values()) <= set(outputs["files_not_created"])
                )

    def test_default_no_write_fixture_runs_the_whole_workflow_without_consent(self):
        data = load_fixture("annual/default-no-write.yaml")
        self.assertEqual(data["saving"]["annual_2025"]["consent"], "declined")
        self.assertEqual(
            data["saving"]["annual_2025"]["declined_at"], ["workflow_start", "generation"]
        )
        conversation = data["expected_conversation"]
        self.assertTrue(conversation["workpack_presented_in_conversation"])
        self.assertTrue(conversation["field_map_summary_presented_in_conversation"])
        chat = data["expected_outputs"]["chat_workpack"]
        self.assertEqual(chat["presentation"], "chat")
        self.assertFalse(chat["yaml_appendices_shown"])
        self.assertFalse(chat["template_fill_notes_shown"])
        self.assertEqual(chat["field_map_shown_as"], "summary_table")
        self.assertTrue(conversation["one_yes_no_question_per_reply"])
        self.assertTrue(conversation["final_review_asks_only_generation_question"])
        self.assertEqual(conversation["save_offer_points_used"], ["workflow_start", "generation"])
        self.assertTrue(conversation["confirmed_so_far_recap_after_each_section"])

    def test_save_on_request_fixture_writes_then_keeps_current(self):
        data = load_fixture("annual/save-on-request.yaml")
        self.assertEqual(data["saving"]["annual_2025"]["at"], "user_request")
        self.assertEqual(data["saving"]["annual_2025"]["declined_first_at"], "workflow_start")
        conversation = data["expected_conversation"]
        self.assertEqual(conversation["file_written_at_turn"], 3)
        self.assertEqual(conversation["file_updated_in_place_at_turns"], [4, 5])
        self.assertFalse(conversation["creates_copies_or_variants"])
        self.assertTrue(data["expected_resume_record"]["updated_after_created"])

    def test_stale_checklist_fixture_blocks_until_regeneration(self):
        data = load_fixture("annual/stale-checklist-after-correction.yaml")
        saving = data["saving"]["annual_2025"]
        self.assertEqual(saving["at"], "user_request")
        self.assertEqual(saving["declined_at"], ["workflow_start", "generation"])
        states = data["expected_state_after_turn"]
        self.assertIs(states[6]["generation_confirmed"], True)
        self.assertIs(states[7]["generation_confirmed"], False)
        self.assertEqual(states[7]["stale_line_in"], ["field_map_summary", "appendix_b"])
        self.assertEqual(states[8]["checklist_values_shown"], [])
        self.assertEqual(states[11]["stale_line_in"], [])
        self.assertEqual(states[11]["field_map_value"]["box1.loon"], 51400)
        conversation = data["expected_conversation"]
        self.assertTrue(conversation["map_rebuilt_from_recorded_facts_at_first_save"])
        self.assertTrue(conversation["checklist_blocked_while_stale"])
        self.assertFalse(conversation["checklist_ever_shows_old_value"])
        self.assertFalse(conversation["resume_reasks_answered_questions"])
        self.assertIs(data["expected_resume_record"]["generation_confirmed"], True)

    def test_reconfirm_fixture_never_reconstructs_amounts(self):
        data = load_fixture("annual/reconfirm-unseen-figure.yaml")
        conversation = data["expected_conversation"]
        visible = data["conversation_state"]["exact_figures_visible_verbatim"]
        self.assertEqual(
            set(conversation["asks_to_reconfirm"]),
            {key for key, shown in visible.items() if not shown},
        )
        self.assertFalse(conversation["reconstructs_amount_from_summary"])
        self.assertFalse(conversation["generates_before_reconfirmation"])


class SeedTests(unittest.TestCase):
    def test_seed_files_exist_and_stay_outside_the_fixed_workpack_paths(self):
        seeded = 0
        for path in iter_fixture_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            for seed in data.get("seed_files") or []:
                with self.subTest(fixture=path.name, seed=seed["path"]):
                    source = REPO_ROOT / seed["from"]
                    self.assertTrue(source.is_file(), source)
                    self.assertTrue(source.is_relative_to(SEEDS_DIR))
                    self.assertNotIn(seed["path"], WORKPACK_BY_FAMILY.values())
                    self.assertIn(
                        seed["role"],
                        {"attached_saved_workpack", "legacy_0_3_ledger", "legacy_0_3_source_document"},
                    )
                    self.assertIn(seed["path"], data["expected_outputs"]["seeded_files_unchanged"])
                    seeded += 1
        self.assertEqual(seeded, 6)

    def test_seeded_saved_workpacks_pass_the_grader(self):
        grader = load_grader()
        for path in iter_fixture_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            for seed in data.get("seed_files") or []:
                if seed["role"] != "attached_saved_workpack":
                    continue
                with self.subTest(seed=seed["from"]):
                    report = grader.validate_workpack_file(
                        REPO_ROOT / seed["from"], expect_saved=True
                    )
                    self.assertEqual(report.errors, [])
                    state = data["attached_workpack_state"]
                    self.assertEqual(report.resume_record["workflow"], data["workflow"])
                    self.assertEqual(report.resume_record["save_consent"], state["save_consent"])
                    for key, status in state["sections"].items():
                        self.assertEqual(report.resume_record["sections"][key]["status"], status)

    def test_legacy_seeds_are_0_3_shaped_and_hold_no_identifiers(self):
        grader = load_grader()
        legacy = SEEDS_DIR / "legacy-0-3"
        profile = yaml.safe_load((legacy / "profile.yaml").read_text(encoding="utf-8"))
        session = yaml.safe_load((legacy / "session-progress.yaml").read_text(encoding="utf-8"))
        index = yaml.safe_load((legacy / "evidence-index.yaml").read_text(encoding="utf-8"))
        self.assertEqual(profile["taxpayer_profile_version"], "1.4")
        self.assertEqual(session["session_progress_version"], "1.4")
        self.assertEqual(index["evidence_index_version"], "1.1")
        for seed in sorted(SEEDS_DIR.rglob("*")):
            if not seed.is_file():
                continue
            text = seed.read_text(encoding="utf-8")
            with self.subTest(seed=seed.name):
                self.assertIsNone(grader.BSN_LIKE.search(text))
                self.assertIsNone(grader.DUTCH_IBAN.search(text))


class ScenarioContractTests(unittest.TestCase):
    def test_annual_entrepreneur_fixture_reaches_review_ready(self):
        """A complete eenmanszaak case reaches review_ready: the reviewed
        zakelijke schema exists, so the business-section schema-review blocker
        does not fire merely because the case has an onderneming."""
        data = load_fixture("annual/entrepreneur-zzp.yaml")
        record = data["expected_resume_record"]

        self.assertEqual(record["readiness"], "review_ready")
        self.assertEqual(record["field_map_readiness"], "review_ready")
        self.assertEqual(record["field_map_blockers"], [])
        self.assertEqual(record["sections"]["winst"], "complete")
        self.assertEqual(record["workpack_owner"], "nl-tax-annual-return")
        self.assertEqual(record["field_map_owner"], "nl-tax-field-mapper")
        self.assertEqual(data["saving"]["annual_2025"]["consent"], "given")

    def test_cowork_behavior_fixtures_preserve_routing_and_resume_contracts(self):
        casual = load_fixture("annual/casual-informational-tax.yaml")
        explicit = load_fixture("annual/explicit-preparation.yaml")
        resume = load_fixture("annual/winst-resume.yaml")
        corrected = load_fixture("annual/corrected-tax-behavior.yaml")

        self.assertFalse(casual["user_request"]["explicitly_requests_preparation"])
        self.assertIn(
            "workspace/nl-tax-annual-2025-workpack.md",
            casual["expected_outputs"]["files_not_created"],
        )

        self.assertTrue(explicit["user_request"]["explicitly_requests_preparation"])
        self.assertEqual(explicit["saving"]["annual_2025"]["consent"], "pending")
        self.assertTrue(explicit["expected_conversation"]["intake_writes_nothing"])
        self.assertEqual(
            explicit["expected_conversation"]["save_offer_points_used"], ["workflow_start"]
        )

        self.assertEqual(resume["seed_files"][0]["role"], "attached_saved_workpack")
        self.assertEqual(resume["attached_workpack_state"]["sections"]["winst"], "in_progress")
        self.assertEqual(resume["expected_resume_record"]["sections"]["winst"], "complete")
        self.assertTrue(resume["expected_resume_record"]["created_at_preserved"])
        conversation = resume["expected_conversation"]
        self.assertFalse(conversation["restarts_intake"])
        self.assertFalse(conversation["reasks_answered_intake_questions"])
        self.assertFalse(conversation["reasks_answered_questions"])
        self.assertEqual(conversation["first_question"], "Q001")
        self.assertEqual(conversation["workpack_owner"], "nl-tax-annual-return")
        self.assertEqual(conversation["field_map_owner"], "nl-tax-field-mapper")

        corrected_checks = corrected["expected_outputs"]["response_checks"]
        self.assertEqual(len(corrected_checks["healthcare_excluded"]), 5)
        self.assertEqual(corrected_checks["credit_reduces"], "gecombineerde_heffing")
        self.assertFalse(corrected_checks["no_invitation_extension_available"])

    def test_provisional_resume_fixture_does_not_rerun_intake(self):
        data = load_fixture("provisional/resume-attached-workpack.yaml")
        conversation = data["expected_conversation"]
        self.assertFalse(conversation["reasks_answered_intake_questions"])
        self.assertTrue(conversation["full_reentry_notice_before_first_question"])
        self.assertEqual(conversation["first_section_resumed"], "income_pension_benefit")
        state = data["attached_workpack_state"]["sections"]
        first_open = next(
            key
            for key in (
                "baseline",
                "income_employment",
                "income_pension_benefit",
                "income_other",
                "winst_forecast",
                "deductions",
                "box2",
                "box3_peildatum",
                "partner_allocation",
                "confirm",
            )
            if state[key] not in {"complete", "chat_only"}
        )
        self.assertEqual(first_open, conversation["first_section_resumed"])

    def test_provisional_entrepreneur_fixture_maps_only_expected_profit(self):
        data = load_fixture("provisional/entrepreneur-profit.yaml")
        state = data["expected_state"]

        self.assertEqual(state["provisional_2026_section"], "winst_forecast")
        self.assertEqual(
            state["required_field_ids"],
            ["onderneming.geschatte_winst"],
        )
        self.assertEqual(
            set(state["forbidden_outputs"]),
            {
                "annual entrepreneur deductions",
                "Zvw calculation",
                "final tax calculation",
            },
        )
        self.assertEqual(state["workpack_owner"], "nl-tax-provisional-assessment")
        self.assertEqual(state["field_map_owner"], "nl-tax-field-mapper")

    def test_annual_evidence_status_counts_only_reviewed_current_year_document(self):
        data = load_fixture("annual/evidence-status.yaml")
        state = data["expected_state"]
        documents = {doc["name"]: doc for doc in data["shared_documents"]}
        rows = {row["document"]: row for row in data["expected_documents_rows"]}

        def closes_gap(row):
            return row["tax_year"] == 2025 and row["status"] == "extracted"

        self.assertEqual(set(documents), set(rows))
        self.assertEqual(state["eligible_document_count"], 1)
        self.assertEqual(
            sorted(name for name, row in rows.items() if closes_gap(row)),
            state["eligible_documents"],
        )
        for name, row in rows.items():
            with self.subTest(document=name):
                self.assertEqual(row["closes_2025_income_gap"], closes_gap(row))
                self.assertEqual(row["tax_year"], documents[name]["tax_year"])
                self.assertIn(row["status"], {"extracted", "needs review"})
        self.assertEqual(
            sorted(state["excluded_documents"]),
            sorted(name for name, row in rows.items() if not closes_gap(row)),
        )
        self.assertTrue(state["decision_owner_is_agent"])
        self.assertEqual(data["expected_resume_record"]["sections"]["box1"], "deferred")

    def test_stopzetten_redirect_fixture_records_the_change(self):
        data = load_fixture("provisional/stopzetten-payment-redirect.yaml")
        record = data["expected_resume_record"]
        self.assertEqual(data["workflow"], "provisional_2026_stopzetten")
        self.assertEqual(record["workflow"], "provisional_2026_change")
        self.assertEqual(record["sections"]["stopzetten_direction"], "complete")
        self.assertEqual(record["sections"]["confirm"], "not_started")
        self.assertFalse(record["generation_confirmed"])

    def test_evidence_types_reference_documents_canonical_extraction_statuses(self):
        reference = (
            PLUGIN_ROOT
            / "skills/nl-tax-shared-resources/reference/extraction-boundaries.md"
        ).read_text(encoding="utf-8")
        for status in ("extracted", "needs review"):
            with self.subTest(status=status):
                self.assertIn(status, reference)
        self.assertFalse(
            (PLUGIN_ROOT / "skills/nl-tax-evidence-indexer").exists(),
            "the evidence indexer is retired in 0.4",
        )


if __name__ == "__main__":
    unittest.main()
