#!/usr/bin/env python3
"""Regression contracts for the July 2026 annual-content audit repairs."""

from pathlib import Path
import unittest


PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "nl-tax-agent-skills"
SKILLS = PLUGIN / "skills"


def read(relative: str) -> str:
    return (SKILLS / relative).read_text(encoding="utf-8").lower()


def compact(value: str) -> str:
    return " ".join(value.lower().split())


class AnnualContentAuditRepairTests(unittest.TestCase):
    def assert_contains_all(self, relative: str, *tokens: str) -> None:
        text = compact(read(relative))
        for token in tokens:
            with self.subTest(relative=relative, token=token):
                self.assertIn(compact(token), text)

    def test_no_letter_routes_are_evidence_labels_not_a_state_machine(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/filing-flow.md",
            "nl-tax-intake/reference/filing-paths.md",
            "nl-tax-annual-return/reference/phases/01-5-filing-status.md",
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
            "nl-tax-submit-companion/reference/annual-submit-steps.md",
        )
        for relative in relatives:
            self.assert_contains_all(
                relative,
                "invited",
                "no_letter_but_mandatory",
                "refund_claim_only",
                "filing_obligation_unresolved",
                "eur 58",
                "eur 19",
                "14 july 2026",
            )
        self.assert_contains_all(
            relatives[0],
            "eur 37,395",
            "eur 74,790",
            "not an automatic decision engine",
        )

    def test_penalty_routes_and_interest_are_not_conflated(self):
        relative = "_shared/knowledge/years/2025/annual/late-filing.md"
        self.assert_contains_all(
            relative,
            "invited return",
            "eur 469",
            "eur 6,709",
            "herinnering",
            "aanmaning",
            "10 werkdagen",
            "separate failure-to-request regime",
            "eur 3,354",
            "6 months",
            "2 weeks",
            "even when the return was filed before 1 may",
        )
        self.assertNotIn(
            "filed on time. no late-filing exposure",
            read(relative),
        )

    def test_expired_standard_extension_is_not_offered(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/filing-flow.md",
            "_shared/knowledge/years/2025/annual/late-filing.md",
            "nl-tax-annual-return/reference/phases/01-5-filing-status.md",
            "nl-tax-submit-companion/reference/annual-submit-steps.md",
        )
        for relative in relatives:
            self.assert_contains_all(
                relative,
                "16 july 2026",
                "1 may 2026",
                "closed",
                "still-future",
                "official form",
            )

    def test_jaaropgaaf_uses_exact_fiscaal_loon(self):
        relatives = (
            "nl-tax-annual-return/reference/phases/02-income.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
            "nl-tax-box1-home/reference/box1-2025.md",
            "nl-tax-field-mapper/reference/annual-field-map.md",
            "nl-tax-field-mapper/reference/mapping-principles.md",
            "nl-tax-evidence-indexer/reference/evidence-types.md",
            "_shared/knowledge/years/2025/annual/evidence-checklist.md",
        )
        for relative in relatives:
            self.assert_contains_all(relative, "fiscaal loon")
        combined = compact("\n".join(read(relative) for relative in relatives))
        self.assertIn("never subtract", combined)
        self.assertIn("informational", combined)
        self.assertNotIn("box1.arbeidskorting_loon", combined)
        self.assertNotIn(
            "gross salary from the jaaropgaaf minus employee insurance premiums",
            combined,
        )

    def test_credit_screens_keep_all_conditions_and_portal_review(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/credits.md",
            "nl-tax-annual-return/reference/phases/05-5-credits.md",
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        for relative in relatives:
            self.assert_contains_all(
                relative,
                "6 months",
                "eur 6,145",
                "31 december 2025",
                "born before 1963",
                "same fiscal partner",
                "sufficient",
            )
        combined = compact("\n".join(read(relative) for relative in relatives))
        self.assertIn("co-parent", combined)
        self.assertIn("child-death", combined)
        self.assertIn("partner-death", combined)
        self.assert_contains_all(
            relatives[0],
            "eur 58,875",
            "eur 58,876",
        )

    def test_joint_filing_is_optional_and_allocations_stay_consistent(self):
        relatives = (
            "nl-tax-annual-return/reference/phases/06-partner.md",
            "nl-tax-field-mapper/reference/annual-field-map.md",
            "_shared/knowledge/years/2025/annual/evidence-checklist.md",
            "nl-tax-submit-companion/reference/annual-submit-steps.md",
        )
        for relative in relatives:
            self.assert_contains_all(
                relative,
                "separate",
                "sign",
                "consistent",
                "100%",
            )
        self.assert_contains_all(relatives[0], "it is not mandatory")

    def test_evidence_checklist_has_current_woz_study_and_alimony_boundaries(self):
        relative = "_shared/knowledge/years/2025/annual/evidence-checklist.md"
        self.assert_contains_all(
            relative,
            "completeness checklist, not an upload list",
            "waardepeildatum 1 january 2024",
            "pre-1 july 2015",
            "duo prestatiebeurs",
            "urgent moral obligation",
            "enforced in court",
            "kinderalimentatie is not deductible",
            "manual review",
        )

    def test_box3_is_data_supply_not_method_election(self):
        relatives = (
            "_shared/knowledge/years/2025/box3/actual-return.md",
            "nl-tax-box3/reference/box3-actual-2025.md",
            "nl-tax-submit-companion/reference/annual-submit-steps.md",
            "nl-tax-field-mapper/reference/annual-field-map.md",
            "nl-tax-field-mapper/reference/mapping-principles.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        for relative in relatives:
            self.assert_contains_all(
                relative,
                "actual-return data",
                "tax-method election",
                "favorable amount",
            )

        combined = compact("\n".join(read(relative) for relative in relatives))
        self.assertNotIn("final election happens", combined)
        self.assertNotIn("opt for taxation based on", combined)

    def test_annual_aow_review_uses_transition_aware_status(self):
        relatives = (
            "nl-tax-annual-return/reference/phases/01-preflight.md",
            "nl-tax-annual-return/reference/phases/02-income.md",
            "nl-tax-annual-return/reference/phases/05-5-credits.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        for relative in relatives:
            self.assert_contains_all(relative, "aow_by_tax_year.2025")
        self.assert_contains_all(
            relatives[2],
            "reaches_during_year",
            "aow_all_year",
            "below_all_year",
            "transition month",
        )


if __name__ == "__main__":
    unittest.main()
