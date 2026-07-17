---
name: nl-tax-evidence-indexer
description: Use when the user explicitly wants Dutch tax documents or chat amounts organized into a source-traceable evidence index.
argument-hint: "[path-to-upload-folder]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Bash(python3:*)
---

# NL Tax Evidence Indexer

Organize the evidence the user actually supplies—selected files, host
attachments, and values stated in chat—without requiring a complete document
folder. Keep the interaction conversational and ask only for evidence that
matters to the active annual or provisional workflow.

## Activation

Use this skill when the user asks to index or organize Dutch tax evidence, when
an active workflow needs evidence for a section, or when selected files or chat
amounts need source-traceable recording. Credit everything already supplied;
do not restart intake or turn the exchange into a fixed upload checklist.

## Read before acting

Resolve bundled paths relative to this skill directory and every `workspace/...`
path against the saved `workspace_root`.

1. Read `../_shared/runtime-contract.md` first.
2. Read `../_shared/knowledge/methods/interactive-elicitation.md` for the shared
   conversational and session-state contract.
3. Read [reference/indexing-flow.md](reference/indexing-flow.md) whenever this
   skill is active; it owns the attachment, indexing, provenance, and update
   procedure.
4. Read [reference/evidence-types.md](reference/evidence-types.md) before
   assigning a canonical `evidence_type`, such as `woz_beschikking`,
   `hypotheek_jaaroverzicht`, or `voorlopige_aanslag_beschikking`.
5. Read [reference/extraction-boundaries.md](reference/extraction-boundaries.md)
   before classifying or extracting document facts.
6. Read `workspace/shared/session-progress.yaml` and the existing
   `workspace/taxpayer/evidence-index.yaml`. If the index does not exist, seed
   it from `templates/evidence-index.yaml`.

Keep resource loading, file maintenance, and orchestration invisible to the
user unless a specific evidence item needs review.

## Core contract

- Accept a user-selected folder, selected host attachments, values stated in
  chat, or any combination of these. Never require a file when the active
  workflow permits a chat value.
- Inventory only the locations the user selected. The optional Python helper
  catalogs file metadata and hashes; it does not classify documents, extract
  tax facts, or choose tax treatment.
- Assign evidence types and confidence conversationally from the document and
  the reviewed references. Do not use a deterministic tax-classification or
  decision engine, compute tax, decide deductibility, or choose a partner
  allocation.
- Preserve provenance. A file stays `source: file`; a value stated in chat uses
  `source: user_chat`, its verbatim `quote`, and `stated_at`; a deferred fact
  uses `source: unknown` and remains open.
- Return chat answers to the active workflow for its profile or section notes.
  An evidence-index chat row is only a resume-compatible record when the
  indexer was already active. Do not invoke this indexer solely to turn chat
  into document evidence; pure chat collection does not require an
  `evidence-index.yaml` entry.
- Never silently choose between conflicting file and chat values or between
  competing documents. Mark the item for review, describe the conflict, and
  ask the user which value or document should control.
- Ask at most three closely related evidence questions in one turn. Defer an
  unavailable item to `missing-info.md` and continue with another useful item.

## Optional catalog helper

Run `scripts/index_evidence.py` only from its resolved bundled location and only
when Python can already access that location and the selected files. The helper
is optional: never ask the user to install Python, and never copy or execute a
script from `workspace/`, `uploads/`, or `evidence/`.

The helper may populate inventory metadata and `file_sha256`. A null hash does
not block classification, extraction, or downstream preparation. Record
`check_performed_by: checked_by_script` when it ran successfully; otherwise use
`checked_by_agent` after completing the inventory with available file tools.

## Output ownership

Write or update only:

- `workspace/taxpayer/evidence-index.yaml`
- `workspace/shared/evidence-review-questions.md`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md` when an item is deferred

Do not write to `workspace/annual/**` or `workspace/provisional/**`. The active
annual or provisional workflow owns tax treatment and its section artifacts.

## User-facing close

In two to four sentences, report files added or updated, chat values recorded,
and the next one or two evidence items that would unblock the active workflow.
Do not add generic warnings.

Authenticated-portal boundary: Never use a browser, Claude in Chrome, computer
use, screen interaction, a connector, or another tool to open or operate an
authenticated tax portal; never log in, enter or change values, click controls,
sign, send, submit, retrieve private account data, or ask for, accept, store, or
process credentials or sessions. Those actions remain human-only even with
taxpayer permission or available credentials.
