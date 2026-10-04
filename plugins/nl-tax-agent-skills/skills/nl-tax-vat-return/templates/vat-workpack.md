# Dutch VAT Return Workpack — {year} {period}

> **STATUS: DRAFT — N deferred section(s) — not for filing.**
> Source/treatment review blockers: [none / named blockers].

> **Provenance:** `F:ev_NNN` document; `U:"quote" (YYYY-MM-DD)` chat;
> `A:ID` explicitly accepted assumption; `?` missing; `C:formula` from sourced
> rows. Missing never means zero. `profile.<key>` points to a sourced profile row.

[Remove fill notes and placeholders from filled output. Not-reached sections
hold `Not yet reviewed.` while collecting. Chat shows only filled sections
and no Appendix A/B YAML. Replace banner only after the output-contract gate.]

## How to use this file

This is the VAT preparation workpack for one confirmed period. Keep it to
resume later. You (the taxpayer) or an authorized human review the figures and
perform all authenticated entry, signing and submission personally in Mijn
Belastingdienst Zakelijk.

## Scope

- Tax year: [2025 / 2026] — Src: profile.vat.tax_year
- Assigned period: [Q1..Q4 / M01..M12 / Y] — Src: profile.vat.period
- Period dates: [start / end] — Src: [F/U]
- Workflow: VAT return (btw-aangifte)
- Created: [timestamp]

## Unsupported-case checks

Record each screen as confirmed standard, sourced not applicable, or open:
legal form and Netherlands establishment; VAT obligation; KOR effective dates; cash or
invoice system; foreign services/sales and ICP follow-up; mixed exemption or
pro-rata; margin schemes; OSS/IOSS; property; car/private-use adjustments.
Supported bounded adjustments use sourced formulas and confirmed treatment.
Unresolved classification/elections remain blocking. ICP/OSS have separate
owners/files and matching reconciliation. Adviser-supplied figures are
recorded with provenance rather than recomputed.

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `vat.established_in_nl` | [yes/no] | [F/U/?] |
| `business.legal_form` | [eenmanszaak/other] | [F/U/?] |
| `vat.tax_year` | [2025/2026] | [F/U/?] |
| `vat.period` | [assigned period] | [F/U/?] |
| `vat.period_confirmed` | [yes/no] | [F/U/?] |
| `vat.return_obligation` | [confirmed/unresolved] | [F/U/?] |
| `vat.already_filed` | [yes/no] | [F/U/?] |
| `vat.accounting_system` | [invoice/cash/unresolved] | [F/U/?] |
| `vat.kor_status_and_dates` | [confirmed participation and dates/not participating/unresolved] | [F/U/?] |
| `vat.special_case_screening` | [standard/manual review/unresolved] | [F/U/?] |

## Documents and sources

Read evidence where shared; record only needed facts and short quotes. No
identifiers, payment references or file hashes. Never renumber ev-IDs.

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [user document name or chat date] | [canonical type] | [year] | taxpayer | [page/section] | [needed facts] | [extracted/needs review] |

## Sources used

[List exactly consulted source_ids matching Appendix A sources_loaded.]

## VAT period and filing status

Assigned period/dates, obligation and KOR status, already-filed screen,
applicable accounting timing, sourced filing/payment deadline, and human
follow-up if status is late/unresolved. Do not infer a frequency or deadline.

## Sales and VAT transaction notes

| Group | Date/period basis | Rubric | Turnover excluding VAT | Output or assessed VAT | Treatment | Src |
|-------|-------------------|--------|------------------------|------------------------|-----------|-----|
| [sales/credit note/reverse charge group] | [basis] | [rubric] | [EUR] | [EUR] | [confirmed/open] | [F/U/C/?] |
| [carried correction from <year> <original period>] | [next return after discovery] | [original rubric] | [signed EUR] | [signed EUR] | [confirmed/open] | [F/U/C/?] |

Keep foreign-service country/treatment and any ICP follow-up visible.

## Input VAT notes

| Group | Correct period | Invoice/other proof | Business use and entitlement | VAT amount | Deductible VAT | Src |
|-------|----------------|--------------------|------------------------------|------------|----------------|-----|
| [purchase group] | [period] | [ev_ID] | [confirmed/open] | [EUR] | [EUR] | [F/U/C/?] |
| [carried 5b correction from <year> <original period>] | [next return after discovery] | [ev_ID] | [confirmed/open] | [signed EUR] | [signed EUR] | [F/U/C/?] |

Record exclusions, accepted helper adjustment formulas and confirmed adviser
figures with provenance, timing, source IDs and duplicate/cap checks.

## VAT rubric reconciliation

| Rubric / stable fact ID | Raw turnover | Raw VAT | Whole-euro entry | Derivation and rounding | Src |
|-------------------------|--------------|---------|------------------|-------------------------|-----|
| [vat.<rubric>.turnover / vat.<rubric>.vat] | [EUR/n/a] | [EUR/n/a] | [EUR] | [components + sourced policy] | [C/F/U/?] |

Output/reverse-charge total: [EUR + formula + Src].
Deductible input VAT total: [EUR + formula + Src].
Signed payable/refundable balance: [EUR + formula + Src].
Bookkeeping/VAT-control difference: [EUR + explanation + Src / unresolved].
Every applicable rubric is populated, sourced zero/not applicable, or open.

## Open questions

| ID | Section | Question | Blocking | Status |
|----|---------|----------|----------|--------|
| Q001 | [section key] | [question] | [yes/no] | [open/answered] |

## Missing information

| ID | Missing item | Linked Q-ID | Why needed |
|----|--------------|-------------|------------|
| M001 | [item] | Q001 | [reason] |

## Assumptions

| ID | Assumption | User acceptance and date | Affected facts |
|----|------------|--------------------------|----------------|
| A001 | [assumption] | [quote/date] | [facts] |

## User-stated values index

| Fact | Value | Verbatim short quote | Stated at |
|------|-------|----------------------|-----------|
| [fact] | [value] | [quote] | [YYYY-MM-DD] |

## Field map summary

not yet mapped

## Manual-entry checklist

not requested

## Human review checklist

- [ ] I confirmed the assigned year/period, VAT status and KOR effective dates.
- [ ] I checked invoice/cash timing, all sales, credit notes and purchase groups.
- [ ] I checked deduction entitlement and each foreign/reverse-charge treatment.
- [ ] I checked all rubric totals, official rounding and the reconciliation.
- [ ] I resolved source-content review, special-case and missing-fact blockers;
  any unresolved item keeps this workpack draft.
- [ ] I checked all user-stated values and accepted assumptions.
- [ ] I will personally check the current form and filing/payment instructions
  in Mijn Belastingdienst Zakelijk and use its genuine payment reference.

## Not submission advice

This workpack is a preparation aid. You (the taxpayer) or an authorized human
must review the figures and perform all portal entry, signing and submission
yourself in Mijn Belastingdienst Zakelijk. The assistant must not access or
operate the portal.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.5.0"
workflow: vat_<year>_<period>
tax_year: null
period: ""
created_at: ""
updated_at: ""
save_consent: not_given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  vat_scope: {status: not_started, open: []}
  vat_transactions: {status: not_started, open: []}
  vat_input_tax: {status: not_started, open: []}
  vat_reconciliation: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

not yet mapped
