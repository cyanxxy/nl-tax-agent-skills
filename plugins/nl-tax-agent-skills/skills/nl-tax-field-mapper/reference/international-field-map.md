# Migration and nonresident preparation map

This is a conceptual draft map, separate from the resident annual 2025 schema.
Read the owning international flow and its exact year-specific knowledge notes.
Map metadata uses `workflow: international_return`, `tax_year` 2025 or 2026 and
`return_form` migration|nonresident, matching Appendix A and the single file path
in `../nl-tax-shared-resources/reference/workflow-scopes.yaml`.

Use `international.<fact>` IDs (local aliases for groups/assets if repeated).
All rows have `entry_mode: internal_routing` and a conceptual label. These are
sourced facts for review, not fabricated M/C portal labels. Never include BSN,
VAT IDs, birth dates, genuine names/addresses, credentials or payment details.

Preserve exact residence periods, income country/source/category/period, asset
valuation dates, partner periods, worldwide income for qualification, proof
status, insurance periods and treaty-review findings as sourced dimensions or
notes. A residence/insurance date is an essential tax fact; it is not a birth
date. Do not use a 90% income ratio as a complete qualification test. Proof
requirements are year-specific. Preserve withheld tax separately from income.

Income-allocation, treaty exemption/credit, conserved income at emigration
(pension, lijfrente, eigen-woning capital insurance, substantial interest),
revisierente, the 30%-ruling partial-foreign-tax-liability choice, insurance,
deductions and partner allocation stay unresolved until exact treaty/year/form
sources and evidence permit them. Do not copy resident tax-credit entitlement
or resident worldwide Box 3 asset scope into a split/nonresident year;
year/form-specific rules decide credits, partner amounts and asset scope. The
2025 M and C explanations deduct the per-person heffingsvrij vermogen in full
in each Box 3 computation (the partner amount only under their partner
conditions). Apply time-based scaling only where the exact year/form source
states its method (for example a rekenhulp's full-month scaling); never apply
a generic day or month fraction.
For 2026 collect actuals separately from forecasts, pending year-end facts and
future annual schema. No final M/C opening date or screen fields are inferred.
All maps stay draft while source/form review is outstanding. Mapper alone owns
Appendix B; submit companion can show only blockers, not an entry checklist.
