---
name: nl-tax-submit-companion
description: Create a manual submission checklist for Dutch annual return or voorlopige aanslag workflows. Does not log in, sign, submit, or handle DigiD.
argument-hint: "[annual|provisional] [2025|2026]"
disable-model-invocation: true
allowed-tools: Read Grep Write Edit
---

# nl-tax-submit-companion

Creates a manual submission checklist for the selected workflow (annual return or voorlopige aanslag). This is a manual-only skill (`disable-model-invocation: true`) -- it must be explicitly invoked by the user.

**This skill does NOT log in, sign, submit, or handle DigiD.** It only prepares a checklist that the taxpayer uses when manually completing the submission through the official Belastingdienst portal.

## What it does

1. Read the appropriate workpack and field map for the selected workflow
2. Check for blocking missing information that must be resolved before submission
3. Generate a workflow-specific submission checklist
4. Include partner signing requirements where relevant (fiscal partner situations)
5. Write the checklist to `workspace/shared/manual-submission-checklist.md`

## Reads

- `workspace/annual/2025/return-pack.md` and `field-map.yaml` (for annual workflow)
- `workspace/provisional/2026/provisional-pack.md` and `field-map.yaml` (for provisional workflow)
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/digid.md`

## Safety

- **This skill does NOT log in, submit, sign, or act as the taxpayer.**
- Do not share DigiD credentials with this tool or any person/tool.
- Use official authorization routes (DigiD Machtigen) when someone else is helping you with submission.
- All submission actions must be performed manually by the taxpayer (or their authorized representative) through the official Mijn Belastingdienst portal.
