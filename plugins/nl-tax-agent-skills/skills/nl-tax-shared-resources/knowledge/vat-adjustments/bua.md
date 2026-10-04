# Rule note: BUA gifts and staff facilities

source_ids: bd_vat_bua_scope, bd_vat_bua_threshold, bd_vat_bua_exceptions, bd_vat_bua_contribution_policy, bd_vat_year_end_adjustments
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Draft source summary; human tax-content review is required.

BUA can exclude deduction for staff facilities, gifts and relationship gifts.
For a gift/relationship benefit, determine whether the beneficiary would have
less than 30% VAT deduction if buying it themselves; that condition and the
recipient's annual threshold matter. Do not automatically deny every business
gift above a spending amount. Staff car private use follows car rules, not
an additional BUA correction. Food/canteen, bicycles, outplacement, necessary
relocation, and food donations have distinct rules; classify them before using
the ordinary-benefit formula.

For ordinary covered benefits, aggregate eligible costs excluding VAT per
anonymous beneficiary per bookyear. Direct costs go to that person; group costs
use the number able to use the facility. Use reasonable evidenced depreciation
for a capital facility. Cash benefits without VAT are not VAT costs. At totals
no higher than EUR 227 excluding VAT, the BUA threshold does not exclude
deduction; normal taxable-use requirements still apply. Above it, the affected
deducted VAT is excluded, not merely VAT on the excess over the threshold.

For 2025 and 2026, employee/relationship contributions do not reduce costs for
the EUR 227 test. The removal of that reduction applies from 2024. VAT must be
accounted for on contributions. Where the threshold is exceeded, VAT already
paid on the related contribution reduces the VAT to repay on those benefits.
Supported ordinary arithmetic is repayment = max(0, affected VAT actually
deducted − contribution VAT already accounted for), bounded to the same
benefit/recipient pool. Record contribution VAT separately; do not credit it
twice or subtract unrelated output VAT. If input VAT was excluded initially,
do not repay it again. The owner corrects year-end input VAT for the established
BUA adjustment and preserves contribution output VAT separately.

Return incomplete beneficiary coverage and special-benefit classification as
explicit questions. Do not infer a complete annual threshold from one quarter
or one gift invoice.

## Canonical repository parity data

```yaml
vat_adjustment_policy:
  bua_threshold_ex_vat: '227'
  gift_recipient_deduction_boundary: '0.30'
```

## Official sources

- bd_vat_bua_scope: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/personeelsvoorzieningen_en_relatiegeschenken/
- bd_vat_bua_threshold: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/personeelsvoorzieningen_en_relatiegeschenken/drempelbedrag_personeelsvoorzieningen_giften_en_relatiegeschenken
- bd_vat_bua_exceptions: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/personeelsvoorzieningen_en_relatiegeschenken/toegestane_aftrek_personeelsvoorzieningen
- bd_vat_bua_contribution_policy: https://zoek.officielebekendmakingen.nl/stcrt-2023-28124.html
- bd_vat_year_end_adjustments: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/btw-aangifte-waar-moet-u-aan-denken/laatste-btw-aangifte-van-het-jaar
