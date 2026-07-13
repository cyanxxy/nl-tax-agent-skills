# Interactive Elicitation Contract

workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-02"
review_status: reviewed
# Internal methodology contract (no external source_id — this file is authored
# in-repo, like the other methods/ playbooks, and is exempt from the
# source-citation rule; see validate_knowledge_pack.py INTERNAL_KNOWLEDGE_PREFIXES).

All taxpayer-facing NL tax skills are **conversational**. The user does not pre-stage a folder of evidence and then run a skill once. They chat with the model, and the skill drives a turn-by-turn dialogue, asking only what is needed at each step and persisting state between turns.

This contract applies to:
- `nl-tax-intake`
- `nl-tax-evidence-indexer`
- `nl-tax-annual-return`
- `nl-tax-provisional-assessment`
- `nl-tax-partner-deductions`
- `nl-tax-box1-home`
- `nl-tax-box2`
- `nl-tax-box3`
- `nl-tax-field-mapper`

## Core principles

1. **Ask, don't assume.** When required information is missing, ask the user for it in chat. Never silently insert placeholder values into a workpack.
2. **Ask one focused thing at a time.** Group at most 2-3 closely related questions per turn. Do not dump a 20-question survey on the user.
3. **Resume, don't restart.** Before asking, read `workspace/shared/session-progress.yaml`. If a question has already been answered, do not re-ask it.
4. **Two paths for every input.** For every fact you need, accept either (a) a file uploaded to `uploads/` or `evidence/`, or (b) a value the user states directly in chat. Both are valid sources.
5. **Persist after every turn.** After each user reply, update the relevant workspace files (profile, evidence-index, session-progress) before continuing the conversation. The conversation must be resumable from disk alone.
6. **Confirm before producing the workpack.** Do not generate `return-pack.md` or `provisional-pack.md` until the user has given the workflow's explicit confirmation and all blocking questions are resolved.
7. **Surface gaps, don't hide them.** Items the user could not answer become entries in `workspace/shared/missing-info.md`, not silent zeros.

## Source of truth for each input

Every recorded value carries a `source` field with one of:

- `file` - extracted/derived from a file in `uploads/` or `evidence/`. Includes `evidence_id`.
- `user_chat` - the user stated this value in chat. Includes a short verbatim quote in `quote` and the date in `stated_at`.
- `calculated` - determined from sourced inputs plus a reviewed rule. Includes `calculated_from` and does not require separate user confirmation.
- `assumption` - a default the user explicitly accepted because the value was not fully determined. Must also be added to `workspace/shared/assumptions.md` with an `assumption_id`.
- `unknown` - the value is required but not yet provided. Must also appear in `workspace/shared/missing-info.md`.

A value with `source: assumption` or `source: unknown` MUST NOT be presented to the user in a workpack as if it were confirmed. A deterministic result from sourced inputs and a reviewed rule uses `source: calculated` plus `calculated_from`; it is not an assumption and needs no separate confirmation.

## Workspace root

Every `workspace/...` path produced by these skills is relative to one
working folder. That folder must stay identical across every turn and every
resumed session, or taxpayer state silently forks into a second tree.

- `nl-tax-intake` sets `workspace_root` on the first turn to the absolute path
  of the working folder, and writes it to both
  `workspace/shared/session-progress.yaml` and `workspace/taxpayer/profile.yaml`.
- Every skill, on every turn, reads `workspace_root` back and resolves all
  `workspace/...` paths against it.
- A non-intake skill requires both `profile.yaml` and `session-progress.yaml`.
  If either is missing, return control to `nl-tax-intake`; downstream skills do
  not create or reconstruct intake-owned state.
- Never change `workspace_root` once set, and never create a second
  `workspace/` directory.

## Session progress file

Path: `workspace/shared/session-progress.yaml`

Purpose: a small, append-friendly state file that any skill can read at the start of a turn to know where the conversation is.

Schema (v1.4 - see `_shared/templates/session-progress.yaml` for the canonical template):

- Each top-level section (`intake`, `evidence`, `annual_2025`, `provisional_2026`) has a status, an `open_questions` list, an `answered` list, and a `subsections` map.
- Subsection status values: `not_started | in_progress | complete | chat_only | deferred`.
- A workflow's workpack-generation gate is satisfied only when every subsection in that workflow is either `complete`, `chat_only`, or `deferred` (with deferred items recorded in `missing-info.md` or as confirmed assumptions). `chat_only` means the user deliberately provided the value in chat instead of uploading a file; it is not a gap.
- `complete` and `chat_only` express completeness, not reliability. Use
  `complete` when the required facts are fully sourced and at least one comes
  from indexed evidence; use `chat_only` when the required facts are fully
  supplied in chat. A mixture of file and chat sources may be `complete`, with
  every chat value still cross-indexed for review.
- `answered` contains only questions resolved by a sourced value or an explicitly
  confirmed assumption. A deferred question remains in `open_questions` and is
  never simultaneously in `answered`. When the user later answers it, remove it
  from `open_questions` and `missing-info.md` before marking the subsection
  `complete` or `chat_only`.
- Whenever a user-chat value is recorded anywhere, also set
  `sections.evidence.subsections.user_chat_values.status: chat_only`, append the
  stable question ID to that subsection's `answered` list, and set
  `sections.evidence.status: chat_only` unless indexed-file processing is
  currently `in_progress`. This evidence section is descriptive and is not a
  workpack-generation gate.
- Keep each workflow section's top-level `answered` and `open_questions` lists
  as de-duplicated rollups of its subsections. Update the subsection and rollup
  in the same write so resume logic never sees a question as both open and
  answered.
- The `provisional_2026` section also carries a `subflow` field (`request | change | review | stopzetten`); the `baseline` subsection applies only to change/review/stopzetten, and `stopzetten_direction` applies only to stopzetten.
- `annual_2025.subsections.winst` and
  `provisional_2026.subsections.winst_forecast` are generation-gate members.
  When the profile establishes that no business applies, the owning workflow
  marks the relevant subsection `complete` and adds a stable answered entry
  containing `not applicable`; absence is never inferred from a blank field.

Legacy resume rule: when an owning workflow reads a pre-1.4 file, migrate older
session state in place by adding the missing `winst` and `winst_forecast`
subsections from the canonical template without changing existing answers or
statuses, then set `session_progress_version: "1.4"`. Only mark either new
subsection not applicable when profile facts or a user answer establish that.

Rules:
- Only `nl-tax-intake` creates `workspace/shared/session-progress.yaml`, from
  the canonical template on its first turn. Every downstream workflow requires
  that file and returns control to intake when it is absent.
- Update `updated_at`, `last_question_asked`, and the relevant section on every turn that asks a question or records an answer.
- A `question_id` is a short stable string (e.g., `intake.residency`, `annual.box1.employer_count`, `box3.peildatum.bank_balance`). Reuse the same id when re-asking a deferred question.
- Write `session-progress.yaml` in one operation with the file-write tool — the no-code default on hosts like Cowork. If you have shell access to the workspace folder and want extra safety against an interrupted write, you may instead write a temp file in the same dir and rename it over the target. The state file is re-derivable from `profile.yaml` and the answered lists, so a rare truncated write is recoverable. Assume a single active session per workspace; do not run two skills concurrently against one `workspace_root`.

## Question-asking pattern

When a skill discovers it needs a value, it follows this loop:

1. **Check progress.** Read `workspace/shared/session-progress.yaml` and the relevant workspace file. Has this `question_id` already been answered? If yes, use the stored value.
2. **Check evidence.** Is this value already derivable from a file in `evidence-index.yaml`? If yes, use it and record `source: file`.
3. **Ask the user.** Pose the question in plain language. Offer at most two clarifying examples. Tell the user they may answer in chat OR upload a file.
4. **Record the answer.** Write the value to its proper home (profile, evidence-index, or workpack draft) with `source: user_chat`, `quote`, `stated_at`. Append the `question_id` to `answered` in session-progress.
5. **Handle "I don't know".** If the user cannot answer:
   - If a sensible default exists, propose it and confirm before applying. On confirm, record `source: assumption`.
   - If no default is acceptable, record `source: unknown`, keep the question ID
     in `open_questions` (not `answered`), set the subsection `deferred`, and add
     it to `missing-info.md`. Continue with the next question.
6. **Never block the whole flow on one missing answer.** Defer it and move on.

## Batching rules

- Initial intake turn may ask up to 4 short screening questions (residency, taxpayer type, living status, workflow choice).
- After intake, default to one section per turn (e.g., "let's do employment income"), with at most 3 sub-questions in that turn.
- If the user pastes a long block of facts, parse out everything you can in one go and only re-ask for items still missing.

## Workpack generation gate

Before writing `return-pack.md` or `provisional-pack.md`:

1. Every applicable subsection of the active workflow in `session-progress.yaml` is either `complete`, `chat_only`, or `deferred`. The top-level workflow status reflects the rollup: `complete` only when every subsection is `complete` or `chat_only`; otherwise it is `in_progress`. Use `deferred` only at subsection/question level, never as the final active-workflow rollup.
2. Every deferred item is reflected in `missing-info.md` or recorded as a confirmed assumption in `assumptions.md`.
3. The user has typed one of the workflow skill's verbatim confirmation phrases (e.g. `generate the workpack`, `genereer de workpack`, `klaar voor workpack`) or run the skill's `confirm` command. A general affirmative ("looks good", "yes", "ok") is **not** confirmation — ask explicitly for the phrase. Do not infer consent. This confirmation gate is an instruction the model follows, not a hard lock; it is a UX guardrail against accidental generation, not a security control.
4. If unresolved blocking gaps remain, do not generate the workpack. If only nonblocking deferred items remain, generate only when the active workflow's output contract permits a draft/review-ready status banner and the user has given the required explicit confirmation phrase; apply that output contract's exact status wording.

## Readiness authority

`session-progress.yaml` is the single readiness authority. Derive the workpack
banner and field-map `readiness` from the same active-workflow rollup:

- `review_ready` only when every applicable subsection is `complete` or
  `chat_only`, no blocking open question remains, and no workflow-specific
  manual-review blocker forces a draft.
- `draft` whenever any applicable subsection is `deferred`, `in_progress`,
  `not_started`, or has an unknown/blocking item.

Optional validators may reject malformed maps or a false `review_ready`
declaration, but they must never promote `draft` to `review_ready`. After final
assembly, clear `active_skill` only for a `complete` workflow. Keep the owning
workflow active when a generated draft still has deferred items so a later chat
answer resumes naturally.

## Credential handling

The skill never needs portal login details. If the user offers them, say so
briefly in one sentence and continue with the tax workflow.
