## Phase 7 — Field map generation

### 7.1 Generate field map

Prepare source-traceable facts needed by the field mapper, but do not write
`workspace/annual/2025/field-map.yaml`. After the workpack generation gate,
`nl-tax-field-mapper` is the sole writer and uses
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`, and
`nl-tax-field-mapper/reference/field-map-rules.yaml`. Until then, keep the
prepared inputs in phase notes.

### 7.2 Separation from provisional

The annual field map must be entirely separate from any provisional field
maps. Do not reference or reuse provisional-2026 field mappings.

---
