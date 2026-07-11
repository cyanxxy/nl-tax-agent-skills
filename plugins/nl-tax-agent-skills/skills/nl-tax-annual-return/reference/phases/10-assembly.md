## Phase 10 — Workpack assembly

### 10.1 Use the template

Read the template from `templates/annual-return-pack.md`. Fill in every section with the data compiled in phases 1.5-9.

### 10.2 Run the workpack self-check

Run every check in `reference/annual-output-contract.md` § "Workpack self-check": structural, content, cross-contamination, and safety. Report each result yes/no in the assembly turn. If any item is "no", do not write the workpack — fix the gap or ask the user, then re-run.

### 10.3 Write the workpack

Write the completed workpack to `workspace/annual/2025/return-pack.md`. Then
invoke `nl-tax-field-mapper`; it alone writes
`workspace/annual/2025/field-map.yaml` using
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`, and
`nl-tax-field-mapper/scripts/validate_field_map.py`. Both artifacts remain
behind the generation gate in `SKILL.md`.

### 10.4 Summary to user

After writing:
- Confirm the workpack location
- Report the count of missing information items
- Report the count of assumptions made
- Remind the user to review the human review checklist
- Remind the user that filing happens through Mijn Belastingdienst
