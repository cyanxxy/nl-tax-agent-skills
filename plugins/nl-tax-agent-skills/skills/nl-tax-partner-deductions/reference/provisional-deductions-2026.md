# Rule note: Deduction allocation for provisional assessment 2026

source_id: bd_fisin_2026_prov_deduction_alloc
workflow: provisional-assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

When fiscal partners submit a voorlopige aanslag (provisional assessment) request for 2026, the allocation of deductions between partners follows the same structural rules as the annual return. However, because the provisional assessment is based on estimates rather than actual amounts, the allocation strategy must account for uncertainty.

These are reference notes for workpack preparation -- not final tax advice.

## Same allocation rules apply

The allocation rules for the provisional assessment 2026 are structurally identical to the annual return:

- Box 3 assets and debts: any split 0-100% between partners
- Eigen woning result: allocated to one partner (or by ownership share for co-owners)
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
- The marginal-rate optimization is based on estimated income levels, which may change.
- A partner currently in the 35.82% bracket may end up in the 49.50% bracket if income changes during the year, or vice versa.
- Deduction amounts may turn out higher or lower than estimated.

## Provisional assessment uses the allocation as submitted

The Belastingdienst applies the allocation exactly as submitted in the provisional assessment request:

- If you allocate all mortgage interest to partner A, the provisional assessment for partner A reflects that full deduction and partner B reflects none.
- The monthly payment or refund amounts for each partner are based on their individual provisional assessments.
- There is no automatic optimization by the Belastingdienst. The allocation you submit is the allocation they use.

## Can be changed later

The provisional allocation is not permanent:

- **Change the voorlopige aanslag:** if circumstances change during the year (income change, new deductions, different partner situation), a new voorlopige aanslag can be requested with a different allocation. This replaces the previous provisional assessment.
- **Annual return overrides:** the final allocation is determined in the annual return for 2026 (filed in 2027). The provisional allocation has no binding effect on the annual return. Partners can choose a completely different allocation when filing the definitive return.

This means the provisional allocation is a best-estimate choice that affects monthly cash flow (payment or refund amounts) but not the final tax liability.

## Key message: do not over-optimize provisional allocation

Because all amounts are estimates and the allocation can be changed:

1. **Avoid excessive precision.** Spending time finding the mathematically optimal allocation for estimated amounts provides limited value when the actual amounts will differ.
2. **Focus on the largest items.** Optimize allocation for the items with the biggest tax impact:
   - **Mortgage interest (hypotheekrenteaftrek):** usually the largest deduction. Allocate to the partner where it provides the most benefit, considering the tariefsaanpassing cap.
   - **Box 3 grondslag:** allocate to make best use of both partners' heffingsvrij vermogen. A straightforward approach is to split box 3 so that neither partner has unused heffingsvrij vermogen.
3. **Use reasonable defaults for smaller items.** For smaller deductions (giften, zorgkosten), a simple allocation (e.g., to the higher-earning partner) is sufficient. Fine-tuning these can wait for the annual return.
4. **Consider cash flow.** The provisional assessment determines monthly payment or refund amounts. An allocation that reduces one partner's monthly payment but increases the other's has no net effect on the household -- unless there is a cash flow reason to prefer one partner's account receiving the refund.

## Focus areas for provisional 2026

### Mortgage interest allocation (biggest impact)

- Determine which partner benefits more from the mortgage interest deduction.
- Consider the tariefsaanpassing cap (projected 2026 rate -- verify in `rates-and-credits.md`).
- If both partners are in the same bracket, allocation has minimal marginal-rate impact but may still affect heffingskortingen.
- For the provisional: a reasonable allocation based on current income levels is sufficient.

### Box 3 allocation (second biggest impact)

- Estimate combined box 3 grondslag for 2026 peildatum (1 January 2026).
- Allocate to maximize use of both partners' heffingsvrij vermogen.
- If combined grondslag exceeds 2x heffingsvrij vermogen, allocate the excess to the partner with the lower overall tax burden (but for provisional purposes, an even split of the excess is a reasonable default).

### Other deductions

- For provisional purposes, allocate other deductions (giften, zorgkosten, alimentatie) to the higher-earning partner as a default.
- Detailed optimization of these items is better left to the annual return when actual amounts are known.

## Interaction with provisional subflows

- **Request:** initial allocation is set when requesting the first voorlopige aanslag. Use reasonable estimates and the guidance above.
- **Change:** when changing the voorlopige aanslag, the entire income and deduction picture is re-entered. The allocation can be revised at this point.
- **Review:** when reviewing an existing voorlopige aanslag, check whether the current allocation is still reasonable given any changes in circumstances (income change, new deduction, partner status change).
- **Stopzetten:** stopping the provisional assessment does not involve allocation choices. It stops the monthly payments or refunds entirely.

## Notes

- The provisional assessment for 2026 uses ONLY the fictitious return method for box 3. Werkelijk rendement is not relevant for the provisional and should not be considered in allocation calculations.
- Provisional 2026 rates may differ from annual 2025 rates. Always use the rates from `rates-and-credits.md` for 2026, not the 2025 annual rates.
- If the partner situation is uncertain (e.g., considering moving in together, possible separation), advise filing the provisional assessment based on the current situation and changing it if the situation changes.
