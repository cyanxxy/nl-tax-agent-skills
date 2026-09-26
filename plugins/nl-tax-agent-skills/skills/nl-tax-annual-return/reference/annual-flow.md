# Annual Return Workpack Generation Flow

This is the common conversational contract and ordered index for the 2025
annual-return workflow. Follow all 14 phases for coverage, but choose questions
within the active phase from the facts and documents already in the
conversation. The phase order is a review structure, not a fixed interview,
state machine, or tax-decision engine. If a phase cannot be completed because
data is missing, record the gap and continue. The owning workflow keeps the
facts, section status, and (only with consent) the saved workpack; background
helpers return facts and questions only.

Every time a knowledge file or rate sheet is loaded, add its matching
`source_id` from `../nl-tax-shared-resources/source-register.yaml` once to this
workflow's source list, which becomes `sources_loaded` in Appendix A and the
workpack's Sources used section. Only annual IDs belong in that list.

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
11. [Phase 7 — Field map preparation](phases/07-field-map.md)
12. [Phase 8 — Missing information](phases/08-missing-info.md)
13. [Phase 9 — Open questions and human review](phases/09-review-questions.md)
14. [Phase 10 — Workpack assembly](phases/10-assembly.md)

These direct links are the phase-resource allowlist. Do not inventory the
plugin, scan sibling skills, or search inactive phases for possible question
IDs. If the current user reply completes Phase N, the same turn may load and
act in Phase N+1. Once the response asks an unresolved question from Phase
N+1, stop reading workflow resources; Phase N+2 cannot be loaded until a later
reply completes or defers the active Phase N+1 work.

## Section status

Track one status per annual section, in the conversation and, when the
workpack is saved, in Appendix A. The keys are fixed:

| Section key | Phase |
|---|---|
| `filing_status` | 1.5 |
| `box1` | 2 |
| `winst` | 2A |
| `eigen_woning` | 3 |
| `box2` | 3A |
| `box3_peildatum` | 4 (assets and debts on 1 January 2025, fictitious return) |
| `box3_actual` | 4 (actual-return data and comparison) |
| `deductions` | 5 |
| `credits_screening` | 5.5 |
| `partner_allocation` | 6 |
| `confirm` | 10 |

Status values: `not_started | in_progress | complete | chat_only | deferred`.
`complete` means the facts are fully sourced with at least one document;
`chat_only` means they were fully supplied in chat. Both are complete input
paths, not reliability grades. A section with no applicable facts (no
onderneming, no own home, no aanmerkelijk belang, no fiscal partner) is
`complete` with its sourced "not applicable" answer; absence is never inferred
from silence. Each section's open Q-IDs sit beside its status.

## Common contract

- Apply `../nl-tax-shared-resources/runtime-contract.md` and
  `../nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md`
  throughout. Keep resource loading, helper selection, and validation
  implementation invisible to the taxpayer.
- Keep annual and provisional sources, facts, and outputs separate.
- Never invent a missing amount or silently treat it as zero.
- Load phase-specific reviewed knowledge only when that phase needs it.
- Load the workpack template only when the taxpayer consents to saving or the
  generation gate opens; load the output contract only after the generation
  gate opens in Phase 10.
- Preserve the phase order and all requirements in the linked phase files.
- Ask one yes/no question per reply. When the workflow starts, the save offer
  in `SKILL.md` is its own reply, before the first collection question (a
  return-capable structured control with clearly separate choices may combine
  them). Never pair an offer with another offer or a question.
- Write only while save consent is active in this conversation; the file's
  `save_consent` value is a record, never an authorization.

### Conversation and evidence loop

For every active phase:

1. Skip sections already `complete` or `chat_only`. Keep deferred questions
   open and revisit them only when the user resumes them or during the final
   missing-information review.
2. Check the conversation, the Taxpayer profile summary facts, and the
   documents already shared before asking anything. Ask at most three closely
   related questions. When every question comes from one document, such as a
   mortgage statement or jaaropgaaf, a single batch may contain up to six
   fields.
3. Accept a document or a chat answer. Read a shared document yourself, assign
   its canonical type from
   `../nl-tax-shared-resources/reference/evidence-types.md`, extract only what
   `../nl-tax-shared-resources/reference/extraction-boundaries.md` allows, and
   record it as the next `ev_NNN` row for `Documents and sources` (never
   renumber). Cite its values as `F:ev_NNN`. A chat value gets a row too
   (named `chat YYYY-MM-DD`, type `user_chat`) and is cited as
   `U:"<short quote>" (<date>)`. Never copy, move, rename, or rewrite the
   user's documents.
4. When a document and a chat value, or two documents, disagree, do not choose:
   mark the row `needs review`, describe the conflict, and ask which controls.
5. If the user defers, keep the question open under a stable Q-ID (reuse the
   same Q-ID when asking again), mark the value `?`, set the section
   `deferred`, and carry the gap to `Missing information`. Continue with
   another useful topic rather than blocking the whole conversation.
6. Record every value with its provenance and update the section status in the
   same turn. When the workpack is saved, update the file at the end of that
   turn.

When a section becomes `complete` or `chat_only`, end the reply with a compact
"Confirmed so far" recap for that section: each value with its provenance
code, citing a document by name with its ev ID (for example
`F:ev_003 (jaaropgaaf ING 2025)`). If a previously established figure is no longer visible verbatim in the
conversation or the saved workpack, re-confirm it with the user; never
reconstruct an amount from memory or a summary.

`chat_only` is a complete input path, not a gap. List chat-sourced values in the
workpack's User-stated values index and Human review checklist. Use an
assumption only after the user explicitly accepts it, and record it as an A-ID.

### Source loading

Each phase file identifies the reviewed knowledge it needs. Load only the active
phase's applicable files and add each actually consulted `source_id` to this
workflow's source list once. The evidence checklist is loaded only when the
user chose document-based collection. If a required file cannot be loaded, stop
that phase and tell the user; never reconstruct a rate from memory. If the list
is no longer visible after a long conversation, rebuild it only from the notes
actually consulted for this workpack's sections; never pad it.

The first time a source is loaded in a session, compare its registered
`last_checked` date with its `freshness_policy`. Warn once, without blocking, if
an applicable source is stale; name the stale IDs and carry them into the Human
review checklist. Never stale-check an inapplicable branch.

### Helper and reviewer delegation

For the active phase, prefer a host Skill/Task invocation when available;
otherwise inline the helper's instructions by reading its `SKILL.md` at the
path listed below (resolved from this skill directory). These helper paths are
part of this workflow's resource allowlist. In either mode, a helper writes
nothing and returns structured facts and open questions. The owning workflow
records those results, asks the user, and re-runs the helper after newly
sourced answers. Keep the delegation invisible and speak in one voice.

- Box 1 / own home: `nl-tax-box1-home` (`../nl-tax-box1-home/SKILL.md`)
- Winst uit onderneming: `nl-tax-winst` (`../nl-tax-winst/SKILL.md`) only when
  `business.has_onderneming` is true. It runs the income-category pre-screen,
  then the ordered chain from the saldo fiscale winstberekening through
  investeringsaftrek, ondernemersaftrek and MKB-winstvrijstelling to the
  belastbare winst uit onderneming, which feeds the box 1 total. It also returns
  the vermogensvergelijking self-check, the bijdrage Zvw and lijfrente handoffs,
  the loss path, and the per-form routing markers that stay manual review.
- Box 2: `nl-tax-box2` (`../nl-tax-box2/SKILL.md`) only when an aanmerkelijk belang exists.
- Box 3: `nl-tax-box3` (`../nl-tax-box3/SKILL.md`), collecting both fictitious and actual-return data for
  the official comparison.
- Partner / deductions: `nl-tax-partner-deductions`
  (`../nl-tax-partner-deductions/SKILL.md`).

After independent sections have been collected, the owning agent may request a
bounded specialist cross-check under the optional reviewer contract in
`../nl-tax-shared-resources/runtime-contract.md`. Give the reviewer the facts,
the section, and the source IDs (plus the workpack path when saved). The
reviewer never writes, and returns conflicts, missing facts, and source checks
without selecting a Box 3 result, partner allocation, or readiness. The owning
agent reconciles every finding and remains the only writer and readiness
authority. Review inline when a specialist agent is unavailable.

A 0.3 `return-pack.md`, notes file, or other older document the user shares is
an ordinary source document: record it as a `Documents and sources` row and
confirm material figures with the user. 0.3 `workspace/` ledgers are not read.
