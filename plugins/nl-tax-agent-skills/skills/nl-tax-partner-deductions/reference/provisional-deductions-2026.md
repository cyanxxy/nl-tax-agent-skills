# Rule note: Deduction allocation for provisional assessment 2026

source_ids: bd_fiscal_partnership, bd_provisional_request_2026, bd_provisional_review_2026, bd_provisional_rates_2026, bd_eigenwoningforfait_2025_2026, bd_own_home_deduction_cap_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Contents

- Rule
- Same allocation rules apply
- Key difference: all amounts are estimates
- Provisional assessment uses the allocation as submitted
- Can be changed later
- Key message: keep provisional scenario comparison proportionate
- Focus areas for provisional 2026
- Interaction with provisional subflows
- Notes

## Rule

When fiscal partners submit a voorlopige aanslag (provisional assessment)
request for 2026, the allocation of deductions between partners follows the
same structural rules as the annual return. Because the provisional assessment
uses estimates rather than actual amounts, comparisons must show uncertainty
and must not rank, recommend, or select a scenario.

These are reference notes for workpack preparation -- not final tax advice.

## Same allocation rules apply

The allocation rules for the provisional assessment 2026 are structurally identical to the annual return:

- Box 3 joint grondslag sparen en beleggen: any split 0-100% between partners
- Box 3 calculation: allocate the joint grondslag sparen en beleggen, not individual assets or debts
- Eigen woning result: fiscal partners may allocate the saldo of own-home income and deductions in any split totaling 100%
- Persoonsgebonden aftrek: allocated freely between partners (with the same per-category constraints as described in `deductions-2025.md`)
- Heffingskortingen: affected indirectly by allocation choices

There are no provisional-specific allocation rules that differ from the annual return rules.

## Key difference: all amounts are estimates

For the provisional assessment:

- Income amounts are estimated (projected from current employment, pension, or benefit data).
- Deduction amounts are estimated (projected mortgage interest, expected donations, anticipated medical costs).
- Box 3 values are estimated (projected asset values on 1 January 2026 peildatum).
- The allocation is therefore applied to estimated amounts, not verified actuals.

This means:
- Any marginal-rate comparison is based on estimated income levels, which may change.
- A partner currently in the 35.75% bracket may end up in the 49.50% bracket if income changes during the year, or vice versa.
- Deduction amounts may turn out higher or lower than estimated.

## Provisional assessment uses the allocation as submitted

The Belastingdienst applies the allocation exactly as submitted in the provisional assessment request:

- If you allocate all mortgage interest to partner A, the provisional assessment for partner A reflects that full deduction and partner B reflects none.
- The monthly payment or refund amounts for each partner are based on their individual provisional assessments.
- The Belastingdienst does not choose or alter the split. The taxpayer-selected
  allocation is the allocation used for the provisional calculation.

## Can be changed later

The provisional allocation is not permanent:

- **Change the voorlopige aanslag:** if circumstances change during the year (income change, new deductions, different partner situation), a new voorlopige aanslag can be requested with a different allocation. This replaces the previous provisional assessment.
- **Annual return overrides:** the final allocation is determined in the annual return for 2026 (filed in 2027). The provisional allocation has no binding effect on the annual return. Partners can choose a completely different allocation when filing the definitive return.

This means the taxpayer-selected provisional allocation is an estimate that
affects monthly cash flow (payment or refund amounts) but not the final tax
liability.

## Key message: keep provisional scenario comparison proportionate

Because all amounts are estimates and the allocation can be changed:

1. **Avoid excessive precision.** Fine-grained comparisons of estimated amounts
   provide limited value when the actual amounts will differ.
2. **Focus on the largest items.** Compare scenarios for the items with the biggest tax impact:
   - **Mortgage interest (hypotheekrenteaftrek):** usually the largest deduction. Compare simple, traceable allocation scenarios, including the tariefsaanpassing cap and heffingskortingen or other credit effects.
   - **Box 3 grondslag:** the combined heffingsvrij vermogen is applied before
     allocation. Show a small set of 100%-total splits for the remaining joint
     grondslag sparen en beleggen and their estimated tax and credit effects;
     do not rank or select one.
3. **Use simple scenarios for smaller items.** For smaller deductions (giften, zorgkosten), show a small set of traceable allocation scenarios and their estimated cap/credit effects. Require taxpayer review; do not select an allocation automatically or label one as the default.
4. **Consider cash flow.** The provisional assessment determines monthly payment or refund amounts. An allocation that reduces one partner's monthly payment but increases the other's has no net effect on the household -- unless there is a cash flow reason to prefer one partner's account receiving the refund.

## Focus areas for provisional 2026

### Mortgage interest allocation (biggest impact)

- Show the estimated effect of the mortgage interest deduction for each partner
  under a small set of eligible splits.
- Consider the tariefsaanpassing cap (projected 2026 rate -- verify in `rates-and-credits.md`).
- If both partners are in the same bracket, allocation has minimal marginal-rate impact but may still affect heffingskortingen.
- Compare simple 100%-total scenarios based on current estimates, keep each result traceable, and require taxpayer review. Do not select the mortgage allocation automatically.

### Box 3 allocation (second biggest impact)

- Estimate combined box 3 grondslag for 2026 peildatum (1 January 2026).
- Apply the combined heffingsvrij vermogen first.
- Allocate the joint grondslag sparen en beleggen, not individual assets or debts.
- For provisional purposes, compare simple scenarios such as 50/50, 100/0, and
  0/100 rather than presenting precise percentages from uncertain estimates.

### Other deductions

- For provisional purposes, compare simple traceable scenarios for other deductions (giften, zorgkosten, alimentatie), including relevant deduction-rate cap and credit effects.
- Present the estimated results for taxpayer review and do not choose a default
  or automatic allocation. More detailed scenario analysis can wait for the
  annual return when actual amounts are known.

## Interaction with provisional subflows

- **Request:** initial allocation is set when requesting the first voorlopige aanslag. Use reasonable estimates and the guidance above.
- **Change:** when changing the voorlopige aanslag, the entire income and deduction picture is re-entered. The allocation can be revised at this point.
- **Review:** when reviewing an existing voorlopige aanslag, check whether the current allocation is still reasonable given any changes in circumstances (income change, new deduction, partner status change).
- **Stopzetten:** stopping does not involve allocation choices and is only available for monthly refund cases. Payment corrections must use the change subflow.

## Allocation arithmetic check

The agent determines fiscal-partner status and row allocatability from the
reviewed sources before checking a provisional scenario. Record
`has_fiscal_partner` as a real boolean on the wrapped scenario and
`allocatable` as a real boolean on every row. Never infer either value from a
row name or use a missing-value default.

For each row, `taxpayer_pct` and `partner_pct` must be finite numbers from 0
through 100 and total 100. An explicitly non-allocatable row must be 100/0 or
0/100, and `partner_pct` must be 0 when `has_fiscal_partner` is false. Apply
these invariants manually and record `check_performed_by: checked_by_agent`, or
record `check_performed_by: checked_by_script` after the optional helper checks
the same explicit payload. Python availability never blocks the workpack.

## Notes

- The provisional assessment for 2026 uses ONLY the fictitious return method for box 3. Werkelijk rendement is not relevant for the provisional and should not be considered in allocation calculations.
- Provisional 2026 rates differ from annual 2025 rates. Always use the rates from `rates-and-credits.md` for 2026, not the 2025 annual rates.
- If the partner situation is uncertain (e.g., considering moving in together, possible separation), advise filing the provisional assessment based on the current situation and changing it if the situation changes.
