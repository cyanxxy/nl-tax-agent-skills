---
name: nl-tax-provisional-assessment
description: Prepare a 2026 voorlopige aanslag workpack — request, change, review, or stopzetten — for manual Mijn Belastingdienst entry. Use after intake routes to a provisional_2026 flow. Fictitious box 3 only; never collects werkelijk rendement.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Provisional Assessment

Prepare local guidance for manually handling a 2026 voorlopige aanslag flow: request, change, review, or stopzetten.

This skill is conversational. Do not assume the user has prepared all estimates upfront. Ask category by category, accept uploaded files or chat values, persist after every turn, and generate the workpack only when the user confirms.

## Read first

Bundled paths (`reference/`, `templates/`, `_shared/`) are relative to this
skill's own directory; `_shared/` is `../_shared/`. Resolve bundled files with
host file tools (`Read` first, `Glob` or `Grep` if a path is not obvious). Do
not use Bash to discover or read plugin files: in Cowork, shell commands run in
an isolated VM that may not see the plugin cache even when `Read` and `Glob`
can. If the host has already expanded `${CLAUDE_PLUGIN_ROOT}` or
`${CLAUDE_SKILL_DIR}`, those absolute paths are fine for file tools; otherwise
search within the loaded plugin/skill tree and resolve relative to this skill
directory. Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second `workspace/`
tree.

Field-map resources are sibling-skill paths, never local `templates/` or
`reference/` paths: `nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/provisional-field-map.md`, and
`nl-tax-field-mapper/scripts/validate_field_map.py`. The field mapper owns use
of those resources and the canonical map artifact.

Before the first user-facing reply each turn, load the profile/session state; before generating any numeric content, load the 2026 provisional rate sheets (each sheet once, when first needed — re-read on resume). Record every loaded `source_id` (from `_shared/source-register.yaml`) in the top-level `sources_loaded` list in `session-progress.yaml` — once per ID, never appending duplicates on a re-read; only those IDs may appear in the workpack's "Sources used" section.

**Source-pack staleness check (warn, don't block):** the first time knowledge files are loaded in a session, compare each loaded source's `last_checked` in `_shared/source-register.yaml` against its `freshness_policy` cadence and today's date. If any source required by this workflow is past its cadence, tell the user once, in one sentence, that the source pack may be stale (name the stale `source_id`s) and that values should be double-checked in Mijn Belastingdienst. Staleness never blocks workpack generation; record the stale `source_id`s in the workpack's review items instead.

Workspace state — re-read every turn:

- `workspace/taxpayer/profile.yaml`
- `workspace/taxpayer/evidence-index.yaml`, if present
- `workspace/shared/session-progress.yaml`

Bundled references and templates — load once when this skill becomes active, and re-read them when resuming a session from disk or when the subflow changes (they do not change mid-conversation):

- `reference/provisional-flow.md` — the ordered subflow procedure this skill follows
- `reference/provisional-output-contract.md` — the structural and safety rules for every output
- `reference/delta-rules.md` — baseline-vs-current delta rules (change subflow)
- `reference/stopzetten-guidance.md` — refund-vs-payment routing and cutoff guidance (stopzetten subflow)
- `templates/provisional-pack.md`
- `templates/delta-summary.md` when the active subflow is `provisional_2026_change`
- `templates/review-questions.md` when the active subflow is `provisional_2026_review`

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

- If `session-progress.yaml` is missing or empty, require intake to create it:
  return control to `nl-tax-intake` and do not create provisional artifacts.
- For a pre-1.4 state, migrate it in place as defined by the shared elicitation
  contract: add missing `provisional_2026.subsections.box2`,
  `annual_2025.subsections.winst`, and
  `provisional_2026.subsections.winst_forecast` entries without changing
  existing answers, then set version 1.4. Treat `box2` and `winst_forecast` as
  generation-gate members. Mark either `complete` with a stable answered `not
  applicable` entry only after profile facts or a user answer support that.
- If `profile.yaml` shows `intake_status: complete`, never restart intake - continue the provisional workflow from recorded progress.
- Skip any subsection already marked `complete` in `session-progress.yaml`.

## Hard scope rules

- Use only 2026 provisional sources and label amounts as estimates unless they come from a baseline.
- Do not use annual 2025 rates, credits, or logic.
- Do not request, calculate, or offer method choices for werkelijk rendement in provisional 2026.
- Use only the provisional fictitious Box 3 method.
- Do not write `workspace/annual/**`.
- For an eenmanszaak/ZZP, invoke or inline `nl-tax-winst` in provisional mode
  and collect only a sourced, user-reviewed expected-profit forecast for the
  portal section `Winst uit onderneming`. Map it only as
  `onderneming.geschatte_winst`, with `manual_review_required: true`.
- Never substitute a generic other-income field for expected business profit.
  Do not prepare annual accounts, entrepreneur deductions, Zvw, cessation
  profit, or final tax in this flow.

If the user asks about werkelijk rendement, respond: "Werkelijk rendement is not part of the 2026 voorlopige aanslag. It may become relevant when filing the annual 2026 return in 2027."

If the user asks about entrepreneur deductions for the voorlopige aanslag,
explain that this flow records only their reviewed full-year expected-profit
forecast; annual deductions and final tax remain outside this preparation.

## Conversational behavior

For every subflow:

1. Use `workspace/shared/session-progress.yaml` to avoid re-asking answered questions.
2. Group at most 3 closely related questions per turn.
3. Accept file inputs or values stated in chat.
4. Record each value in `workspace/provisional/2026/notes/<section>.yaml` with `source` (`file`, `user_chat`, `assumption`, `unknown`, or `baseline`) and either `evidence_id`, `baseline_ref`, or `quote` plus `stated_at`.
5. If the user cannot answer, record `unknown`, add it to `workspace/shared/missing-info.md`, and continue.
6. Never silently treat missing values as zero.

### Helper delegation

Use the box and partner helpers as the canonical contracts for their sections.
If the host exposes a Skill/Task-style tool, invoke them; otherwise inline their
instructions. In both modes each helper returns structured facts and open
questions in its response and writes nothing. This owning workflow must
persist the returned facts and open questions in the matching
`workspace/provisional/2026/notes/<section>.yaml`, update session state, ask the
user, and re-run the helper with newly sourced answers.

- **Box 1 / own home** → `nl-tax-box1-home` (use the 2026 provisional references)
- **Winst uit onderneming forecast** → `nl-tax-winst` in provisional mode; persist only `onderneming.geschatte_winst` with provenance and manual review
- **Box 2** → `nl-tax-box2` (label all amounts as estimates or baseline-derived)
- **Box 3** → `nl-tax-box3` (**fictitious method only** — never request werkelijk rendement)
- **Partner / allocation** → `nl-tax-partner-deductions`

Historical `workspace/shared/*-notes.md`, `*-open-questions.yaml`, and helper
review files remain readable for resume compatibility only. They must not be
updated or created in a new run. Fold any useful legacy content into the
workflow-owned provisional notes before continuing. This skill owns session
state, provisional notes, and provisional workpacks; helpers own no persisted
artifact.

## Subflow: request

Walk the user through these sections one at a time:

1. Confirm workflow. A later unsolicited 2026 voorlopige aanslag may be issued
   from earlier data, but it is not guaranteed. Check whether a current 2026
   beschikking or monthly amount already exists. If it does, this is a
   change/review rather than a request; route accordingly and use that
   beschikking as the baseline.
2. Estimated 2026 employment income per employer.
3. Estimated 2026 pension and benefit income.
4. Estimated 2026 other income.
5. Expected 2026 profit from enterprise, when applicable: one sourced and user-reviewed `onderneming.geschatte_winst` forecast only.
6. Estimated deductions, including own home, alimony, lijfrente/AOV, gifts, and other expenses.
7. Standard Box 2 estimates where applicable: regular benefits/dividends, disposal benefits, costs, withholding tax, BV lending fictitious benefit, and partner allocation.
8. Box 3 assets and debts on 1 January 2026 using the fictitious method only.
9. Fiscal partner and allocation.
10. Final review and confirmation.

## Subflow: change

1. Confirm `provisional_2026_change`.
2. Establish the baseline from the current beschikking or from chat.
3. Re-collect all current estimates, not just changed items. Remind the user every turn until confirmed: "Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item."
4. Generate a delta summary comparing baseline and current estimates.
5. Ask for final confirmation before generating the workpack.

## Subflow: review

1. Confirm `provisional_2026_review`.
2. Collect the current VA baseline by file or chat.
3. Walk category by category and ask whether each item has changed since the VA was issued.
4. Record changes incrementally.
5. Generate `workspace/provisional/2026/review-questions.md` from `templates/review-questions.md` and recommend the change subflow if significant changes are found.
6. Ask for final confirmation before generating outputs.

## Subflow: stopzetten

1. Confirm `provisional_2026_stopzetten`.
2. Compare the current date with the stopzetten cutoff before asking for a manual checkbox. If the current date is on or after 2026-10-01, do not generate a stopzetten checklist; record the cutoff as passed and explain that the annual return or a change/review flow is the remaining route.
3. Ask whether the user is receiving a monthly refund or paying a monthly amount.
4. If the user receives a refund, it is before 2026-10-01, and the user wants to stop, generate structured stopzetten guidance in the workpack's `Stopzetten outcome` section after confirmation.
5. If the user pays monthly and the amount is wrong, redirect to change; stopping payments does not reduce the debt. To avoid a stopzetten loop, mutate progress before the next question: set `active_workflow: provisional_2026_change`, set `provisional_2026.subflow: change`, record the known payment baseline (monthly amount, beschikking details if stated) in `workspace/provisional/2026/notes/baseline.yaml` with provenance and mark the `baseline` subsection `in_progress`, mark `stopzetten_direction` as `complete` with `answered: ["routed_to_change_payment_case"]`, and reset `confirm` to `not_started`.
6. If the user pays monthly and the amount is correct, confirm no action is needed.

## Workpack generation gate

Do not write `workspace/provisional/2026/provisional-pack.md` or related outputs until all of the following are true:

1. The subflow's final review is complete.
2. Every applicable `provisional_2026` subsection, including `winst_forecast`
   and `box2`, exists and has terminal status `complete`, `chat_only`, or `deferred`.
   Mark a subsection `complete` with a stable
   answered `not applicable` entry only when profile facts or a user answer
   establish that it does not apply. An empty `open_questions` list is not sufficient:
   a `not_started` or `in_progress` subsection keeps the workpack
   in draft and blocks generation.
3. Every deferred item is present in `workspace/shared/missing-info.md` or is a
   confirmed assumption in `workspace/shared/assumptions.md`.
4. The user has typed one of these confirmation phrases verbatim in chat:
   - `generate the workpack`
   - `genereer de workpack`
   - `klaar voor workpack`

   Or the user has run `/nl-tax-agent-skills:nl-tax-provisional-assessment confirm`. Anything else (including "looks good", "yes", "ok", "sounds good") is **not** confirmation — ask explicitly: "Type 'generate the workpack' when you want me to assemble it."

When generating, preserve source provenance for every numeric line using `Src` codes from the templates and mark unresolved sections clearly.

For request and change subflows, after the confirmed workpack is written,
invoke `nl-tax-field-mapper`. Pass it the workpack and workflow context; it
alone writes and validates `workspace/provisional/2026/field-map.yaml` using
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/provisional-field-map.md`, and
`nl-tax-field-mapper/scripts/validate_field_map.py`. Treat a mapper-reported
validation failure as blocking before presenting the manual-entry map. The
provisional map uses the fictitious Box 3 method only.

## Output files

Write incrementally:

- `workspace/provisional/2026/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md` (seed from `_shared/templates/missing-info.md` on first write)
- `workspace/shared/assumptions.md` (seed from `_shared/templates/assumptions.md` on first write)

Write at the generation gate (per-subflow scope — must match `reference/provisional-output-contract.md`):

- `workspace/provisional/2026/provisional-pack.md` (all subflows)
- `workspace/provisional/2026/delta-summary.md` (change only)
- `workspace/provisional/2026/review-questions.md` from `templates/review-questions.md` (review only)

For request and change, the invoked field mapper separately produces the
unchanged public artifact `workspace/provisional/2026/field-map.yaml`; this
workflow does not write it.

## Safety

- Do not log in, submit, sign, automate forms, or collect BSN.
- Route complex Box 2 facts to manual review or unsupported: valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA cases.
- This workpack is a preparation aid, not tax advice or submission.

## Worked example

> Profile shows `provisional_2026_change`. The agent confirms the change subflow, reconstructs the baseline from the user's current beschikking, and every turn repeats the "prepare and verify the complete dataset; include all applicable categories, not only the changed item" reminder. It re-collects all current estimates (not just the changed salary), delegating Box 3 to `nl-tax-box3` using the fictitious method only — when the user asks about werkelijk rendement, it answers that this is not part of the 2026 voorlopige aanslag and may become relevant when filing the annual 2026 return in 2027. After the final review it waits for the verbatim `generate the workpack` phrase, writes `provisional-pack.md` and `delta-summary.md`, then invokes `nl-tax-field-mapper` to produce the canonical `field-map.yaml`.

## End-of-turn report

After each turn, tell the user in 2-4 sentences which 2026 voorlopige-aanslag topic was covered, what was recorded in plain language, and what comes next. Do not mention internal status names or file-maintenance details.
