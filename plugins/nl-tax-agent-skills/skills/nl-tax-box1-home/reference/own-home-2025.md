# Eigen Woning (Own Home) Rules — Annual Return 2025

source_ids: bd_own_home_deduction_cap_2025, bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes, bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest, bd_fiscal_partnership
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-10"
review_status: reviewed

## Contents

- Purpose
- Eigenwoningforfait calculation
- Hypotheekrenteaftrek (mortgage interest deduction)
- Tariefsaanpassing eigen woning (rate adjustment for high earners)
- Hillenregeling (aftrek wegens geen of geringe eigenwoningschuld)
- Multiple own-home situations
- Missing data flags
- Notes

## Purpose

This reference describes the detailed eigen woning rules for the annual return 2025. It covers eigenwoningforfait calculation, hypotheekrenteaftrek, tariefsaanpassing, Hillenregeling, and edge cases for property changes during the year.

These are reference notes for workpack preparation -- not final tax advice.

## Own-home calculation contract

- `total_deductible_own_home_costs = mortgage interest + qualifying financing costs + periodic erfpacht/opstal/beklemming`.
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Hillen compares eigenwoningforfait with `total_deductible_own_home_costs`, not mortgage interest alone.
- `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
- `box1_balance_components` contains only eigenwoningforfait, `total_deductible_own_home_costs`, and `hillen_deduction`.
- Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and must not be added to taxable Box 1 income.
- Put tariefsaanpassing under `review_adjustments`, never in `box1_balance_components`.
- Record `check_performed_by: checked_by_agent` after the manual check or `check_performed_by: checked_by_script` after the optional helper checks the same accepted amounts.
- Optional helper fields are review inputs. The agent verifies them against the evidence and keeps missing or uncertain qualification facts visible for manual review.
- One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review.

---

## Eigenwoningforfait calculation

The eigenwoningforfait is a deemed rental income amount based on the WOZ-waarde of the taxpayer's primary residence. It is added to box 1 income.

### 2025 percentages by WOZ-waarde range

| WOZ-waarde range | Percentage | Example |
|-----------------|-----------|---------|
| Up to EUR 12,500 | 0.00% | EUR 10,000 -> EUR 0 |
| EUR 12,500 to EUR 25,000 | 0.10% | EUR 20,000 -> EUR 20 |
| EUR 25,000 to EUR 50,000 | 0.20% | EUR 40,000 -> EUR 80 |
| EUR 50,000 to EUR 75,000 | 0.25% | EUR 60,000 -> EUR 150 |
| EUR 75,000 to EUR 1,330,000 | 0.35% | EUR 400,000 -> EUR 1,400 |
| Above EUR 1,330,000 | EUR 4,655 + 2.35% of excess | EUR 1,500,000 -> EUR 8,650 |

The vast majority of Dutch homes fall in the EUR 75,000 to EUR 1,330,000 bracket. Use 0.35% as the standard calculation unless the WOZ-waarde falls outside this range.

### WOZ-waarde source

- The WOZ-waarde is determined annually by the municipality via the WOZ-beschikking
- For tax year 2025, the relevant WOZ-waarde has waardepeildatum (valuation reference date) 1 January 2024
- If the taxpayer objected (bezwaar) to the WOZ-waarde and received a corrected value, use the corrected value
- The WOZ-beschikking is a required evidence document

### Calculation steps

1. Obtain the WOZ-waarde from the WOZ-beschikking (or taxpayer-provided value)
2. Determine the applicable percentage from the table above
3. Multiply: eigenwoningforfait = WOZ-waarde x percentage
4. Round to whole euros

---

## Hypotheekrenteaftrek (mortgage interest deduction)

Mortgage interest paid on the eigen woning loan is deductible from box 1 income. This typically results in a negative eigen woning amount (deduction) when interest exceeds the eigenwoningforfait.

### Qualifying conditions for the mortgage

1. **Purpose:** the loan must be used to purchase, improve, or maintain the primary residence (eigen woning)
2. **Repayment requirement for post-2013 mortgages:** mortgages taken out on or after 1 January 2013 must follow an annuitair (annuity) or lineair (linear) repayment schedule. Interest-only (aflossingsvrij) mortgages taken after this date do NOT qualify for interest deduction.
3. **Pre-2013 transitional rules (overgangsrecht):** mortgages taken out before 1 January 2013 retain interest deductibility even if aflossingsvrij, provided the loan has not been materially changed (e.g., increased, refinanced with new terms).
4. **Primary residence requirement:** the property must be the taxpayer's hoofdverblijf (main residence). Holiday homes, rental properties, and second homes do not qualify.
5. **Maximum deduction period:** 30 years from the date the loan was first taken out.

### Deductible items

- Mortgage interest (hypotheekrente) paid during calendar year 2025
- Qualifying one-off mortgage financing costs in the year paid (for example mortgage-advice/intermediary fees, mortgage-deed notary costs, mortgage-deed cadastral fees, valuation costs for obtaining the loan, NHG application costs)
- Penalty interest (boeterente) for early repayment, under specific conditions
- Periodic payments for erfpacht, opstal, or beklemming

### Non-deductible items

- Principal repayments (aflossingen)
- Home insurance premiums (opstalverzekering, inboedelverzekering)
- Maintenance and renovation costs
- Purchase costs such as transfer tax, purchase broker fees, and purchase-deed notary or cadastral fees

### Evidence required

- Hypotheek jaaroverzicht (mortgage annual statement) showing interest paid, principal repaid, and remaining debt
- If the mortgage was taken out or changed during 2025: the mortgage deed or amendment documentation

---

## Tariefsaanpassing eigen woning (rate adjustment for high earners)

For taxpayers whose box 1 income exceeds the schijf 2 boundary (EUR 76,817 in 2025), the effective tax benefit of deductible own-home costs is limited.

### 2025 rules

- The maximum effective deduction rate for own-home deductible costs is capped at 37.48% (the schijf 2 rate)
- Taxpayers in schijf 3 (49.50%) do not get the full 49.50% tax benefit on those costs
- The tariefsaanpassing adds back the difference: (49.50% - 37.48%) = 12.02% of the deductible own-home costs that fall within the schijf 3 portion of income
- Record the amount only in a separate tax-benefit-adjustment review table; it does not change `box1_own_home_balance`.

### When tariefsaanpassing applies

- The taxpayer's box 1 taxable income (before eigen woning deduction) exceeds EUR 76,817
- The taxpayer has deductible own-home costs

### When tariefsaanpassing does NOT apply

- Income is below EUR 76,817 (entirely in schijf 1 and/or schijf 2)
- No deductible own-home costs are deducted

### Calculation approach

The bundled `scripts/validate_own_home_inputs.py` follows the official
Belastingdienst grondslag method rather than applying the rate gap directly to the
own-home costs:

1. Determine belastbaar inkomen uit werk en woning (the box 1 taxable income after
   the eigen woning deduction, after the Hillenregeling adjustment).
2. Build the grondslag voor tariefsaanpassing, **capped at the deducted own-home
   costs** (art. 2.10 lid 2 Wet IB 2001):
   `grondslag = min(afgetrokken eigenwoningkosten, max(0, belastbaar inkomen + afgetrokken eigenwoningkosten - drempel))`,
   where the drempel is the schijf boundary (EUR 76,817 in 2025). It applies only
   when income WITHOUT the deduction (belastbaar inkomen + costs) exceeds the drempel.
3. The tariefsaanpassing is `grondslag x (schijf 3 rate - cap rate)` =
   `grondslag x (49.50% - 37.48%)`, recorded as an adjustment that reduces the net
   tax benefit of the deduction. Because the grondslag is capped at the deducted
   costs, the correction can never exceed `(49.50% - 37.48%) x deducted costs`. The
   Belastingdienst computes the definitive figure automatically in the aangifte.
4. If income context is not yet available when this skill runs, output a WARNING
   that tariefsaanpassing may apply and must be checked by the calling skill.

The optional script accepts only ordinary-home amounts that the agent has
already reviewed. The agent decides residence status, cost qualification,
ownership or partner shares, and whether the home situation is too complex for
this arithmetic check.

---

## Hillenregeling (aftrek wegens geen of geringe eigenwoningschuld)

The Hillenregeling provides relief for homeowners who have paid off their mortgage fully or substantially. It reduces the positive own-home balance when the eigenwoningforfait is greater than all qualifying deductible own-home costs.

### Phase-out status for 2025

For 2025, 76.667% of the difference between the eigenwoningforfait and deductible own-home costs is taken into account as the aftrek wegens geen of geringe eigenwoningschuld. Use this reviewed percentage in calculations.

### When the Hillenregeling applies

The Hillenregeling applies when:
- Eigenwoningforfait > `total_deductible_own_home_costs`, including when those costs are zero
- The excess after mortgage interest, qualifying financing costs, and periodic erfpacht/opstal/beklemming would otherwise remain in box 1 income

### Calculation

1. Determine eigenwoningforfait (A)
2. Determine `total_deductible_own_home_costs` (B): mortgage interest plus qualifying financing costs plus periodic erfpacht, opstal, or beklemming
3. If A > B, the excess = A - B
4. `hillen_deduction` = excess x 76.667% (for 2025)
5. `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`
6. Add only `box1_own_home_balance` to box 1 income; keep any tariefsaanpassing separate

### Practical effect

- For a homeowner with NO mortgage: the eigenwoningforfait is reduced by 76.667%, so 23.333% of it remains before other box 1 effects
- For a homeowner with low total deductible own-home costs: partial benefit may apply
- When total deductible own-home costs equal or exceed the forfait: the Hillenregeling does not apply, and the own-home balance remains zero or negative

---

## Multiple own-home situations

This section identifies facts to collect, not cases for a standard calculation. One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review.

### Sold and bought in the same year

- If the taxpayer sold one home and bought another during 2025:
  - Collect registration, sale, purchase, mortgage, and use dates for both addresses
  - Record the evidence and route the period allocation and qualification outcome to manual review

### Temporary double housing (verhuisregeling)

- When the old home is for sale and the new home is already purchased, the taxpayer may temporarily have two own homes
- Under the verhuisregeling, mortgage interest on the old home remains deductible for the year of moving plus the following 3 calendar years, provided it is for sale, empty, and not rented out
- The eigenwoningforfait for the old home is EUR 0 while it is empty and for sale
- Collect: move/registration date, date old home listed for sale, vacancy/rental status, date old home sold
- Do not apply the exception automatically; route the collected facts and possible temporary double-home deduction to manual review

### Partial year ownership

- If the eigen woning was owned for only part of 2025 (purchased or sold during the year):
  - Collect the registration, ownership, use, and mortgage dates
  - Route the period calculation to manual review

---

## Missing data flags

When producing notes, flag the following if not available in the evidence index:

| Missing item | Flag | Impact |
|-------------|------|--------|
| WOZ-beschikking not provided | `missing_woz: true` | Cannot calculate eigenwoningforfait |
| Hypotheek jaaroverzicht not provided | `missing_mortgage_statement: true` | Cannot determine deductible interest |
| Mortgage start year unknown | `missing_mortgage_start_year: true` | Cannot verify annuitair/lineair requirement |
| Property ownership percentage unknown | `missing_ownership_share: true` | Cannot split between partners |
| Move date not provided (if applicable) | `missing_move_date: true` | Cannot pro-rate eigenwoningforfait |
| WOZ-waarde provided without beschikking | `unverified_woz: true` | Value should be verified against official document |

Each missing item should generate a corresponding entry in `workspace/shared/review-questions.md`.

---

## Notes

- The eigenwoningforfait percentage of 0.35% applies specifically to 2025. Do not carry forward to other years without verification.
- The tariefsaanpassing cap of 37.48% is specific to 2025 and may change in subsequent years.
- The Hillenregeling phase-out percentage (76.667% remaining) is specific to 2025.
- For fiscal partners: the saldo of own-home income and deductions is an allocatable item in the return. Any allocation must be consistent across both partners and total 100%.
- This skill produces notes only. The calling skill (annual return or provisional assessment) is responsible for incorporating these notes into the final workpack.
