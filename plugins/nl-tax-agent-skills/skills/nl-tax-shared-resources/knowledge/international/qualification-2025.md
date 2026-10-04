# Rule note: qualifying nonresident preparation for 2025

source_ids: bd_intl_c_notes_2025, bd_intl_fisin_2025, bd_intl_income_statement
workflow: all
tax_year: 2025
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Official research dated 2 October 2026; human tax-content/form review pending.
This note supports sourced draft tests, not an eligibility decision.

## Conditions and proof

The 2025 guidance generally requires residence in an EU country,
Liechtenstein, Norway, Iceland, Switzerland or Bonaire/Sint Eustatius/Saba;
at least 90% of worldwide income taxed in the Netherlands; and the applicable
foreign income statement (inkomensverklaring). A nonresident who meets them is
a kwalificerend buitenlands belastingplichtige. The C explanation confirms
these conditions.
Salary alone is insufficient; Dutch-taxed and worldwide Box 1, Box 2 and
Box 3 measures must be established under Dutch rules.

Collect the income statement's stage and whether one was provided earlier
with uninterrupted continuing eligibility. The current official statement
page says a new statement is then generally unnecessary unless requested.
Otherwise the taxpayer obtains the correct-year model, has the residence
country's tax authority certify it, and sends it using current official
instructions. Do not infer continuing eligibility or store its identifying
fields. Missing required proof remains open.

## Supported preparation test

The 2025 Fisin calculation has two columns: Dutch-taxed and worldwide
income. Q totals categories A–P; U deducts the applicable R/S/T components
shown in that column. Include business, wages, pensions, other income,
substantial interests and savings/investments, with sourced zero/not
applicable answers. Own-home, income-provision and personal deductions are
not subtracted merely because ordinary taxable income deducts them.

After the exact applicable form/model measures and every component are
confirmed, call them `U_NL` and `U_world`. If both are positive:

`preparation_percentage = min(100, floor(100 × U_NL / U_world))`

The C form explanation caps the positive-income test at 100 and rounds down
to whole percentages. Compare with the inclusive 90% boundary. Record
unrounded ratio, displayed percentage, components and rule provenance.
Special branch (C 2025 explanation, question 39a): if `U_NL` is zero or
negative and `U_world` is zero or positive, the percentage is 0; if `U_NL`
is positive and `U_world` is zero or negative, the percentage is 100. The
source does not cover the remaining combination (`U_NL` zero or negative and
`U_world` negative): leave the test uncomputed and open.

The percentage establishes one condition only (the 90%-eis). Check residence
intervals, partner aggregation/eligibility and the pension/low-income
exception separately. The 2025 Fisin guidance computes the benefits of a
kwalificerend buitenlands belastingplichtige, including the tax part of the
heffingskortingen, time-proportionally when the taxpayer lived in a
qualifying country for only part of the year; record the exact qualifying
interval and do not apply a ratio without it.

A non-qualifying nonresident outside the Belgium, Suriname and Aruba rules
has no fiscal partner and no deductions (aftrekposten); only the tax parts of
the arbeidskorting and the inkomensafhankelijke combinatiekorting can apply.
Belgium, Suriname and Aruba can have benefits outside ordinary qualification;
for those countries do not automatically deny all deductions below the
boundary. Country-specific deduction/credit and partner treatment remains
review work.

## Official sources

- bd_intl_c_notes_2025: https://download.belastingdienst.nl/belastingdienst/docs/toelichting_c_biljet_ib3161t51fd.pdf
- bd_intl_fisin_2025: https://www.belastingdienst.nl/wps/wcm/connect/fisin/fisin2025/u_woont_buiten_nederland
- bd_intl_income_statement: https://www.belastingdienst.nl/wps/wcm/connect/nl/buitenland/content/inkomensverklaring-aangifte-inkomstenbelasting-buitenlandse-belastingplichtigen
