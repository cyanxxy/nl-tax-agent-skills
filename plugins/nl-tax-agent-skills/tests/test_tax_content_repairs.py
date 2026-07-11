#!/usr/bin/env python3
"""RED contracts for the reviewed 2025/2026 tax-content repairs."""

from pathlib import Path
import re
import unittest
from urllib.parse import urlparse

import yaml


PLUGIN = Path(__file__).resolve().parents[1]
SKILLS = PLUGIN / "skills"


class TaxContentRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register = yaml.safe_load(
            (SKILLS / "_shared/source-register.yaml").read_text(encoding="utf-8")
        )
        cls.sources = {item["id"]: item for item in register["sources"]}

    def assert_official_reference(self, source_id, relatives):
        """Validate an official registered reference without inventing a tax year."""
        self.assertIn(source_id, self.sources)
        source = self.sources[source_id]
        self.assertEqual(source.get("domain"), "belastingdienst.nl")
        parsed = urlparse(source["url"])
        self.assertEqual(parsed.scheme, "https")
        hostname = (parsed.hostname or "").lower()
        self.assertTrue(
            hostname == "belastingdienst.nl"
            or hostname.endswith(".belastingdienst.nl"),
            f"{source_id}: non-Belastingdienst URL hostname {hostname!r}",
        )
        self.assertTrue(
            source.get("source_type", "").startswith("official_"),
            f"{source_id}: source_type is not official",
        )
        snapshot = source.get("snapshot_path", "")
        if snapshot.startswith("skills/"):
            snapshot = snapshot[len("skills/") :]
        self.assertIn(
            snapshot,
            relatives,
            f"{source_id}: registered snapshot {snapshot!r} is not tested",
        )
        return source

    def assert_official_source(self, source_id, year, relatives):
        """Validate an official source and require explicit year coupling."""
        self.assertIsNotNone(year, f"{source_id}: expected tax year must be explicit")
        source = self.assert_official_reference(source_id, relatives)
        self.assertEqual(source.get("tax_year"), year)

    def read_skill_text(self, relative):
        path = SKILLS / relative
        if not path.is_file():
            self.fail(f"{relative}: required consumer file is missing")
        text = path.read_text(encoding="utf-8")
        if relative == "nl-tax-annual-return/reference/annual-flow.md":
            links = re.findall(r"\]\((phases/[^)]+\.md)\)", text)
            text += "\n".join(
                (path.parent / link).read_text(encoding="utf-8")
                for link in links
            )
        elif relative in {
            "nl-tax-provisional-assessment/SKILL.md",
            "nl-tax-provisional-assessment/reference/provisional-flow.md",
        }:
            index_path = (
                SKILLS
                / "nl-tax-provisional-assessment/reference/provisional-flow.md"
            )
            index = index_path.read_text(encoding="utf-8")
            links = re.findall(r"\]\((subflows/[^)]+\.md)\)", index)
            text += "\n" + index + "\n".join(
                (index_path.parent / link).read_text(encoding="utf-8")
                for link in links
            )
        return text.lower()

    def assert_text_contract(
        self, relative, required=(), forbidden=(), required_any=()
    ):
        text = self.read_skill_text(relative)
        for token in required:
            if token.lower() not in text:
                self.fail(f"{relative}: missing {token!r}")
        for token in forbidden:
            if token.lower() in text:
                self.fail(f"{relative}: contains forbidden {token!r}")
        for alternatives in required_any:
            if not any(token.lower() in text for token in alternatives):
                self.fail(
                    f"{relative}: missing one of semantic alternatives {alternatives!r}"
                )

    def assert_scoped_contract(
        self,
        relative,
        *,
        anchors,
        required_any,
        forbidden=(),
        before=400,
        after=3200,
    ):
        """Require related policy tokens in one bounded subject-area window."""
        text = self.read_skill_text(relative)
        positions = [
            match.start()
            for anchor in anchors
            for match in re.finditer(re.escape(anchor.lower()), text)
        ]
        if not positions:
            self.fail(f"{relative}: none of scoped anchors {anchors!r} found")
        for position in positions:
            block = text[max(0, position - before) : position + after]
            if all(
                any(token.lower() in block for token in alternatives)
                for alternatives in required_any
            ) and not any(token.lower() in block for token in forbidden):
                return
        self.fail(
            f"{relative}: no bounded policy block satisfies {required_any!r}"
        )

    def assert_normalized_equation(self, relative, equation):
        text = self.read_skill_text(relative)
        normalized = re.sub(r"[`\s]+", "", text)
        expected = re.sub(r"[`\s]+", "", equation.lower())
        if expected not in normalized:
            self.fail(f"{relative}: missing normalized equation {equation!r}")

    def assert_claim(
        self,
        source_id,
        year,
        relatives,
        *,
        required=(),
        forbidden=(),
        required_any=(),
    ):
        self.assert_official_source(source_id, year, relatives)
        for relative in relatives:
            with self.subTest(relative=relative):
                self.assert_text_contract(
                    relative,
                    required=required,
                    forbidden=forbidden,
                    required_any=required_any,
                )

    def test_healthcare_exclusions_and_manual_threshold(self):
        self.assert_claim(
            "bd_zorgkosten_overzicht_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/deductions.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("wheelchair: not deductible", "threshold: manual review"),
            forbidden=("wheelchairs and mobility aids are deductible",),
        )

    def test_own_home_balance_excludes_tariefsaanpassing(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/own-home.md",
            "_shared/knowledge/own-home/eigenwoningforfait.md",
            "_shared/knowledge/own-home/hypotheekrenteaftrek.md",
            "_shared/knowledge/years/2026/provisional/own-home.md",
            "nl-tax-box1-home/reference/own-home-2025.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        self.assert_official_source(
            "bd_own_home_deduction_cap_2025", 2025, relatives
        )
        self.assert_official_reference(
            "bd_eigenwoningforfait_multiple_homes", relatives
        )
        self.assert_official_reference("bd_temporary_two_homes_interest", relatives)
        equation = (
            "box1_own_home_balance = eigenwoningforfait - "
            "total_deductible_own_home_costs - hillen_deduction"
        )
        for relative in relatives:
            with self.subTest(relative=relative):
                self.assert_normalized_equation(relative, equation)
                self.assert_text_contract(
                    relative,
                    required=(
                        "tariefsaanpassing",
                        "one ordinary main residence",
                        "two homes",
                        "sale/purchase overlap",
                        "temporary double-home deductions",
                        "divorce use",
                        "collect facts",
                        "manual review",
                    ),
                    required_any=(
                        (
                            "separate from box1_own_home_balance",
                            "not part of box1_own_home_balance",
                            "never part of box1_own_home_balance",
                            "excluded from box1_own_home_balance",
                        ),
                    ),
                )

    def test_hillen_uses_all_qualifying_costs(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/own-home.md",
            "_shared/knowledge/own-home/eigenwoningforfait.md",
            "_shared/knowledge/own-home/hypotheekrenteaftrek.md",
            "_shared/knowledge/years/2026/provisional/own-home.md",
            "nl-tax-box1-home/reference/own-home-2025.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        self.assert_official_source(
            "bd_own_home_deduction_cap_2026", 2026, relatives
        )
        self.assert_official_reference(
            "bd_eigenwoningforfait_2025_2026", relatives
        )
        self.assert_official_reference("bd_own_home_deductible_costs", relatives)
        self.assert_claim(
            "bd_own_home_deduction_cap_2025",
            2025,
            relatives,
            required=(
                "total deductible own-home costs",
                "financing costs",
                "erfpacht",
                "opstal",
                "beklemming",
            ),
            forbidden=("eigenwoningforfait exceeds mortgage interest",),
        )

    def test_company_car_boundary_and_first_admission(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/box1-rates.md",
            "_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md",
            "nl-tax-box1-home/reference/box1-2025.md",
            "nl-tax-winst/reference/winst-2025.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        self.assert_official_source("bd_bijtelling_auto_2025", 2025, relatives)
        for relative in relatives:
            with self.subTest(relative=relative):
                self.assert_scoped_contract(
                    relative,
                    anchors=("company car", "auto van de zaak", "bijtelling"),
                    required_any=(
                        ("company car", "auto van de zaak", "bijtelling"),
                        (
                            "500 private kilometres or fewer",
                            "no more than 500 private kilometres",
                            "500 private kilometres or less",
                            "500 privékilometers of minder",
                        ),
                        ("first admission", "date of first admission", "datum eerste toelating"),
                        ("confirm", "confirmed", "verify", "known"),
                        ("manual review", "withhold the rate", "do not show", "do not present"),
                    ),
                    forbidden=("fewer than 500 private kilometres",),
                )

    def test_stock_options_use_tradability_or_election(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/box1-rates.md",
            "nl-tax-box1-home/reference/box1-2025.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        self.assert_official_source("bd_stock_options_2025", 2025, relatives)
        for relative in relatives:
            with self.subTest(relative=relative):
                self.assert_scoped_contract(
                    relative,
                    anchors=("stock option", "share option", "aandelenopt"),
                    required_any=(
                        ("stock option", "share option", "aandelenopt"),
                        ("tradability", "tradable"),
                        ("default tax point", "default taxation point", "default rule", "by default"),
                        ("election", "elect"),
                        ("manual review", "review required"),
                    ),
                    forbidden=("taxable at the moment of exercise",),
                )

    def test_akw_is_not_taxable_box1_income(self):
        self.assert_claim(
            "bd_annual_data_checklist_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/evidence-checklist.md",
                "_shared/knowledge/years/2025/annual/credits.md",
                "nl-tax-box1-home/reference/box1-2025.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("akw", "not taxable box 1 income"),
        )

    def test_zw_wazo_arbeidskorting_is_conditional(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/credits.md",
            "nl-tax-box1-home/reference/box1-2025.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        )
        self.assert_official_source(
            "bd_arbeidsinkomen_definition_2025", 2025, relatives
        )
        for relative in relatives:
            with self.subTest(relative=relative):
                self.assert_scoped_contract(
                    relative,
                    anchors=("arbeidskorting", "ziektewet", "wazo"),
                    required_any=(
                        ("zw", "ziektewet"),
                        ("wazo",),
                        ("conditional", "depends on", "depending on"),
                        ("employment relationship", "dienstbetrekking", "still employed"),
                    ),
                )

    def test_iack_is_younger_than_12_on_january_1(self):
        self.assert_claim(
            "bd_iack_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/credits.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/reference/annual-output-contract.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required_any=(
                ("under 12", "younger than 12", "younger_than_12"),
                ("1 january 2025", "1 jan 2025", "2025-01-01"),
            ),
            forbidden=("12 or under on 1 jan 2025", "12 or younger on 1 january 2025"),
        )

    def test_elderly_single_credit_uses_aow_single_person_entitlement(self):
        self.assert_claim(
            "bd_heffingskortingen_aow_2025_2026",
            2025,
            (
                "_shared/knowledge/years/2025/annual/credits.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/reference/annual-output-contract.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("aow",),
            required_any=(
                ("entitled", "entitlement"),
                ("single-person", "single person", "for a single person", "alleenstaande"),
            ),
            forbidden=("single_parent_status",),
        )

    def test_upo_is_not_payment_or_withholding_evidence(self):
        self.assert_claim(
            "bd_annual_data_checklist_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/evidence-checklist.md",
                "nl-tax-box1-home/reference/box1-2025.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("upo", "accrual or projection context only", "payment-year pension statement"),
        )

    def test_periodic_gift_cap_and_transition(self):
        self.assert_claim(
            "bd_giften_aftrek_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/deductions.md",
                "nl-tax-partner-deductions/reference/deductions-2025.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("eur 1.5 million", "transition"),
            forbidden=("periodieke giften (no threshold, no cap)", "fully deductible, no threshold or cap"),
        )

    def test_aov_is_not_an_ordinary_business_cost(self):
        self.assert_claim(
            "bd_zakelijke_kosten_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/deductions.md",
                "_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=(
                "aov",
                "private income-provision category",
                "not ordinary business costs",
                "manual review",
            ),
        )

    def test_prior_year_remainder_can_be_allocated_for_eligible_partners(self):
        self.assert_claim(
            "bd_deduction_rate_cap_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/deductions.md",
                "nl-tax-partner-deductions/reference/deductions-2025.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required_any=(
                ("prior-year", "prior year", "prior years"),
                (
                    "personal-deduction remainder",
                    "personal deduction remainder",
                    "persoonsgebonden aftrek",
                    "carryforward",
                ),
                ("eligible whole-year partners", "eligible whole-year fiscal partners", "whole-year fiscal partners"),
                ("can be allocated", "may allocate", "allocatable", "allocation"),
            ),
            forbidden=("is not reallocatable",),
        )

    def test_no_universal_higher_earner_optimization(self):
        self.assert_claim(
            "bd_deduction_rate_cap_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/deductions.md",
                "nl-tax-partner-deductions/reference/deductions-2025.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("allocation", "review"),
            forbidden=(
                "| persoonsgebonden aftrek | [to higher-rate partner]",
                "always allocate to the higher earner",
                "the higher earner is always optimal",
            ),
        )

    def test_invitation_deadline_and_conditional_14_july(self):
        self.assert_claim(
            "bd_annual_deadline_2025",
            2025,
            (
                "_shared/knowledge/years/2025/annual/filing-flow.md",
                "_shared/knowledge/years/2025/annual/late-filing.md",
                "nl-tax-intake/reference/filing-paths.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
                "nl-tax-submit-companion/reference/annual-submit-steps.md",
                "_shared/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md",
            ),
            required=("invitation letter", "no invitation", "14 july 2026"),
            forbidden=(
                "standard: 1 may 2026",
                "filed before 1 may 2026",
                "original deadline: 1 may 2026",
            ),
        )

    def test_extension_is_invitation_only_with_fixed_2025_dates(self):
        relatives = (
            "_shared/knowledge/years/2025/annual/filing-flow.md",
            "_shared/knowledge/years/2025/annual/late-filing.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-submit-companion/reference/annual-submit-steps.md",
            "_shared/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md",
        )
        self.assert_official_source(
            "bd_annual_extension_eligibility_2025", 2025, relatives
        )
        self.assert_claim(
            "bd_annual_extension_2025",
            2025,
            relatives,
            required=(
                "invitation letter",
                "before 1 may 2026",
                "no invitation",
                "extension is unavailable",
                "1 september 2026",
                "4 months",
            ),
            required_any=(
                ("another date", "different filing date"),
                ("official form", "form route"),
            ),
        )

    def test_late_penalty_is_conditional_after_escalation(self):
        self.assert_claim(
            "bd_verzuimboete",
            2025,
            (
                "_shared/knowledge/years/2025/annual/late-filing.md",
                "nl-tax-annual-return/reference/annual-flow.md",
                "nl-tax-annual-return/reference/annual-output-contract.md",
                "nl-tax-annual-return/templates/annual-return-pack.md",
            ),
            required=("herinnering", "aanmaning", "10 werkdagen"),
            required_any=(("potential exposure", "conditional exposure"),),
            forbidden=("expect a verzuimboete",),
        )

    def test_provisional_partner_allocation_uses_reviewed_scenarios_not_defaults(self):
        self.assert_official_source(
            "bd_own_home_deduction_cap_2026", 2026,
            (
                "_shared/knowledge/years/2026/provisional/own-home.md",
                "nl-tax-partner-deductions/reference/provisional-deductions-2026.md",
            ),
        )
        self.assert_text_contract(
            "nl-tax-partner-deductions/reference/provisional-deductions-2026.md",
            required=("allocation", "scenario", "review"),
            required_any=(
                ("tariefsaanpassing cap", "deduction-rate cap"),
                ("credit effects", "heffingskortingen"),
                ("do not select", "no automatic", "not automatically"),
            ),
            forbidden=(
                "allocate to the partner where it provides the most benefit",
                "use reasonable defaults for smaller items",
                "to the higher-earning partner as a default",
            ),
        )

    def test_unsolicited_va_is_possible_not_automatic(self):
        self.assert_claim(
            "bd_provisional_review_2026",
            2026,
            (
                "_shared/knowledge/years/2026/provisional/review-flow.md",
                "_shared/knowledge/years/2026/provisional/vva-eva-baseline-delta.md",
                "nl-tax-provisional-assessment/SKILL.md",
                "nl-tax-provisional-assessment/reference/provisional-flow.md",
                "nl-tax-provisional-assessment/reference/provisional-output-contract.md",
                "nl-tax-provisional-assessment/reference/delta-rules.md",
                "nl-tax-provisional-assessment/templates/provisional-pack.md",
            ),
            required=("unsolicited", "may be issued", "not guaranteed"),
            forbidden=("auto-issues", "automatically issues"),
        )

    def test_complete_change_dataset_without_zero_default_claim(self):
        self.assert_claim(
            "bd_provisional_change_2026",
            2026,
            (
                "_shared/knowledge/years/2026/provisional/change-flow.md",
                "_shared/knowledge/years/2026/provisional/refund-payment-timing.md",
                "_shared/knowledge/years/2026/provisional/review-flow.md",
                "nl-tax-provisional-assessment/SKILL.md",
                "nl-tax-provisional-assessment/reference/provisional-flow.md",
                "nl-tax-provisional-assessment/reference/provisional-output-contract.md",
                "nl-tax-provisional-assessment/templates/provisional-pack.md",
                "nl-tax-provisional-assessment/templates/delta-summary.md",
                "nl-tax-submit-companion/SKILL.md",
                "nl-tax-submit-companion/reference/provisional-submit-steps.md",
            ),
            required=("complete dataset", "verify"),
            forbidden=("omitted data defaults to zero",),
        )

    def test_moving_abroad_routes_to_residency_review(self):
        self.assert_claim(
            "bd_provisional_stopzetten_2026",
            2026,
            (
                "_shared/knowledge/years/2026/provisional/stopzetten-flow.md",
                "nl-tax-provisional-assessment/reference/stopzetten-guidance.md",
                "nl-tax-provisional-assessment/reference/provisional-flow.md",
                "nl-tax-provisional-assessment/reference/provisional-output-contract.md",
                "nl-tax-provisional-assessment/templates/provisional-pack.md",
            ),
            required=("moving abroad", "residency review", "not a categorical stopzetten reason"),
            forbidden=("moving abroad                         | stopzetten",),
        )

    def test_annual_box3_explains_both_methods_and_records_actual_complete_or_deferred(self):
        relatives = (
            "_shared/knowledge/years/2025/box3/actual-return.md",
            "nl-tax-box3/reference/box3-annual-2025.md",
            "nl-tax-box3/reference/box3-actual-2025.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/reference/annual-output-contract.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
            "nl-tax-field-mapper/reference/annual-field-map.md",
        )
        self.assert_official_source("bd_box3_2025_actual_return", 2025, relatives)
        for relative in relatives:
            with self.subTest(relative=relative):
                self.assert_scoped_contract(
                    relative,
                    anchors=("box 3", "actual return", "werkelijk rendement"),
                    required_any=(
                        ("fictitious", "forfaitair"),
                        ("actual return", "werkelijk rendement"),
                        ("complete", "deferred", "manual review", "manual_review"),
                    ),
                    forbidden=("fictitious method will apply by default",),
                    after=4200,
                )


if __name__ == "__main__":
    unittest.main()
