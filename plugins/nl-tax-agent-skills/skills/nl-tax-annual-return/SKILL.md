---
name: nl-tax-annual-return
description: Use when the user explicitly wants a 2025 Dutch annual-tax workpack for manual entry, including supported sole traders and Boxes 1–3.
argument-hint: "[2025] [confirm]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Bash(python3:*)
---

# NL Tax Annual Return

Prepare a local, source-traceable 2025 annual-return workpack for manual entry
in Mijn Belastingdienst. The taxpayer or an authorized human performs every
authenticated portal action. Do not use a browser, Claude in Chrome, computer
use, screen interaction, or another tool to open or operate the portal; do not
log in, enter values, click controls, sign, send, submit, collect credentials or
BSN, present a final calculation, or describe the workpack as official advice.

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

Confirm `workflow_candidate: annual_2025`. If profile/session state is absent,
require intake to create it and return to `nl-tax-intake`; do not create or
reconstruct intake-owned state. If intake is complete, never restart it.

For a request covering both supported workflows, annual 2025 must still be the
only active candidate and owner; the profile may also show provisional 2026 as
requested with status `queued`. Do not load provisional resources or write
provisional artifacts before the completed annual handoff in Phase 10.

For a pre-1.4 progress file, apply the legacy migration in
`../_shared/knowledge/methods/interactive-elicitation.md` without changing
existing answers. Use the saved conversation ledger to resume; it records facts
and gaps but does not dictate question order.

## Progressive workflow loading

Load `reference/annual-flow.md` when this workflow becomes active. It is the
common conversational, source-loading, helper, and reviewer contract. Then
load exactly one active phase file immediately before that phase; do not preload
later phases:

1. `reference/phases/01-preflight.md`
2. `reference/phases/01-5-filing-status.md`
3. `reference/phases/02-income.md`
4. `reference/phases/02a-winst.md`
5. `reference/phases/03-own-home.md`
6. `reference/phases/03a-box2.md`
7. `reference/phases/04-box3.md`
8. `reference/phases/05-deductions.md`
9. `reference/phases/05-5-credits.md`
10. `reference/phases/06-partner.md`
11. `reference/phases/07-field-map.md`
12. `reference/phases/08-missing-info.md`
13. `reference/phases/09-review-questions.md`
14. `reference/phases/10-assembly.md`

The paths above are exhaustive and directly loadable. Do not enumerate the
skill package, scan sibling skills, or search inactive phases for question IDs.
Use saved subsection status to choose the active phase. If a user reply
completes Phase N, this turn may advance to and act in Phase N+1; once the reply
asks an unresolved Phase N+1 question, stop resource loading and never preload
Phase N+2.

Each phase file names the reviewed knowledge required for that topic. Load only
applicable active-phase notes, record each actually consulted `source_id` once
in `sources_loaded_by_workflow.annual_2025`, mirror that list in the top-level
`sources_loaded`, and never fabricate a rate when a source cannot be loaded.

Do not load `reference/annual-output-contract.md` or
`templates/annual-return-pack.md` during collection. Phase 10 loads both only
after its explicit generation gate opens.

## Non-negotiable annual boundaries

- Keep annual 2025 and provisional 2026 sources, notes, and outputs separate.
- Never silently treat a missing value as zero. A chat value is valid sourced
  input; a deferred value stays open; an assumption requires explicit user
  acceptance.
- Standard eenmanszaak/ZZP support is preparation-only: organize finalized
  profit-and-loss and balance evidence, keep the business field map draft, and
  never derive final taxable business profit or entrepreneur deductions.
- Annual Box 3 collects fictitious and actual-return data for the official
  comparison; supplying actual-return data is not a taxpayer method election.
- Apply the three-state AOW review (`below_all_year`, `reaches_during_year`, or
  `aow_all_year`) and preserve a transition month where applicable.
- Helpers and optional specialist reviewers return findings to the owner and do
  not choose allocations, results, or final readiness. The owner reconciles and
  persists their findings under `reference/annual-flow.md` and the shared
  runtime contract.

## Generation and mapping

When final review is reached or the user asks to generate, load
`reference/phases/10-assembly.md`. It contains the contextual natural-language
confirmation contract, completion/deferred rules, regeneration reset,
output-contract self-check, and rollup-before-mapper ordering. Do not write a
canonical workpack or field map before that gate passes.

After the confirmed workpack is written, invoke `nl-tax-field-mapper`; it alone
writes and validates `workspace/annual/2025/field-map.yaml`. The confirmed
workpack authorizes this companion map without a second activation or consent
phrase. Keep validation implementation and the internal handoff invisible.

When Phase 10 completes a queued annual-to-provisional handoff, the user's
original request for both workflows authorizes provisional collection to begin
without another activation phrase. It does not replace the later provisional
final-generation confirmation.

Do not probe speculative template names, add repository/Git checks to taxpayer
self-checks, or treat a failed command as a successful validation.

## Outputs

Write incrementally:

- `workspace/annual/2025/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md`
- `workspace/shared/assumptions.md` only when assumptions exist

Write `workspace/annual/2025/return-pack.md` only in Phase 10. The field mapper
separately owns `workspace/annual/2025/field-map.yaml`. Never write
`workspace/provisional/**`.

## End-of-turn report

In two to four sentences, tell the user which tax topic was covered, whether
values came from uploaded/indexed files or chat, and what comes next. Do not
mention internal phases, skill handoffs, status names, or file maintenance.
