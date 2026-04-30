# Box 1 for Provisional Assessment 2026

source_id: bd_provisional_rates_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Purpose

This reference describes how to apply box 1 income and own-home rules when preparing the voorlopige aanslag (provisional assessment) for 2026. All amounts in a provisional assessment are ESTIMATES. No evidence verification is performed.

These are reference notes for workpack preparation -- not final tax advice.

---

## Key principle: all amounts are estimates

The provisional assessment is forward-looking. It covers a tax year that is either in progress or has not yet ended. Therefore:

- All income amounts are ESTIMATES based on the taxpayer's current or expected situation
- No jaaropgaaf or other year-end evidence documents are available or required
- Every calculated amount must be clearly marked as "estimated" or "provisional"
- The taxpayer will reconcile the provisional assessment against actual data when the annual return is filed

---

## Rates and credits

Use the 2026 provisional rates from `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2026/provisional/rates-and-credits.md`.

Do NOT use 2025 rates for the provisional 2026 calculation. The 2026 rates may differ from 2025. If 2026 rates are marked as "pending verification" in the knowledge file, note this caveat in the output but still use the provisional 2026 values.

### 2026 provisional brackets (approximate, from rates-and-credits.md)

| Schijf | Taxable income | Rate |
|--------|---------------|------|
| 1 | Up to ~EUR 38,441 | ~35.82% |
| 2 | ~EUR 38,441 to ~EUR 76,817 | ~37.48% |
| 3 | Above ~EUR 76,817 | ~49.50% |

All values marked with ~ are provisional and subject to change.

---

## Estimated employment income

For the provisional assessment, estimated employment income is determined as follows:

1. **Current salary basis:** use the taxpayer's current gross annual salary (bruto jaarsalaris) as the best estimate for 2026
2. **If known:** apply any expected salary changes (e.g., scheduled raise, job change, reduction in hours)
3. **Holiday allowance (vakantiegeld):** include if the salary figure does not already account for it (typically 8% of base salary)
4. **13th month / bonus:** include if the taxpayer expects to receive one, but mark as uncertain
5. **If no salary information is available:** ask the taxpayer for an estimate or use the most recent jaaropgaaf as a baseline with a note that it may not reflect 2026

### Multiple income sources

- If the taxpayer expects income from multiple employers, sum the expected amounts
- Note that the provisional assessment may result in underpayment if multiple sources are not properly accounted for

---

## Estimated pension and benefit amounts

- **Pension income:** use the current pension payment amount, annualised (monthly amount x 12)
- **AOW:** use the current AOW rate for the taxpayer's situation (single or partnered)
- **UWV benefits (WW, WIA):** use the current benefit amount if known; note that WW benefits typically decrease or expire during the year
- **Other benefits:** use current amounts projected to 2026

Mark all pension and benefit estimates with a note that actual amounts may differ.

---

## Estimated own-home deduction

For the provisional assessment, the eigen woning calculation uses projected 2026 values:

### Eigenwoningforfait

- Use the most recent known WOZ-waarde as the basis
- Note: the WOZ-waarde for 2026 returns (waardepeildatum 1 January 2025) may not yet be known when the provisional assessment is prepared
- If the 2026 WOZ-waarde is not available, use the 2025 WOZ-waarde as an estimate and flag it
- Apply the 2026 eigenwoningforfait percentage (verify against 2026 knowledge file; if not available, use the 2025 percentage as an estimate with a note)

### Hypotheekrenteaftrek

- Use the current mortgage terms to project interest payments into 2026
- For annuity mortgages: the interest component decreases each year as principal is repaid. Use the projected 2026 interest from the mortgage schedule if available, or estimate based on the current remaining balance and interest rate.
- For linear mortgages: calculate based on remaining balance minus annual principal repayment, multiplied by the interest rate
- For interest-only mortgages (pre-2013): use the current annual interest amount
- If the interest rate is variable or subject to reset in 2026, note the uncertainty

### Tariefsaanpassing

- If estimated 2026 income exceeds the schijf 3 threshold (~EUR 76,817), note that tariefsaanpassing will apply
- Use the 2026 provisional cap rate (~37.48%, verify against rates-and-credits.md)

### Hillenregeling

- If the eigenwoningforfait exceeds the estimated mortgage interest, the Hillenregeling may apply
- Use the 2026 phase-out percentage: approximately 73.33% (year 8 of the 30-year phase-out)
- Mark as estimated

---

## What is NOT required for provisional assessments

The following are required for the annual return but NOT for the provisional assessment:

| Item | Required for annual 2025 | Required for provisional 2026 |
|------|-------------------------|------------------------------|
| Jaaropgaaf | Yes (actual data) | No (use salary estimate) |
| WOZ-beschikking 2026 | N/A | No (use best available WOZ) |
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
| Verification | Yes -- cross-check against evidence | No -- trust taxpayer input |
| Output caveat | None needed | "Based on provisional rates and estimated amounts" |
| Missing evidence | Flag as blocking issue | Not applicable |

---

## Output requirements

When producing notes for the provisional 2026 workflow:

1. Clearly label every amount as "ESTIMATED"
2. Note the source of each estimate (current salary, current mortgage, etc.)
3. Include a caveat that provisional rates may differ from final 2026 rates
4. Do not present provisional amounts with false precision -- round to the nearest EUR 10 or EUR 100 as appropriate
5. Flag any estimates that are highly uncertain (e.g., variable income, expected job change)

---

## Notes

- The provisional assessment can be requested, changed, reviewed, or stopped (stopgezet). This skill provides the box 1 calculation notes; the calling skill handles the workflow-specific logic.
- For change requests (wijzigen): the taxpayer may have updated income estimates. Use the latest estimates, not the original provisional amounts.
- For review requests (controleren): compare the current provisional assessment against updated estimates.
- Do not require the taxpayer to provide evidence documents for a provisional assessment. The annual return (due later) is when evidence is required.
