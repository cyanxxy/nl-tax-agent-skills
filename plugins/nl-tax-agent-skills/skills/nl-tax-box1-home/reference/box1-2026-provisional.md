# Box 1 for Provisional Assessment 2026

source_ids: bd_provisional_rates_2026, bd_box1_rates_2026, bd_heffingskortingen_aow_2025_2026, bd_eigenwoningforfait_2025_2026, bd_woz_value_provisional_2026, bd_own_home_deduction_cap_2026, bd_hypotheekrenteaftrek_conditions
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Contents

- Purpose
- Key principle: all amounts are estimates
- Rates and credits
- Estimated employment income
- Estimated pension and benefit amounts
- Estimated own-home deduction
- What is NOT required for provisional assessments
- Differences from the annual return workflow
- Output requirements
- Notes

## Purpose

This reference describes how to apply box 1 income and own-home rules when preparing the voorlopige aanslag (provisional assessment) for 2026. All amounts in a provisional assessment are estimates. Current payslips, benefit statements, mortgage schedules, and the 2026 WOZ notice can support an estimate when available, but year-end evidence is not a prerequisite.

These are reference notes for workpack preparation -- not final tax advice.

---

## Key principle: all amounts are estimates

The provisional assessment is forward-looking. It covers a tax year that is either in progress or has not yet ended. Therefore:

- All income amounts are ESTIMATES based on the taxpayer's current or expected situation
- A 2026 jaaropgaaf and other year-end evidence are not yet available or
  required. Current documents may still be used as traceable estimate sources.
- Every calculated amount must be clearly marked as "estimated" or "provisional"
- If an annual return is later required or filed, reconcile the provisional
  estimate against the actual data in that return.

---

## Rates and credits

Use the 2026 provisional rates from `_shared/knowledge/years/2026/provisional/rates-and-credits.md`.

Do NOT use 2025 rates for the provisional 2026 calculation. Use the 2026 provisional values in `rates-and-credits.md`.

### 2026 provisional brackets from rates-and-credits.md

| Schijf | Taxable income | Rate |
|--------|---------------|------|
| 1 | Up to and including EUR 38,883 | 35.75% |
| 2 | More than EUR 38,883 up to and including EUR 78,426 | 37.56% |
| 3 | More than EUR 78,426 | 49.50% |

These are the reviewed provisional 2026 values in the local source pack. Do not use them for any other year.

---

## Estimated employment income

For the provisional assessment, estimated employment income is determined as follows:

1. **Taxable-wage basis:** estimate the expected 2026 `fiscaal loon` / `loon
   voor de loonheffingen`, preferably from 2026 year-to-date payroll data plus
   expected remaining pay. Do not assume a contract's generic gross salary is
   already the portal's taxable-wage figure.
2. **Known changes:** account for a scheduled raise, job change, unpaid leave,
   reduction in hours, or employment ending during 2026.
3. **Holiday allowance:** ask whether it is already included before adding it;
   never add a generic percentage twice.
4. **13th month, bonus, and taxable benefits:** include only when expected and
   record uncertainty rather than forcing one forecast.
5. **Fallback:** if no 2026 payroll basis is available, use the taxpayer's
   estimate or the most recent jaaropgaaf as a clearly labelled baseline and
   ask about material 2026 changes.

### Multiple income sources

- If the taxpayer expects income from multiple employers, sum the expected amounts
- Note that the provisional assessment may result in underpayment if multiple sources are not properly accounted for

---

## Estimated pension and benefit amounts

- **Pension income:** use a 2026 payment schedule where available. Otherwise
  annualise the current taxable payment while recording any known 2026 change.
- **AOW:** use the taxpayer's actual 2026 start month and payment situation;
  never multiply a post-start monthly payment by 12 in a transition year.
- **UWV benefits (WW, WIA):** use the current benefit amount if known; note that WW benefits typically decrease or expire during the year
- **Other benefits:** use current amounts projected to 2026

Mark all pension and benefit estimates with a note that actual amounts may differ.

---

## Estimated own-home deduction

For the provisional assessment, the eigen woning calculation uses projected 2026 values:

### Eigenwoningforfait

- Use the WOZ value for the 2026 tax year with **waardepeildatum 1 January
  2025** when the notice is available.
- If that notice was not yet available when the estimate was prepared, use the
  latest available notice only as a labelled fallback and create a review item
  to replace it. Do not silently call the fallback the 2026 WOZ value.
- Apply the reviewed 2026 eigenwoningforfait table from `_shared/knowledge/years/2026/provisional/own-home.md`. Do not carry forward 2025 thresholds.

### Hypotheekrenteaftrek

- Use the current mortgage terms to project interest payments into 2026
- For annuity mortgages: the interest component decreases each year as principal is repaid. Use the projected 2026 interest from the mortgage schedule if available, or estimate based on the current remaining balance and interest rate.
- For linear mortgages: calculate based on remaining balance minus annual principal repayment, multiplied by the interest rate
- For interest-only mortgages (pre-2013): use the current annual interest amount
- If the interest rate is variable or subject to reset in 2026, note the uncertainty

### Tariefsaanpassing

- If estimated 2026 income exceeds the schijf 3 threshold (EUR 78,426), note that tariefsaanpassing will apply
- Use the 2026 cap rate of 37.56% and tariefsaanpassing percentage of 11.94% from `_shared/knowledge/years/2026/provisional/own-home.md`

### Hillenregeling

- If the eigenwoningforfait exceeds the estimated `total_deductible_own_home_costs`, the aftrek wegens geen of geringe eigenwoningschuld may apply.
- Use the reviewed 2026 percentage from `_shared/knowledge/years/2026/provisional/own-home.md`: 71.867% of the difference between eigenwoningforfait and deductible own-home costs.
- Mark as estimated

### Manual/script parity

For one ordinary home, add estimated mortgage interest, qualifying financing
costs, and periodic erfpacht/opstal/beklemming as
`total_deductible_own_home_costs`. Compute `hillen_deduction`, list only
eigenwoningforfait, that total, and the Hillen amount in
`box1_balance_components`, then calculate `box1_own_home_balance`. Keep
tariefsaanpassing under `review_adjustments`, separate from the balance.

Record `check_performed_by: checked_by_agent` for the manual check or
`check_performed_by: checked_by_script` when the optional helper checks the same
accepted estimates. Eligibility and complex-home decisions remain with the
agent.

---

## What is NOT required for provisional assessments

The following are required for the annual return but NOT for the provisional assessment:

| Item | Required for annual 2025 | Required for provisional 2026 |
|------|-------------------------|------------------------------|
| Jaaropgaaf | Yes (actual data) | No (use salary estimate) |
| WOZ-beschikking for tax year 2026 (peildatum 1 January 2025) | N/A | Use when available; otherwise label the latest notice as a fallback estimate |
| Hypotheek jaaroverzicht 2026 | N/A | No (use current mortgage terms) |
| Pensioenoverzicht 2026 | N/A | No (use current pension amount) |
| Evidence verification | Yes | No |
| Exact employer details | Yes | No (employer name is sufficient) |

---

## Differences from the annual return workflow

| Aspect | Annual 2025 | Provisional 2026 |
|--------|-------------|-------------------|
| Data source | Evidence documents (jaaropgaaf, WOZ, etc.) | Taxpayer estimates |
| Accuracy | Must match source documents | Best-effort estimate |
| Rates | Definitive 2025 rates | Provisional 2026 rates |
| Verification | Cross-check actuals against evidence | Trace estimates to taxpayer statements and any current documents used |
| Output caveat | Draft for taxpayer review and manual entry | "Based on 2026 rules and estimated amounts" |
| Missing evidence | Flag as blocking issue | Not applicable |

---

## Output requirements

When producing notes for the provisional 2026 workflow:

1. Clearly label every amount as "ESTIMATED"
2. Note the source of each estimate (current salary, current mortgage, etc.)
3. Include a caveat that the output is a provisional-assessment calculation
4. Do not invent precision. Preserve a source amount when supplied; otherwise
   use an honestly labelled estimate and the whole-euro unit expected by the
   official environment rather than imposing an arbitrary EUR 10 or EUR 100
   rounding rule.
5. Flag any estimates that are highly uncertain (e.g., variable income, expected job change)

---

## Notes

- The provisional assessment can be requested, changed, reviewed, or stopped (stopgezet). This skill provides the box 1 calculation notes; the calling skill handles the workflow-specific logic.
- For change requests (wijzigen): the taxpayer may have updated income estimates. Use the latest estimates, not the original provisional amounts.
- For review requests (controleren): compare the current provisional assessment against updated estimates.
- Do not require the taxpayer to provide evidence documents for a provisional
  assessment. If an annual return is later required or filed, use actual
  year-end amounts and available supporting documents for that return.
