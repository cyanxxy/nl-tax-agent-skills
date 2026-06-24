---
name: nl-tax-provisional-assessment
description: Prepare a 2026 voorlopige aanslag workpack — request, change, review, or stopzetten — for manual Mijn Belastingdienst entry. Use after intake routes to a provisional_2026 flow. Fictitious box 3 only; never collects werkelijk rendement.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-field-mapper/scripts/*.py:*)
---

# NL Tax Provisional Assessment

Prepare local guidance for manually handling a 2026 voorlopige aanslag flow: request, change, review, or stopzetten.

This skill is conversational. Do not assume the user has prepared all estimates upfront. Ask category by category, accept uploaded files or chat values, persist after every turn, and generate the workpack only when the user confirms.

## Read first

Bundled paths (`reference/`, `templates/`, `_shared/`) are relative to this
skill's own directory; `_shared/` is `../_shared/`. If a path does not resolve
from your working directory, run `echo "${CLAUDE_PLUGIN_ROOT}"` in Bash and
resolve from `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-provisional-assessment/`
(`CLAUDE_PLUGIN_ROOT` is set by Claude Code and Cowork; if unset, resolve
relative to your working directory). Prefer `${CLAUDE_PLUGIN_ROOT}` for
cross-host portability; Claude Code also exposes `${CLAUDE_SKILL_DIR}` (the
skill's own subdirectory) but Codex does not, so do not depend on
`CLAUDE_SKILL_DIR`. Resolve every `workspace/...` path against `workspace_root`
from `session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree.

Safety: only run Python under `${CLAUDE_PLUGIN_ROOT}/skills/.../scripts/` (this skill runs the bundled `nl-tax-field-mapper/scripts/validate_field_map.py`). Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

Before the first user-facing reply each turn, load the security notes and the profile/session state; before generating any numeric content, load the 2026 provisional rate sheets. Append every loaded `source_id` (from `_shared/source-register.yaml`) to `sections … sources_loaded` in `session-progress.yaml`; only those IDs may appear in the workpack's "Sources used" section.

Always:

- `_shared/knowledge/security/digid.md` and `_shared/knowledge/security/prompt-injection.md`
- `templates/provisional-pack.md`
- `workspace/taxpayer/profile.yaml`
- `workspace/taxpayer/evidence-index.yaml`, if present
- `workspace/shared/session-progress.yaml`

2026 provisional rate sheets and flow notes — canonical for every numeric line; do not paraphrase rates from memory, and if a sheet fails to load, stop and tell the user rather than fabricating a rate:

- `_shared/knowledge/years/2026/provisional/rates-and-credits.md`
- `_shared/knowledge/years/2026/provisional/box3-provisional.md`
- `_shared/knowledge/years/2026/provisional/box2.md`
- `_shared/knowledge/years/2026/provisional/own-home.md`
- `_shared/knowledge/years/2026/provisional/fisin-aanmerkelijk-belang.md`
- `_shared/knowledge/years/2026/provisional/vva-eva-baseline-delta.md`
- `_shared/knowledge/own-home/eigenwoningforfait.md` and `_shared/knowledge/own-home/hypotheekrenteaftrek.md`
- `_shared/knowledge/partners/fiscal-partnership.md`
- The active subflow's flow note: `_shared/knowledge/years/2026/provisional/request-flow.md`, `change-flow.md`, `review-flow.md`, or `stopzetten-flow.md` (all in the same directory)

Use only 2026 provisional sources — never load or reuse 2025 annual rate sheets.

Confirm an active workflow candidate of `provisional_2026_request`, `provisional_2026_change`, `provisional_2026_review`, or `provisional_2026_stopzetten`. If the taxpayer profile is missing or the workflow is wrong, continue with `nl-tax-intake` first.

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

### Helper delegation

Delegate the box and partner work to the background helpers instead of inlining it. Invoke the matching helper, collect its question packet from `workspace/shared/`, ask the user, record answers, then re-invoke:

- **Box 1 / own home** → `nl-tax-box1-home` (use the 2026 provisional references)
- **Box 2** → `nl-tax-box2` (label all amounts as estimates or baseline-derived)
- **Box 3** → `nl-tax-box3` (**fictitious method only** — never request werkelijk rendement)
- **Partner / allocation** → `nl-tax-partner-deductions`

Read the helpers' `workspace/shared/*-notes.md` back before assembling outputs. The helpers never write to `workspace/provisional/**`; this skill owns that tree.

## Subflow: request

Walk the user through these sections one at a time:

1. Confirm workflow. First check they have NOT already received a 2026 voorlopige aanslag: if they had a 2025 VA, the Belastingdienst auto-issues a 2026 one (EVA) with payments/refunds already starting in January. If a 2026 beschikking or monthly amount already exists, this is a change/review, not a request — route accordingly and use that beschikking as the baseline.
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
2. All open items in `session-progress.yaml` for `provisional_2026` are answered, deferred, or recorded as confirmed assumptions.
3. The user has typed one of these confirmation phrases verbatim in chat:
   - `generate the workpack`
   - `genereer de workpack`
   - `klaar voor workpack`

   Or the user has run `/nl-tax-agent-skills:nl-tax-provisional-assessment confirm`. Anything else (including "looks good", "yes", "ok", "sounds good") is **not** confirmation — ask explicitly: "Type 'generate the workpack' when you want me to assemble it."

When generating, preserve source provenance for every numeric line using `Src` codes from the templates and mark unresolved sections clearly.

When a `field-map.yaml` is produced (request and change subflows), after writing it run `nl-tax-field-mapper/scripts/validate_field_map.py` against it and treat validation failure as a blocking self-check item; the field-map MUST conform to the `nl-tax-field-mapper` schema (`templates/field-map-template.yaml` + `reference/provisional-field-map.md`) and use `field_id`s from that reference. The provisional field-map uses the fictitious Box 3 method only — never include werkelijk-rendement fields.

## Output files

Write incrementally:

- `workspace/provisional/2026/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md`
- `workspace/shared/assumptions.md`

Write at the generation gate (per-subflow scope — must match `reference/provisional-output-contract.md`):

- `workspace/provisional/2026/provisional-pack.md` (all subflows)
- `workspace/provisional/2026/field-map.yaml` (request, change)
- `workspace/provisional/2026/delta-summary.md` (change only)
- `workspace/provisional/2026/review-questions.md` (review only)

## Safety

- Do not log in, submit, sign, automate forms, handle DigiD, or collect BSN.
- Route complex Box 2 facts to manual review or unsupported: valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA cases.
- This workpack is a preparation aid, not tax advice or submission.

## Worked example

> Profile shows `provisional_2026_change`. The agent confirms the change subflow, reconstructs the baseline from the user's current beschikking, and every turn repeats the "enter ALL data again — anything not re-entered defaults to zero" reminder. It re-collects all current estimates (not just the changed salary), delegating Box 3 to `nl-tax-box3` using the fictitious method only — when the user asks about werkelijk rendement, it answers that this is not part of the 2026 voorlopige aanslag and may become relevant when filing the annual 2026 return in 2027. After the final review it waits for the verbatim `generate the workpack` phrase, then writes `provisional-pack.md`, `field-map.yaml`, and `delta-summary.md`.

## End-of-turn report

After each turn, tell the user in 2-4 sentences which 2026 voorlopige-aanslag topic was covered, what was recorded in plain language, and what comes next. Do not mention internal status names or file-maintenance details.
