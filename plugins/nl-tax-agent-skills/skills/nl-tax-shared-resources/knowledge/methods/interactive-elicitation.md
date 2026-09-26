# Interactive Elicitation Contract

workflow: all
tax_year: all
status: active
last_reviewed: "2026-09-26"
review_status: reviewed
# Internal methodology contract (no external source_id — this file is authored
# in-repo, like the other methods/ playbooks, and is exempt from the
# source-citation rule; see validate_knowledge_pack.py INTERNAL_KNOWLEDGE_PREFIXES).

All taxpayer-facing NL tax skills are **conversational**. The user does not
pre-stage a folder of evidence and then run a skill once. They talk with the
model, share documents or state values when asked, and the owning workflow
drives a turn-by-turn dialogue that asks only what is needed next. The
conversation is the working record. One workpack file per workflow is written
only when the user asks to keep it; file rules live in
`../nl-tax-shared-resources/runtime-contract.md` under "User files and outputs".

Section statuses and the resume record describe what has been established and
what remains open. They are a record, not a state machine: they do not
prescribe a fixed interview order, choose a tax treatment, or replace the
agent's judgment about the clearest next question.

This contract applies to:
- `nl-tax-intake`
- `nl-tax-annual-return`
- `nl-tax-provisional-assessment`
- `nl-tax-box1-home`
- `nl-tax-box2`
- `nl-tax-box3`
- `nl-tax-partner-deductions`
- `nl-tax-winst`
- `nl-tax-field-mapper`
- `nl-tax-submit-companion`

Background helpers return their questions to the owning workflow, which asks
them in the main conversation.

## Core principles

1. **Ask, don't assume.** When required information is missing, ask the user
   for it. Never silently insert a placeholder value into a workpack.
2. **Ask one focused thing at a time.** Group at most 2-3 closely related
   questions per turn. Do not dump a 20-question survey on the user.
3. **Don't re-ask what is established.** Before asking, check the conversation,
   the documents already read, and any attached or confirmed saved workpack. If
   a fact is already established there with provenance, use it.
4. **Two paths for every input.** Accept either (a) a document the user shares
   in the conversation or has in the selected working folder, or (b) a value
   the user states in chat. Both are valid sources. Never require a document
   when the active workflow permits a chat value.
5. **Nothing is written by default.** Collection, questions, recaps, the
   workpack, the field map, and the checklist happen in the conversation. The
   owning workflow offers to save only at the natural points the runtime
   contract names, each at most once; after "don't ask again" it stops
   offering. Consent is session-scoped: a skill writes only while save consent
   is active in this conversation, never because a file records
   `save_consent: given`. After consent it keeps the one workpack file current
   at the end of every turn that changes a sourced fact, an open question, a
   section status, the field map, or the checklist. Showing the workpack never
   writes: without consent it appears as Markdown in the reply, with only
   filled sections and no Appendix A or B YAML.
6. **One yes/no question per reply.** Never put two yes/no offers, or a
   question plus an offer, in the same reply, so a bare "yes" is unambiguous.
   The workflow-start save offer is its own reply, before the first collection
   question; a return-capable structured control with clearly separate choices
   may combine them.
7. **Keep exact figures safe from compaction.** After each completed section,
   show a compact "Confirmed so far" recap for that section: each value with its
   provenance code, citing a document by name with its ev ID (for example
   `F:ev_003 (jaaropgaaf ING 2025)`). If a previously established figure is no
   longer visible verbatim in the conversation or the saved workpack,
   re-confirm it with the user; never reconstruct an amount from memory or a
   summary.
8. **Confirm before generation.** Do not assemble the final workpack until final
   review, when the user has clearly authorized generation in natural language
   and all blocking questions are resolved. Never require a magic phrase.
9. **Surface gaps, don't hide them.** Items the user could not answer become
   entries in `## Open questions` and `## Missing information`, not silent
   zeros.
10. **Prefer return-capable controls.** For finite choices, use a native
    multiple-choice control or compact form when the active host can return its
    selections to this same conversation. If that capability is absent or
    uncertain, ask the same short questions in chat. A display-only visual is
    never a substitute for a reply.

## Provenance for every recorded value

Every recorded value carries a source type and the matching workpack
provenance code:

| Source type | Code | Record |
|---|---|---|
| `file` | `F:<evidence_id>` | Read from a document the user shared. Add one row to `## Documents and sources` with the next unused `ev_NNN` ID (`ev_001`, `ev_002`, …; never renumber), the document as the user named it, type, tax year, owner, location (page/section), values taken, and status (`extracted` / `needs review`). |
| `user_chat` | `U:"<short quote>" (<YYYY-MM-DD>)` | Stated by the user in chat or returned by a structured-input control. Keep the short verbatim `quote` and `stated_at` date, add a `Documents and sources` row of type `user_chat` when the value is used, named `chat YYYY-MM-DD`, and list it in `## User-stated values index`. |
| `calculated` | `C:<formula>` | Determined from sourced inputs plus a reviewed rule. Record `calculated_from`; it needs no separate user confirmation. |
| `assumption` | `A:<assumption_id>` | A default the user explicitly accepted because the value was not fully determined. Record it in `## Assumptions` with an A-ID. |
| `unknown` | `?` | Required but not yet provided. Record it in `## Missing information` with an M-ID; keep any question still owed to the user in `## Open questions` with its Q-ID. |

Provisional workpacks also use `B:<baseline_ref>` for a value carried over from
the existing voorlopige-aanslag baseline, as the provisional output contract
defines.

Read documents directly inside the owning workflow. Classify each one with
`../nl-tax-shared-resources/reference/evidence-types.md` and take values only
within `../nl-tax-shared-resources/reference/extraction-boundaries.md`. Keep a
row short: no file hashes and no copied content beyond the short quote that
provenance needs.

A value with source `assumption` or `unknown` MUST NOT be presented as if it
were confirmed. A rule-derived value from sourced inputs and a reviewed rule
uses `calculated` plus `calculated_from`; it is not an assumption and needs no
separate confirmation.

IDs are stable. Give each open question a Q-ID, each missing item an M-ID, each
accepted assumption an A-ID, and each document or chat source row an `ev_NNN`
ID; never renumber them, and reuse the same Q-ID when re-asking a deferred
question.

## Section status and the resume record

The owning workflow tracks one status per applicable section, in the
conversation and, when the workpack is saved, in `## Appendix A — Resume
record` as one fenced `yaml` block:

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.4.0"
workflow: annual_2025            # or provisional_2026_request|change|review|stopzetten
tax_year: 2025                   # 2026 for provisional
created_at: ""                   # ISO 8601
updated_at: ""
save_consent: not_given         # not_given in the template; given in the written file (a record, never an authorization)
readiness: draft                 # draft | review_ready (derived; see Readiness authority)
generation_confirmed: false      # true after the final-review confirmation
queued_workflow: null            # e.g. provisional_2026_change when the user asked for both
sections:
  filing_status: {status: not_started, open: []}
  # annual keys: filing_status, box1, winst, eigen_woning, box2, box3_peildatum,
  #   box3_actual, deductions, credits_screening, partner_allocation, confirm
  # provisional keys: baseline, income_employment, income_pension_benefit,
  #   income_other, winst_forecast, deductions, box2, box3_peildatum,
  #   partner_allocation, stopzetten_direction, confirm
sources_loaded: []               # reviewed source_ids consulted for THIS workflow only
```

- Status values: `not_started | in_progress | complete | chat_only | deferred`.
- `complete` and `chat_only` express completeness, not reliability. Use
  `complete` when the section's required facts are fully sourced and at least
  one comes from a document; use `chat_only` when they are fully supplied in
  chat. `chat_only` is a deliberate choice, not a gap. A mix of document and
  chat sources may be `complete`.
- `deferred` means a question in that section is still open: its Q-ID stays in
  `open` and in `## Open questions`, and the gap is in `## Missing information`
  or covered by an accepted assumption. When the user later answers, remove the
  Q-ID and M-ID before marking the section `complete` or `chat_only`.
- `open` lists that section's open Q-IDs. Facts never live in the resume
  record; they live in the readable sections with provenance.
- Provisional `baseline` applies only to change, review, and stopzetten;
  `stopzetten_direction` applies only to stopzetten.
- Annual `winst` and provisional `winst_forecast` are generation-gate members.
  When the taxpayer profile establishes that no business applies, mark the
  section `complete` and record `not applicable` with its provenance in that
  section; never infer absence from a blank.
- The owning workflow updates `updated_at` whenever it writes the file.

## Question-asking pattern

When a skill needs a value, use this judgment-led pattern. The numbered items
are provenance and continuity checks, not a prescribed interview sequence; skip
or reorder them when the conversation has already supplied the fact:

1. **Check what is established.** Is the fact already in the conversation, a
   document already read, or the attached workpack? If yes, use it.
2. **Check documents.** Can a document the user shared answer it? If yes, read
   it, add or update its `Documents and sources` row, and record `F:`.
3. **Ask the user.** For finite choices, capability-check and prefer a
   return-capable structured-input control. Otherwise ask in plain language
   with at most two clarifying examples. When a document can answer the
   question, say the user may share it or state the value in chat.
4. **Record the answer** in its section with provenance and update the section
   status. If the workpack is saved, update the file at the end of the turn.
5. **Handle "I don't know".** If the user cannot answer:
   - If a sensible default exists, propose it and confirm before applying. On
     confirmation, record it as an assumption with an A-ID.
   - If no default is acceptable, record `?`, add an M-ID under
     `Missing information`, keep the Q-ID open, set the section `deferred`,
     and continue with the next question.
6. **Never block the whole flow on one missing answer.** Defer it and move on.
7. **Never resolve a conflict silently.** When a document and a chat value
   disagree, or two documents conflict, keep both sources, mark the row
   `needs review`, describe the conflict, and ask which value controls.

## Batching rules

- Initial intake may present its four short screening questions (residency,
  taxpayer type, living status, workflow choice) in one compact return-capable
  form. If the host's native question control allows at most four options per
  question, ask annual-versus-2026 first and ask the four 2026 subflows only
  after the user chooses 2026. If no return-capable control is available, use
  the ordinary short chat batch.
- After intake, default to one section per turn (for example "let's do
  employment income"), with at most 3 sub-questions in that turn.
- If the user pastes a long block of facts or shares several documents at once,
  take everything you can in one go and ask only for what is still missing.

## Workpack generation gate

Before assembling the final workpack, whether it is delivered in the
conversation or written to the saved file:

1. Every applicable section of the active workflow is `complete`, `chat_only`,
   or `deferred`. The workflow rollup is `complete` only when every section is
   `complete` or `chat_only`; otherwise it is `in_progress`. Use `deferred`
   only at section or question level, never as the workflow rollup.
2. Every deferred item is in `## Open questions` and `## Missing information`,
   or is covered by an accepted assumption in `## Assumptions`.
3. At final review, summarize what the workpack will contain and ask a scoped
   question such as "Shall I prepare the final workpack and field map now?"
   Clear authorization is any of: a direct generation request made after that
   review; an unambiguous affirmative reply to the immediately preceding scoped
   question (for example "yes", "go ahead", "looks good", or a natural Dutch
   equivalent); or the optional skill `confirm` command. Do not require exact
   wording. Do not reuse an opening preparation request or an unrelated
   affirmative answer as final generation consent. If context is ambiguous, ask
   one short clarification. Record the confirmation in the `confirm` section
   and set `generation_confirmed: true`. Keep the generation question the only
   question in that reply. If the user has not opted in to saving, the save
   offer comes after generation and mapping, in its own reply; a checklist
   offer comes in the reply after that.
4. If unresolved blocking gaps remain, do not generate the workpack. If only
   nonblocking deferred items remain, generate only when the active workflow's
   output contract permits a draft/review-ready status banner and the user has
   given the clear contextual confirmation above; apply that output contract's
   exact status wording.
5. If a sourced fact changes after generation, `generation_confirmed` returns
   to `false`, and the field map summary, Appendix B, and any manual-entry
   checklist are marked with the line `STALE — predates the change to <fact>
   (<YYYY-MM-DD>); regenerate before use.` A stale map or checklist is never a
   source for a value. Regenerate only after fresh contextual confirmation;
   the field mapper then rebuilds the map from the recorded facts, because an
   unsaved or stale map is not state.

## Readiness authority

The owning workflow is the single readiness authority. It tracks section status
in the conversation and, when the workpack is saved, in Appendix A. The STATUS
banner, the resume record's `readiness`, and the field-map `readiness` all
derive from the same rollup:

- `review_ready` only when every applicable section is `complete` or
  `chat_only`, no blocking open question remains, and no workflow-specific
  manual-review blocker forces a draft.
- `draft` whenever any applicable section is `deferred`, `in_progress`,
  `not_started`, or has an unknown or blocking item.

Validators may reject malformed maps or a false `review_ready` declaration, but
they never promote `draft` to `review_ready`. When a generated draft still has
deferred items, the owning workflow stays active so a later answer resumes
naturally.

## Credential handling

The skill never needs portal login details. If the user offers them, say so
briefly in one sentence and continue with the tax workflow.
