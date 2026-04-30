# Rule note: VVA/EVA baseline + delta model for provisional assessment 2026

source_id: bd_algoritmeregister_vva_eva
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The Belastingdienst uses a baseline + forecast + delta approach for provisional assessments. The provisional workflow must be modeled as a forward-looking estimate, distinct from the backward-looking annual return.

## Key terms

### VVA -- Verzoek Voorlopige Aanslag

A VVA is a request for a provisional assessment submitted by the taxpayer. The taxpayer provides estimated income, deductions, and assets/debts for the current year. The Belastingdienst processes this into a monthly payment or refund schedule.

### EVA -- Eerste Voorlopige Aanslag

An EVA is the first provisional assessment generated automatically by the Belastingdienst, typically based on prior-year data. The taxpayer receives this without requesting it. If the taxpayer's situation has changed, the EVA should be reviewed and potentially changed (see review-flow.md and change-flow.md).

## Baseline + forecast + delta model

The Belastingdienst applies a three-part model for provisional assessments:

### Baseline

- The starting point for the provisional assessment
- Sources: prior-year annual return data, earlier submitted VVA, or prior EVA
- Represents the last known tax position of the taxpayer

### Forecast

- The expected current-year amounts
- Sources: taxpayer-submitted estimates (VVA) or Belastingdienst projections (EVA)
- Represents the anticipated tax position for the provisional year

### Delta

- The difference between the baseline and the forecast
- Determines the adjustment to the monthly payment or refund
- A positive delta means higher tax expected; a negative delta means lower tax expected

## Important distinctions

### Provisional assessment is NOT the annual return

- The provisional assessment is **forward-looking**: it estimates what the taxpayer will owe or be refunded for the current year
- The annual return is **backward-looking**: it calculates actual tax based on realized income, deductions, and assets
- These are fundamentally different workflows and must not be conflated

### Provisional assessment is NOT "annual return lite"

- The data collected for a provisional assessment is a subset of what the annual return requires
- Estimates are accepted (and expected) for the provisional assessment
- Precision requirements are lower -- the goal is a reasonable monthly amount, not an exact tax calculation
- Some elements of the annual return (e.g., werkelijk rendement for box 3) do not apply to the provisional assessment

## Weegmodule (weighing module)

The Belastingdienst applies a weegmodule (weighing module) to VVA submissions:

- Business rules evaluate whether submitted estimates are plausible
- Implausible values may be flagged, adjusted, or trigger follow-up
- The weegmodule compares submitted values against the baseline and expected ranges
- This is an internal Belastingdienst process -- the taxpayer does not interact with the weegmodule directly

## Developer instruction

When modeling the provisional assessment workflow:

1. **Model as baseline + forecast + delta**, not as "annual return lite"
2. Start from a baseline (prior-year data or earlier VVA/EVA) when available
3. Collect the forecast (estimated current-year amounts) from the taxpayer
4. Calculate the delta to show the change in expected tax position
5. Present the result as a monthly payment or refund based on the delta
6. Do not reuse annual return data structures or flows for the provisional assessment -- build separate, purpose-built flows
7. Accept estimates and indicate that precision is not required for the provisional assessment
8. When an EVA is present, treat it as the baseline and allow the user to adjust it through a VVA

## Common failure

Do not model the provisional assessment as a copy of the annual return with reduced fields. The provisional assessment has its own logic (baseline + forecast + delta), its own data requirements (estimates, not actuals), and its own purpose (monthly payment/refund scheduling). Treating it as a simplified annual return leads to incorrect workflows, incorrect data collection, and user confusion.
