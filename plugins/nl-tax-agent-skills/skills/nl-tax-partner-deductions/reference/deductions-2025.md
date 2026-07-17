# Rule note: Deduction allocation for annual return 2025

source_ids: bd_fisin_2025_index, bd_fiscal_partnership, bd_own_home_deduction_cap_2025, bd_deduction_rate_cap_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Contents

- Rule
- Persoonsgebonden aftrek: allocation rules per category
- Scenario-comparison principle
- Heffingskorting interaction
- Warning: this skill compares options but never selects one
- Common errors

## Rule

When fiscal partners file their annual return for 2025, they can allocate
certain deductions between them. This note covers the allocation rules and how
to compare traceable scenarios without ranking, recommending, or selecting one
for the taxpayers.

These are reference notes for workpack preparation -- not final tax advice.

## Persoonsgebonden aftrek: allocation rules per category

The persoonsgebonden aftrek is freely allocatable between fiscal partners, but individual deduction categories have specific constraints.

### Alimentatie (maintenance payments)

- Whole-year fiscal partners may distribute common deductions, including paid partneralimentatie, in any split that totals 100%.
- The receiving ex-partner reports partneralimentatie received as income.
- If the taxpayer is not a whole-year fiscal partner, flag the allocation for manual review instead of assuming free allocation.
- Kinderalimentatie is NOT deductible and not relevant to allocation.

### Zorgkosten (specific healthcare costs)

- The drempel (threshold) is calculated based on the combined household drempelinkomen of both partners.
- The total qualifying zorgkosten of the household are compared against the single combined drempel.
- Only the excess above the drempel is deductible.
- The allocation of this excess between partners is free. Show traceable
  eligible splits and their estimated effects; the taxpayers choose the split.
- Important: the drempel is household-level, not per-partner. Do not calculate separate thresholds for each partner.

### Giften (charitable donations)

- **Periodieke giften (periodic gifts):** require a qualifying notarial deed or
  written agreement. For 2025 the combined maximum is **EUR 1.5 million**,
  subject to the reviewed **transition** rule for qualifying older agreements.
  Record the agreement date and route uncertain transition facts to manual
  review. For whole-year fiscal partners, treat gifts as allocatable unless the
  official form indicates otherwise.
- **Gewone giften / eenmalige giften (incidental gifts):** can be allocated freely between whole-year fiscal partners.
- The drempel (1% of drempelinkomen) and maximum (10% of drempelinkomen) for incidental gifts are calculated on the combined drempelinkomen of both partners.
- Cultural ANBI multiplier (1.25x, max EUR 1,250 increase) applies before the drempel and cap calculation.

### Lijfrentepremie (annuity premiums)

- The deduction is allocated to the partner who pays the premium.
- However, the jaarruimte (annual space) calculation considers the pension gap of the paying partner.
- If one partner has a large pension gap and the other does not, the partner with the gap should pay and claim the premium.
- The reservation space (reserveringsruimte) from prior years is also personal to the partner who had the unused jaarruimte.

### Restant persoonsgebonden aftrek (carryforward)

- Record which partner originally had the unused deduction and the confirmed amount carried into 2025.
- Eligible whole-year fiscal partners may allocate the prior-year personal-deduction remainder in the current return. Model traceable scenarios whose shares total 100%, including the portal/default position and at least one alternative when material.
- Require both taxpayers to review the scenarios and select the allocation in the official filing environment; do not select it automatically.

## Scenario-comparison principle

The core comparison principle for deduction allocation:

**Model multiple allocation scenarios; do not automatically allocate everything to the highest marginal-rate partner.**

### Why this works

Before the high-income deduction-rate cap and credit effects, a deduction has more value when applied against higher taxable income. For 2025, however, listed deductions in the highest box 1 bracket are capped at 37.48%, so a 49.50% marginal-rate comparison overstates the benefit.

### High-income deduction-rate cap

The tariefsaanpassing (rate adjustment) limits the effective deduction rate for listed deductions to 37.48% in 2025, even if the partner is in the 49.50% bracket.

This means:
- For own-home deductible costs and other listed deductions, the benefit of allocating to the higher-bracket partner is reduced.
- The effective rate difference can be much smaller than the headline 49.50% vs 35.82% bracket spread.
- Non-own-home deductions such as zorgkosten, giften, and paid partneralimentatie can also fall under the 37.48% cap.

Implication: model more than one allocation instead of assuming the highest-bracket partner is always best. Fiscal partners may allocate common income and deduction items in any split that totals 100%, subject to the official form.

## Heffingskorting interaction

Allocation choices affect the heffingskortingen because they can change each partner's verzamelinkomen:

### Algemene heffingskorting (general tax credit)

- Use the exact 2025 algemene heffingskorting table in `_shared/knowledge/years/2025/annual/credits.md`.
- If allocating deductions to the higher-income partner reduces their verzamelinkomen below the phase-out threshold, it may increase their algemene heffingskorting.
- Conversely, not allocating deductions to the lower-income partner keeps their verzamelinkomen higher, potentially reducing their algemene heffingskorting.
- Do not estimate the phase-out rate from memory; use the reviewed source-backed table.

### Arbeidskorting (employment tax credit)

- The arbeidskorting is based on individual employment income and cannot be affected by deduction allocation.
- However, the arbeidskorting phases out at higher incomes under the exact 2025 table in `_shared/knowledge/years/2025/annual/credits.md`.
- Deduction allocation does not change employment income, so it does not directly affect the arbeidskorting.

### Net effect

The heffingskorting interaction can partially offset or amplify bracket-rate
effects. Each scenario comparison therefore shows both the marginal-rate and
heffingskorting effects, with assumptions and uncertainty, without ranking the
scenarios.

## Warning: this skill compares options but never selects one

This skill generates allocation scenarios with estimated tax impact. The final allocation choice requires human review because:

1. The tax impact depends on exact income amounts, which may not be fully known.
2. Heffingskorting phase-out interactions require precise income calculations.
3. There may be carry-forward effects from prior years.
4. Box 3 allocation interacts with deduction allocation (both change taxable income).
5. The tariefsaanpassing complicates the straightforward "highest bracket" rule.

The calling skill must present labeled allocation scenarios to the taxpayer for
review, not rank, recommend, or select one automatically. Record an allocation
only after the taxpayer explicitly chooses it; otherwise leave it unresolved.

## Allocation arithmetic check

The agent, not the optional Python helper, decides fiscal-partner status and
whether each proposed row is legally allocatable from the reviewed sources.
Record both decisions as real booleans: `has_fiscal_partner` for the wrapped
scenario and `allocatable` for every row. Do not infer allocatability from a
label or silently default missing decisions.

For every row, check that `taxpayer_pct` and `partner_pct` are finite numbers in
the 0–100 range and total 100. A row explicitly marked non-allocatable must be
100/0 or 0/100; when `has_fiscal_partner` is false, `partner_pct` must be 0.
Record `check_performed_by: checked_by_agent` for the manual path or
`check_performed_by: checked_by_script` when the optional helper checks the same
wrapped payload. Python availability does not block preparation.

## Common errors

1. **Allocating employment income between partners.** Employment income is not allocatable. It stays with the earner.
2. **Forgetting to consider heffingskorting impact.** Moving deductions to the higher-bracket partner reduces their income, which may change their heffingskorting. The net benefit may be smaller than the bracket-rate difference suggests.
3. **Treating 50/50 as a preferred split.** It may be one useful Scenario A,
   but the workpack should show alternatives when the amounts are material and
   leave the choice to the taxpayers.
4. **Ignoring tariefsaanpassing for listed deductions.** Treating deductible own-home costs, gifts, healthcare costs, or partneralimentatie at the full 49.50% marginal rate overstates the benefit for higher-bracket partners.
5. **Treating the eigen woning result as tied to ownership share for fiscal partners.** Fiscal partners may allocate the saldo of own-home income and deductions in any split totaling 100%. Ownership-share rules matter when people are not fiscal partners.
6. **Not verifying that both partners file consistently.** Both partners must use the same allocation in their returns. Inconsistent filing leads to rejection.
