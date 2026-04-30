---
name: nl-tax-field-mapper
description: Convert Dutch annual return or voorlopige aanslag workpack findings into a manual-entry field map.
argument-hint: "[annual|provisional] [year]"
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_SKILL_DIR}/../nl-tax-field-mapper/scripts/*.py *)
---

# NL Tax Field Mapper

Convert workpack findings into manual-entry field maps that guide the taxpayer through data entry on the official Belastingdienst portal.

## When to use

- After an annual return workpack has been generated at `workspace/annual/2025/return-pack.md`
- After a provisional assessment workpack has been generated at `workspace/provisional/2026/provisional-pack.md`
- When the user asks to prepare a field map for manual data entry

## What this skill does

1. **Read the workpack** — annual `workspace/annual/2025/return-pack.md` or provisional `workspace/provisional/2026/provisional-pack.md`
2. **Read the appropriate field reference** — `reference/annual-field-map.md` for annual, `reference/provisional-field-map.md` for provisional
3. **Read mapping principles** — `reference/mapping-principles.md` for confidence scoring, source tracking, and missing-field rules
4. **Map each workpack finding to a submission field** — using the field reference as the canonical list of fields
5. **Assign source** — trace every value back to an `evidence_id` or `assumption_id`
6. **Assign confidence** — score each mapping 0.0 to 1.0 per the mapping principles
7. **Flag fields requiring manual review** — any field with low confidence, missing evidence, or known ambiguity
8. **List missing fields** — fields needed for the return/assessment that have no data available
9. **Write the field-map.yaml** — using the template at `templates/field-map-template.yaml`

## Annual vs provisional separation

Annual and provisional field maps are NEVER merged. They are separate files serving separate workflows:

- **Annual field map:** backward-looking, evidence-based, covers all boxes including werkelijk rendement option
- **Provisional field map:** forward-looking, estimate-based, fewer fields, NO werkelijk rendement

If both workflows have been prepared, each gets its own field-map.yaml in its own directory. Do not combine, cross-reference, or merge them.

## Field metadata

Each field in the map includes:

| Attribute                | Description                                                  |
|--------------------------|--------------------------------------------------------------|
| `field_id`               | Unique identifier matching the field reference               |
| `label`                  | Dutch field label as it appears on the portal                |
| `source.type`            | One of: `evidence`, `estimate`, `baseline`, `calculated`     |
| `source.evidence_id`     | Reference to evidence-index.yaml entry (if applicable)       |
| `source.profile_path`    | Path in taxpayer profile (if applicable)                     |
| `value`                  | The value to enter                                           |
| `confidence`             | 0.0 to 1.0 per mapping principles                           |
| `manual_review_required` | Boolean — true if human must verify before entry             |
| `notes`                  | List of notes, warnings, or context for this field           |

## Credential exclusion

The following are NEVER mapped:

- DigiD credentials (username, password, SMS codes)
- BSN for manual entry (note it is needed, but do not store the value)
- Bank login credentials
- Any authentication tokens or session data

## Validation

After generating a field map, run the validation script:

```
python ${CLAUDE_SKILL_DIR}/../nl-tax-field-mapper/scripts/validate_field_map.py <path-to-field-map.yaml>
```

The validation checks:
- All required fields for the workflow are present or listed as missing
- No workflow mismatch (annual field in provisional map or vice versa)
- No credential or login fields
- All confidence values in range 0.0 to 1.0
- All source types are valid
- For provisional: no werkelijk rendement field exists

## Rendering

To generate a human-readable review table:

```
python ${CLAUDE_SKILL_DIR}/../nl-tax-field-mapper/scripts/render_field_map.py <path-to-field-map.yaml>
```

## Safety

Read and follow:
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/digid.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/security/prompt-injection.md`

Do not share DigiD credentials. This skill does not log in, submit, sign, or act as you. Use official authorization routes, such as DigiD Machtigen, when someone else is helping you.

## Output files

Write:
- `workspace/annual/2025/field-map.yaml` (for annual return workflow)
- `workspace/provisional/2026/field-map.yaml` (for provisional assessment workflow)

NEVER merge these files. NEVER write an annual field map to the provisional directory or vice versa.

## Write restrictions

- Do NOT write to `${CLAUDE_SKILL_DIR}/../**` — do not modify skill definitions or knowledge files
- Do NOT write workpacks — those are generated by the annual-return or provisional-assessment skills
- Do NOT modify the evidence index or taxpayer profile
