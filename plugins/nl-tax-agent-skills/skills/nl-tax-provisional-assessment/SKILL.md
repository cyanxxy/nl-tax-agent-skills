---
name: nl-tax-provisional-assessment
description: Prepare a Dutch voorlopige aanslag 2026 request, change, review, or stopzetten guidance package from taxpayer profile, evidence, baseline, and current-year estimates.
argument-hint: "[2026] [request|change|review|stopzetten]"
context: fork
agent: general-purpose
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_SKILL_DIR}/../nl-tax-provisional-assessment/scripts/*.py *)
---

# NL Tax Provisional Assessment

Prepare a voorlopige aanslag 2026 workpack for one of four subflows: request, change, review, or stopzetten.

## When to use

- After the intake skill has identified a `provisional_2026` workflow
- The taxpayer profile at `workspace/taxpayer/profile.yaml` exists and contains a `workflow_candidate` matching one of: `provisional_2026_request`, `provisional_2026_change`, `provisional_2026_review`, `provisional_2026_stopzetten`

## Subflows

| Subflow    | Purpose                                                  |
|------------|----------------------------------------------------------|
| request    | Request a new voorlopige aanslag for 2026                |
| change     | Change an existing voorlopige aanslag for 2026           |
| review     | Check if an existing voorlopige aanslag is still correct |
| stopzetten | Stop monthly payments or refunds                         |

## Prerequisites

- Taxpayer profile exists at `workspace/taxpayer/profile.yaml`
- The profile contains a valid `workflow_candidate` for a provisional 2026 subflow
- For change, review, and stopzetten: the user has an existing voorlopige aanslag for 2026

## Knowledge sources

Use ONLY `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2026/provisional/**` for all provisional calculations, rates, and rules.

**NEVER use annual 2025 knowledge for provisional 2026 calculations.**

The following knowledge files apply:
- `box3-provisional.md` — box 3 fictitious return method and asset categories
- `request-flow.md` — 4-step request process
- `change-flow.md` — change procedure and full re-entry requirement
- `review-flow.md` — review triggers and comparison process
- `stopzetten-flow.md` — when to stop vs when to change
- `rates-and-credits.md` — provisional tax rates and credits for 2026
- `vva-eva-baseline-delta.md` — baseline + forecast + delta model

## BOX 3 HARD RULE

```
CRITICAL: For the 2026 voorlopige aanslag, use ONLY the fictitious return method for box 3.
Do NOT collect werkelijk rendement for 2026 provisional calculations.
Werkelijk rendement is not part of the provisional calculation; it may become relevant
later in the annual 2026 return.
```

If the user asks about werkelijk rendement in the context of the provisional 2026 assessment, respond with: "Werkelijk rendement is not part of the 2026 provisional assessment. It may become relevant when filing the annual 2026 return in 2027."

This is the single most critical validation in this skill. Violation of this rule produces an incorrect workpack.

## Annual/provisional separation

- NEVER use annual 2025 rates, credits, or rules for the provisional 2026 calculation
- NEVER apply annual return logic (backward-looking, evidence-based) to the provisional assessment (forward-looking, estimate-based)
- NEVER ask for werkelijk rendement in provisional 2026
- NEVER write output files to `workspace/annual/**`
- The provisional assessment is NOT "annual return lite" — it has its own logic, data requirements, and purpose

## Subflow: request

1. Read `workspace/taxpayer/profile.yaml`, confirm `workflow_candidate: provisional_2026_request`
2. Collect estimated 2026 employment income
3. Collect estimated 2026 pension/benefit income
4. Collect estimated 2026 other income
5. Collect estimated 2026 deductions:
   - Mortgage interest (hypotheekrente) and eigenwoningforfait
   - Alimony (alimentatie)
   - Insurance premiums (lijfrentepremie, arbeidsongeschiktheidsverzekering)
   - Other deductible expenses
6. Collect box 3 assets and debts as of 1 January 2026 (peildatum):
   - Categorie I: Banktegoeden (savings and bank deposits)
   - Categorie II: Overige bezittingen (other assets)
   - Categorie III: Schulden (debts, excluding eigenwoningschuld)
   - Apply heffingsvrij vermogen
   - Use FICTITIOUS METHOD ONLY — do NOT collect werkelijk rendement
7. If fiscal partner: collect partner data and determine optimal box 3 allocation
8. Generate provisional workpack using the template
9. ALL amounts MUST be labeled as estimates

## Subflow: change

1. Read `workspace/taxpayer/profile.yaml`, confirm `workflow_candidate: provisional_2026_change`
2. Read existing voorlopige aanslag baseline:
   - From evidence index if a beschikking is indexed
   - From user input if no evidence is available
   - Record the baseline in the workpack
3. Collect ALL current estimates — not just the changed items
   - **CRITICAL: When changing a voorlopige aanslag, the taxpayer must re-enter everything. The new assessment replaces the old one entirely. Any data not re-entered defaults to zero.**
4. Generate delta summary: baseline vs current estimates comparison table
5. Generate provisional workpack with change context
6. Include this reminder prominently: "When changing your voorlopige aanslag, you must enter ALL data again — not only the items that changed. The new voorlopige aanslag replaces the previous one entirely."

## Subflow: review

1. Read `workspace/taxpayer/profile.yaml`, confirm `workflow_candidate: provisional_2026_review`
2. Read existing voorlopige aanslag (from evidence or user input)
3. Walk through each category and compare to the user's current situation:
   - Income: has it changed since the voorlopige aanslag was issued?
   - Deductions: are they still applicable and at the same level?
   - Box 3: have assets or debts changed significantly?
   - Partner status: any changes?
4. Generate review notes: which items may need updating and why
5. If changes are needed: recommend running the change subflow
6. Generate review questions at `workspace/provisional/2026/review-questions.md`

## Subflow: stopzetten

1. Read `workspace/taxpayer/profile.yaml`, confirm `workflow_candidate: provisional_2026_stopzetten`
2. Determine whether the user RECEIVES a monthly refund (teruggaaf) or PAYS a monthly amount (betaling)
3. **If the user receives a monthly refund and wants to stop:**
   - Stopzetten is the appropriate action
   - Generate stopzetten guidance
   - Explain that refunds will cease and settlement happens at annual return time
   - Provide manual checklist for the official stopzetten path via Mijn Belastingdienst
4. **If the user pays a monthly amount and the amount is wrong:**
   - REDIRECT to the change subflow — stopzetten is NOT appropriate
   - Explain that stopping payments does not reduce what is owed
   - Explain the risk of a large lump-sum bill at annual return time
5. **If the user pays a monthly amount and it is correct:**
   - No action needed — confirm this
6. Do NOT calculate final tax consequences unless ALL assumptions are explicitly stated and confirmed by the user

## Safety rules

Read and follow:
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/digid.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/prompt-injection.md`

Do not share DigiD credentials. This skill does not log in, submit, sign, or act as you. Use official authorization routes, such as DigiD Machtigen, when someone else is helping you.

## Output files

Write these files as applicable to the subflow:

| File                                              | Subflow(s)                      |
|---------------------------------------------------|---------------------------------|
| `workspace/provisional/2026/provisional-pack.md`  | request, change, review, stopzetten |
| `workspace/provisional/2026/field-map.yaml`       | request, change, review         |
| `workspace/provisional/2026/delta-summary.md`     | change, review                  |
| `workspace/provisional/2026/review-questions.md`  | request, change, review, stopzetten |
| `workspace/shared/assumptions.md`                 | all                             |

**Must NOT write to `workspace/annual/**`.**

## Not submission advice

This workpack is a preparation aid. It does not constitute tax advice, does not submit a request, and does not interact with the Belastingdienst. You must review all information and submit through the official Mijn Belastingdienst portal using your DigiD. Do not share DigiD credentials with this tool.
