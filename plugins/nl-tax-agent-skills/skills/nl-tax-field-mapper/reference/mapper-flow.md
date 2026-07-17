# Mapper Flow

Use this procedure whenever a field-map run begins or resumes. `SKILL.md` owns
activation and hard boundaries; this file owns execution order. Do not copy
field rules into this procedure: use `mapping-principles.md` plus the relevant
annual or provisional field reference.

## 1. Load the mapping state

Read, in order:

1. `workspace/shared/session-progress.yaml`.
2. The relevant workpack:
   `workspace/annual/2025/return-pack.md` or
   `workspace/provisional/2026/provisional-pack.md`.
3. `reference/mapping-principles.md`.
4. The matching submission reference:
   `reference/annual-field-map.md` or
   `reference/provisional-field-map.md`.
5. The existing canonical workflow map, if present.
6. Existing `workspace/shared/field-map-open-questions.yaml` and
   `workspace/shared/missing-info.md`, if present.

Resolve every workspace path from the session's `workspace_root`. Treat the
field reference as the canonical submission-field list and the workpack as the
current set of reviewed facts. Never infer that a prior annual value is a
current provisional estimate.

## 2. Build or update the map

1. Select the annual or provisional workflow and set its explicit `tax_year`.
2. Map each supported workpack finding to the matching field-reference ID.
3. Preserve a valid, sourced existing entry unless the current workpack or
   reference supersedes it.
4. Attach one supported source record and score confidence from 0.0 to 1.0
   using `mapping-principles.md`.
5. Flag any value the taxpayer must verify with
   `manual_review_required: true` and explain why in `notes`.
6. Omit portal-prefilled identity/identifier rows and all credential or session
   data.
7. Create or refresh the open-question and missing-info records for every
   unresolved required data-entry field.
8. Derive top-level readiness from session progress, then write the one
   canonical workflow map.

Do not merge annual and provisional data, cross-reference one map as a source
for the other, or create an alternate output. Annual 2025 may map supplied
actual-return inputs; provisional 2026 must contain only estimates or explicit
baselines and the explanatory note that werkelijk rendement is not part of the
provisional workflow.

## 3. Field record contract

Each mapped field uses the template and these attributes:

| Attribute | Rule |
| --- | --- |
| `field_id` | Unique ID from the selected field reference. |
| `label` | Dutch portal label from that reference. |
| `source.type` | `evidence`, `user_chat`, `estimate`, `baseline`, `calculated`, `assumption`, or `unknown`. |
| `source.evidence_id` | Required for `evidence`. |
| `source.quote` | Required verbatim text for `user_chat`. |
| `source.stated_at` | Preserve the date for `user_chat`. |
| `source.assumption_id` | Required for `assumption`. |
| `source.baseline_ref` | Preserve for `baseline` when available. |
| `source.calculated_from` | Preserve for `calculated` when available. |
| `source.profile_path` | Profile path when applicable. |
| `value` | Manual-entry value, or `null` for `unknown`. |
| `confidence` | 0.0 to 1.0 under `mapping-principles.md`. |
| `manual_review_required` | `true` when taxpayer verification is required. |
| `notes` | Entry mode, warnings, and context. |

Apply the full provenance rules in `mapping-principles.md`. In particular,
`user_chat` is sourced data rather than a missing document: preserve its quote
and date in the field and add the matching entry to `user_chat_values_index`.
Never convert it to `unknown` merely because no file was uploaded.

## 4. Handle gaps conversationally

An unsourced required data-entry field gets all three of:

- `source.type: unknown` with `value: null` in `fields`;
- a matching `missing_fields` entry and `workspace/shared/missing-info.md` item;
- an open question in `workspace/shared/field-map-open-questions.yaml`.

Never use zero as a placeholder. A deferred optional field may be omitted from
`fields` until sourced, while its question and missing-info state remain. In
either case, preserve `readiness: draft` when session progress is incomplete.

Use a stable question record such as:

```yaml
- question_id: "annual.field.box1.row01.gross_income"
  workflow: "annual_2025"
  field_id: "BOX1.ROW01.GROSS_INCOME"
  prompt_for_user: "I don't have a value for {field_label}. Do you want to provide it, or shall I leave it blank for manual entry?"
  acceptable_sources: ["file", "user_chat", "leave_blank"]
```

Tell the user about open questions before finalizing. Offer two paths: provide a
sourced value now, or retain a clear `MISSING - enter manually` marker in the
manual-entry view. Reuse answers already present in session state, the workpack,
and the current conversation. Ask a small, coherent packet of the most useful
related questions for this case; do not replay intake or impose a fixed
questionnaire.

## 5. Derive readiness and write

Use the active workflow rollup in `session-progress.yaml` as authoritative:

- `review_ready` requires a complete active workflow with no blocking or
  manual-review blocker;
- every other state maps to `draft`.

Mechanical completeness does not change this declaration. Write only:

- `workspace/annual/2025/field-map.yaml` for `annual_return`; or
- `workspace/provisional/2026/field-map.yaml` for
  `provisional_assessment`.

If the canonical map exists, update it in place and revalidate the whole map.
Preserve still-valid source records and resolved questions. Remove a stale
entry only when the current workpack or selected field reference makes it
obsolete. Never write a versioned copy or second map.

## 6. Validate

The agent owns the mapping and readiness decision. After writing, use the
optional bundled validator when `python3` and its resolved path are available:

```bash
python3 <resolved-plugin-root>/skills/nl-tax-field-mapper/scripts/validate_field_map.py --require-ready <path-to-field-map.yaml>
```

Omit `--require-ready` for a draft. The validator checks metadata, workflow and
tax year, source provenance, confidence, duplicate IDs, finite values,
reference coverage, `unknown`/`missing_fields` alignment, the
`user_chat_values_index`, omitted portal-prefilled rows, provisional
werkelijk-rendement exclusion, and whether declared `review_ready` is
structurally possible. It may reject false readiness but never promotes a
draft.

After a successful script check, set
`check_performed_by: checked_by_script`. If the script cannot run, complete
every stable check ID in the manual checklist in `mapping-principles.md`, then
set `check_performed_by: checked_by_agent`. Those are the only accepted check
trails. The manual fallback is required; never skip validation or copy the
script into the workspace.

## 7. Render and report

When available, render the checked YAML with:

```bash
python3 <resolved-plugin-root>/skills/nl-tax-field-mapper/scripts/render_field_map.py <path-to-field-map.yaml>
```

Otherwise read the written YAML directly and present each field's Dutch label,
manual-entry value or `MISSING - enter manually` marker, and source. Rendering
is presentation only and cannot change the map.

End the turn in two to four sentences with:

1. the number of fields mapped from sourced values;
2. the number unknown or low-confidence; and
3. the next decision: answer open questions or finalize the missing markers.

After a canonical map is successfully created or updated, offer to create the
human-only manual-entry checklist. Do not create it solely because the map now
exists. A direct natural-language request, or an unambiguous affirmative reply
to that immediately preceding offer, authorizes the checklist without a slash
command or magic phrase.
