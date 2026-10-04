# Rule note: Direct attribution and taxable/exempt pro-rata

source_ids: bd_vat_mixed_taxable_exempt, bd_vat_deduction_ratio, bd_vat_ordinary_revision, bd_vat_deduction_policy, bd_vat_deduction_policy_amendment_2025, bd_vat_deduction_policy_amendment_2026
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Draft source summary; human tax-content review is required.

First allocate eligible invoice VAT directly: taxable-only costs are deductible,
exempt-only costs are not. Apply a ratio only to genuinely shared costs, after
separate private-use and other deduction exclusions. Do not reduce directly
attributable taxable costs by a blanket business-wide ratio.

For ordinary shared goods/services, the initial ratio is eligible taxable
turnover excluding VAT divided by relevant total taxable plus exempt turnover
excluding VAT for the invoice's filing period. Convert that fraction to a
percentage and round upward to a whole percentage before applying it to VAT:
69.4% becomes 70%, so a EUR 1,000 shared-VAT pool gives EUR 700. Apply the same
turnover-percentage rule when determining the final annual ratio. This is
distinct from rounding euro entries and from an accepted actual-use key. The
authority for the upward rounding is the deduction decree, Stcrt. 2020, 63000,
paragraph 3.3.4.2 (bd_vat_deduction_policy: "waarbij op hele procenten naar
boven wordt afgerond"). The bd_vat_deduction_ratio worked example (2/3 of
EUR 2,100 = EUR 1,400) is illustrative and unrounded; under the decree rule the
ratio is 67% and the deduction is EUR 1,407. Do not copy the example amount and
do not report it as a source conflict.

Disposal of business-used goods is normally excluded from the turnover ratio.
Include it when the sale is a usual economic activity or is inseparable from,
or a necessary extension of, that activity. Unclear classification blocks that
denominator item, not every shared-cost calculation. Zero denominator does not
mean zero deduction; it needs an evidenced prospective-use determination. Financial,
incidental, subsidies, foreign supplies and other ambiguous denominator items
require classification before calculation. A zero-rated taxable supply is not
an exempt supply merely because no VAT was charged.

Initial shared deduction = shared eligible invoice VAT × period ratio.
For a simple pool used immediately, year-end final deduction = shared eligible
annual VAT × accepted annual ratio. Delta = final entitlement minus total net
deduction already claimed, including prior adjustments. A positive delta adds
input VAT; a negative delta reduces it. This is a reconciliation of the full
ordinary pool, not a capital-good one-fifth adjustment. Where first use follows
the invoice period, reconcile at first use and again at year end using the
deductions actually remaining after the earlier change.

An evidenced actual-use key can replace turnover under the applicable policy
when it reflects ordinary shared goods/services as a whole. Before 1 July 2025,
apply the base decree's objective more-accurate-use test; from that date use the
amendment's objectively and accurately determinable data wording. Do not
apply the changed wording retroactively to an earlier 2025 period. Do not
round an actual-use key upward under the turnover rule or cherry-pick cost-by-cost keys
to increase deduction. Capital goods have item-level analysis; read revision
rules. Alternative allocation eligibility that is unsettled remains a question,
while arithmetic on an already accepted key is supported. Return period ratio,
annual ratio, prior net claim, unrounded delta, relevant invoices and timing to
the VAT owner. Do not copy a tentative period ratio into a final-year answer.

The 2026 amendment (Stcrt. 2026, 29217) took effect on 25 August 2026, changes
investment-service and VvE (vereniging van eigenaren) provisions, and leaves
the turnover-percentage rounding rule intact. Its investment-service provisions
belong to the investment-service regime that applies to services first used on
or after 1 January 2026, and they are not authority for a service first used in
2025. Its VvE condition for the member-deduction approval (the association did
not acquire the goods or services as an entrepreneur, replacing the earlier
condition that the association does not qualify as an entrepreneur) is described
by the decree as a clarification that also covers existing situations, so it
may be applied to an open 2025 or 2026 period. The member's deductible share
still follows the member's documented financial contribution to the association
and the member's own taxable use.

## Canonical repository parity data

```yaml
vat_adjustment_policy:
  turnover_pro_rata_percentage_scale: 100
  turnover_pro_rata_rounding: ceiling
```

## Official sources

- bd_vat_mixed_taxable_exempt: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/belaste_en_vrijgestelde_omzet/
- bd_vat_deduction_ratio: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/belaste_en_vrijgestelde_omzet/inschatting_van_het_gebruik2/inschatting_van_het_gebruik
- bd_vat_ordinary_revision: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/belaste_en_vrijgestelde_omzet/inschatting_van_het_gebruik2/herziening_aftrek_niet_investeringsgoederen_en_diensten
- bd_vat_deduction_policy: https://zoek.officielebekendmakingen.nl/stcrt-2020-63000.html
- bd_vat_deduction_policy_amendment_2025: https://zoek.officielebekendmakingen.nl/stcrt-2024-38540.html
- bd_vat_deduction_policy_amendment_2026: https://zoek.officielebekendmakingen.nl/stcrt-2026-29217.html
