---
name: nl-tax-provisional-assessment
description: Use when the user explicitly wants a 2026 Dutch provisional request, change, review, or stopzetten workpack. Changes require complete-data re-entry before questions; Box 3 is fictitious-only.
argument-hint: "[2026] [request|change|review|stopzetten|confirm]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Bash(python3:*)
---

# NL Tax Provisional Assessment

Prepare a local, source-traceable 2026 voorlopige-aanslag workpack for manual
entry or review. The taxpayer or an authorized human performs every
authenticated portal action. Do not use a browser, Claude in Chrome, computer
use, screen interaction, a connector, or another tool to open or operate the
portal; do not log in, enter or change values, click controls, sign, send,
submit, retrieve private account data, ask for, accept, store, or process
credentials or sessions, collect BSN, present a final calculation, or describe
the workpack as official advice.

This is an agent-led conversation, not a fixed interview or tax-decision
engine. Credit facts and evidence already supplied, ask the smallest useful
follow-up, persist after every turn, and keep one owning agent as the sole
writer and readiness authority.

## Activation and paths

Read `../_shared/runtime-contract.md` first. Resolve bundled resources relative
to this skill directory and every `workspace/...` path against the saved
`workspace_root`; never depend on vendor-specific environment variables or
create a second workspace tree.

Before the first user-facing reply on every turn, re-read:

1. `workspace/taxpayer/profile.yaml`
2. `workspace/shared/session-progress.yaml`
3. `workspace/taxpayer/evidence-index.yaml`, if it exists

Confirm one active candidate: `provisional_2026_request`,
`provisional_2026_change`, `provisional_2026_review`, or
`provisional_2026_stopzetten`. If profile/session state is absent, require
intake to create it and return to `nl-tax-intake`; do not create or reconstruct
intake-owned state. If intake is complete, never restart it.

When this candidate was activated by the completed annual-to-provisional
handoff, require `workflows.annual_2025.status: complete`,
`workflows.provisional_2026.status: in_progress`, and matching profile/session
candidates. The original natural-language request for both workflows authorizes
this collection to continue without another activation phrase. Leave the
completed annual section and all `workspace/annual/**` artifacts unchanged.

Only for a pre-1.4 state or a legacy complete profile without the three-state
AOW field, load `reference/resume-contract.md` and apply its normalization
without changing existing answers. Otherwise use the conversation ledger to
resume; it records facts and gaps but does not dictate question order.

## Progressive workflow loading

Load `reference/provisional-flow.md` when this workflow becomes active. Route
from the recorded user goal, then load exactly one active subflow:

- `reference/subflows/request.md`
- `reference/subflows/change.md`
- `reference/subflows/review.md`
- `reference/subflows/stopzetten.md`

For `provisional_2026_change`, always give this notice before asking any
questions: "Prepare and verify the complete dataset; the change form requires
all applicable categories, not only the changed item." With valid intake state,
read `reference/subflows/change.md` before that first change reply. If intake
state is absent, give the notice, return to intake for only its missing setup
facts, and load `change.md` as soon as intake records the change candidate.
Keep the reminder in every collection turn until final confirmation.

For change, load `reference/delta-rules.md` only while change is active. For
stopzetten, load `reference/stopzetten-guidance.md` only while stopzetten is
active. If a payment case redirects from stopzetten to change, persist the
redirect, stop using the stopzetten files, and load only the change files.

Load only the exact source resource required by the active subflow or topic:

- request procedure: `reference/source-projections/request-flow-human.md`
- change procedure: `reference/source-projections/change-flow-human.md`
- stopzetten procedure: `reference/source-projections/stopzetten-flow-human.md`
- review procedure: `../_shared/knowledge/years/2026/provisional/review-flow.md`
- rates and credits: `../_shared/knowledge/years/2026/provisional/rates-and-credits.md`
- Box 2: `../_shared/knowledge/years/2026/provisional/box2.md`
- FISIN / substantial-interest classification: `../_shared/knowledge/years/2026/provisional/fisin-aanmerkelijk-belang.md`
- Box 3: `../_shared/knowledge/years/2026/provisional/box3-provisional.md`
- own home: `../_shared/knowledge/years/2026/provisional/own-home.md`
- request/change baseline and delta: `../_shared/knowledge/years/2026/provisional/vva-eva-baseline-delta.md`
- payment/refund timing: `../_shared/knowledge/years/2026/provisional/refund-payment-timing.md`
- shared own-home details, only when applicable:
  `../_shared/knowledge/own-home/eigenwoningforfait.md` and
  `../_shared/knowledge/own-home/hypotheekrenteaftrek.md`
- fiscal-partner details, only when applicable:
  `../_shared/knowledge/partners/fiscal-partnership.md`

The three `*-human.md` resources are mechanically reversible runtime
projections of reviewed source notes. Use the projection header's `source_ids`
for provenance; the projection is not an independent review attestation. Do
not open the raw reviewed `request-flow.md`, `change-flow.md`, or
`stopzetten-flow.md` during a taxpayer workflow. Their registered
`snapshot_path` values are maintainer provenance only.

Record each actually consulted `source_id` once in
`sources_loaded_by_workflow.provisional_2026`, mirror that list in the
top-level `sources_loaded`, never fabricate a rate when a required note cannot
be loaded, and never use a 2025 annual rate sheet.

Do not preload `reference/provisional-output-contract.md` or output templates.
Load them only after the generation gate opens, together with only the active
subflow's additional template.

## Non-negotiable provisional boundaries

- Keep provisional 2026 and annual 2025 sources, notes, and outputs separate.
- Do not copy annual actuals into provisional state. A 2025 amount may inform a
  2026 estimate only after the taxpayer reviews or states that estimate; record
  it independently with provisional provenance.
- Label forward-looking amounts as estimates and carried values as baseline;
  never silently treat a missing value as zero.
- Box 3 uses the provisional fictitious method only. Never request, calculate,
  or offer a choice involving werkelijk rendement; explain that it may become
  relevant only for the later annual 2026 return.
- Apply AOW status as `below_all_year`, `reaches_during_year`, or
  `aow_all_year` from `person.aow_by_tax_year.2026` and the partner equivalent.
  Preserve the transition month, use the published month-specific
  first-bracket rate, and defer affected credits to the live portal result
  instead of choosing a whole-year credit table.
- For an eenmanszaak/ZZP, collect only a sourced, user-reviewed full-year
  `onderneming.geschatte_winst` forecast with manual review -- the winst before
  ondernemersaftrek and mkb-winstvrijstelling, excluding btw, with a minus sign
  for a loss. Include it in the Box 1 rollup and change delta; do not prepare
  annual accounts, entrepreneur deductions, a Zvw amount, cessation profit, or
  final tax.
- Surface the separate voorlopige aanslag Zorgverzekeringswet as a companion
  item: it is a second aanslag with its own change route. Coupling between an
  income-tax change and the Zvw assessment is not established in the reviewed
  sources, so naming it, requiring the taxpayer to check it separately, and
  recording what they find is required; sizing or merging a Zvw amount stays
  out of scope.
- Own-home review uses the WOZ value with peildatum 1 January 2025 and preserves
  all reviewed `box1_own_home_balance` components. Candidate Box 3 debts enter
  accepted totals only after the official inclusion/exclusion screen.
- The live Mijn Belastingdienst calculation and resulting beschikking control
  actual payment/refund amounts and timing; workpack deltas are review
  directions, not cash-flow predictions.
- Helpers and optional specialist reviewers return findings to the owner and do
  not choose estimates, allocations, or final readiness. The owner
  reconciles and persists their findings under `reference/provisional-flow.md`
  and the shared runtime contract.

## Generation and mapping

At final review, load `reference/provisional-output-contract.md`. Do not write
canonical outputs while any applicable
`sections.provisional_2026.subsections` member is `not_started` or
`in_progress`. Every applicable member must be `complete`, `chat_only`, or
`deferred`; every deferred item must be recorded in `missing-info.md` and no
blocking item may remain. `box2` and `winst_forecast` are always gate members
and may be marked complete as not applicable only from a profile fact or user
answer, never from a blank field. After those checks, summarize the readiness
status and artifacts, then ask whether the user wants them created now. Accept a
direct natural-language generation request made after that review, or an
unambiguous affirmative reply such as “yes”, “go ahead”, “looks good”, or a
natural Dutch equivalent to the immediately preceding scoped question. The
explicit `confirm` command is optional. Never require exact wording, reuse the
opening preparation request as final consent, or interpret an unrelated “yes”
as generation authorization; ask one short clarification when context is
ambiguous.

Load `templates/provisional-pack.md` only after that gate. Load
`templates/delta-summary.md` only for change and
`templates/review-questions.md` only for review. Recompute the workflow rollup
before mapping and retain this skill as active through validation.

For request and change only, invoke `nl-tax-field-mapper` after the confirmed
workpack is written. It alone writes and validates
`workspace/provisional/2026/field-map.yaml`; the confirmed workpack authorizes
that companion map without a second activation or consent phrase. A script may
check structure and provenance but cannot promote a draft. If a sourced fact
changes after generation, reset confirmation, present the updated summary, and
require fresh contextual confirmation before overwriting canonical outputs.
The income-tax field map MUST NOT contain a Zvw field or value: no Zvw
`field_id`, label, note, amount, baseline, estimate, or manual-entry row. The Zvw
companion remains workpack prose and a separate human check only.

After every output required for the active subflow validates and the
provisional rollup is complete, set
`workflows.provisional_2026.status: complete` in the profile and clear
`active_skill`. When this workflow began through the annual handoff, preserve
`workflows.annual_2025.status: complete` and the annual session section exactly
as handed off; for a provisional-only request, leave the untouched annual
`not_started` state unchanged. Keep the provisional owner active when its
rollup is still a draft or any required output fails validation.

Do not probe speculative template names, add repository/Git checks to taxpayer
self-checks, or treat a failed command as a successful validation.

## Outputs

Write incrementally:

- `workspace/provisional/2026/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md`
- `workspace/shared/assumptions.md` only when assumptions exist

At the generation gate, write the subflow outputs required by
`reference/provisional-output-contract.md`. The field mapper separately owns
the request/change `field-map.yaml`. Never write `workspace/annual/**`.

## End-of-turn report

In two to four sentences, tell the user which 2026 provisional-assessment topic
was covered, whether values came from uploaded/indexed files, chat, or a
baseline, and what comes next. Do not mention internal subflows, skill
handoffs, status names, or file maintenance.
