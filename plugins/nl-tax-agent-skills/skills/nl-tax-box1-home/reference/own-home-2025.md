# Eigen Woning (Own Home) Rules — Annual Return 2025

source_ids: bd_own_home_deduction_cap_2025, bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes, bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest, bd_fiscal_partnership
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-05-10"
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

### When tariefsaanpassing applies

- The taxpayer's box 1 taxable income (before eigen woning deduction) exceeds EUR 76,817
- The taxpayer has deductible own-home costs

### When tariefsaanpassing does NOT apply

- Income is below EUR 76,817 (entirely in schijf 1 and/or schijf 2)
- No deductible own-home costs are deducted

### Calculation approach

1. Determine total box 1 income before the eigen woning deduction
2. If income > EUR 76,817, calculate the tariefsaanpassing:
   - Tariefsaanpassing = deductible own-home costs x (49.50% - 37.48%)
   - This amount is recorded as an adjustment that reduces the net tax benefit of the deduction
3. If income context is not yet available when this skill runs, output a WARNING that tariefsaanpassing may apply and must be checked by the calling skill

---

## Hillenregeling (aftrek wegens geen of geringe eigenwoningschuld)

The Hillenregeling provides relief for homeowners who have paid off their mortgage (fully or substantially). It reduces the eigenwoningforfait when the forfait exceeds the deductible mortgage interest.

### Phase-out status for 2025

For 2025, 76.667% of the difference between the eigenwoningforfait and deductible own-home costs is taken into account as the aftrek wegens geen of geringe eigenwoningschuld. Use this reviewed percentage in calculations.

### When the Hillenregeling applies

The Hillenregeling applies when:
- Eigenwoningforfait > deductible mortgage interest (including the case of zero mortgage interest)
- The excess forfait (eigenwoningforfait minus mortgage interest) would otherwise be added to box 1 income

### Calculation

1. Determine eigenwoningforfait (A)
2. Determine deductible mortgage interest (B)
3. If A > B, the excess = A - B
4. Hillenregeling correction = excess x 76.667% (for 2025)
5. Net eigenwoningforfait after Hillenregeling = A - Hillenregeling correction
6. The remaining net amount is added to box 1 income

### Practical effect

- For a homeowner with NO mortgage: the eigenwoningforfait is reduced by 76.667%, so 23.333% of it remains before other box 1 effects
- For a homeowner with a small mortgage where forfait > interest: partial benefit applies
- For a homeowner whose mortgage interest exceeds the forfait (the common case): the Hillenregeling does not apply, and the net result remains a deduction

---

## Multiple own-home situations

### Sold and bought in the same year

- If the taxpayer sold one home and bought another during 2025:
  - Eigenwoningforfait is calculated for the period the taxpayer was registered at each address as their main residence
  - Mortgage interest is deductible only for the period each loan was active
  - Both properties must be the taxpayer's primary residence during their respective periods

### Temporary double housing (verhuisregeling)

- When the old home is for sale and the new home is already purchased, the taxpayer may temporarily have two own homes
- Under the verhuisregeling, mortgage interest on the old home remains deductible for the year of moving plus the following 3 calendar years, provided it is for sale, empty, and not rented out
- The eigenwoningforfait for the old home is EUR 0 while it is empty and for sale
- Collect: move/registration date, date old home listed for sale, vacancy/rental status, date old home sold

### Partial year ownership

- If the eigen woning was owned for only part of 2025 (purchased or sold during the year):
  - Eigenwoningforfait is calculated for the period the taxpayer was registered there as their main residence, not simply by ownership days
  - Mortgage interest deduction applies only for the period the mortgage was active

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
