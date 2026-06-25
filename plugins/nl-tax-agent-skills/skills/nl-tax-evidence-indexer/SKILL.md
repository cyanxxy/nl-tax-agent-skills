---
name: nl-tax-evidence-indexer
description: Catalog and hash Dutch tax documents (`jaaropgaaf`, `bankafschrift`, `woz_beschikking`, `hypotheek_jaaroverzicht`, `voorlopige_aanslag_beschikking`) and chat-stated amounts into an evidence index. Use when the user shares or mentions tax documents, or a workflow needs evidence for a section.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-evidence-indexer/scripts/*.py:*)
---

# NL Tax Evidence Indexer

Catalog whatever evidence the user has - files in `uploads/`/`evidence/`, **and values stated in chat** - into a single structured index. This skill is conversational: it does not assume the user has dropped a complete folder of documents.

## When to use

- The user mentions having (or being about to share) tax documents.
- A workflow skill (annual / provisional) needs evidence for a section.
- New files appear in `uploads/` or `evidence/`.
- The user wants to record a value in chat ("my 2025 employer paid me EUR 52,400") that should be tracked alongside files.

## Read first (every turn)

Bundled paths below are relative to this skill's own directory: `reference/`
and `templates/` are subfolders, and `_shared/` is the plugin-shared folder at
`../_shared/`. Resolve bundled files with host file tools (`Read` first, `Glob`
or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin
files: in Cowork, shell commands run in an isolated VM that may not see the
plugin cache even when `Read` and `Glob` can. If the host has already expanded
`${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine
for file tools; otherwise search within the loaded plugin/skill tree and resolve
relative to this skill directory. Resolve every `workspace/...` path against
`workspace_root` recorded in `session-progress.yaml` (or `profile.yaml`); never
create a second `workspace/` tree.

1. `_shared/knowledge/methods/interactive-elicitation.md` - the conversational contract.
2. `reference/evidence-types.md`, `reference/extraction-boundaries.md`
3. `workspace/shared/session-progress.yaml` - to see which evidence questions are open.
4. `workspace/taxpayer/evidence-index.yaml` if it exists. Otherwise prepare to create it from `templates/evidence-index.yaml`.

Items 2-3 are internal rules. Do not quote or summarize them to the user unless
the user offers credentials, asks for login/submission help, or a specific
uploaded item needs review.

## How files arrive (folder drop AND host attachments)

`uploads/` and `evidence/` are the canonical evidence locations, but the user
does not have to put files there by hand. Accept all of these:

- **Folder drop** - files the user placed in `uploads/` or `evidence/` directly.
- **Host attachment** - files attached in the chat UI (Cowork, Claude Code,
  Codex). Hosts place these somewhere in the session working directory - often
  the workspace root or a host-specific attachments path, not `uploads/`.
- **Stated in chat** - no file at all; record as a `user_chat` item.

When the user mentions attaching or sharing a file and it is not in `uploads/`
or `evidence/`, look for it in the working directory (and any host attachment
path visible to you). When found, copy it into `uploads/` with its original
filename before indexing, tell the user you did so, and index the `uploads/`
copy. Never ask the user to re-upload a file that is already in the session;
never treat "it's not in uploads/" as "the user has no evidence".

## What this skill does

- **Scan** `uploads/` and `evidence/` for new files; classify each one.
- **Hash** each file (sha256) for integrity tracking.
- **Record user-stated values** as evidence items with `extraction_status: "user_chat"` (no file).
- **Drive the conversation** when a workflow needs evidence that is not yet present.
- **Generate** review questions for items the user must verify.

## Conversational behavior

The indexer never tries to do everything in one shot. Its turn-by-turn loop is:

1. **Inventory pass.** List what is currently in `uploads/` and `evidence/`, plus any host-attached files elsewhere in the session (copy those into `uploads/` first - see **How files arrive**). Diff against existing entries in `evidence-index.yaml`. Add or update items as needed.
2. **Tell the user what was found.** One short sentence per file: "Found `jaaropgaaf-2025.pdf` - looks like a 2025 jaaropgaaf from {employer}, confidence 0.85." Do not paste long extracts.
3. **Ask only about gaps that are blocking the active workflow.** If the active workflow is `annual_2025` and there is no jaaropgaaf and no employment income recorded, ask: "Do you have a 2025 jaaropgaaf? You can attach it here in the chat, drop it into `uploads/`, or just tell me the amount."
4. **Accept whichever the user offers** - file or chat - and record it accordingly.
5. **Defer politely.** If the user can't provide it now, mark `extraction_status: "deferred"`, add to `missing-info.md`, and move on.

Batch at most three evidence questions per turn.

## Two paths for every fact

Each item in `evidence-index.yaml` carries a `source` field:

- `file` - a real file in `uploads/` or `evidence/`.
- `user_chat` - a value the user stated. Includes `quote` (verbatim user text) and `stated_at`.
- `deferred` - promised but not yet provided.

For `user_chat` items, set `file_path: null`, `file_sha256: null`, `extraction_status: "user_chat"`, and put the stated amounts under `extracted_fields` with a clear key (e.g., `gross_employment_income_eur`).

## Evidence classification

For each file or user-stated item, determine:
- `evidence_type` (`jaaropgaaf`, `bankafschrift`, `woz_beschikking`, `hypotheek_jaaroverzicht`, `voorlopige_aanslag_beschikking`, `definitieve_aanslag`, etc.)
- `tax_year`
- `owner` (taxpayer or partner)
- `confidence` (0.0-1.0)
- `review_required` (true if confidence < 0.8 or content is ambiguous)

For `user_chat` items, `confidence` reflects how clearly the user stated the value, not OCR confidence.

## Extraction boundaries

The indexer MAY extract:
- Document type, tax year, employer/institution name, summary amounts.
- For chat-sourced items: only what the user explicitly stated.

The indexer MUST NOT:
- Decide tax treatment (deductible vs not).
- Compute tax amounts.
- Override user-provided values with file-derived ones without surfacing the conflict.
- Extract or store the BSN or similar identity numbers — workpack preparation does
  not need them; record document type, year, institution, and amounts instead.

If a file value and a user-stated value disagree, do NOT silently pick one. Add a `review_required: true` note and ask the user which to use.

## Safety

- This skill does not log in, submit, or sign anything.
- Only run Python under an already-resolved plugin `skills/.../scripts/` path (for this skill, `scripts/index_evidence.py`), and only if Bash can access that path. If Bash cannot see the plugin path, keep indexing manually from the file inventory: `uploads/` and `evidence/` live in the working folder, so you may compute `file_sha256` with a host hash command (e.g. `shasum -a 256 <file>` or `sha256sum <file>`); if no hash tool is reachable, set `file_sha256: null` (the schema permits a null hash) and continue — cataloging and classification do not depend on the hash. Never copy bundled scripts into `workspace/`, and never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.
- Do not add generic safety-warning paragraphs to normal user-facing replies.

## Output files

Write or update:
- `workspace/taxpayer/evidence-index.yaml`
- `workspace/shared/evidence-review-questions.md`
- `workspace/shared/session-progress.yaml` (record answered/open evidence question_ids)
- `workspace/shared/missing-info.md` (when items are deferred)

Do NOT write to:
- `workspace/annual/**`
- `workspace/provisional/**`

## End-of-turn report

After each turn, report to the user in 2-4 sentences:
- How many files indexed (added / updated).
- How many user-stated values recorded.
- The one or two next pieces of evidence that would unblock the active workflow.
