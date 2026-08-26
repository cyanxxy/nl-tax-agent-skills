#!/usr/bin/env python3
"""Regression contracts for the non-security provisional-content audit."""

from pathlib import Path
import unittest


PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "nl-tax-agent-skills"


def read(relative_path):
    return (PLUGIN / relative_path).read_text(encoding="utf-8")


class ProvisionalContentAuditRepairTests(unittest.TestCase):
    def assert_all_contain(self, paths, *phrases):
        for path in paths:
            text = " ".join(read(path).lower().split())
            with self.subTest(path=path):
                for phrase in phrases:
                    self.assertIn(phrase.lower(), text)

    def test_stopzetten_separates_timing_repayment_and_filing(self):
        core_paths = (
            "skills/_shared/knowledge/years/2026/provisional/stopzetten-flow.md",
            "skills/nl-tax-provisional-assessment/reference/stopzetten-guidance.md",
            "skills/nl-tax-provisional-assessment/reference/subflows/stopzetten.md",
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md",
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
        )
        self.assert_all_contain(core_paths, "1 january 2026", "iack")
        self.assert_all_contain(
            core_paths[:4],
            "algemene heffingskorting",
            "prospective",
        )
        self.assert_all_contain(
            core_paths[:4],
            "separate",
            "repayment",
        )
        self.assert_all_contain(
            core_paths,
            "filing",
        )
        for path in core_paths:
            text = read(path).lower()
            with self.subTest(path=path):
                self.assertNotIn(
                    "filing the annual return is required regardless",
                    text,
                )
                self.assertNotIn("annual return is still required", text)

    def test_aow_has_three_states_and_transition_month(self):
        profile = read("skills/nl-tax-intake/templates/taxpayer-profile.yaml")
        aow = read("skills/_shared/knowledge/aow/aow-leeftijd.md")
        rates = read(
            "skills/_shared/knowledge/years/2026/provisional/rates-and-credits.md"
        )
        skill = read("skills/nl-tax-provisional-assessment/SKILL.md")
        pack = read(
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md"
        )
        for text in (profile, aow, rates, skill, pack):
            with self.subTest(text=text[:60]):
                self.assertIn("below_all_year", text)
                self.assertIn("reaches_during_year", text)
                self.assertIn("aow_all_year", text)
        for text in (profile, aow, rates, skill, pack):
            self.assertIn("transition", text.lower())
        self.assertIn("manual portal", " ".join(aow.split()).lower())
        self.assertIn("live portal result", " ".join(skill.split()).lower())
        resume = read(
            "skills/nl-tax-provisional-assessment/reference/resume-contract.md"
        ).lower()
        self.assertIn("reference/resume-contract.md", skill)
        self.assertIn(
            "conversational profile normalization",
            " ".join(resume.split()),
        )
        self.assertIn("not a script or tax-decision engine", " ".join(resume.split()))

    def test_2026_aow_transition_month_rates_are_bundled(self):
        rates = read(
            "skills/_shared/knowledge/years/2026/provisional/rates-and-credits.md"
        )
        compact = " ".join(rates.split())
        for month, percentage in (
            ("January", "17.85%"),
            ("February", "19.34%"),
            ("March", "20.83%"),
            ("April", "22.32%"),
            ("May", "23.81%"),
            ("June", "25.30%"),
            ("July", "26.80%"),
            ("August", "28.29%"),
            ("September", "29.78%"),
            ("October", "31.27%"),
            ("November", "32.76%"),
            ("December", "34.25%"),
        ):
            with self.subTest(month=month):
                self.assertIn(f"| {month} | {percentage} |", rates)
        # Two official pages disagree on six of these rows by 0.01pp. The
        # belastingberekening series is used because it keeps the convention
        # both official 2025 pages share; the note must record the conflict
        # rather than silently pick a side.
        self.assertIn("bd_fisin_2026_belastingberekening", rates)
        self.assertIn("0.01 percentage point higher", rates)
        self.assertIn("published month-specific first-bracket rate", compact)
        self.assertIn("official portal result for affected credits", compact)

    def test_shared_aow_note_routes_to_the_active_workflow(self):
        aow = " ".join(
            read("skills/_shared/knowledge/aow/aow-leeftijd.md").split()
        )
        self.assertIn("annual income-tax return", aow)
        self.assertIn("Verzoek of wijziging voorlopige aanslag", aow)
        self.assertIn("aow_by_tax_year.<tax_year>.status", aow)

    def test_shared_2026_own_home_note_names_the_woz_valuation_date(self):
        own_home = " ".join(
            read("skills/_shared/knowledge/own-home/eigenwoningforfait.md").split()
        )
        self.assertIn("valuation date 1 January 2025", own_home)
        self.assertIn("labelled estimate", own_home)

    def test_provisional_box1_does_not_assume_later_annual_filing(self):
        text = " ".join(
            read("skills/nl-tax-box1-home/reference/box1-2026-provisional.md").split()
        )
        self.assertIn("If an annual return is later required or filed", text)
        self.assertNotIn("annual return (due later)", text)
        self.assertNotIn("will reconcile the provisional assessment", text)

    def test_business_profit_and_own_home_components_reach_rollup_and_delta(self):
        paths = (
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
            "skills/nl-tax-provisional-assessment/templates/delta-summary.md",
            "skills/nl-tax-provisional-assessment/reference/delta-rules.md",
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md",
            "skills/nl-tax-provisional-assessment/reference/subflows/change.md",
        )
        self.assert_all_contain(paths, "expected business profit")
        self.assert_all_contain(
            paths,
            "eigenwoningforfait",
            "total deductible own-home costs",
            "hillen",
            "box1_own_home_balance",
        )
        pack = read(paths[0]).lower()
        self.assertIn("total box 1 income before own-home balance", pack)
        self.assertIn("onderneming.geschatte_winst", pack)

    def test_own_home_woz_uses_1_january_2025(self):
        paths = (
            "skills/_shared/knowledge/years/2026/provisional/own-home.md",
            "skills/nl-tax-provisional-assessment/reference/subflows/request.md",
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
            "skills/nl-tax-field-mapper/reference/provisional-field-map.md",
        )
        self.assert_all_contain(paths, "peildatum 1 january 2025")
        field_map = read(paths[-1]).lower()
        self.assertIn("box 3 assets and qualifying debts", field_map)
        self.assertIn("peildatum 1 january 2026", field_map)

    def test_box1_estimates_use_taxable_wage_and_current_evidence(self):
        relative = "skills/nl-tax-box1-home/reference/box1-2026-provisional.md"
        text = " ".join(read(relative).lower().split())
        for phrase in (
            "fiscaal loon",
            "year-to-date payroll data",
            "current documents may still be used",
            "waardepeildatum 1 january 2025",
            "labelled fallback",
            "never add a generic percentage twice",
            "never multiply a post-start monthly payment by 12",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertNotIn("round to the nearest eur 10 or eur 100", text)

    def test_alleenstaandeouderenkorting_is_an_aow_pension_test(self):
        paths = (
            "skills/_shared/knowledge/years/2026/provisional/rates-and-credits.md",
            "skills/nl-tax-provisional-assessment/reference/subflows/review.md",
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
            "skills/nl-tax-provisional-assessment/templates/review-questions.md",
            "skills/nl-tax-field-mapper/reference/provisional-field-map.md",
            "skills/nl-tax-intake/templates/taxpayer-profile.yaml",
        )
        self.assert_all_contain(
            paths,
            "aow pension for a single person",
            "single-parent status",
        )

    def test_box3_rounding_inconsistency_defers_to_portal(self):
        paths = (
            "skills/_shared/knowledge/years/2026/provisional/box3-provisional.md",
            "skills/nl-tax-box3/reference/box3-provisional-2026.md",
            "skills/nl-tax-field-mapper/reference/provisional-field-map.md",
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md",
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
        )
        self.assert_all_contain(
            paths,
            "3 decimals",
            "2 decimals",
            "portal",
            "beschikking",
        )

    def test_box3_debts_require_qualification_screen(self):
        paths = (
            "skills/_shared/knowledge/years/2026/provisional/box3-provisional.md",
            "skills/nl-tax-box3/SKILL.md",
            "skills/nl-tax-box3/reference/box3-provisional-2026.md",
            "skills/nl-tax-provisional-assessment/SKILL.md",
            "skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md",
            "skills/nl-tax-provisional-assessment/templates/provisional-pack.md",
            "skills/nl-tax-field-mapper/reference/provisional-field-map.md",
        )
        self.assert_all_contain(
            paths,
            "inclusion/exclusion screen",
            "manual",
        )
        shared = read(paths[0]).lower()
        self.assertIn("do not treat every non-own-home debt", shared)

    def test_provisional_routing_remains_conversational_not_a_tax_engine(self):
        flow = read(
            "skills/nl-tax-provisional-assessment/reference/provisional-flow.md"
        ).lower()
        self.assertIn("conversational routing guide", flow)
        self.assertIn("not an executable state machine", flow)
        self.assertIn("tax-decision engine", flow)
        for name in ("request", "change", "review", "stopzetten"):
            subflow = read(
                f"skills/nl-tax-provisional-assessment/reference/subflows/{name}.md"
            ).lower()
            with self.subTest(subflow=name):
                self.assertIn("conversational review checkpoints", subflow)
                self.assertNotIn("### decision points", subflow)


if __name__ == "__main__":
    unittest.main()
