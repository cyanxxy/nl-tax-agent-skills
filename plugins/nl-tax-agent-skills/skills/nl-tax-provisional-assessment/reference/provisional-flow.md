# Provisional Flow — Subflow Routing and Generation

## Overview

This document defines the routing logic, data collection steps, decision points, and output generation for each of the four provisional assessment subflows.

## Subflow routing

```
User enters provisional skill
  │
  ├── workflow_candidate = provisional_2026_request
  │     → Request subflow
  │
  ├── workflow_candidate = provisional_2026_change
  │     → Change subflow
  │
  ├── workflow_candidate = provisional_2026_review
  │     → Review subflow
  │
  └── workflow_candidate = provisional_2026_stopzetten
        → Stopzetten subflow
              │
              ├── User receives monthly refund (teruggaaf)
              │     → Stopzetten guidance
              │
              └── User pays monthly amount (betaling) + amount is wrong
                    → REDIRECT to Change subflow
```

---

## Request subflow

### Decision points

1. Does the taxpayer profile exist? If not, route back to intake.
2. Does the profile contain `provisional_2026_request`? If not, route to the correct subflow.
3. Does the taxpayer have a fiscal partner? If yes, collect partner data and determine box 3 allocation.

### Data collection steps

1. **Employment income estimate** — gross annual salary, holiday allowance, bonuses expected in 2026
2. **Pension/benefit income estimate** — AOW, pension, WW, WIA, bijstand expected in 2026
3. **Other income estimate** — freelance, rental, foreign income expected in 2026
4. **Own-home deduction estimate** — mortgage interest (hypotheekrente) for 2026, eigenwoningforfait based on WOZ-waarde
5. **Other deductions estimate** — alimentatie, lijfrentepremie, arbeidsongeschiktheidsverzekering, specific care costs, gifts
6. **Box 3 data** — assets and debts as of peildatum 1 January 2026:
   - Categorie I: Banktegoeden
   - Categorie II: Overige bezittingen
   - Categorie III: Schulden (excluding eigenwoningschuld)
   - Heffingsvrij vermogen deduction
   - FICTITIOUS METHOD ONLY — no werkelijk rendement

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` using the template
2. Generate `workspace/provisional/2026/field-map.yaml` with all collected fields mapped to Belastingdienst portal fields
3. Update `workspace/shared/assumptions.md` with all assumptions made
4. Label all amounts as estimates

---

## Change subflow

### Decision points

1. Does the taxpayer profile exist and contain `provisional_2026_change`?
2. Is there a baseline available?
   - From evidence index (beschikking indexed by the evidence-indexer skill)
   - From user input (user provides current voorlopige aanslag details)
   - If no baseline at all: ask user to provide the current monthly amount and key figures from their beschikking
3. Does the taxpayer have a fiscal partner? Has partner status changed?

### Data collection steps

1. **Baseline capture** — record the existing voorlopige aanslag details:
   - Monthly payment or refund amount
   - Income categories as submitted
   - Deductions as submitted
   - Box 3 data as submitted
2. **Full re-entry of all current estimates** (CRITICAL — not just changes):
   - All income categories (employment, pension/benefit, other)
   - All deductions (own-home, alimentatie, premiums, other)
   - All box 3 data (assets and debts as of 1 January 2026, fictitious method only)
3. **Delta calculation** — compare baseline to current estimates:
   - Per-category: income (up/down), deductions (up/down), box 3 (up/down), partner changes
   - Expected impact on monthly payment or refund

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` with change context
2. Generate `workspace/provisional/2026/field-map.yaml` with all fields
3. Generate `workspace/provisional/2026/delta-summary.md` — baseline vs forecast comparison
4. Update `workspace/shared/assumptions.md`
5. Include the full-re-entry reminder in the workpack

---

## Review subflow

### Decision points

1. Does the taxpayer profile exist and contain `provisional_2026_review`?
2. Is there a current voorlopige aanslag available to review?
   - From evidence index
   - From user input
3. Was the current voorlopige aanslag automatically generated (EVA) or user-submitted (VVA)?
   - EVA: especially important to verify, as it is based on prior-year data that may be outdated
4. Have any life events occurred since the voorlopige aanslag was issued?

### Data collection steps

1. **Current voorlopige aanslag capture** — record all key figures:
   - Monthly payment or refund amount
   - Income figures used
   - Deductions used
   - Box 3 data used
2. **Life event screening** — ask about changes in each category:
   - Income: new job, salary change, retirement, job loss, started/stopped benefits
   - Housing: new mortgage, sold home, refinanced, paid off mortgage
   - Partner: marriage, separation, divorce, partner income changes
   - Deductions: started/stopped alimentatie, changed premiums, other
   - Box 3: significant asset or debt changes since 1 January 2026
3. **Comparison** — for each category, note whether the current voorlopige aanslag figure still matches reality

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` with review context
2. Generate `workspace/provisional/2026/review-questions.md` — items flagged for user verification
3. Update `workspace/shared/assumptions.md`
4. If changes are needed: explicitly recommend running the change subflow and explain what would change

---

## Stopzetten subflow

### Decision points

1. Does the taxpayer profile exist and contain `provisional_2026_stopzetten`?
2. Is the user receiving a monthly refund (teruggaaf) or paying a monthly amount (betaling)?
   - **Refund → stopzetten may be appropriate**
   - **Payment + amount is wrong → REDIRECT to change subflow**
   - **Payment + amount is correct → no action needed**
3. Why does the user want to stop?
   - Deductions no longer apply → stopzetten appropriate
   - Situation changed → review whether change or stopzetten is better
   - Wants to avoid repayment risk → stopzetten appropriate
   - Will file early and settle then → explain that the annual return handles this; stopzetten is optional

### Data collection steps

1. **Current voorlopige aanslag type** — receiving refund or making payments
2. **Current monthly amount** — how much per month
3. **Reason for wanting to stop** — to determine correct routing
4. **If redirecting to change:** collect all estimates as per the change subflow

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` with stopzetten context
2. Update `workspace/shared/assumptions.md`
3. If stopzetten is appropriate: include manual checklist for the Mijn Belastingdienst stopzetten process
4. If redirecting to change: generate change subflow output instead
5. Do NOT calculate final tax consequences unless all assumptions are explicit and confirmed

---

## Common rules across all subflows

- All amounts are estimates unless explicitly labeled as from-baseline
- Box 3 uses fictitious method only — werkelijk rendement is never collected
- Every workpack must include the "Not submission advice" footer
- Every workpack must include the DigiD warning
- Every workpack must list source_ids for all knowledge sources used
- Every workpack must include the assumptions section
- Output files go to `workspace/provisional/2026/` — never to `workspace/annual/`
