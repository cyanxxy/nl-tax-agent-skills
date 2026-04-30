---
name: nl-tax-intake
description: Determine the correct Dutch tax workflow and create a taxpayer profile for annual return 2025 or voorlopige aanslag 2026.
argument-hint: "[annual|provisional|review|stopzetten]"
context: fork
allowed-tools: Read Grep Write Edit
---

# NL Tax Intake

Determine which Dutch tax workflow applies and create the base taxpayer profile.

## When to use

- User wants to file a Dutch income tax return
- User wants to request, change, review, or stop a voorlopige aanslag
- User mentions Dutch taxes, belastingaangifte, aangifte, or voorlopige aanslag
- First contact for any Dutch tax preparation task

## What this skill does

1. **Screen the taxpayer** — determine if the case is within v1 scope
2. **Identify the workflow** — annual return 2025, or voorlopige aanslag 2026 (request/change/review/stopzetten)
3. **Create the taxpayer profile** — write `workspace/taxpayer/profile.yaml`
4. **Identify missing information** — write `workspace/shared/missing-info.md`
5. **Record assumptions** — write `workspace/shared/assumptions.md`

## Screening questions

Ask these in order, stopping if the case is out of scope:

### 1. Residency
- Were you a Dutch resident for the full tax year?
- If part-year or non-resident: route to unsupported case

### 2. Taxpayer type
- Are you an individual (not a business/BV)?
- If entrepreneur with IB-onderneming as primary case: route to unsupported (v1 covers employed/pension/benefit income)

### 3. Living status
- Is this for a living taxpayer?
- If deceased: route to unsupported case

### 4. Workflow selection
- **Annual return 2025:** User wants to file their 2025 income tax return
- **Provisional 2026 request:** User wants to request a new voorlopige aanslag for 2026
- **Provisional 2026 change:** User wants to change an existing voorlopige aanslag for 2026
- **Provisional 2026 review:** User wants to check if their voorlopige aanslag is still correct
- **Provisional 2026 stopzetten:** User wants to stop their voorlopige aanslag

### 5. Fiscal partner
- Do you have a fiscal partner?
- If yes: note partner status, do NOT collect partner DigiD

## Safety rules

Read and follow:
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/digid.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/prompt-injection.md`

Do not share DigiD credentials. This skill does not log in, submit, sign, or act as you. Use official authorization routes, such as DigiD Machtigen, when someone else is helping you.

## Unsupported cases

Read `${CLAUDE_SKILL_DIR}/../nl-tax-intake/reference/unsupported-cases.md` for the full list. When a case is unsupported:

1. Clearly tell the user their case is not covered in v1
2. Set `workflow_candidate: unsupported` in the profile
3. Suggest they consult a tax adviser or use the official Belastingdienst portal
4. Do NOT attempt to generate a workpack for unsupported cases

## Output files

Write these files:
- `workspace/taxpayer/profile.yaml` — use the template from `templates/taxpayer-profile.yaml`
- `workspace/shared/missing-info.md` — list all information still needed
- `workspace/shared/assumptions.md` — list all assumptions made

Do NOT write to:
- `workspace/annual/**`
- `workspace/provisional/**`

## After intake

Tell the user which workflow was selected and what happens next:
- Annual 2025 → suggest uploading evidence, then running the annual return skill
- Provisional 2026 → explain what estimates are needed, then running the provisional assessment skill
