## Change subflow

### Decision points

1. Does the taxpayer profile exist and contain `provisional_2026_change`?
2. Is there a baseline available?
   - From evidence index (beschikking indexed by the evidence-indexer skill)
   - From user input (user provides current voorlopige aanslag details)
   - If no baseline at all: ask user to provide the current monthly amount and key figures from their beschikking
3. Does the taxpayer have a fiscal partner? Has partner status changed?

### Data collection steps

1. **Baseline capture** — record the existing voorlopige aanslag details:
   - Monthly payment or refund amount
   - Income categories as submitted
   - Deductions as submitted
   - Box 3 data as submitted
2. **Full re-entry of all current estimates** (CRITICAL — not just changes):
   - All income categories (employment, pension/benefit, other, and the dedicated expected-profit forecast when applicable)
   - All deductions (own-home, alimentatie, premiums, other)
   - All standard Box 2 estimates (regular benefits, disposal benefits, costs, withholding tax, partner allocation)
   - All box 3 data (assets and debts as of 1 January 2026, fictitious method only)
   - On every turn until final confirmation, remind the user: "Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item."
3. **Delta calculation** — compare baseline to current estimates:
   - Per-category: income (up/down), deductions (up/down), box 3 (up/down), partner changes
   - Expected impact on monthly payment or refund

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` with change context
2. After the generation gate opens, invoke `nl-tax-field-mapper`; it alone writes and validates `workspace/provisional/2026/field-map.yaml` using `nl-tax-field-mapper/templates/field-map-template.yaml`, `nl-tax-field-mapper/reference/mapping-principles.md`, `nl-tax-field-mapper/reference/provisional-field-map.md`, and the optional `nl-tax-field-mapper/scripts/validate_field_map.py` check.
3. Generate `workspace/provisional/2026/delta-summary.md` — baseline vs forecast comparison
4. Update `workspace/shared/assumptions.md`
5. Include the full-re-entry reminder in the workpack

---
