# VAT mapping for 2025/2026

Read `../nl-tax-shared-resources/knowledge/vat/return-and-rubrics.md` and
`../nl-tax-shared-resources/knowledge/vat/invoices-and-deduction.md` for a VAT
return. Also read `../nl-tax-shared-resources/knowledge/vat/corrections.md` for
a correction. Tax rules, rates, rounding and correction thresholds are
canonical in those notes. This reference defines identifiers and checks.

Use field-map workflow `vat_return` or `vat_correction`, `tax_year` 2025/2026,
and explicit `period`, matching the owner's resume record and filename. A
month token always has two digits. Confirm scope from assigned filing facts,
not the file's name alone. Never map names, addresses, VAT numbers, BSN,
IBAN, account identifiers, credentials, payment references, or tax numbers.

## Rubric inventory

| Rubric | Meaning | Turnover ID | VAT ID |
|---|---|---|---|
| 1a | Domestic high rate | `vat.1a.turnover` | `vat.1a.vat` |
| 1b | Domestic low rate | `vat.1b.turnover` | `vat.1b.vat` |
| 1c | Other rates, when established | `vat.1c.turnover` | `vat.1c.vat` |
| 1d | Established private-use adjustment | `vat.1d.turnover` | `vat.1d.vat` |
| 1e | Domestic 0% or not taxed with the supplier (including domestic reverse charge); never export, EU supplies or exempt supplies | `vat.1e.turnover` | none |
| 2a | Domestic reverse charge received | `vat.2a.turnover` | `vat.2a.vat` |
| 3a | Outside-EU supplies, review boundary | `vat.3a.turnover` | none |
| 3b | EU supplies/services specified in the opgaaf ICP, review boundary | `vat.3b.turnover` | none |
| 3c | EU installation/distance sales, review boundary | `vat.3c.turnover` | none |
| 4a | Non-EU purchases/services, treatment established | `vat.4a.turnover` | `vat.4a.vat` |
| 4b | EU acquisitions/services, treatment established | `vat.4b.turnover` | `vat.4b.vat` |
| 5a | VAT due in rubrics 1–4 | none | `vat.5a.vat` |
| 5b | Eligible Dutch input VAT | none | `vat.5b.vat` |

Listed foreign/other/private-use rubrics are an inventory, not permission to
compute unsupported treatments. Follow the owner's boundary and keep an
unsettled applicable rubric as a gap. Zero-rate domestic supplies and exempt
supplies are different: never put exempt turnover in 1e merely because no VAT
was charged. Ordinary foreign supplier services need established location,
reverse-charge treatment, tax rate and deduction entitlement before mapping.

The resident online form computes 5a and the net outcome. Record `vat.5a.vat`
as `entry_mode: internal_routing` and label it as a verification amount in
the workpack, rather than a value to type. The public resident walkthrough does not
establish a universal numbered net-total box. Use `vat.total.balance` for
5a minus 5b as `entry_mode: internal_routing`, never a fabricated 5c/5g
manual-entry field. Display its value in the VAT workpack's reconciliation,
separately from the map's manual-entry summary.

## Completeness, rounding and provenance

Audit every rubric as `applicable_mapped`, `not_applicable_sourced`, or
`unresolved` in map notes, for example
`vat_rubric_coverage:1b=not_applicable_sourced; U:"no low-rate sales" (date)`
or `vat_rubric_coverage:1a=applicable_mapped; F:ev_001`. An unresolved rubric
has `vat_rubric_coverage:<rubric>=unresolved`. A sourced inapplicable liability
rubric contributes zero to arithmetic but is not a fabricated zero entry.
Missing or unsupported coverage remains unknown and blocks readiness.
An explicit scope statement can support inapplicable
rubrics; silence never establishes zero. Retain original cents in workpack
totals, then record the separately rounded whole-euro rubric values and the
rounding direction from the note. Do not round each invoice before summing.
Reconcile 5a to VAT in 1a+1b+1c+1d+2a+4a+4b, and the net to 5a minus 5b.
Credit-note signs and corrections must preserve the net/turnover distinction.

Each input VAT amount needs a valid source plus established eligible business
use. Reverse-charge VAT due and its deductible part are independent; never
claim the latter automatically or deduct foreign VAT. Calculated dependencies
must resolve to source-backed inputs or explicit workpack calculation lines.
No taxpayer-confirmed zero gets fabricated just to make the map reconcile.

## Corrections

Every `vat_correction` map declares the route that the correction owner chose
in exactly one Appendix B `notes` line: `vat_correction_route: suppletie`,
`vat_correction_route: next_return`, `vat_correction_route: letter`, or
`vat_correction_route: human_review`. Copy the route from the workpack's
correction route section; never infer it from the amounts. A map without this
line, with two route lines, or with another value fails the FM-VAT-PERIOD
check. Only the `suppletie` route may map `vat.correction.previous_balance`.

The correction owner keeps original filed totals, revised full rubric totals,
and the difference distinct. A suppletie map uses revised full totals,
including unchanged rubrics, rather than incremental differences.
For a suppletie, map `vat.correction.previous_balance` as a manual-entry row
labelled "Totaalbedrag eerdere btw-aangifte over dit tijdvak"
(bd_vat_suppletie_explanation), valued at the net VAT already declared for
that period. `vat.total.balance` (the form's Eindtotaal) and
`vat.correction.delta` (Totaal te betalen or terug te vragen) stay
`internal_routing` verification amounts. A small next-return route maps no
`vat.correction.previous_balance` row. The taxpayer or an authorized human confirms the actual form's
labels before entry; never invent a current screen identifier or
payment reference.

A small correction carried into a later return is an adjustment in the
original rubric, not a second filing of a corrected return. Keep the original
period and destination period explicit. The later return owner accepts it only
with fresh provenance and checks it has not already been carried. The
destination is the next (eerstvolgende) return after discovery. A whole-year
suppletie for a monthly or quarterly filer is not mapped; keep a route
blocker for human review. `Y` maps only an annual assigned filing period.
A letter-route item (margin globalisation, double-declared intra-Community
acquisition, or a rubric 3b letter) is never a map row.

## VAT checks in addition to FM checks

- `FM-VAT-PERIOD`: map year/period, owner identity, source period and filename
  agree; original and destination correction periods remain distinct; a
  `vat_correction` map carries exactly one valid `vat_correction_route:` note,
  and only the `suppletie` route maps `vat.correction.previous_balance`.
- `FM-VAT-RUBRICS`: only actual rubric columns are mapped; no VAT column in
  1e or 3a–3c, no IB fields, no invented total box; every rubric has coverage.
- `FM-VAT-RECONCILIATION`: complete source totals, whole-euro entry values,
  5a and net arithmetic, credit notes, and correction totals reconcile.
- `FM-VAT-DEDUCTION`: source and deduction entitlement are established
  independently, including reverse charge and any KOR/exemption status.
- `FM-VAT-REVIEW`: any `needs_review` note or owner scope blocker keeps
  `readiness: draft` with `VAT source-content review` or the exact case gap.
  Agent checks never attest human tax-content review. Do not offer a checklist
  with entry values while this blocker exists.
