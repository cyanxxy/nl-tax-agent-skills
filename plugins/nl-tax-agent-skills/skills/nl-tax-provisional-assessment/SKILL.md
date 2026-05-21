---
name: nl-tax-provisional-assessment
description: Prepare a conversational 2026 voorlopige aanslag manual-entry guide.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 *.py:*)
---

# NL Tax Provisional Assessment

Prepare local guidance for manually handling a 2026 voorlopige aanslag flow: request, change, review, or stopzetten.

This skill is conversational. Do not assume the user has prepared all estimates upfront. Ask category by category, accept uploaded files or chat values, persist after every turn, and generate the workpack only when the user confirms.

## Read first

Bundled paths (`reference/`, `templates/`, `_shared/`) are relative to this
skill's own directory; `_shared/` is `../_shared/`. If a path does not resolve
from your working directory, run `echo "$CLAUDE_SKILL_DIR"` in Bash and resolve
from there. Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second `workspace/`
tree.

Load as needed:

- Supported workflows and the relevant provisional references
- `_shared/knowledge/security/digid.md` and `_shared/knowledge/security/prompt-injection.md`
- 2026 provisional knowledge only
- `templates/provisional-pack.md`
- `workspace/taxpayer/profile.yaml`
- `workspace/taxpayer/evidence-index.yaml`, if present
- `workspace/shared/session-progress.yaml`

Confirm an active workflow candidate of `provisional_2026_request`, `provisional_2026_change`, `provisional_2026_review`, or `provisional_2026_stopzetten`. If the profile is missing or the workflow is wrong, hand back to intake.

### Resume guard

`session-progress.yaml` is the resume contract. Before doing any work:

- If `session-progress.yaml` is missing or empty, reconstruct it from `profile.yaml` and `_shared/templates/session-progress.yaml` before proceeding.
- If `profile.yaml` shows `intake_status: complete`, never restart intake - continue the provisional workflow from recorded progress.
- Skip any subsection already marked `complete` in `session-progress.yaml`.

## Hard scope rules

- Use only 2026 provisional sources and label amounts as estimates unless they come from a baseline.
- Do not use annual 2025 rates, credits, or logic.
- Do not request, calculate, or offer method choices for werkelijk rendement in provisional 2026.
- Use only the provisional fictitious Box 3 method.
- Do not write `workspace/annual/**`.

If the user asks about werkelijk rendement, respond: "Werkelijk rendement is not part of the 2026 voorlopige aanslag. It may become relevant when filing the annual 2026 return in 2027."

## Conversational behavior

For every subflow:

1. Use `workspace/shared/session-progress.yaml` to avoid re-asking answered questions.
2. Group at most 3 closely related questions per turn.
3. Accept file inputs or values stated in chat.
4. Record each value in `workspace/provisional/2026/notes/<section>.yaml` with `source` (`file`, `user_chat`, `assumption`, `unknown`, or `baseline`) and either `evidence_id`, `baseline_ref`, or `quote` plus `stated_at`.
5. If the user cannot answer, record `unknown`, add it to `workspace/shared/missing-info.md`, and continue.
6. Never silently treat missing values as zero.

## Subflow: request

Walk the user through these sections one at a time:

1. Confirm workflow.
2. Estimated 2026 employment income per employer.
3. Estimated 2026 pension and benefit income.
4. Estimated 2026 other income.
5. Estimated deductions, including own home, alimony, lijfrente/AOV, gifts, and other expenses.
6. Standard Box 2 estimates where applicable: regular benefits/dividends, disposal benefits, costs, withholding tax, BV lending fictitious benefit, and partner allocation.
7. Box 3 assets and debts on 1 January 2026 using the fictitious method only.
8. Fiscal partner and allocation.
9. Final review and confirmation.

## Subflow: change

1. Confirm `provisional_2026_change`.
2. Establish the baseline from the current beschikking or from chat.
3. Re-collect all current estimates, not just changed items. Remind the user every turn until confirmed: "When changing your voorlopige aanslag, you must enter ALL data again. Anything not re-entered defaults to zero. The new VA replaces the old one entirely."
4. Generate a delta summary comparing baseline and current estimates.
5. Ask for final confirmation before generating the workpack.

## Subflow: review

1. Confirm `provisional_2026_review`.
2. Collect the current VA baseline by file or chat.
3. Walk category by category and ask whether each item has changed since the VA was issued.
4. Record changes incrementally.
5. Generate review notes and recommend the change subflow if significant changes are found.
6. Ask for final confirmation before generating outputs.

## Subflow: stopzetten

1. Confirm `provisional_2026_stopzetten`.
2. Ask whether the user is receiving a monthly refund or paying a monthly amount.
3. If the user receives a refund and wants to stop, generate stopzetten guidance after confirmation.
4. If the user pays monthly and the amount is wrong, redirect to change; stopping payments does not reduce the debt.
5. If the user pays monthly and the amount is correct, confirm no action is needed.

## Workpack generation gate

Do not write `workspace/provisional/2026/provisional-pack.md` or related outputs until all of the following are true:

1. The subflow's final review is complete.
2. The user explicitly confirms in chat that the workpack should be generated.
3. All open items in `session-progress.yaml` for `provisional_2026` are answered, deferred, or recorded as confirmed assumptions.

When generating, preserve source provenance for every numeric line using `Src` codes from the templates and mark unresolved sections clearly.

## Output files

Write incrementally:

- `workspace/provisional/2026/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md`
- `workspace/shared/assumptions.md`

Write at the generation gate:

- `workspace/provisional/2026/provisional-pack.md`
- `workspace/provisional/2026/field-map.yaml`
- `workspace/provisional/2026/delta-summary.md` for change/review
- `workspace/provisional/2026/review-questions.md`

## Safety

- Do not log in, submit, sign, automate forms, handle DigiD, or collect BSN.
- Route complex Box 2 facts to manual review or unsupported: valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA cases.
- This workpack is a preparation aid, not tax advice or submission.

## End-of-turn report

After each turn, tell the user in 2-4 sentences which subflow and section were covered, what was recorded, and what comes next.
