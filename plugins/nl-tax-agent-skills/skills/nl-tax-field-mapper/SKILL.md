---
name: nl-tax-field-mapper
description: Convert an annual or provisional workpack into a manual-entry field map for the Mijn Belastingdienst portal, tracing every value to its source. Use after a workpack exists and the user wants to prepare data entry.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Field Mapper

Convert workpack findings into a manual-entry field map that guides the taxpayer through data entry on the official Belastingdienst portal.

This skill is conversational. It does not silently emit a field map full of zeros. When a required field has no sourced value, surface a question to the user instead of inventing data.

## When to use

- After an annual workpack exists at `workspace/annual/2025/return-pack.md`.
- After a provisional workpack exists at `workspace/provisional/2026/provisional-pack.md`.
- When the user explicitly asks to prepare a field map for manual data entry.

If the relevant workpack does not exist, tell the user it must be generated first and offer to continue with the relevant workflow skill.

## Read first

Bundled paths below are relative to this skill's own directory: `reference/`
is a subfolder, and `_shared/` is the plugin-shared folder at `../_shared/`.
Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a
path is not obvious). Do not use Bash to discover or read plugin files: in
Cowork, shell commands run in an isolated VM that may not see the plugin cache
even when `Read` and `Glob` can. If the host has already expanded
`${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine
for file tools; otherwise search within the loaded plugin/skill tree and resolve
relative to this skill directory. Resolve every `workspace/...` path against
`workspace_root` recorded in `session-progress.yaml` (or `profile.yaml`); never
create a second `workspace/` tree.

1. `_shared/knowledge/methods/interactive-elicitation.md`
2. `workspace/shared/session-progress.yaml`
3. The workpack the user is asking about.
4. The relevant field reference: `reference/annual-field-map.md` or `reference/provisional-field-map.md`.
5. `reference/mapping-principles.md`.

The field-map rules are also summarized in **Fields to omit** and
**Safety** below.

## Workflow

1. Read the annual or provisional workpack.
2. Read the appropriate field reference as the canonical list of submission fields.
3. Map each workpack finding to a submission field.
4. Trace every value back to an `evidence_id`, user-chat `quote`, `assumption_id`, `baseline_ref`, `calculated_from`, or profile path.
5. Score each mapping 0.0 to 1.0 per `reference/mapping-principles.md`.
6. For any required data-entry field with no sourced value, add an open-question entry and tell the user before finalizing the field map. Omit portal-prefilled personal/identifier rows from both `fields` and `missing_fields`.
7. Flag fields requiring manual review.
8. List missing data-entry fields.
9. Write the field map and validate it.

## Annual vs Provisional

Annual and provisional field maps are never merged. Each gets its own file:

- Annual: backward-looking, evidence-based, includes werkelijk rendement option fields.
- Provisional: forward-looking, estimate-based, no werkelijk rendement field exists.

Do not combine, cross-reference, or merge them.

## Field Metadata

Each field includes:

| Attribute | Description |
| --- | --- |
| `field_id` | Unique id matching the field reference. |
| `label` | Dutch field label as shown on the portal. |
| `source.type` | One of `evidence`, `user_chat`, `estimate`, `baseline`, `calculated`, `assumption`, `unknown`. |
| `source.evidence_id` | Required when `source.type` is `evidence`. |
| `source.quote` | Required when `source.type` is `user_chat`. |
| `source.stated_at` | Recommended when `source.type` is `user_chat`. |
| `source.assumption_id` | Required when `source.type` is `assumption`. |
| `source.baseline_ref` | Recommended when `source.type` is `baseline`. |
| `source.calculated_from` | Recommended when `source.type` is `calculated`. |
| `source.profile_path` | Path in taxpayer profile when applicable. |
| `value` | The value to enter, or `null` if `source.type` is `unknown`. |
| `confidence` | 0.0 to 1.0 per mapping principles. |
| `manual_review_required` | True if the user must verify before entry. |
| `notes` | Notes, warnings, or context. |

A field with `source.type: unknown` must also be listed in `missing_fields` and in `workspace/shared/missing-info.md`. It is never silently set to zero.

Set `tax_year` explicitly before writing the map: `2025` for `annual_return` and
`2026` for `provisional_assessment`. Do not leave the template value blank,
`null`, or as a placeholder.

## Question Packet

When required fields have no sourced value, append to `workspace/shared/field-map-open-questions.yaml`:

```yaml
- question_id: "annual.field.box1.row01.gross_income"
  workflow: "annual_2025"
  field_id: "BOX1.ROW01.GROSS_INCOME"
  prompt_for_user: "I don't have a value for {field_label}. Do you want to provide it, or shall I leave it blank for manual entry?"
  acceptable_sources: ["file", "user_chat", "leave_blank"]
```

Tell the user about open questions before finalizing the field map. Offer two paths: provide the value now, or leave blank with a clear `MISSING - enter manually` marker on that row.

## Fields to omit

The tool never logs in, signs, or submits, and the portal pre-fills identity
rows — so these never become field-map entries (this is mapping scope, not a
security control; sensitive-data handling is the host's responsibility):

- Portal credentials: username, password, SMS codes.
- BSN, IBAN, or portal-prefilled personal identity rows such as name, address, or date of birth.
- Bank login credentials.
- Authentication tokens or session data.

## Validation

After writing the field map, validate it. If a Python interpreter is available in
this environment and Bash can access the resolved plugin script path, run the
bundled validator:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-field-mapper/scripts/validate_field_map.py <path-to-field-map.yaml>
```

The validator checks required metadata, workflow names, portal-automation (no-submission) fields, confidence range, source provenance rules, duplicate `field_id`s, non-finite values, required-reference coverage, readiness, unknown-field missing entries, and the provisional werkelijk rendement exclusion.

**If `python3` is not available or Bash cannot see the plugin script path** (for
example in Cowork's isolated VM), do not skip validation - verify the field map
by hand against `reference/mapping-principles.md` and the checks above: every
field has a valid `source.type` with its required sub-fields; no browser/submission
(portal-automation) fields; no duplicate `field_id`s and no non-finite (NaN/inf)
values; every required reference field other than portal-prefilled identifiers
appears in `fields` or `missing_fields`; every `unknown` field also appears in
`missing_fields`; and (for provisional) no werkelijk-rendement field exists. The
map is ready for entry only when at least one field is populated-and-sourced and
no required reference field is left unpopulated. Never copy bundled scripts into
`workspace/` to make them executable.

## Rendering

If `python3` is available and Bash can access the resolved plugin script path,
render a human-readable preview with the bundled renderer:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-field-mapper/scripts/render_field_map.py <path-to-field-map.yaml>
```

If `python3` is not available or Bash cannot see the plugin script path, present
the field map to the user directly from the YAML you wrote (field label, the
value or a `MISSING - enter manually` marker, and the source) instead of running
the script.

## Output Files

Write:

- `workspace/annual/2025/field-map.yaml` for annual workflows.
- `workspace/provisional/2026/field-map.yaml` for provisional workflows.
- `workspace/shared/field-map-open-questions.yaml` when gaps exist.
- `workspace/shared/missing-info.md` when unknown fields remain.

Never merge annual and provisional field maps.

If the workflow skill already wrote a `field-map.yaml`, read it before updating
the same workflow-specific file. Preserve valid sourced entries unless the
current workpack/reference makes them obsolete, then validate the result. The
most recently validated `field-map.yaml` at that workflow path is the
authoritative manual-entry artifact; do not create a competing `field-map-v2`,
copy, or alternate path.

## Write Restrictions

- Do not write anywhere inside the plugin's skill directories; only write under the `workspace/` tree.
- Do not write workpacks.
- Do not modify the evidence index or taxpayer profile.

## Safety

- This skill does not log in, submit, sign, or act as the user.
- Only run Python under an already-resolved plugin `skills/.../scripts/` path (for this skill, `scripts/validate_field_map.py` and `scripts/render_field_map.py`), and only if Bash can access that path. If Bash cannot see the plugin path, use the manual validation/rendering fallbacks above; never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## End-of-turn Report

After each turn, tell the user in 2 to 4 sentences:

1. How many fields were mapped from sourced values.
2. How many fields are unknown or low-confidence.
3. The next decision point: answer open questions, or finalize with `MISSING - enter manually` markers.
