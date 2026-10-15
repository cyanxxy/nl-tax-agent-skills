#!/usr/bin/env python3
"""The reviewed 2025/2026 tax content cites registered official sources."""

from pathlib import Path
import unittest
from urllib.parse import urlparse

import yaml


PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "nl-tax-agent-skills"
SKILLS = PLUGIN / "skills"


class TaxContentSourceTests(unittest.TestCase):
    # (source_id, tax_year or None for all-year guidance, files that cite it)
    OFFICIAL_SOURCES = (
        (
            'bd_zorgkosten_overzicht_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_fisin_zorgkosten_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_vervoerskosten_ziekte_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_fisin_lijfrente_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_fisin_studiekosten_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_own_home_deduction_cap_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md',
                'nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md',
                'nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-box1-home/reference/own-home-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_eigenwoningforfait_multiple_homes',
            None,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md',
                'nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md',
                'nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-box1-home/reference/own-home-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_temporary_two_homes_interest',
            None,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md',
                'nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md',
                'nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-box1-home/reference/own-home-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_own_home_deduction_cap_2026',
            2026,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md',
                'nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md',
                'nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-box1-home/reference/own-home-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_eigenwoningforfait_2025_2026',
            None,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md',
                'nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md',
                'nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-box1-home/reference/own-home-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_own_home_deductible_costs',
            None,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md',
                'nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md',
                'nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-box1-home/reference/own-home-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_bijtelling_auto_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/box1-rates.md',
                'nl-tax-shared-resources/knowledge/years/2025/entrepreneur/winst-en-kosten.md',
                'nl-tax-box1-home/reference/box1-2025.md',
                'nl-tax-winst/reference/winst-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_stock_options_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/box1-rates.md',
                'nl-tax-box1-home/reference/box1-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_annual_data_checklist_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/evidence-checklist.md',
                'nl-tax-shared-resources/knowledge/years/2025/annual/credits.md',
                'nl-tax-box1-home/reference/box1-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_arbeidsinkomen_definition_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/credits.md',
                'nl-tax-box1-home/reference/box1-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_iack_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/credits.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_heffingskortingen_aow_2025_2026',
            None,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/credits.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_annual_data_checklist_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/evidence-checklist.md',
                'nl-tax-box1-home/reference/box1-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_giften_aftrek_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-partner-deductions/reference/deductions-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_zakelijke_kosten_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-shared-resources/knowledge/years/2025/entrepreneur/winst-en-kosten.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_deduction_rate_cap_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md',
                'nl-tax-partner-deductions/reference/deductions-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_annual_deadline_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/filing-flow.md',
                'nl-tax-shared-resources/knowledge/years/2025/annual/late-filing.md',
                'nl-tax-intake/reference/filing-paths.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
                'nl-tax-submit-companion/reference/annual-submit-steps.md',
                'nl-tax-shared-resources/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md',
            ),
        ),
        (
            'bd_annual_extension_eligibility_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/filing-flow.md',
                'nl-tax-shared-resources/knowledge/years/2025/annual/late-filing.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-submit-companion/reference/annual-submit-steps.md',
                'nl-tax-shared-resources/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md',
            ),
        ),
        (
            'bd_annual_extension_2025',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/filing-flow.md',
                'nl-tax-shared-resources/knowledge/years/2025/annual/late-filing.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-submit-companion/reference/annual-submit-steps.md',
                'nl-tax-shared-resources/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md',
            ),
        ),
        (
            'bd_verzuimboete',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/annual/late-filing.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
            ),
        ),
        (
            'bd_own_home_deduction_cap_2026',
            2026,
            (
                'nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md',
                'nl-tax-partner-deductions/reference/provisional-deductions-2026.md',
            ),
        ),
        (
            'bd_provisional_review_2026',
            2026,
            (
                'nl-tax-shared-resources/knowledge/years/2026/provisional/review-flow.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/vva-eva-baseline-delta.md',
                'nl-tax-provisional-assessment/SKILL.md',
                'nl-tax-provisional-assessment/reference/provisional-flow.md',
                'nl-tax-provisional-assessment/reference/provisional-output-contract.md',
                'nl-tax-provisional-assessment/reference/delta-rules.md',
                'nl-tax-provisional-assessment/templates/provisional-workpack.md',
            ),
        ),
        (
            'bd_provisional_change_2026',
            2026,
            (
                'nl-tax-shared-resources/knowledge/years/2026/provisional/change-flow.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/refund-payment-timing.md',
                'nl-tax-shared-resources/knowledge/years/2026/provisional/review-flow.md',
                'nl-tax-provisional-assessment/SKILL.md',
                'nl-tax-provisional-assessment/reference/provisional-flow.md',
                'nl-tax-provisional-assessment/reference/provisional-output-contract.md',
                'nl-tax-provisional-assessment/templates/provisional-workpack.md',
                'nl-tax-provisional-assessment/templates/provisional-workpack.md#Delta summary',
                'nl-tax-submit-companion/SKILL.md',
                'nl-tax-submit-companion/reference/provisional-submit-steps.md',
            ),
        ),
        (
            'bd_provisional_stopzetten_2026',
            2026,
            (
                'nl-tax-shared-resources/knowledge/years/2026/provisional/stopzetten-flow.md',
                'nl-tax-provisional-assessment/reference/stopzetten-guidance.md',
                'nl-tax-provisional-assessment/reference/provisional-flow.md',
                'nl-tax-provisional-assessment/reference/provisional-output-contract.md',
                'nl-tax-provisional-assessment/templates/provisional-workpack.md',
            ),
        ),
        (
            'bd_box3_2025_actual_return',
            2025,
            (
                'nl-tax-shared-resources/knowledge/years/2025/box3/actual-return.md',
                'nl-tax-box3/reference/box3-annual-2025.md',
                'nl-tax-box3/reference/box3-actual-2025.md',
                'nl-tax-annual-return/reference/annual-flow.md',
                'nl-tax-annual-return/reference/annual-output-contract.md',
                'nl-tax-annual-return/templates/annual-workpack.md',
                'nl-tax-field-mapper/reference/annual-field-map.md',
            ),
        ),
    )

    @classmethod
    def setUpClass(cls):
        register = yaml.safe_load(
            (SKILLS / "nl-tax-shared-resources/source-register.yaml").read_text(encoding="utf-8")
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

    def test_tax_content_cites_registered_official_sources(self):
        for source_id, year, relatives in self.OFFICIAL_SOURCES:
            with self.subTest(source_id=source_id, year=year):
                if year is None:
                    self.assert_official_reference(source_id, relatives)
                else:
                    self.assert_official_source(source_id, year, relatives)


if __name__ == "__main__":
    unittest.main()
