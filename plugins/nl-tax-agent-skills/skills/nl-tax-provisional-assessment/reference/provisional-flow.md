# Provisional Flow — Subflow Routing and Generation

This is the common routing and output contract for the 2026 provisional-assessment workflow. Load this index when the workflow starts, then load exactly one active subflow file. If routing changes, stop using the old subflow and load exactly one newly active subflow.

## Overview

This document is a conversational routing guide for the four provisional
assessment intents. The owning agent confirms the user's goal and facts, asks
the next useful questions, and keeps judgment and writing in the conversation;
the candidate labels below are resume aids, not an executable state machine or
tax-decision engine.

Across review/change output, state that a later **unsolicited** VA based on earlier data **may be issued**, but is **not guaranteed**. For a change, prepare and **verify** the **complete dataset**; all applicable categories are required, not only the changed item. **Moving abroad** routes to **residency review** and is **not a categorical stopzetten reason**.

For `provisional_2026_change` with valid intake state, load
`subflows/change.md` before the first downstream change reply. When intake
state was initially absent, the entry skill already gave the canonical notice;
load this flow and `change.md` immediately after intake records the change
candidate, without replaying completed setup. Lead each change-collection
reply with the substance of this notice before focused questions: "Prepare and
verify the complete dataset; the change form requires all applicable
categories, not only the changed item."

## Subflow routing

```
User enters provisional skill
  │
  ├── workflow_candidate = provisional_2026_request
  │     → Request subflow
  │
  ├── workflow_candidate = provisional_2026_change
  │     → Change subflow
  │
  ├── workflow_candidate = provisional_2026_review
  │     → Review subflow
  │
  └── workflow_candidate = provisional_2026_stopzetten
        → Stopzetten subflow
              │
              ├── User receives monthly refund (teruggaaf)
              │     → Stopzetten guidance
              │
              └── User pays monthly amount (betaling) + amount is wrong
                    → REDIRECT to Change subflow
```

---

## Direct subflow links

- [Request subflow](subflows/request.md) — only when no 2026 provisional assessment exists yet.
- [Change subflow](subflows/change.md) — rebuild and verify the complete current dataset against a baseline.
- [Review subflow](subflows/review.md) — compare a current assessment with present facts.
- [Stopzetten subflow](subflows/stopzetten.md) — apply refund/payment routing and the cutoff rule.

Do not load multiple subflow files for comparison. Route first and load exactly one active file. A stopzetten payment case that redirects to change must update the workflow state before loading `subflows/change.md`.

## Common rules across all subflows

- All amounts are estimates unless explicitly labeled as from-baseline
- Box 2 amounts must be labeled as estimates or from-baseline.
- Box 3 uses the provisional fictitious method only. Include only the explanatory note: "Werkelijk rendement is not part of provisional 2026."
- Candidate Box 3 debts require the official inclusion/exclusion screen;
  unresolved debts remain outside accepted totals under manual review.
- Own-home WOZ uses peildatum 1 January 2025; Box 3 uses peildatum
  1 January 2026.
- AOW review uses `below_all_year`, `reaches_during_year`, or `aow_all_year`.
  A transition-year case records the month, uses the published month-specific
  first-bracket rate, and relies on the live portal result for affected
  credits.
- Workpack impact wording describes possible future direction only. The live
  portal and resulting beschikking control actual payment/refund amounts and
  timing.
- Every workpack must include the "Not submission advice" footer
- Every workpack must list exactly the source IDs in
  `sources_loaded_by_workflow.provisional_2026`; do not copy the annual ledger
- Every workpack must include the assumptions section
- Output files go to `workspace/provisional/2026/` — never to `workspace/annual/`

The first time an applicable source is loaded, compare its registered
`last_checked` date with its `freshness_policy`. Warn once, without blocking,
when it is past cadence; name the stale `source_id`s and carry them into the
workpack review items. Do not stale-check an inactive subflow or topic.

Append each consulted provisional `source_id` once to
`sources_loaded_by_workflow.provisional_2026` and update the top-level active
`sources_loaded` mirror in the same state write. Never append an annual source
merely because the annual workflow ran earlier in this workspace. The same ID
may appear in both ledgers only when it was independently consulted for both.

## Helper and reviewer delegation

Use the active subflow to select only the relevant background helpers:
`nl-tax-box1-home`, `nl-tax-winst`, `nl-tax-box2`, `nl-tax-box3`, or
`nl-tax-partner-deductions`. Prefer a host Skill/Task invocation when available;
otherwise inline the helper's instructions. In either mode, the helper writes
nothing and returns structured facts and open questions. The owning provisional
workflow persists those results in its section notes, asks the user, and
re-runs the helper after newly sourced answers. Keep the handoff invisible.

After independent facts are collected, the owner may request a bounded
specialist review under `../_shared/runtime-contract.md`. The reviewer returns
conflicts, missing facts, and source checks without choosing estimates,
allocations, or readiness. The owner reconciles every finding and remains the
canonical-state writer and readiness authority; review inline when a specialist
agent is unavailable.

Historical `workspace/shared/*-notes.md`, `*-open-questions.yaml`, and helper
review files are resume-only inputs. Fold useful content into the
workflow-owned provisional notes; never update or create those legacy
artifacts in a new run.

## Conversation and persistence loop

After every user reply and before asking the next question:

1. Accept either an indexed file value or a chat value. Record chat values with
   `source: user_chat`, a short verbatim `quote`, and `stated_at`, and add the
   stable question ID to
   `sections.evidence.subsections.user_chat_values.answered` with that
   subsection set to `chat_only`.
2. Persist the value in the applicable
   `workspace/provisional/2026/notes/<section>.yaml`. Update the subsection and
   provisional rollups in the same `session-progress.yaml` write so an answer
   is never simultaneously open and answered.
3. If the user defers, keep the stable question ID in `open_questions`, set the
   applicable subsection to `deferred`, and add the unresolved fact to
   `workspace/shared/missing-info.md`; never insert zero.
4. Re-read the ledger on the next turn, skip facts already answered, and ask at
   most three closely related unresolved questions.
