# Rule note: Own home (eigen woning) rules for 2025

source_ids: bd_own_home_deduction_cap_2025, bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes, bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-10"
review_status: reviewed

## Rule

The eigen woning (owner-occupied home) is taxed in box 1 through the eigenwoningforfait and all qualifying deductible own-home costs. The workpack separates the taxable own-home balance from the tax-benefit rate adjustment.

These are reference notes for workpack preparation -- not final tax advice.

### Calculation and review contract

- `total_deductible_own_home_costs = mortgage interest + qualifying financing costs + periodic erfpacht/opstal/beklemming`.
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Hillen uses `total_deductible_own_home_costs`, not mortgage interest alone.
- `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
- Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and must never be added to taxable Box 1 income.
- Optional helper fields are review inputs only. The agent verifies the cited evidence and retains incomplete or uncertain qualifications as manual review.
- One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review.

## Eigenwoningforfait (deemed rental value)

The eigenwoningforfait is a deemed income percentage applied to the WOZ-waarde (official property valuation) of the taxpayer's primary residence.

### 2025 percentages

| WOZ-waarde                             | Eigenwoningforfait              |
|----------------------------------------|---------------------------------|
| Up to EUR 12,500                       | 0%                              |
| EUR 12,500 to EUR 25,000              | 0.10%                           |
| EUR 25,000 to EUR 50,000              | 0.20%                           |
| EUR 50,000 to EUR 75,000              | 0.25%                           |
| EUR 75,000 to EUR 1,330,000           | 0.35%                           |
| Above EUR 1,330,000                   | EUR 4,655 + 2.35% of excess over EUR 1,330,000 |

The most common bracket is EUR 75,000 to EUR 1,330,000 at 0.35%. For example, a property with WOZ-waarde of EUR 400,000 has an eigenwoningforfait of EUR 1,400 (400,000 x 0.35%).

### WOZ-waarde determination

- The WOZ-waarde is set annually by the municipality (gemeente) via the WOZ-beschikking.
- The 2025 return uses the WOZ-waarde with valuation date (waardepeildatum) 1 January 2024.
- The taxpayer should verify the WOZ-waarde against their beschikking. If the value seems too high, they may have filed a bezwaar (objection) -- use the corrected value if applicable.

## Hypotheekrenteaftrek (mortgage interest deduction)

Mortgage interest paid on the eigen woning loan is deductible in box 1.

### Qualifying conditions

1. The loan must be used to purchase, improve, or maintain the eigen woning (the taxpayer's primary residence).
2. For mortgages taken out on or after 1 January 2013: the mortgage must be annuitair (annuity-based) or lineair (linear repayment). Interest-only (aflossingsvrij) mortgages taken after this date do not qualify for interest deduction.
3. For mortgages taken out before 1 January 2013: interest-only mortgages still qualify under transitional rules (overgangsrecht), provided the loan has not been materially changed.
4. Maximum deduction period: 30 years from the date the loan was taken out.

### What is deductible

- Mortgage interest (hypotheekrente) paid during the calendar year
- Qualifying one-off mortgage financing costs (e.g., notarial costs for the mortgage deed, appraisal fees for obtaining the loan, NHG application costs) -- deductible at once in the year paid
- Periodic payments for erfpacht, opstal, or beklemming
- Penalty interest (boeterente) for early repayment in certain situations

### What is NOT deductible

- Principal repayments (aflossingen)
- Home insurance premiums
- Maintenance costs (these are for the homeowner's account and not tax-deductible)

## Tariefsaanpassing eigen woning (rate adjustment for high-income earners)

For taxpayers with box 1 income in the highest bracket (schijf 3, above EUR 76,817 at 49.50%), the effective tax benefit of deductible own-home costs is capped.

### 2025 cap

- In 2025, deductible own-home costs are effectively limited to 37.48% (the schijf 2 rate).
- This means that for high-income taxpayers, the portion of own-home costs that would otherwise be deductible at 49.50% is only deductible at 37.48%.
- The difference (49.50% - 37.48% = 12.02% of the deductible own-home costs falling in schijf 3) is added back as a tariefsaanpassing, reducing the tax benefit.
- Keep this adjustment in its own review table; it does not change the taxable own-home balance.

### Calculation in the workpack

1. Calculate the gross eigenwoningforfait based on WOZ-waarde
2. Determine `total_deductible_own_home_costs`, including mortgage interest, qualifying financing costs, and periodic erfpacht/opstal/beklemming
3. Calculate Hillen against that total when applicable
4. Calculate `box1_own_home_balance` using the contract above
5. If the taxpayer's income falls in schijf 3, record the tariefsaanpassing separately and note the reduced tax benefit

## Hillenregeling (aftrek geen of geringe eigenwoningschuld)

The Hillenregeling reduces a positive own-home balance when a homeowner has no or low qualifying deductible own-home costs. The comparison uses the total of mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.

### Phase-out status for 2025

- The Hillenregeling (aftrek wegens geen of geringe eigenwoningschuld) is being gradually phased out. The phase-out began in 2019 and was accelerated: the annual reduction increased from 3.33 to 4.8 percentage points from 2026 onward.
- In 2025, 76.667% of the difference between the eigenwoningforfait and deductible own-home costs is taken into account; in 2026 this drops to 71.867%.
- Because the annual reduction is no longer a constant step, use the stored per-year percentage for each tax year rather than extrapolating a flat 1/30th reduction.
- From 1 January 2041 the aftrek is fully phased out (the original 2048 end date was brought forward to 2041).

### When it applies

- The Hillenregeling is relevant for homeowners who have fully or substantially paid off their mortgage.
- For these taxpayers, the eigenwoningforfait effectively becomes taxable income in box 1 (partially offset by the remaining Hillenregeling benefit).
- The workpack should note the Hillenregeling calculation for taxpayers with low or zero mortgage debt.

## Fiscal partner and eigen woning

- Fiscal partners may allocate the saldo of own-home income and deductions in the return.
- The allocation must be consistent across both partners and total 100%.

## Moving during 2025

- The workpack may prepare a review estimate only for one ordinary main residence.
- For two homes, sale/purchase overlap, temporary double-home deductions, divorce use, or another complex case, collect registration/move dates, both addresses, sale/listing and vacancy/rental status, expected occupancy, mortgage evidence, and use arrangements.
- Route the qualification and period calculation to manual review rather than determining a standard filing amount.

## Notes

- The WOZ-waarde used for 2025 is the value set by the municipality with waardepeildatum 1 January 2024.
- The eigenwoningforfait percentage of 0.35% has been adjusted over the years; always use the percentage valid for the relevant tax year.
- The tariefsaanpassing rate (37.48% cap) is part of the broader policy to gradually reduce the benefit of mortgage interest deduction for higher incomes.
- For the workpack: collect the WOZ-beschikking and mortgage annual statement (jaaroverzicht hypotheek) as evidence. See evidence-checklist.md.
