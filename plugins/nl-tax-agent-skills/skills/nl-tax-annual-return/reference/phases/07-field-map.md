## Phase 7 — Field map preparation

### 7.1 Prepare the mapper's inputs

Make sure every value the field mapper will need is in its workpack section
with provenance: `F:ev_NNN` pointing to a `Documents and sources` row, a
Taxpayer profile summary key, a `U:` quote, an accepted A-ID, or an open Q-ID
for a gap. Do not compose the field map yourself.

After the workpack generation gate in Phase 10, `nl-tax-field-mapper` is the
only author of the field map. It produces the `Field map summary` table and the
canonical `yaml` block for Appendix B, using
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`, and
`nl-tax-field-mapper/reference/field-map-rules.yaml`. Until then both sections
read `not yet mapped`.

### 7.2 Separation from provisional

The annual field map must be entirely separate from any provisional field
map. Do not reference or reuse provisional-2026 field mappings or the
provisional workpack.

---
