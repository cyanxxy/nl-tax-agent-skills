# Annual Return Workpack Generation Flow

This is the common conversational contract and ordered index for the 2025
annual-return workflow. Follow all 14 phases for coverage, but choose questions
within the active phase from the facts and evidence already available. The phase
order is a review structure, not a fixed interview, state machine, or tax-decision
engine. If a phase cannot be completed because data is missing, record the gap
and continue. The owning workflow persists all state and artifacts; background
helpers return facts and questions only.

Every time a knowledge file or rate sheet is loaded, record its matching
`source_id` from `_shared/source-register.yaml` once in
`session-progress.yaml` → `sources_loaded_by_workflow.annual_2025` and mirror
that list in the top-level `sources_loaded`. Only the annual workflow-specific
IDs may appear in the annual workpack's Sources used section.

## Progressive loading

Load this common index when the annual workflow starts. Then load exactly one active phase file at a time, immediately before performing that phase. Each phase is linked directly here and from `SKILL.md`; do not follow a deeper reference chain.

1. [Phase 1 — Pre-flight checks](phases/01-preflight.md)
2. [Phase 1.5 — Filing status and late-filing exposure](phases/01-5-filing-status.md)
3. [Phase 2 — Income compilation](phases/02-income.md)
4. [Phase 2A — Winst uit onderneming](phases/02a-winst.md)
5. [Phase 3 — Own-home compilation](phases/03-own-home.md)
6. [Phase 3A — Box 2 compilation](phases/03a-box2.md)
7. [Phase 4 — Box 3 compilation](phases/04-box3.md)
8. [Phase 5 — Deductions compilation](phases/05-deductions.md)
9. [Phase 5.5 — Credits screening](phases/05-5-credits.md)
10. [Phase 6 — Partner handling](phases/06-partner.md)
11. [Phase 7 — Field map generation](phases/07-field-map.md)
12. [Phase 8 — Missing info compilation](phases/08-missing-info.md)
13. [Phase 9 — Review question generation](phases/09-review-questions.md)
14. [Phase 10 — Workpack assembly](phases/10-assembly.md)

These direct links are the phase-resource allowlist. Do not inventory the
plugin, scan sibling skills, or search inactive phases for possible question
IDs. If the current user reply completes Phase N, the same turn may load and
act in Phase N+1. Once the response asks an unresolved question from Phase
N+1, stop reading workflow resources; Phase N+2 cannot be loaded until a later
reply completes or defers the active Phase N+1 work.

## Common contract

- Apply `../_shared/runtime-contract.md` throughout. Keep resource loading,
  helper selection, validation implementation, and state-file maintenance
  invisible to the taxpayer.
- Keep annual and provisional notes and output paths separate.
- Never invent a missing amount or silently treat it as zero.
- Load phase-specific reviewed knowledge only when that phase needs it.
- Load the output contract and workpack template only after the generation gate opens in Phase 10.
- Preserve the phase order and all requirements in the linked phase files.

### Conversation and evidence loop

For every active phase:

1. Re-read `workspace/shared/session-progress.yaml`; skip `complete` and
   `chat_only` subsections. Keep deferred questions open and revisit them only
   when the user resumes them or during final missing-information review.
2. Check the profile, notes, and evidence index before asking anything. Ask at
   most three closely related questions. When every question comes from one
   artifact, such as a mortgage statement or jaaropgaaf, a single batch may
   contain up to six fields.
3. Accept a file or a chat answer. A file is indexed through
   `nl-tax-evidence-indexer` and cited by `evidence_id`; a chat value is recorded
   with `source: user_chat`, a verbatim `quote`, and `stated_at`, and is added to
   `sections.evidence.subsections.user_chat_values`.
4. If the user defers, record `source: unknown`, keep the stable question ID in
   `open_questions` rather than `answered`, set the subsection `deferred`, and
   add it to `workspace/shared/missing-info.md`. Continue with another useful
   topic rather than blocking the whole conversation.
5. Persist every value in
   `workspace/annual/2025/notes/<section>.yaml` with its provenance, then update
   the subsection and workflow rollups in the same session-state write.

`chat_only` is a complete input path, not a gap. List chat-sourced values in the
workpack's user-stated-values index and Human review checklist. Use an assumption
only after the user explicitly accepts it.

### Source loading

Each phase file identifies the reviewed knowledge it needs. Load only the active
phase's applicable files and append each actually consulted `source_id` to
`sources_loaded_by_workflow.annual_2025` once, updating the active
`sources_loaded` mirror in the same write. The evidence checklist is loaded only when the user chose
document-based collection. If a required file cannot be loaded, stop that phase
and tell the user; never reconstruct a rate from memory.

The first time a source is loaded in a session, compare its registered
`last_checked` date with its `freshness_policy`. Warn once, without blocking, if
an applicable source is stale; name the stale IDs and carry them into the Human
review checklist. Never stale-check an inapplicable branch.

### Helper and reviewer delegation

For the active phase, prefer a host Skill/Task invocation when available;
otherwise inline the helper's instructions. In either mode, a helper writes
nothing and returns structured facts and open questions. The owning workflow
persists those results, asks the user, and re-runs the helper after newly sourced
answers. Keep the delegation invisible and speak in one voice.

- Box 1 / own home: `nl-tax-box1-home`
- Winst uit onderneming: `nl-tax-winst` only when
  `business.has_onderneming.value` is true. It runs the income-category
  pre-screen, then the ordered chain from the saldo fiscale winstberekening
  through investeringsaftrek, ondernemersaftrek and MKB-winstvrijstelling to the
  belastbare winst uit onderneming, which feeds the box 1 total. It also returns
  the vermogensvergelijking self-check, the bijdrage Zvw and lijfrente handoffs,
  the loss path, and the per-form routing markers that stay manual review.
- Box 2: `nl-tax-box2` only when an aanmerkelijk belang exists.
- Box 3: `nl-tax-box3`, collecting both fictitious and actual-return data for
  the official comparison.
- Partner / deductions: `nl-tax-partner-deductions`.

After independent sections have been collected, the owning agent may request a
bounded specialist cross-check under the optional reviewer contract in
`../_shared/runtime-contract.md`. The reviewer returns conflicts, missing facts,
and source checks without selecting a Box 3 result, partner allocation, or
readiness. The owning agent reconciles every finding and remains the canonical-
state writer and readiness authority. Review inline when a specialist agent is
unavailable.

Historical `workspace/shared/*-notes.md`, `*-open-questions.yaml`, and helper
review files are resume-only inputs. Fold useful content into the workflow-owned
annual notes; never update or create those legacy artifacts in a new run.
