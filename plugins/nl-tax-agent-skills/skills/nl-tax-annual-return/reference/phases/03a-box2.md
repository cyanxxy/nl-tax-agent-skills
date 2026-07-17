## Phase 3A — Box 2 compilation

Compile standard aanmerkelijk-belang data for the annual 2025 return when applicable. If the taxpayer has no Box 2 position, emit the canonical "not applicable" line from the output contract and continue.

When the taxpayer has an aanmerkelijk belang, read the rates from
`_shared/knowledge/years/2025/box2/box2-rates.md` — never paraphrase the 24.5% /
31% box 2 bracket from memory — and append `bd_box2_rates_2025_2026`,
`bd_box2_income_ab_guidance`, and `bd_fisin_aanmerkelijk_belang_2025` to
`session-progress.yaml` → `sources_loaded_by_workflow.annual_2025`, mirrored
in the active `sources_loaded` list.

### 3A.1 Substantial-interest status

- Confirm whether the taxpayer has an aanmerkelijk belang.
- Standard threshold: generally 5%, assessed together with the fiscal partner where applicable.
- Record `box2.has_aanmerkelijk_belang` as `true`/`false` in the profile (the template's boolean enum); route to manual review when the status is unclear.

### 3A.2 Regular benefits

- Collect gross regular benefits, normally dividends from the substantial-interest company.
- Collect directly related costs of regular benefits.
- Collect dividend withholding tax that can be credited.
- Map:
  - `box2.reguliere_voordelen_bruto`
  - `box2.kosten_reguliere_voordelen`
  - `box2.ingehouden_dividendbelasting`

### 3A.3 Disposal benefits

- Collect net transfer price, acquisition price, and any disposal costs needed to reconcile gross sale proceeds to the official net transfer price.
- Disposal benefit is the official net transfer price minus acquisition price, unless manual review is required. If evidence starts from gross sale proceeds, subtract disposal costs once to derive the net transfer price first.
- Map:
  - `box2.vervreemdingsprijs`
  - `box2.verkrijgingsprijs`
  - `box2.vervreemdingskosten`
  - `box2.vervreemdingsvoordeel`

### 3A.4 Other standard Box 2 fields

- Collect any fictitious regular benefit from excess borrowing from the BV as `box2.fictief_regulier_voordeel_bv_lening`.
- Collect any substantial-interest loss available for setoff as `box2.te_verrekenen_verlies_ab`.
- If fiscal partners were full-year partners, record `partner.verdeling_box2_inkomen` and verify that the combined allocation totals 100%.

### 3A.5 Manual-review triggers

- Require manual review for valuation disputes, informal capital, non-arm's-length transfers, restructurings, treaty/nonresident issues, emigration, death, and corporate-tax-heavy DGA cases.
- Do not calculate complex Box 2 positions when these triggers appear; record the facts and ask for professional review.

---
