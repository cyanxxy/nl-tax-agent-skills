# Dutch ICP Workpack — {year} {period}

> **STATUS: DRAFT — N deferred section(s) — not for filing.**
> Source/treatment review blockers: [named blockers / none].
> Customer aliases do not replace actual VAT IDs. The human verifies and
> supplies the genuine IDs separately from their administration.

> **Provenance:** F:ev_NNN document; U:short quote (YYYY-MM-DD) chat;
> A:ID explicitly accepted assumption; ? missing; C:formula from sourced rows.
> Missing never means zero; profile keys refer to sourced profile rows.

[Remove fill notes from established output. Unopened collection sections hold
Not yet reviewed. Chat shows only filled sections and no Appendix A/B YAML.]

## How to use this file

This is the ICP preparation workpack for one confirmed period. Keep it to
resume. You (the taxpayer) or an authorized human supply the actual customer
VAT IDs and perform authenticated entry, signing and submission personally
in Mijn Belastingdienst Zakelijk.

## Scope

- Tax year: [2025 / 2026] — Src: profile.icp.tax_year
- Assigned period and exact dates: [period; start/end] — Src: [F/U/?]
- Workflow: opgaaf ICP
- Created: [timestamp]

## Unsupported-case checks

Record establishment/legal form, filing frequencies, annual permit, goods
lookback, customer business status, KOR/exempt treatment, goods transport,
triangulation, own-goods movements, call-off stock, fiscal units and two-month
transitions as confirmed standard, sourced not applicable or open. Record
specialist conclusions with provenance; unresolved specials stay blocking.

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `icp.tax_year` | [2025/2026] | [F/U/?] |
| `icp.period` | [Q1..Q4/M01..M12/Y] | [F/U/?] |
| `icp.period_confirmed` | [yes/no] | [F/U/?] |
| `icp.established_in_nl` | [yes/no] | [F/U/?] |
| `business.legal_form` | [eenmanszaak/other] | [F/U/?] |
| `icp.goods_frequency` | [confirmed/not applicable/open] | [F/U/?] |
| `icp.services_frequency` | [confirmed/not applicable/open] | [F/U/?] |
| `icp.annual_permit` | [confirmed/not applicable/open] | [F/U/?] |
| `icp.already_filed` | [yes/no] | [F/U/?] |
| `icp.special_case_screening` | [ordinary/review/open] | [F/U/?] |

## Documents and sources

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [document name/chat date] | [canonical type] | [year] | taxpayer | [page/section] | [needed non-identifying facts] | [extracted/needs review] |

## Sources used

[Exactly consulted applicable source_ids, matching sources_loaded.]

## ICP period and customer checks

Sourced assignment, exact dates, goods current/prior-four-quarter totals,
frequency test, permit if annual, deadline and actual filing status.

| Customer alias | Country | Actual-ID check performed by human/date | Result and business status | Src | Blocker |
|----------------|---------|-----------------------------------------|----------------------------|-----|---------|
| [alias] | [country] | [confirmation/date or missing] | [verified/failed/unavailable/open] | [F/U/?] | [open Q-ID/none] |

Actual customer VAT IDs stay in the human's administration and are entered
separately. The workpack is an alias-based draft, not a complete filing dataset.

## ICP transaction notes

| Row alias/customer alias | Country | Goods/services/special | Date and period basis | Net amount | Rubric and treatment | Src |
|--------------------------|---------|------------------------|-----------------------|------------|----------------------|-----|
| [alias/customer] | [country] | [kind] | [invoice/supply date and assigned period] | [EUR] | [ICP 3a/reviewed special/open] | [F/U/C/?] |

Current credit notes are identified once and distinguished from earlier
declaration errors. Preserve exact cents and confirmed form precision.

## ICP correction notes

| Correction alias | Original filed period | Old/correct customer alias | Original amount | Already reported corrections | Target corrected amount | Remaining signed delta | Reason and rubric | Src |
|------------------|-----------------------|----------------------------|-----------------|------------------------------|-------------------------|------------------------|-------------------|-----|
| [alias] | [year/period] | [alias/alias] | [EUR] | [EUR] | [EUR] | [C:target-original-prior corrections] | [ICP 2a/reviewed special/open] | [F/U/C/?] |

Wrong-ID changes use paired reversal/restoration with human-retained genuine
IDs. Corrections reconcile to their original coverage and separate VAT
correction; no current turnover is duplicated.

## ICP reconciliation

| Stable fact ID/customer | Raw amount | Form amount | Derivation/precision | Src |
|-------------------------|------------|-------------|----------------------|-----|
| [icp.row.alias.goods_amount/services_amount/triangulation_amount] | [EUR] | [EUR/open] | [sourced components and confirmed method] | [C/F/U/?] |

Current goods + services + reviewed specials: [EUR/formula/Src].
Same-coverage btw-aangifte rubric 3b: [EUR/date coverage/Src].
Coverage bridge for different frequencies: [sourced period totals / n/a].
Difference: [EUR; an explained and recorded cents or entry-rounding
difference, or a difference tied to the new-means-of-transport
specialist-review item; otherwise open Q-ID].
Earlier-error deltas: [EUR by original period/formula/Src], excluded from
current rubric 3 total.

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

- [ ] I checked the assigned coverage/frequency and annual permit if applicable.
- [ ] I verified genuine customer IDs in my records; none are stored here.
- [ ] I checked goods/services timing and all current credits.
- [ ] I checked signed earlier-error corrections and prior corrections.
- [ ] I reconciled the current ICP rubric 3 total to btw-aangifte rubric 3b
  for identical coverage.
- [ ] I resolved source/form review and special-case blockers.
- [ ] I checked every user-stated value and accepted assumption.
- [ ] I will personally check the current form and supply actual customer IDs
  in Mijn Belastingdienst Zakelijk before entry/signing/submission.

## Not submission advice

This workpack is a preparation aid and omits genuine customer VAT IDs. You
(the taxpayer) or an authorized human must review the figures, supply those
IDs from your administration and perform every authenticated entry, signing
and submission yourself in Mijn Belastingdienst Zakelijk. The assistant must
not access or operate the portal.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.5.0"
workflow: icp_<year>_<period>
tax_year: null
period: ""
created_at: ""
updated_at: ""
save_consent: not_given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  icp_scope: {status: not_started, open: []}
  icp_transactions: {status: not_started, open: []}
  icp_corrections: {status: not_started, open: []}
  icp_reconciliation: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

not yet mapped
