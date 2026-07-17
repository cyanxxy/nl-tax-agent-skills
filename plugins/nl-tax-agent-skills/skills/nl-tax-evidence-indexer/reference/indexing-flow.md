# Evidence Indexing Flow

Use this procedure after the evidence-indexer skill is active. It coordinates
selected files, host attachments, and chat values; the owning annual or
provisional workflow remains responsible for tax treatment.

## 1. Resume and establish scope

1. Read the saved session state and existing evidence index before asking a
   question. Do not re-index unchanged entries or re-ask resolved questions.
2. Ask which visible folder or attachments the user wants included. `uploads/`
   and `evidence/` are convenient defaults, not prerequisites.
3. Limit the inventory to those selected locations. Accept chat-stated values
   even when no file is available.

## 2. Handle each input surface

### Folder files

Inventory files in each selected folder and compare them with existing index
entries. Add new items and update an existing item only when its current file
metadata or reviewed facts changed.

### Host attachments

When an attachment is not visible in `uploads/` or `evidence/`, look in the
working directory or host attachment location exposed for the task. Prefer a
byte-faithful copy into `uploads/` with the original filename when both source
and destination are available, using a host copy facility or an equivalent
copy operation. Never recreate a PDF, image, spreadsheet, or other binary by
round-tripping it through text Read and Write tools.

If a faithful copy is unavailable, index the attachment in place, record its
real path in `file_path`, and add `location: host_attachment` to its notes.
Do not ask the user to upload an attachment again merely because it is outside
`uploads/`.

### Chat values

Return a chat answer to the active workflow for storage with `source:
user_chat`, the user's verbatim `quote`, and `stated_at`. Also update
`sections.evidence.subsections.user_chat_values` and the evidence rollup in
`session-progress.yaml` as required by the shared elicitation contract.

Create an evidence-index chat row only when resume compatibility requires it
because the indexer was already active. In that row set:

- `source: user_chat`
- `file_path: null` and `file_sha256: null`
- `extraction_status: user_chat`
- `quote` and `stated_at`
- clearly named values under `extracted_fields`

## 3. Inventory, classify, and extract

1. Inventory selected files. The bundled script may supply file metadata and a
   SHA-256 hash only; an unavailable hash remains null and is nonblocking.
2. Review each new or changed file and assign the exact canonical token from
   `reference/evidence-types.md`, plus `tax_year`, `owner`, `confidence`, and
   `review_required`.
3. Apply `reference/extraction-boundaries.md` to every extracted fact. Preserve
   only allowed summary facts and leave tax meaning to the owning workflow.
4. Set `extraction_status` to reflect actual progress: `indexed_only`,
   `classified`, `extracted`, or `failed`.
5. Tell the user briefly what was found. Use one short sentence per relevant
   item and do not paste long document extracts.

## 4. Resolve uncertainty and conflicts

- When classification is ambiguous, keep the candidate type and reason in the
  review questions, set `review_required: true`, and ask for confirmation only
  when it matters to the active workflow.
- When file and chat values disagree, or two documents conflict, record both
  sources. Never overwrite one silently or infer which is final.
- If the user cannot provide a needed fact now, use `source: unknown`, set
  `extraction_status: deferred`, keep the question ID in `open_questions`, add
  it to `missing-info.md`, and move on. Do not add it to `answered` yet.

Ask no more than three closely related questions per turn.

## 5. Persist one coherent update

Update the evidence index, review questions, session progress, and any deferred
items together so a later turn can resume from disk. Keep totals and review
counts consistent with the item rows. Record whether the inventory was checked
by the bundled script or by the agent. Seed a missing review-questions file
from `templates/evidence-review-questions.md` before its first update.

Finish with a two-to-four-sentence report covering:

1. files added or updated;
2. chat values recorded; and
3. the next one or two evidence items that would unblock the active workflow.
