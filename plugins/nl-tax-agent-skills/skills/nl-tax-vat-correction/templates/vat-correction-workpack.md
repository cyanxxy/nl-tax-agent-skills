# Dutch VAT Correction Workpack — {year} {period}

> **STATUS: DRAFT — N deferred section(s) — not for filing.**
> Source/treatment/reporting review blockers: [none / named blockers].

> **Provenance:** `F:ev_NNN` document; `U:"quote" (YYYY-MM-DD)` chat;
> `A:ID` accepted assumption; `?` missing; `C:formula` from sourced rows.
> Missing never means zero. A profile reference points to a sourced row.

[Remove fill notes and placeholders. Unreached collection sections hold
`Not yet reviewed.`; chat shows filled sections without Appendix A/B YAML.]

## How to use this file

This compares original and corrected VAT figures for one filed period.
Keep it to resume. You (the taxpayer) or an authorized human review the
figures and perform every authenticated action personally in Mijn
Belastingdienst Zakelijk.

## Scope

- Original tax year: [2025/2026] — Src: profile.vat.tax_year
- Original assigned period: [Q1..Q4/M01..M12/Y] — Src: profile.vat.period
- Original period dates: [start/end] — Src: [F/U]
- Workflow: VAT correction preparation (later return / suppletie)
- Created: [timestamp]

## Unsupported-case checks

Confirm Netherlands-established eenmanszaak/ZZP scope, actual original filing, KOR
status/dates and relevant transaction screens. Supported mixed-use, margin,
property/revision and car/private-use adjustments carry helper formulas and
accepted sourced treatment; unresolved classification/elections remain blocked.
ICP/OSS corrections use their separate owners, files and thresholds. Record
confirmed adviser figures with provenance, without recomputing their basis.

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `vat.established_in_nl` | [yes/no] | [F/U/?] |
| `business.legal_form` | [eenmanszaak/other] | [F/U/?] |
| `vat.tax_year` | [2025/2026] | [F/U/?] |
| `vat.period` | [original assigned period] | [F/U/?] |
| `vat.period_confirmed` | [yes/no] | [F/U/?] |
| `vat.already_filed` | [yes/no] | [F/U/?] |
| `vat.prior_corrections` | [confirmed details/none/unresolved] | [F/U/?] |
| `vat.kor_status_and_dates` | [confirmed participation and dates/not participating/unresolved] | [F/U/?] |
| `vat.special_case_screening` | [standard/manual review/unresolved] | [F/U/?] |

## Documents and sources

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [user document name or chat date] | [canonical type] | [year] | taxpayer | [page/section] | [needed facts] | [extracted/needs review] |

No identifiers, payment references, copied evidence or file hashes.

## Sources used

[Exactly consulted source_ids matching Appendix A sources_loaded.]

## Original filed return

Original filing confirmation/date and baseline accounting period — Src: [F/U].
Prior corrections and controlling baseline — Src: [F/U / unresolved].

| Original rubric / fact | Turnover excluding VAT | VAT / balance | Src |
|------------------------|-------------------------|---------------|-----|
| [original rubric] | [EUR/n/a] | [EUR/n/a] | [F/U/?] |
| `vat.correction.previous_balance` | n/a | [signed EUR] | [F/U/?] |

Sign convention: positive net balance means VAT payable; negative means refund.

## Correction facts and timeline

- Error description/affected invoices and period basis: [facts + Src].
- Discovery date: [YYYY-MM-DD / unresolved + Src].
- Already reported: [yes/no/unresolved + Src].
- Sourced reporting timing and human follow-up: [rule/source_id + facts].

## Corrected rubric reconciliation

Every applicable rubric includes its unchanged full amount or sourced zero;
it is never omitted because the error affected a different rubric.

| Rubric / stable fact ID | Original full amount | Corrected full amount | Difference | Derivation, rounding and Src |
|-------------------------|----------------------|-----------------------|------------|------------------------------|
| [vat.<rubric>.turnover / vat.<rubric>.vat] | [EUR] | [EUR] | [signed EUR] | [components + C/F/U/?] |

| Comparison fact | Signed amount | Derivation and Src |
|-----------------|---------------|--------------------|
| `vat.correction.previous_balance` | [EUR] | [original declaration + F/U/?] |
| `vat.total.balance` | [EUR] | [corrected output/assessed VAT minus eligible input VAT + C] |
| `vat.correction.delta` | [EUR] | [corrected balance minus previous balance + C] |

Positive delta = additional VAT payable; negative delta = additional refund
or reduction. Show raw calculations and official rounded entry figures
separately. Record bookkeeping reconciliation and every unresolved difference.

## Correction route

- Original-period deadline passed on correction date: [yes/no + Src].
- Original-period VAT correction measure: [signed delta and magnitude + Src].
- Sourced threshold and route: [small later-return / suppletie / unresolved;
  knowledge note source_id].
- Separate-period screen: [this original period only; other periods separate].
- Small correction: [confirmed next (eerstvolgende) return's year/assigned
  period after discovery or unresolved; carry-once correction components with
  provenance].
- Suppletie: [corrected full original-period figures, unchanged rubrics included;
  prior declared balance and difference kept separate].
- Net-zero differences: [reporting treatment confirmed or human-review blocker].
- Letter-route items and rubric 3b letter: [none / named items for human handling].
- Payment/refund follow-up: [deadline not passed: the human pays by that
  period's deadline using its genuine payment reference / deadline passed:
  the human awaits the naheffingsaanslag or teruggaafbeschikking and uses its
  details]; no payment reference is fabricated.

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

- [ ] I confirmed the actual original filing, assigned period and prior corrections.
- [ ] I checked every original and corrected full rubric against records.
- [ ] I checked timing, deduction, any foreign services and adviser adjustments.
- [ ] I checked original/corrected net balances and the separate signed VAT delta.
- [ ] I checked the threshold for this original period and the discovery timeline.
- [ ] I confirmed the target period for a small correction or the exact suppletie
  period/form; I did not substitute differences for corrected full totals.
- [ ] I resolved source-content, treatment, reconciliation and route blockers;
  unresolved items keep this workpack draft.
- [ ] I checked all chat values, assumptions and open questions.
- [ ] I will perform reporting and any payment steps personally using the genuine
  instructions in Mijn Belastingdienst Zakelijk or the official notice.

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
workflow: vat_correction_<year>_<period>
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
  vat_original: {status: not_started, open: []}
  vat_reconciliation: {status: not_started, open: []}
  vat_correction_route: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

not yet mapped
