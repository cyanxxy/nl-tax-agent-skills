---
name: nl-tax-box1-home
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — returns Box 1 and eigen-woning facts and questions. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Box 1 And Own Home

Background helper for box 1 income and eigen woning notes.

Use actual evidence and 2025 sources for annual workpacks. Use clearly labeled estimates and 2026 provisional sources for voorlopige aanslag workpacks. Run the bundled scripts (`scripts/summarize_box1_inputs.py` and `scripts/validate_own_home_inputs.py`) when structured inputs are available and Bash can access the resolved plugin script path. If Bash cannot see the plugin path, continue manually from the sourced inputs and rules; never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

This helper participates in a conversational workflow. It does not assume all inputs are pre-staged. When values are missing, return a structured open-question packet for the calling skill instead of inventing zeros or treating missing values as not applicable.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Read first

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree. `_shared/` is the plugin-shared folder at this skill's
`../_shared/`. Resolve bundled files with host file tools (`Read` first, `Glob`
or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin
files: in Cowork, shell commands run in an isolated VM that may not see the
plugin cache even when `Read` and `Glob` can. If the host has already expanded
`${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine
for file tools; otherwise search within the loaded plugin/skill tree and resolve
relative to this skill directory.

Bundled references — read the ones matching the active workflow before computing any line:

- `reference/box1-2025.md` — annual 2025 box 1 income rules (annual workpacks)
- `reference/own-home-2025.md` — annual 2025 eigen-woning rules (annual workpacks)
- `reference/box1-2026-provisional.md` — 2026 provisional box 1 and own-home estimate rules (provisional workpacks; this is the "2026 provisional references" file the provisional workflow points at)

Workspace state:

- `workspace/shared/session-progress.yaml`, if present
- `workspace/taxpayer/profile.yaml`
- `workspace/taxpayer/evidence-index.yaml`, if present
- The relevant notes under `workspace/annual/2025/notes/` or `workspace/provisional/2026/notes/`

## Behavior

For every needed value, including employer count, gross income, loonheffing, WOZ value, mortgage interest, mortgage type, and outstanding mortgage balance:

1. Use existing notes when the value has `source: file` or `source: user_chat`.
2. Use evidence-index entries when available and record `source: file` plus `evidence_id`.
3. If still missing, return a question packet entry and stop short of calculating that line.
4. Compute only from values with a real source or an explicitly confirmed assumption.

## Question packet

Return missing inputs to the calling workflow in this shape:

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

The calling skill asks these questions, records the answer with `source`,
`quote`/`evidence_id`, and timestamp, then re-invokes this helper.

Return structured facts and open questions to the owning workflow. Do not
persist any final artifact, including shared notes, question packets, session
state, workpacks, or field maps. The annual/provisional workflow owns all
workspace persistence and may read historical helper notes for resume
compatibility only.
