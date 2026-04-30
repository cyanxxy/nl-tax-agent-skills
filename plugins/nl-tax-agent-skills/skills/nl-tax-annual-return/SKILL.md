---
name: nl-tax-annual-return
description: Prepare a Dutch annual income-tax return 2025 workpack from taxpayer profile, evidence index, and local annual tax knowledge.
argument-hint: "[2025]"
context: fork
agent: general-purpose
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_SKILL_DIR}/../nl-tax-annual-return/scripts/*.py *)
---

# NL Tax Annual Return

Prepare a complete annual income-tax return workpack for tax year 2025 (aangifte inkomstenbelasting 2025). The workpack is a preparation document that the taxpayer uses when filing through the official Mijn Belastingdienst portal -- it does not file, submit, or sign anything.

## When to use

- After the intake skill has identified the `annual_2025` workflow
- The taxpayer profile at `workspace/taxpayer/profile.yaml` exists and has `workflow_candidate: annual_2025`
- Evidence has been indexed (or at least partially indexed) in `workspace/taxpayer/evidence-index.yaml`
- The user explicitly wants to prepare their 2025 annual return

## Prerequisites

1. **Taxpayer profile exists** at `workspace/taxpayer/profile.yaml` with `workflow_candidate: annual_2025`
2. **Evidence index exists** at `workspace/taxpayer/evidence-index.yaml` (partial indexing is acceptable -- missing evidence will be flagged in the workpack)
3. **Shared knowledge is available** under `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/annual/**` and `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/**`

## What this skill does

Produces a complete annual return workpack for 2025, written to `workspace/annual/2025/return-pack.md`. The workpack covers all income boxes, deductions, credits, partner allocation, and submission preparation. It follows the template at `templates/annual-return-pack.md` and must include every section defined in the output contract at `reference/annual-output-contract.md`.

## Step-by-step workflow

Execute the following steps in order. Do not skip steps. If a step cannot be completed due to missing data, note the gap and continue.

### Step 1 — Read the taxpayer profile

Read `workspace/taxpayer/profile.yaml`. Extract:
- Personal details (date of birth, residency status)
- Workflow confirmation (`workflow_candidate` must be `annual_2025`)
- Fiscal partner status and partner details
- Any notes or flags from intake

### Step 2 — Read the evidence index

Read `workspace/taxpayer/evidence-index.yaml`. Build a summary of:
- Which evidence files are available and classified
- Which tax categories have supporting evidence
- Which evidence items are flagged for review
- Confidence levels for classifications

### Step 3 — Read annual 2025 knowledge

Read ALL files under `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/annual/`:
- `box1-rates.md` — income tax brackets and rates
- `credits.md` — heffingskortingen (algemene heffingskorting, arbeidskorting, etc.)
- `deductions.md` — persoonsgebonden aftrek, lijfrentepremie, etc.
- `evidence-checklist.md` — required documents per category
- `filing-flow.md` — the four-step filing process
- `own-home.md` — eigenwoningforfait, hypotheekrenteaftrek, tariefsaanpassing

### Step 4 — Read box 3 knowledge

Read ALL files under `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/`:
- `fictitious.md` — forfaitair rendement calculation (categories, percentages, peildatum)
- `actual-return.md` — werkelijk rendement data collection and comparison
- `examples.md` — worked examples for box 3 calculations

### Step 5 — Check for unsupported case markers

Verify the taxpayer profile does not contain unsupported case markers:
- Full-year Dutch resident: confirmed
- Individual taxpayer (not IB-onderneming as primary): confirmed
- Living taxpayer: confirmed
- No M-biljet required: confirmed

If any marker indicates an unsupported case, stop and inform the user. Do not generate a workpack for unsupported cases.

### Step 6 — Compile income notes (box 1)

From the evidence index and profile, compile:
- Employment income (loon uit dienstbetrekking) — from jaaropgaven
- Pension income — from pension jaaroverzichten
- Benefit income (uitkeringen) — from UWV/SVB jaaropgaven
- Other box 1 income — from evidence or user-provided data

For each income source, record the amount, the evidence_id, and any discrepancies or review notes.

### Step 7 — Compile own-home notes

If the taxpayer has an eigen woning:
- WOZ-waarde from WOZ-beschikking (evidence_id)
- Mortgage interest from jaaroverzicht hypotheek (evidence_id)
- Calculate eigenwoningforfait using the rate table from `own-home.md`
- Calculate tariefsaanpassing if income exceeds schijf 3 threshold
- Calculate Hillenregeling if applicable (low/zero mortgage)
- Determine net own-home result

### Step 8 — Compile box 3 notes

Compile BOTH fictitious and actual return data. This is required for the annual 2025 return.

#### Fictitious return (forfaitair rendement)
- Collect asset values per category on peildatum 1 January 2025
- Banktegoeden (category I, 0.36%)
- Overige bezittingen (category II, 6.04%)
- Schulden (category III, 2.47%)
- Calculate weighted fictitious return percentage
- Apply heffingsvrij vermogen (EUR 57,000 single / EUR 114,000 partners)
- Calculate rendementsgrondslag, forfaitair rendement, and box 3 tax at 36%

#### Actual return (werkelijk rendement) data collection
- Collect actual interest received on bank accounts
- Collect dividends received
- Collect rental income (net of attributable costs)
- Collect realized capital gains/losses
- Collect unrealized value changes (mark-to-market for listed securities)
- Collect deductible costs (custody fees, transaction costs)

#### Comparison
- Present fictitious return calculation alongside actual return data
- Note which method appears more favorable
- Note that the final election happens in the official filing environment

#### Partner allocation for box 3
- If fiscal partners: compute optimal allocation split
- Note that the allocation percentage applies to the entire box 3 base

### Step 9 — Compile deductions notes

From evidence and profile:
- Alimentatie (partneralimentatie only -- kinderalimentatie is NOT deductible)
- Specifieke zorgkosten (medical expenses above the drempel)
- Giften (periodic and incidental, ANBI verification)
- Lijfrentepremie (annuity premium, jaarruimte/reserveringsruimte)
- Other deductions (studiekosten if applicable, restant persoonsgebonden aftrek)

For each deduction, note the amount, threshold/drempel calculations, evidence_id, and any assumptions.

### Step 10 — Compile fiscal partner notes

If the taxpayer has a fiscal partner:
- Confirm partner status (married, registered partnership, cohabiting with conditions)
- List allocatable items: eigen woning result, box 3 grondslag, persoonsgebonden aftrek
- Note non-allocatable items: arbeidskorting, ondernemersaftrek
- Identify review points for optimal allocation

### Step 11 — Generate field map summary

Generate or reference a field map that maps each workpack item to the corresponding field in the Belastingdienst online return. Write the field map to `workspace/annual/2025/field-map.yaml`.

This field map is separate from any provisional field maps and must only reference annual return fields.

### Step 12 — List missing information

Compile all information gaps identified during steps 6-10:
- Missing evidence (e.g., no jaaropgaaf for a reported employer)
- Incomplete data (e.g., bank balance on 1 January 2025 not confirmed)
- Items requiring user input (e.g., actual interest received for werkelijk rendement)

Write or update `workspace/shared/missing-info.md` with items tagged `workflow: annual_2025`.

### Step 13 — List assumptions

Compile all assumptions made during workpack generation:
- Assumed values where evidence was incomplete
- Assumed tax treatment where multiple options exist
- Assumed partner allocation where not explicitly chosen

Each assumption must have an `assumption_id` and be listed in `workspace/shared/assumptions.md` with tag `workflow: annual_2025`.

### Step 14 — Generate human review checklist

Create a checklist of items requiring human verification before filing:
- All income sources accounted for
- Evidence matches reported amounts
- Box 3 peildatum values verified
- Box 3 method choice reviewed (fictitious vs actual)
- Partner allocation reviewed
- Deductions have supporting evidence
- All assumptions reviewed and confirmed
- Missing information resolved or accepted

### Step 15 — Write the workpack

Assemble all compiled sections into the workpack using the template at `templates/annual-return-pack.md`. Write the completed workpack to `workspace/annual/2025/return-pack.md`.

Verify the output against the contract at `reference/annual-output-contract.md` before finalizing.

## Safety

Read and follow:
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/digid.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/prompt-injection.md`

Do not share DigiD credentials. This skill does not log in, submit, sign, or act as you. Use official authorization routes, such as DigiD Machtigen, when someone else is helping you.

Every workpack must include the "Not submission advice" section. This section is mandatory and must not be removed or weakened.

## Output contract

The workpack must include ALL required sections defined in `reference/annual-output-contract.md`. See that file for validation rules, source attribution requirements, and structural constraints.

## Output files

Write:
- `workspace/annual/2025/return-pack.md` — the complete workpack
- `workspace/annual/2025/field-map.yaml` — field map for the annual return
- `workspace/shared/missing-info.md` — updated with annual_2025 items
- `workspace/shared/assumptions.md` — updated with annual_2025 items

## Write restrictions

Do NOT write to:
- `workspace/provisional/**` — provisional assessment output belongs to a different skill
- `${CLAUDE_SKILL_DIR}/../**` — do not modify skill definitions or knowledge files

## Knowledge scope

This skill uses annual 2025 knowledge only:
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/annual/**`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/**`

Do NOT use provisional 2026 knowledge (`${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2026/provisional/**`) for annual return preparation. The annual return is backward-looking at tax year 2025; provisional knowledge is forward-looking at tax year 2026.

## Box 3 scope

The annual 2025 return supports BOTH methods for box 3:
- **Fictitious return (forfaitair rendement):** the standard calculation using asset categories and fixed percentages
- **Actual return (werkelijk rendement):** the opt-in method where the taxpayer provides actual income and value changes

Both methods must be covered in the workpack. The actual return option is ONLY available in the annual return -- it is never available in the voorlopige aanslag. The workpack collects data for both methods and presents a comparison, but the final election happens in the official filing environment.

## After workpack generation

Tell the user:
1. The workpack has been written to `workspace/annual/2025/return-pack.md`
2. How many missing information items remain
3. How many assumptions were made
4. That they should review the human review checklist before filing
5. That filing happens through Mijn Belastingdienst using their DigiD -- this tool does not file the return
