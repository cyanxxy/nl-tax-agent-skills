# Voorlopige Aanslag Workpack — 2026

> **STATUS: DRAFT — 5 open section(s) — not for filing.** This workpack is never submission advice; you (the taxpayer) or an authorized human make every request, change, or stop manually in Mijn Belastingdienst.

> **Provenance convention.** Every numeric line in this workpack records its source in a `Src` column or inline `Src:` note.
> Source codes:
> - `F:<evidence_id>` -- value from a document listed under Documents and sources, such as a beschikking
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat, also listed under User-stated values index
> - `A:<assumption_id>` -- user-accepted assumption, also listed under Assumptions
> - `B:<baseline_ref>` -- value carried over from the existing voorlopige aanslag baseline
> - `?` -- required but still missing, also listed under Missing information
> - `C:<formula>` -- computed from other sourced rows
>
> All amounts are estimates unless explicitly tagged `B:` as baseline/from-baseline.

## How to use this file

- This is your own working file for the 2026 voorlopige aanslag; you decide where it is kept and when it is deleted.
- To continue later, attach this file to a new conversation or keep it in your working folder as `workspace/nl-tax-provisional-2026-workpack.md`.
- Filing is always manual: you (the taxpayer) or an authorized human request, change, or stop the voorlopige aanslag in Mijn Belastingdienst.

## Contents

- Subflow: change
- Scope
- Unsupported-case checks
- Taxpayer profile summary
- Documents and sources
- Sources used
- Existing baseline, if any
- Current-year estimates
- Delta summary
- Review questions
- Stopzetten outcome
- Income estimate
- Winst uit onderneming forecast
- Own-home estimate
- Box 2 provisional estimate
- Box 3 provisional estimate
- Deductions estimate
- Change subflow — full re-entry reminder
- Open questions
- Missing information
- Assumptions
- User-stated values index
- Field map summary
- Manual-entry checklist
- Human review checklist
- Not submission advice
- Appendix A — Resume record
- Appendix B — Field map

## Subflow: change

## Scope

| Field            | Value                                |
|------------------|--------------------------------------|
| Tax year         | 2026                                 |
| Workflow         | Voorlopige aanslag (change)          |
| Fiscal partner   | no                                   |
| Created          | 2026-09-19                           |
| Last updated     | 2026-09-19                           |

## Unsupported-case checks

- [x] Dutch resident for all of 2026, with no migration planned: yes
- [x] Individual taxpayer -- non-business individual or recognised IB business form: yes (non-business individual)
- [x] Living taxpayer: yes
- [x] No non-resident, treaty-heavy, or foreign-pension treaty issue: yes
- [x] No complex Box 2 manual-review trigger blocking standard preparation: not applicable
- [x] Complex business form or event present: not applicable

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `residency.full_year_nl_resident` | yes | U:"I live in Amersfoort and will all year" (2026-09-19) |
| `taxpayer.type` | non-business individual | U:"I'm employed, no business" (2026-09-19) |
| `person.aow_by_tax_year.2026.status` | below_all_year | C:aow_rule(person.date_of_birth) |
| `partner.has_fiscal_partner` | no | U:"single, no partner" (2026-09-19) |
| `household.children_at_home_count` | none | U:"no kids" (2026-09-19) |
| `box2.has_aanmerkelijk_belang` | no | U:"no BV shares" (2026-09-19) |
| `routing.complex_box2_screening` | not applicable | U:"no BV shares" (2026-09-19) |
| `business.has_onderneming` | no | U:"I'm employed, no business" (2026-09-19) |
| `routing.complex_business_screening` | not applicable | U:"I'm employed, no business" (2026-09-19) |
| `provisional.current_va_direction` | monthly payment | F:ev_001 |

## Documents and sources

| ID | Document (as you named it) | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------------------------|------|----------|-------|----------|--------------|--------|
| ev_001 | VA 2026 letter | voorlopige_aanslag_beschikking | 2026 | taxpayer | page 1 and page 2 | monthly payment: EUR 150; employment income basis: EUR 48,000; mortgage interest basis: EUR 12,000 | extracted |
| ev_002 | chat 2026-09-19 | user_chat | 2026 | taxpayer | chat | expected 2026 salary: "my salary this year will be EUR 58,000" | extracted |

## Sources used

- bd_provisional_change_2026
- bd_algoritmeregister_vva_eva
- bd_box1_rates_2026

## Existing baseline, if any

| Field | Value | Src |
|-------|-------|-----|
| Beschikking date | 2026-01-24 | F:ev_001 |
| Monthly amount | EUR 150 payment (from-baseline) | F:ev_001 |
| Source type | beschikking | F:ev_001 |

## Current-year estimates

### Estimated employment income 2026

| Item                        | Amount (estimate) | Src |
|-----------------------------|-------------------|-----|
| Gross annual salary         | EUR 58,000 (estimate) | U:"my salary this year will be EUR 58,000" (2026-09-19) |
| **Total employment income** | EUR 58,000 (estimate) | C:sum |

### Estimated pension/benefit income 2026

Not yet reviewed.

### Estimated other income 2026

Not yet reviewed.

## Delta summary

| Category               | Baseline      | Src (baseline) | Current Estimate | Src (current) | Delta         | Notes |
|------------------------|---------------|----------------|------------------|---------------|---------------|-------|
| Employment income      | EUR 48,000 (from-baseline) | B:ev_001 | EUR 58,000 (estimate) | U:"my salary this year will be EUR 58,000" (2026-09-19) | EUR 10,000 | |

Other categories: not yet reviewed.

## Review questions

N/A — not applicable for this subflow

## Stopzetten outcome

N/A — not applicable for this subflow

## Income estimate

Not yet reviewed.

## Winst uit onderneming forecast

Not applicable -- no expected profit from enterprise reported. -- Src: U:"I'm employed, no business" (2026-09-19)

## Own-home estimate

Not yet reviewed.

## Box 2 provisional estimate

Not applicable -- no substantial interest (aanmerkelijk belang) reported.

## Box 3 provisional estimate

> Werkelijk rendement is not part of provisional 2026.

Not yet reviewed.

## Deductions estimate

Not yet reviewed.

## Change subflow — full re-entry reminder

> Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

The portal may offer to pre-fill figures from the most recent annual return; it
does not carry forward the current voorlopige-aanslag figures. Whether the form
opens blank or pre-filled, you (the taxpayer) verify every applicable category.

## Open questions

| Q-ID | Section | Question | Blocking | Status |
|------|---------|----------|----------|--------|
| Q001 | `deductions` | What mortgage interest do you expect to pay in 2026 after this year's repayments? | yes | deferred |

## Missing information

| M-ID | Description | Workpack row | Q-ID | How to resolve |
|------|-------------|--------------|------|----------------|
| M001 | Expected 2026 mortgage interest | Own-home estimate / mortgage interest | Q001 | The lender's 2026 overview or online mortgage account |

Total missing items: 1

## Assumptions

None -- no assumptions were used.

## User-stated values index

| Workpack row | Value | Quote | Stated at | Document row |
|--------------|-------|-------|-----------|--------------|
| Current-year estimates / gross annual salary | EUR 58,000 | "my salary this year will be EUR 58,000" | 2026-09-19 | ev_002 |

## Field map summary

not yet mapped

## Manual-entry checklist

not requested

## Human review checklist

- [ ] All income estimates are reasonable and based on current knowledge
- [ ] For change subflow: all data has been entered, not just the changed items
- [ ] All `U:` user-chat values reviewed for accuracy
- [ ] All `?` missing information resolved or consciously accepted

## Not submission advice

This workpack is a preparation aid. You, the taxpayer or an authorized human,
must review the figures and perform all portal entry, signing, sending, or
changes yourself. The assistant must not access or operate Mijn
Belastingdienst.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.4.0"
workflow: provisional_2026_change
tax_year: 2026
created_at: "2026-09-19T08:15:00Z"
updated_at: "2026-09-19T08:52:00Z"
save_consent: given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  baseline: {status: complete, open: []}
  income_employment: {status: chat_only, open: []}
  income_pension_benefit: {status: not_started, open: []}
  income_other: {status: not_started, open: []}
  winst_forecast: {status: chat_only, open: []}
  deductions: {status: deferred, open: [Q001]}
  box2: {status: chat_only, open: []}
  box3_peildatum: {status: not_started, open: []}
  partner_allocation: {status: chat_only, open: []}
  confirm: {status: not_started, open: []}
sources_loaded:
  - bd_provisional_change_2026
  - bd_algoritmeregister_vva_eva
  - bd_box1_rates_2026
```

## Appendix B — Field map

not yet mapped
