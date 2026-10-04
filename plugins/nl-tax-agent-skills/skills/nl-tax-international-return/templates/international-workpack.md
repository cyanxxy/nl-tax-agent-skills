# Dutch International Income-Tax Workpack — {year} {form}

> **STATUS: DRAFT — N deferred section(s) — not for filing.**
> Source/form/treatment blockers: [named blockers].
> [For 2026: 2026 precollection only — final annual M/C schema not established.]

> **Provenance:** `F:ev_NNN` document; `U:"quote" (YYYY-MM-DD)` chat;
> `A:ID` accepted factual assumption; `?` missing; `C:formula` sourced calculation.
> Missing never means zero. Profile references point to sourced rows.

[Remove fill notes and placeholders. Unreached collection sections may hold
`Not yet reviewed.`. Chat shows filled sections without Appendix A/B YAML.]

## How to use this file

Keep this one year/form workpack to resume preparation. You (the taxpayer)
or an authorized human review the facts and personally perform every
authenticated action in Mijn Belastingdienst.

## Scope

- Tax year: [2025/2026] — Src: profile.international.tax_year
- Form: [migration/nonresident] — Src: profile.international.return_form
- Preparation stage: [2025 annual preparation / 2026 precollection only]
- Created: [timestamp]

## Unsupported-case checks

- Deceased taxpayer (F-biljet): [not applicable, sourced / outside this owner] — Src: [F/U/?]
- Other tax year than 2025 or 2026: [not applicable / outside this owner] — Src: [F/U/?]
- Disputed treaty residence, government posting, special pension or treaty issue, or exit-tax issue: [not applicable, sourced / open review blocker] — Src: [F/U/?]

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `international.tax_year` | [year] | [F/U/?] |
| `international.return_form` | [migration/nonresident] | [F/U/?] |
| `international.form_confirmed` | [yes/no] | [F/U/?] |
| `international.residence_status` | [confirmed facts/unresolved] | [F/U/?] |
| `international.filing_status` | [invited/other official basis/unresolved] | [F/U/?] |
| `international.already_filed` | [yes/no] | [F/U/?] |
| `international.partner_status` | [confirmed facts/not applicable/unresolved] | [F/U/?] |
| `international.partial_foreign_liability_choice` | [not applicable/chosen/not chosen/unresolved] | [F/U/?] |

## Documents and sources

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [source name or chat date] | [canonical type] | [year] | taxpayer | [page/section] | [needed facts] | [extracted/needs review] |

No identifiers, file hashes or copied evidence.

## Sources used

[Exactly consulted source_ids matching Appendix A sources_loaded.]

## Filing status and deadlines

Invitation/other official basis, genuine deadline, extension and earlier
filing — [facts with F/U/?]. Unresolved or late matters — [human follow-up].

## Residence timeline

| Interval | Start | End | Country | Actual/domestic-law/treaty residence basis | Src |
|----------|-------|-----|---------|-------------------------------------------|-----|
| [interval] | [date] | [date] | [country] | [confirmed basis/unresolved] | [F/U/?] |

Full-year coverage/boundary check — [result or exact gaps/overlaps].
Migration dates, relevant household/home ties and disputed status — [facts].

## Income and assets by country and period

| Group | Category | Source/work country | Covered interval | Gross EUR | Dutch/foreign withholding EUR | Dutch-reportable treatment | Src |
|-------|----------|---------------------|------------------|-----------|-------------------------------|---------------------------|-----|
| [group] | [category] | [country] | [interval] | [EUR/?] | [separate amounts/?] | [confirmed basis/unresolved] | [F/U/?] |

Currency conversion — [original amount, currency, rate, rate date, rate source and EUR derivation per item].

| Asset/debt group | Category/location | Valuation date/interval | Ownership share | Value EUR | Fictitious/actual-return evidence status | Src |
|------------------|-------------------|-------------------------|-----------------|-----------|-----------------------------------------|-----|
| [group] | [category/country] | [date/interval] | [confirmed/?] | [EUR/?] | [confirmed/not yet collected] | [F/U/?] |

Conserved income and revisierente (emigration: pension or lijfrente
aanspraken, eigen-woning capital insurance, substantial interest at the
emigration date; every M and C return: pension or lijfrente capital moved to
a foreign insurer, a lijfrente continued at a non-admitted foreign insurer
after immigration, a pension or lijfrente buy-out or breach; C: onward
emigration or a substantial interest acquired as a nonresident) — [facts +
Src / open Q-ID / not applicable: sourced answer per item + Src].

Worldwide evidence inventory is separate from Dutch-taxable amounts.
Period/category omissions and unsupported computations — [open questions].

## Qualifying nonresident status and income statement

Qualifying-country intervals, partner/exception facts and legal status —
[confirmed/unresolved + Src].

| Preparation measure | Amount/result | Components and rule provenance |
|---------------------|---------------|--------------------------------|
| Dutch-taxed qualification measure | [EUR/?] | [F/U/C/rule] |
| Worldwide qualification measure | [EUR/?] | [F/U/C/rule] |
| Sourced percentage test | [result/not computed] | [formula and exclusions or missing inputs] |

This tests one condition only; it does not decide qualification or residence.
Income-statement stage, prior provision/continuing eligibility, authority
request and remaining human action — [facts + Src]. For 2026 use only the
2026 note; do not inherit a 2025 proof requirement.

## Social insurance and healthcare

| Scheme/status | Mandatory/voluntary | Exact start/end | Work/coverage country | Authority/adviser basis | Src |
|---------------|---------------------|-----------------|-----------------------|------------------------|-----|
| [AOW/Anw/Wlz/Zvw/overseas contribution] | [status/?] | [dates/?] | [country] | [confirmed/unresolved] | [F/U/?] |

Unresolved posting/EU applicable-legislation certificate/SVB or foreign-coverage issues — [questions].

## Treaty and source-country review

| Group | Countries | Asserted taxing right | Treaty/article/version or official basis | Relief method | Status and Src |
|-------|-----------|-----------------------|------------------------------------------|---------------|----------------|
| [group] | [countries] | [confirmed/unresolved] | [basis/?] | [confirmed/unresolved] | [F/U/? + review blocker] |

No default treaty exemption or foreign-withholding credit.

## Deductions, credits and partner facts

| Item | Relevant residence/qualification/insurance period | Conditions and amount | Foreign benefit/partner check | Status and Src |
|------|---------------------------------------------------|-----------------------|-------------------------------|----------------|
| [item] | [interval/?] | [confirmed facts/?] | [confirmed/unresolved] | [F/U/C/?] |

Taxpayer-selected allocation, if legally available — [not selected/confirmed
human selection + U]. No automatic selection or eligibility.

## Preparation reconciliation

| Check/formula | Sourced components | Result | Unresolved difference |
|---------------|--------------------|--------|-----------------------|
| [group/annual/qualification check] | [F/U] | [C:formula/not computed] | [none/question ID] |

No final liability, treaty relief or premium estimate from incomplete inputs.

## Open questions

| ID | Section | Question | Blocking | Status |
|----|---------|----------|----------|--------|
| Q001 | [section key] | [question] | [yes/no] | [open/answered] |

## Missing information

| ID | Missing item | Linked Q-ID | Why needed |
|----|--------------|-------------|------------|
| M001 | [item] | Q001 | [reason] |

## Assumptions

| ID | Factual assumption | User acceptance and date | Affected facts |
|----|--------------------|--------------------------|----------------|
| A001 | [assumption] | [quote/date] | [facts] |

## User-stated values index

| Fact | Value | Verbatim short quote | Stated at |
|------|-------|----------------------|-----------|
| [fact] | [value] | [quote] | [date] |

## Field map summary

not yet mapped

## Manual-entry checklist

not requested

## Human review checklist

- [ ] I confirmed year/form, the filing basis and the exact full-year timeline.
- [ ] I checked each country/period income and asset group and every chat value.
- [ ] I answered the conserved-income, revisierente, foreign-insurer and 30%-ruling choice questions where they apply.
- [ ] I resolved tax/treaty residence, qualification and income-statement issues.
- [ ] I checked insurance periods separately from income-tax treatment.
- [ ] I reviewed source-country rights, relief, deductions and partner facts.
- [ ] I reconciled permitted calculations and resolved source/form review gaps.
- [ ] I understand that 2026 precollection cannot become a final M/C entry map.
- [ ] I will perform authenticated filing actions personally.

## Not submission advice

This workpack is a preparation aid. You (the taxpayer) or an authorized human
must review the facts and perform all portal entry, signing and submission
yourself in Mijn Belastingdienst. The assistant must not access or operate it.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.5.0"
workflow: international_<year>_<form>
tax_year: null
return_form: ""
created_at: ""
updated_at: ""
save_consent: not_given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  international_scope: {status: not_started, open: []}
  residence_periods: {status: not_started, open: []}
  income_assets: {status: not_started, open: []}
  qualifying_status: {status: not_started, open: []}
  social_insurance: {status: not_started, open: []}
  treaty_review: {status: not_started, open: []}
  deductions_credits: {status: not_started, open: []}
  reconciliation: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

not yet mapped
