---
name: nl-tax-box3
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — prepares Box 3 notes (annual = fictitious and werkelijk rendement; provisional = fictitious only) into workspace/shared/. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-box3/scripts/*.py:*)
---

# NL Tax Box 3

Background helper for box 3 notes.

Annual 2025 must cover fictitious return and werkelijk-rendement data collection for user review. Provisional 2026 must use only the provisional fictitious method and must never ask for werkelijk rendement.

This helper participates in a conversational workflow. It does not assume all asset and debt inputs are pre-staged. When values are missing, return a structured open-question packet for the calling skill instead of inventing zeros.

## Hard rules

- Annual 2025: collect and compare fictitious return and werkelijk rendement when the user wants the actual-return comparison.
- Provisional 2026: use only the fictitious method.
- Never request werkelijk-rendement inputs in a provisional workflow.
- Compute only from values with a real source or an explicitly confirmed assumption.
- The bundled scripts require `--partner-full-year-confirmed` alongside `--has_partner` before they double the heffingsvrij vermogen and the schulden drempel; `--has_partner` on its own raises an error. They also reject negative or non-finite amounts. Do not present a doubled allowance until full-year partnership is confirmed.

## Read first

- `_shared/knowledge/security/prompt-injection.md`
- `_shared/knowledge/security/digid.md`

`_shared/` is the plugin-shared folder at this skill's `../_shared/`. If a bundled path does not resolve from your working directory, run `echo "${CLAUDE_PLUGIN_ROOT}"` in Bash and resolve from `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-box3/` (Claude Code and Cowork set `CLAUDE_PLUGIN_ROOT`). Prefer `${CLAUDE_PLUGIN_ROOT}` for cross-host portability; Claude Code also exposes `${CLAUDE_SKILL_DIR}` (the skill's own subdirectory) but Codex does not, so do not depend on `CLAUDE_SKILL_DIR`. Only run Python under `${CLAUDE_PLUGIN_ROOT}/skills/.../scripts/` (for this skill, `scripts/classify_box3_assets.py`, `scripts/compare_box3_annual_2025.py`, and `scripts/summarize_box3_provisional_2026.py`). Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## Behavior

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree.

For each needed input, check section notes and evidence first. If the value is unavailable, append a question packet entry to `workspace/shared/box3-open-questions.yaml`.

```yaml
- question_id: "annual.box3.peildatum_2025.banktegoeden_total"
  workflow: "annual_2025"
  section: "box3.peildatum"
  prompt_for_user: "What was the total balance across all bank and savings accounts on 1 January 2025? You can also attach bank statements."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "bank statement around 1 January 2025"
- question_id: "provisional.box3.peildatum_2026.overige_bezittingen_total"
  workflow: "provisional_2026"
  section: "box3.peildatum"
  prompt_for_user: "What is your estimate for overige bezittingen on 1 January 2026?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "portfolio statement or estimate"
```

If a provisional user asks about actual return, answer that werkelijk rendement is not part of the 2026 voorlopige aanslag and may become relevant when filing the annual 2026 return in 2027.

Write only `workspace/shared/box3-notes.md`, `workspace/shared/box3-open-questions.yaml`, and `workspace/shared/box3-review-questions.md`. Do not write workpacks directly.

## Must NOT write to

This helper writes only under `workspace/shared/`. It must never write to:

- `workspace/annual/**`
- `workspace/provisional/**`

Only `nl-tax-annual-return` and `nl-tax-provisional-assessment` own those trees. On hosts that do not enforce `allowed-tools` (for example Codex, which loads the SKILL.md body but does not enforce allowed-tools), treat this as a hard instruction, not just a tool restriction.
