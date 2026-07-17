---
name: nl-tax-intake
description: Use when the user explicitly wants to start Dutch annual 2025/provisional 2026 tax work or asks a bundled-rule question. Do not use after intake is complete; informational questions create no state.
argument-hint: "[annual|request|change|review|stopzetten]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
---

# NL Tax Intake

Open a supported Dutch tax conversation and progressively build the taxpayer
profile. This skill is **conversational, not a fixed interview**: credit facts
and evidence already supplied, ask only the smallest useful follow-up, and let
the conversation determine the order.

## Always-on authenticated-portal boundary

Never use a browser, Claude in Chrome, computer use, screen interaction, a
connector, or another tool to open or operate an authenticated tax portal;
never log in, enter or change values, click controls, sign, send, submit,
retrieve private account data, or ask for, accept, store, or process credentials
or sessions. Those actions remain human-only even with taxpayer permission or
available credentials. This boundary also applies on the informational fast
path before any shared runtime resource is loaded.

## Informational fast path — no intake state

Before reading or creating taxpayer/session files, decide whether the user is
asking only for information. If they do not explicitly ask to prepare,
organize, request, change, review, or stop a workpack:

1. Do not create or update `profile.yaml`, `session-progress.yaml`, workpacks,
   field maps, assumptions, or missing-info files.
2. Identify the supported year/topic and load only the directly relevant
   source resource. For a 2026 provisional procedure question, use these exact
   runtime paths instead of the raw reviewed portal-flow snapshots:
   - request:
     `../nl-tax-provisional-assessment/reference/source-projections/request-flow-human.md`
   - change:
     `../nl-tax-provisional-assessment/reference/source-projections/change-flow-human.md`
   - stopzetten:
     `../nl-tax-provisional-assessment/reference/source-projections/stopzetten-flow-human.md`
   For another topic, load only its directly relevant reviewed note under
   `../_shared/knowledge/`. Read the selected resource's `source_ids`, then
   search `../_shared/source-register.yaml` for only those matching entries;
   do not read the complete register. Never open the raw reviewed
   `request-flow.md`, `change-flow.md`, or `stopzetten-flow.md` in this fast
   path; their registered `snapshot_path` values are maintainer provenance.
3. Answer from the reviewed note and matched entries, not model memory. Keep
   annual and provisional rules distinct and state any manual-review or
   unsupported boundary in the note.
4. Answer directly. A short offer to prepare later is fine, but do not ask screening questions
   unless the user then explicitly requests preparation.

The remaining instructions apply only after explicit preparation intent.

## User-facing boundary

Keep setup invisible: do not narrate skill selection, resource loading, path
resolution, state-file writes, or policy loading. Say only that you can prepare
a local workpack and ask the questions currently needed. If the workflow and
documents are already clear, ask for the relevant tax files instead of asking
for workspace/state files. Never mention internal skill names or handoffs.

Python is optional. Do not ask the taxpayer to install Python; the agent owns
intake and applies the documented checks directly.

## Load for explicit preparation

Read `../_shared/runtime-contract.md` first on every turn. Then read:

1. `../_shared/knowledge/methods/interactive-elicitation.md` for the shared
   conversation, state, provenance, and generation contracts.
2. [`reference/intake-flow.md`](reference/intake-flow.md) for the complete
   screening, follow-up, terminal-routing, and closing contract.
3. `workspace/shared/session-progress.yaml` and
   `workspace/taxpayer/profile.yaml` when present; otherwise create them only
   as directed by `intake-flow.md` and the bundled templates.

Load [`reference/filing-paths.md`](reference/filing-paths.md) only when annual
versus provisional intent or the 2026 subflow is materially ambiguous. It is a
conversational intent guide, not a questionnaire or decision tree. Load
[`reference/unsupported-cases.md`](reference/unsupported-cases.md) when facts
indicate an unsupported or terminal-manual-review route.

Resolve bundled paths relative to this skill directory and every
`workspace/...` path against the saved `workspace_root`. Use progress to avoid
repetition, but choose the next question from the user's message, existing
facts/evidence, and the smallest material gap; the file does not dictate the order.
Never re-ask an answered question.

## Conversation and input controls

Prefer a **return-capable** native control only when its answer returns to this
same conversation. Do not use a display-only visual.

- **Claude chat or Cowork:** prefer native inputs. A custom HTML visual is not
  an answer form, and `AskUserQuestion` is not a guaranteed Cowork API.
- **Claude Code:** use `AskUserQuestion` when available.
- **Codex:** use a native control or inline form only when submit posts back to
  the same conversation.
- At a four-option limit, split the workflow choice exactly as described in
  `intake-flow.md`; otherwise use the short chat fallback.

Treat a returned selection like chat: record `source: user_chat`, its returned
wording as `quote`, and `stated_at`. Never record a selection before it returns.

After each reply, parse and credit every supplied fact before asking anything.
Preserve the three input paths: indexed file, sourced chat value, or deferred
unknown. Never silently use zero; use an assumption only after explicit user
acceptance.

Before the workflow-specific anchor, screen complex Box 2 facts involving a
share sale/valuation dispute, migration, restructuring, inheritance/gift,
non-arm's-length pricing, or borrowing from an own BV; unresolved complexity is
manual review. A standard `eenmanszaak` remains supported with
`business.has_onderneming`; complex business cases retain
`annual_2025_entrepreneurs` routing. Terminal routes set
`workflow_candidate: manual_review` or the specific blocked candidate and
`intake_status: complete` as detailed in `intake-flow.md`.

## Workspace location

Intake sets one immutable `workspace_root` and records it in both state files.
Never create a competing workspace tree. Do not volunteer the path unless the
user asks or a resume problem requires it.

This skill is the sole creator of `workspace/shared/session-progress.yaml`.
Downstream workflows update, but never create or reconstruct, intake-owned
state.

## State and provenance

Write incrementally after every user reply:

- `workspace/taxpayer/profile.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md` for deferred items
- `workspace/shared/assumptions.md` only for confirmed assumptions

Do not write `workspace/annual/**` or `workspace/provisional/**`.

Every recorded fact keeps provenance. A chat fact has `source: user_chat`, a
verbatim `quote`, and `stated_at`; a rule-derived fact has `source: calculated`
and `calculated_from`; an accepted default has `source: assumption`; an
unresolved fact has `source: unknown`, stays open, and appears in
`missing-info.md`.

### Household composition

Collect the taxpayer/partner DOBs and the child/single-parent facts required by
`intake-flow.md`. For every requested tax year, derive
`person.aow_by_tax_year.<year>.status` and the partner equivalent as
`below_all_year`, `reaches_during_year`, or `aow_all_year`; for a transition
record that year's `transition_month`. Keep 2025 and 2026 as separate entries
when both workflows are requested. Store each derivation with
`source: calculated` and `calculated_from`. Do not create an assumption or
request confirmation for undisputed date arithmetic.

## After intake is complete

Close only after the full completion and resume checks in `intake-flow.md` pass.
Tell the user the selected workflow, anything deferred, and the next tax topic
in ordinary language.

On a later continuation with complete intake and a recorded active annual or
provisional workflow, intake is no longer an active skill: do not reload this
body or its references. Let the recorded downstream workflow resume directly.

If the active request already asks for preparation, continue directly in
the same conversation with the next relevant evidence or tax question; do not
require a second activation phrase. If the user asked only to identify the
workflow or complete intake, stop after the summary.

When the user requested both supported workflows, start annual 2025 and keep
the selected provisional 2026 subflow queued under the shared runtime contract.
The original request authorizes the later annual-to-provisional collection
handoff; do not ask the user to activate provisional preparation again. Keep
the provisional final-generation confirmation separate from the annual one.

## Worked example

For a full-year resident individual requesting the 2025 return, credit those
facts, ask only the still-material partner, Box 2/business, evidence-anchor, and
household questions, then resume the annual conversation once the saved intake
contract is complete. See `reference/intake-flow.md` for exact recording and
terminal-routing behavior.
