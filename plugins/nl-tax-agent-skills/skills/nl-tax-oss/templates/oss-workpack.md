# Dutch OSS Workpack — {scheme} {year} {period}

> **STATUS: DRAFT — N deferred section(s) — not for filing.**
> Source/treatment review blockers: [named blockers / none].
> The human supplies genuine registration identifiers and payment instructions
> separately from their administration/current declaration.

> **Provenance:** F:ev_NNN document; U:short quote (YYYY-MM-DD) chat;
> A:ID explicitly accepted assumption; ? missing; C:formula from sourced rows.
> Missing never means zero; profile keys refer to sourced profile rows.

[Remove fill notes from established output. Unopened collection sections hold
Not yet reviewed. Chat shows only filled sections and no Appendix A/B YAML.]

## How to use this file

This is the OSS/IOSS preparation workpack for one scheme and confirmed period.
Keep it to resume. You (the taxpayer) or an authorized human check the genuine
registration identifiers and personally perform all authenticated entry,
signing and submission in Mijn Belastingdienst Zakelijk.

## Scope

- Scheme: [union / non_union / ioss] — Src: profile.oss.scheme
- Tax year: [2025 / 2026] — Src: profile.oss.tax_year
- Period and exact dates: [Q1..Q4 / M01..M12; start/end] — Src: [F/U/?]
- Member state of identification: Netherlands — Src: profile.oss.identification_state
- Workflow: scheme-specific OSS/IOSS declaration
- Created: [timestamp]

## Unsupported-case checks

Record scheme eligibility/registration, business and fixed establishments,
intermediary, destination/rate evidence, threshold/election, KOR/EU-KOR,
marketplace liability, special goods, imports, fiscal units and customs-base
questions as confirmed ordinary, sourced not applicable or open. Unresolved
special treatments stay blocking; confirmed specialist facts carry provenance.

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `oss.scheme` | [union/non_union/ioss] | [F/U/?] |
| `oss.tax_year` | [2025/2026] | [F/U/?] |
| `oss.period` | [scheme-correct period] | [F/U/?] |
| `oss.period_confirmed` | [yes/no] | [F/U/?] |
| `oss.period_closed` | [yes/no] | [F/U/?] |
| `oss.identification_state` | [Netherlands/other/open] | [F/U/?] |
| `oss.registration_and_dates` | [confirmed active scheme/dates/open] | [F/U/?] |
| `oss.establishment_screen` | [countries and confirmed business/fixed status/open] | [F/U/?] |
| `oss.intermediary_status` | [confirmed/not applicable/open] | [F/U/?] |
| `oss.already_filed` | [yes/no] | [F/U/?] |
| `oss.threshold_and_election` | [confirmed/not applicable/open] | [F/U/?] |
| `oss.kor_eu_kor_screen` | [confirmed/not applicable/open] | [F/U/?] |

## Documents and sources

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [document name/chat date] | [canonical type] | [year] | taxpayer | [page/section] | [needed non-identifying facts] | [extracted/needs review] |

## Sources used

[Exactly consulted applicable source_ids matching sources_loaded.]

## OSS scheme and period

Registration/effective dates, establishment and intermediary confirmation,
calendar dates/closed-period status, filing/payment deadline and human follow-up.
Current/prior-year threshold and election screen if applicable. Nil requires
sourced no-current-supplies and no-corrections; a correction-only period is
distinct. IOSS eligibility/payment timing and relevant 2026 customs-base
breakdown are explicit.

## OSS transaction notes

| Group alias | Consumption state | Supply kind/origin | Period basis | Taxable base/currency | Verified rate/evidence and date | VAT/currency | EUR conversion/source | Src |
|-------------|-------------------|--------------------|--------------|-----------------------|-----------------------------|--------------|-----------------------|-----|
| [alias] | [country] | [goods/services/imports; origin] | [supply/payment date] | [amount/currency] | [rate/category/official evidence and human date] | [amount/currency] | [ECB date/rate/direction/formula] | [F/U/C/?] |

Record excluded domestic/exempt/zero-rated supplies separately and explain
their evidence-based classification. Input VAT is not an OSS deduction.

## OSS correction notes

| Correction alias | Scheme/original period | Consumption state | Originally filed VAT | Prior correction deltas | Target corrected VAT | Remaining signed delta | Reason/window | Src |
|------------------|------------------------|-------------------|----------------------|-------------------------|----------------------|------------------------|---------------|-----|
| [alias] | [same scheme/year/period] | [country] | [EUR] | [EUR] | [EUR] | [C:target-original-prior] | [error/credit note; original due date, window end = due date + 3 years, this return's due date] | [F/U/C/?] |

Later credits correct their original supply period once. Expired-window or
terminated-registration cases require the consumption state's human process.

## OSS reconciliation

| Stable row ID | Dimensions | Raw EUR | Form EUR | Derivation/precision | Src |
|---------------|------------|---------|----------|----------------------|-----|
| [oss.row.alias.taxable_base/vat_amount] | [scheme/country/rate/kind/origin; original period for correction] | [EUR] | [EUR/open] | [components/form-confirmed method] | [F/U/C/?] |

| Consumption state | Current VAT | Signed prior-period corrections | Country balance | Positive payable | Negative balance for refund review | Src |
|-------------------|-------------|---------------------------------|-----------------|------------------|------------------------------------|-----|
| [country] | [EUR] | [EUR] | [C:current+corrections] | [C:max(0,balance)] | [C:max(0,-balance)] | [F/U/C/?] |

Total payable: [C:sum(positive country balances) / EUR / Src].
Separate refund-review totals: [EUR per state / Src], never offset against
another state's payable.
Source grid/control-account difference: [EUR/explanation/Src or Q-ID].
Separate domestic VAT/ICP follow-up: [confirmed scope / open].

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

- [ ] I checked scheme eligibility, registration dates and exact period.
- [ ] I checked destination, each product/service rate and origin evidence.
- [ ] I checked applicable threshold/KOR and IOSS import/payment screens.
- [ ] I checked source VAT, period-end ECB conversion (or the next ECB
  publication day) and form precision.
- [ ] I checked original filed figures, prior corrections and remaining deltas.
- [ ] I kept negative country balances separate from other countries' payable.
- [ ] I reconciled all current transactions once and excluded input VAT deductions.
- [ ] I resolved source/form and special-treatment blockers.
- [ ] I checked every user-stated value and accepted assumption.
- [ ] I will personally check the current form and its genuine registration/
  payment instructions in Mijn Belastingdienst Zakelijk before submission.

## Not submission advice

This workpack is a preparation aid. You (the taxpayer) or an authorized human
review the figures, obtain the genuine registration/payment information and
perform every authenticated entry, signing and submission yourself in Mijn
Belastingdienst Zakelijk. The assistant must not access or operate the portal.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.5.0"
workflow: oss_<scheme>_<year>_<period>
tax_year: null
scheme: ""
period: ""
created_at: ""
updated_at: ""
save_consent: not_given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  oss_scope: {status: not_started, open: []}
  oss_transactions: {status: not_started, open: []}
  oss_corrections: {status: not_started, open: []}
  oss_reconciliation: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

not yet mapped
