---
name: nl-tax-box1-home
description: Background helper that returns sourced Box 1 and own-home facts and questions; use annual 2025 evidence for annual workpacks and labeled 2026 estimates for provisional workpacks.
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Box 1 And Own Home

Background helper for box 1 income and eigen woning notes.

Use actual evidence and 2025 sources for annual workpacks. Use clearly labeled estimates and 2026 provisional sources for voorlopige aanslag workpacks. Read `workspace/taxpayer/evidence-index.yaml` directly; the agent, not Python, decides whether evidence is complete. For an annual input, only an evidence entry that is reviewed, successfully processed, and for the correct tax year closes the corresponding gap. A provisional estimate instead needs an explicit source and uncertainty note.

Python is optional. If the agent has already accepted the amounts for one ordinary home and Bash can access the resolved plugin script path, `scripts/validate_own_home_inputs.py` may check the arithmetic. Do not pass eligibility, mortgage qualification, ownership decisions, or complex-home facts to the script. If Python is unavailable, perform the same short manual check below; do not ask the user to install Python. Never copy bundled scripts into `workspace/` or execute a `.py` under `workspace/`, `uploads/`, or `evidence/`.

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

1. Use an existing note only when `source: user_chat` is explicitly confirmed, or when `source: file` links to an evidence entry that passes step 2.
2. For an annual file, close the input gap only when its evidence entry has `extraction_status: extracted`, `review_required: false`, and `tax_year` equal to the return year. Record `source: file` plus `evidence_id`. An `indexed_only`, `deferred`, or `failed` entry, an entry still requiring review, or a wrong-year entry never closes the gap.
3. For a provisional estimate, require an explicit source and uncertainty note; do not present the estimate as annual evidence.
4. If still missing, return a question packet entry and stop short of calculating that line.
5. Compute only from values that pass these gates or from an explicitly confirmed assumption.

## Own-home arithmetic parity

For one ordinary home, after the agent has accepted each amount:

1. Add mortgage interest, qualifying financing costs, and periodic erfpacht/opstal/beklemming as `total_deductible_own_home_costs`.
2. Compute `hillen_deduction` from the positive excess of eigenwoningforfait over that full total using the reviewed year percentage; otherwise use EUR 0.
3. Record `box1_balance_components` as eigenwoningforfait, `total_deductible_own_home_costs`, and `hillen_deduction`.
4. Compute `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
5. Put tariefsaanpassing only under `review_adjustments`; never include it in `box1_balance_components` or taxable Box 1 income.

Record `check_performed_by: checked_by_agent` for this manual path or
`check_performed_by: checked_by_script` when the optional helper checks the same
accepted amounts. Eligibility and complex own-home cases always remain with the
agent and may require manual review.

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
