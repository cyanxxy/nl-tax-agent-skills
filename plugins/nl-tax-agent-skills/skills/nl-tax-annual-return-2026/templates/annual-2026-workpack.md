# Dutch Annual Income Tax Workpack — 2026

> **STATUS: DRAFT — N deferred section(s) — not for filing.**
> Source/treatment review blockers: [none / named blockers].

> **Provenance:** `F:ev_NNN` document; `U:"quote" (YYYY-MM-DD)` chat;
> `A:ID` explicitly accepted assumption; `?` missing; `C:formula` from sourced
> rows. Missing never means zero. `profile.<key>` points to a sourced profile row.

[Remove fill notes and placeholders from filled output. Not-reached sections
hold `Not yet reviewed.` while collecting. Chat shows only filled sections
and no Appendix A/B YAML. Replace banner only after the output-contract gate.]

## How to use this file

This is the draft annual income-tax workpack for 2026. Keep it to
resume later. You (the taxpayer) or an authorized human review the figures and
perform all authenticated entry, signing and submission personally in Mijn
Belastingdienst.

## Scope

- Tax year: 2026 — Src: profile.tax_year
- Workflow: resident annual income-tax return — Src: profile.workflow
- Evidence coverage: [start/end; year open/ended; final documents pending] — Src: [F/U]
- Created: [timestamp]

## Unsupported-case checks

Residence/migration/nonresident/deceased; foreign income/treaties; AOW/social
insurance; special business valuations, cessation/reserves/partnerships; annual
schema and source review. Route M/C to international owner; retain blockers.

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `tax_year` | 2026 | [F/U] |
| `workflow` | annual_2026 | [F/U] |
| `resident_all_year` | [yes/no/unresolved] | [F/U/?] |
| `evidence_coverage` | [actual coverage dates and final/forecast] | [F/U/?] |
| `year_end_evidence` | [pending/complete] | [F/U/?] |

## Documents and sources

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [document/chat date] | [canonical type] | 2026 | taxpayer | [section] | [needed facts] | [extracted/needs review] |

## Sources used

[List exactly consulted source_ids matching Appendix A sources_loaded.]

## Household and income

Partner/AOW/children periods and income categories, withholding, actual coverage,
foreign items and missing final statements. Every amount has Src.

## Business profit and reconciliation

P&L, opening/closing balance, private capital movements, tax adjustments,
investments/disposals and deduction chain. Actual final profit differs from
provisional estimated profit. Unknown eligibility or valuation stays open.

## Own home and Box 2

Dates, valuation and acquisition/debt/interest evidence; dividends, disposals,
withholding, costs and partner allocation inputs with provenance.

## Box 3

Expat-ruling (30%-regeling) transitional partial foreign tax liability choice
for 2026: [not applicable / chosen / not chosen / unresolved review item].
1 January categories plus full-year actual income, value changes, capital
movements, debt interest and, for the actual-return comparison only, the 2026
property own-use addition. Reporting the actual return is optional. Separate
provisional forfaits from unresolved final annual percentages and incomplete
year-end values.

## Deductions, credits and reconciliation

Evidence and eligibility conditions, prior decisions, withholding/prepayments,
source review and annual-schema gaps. Do not invent a final tax liability.

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

- [ ] I confirmed resident annual 2026 scope and actual evidence coverage.
- [ ] I checked final annual statements and all year-end balances when available.
- [ ] I reconciled income, business capital/profit, own home, Box 2 and Box 3.
- [ ] Where actual return is compared, I included any 2026 own-use property benefit in that actual-return calculation only.
- [ ] I checked deductions, credits, withholding and prepayments against sources.
- [ ] Source-content and exact annual-schema review remain visible blockers.
- [ ] I will personally verify the current form, deadline and notice details.

## Not submission advice

This workpack is a preparation aid. You (the taxpayer) or an authorized human
must review the figures and perform all portal entry, signing and submission
yourself in Mijn Belastingdienst. The assistant must not access or
operate the portal.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.5.0"
workflow: annual_2026
tax_year: 2026
created_at: ""
updated_at: ""
save_consent: not_given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  annual_scope: {status: not_started, open: []}
  household: {status: not_started, open: []}
  income: {status: not_started, open: []}
  business: {status: not_started, open: []}
  home: {status: not_started, open: []}
  box2: {status: not_started, open: []}
  box3: {status: not_started, open: []}
  deductions_credits: {status: not_started, open: []}
  reconciliation: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

not yet mapped
