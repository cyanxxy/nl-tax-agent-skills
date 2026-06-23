---
name: nl-tax-box1-home
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — prepares Box 1 income and eigen-woning notes into workspace/shared/. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-box1-home/scripts/*.py:*)
---

# NL Tax Box 1 And Own Home

Background helper for box 1 income and eigen woning notes.

Use actual evidence and 2025 sources for annual workpacks. Use clearly labeled estimates and 2026 provisional sources for voorlopige aanslag workpacks. Run the bundled scripts when structured inputs are available. Only run Python under `${CLAUDE_PLUGIN_ROOT}/skills/.../scripts/` (for this skill, `scripts/validate_own_home_inputs.py` and `scripts/summarize_box1_inputs.py`). Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

This helper participates in a conversational workflow. It does not assume all inputs are pre-staged. When values are missing, return a structured open-question packet for the calling skill instead of inventing zeros or treating missing values as not applicable.

## Read first

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree. `_shared/` is the plugin-shared folder at this skill's
`../_shared/`. If a bundled path does not resolve from your working directory,
run `echo "${CLAUDE_PLUGIN_ROOT}"` in Bash and resolve from
`${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-box1-home/` (Claude Code and Cowork set
`CLAUDE_PLUGIN_ROOT`). Prefer `${CLAUDE_PLUGIN_ROOT}` for cross-host
portability; Claude Code also exposes `${CLAUDE_SKILL_DIR}` (the skill's own
subdirectory) but Codex does not, so do not depend on `CLAUDE_SKILL_DIR`.

- `_shared/knowledge/security/prompt-injection.md`
- `_shared/knowledge/security/digid.md`
- `workspace/shared/session-progress.yaml`, if present
- `workspace/taxpayer/profile.yaml`
- `workspace/taxpayer/evidence-index.yaml`, if present
- The relevant notes under `workspace/annual/2025/notes/` or `workspace/provisional/2026/notes/`

## Behavior

For every needed value, including employer count, gross income, loonheffing, WOZ value, mortgage interest, mortgage type, and outstanding mortgage balance:

1. Use existing notes when the value has `source: file` or `source: user_chat`.
2. Use evidence-index entries when available and record `source: file` plus `evidence_id`.
3. If still missing, append a question packet entry and stop short of calculating that line.
4. Compute only from values with a real source or an explicitly confirmed assumption.

## Question packet

Append missing inputs to `workspace/shared/box1-home-open-questions.yaml`:

```yaml
- question_id: "annual.box1.employment.gross_income.employer_1"
  workflow: "annual_2025"
  section: "box1.employment"
  prompt_for_user: "What was your gross 2025 employment income from this employer? You can also attach the jaaropgaaf."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "jaaropgaaf 2025"
- question_id: "annual.eigen_woning.woz_2024_for_2025"
  workflow: "annual_2025"
  section: "eigen_woning"
  prompt_for_user: "What is your WOZ-waarde with peildatum 1 January 2024, used for the 2025 return?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "WOZ-beschikking"
```

The calling skill asks these questions, records the answer with `source`, `quote`/`evidence_id`, and timestamp, then re-invokes this helper.

Write only `workspace/shared/box1-home-notes.md`, `workspace/shared/box1-home-open-questions.yaml`, and shared review questions under `workspace/shared/`. Do not write workpacks, mix years, store full identifiers, or handle credentials.

## Must NOT write to

This helper writes only under `workspace/shared/`. It must never write to:

- `workspace/annual/**`
- `workspace/provisional/**`

Only `nl-tax-annual-return` and `nl-tax-provisional-assessment` own those trees. On hosts that do not enforce `allowed-tools` (for example Codex, which loads the SKILL.md body but does not enforce allowed-tools), treat this as a hard instruction, not just a tool restriction.
