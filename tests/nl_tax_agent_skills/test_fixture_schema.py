#!/usr/bin/env python3
"""Shape checks for the eval fixtures under evals/nl-tax-agent-skills/fixtures/.

Fixtures are consumed by humans and by the structural contract harness, so they must
share one minimal schema: identifying metadata, a workflow label drawn from the
intake routing vocabulary, and explicit expectations (either an
``expected_behavior`` list or an ``acceptance_criteria`` list; both may be
present).
"""

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
DATASET_PATH = REPO_ROOT / "evals/nl-tax-agent-skills/offline-dataset.yaml"

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


def load_fixture(relative_path):
    path = FIXTURES_DIR / relative_path
    if not path.is_file():
        raise AssertionError(f"required fixture does not exist: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


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

    def test_annual_entrepreneur_fixture_keeps_field_map_draft(self):
        data = load_fixture("annual/entrepreneur-zzp.yaml")
        state = data["expected_state"]

        self.assertEqual(state["session_progress_version"], "1.4")
        self.assertEqual(state["field_map_readiness"], "draft")
        self.assertIn(
            "business-section schema review",
            state["field_map_blockers"],
        )
        self.assertEqual(state["annual_2025_subsection"], "winst")
        self.assertEqual(state["workpack_owner"], "nl-tax-annual-return")
        self.assertEqual(state["field_map_owner"], "nl-tax-field-mapper")

    def test_cowork_behavior_fixtures_preserve_routing_and_resume_contracts(self):
        casual = load_fixture("annual/casual-informational-tax.yaml")
        explicit = load_fixture("annual/explicit-preparation.yaml")
        resume = load_fixture("annual/winst-resume.yaml")
        corrected = load_fixture("annual/corrected-tax-behavior.yaml")

        self.assertFalse(casual["user_request"]["explicitly_requests_preparation"])
        self.assertIn(
            "workspace/taxpayer/profile.yaml",
            casual["expected_outputs"]["files_not_created"],
        )

        self.assertTrue(explicit["user_request"]["explicitly_requests_preparation"])
        self.assertEqual(
            explicit["expected_state"]["session_progress_version"], "1.4"
        )

        resume_state = resume["expected_state"]
        self.assertEqual(resume_state["annual_2025_subsection"], "winst")
        self.assertTrue(resume_state["preserves_completed_subsections"])
        self.assertFalse(resume_state["resets_profile_or_session"])
        self.assertEqual(resume_state["workpack_owner"], "nl-tax-annual-return")
        self.assertEqual(resume_state["field_map_owner"], "nl-tax-field-mapper")

        corrected_checks = corrected["expected_outputs"]["response_checks"]
        self.assertEqual(len(corrected_checks["healthcare_excluded"]), 5)
        self.assertEqual(corrected_checks["credit_reduces"], "gecombineerde_heffing")
        self.assertFalse(corrected_checks["no_invitation_extension_available"])

    def test_provisional_entrepreneur_fixture_maps_only_expected_profit(self):
        data = load_fixture("provisional/entrepreneur-profit.yaml")
        state = data["expected_state"]

        self.assertEqual(state["session_progress_version"], "1.4")
        self.assertEqual(state["provisional_2026_subsection"], "winst_forecast")
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

    def test_annual_evidence_status_counts_only_reviewed_current_year_item(self):
        data = load_fixture("annual/evidence-status.yaml")
        state = data["expected_state"]
        items = {
            item["evidence_id"]: item
            for item in data["evidence_index"]["items"]
        }

        def satisfies_all_gates(item):
            return (
                item["extraction_status"] == "extracted"
                and item["tax_year"] == 2025
                and item["review_required"] is False
                and bool(item["extracted_fields"])
            )

        self.assertEqual(state["session_progress_version"], "1.4")
        self.assertEqual(state["eligible_evidence_count"], 1)
        self.assertEqual(state["eligible_evidence_ids"], ["ev_current_reviewed"])
        self.assertTrue(state["decision_owner_is_agent"])
        self.assertTrue(satisfies_all_gates(items["ev_current_reviewed"]))

        prior_year = items["ev_previous_reviewed"]
        self.assertEqual(prior_year["extraction_status"], "extracted")
        self.assertIs(prior_year["review_required"], False)
        self.assertTrue(prior_year["extracted_fields"])
        self.assertNotEqual(prior_year["tax_year"], 2025)

        needs_review = items["ev_current_needs_review"]
        self.assertEqual(needs_review["extraction_status"], "extracted")
        self.assertEqual(needs_review["tax_year"], 2025)
        self.assertTrue(needs_review["extracted_fields"])
        self.assertIs(needs_review["review_required"], True)

        for evidence_id in state["excluded_evidence_ids"]:
            with self.subTest(evidence_id=evidence_id):
                self.assertFalse(satisfies_all_gates(items[evidence_id]))

    def test_evidence_index_template_documents_canonical_extraction_statuses(self):
        skills_dir = REPO_ROOT / "plugins/nl-tax-agent-skills/skills"
        template = (
            skills_dir
            / "nl-tax-evidence-indexer/templates/evidence-index.yaml"
        ).read_text(encoding="utf-8")
        reference = (
            skills_dir
            / "nl-tax-evidence-indexer/reference/extraction-boundaries.md"
        ).read_text(encoding="utf-8")
        status_line = next(
            line
            for line in template.splitlines()
            if line.startswith("#   extraction_status:")
        )

        for status in ("indexed_only", "classified", "extracted", "failed"):
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", reference)
                self.assertIn(f'"{status}"', status_line)

    def test_simple_resident_fixture_expects_schema_1_4_session_state(self):
        data = load_fixture("annual/simple-resident.yaml")
        state = data["expected_state"]

        self.assertEqual(state["session_progress_version"], "1.4")
        self.assertEqual(state["annual_2025_subsection"], "box1")
        self.assertEqual(state["workpack_owner"], "nl-tax-annual-return")
        self.assertEqual(state["field_map_owner"], "nl-tax-field-mapper")

    def test_declared_annual_subsections_exist_in_schema_1_4(self):
        skills_dir = REPO_ROOT / "plugins/nl-tax-agent-skills/skills"
        session_template = yaml.safe_load(
            (
                skills_dir / "_shared/templates/session-progress.yaml"
            ).read_text(encoding="utf-8")
        )
        canonical = set(
            session_template["sections"]["annual_2025"]["subsections"]
        )

        for path in iter_fixture_paths():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            declared = (data.get("expected_state") or {}).get(
                "annual_2025_subsection"
            )
            if declared is not None:
                with self.subTest(fixture=path.name, subsection=declared):
                    self.assertIn(declared, canonical)


if __name__ == "__main__":
    unittest.main()
