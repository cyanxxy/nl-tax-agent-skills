# Rule note: Deduction allocation for annual return 2025

source_id: bd_fisin_2025_deduction_alloc
workflow: annual-return
tax_year: 2025
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

When fiscal partners file their annual return for 2025, they can allocate certain deductions between them to optimize their combined tax position. This note covers the allocation rules and optimization principles specific to the 2025 annual return.

These are reference notes for workpack preparation -- not final tax advice.

## Persoonsgebonden aftrek: allocation rules per category

The persoonsgebonden aftrek is freely allocatable between fiscal partners, but individual deduction categories have specific constraints.

### Alimentatie (maintenance payments)

- Partneralimentatie must be allocated to the partner who actually pays it.
- The paying partner claims the deduction; the receiving ex-partner reports it as income.
- Although technically part of the freely allocatable persoonsgebonden aftrek, the practical constraint is that only the paying partner has the deduction to allocate.
- Kinderalimentatie is NOT deductible and not relevant to allocation.

### Zorgkosten (specific healthcare costs)

- The drempel (threshold) is calculated based on the combined household drempelinkomen of both partners.
- The total qualifying zorgkosten of the household are compared against the single combined drempel.
- Only the excess above the drempel is deductible.
- The allocation of this excess between partners is free -- assign it to the partner where it yields the most tax benefit.
- Important: the drempel is household-level, not per-partner. Do not calculate separate thresholds for each partner.

### Giften (charitable donations)

- **Periodieke giften (periodic gifts):** the deduction is locked to the partner who signed the notarial deed or written agreement. It cannot be reallocated to the other partner.
- **Gewone giften / eenmalige giften (incidental gifts):** can be allocated freely between partners.
- The drempel (1% of drempelinkomen) and maximum (10% of drempelinkomen) for incidental gifts are calculated on the combined drempelinkomen of both partners.
- Cultural ANBI multiplier (1.25x, max EUR 1,250 increase) applies before the drempel and cap calculation.

### Lijfrentepremie (annuity premiums)

- The deduction is allocated to the partner who pays the premium.
- However, the jaarruimte (annual space) calculation considers the pension gap of the paying partner.
- If one partner has a large pension gap and the other does not, the partner with the gap should pay and claim the premium.
- The reservation space (reserveringsruimte) from prior years is also personal to the partner who had the unused jaarruimte.

### Restant persoonsgebonden aftrek (carryforward)

- Unused deductions from prior years are personal to the partner who had the excess.
- When applied in the current year, the carryforward deduction is personal to that partner and is not reallocatable.

## Optimization principle

The core optimization principle for deduction allocation:

**Allocate deductions to the partner with the highest marginal tax rate.**

### Why this works

A deduction of EUR 1,000 saves:
- EUR 495 if the partner is in the 49.50% bracket (box 1 schijf 2, income above approximately EUR 76,817 in 2025)
- EUR 358 if the partner is in the 35.82% bracket (box 1 schijf 1, income up to approximately EUR 76,817 in 2025)

The difference is EUR 137 per EUR 1,000 of deductions. For large deduction amounts (e.g., mortgage interest of EUR 10,000+), this can result in savings of over EUR 1,000.

### Exception: tariefsaanpassing eigen woning

The tariefsaanpassing (rate adjustment) for mortgage interest limits the effective deduction rate for hypotheekrenteaftrek to 37.48% in 2025, even if the partner is in the 49.50% bracket.

This means:
- For mortgage interest specifically, the benefit of allocating to the higher-bracket partner is reduced.
- The effective rate difference for mortgage interest is 37.48% vs 35.82% = only 1.66 percentage points.
- For other deductions (zorgkosten, giften, alimentatie), the full bracket difference applies.

Implication: it may be better to allocate mortgage interest to the lower-bracket partner (where tariefsaanpassing has no impact because they are already below the cap) and allocate other deductions to the higher-bracket partner (where they benefit from the full 49.50% rate).

## Heffingskorting interaction

Allocation choices affect the heffingskortingen because they change each partner's taxable income:

### Algemene heffingskorting (general tax credit)

- Phases out as income increases above approximately EUR 24,813 (2025).
- If allocating deductions to the higher-income partner reduces their income below the phase-out threshold, it may increase their algemene heffingskorting.
- Conversely, not allocating deductions to the lower-income partner keeps their income higher, potentially reducing their algemene heffingskorting.
- The phase-out rate is approximately 6.63% of income above the threshold.

### Arbeidskorting (employment tax credit)

- The arbeidskorting is based on individual employment income and cannot be affected by deduction allocation.
- However, the arbeidskorting phases out at higher incomes (above approximately EUR 39,958 in 2025 at a rate of approximately 6.51%).
- Deduction allocation does not change employment income, so it does not directly affect the arbeidskorting.

### Net effect

The heffingskorting interaction can partially offset or amplify the bracket-rate optimization. A complete optimization requires modelling both the marginal rate savings and the heffingskorting changes.

## Warning: this skill suggests options, not optimal strategy

This skill generates allocation scenarios with estimated tax impact. The final allocation choice requires human review because:

1. The tax impact depends on exact income amounts, which may not be fully known.
2. Heffingskorting phase-out interactions require precise income calculations.
3. There may be carry-forward effects from prior years.
4. Box 3 allocation interacts with deduction allocation (both change taxable income).
5. The tariefsaanpassing complicates the straightforward "highest bracket" rule.

The calling skill (annual return or provisional assessment) must present the allocation options to the taxpayer for review, not select one automatically.

## Common errors

1. **Allocating employment income between partners.** Employment income is not allocatable. It stays with the earner.
2. **Forgetting to consider heffingskorting impact.** Moving deductions to the higher-bracket partner reduces their income, which may change their heffingskorting. The net benefit may be smaller than the bracket-rate difference suggests.
3. **Assuming 50/50 split is always optimal.** It almost never is. The marginal-rate-optimized allocation typically outperforms an even split. The only situation where 50/50 is optimal is when both partners have identical marginal rates and identical heffingskorting positions.
4. **Ignoring tariefsaanpassing for mortgage interest.** Treating mortgage interest deduction at the full marginal rate overstates the benefit for higher-bracket partners.
5. **Splitting the eigen woning result partially.** The eigen woning result should generally be allocated as a unit to one partner (unless both are co-owners with separate mortgage portions).
6. **Not verifying that both partners file consistently.** Both partners must use the same allocation in their returns. Inconsistent filing leads to rejection.
