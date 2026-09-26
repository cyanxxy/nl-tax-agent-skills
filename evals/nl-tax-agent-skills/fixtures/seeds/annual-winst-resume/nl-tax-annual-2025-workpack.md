# Annual Income-Tax Return Workpack -- 2025

> **STATUS: DRAFT — 7 open section(s) — not for filing.** This workpack is never submission advice; filing always happens manually via Mijn Belastingdienst.

> **Provenance convention.** Every numeric line in this workpack records its source in a `Src` column or inline `Src:` note.
> Source codes:
> - `F:<evidence_id>` -- value taken from a document row (`ev_NNN`) in Documents and sources
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat, also listed in the User-stated values index
> - `A:<assumption_id>` -- assumption the taxpayer explicitly accepted, also listed under Assumptions
> - `?` -- required but still missing, also listed under Missing information
> - `C:<formula>` -- computed from other sourced rows

## How to use this file

- This is your own working file for your 2025 Dutch income-tax return, built only from what you shared in the conversation.
- To continue later, keep it in your working folder or attach it to a new conversation.
- Filing is always manual: you (the taxpayer) or an authorized human enter, sign, and submit the return in Mijn Belastingdienst.

## Contents

- Scope
- Unsupported-case checks
- Taxpayer profile summary
- Documents and sources
- Sources used
- Filing status and late-filing exposure
- Income notes
- Winst uit onderneming notes
- Own-home notes
- Box 2 notes
- Box 3 notes
- Deductions notes
- Credits screening
- Fiscal partner notes
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

## Scope

Tax year: 2025
Workflow: Annual income-tax return (aangifte inkomstenbelasting)
Taxpayer: the taxpayer (eenmanszaak)
Fiscal partner: no -- Src: profile.partner.has_fiscal_partner
Created: 2026-09-18T19:02:00Z

## Unsupported-case checks

- [x] Full-year Dutch resident: yes
- [x] Individual taxpayer -- non-business individual or recognised IB business form: yes (eenmanszaak)
- [x] Living taxpayer: yes
- [x] No M-biljet required: yes
- [x] No complex Box 2 manual-review trigger blocking standard preparation: not applicable
- [x] Terminal business-computation trigger present: no

## Taxpayer profile summary

| Key | Value | Src |
|-----|-------|-----|
| `residency.full_year_nl_resident` | yes | U:"I lived in Utrecht all of 2025" (2026-09-18) |
| `taxpayer.type` | individual with a recognised IB business form | U:"I run an eenmanszaak" (2026-09-18) |
| `taxpayer.primary_income_type` | business | U:"the business is my only income" (2026-09-18) |
| `person.aow_by_tax_year.2025.status` | below_all_year | C:aow_rule(person.date_of_birth) |
| `partner.has_fiscal_partner` | no | U:"no partner" (2026-09-18) |
| `household.children_at_home_count` | 0 | U:"no children" (2026-09-18) |
| `box2.has_aanmerkelijk_belang` | no | U:"no shares in a BV" (2026-09-18) |
| `routing.complex_box2_screening` | not applicable | U:"no shares in a BV" (2026-09-18) |
| `business.has_onderneming` | yes | U:"I run an eenmanszaak" (2026-09-18) |
| `business.legal_form` | eenmanszaak | F:ev_001 |
| `routing.complex_business_screening` | standard | U:"no partners in the business, no BV" (2026-09-18) |
| `special_circumstances` | none | U:"nothing unusual" (2026-09-18) |

## Documents and sources

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | winst-verlies-rekening-2025 | winst_verlies_rekening | 2025 | taxpayer | page 1 | omzet: EUR 62,000; kosten: EUR 14,000; saldo: EUR 48,000 | extracted |
| ev_002 | balans-2025 | balans | 2025 | taxpayer | page 1, begin and eind column | ondernemingsvermogen begin: EUR 20,000; eind: EUR 24,500 | extracted |
| ev_003 | urenadministratie-2025 | urenadministratie | 2025 | taxpayer | totals row | uren: 1,600 | extracted |
| ev_004 | chat 2026-09-18 | user_chat | 2025 | taxpayer | chat | aangiftebrief received: "I got the letter to file for 2025" | extracted |

## Sources used

- bd_annual_filing_obligation_2025
- bd_annual_deadline_2025
- bd_ondernemer_criteria_2025
- bd_ib_aangifte_voor_ondernemers

## Filing status and late-filing exposure

- Filing-route label: `invited` -- Src: F:ev_004
- Filing status: on time. No late-filing penalty exposure. This does not promise zero belastingrente.

## Income notes

Not applicable -- no employment, pension, benefit, or other box 1 income reported. -- Src: U:"the business is my only income" (2026-09-18)

## Winst uit onderneming notes

### Income-category screen

- Bron van inkomen confirmed: yes -- Src: F:ev_001
- Category: winst uit onderneming -- Src: F:ev_001
- Ondernemer voor de inkomstenbelasting (eenmanszaak / ZZP): yes -- Src: F:ev_001
- Urencriterium met: yes, 1,600 uren -- Src: F:ev_003
- Starter history, S&O-verklaring, meewerkende partner: no starter years, no S&O, no meewerkende partner -- Src: U:"not a starter, no S&O, I work alone" (2026-09-18)
- Investeringen in 2025: ? -- open question Q001

### Finalized accounts evidence

| Item | Status / evidence | Src |
|------|-------------------|-----|
| Finalized profit-and-loss statement for 2025 | reviewed | F:ev_001 |
| Finalized balance for 2025 (begin and eind column) | reviewed | F:ev_002 |

### Ordered profit chain

| Line | Step | Amount | Derivation | Src |
|------|------|--------|------------|-----|
| A | Winst uit onderneming (saldo fiscale winstberekening) | EUR 48,000 | omzet EUR 62,000 minus kosten EUR 14,000; no fiscal corrections reported | F:ev_001 |
| B | Minus investeringsaftrek | ? | depends on Q001 | ? |
| C | Minus ondernemersaftrek | Not yet reviewed. | | |
| D | Minus MKB-winstvrijstelling | Not yet reviewed. | | |
| E | Belastbare winst uit onderneming | Not yet reviewed. | | |

## Own-home notes

Not yet reviewed.

## Box 2 notes

> Not applicable -- no substantial interest (aanmerkelijk belang) reported.
> box2.has_aanmerkelijk_belang: no

## Box 3 notes

Not yet reviewed.

## Deductions notes

Not yet reviewed.

## Credits screening

Not yet reviewed.

## Fiscal partner notes

Not applicable -- the taxpayer does not have a fiscal partner for tax year 2025.

## Open questions

| Q-ID | Section | Question | Blocking | Status |
|------|---------|----------|----------|--------|
| Q001 | `winst` | Did you buy business assets (investeringen) in 2025, and if so which assets, when, and for how much? | yes | open |

## Missing information

### Critical (blocks accurate filing)

| M-ID | Description | Workpack row | Q-ID | How to resolve |
|------|-------------|--------------|------|----------------|
| M001 | 2025 investments for the investeringsaftrek screen | Winst uit onderneming notes / line B | Q001 | Check the 2025 purchase invoices for business assets |

Total missing items: 1

## Assumptions

None -- no assumptions were used.

## User-stated values index

| Workpack row | Value | Quote | Stated at | Document row |
|--------------|-------|-------|-----------|--------------|
| Taxpayer profile summary / residency | yes | "I lived in Utrecht all of 2025" | 2026-09-18 | — |
| Winst uit onderneming notes / starter history | none | "not a starter, no S&O, I work alone" | 2026-09-18 | — |

## Field map summary

not yet mapped

## Manual-entry checklist

not requested

## Human review checklist

- [ ] Winst uit onderneming reviewed: every line of the chain checked against my own jaarstukken
- [ ] All `U:` user-chat values reviewed for accuracy
- [ ] All `?` missing information resolved or consciously accepted
- [ ] Every blocking open question answered; any question left open keeps this workpack a draft

## Not submission advice

This workpack is a preparation aid. You, the taxpayer or an authorized human,
must review the figures and perform all portal entry, signing, and submission
yourself. The assistant must not access or operate Mijn Belastingdienst.

## Appendix A — Resume record

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.4.0"
workflow: annual_2025
tax_year: 2025
created_at: "2026-09-18T19:02:00Z"
updated_at: "2026-09-18T20:41:00Z"
save_consent: given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  filing_status: {status: complete, open: []}
  box1: {status: chat_only, open: []}
  winst: {status: in_progress, open: [Q001]}
  eigen_woning: {status: not_started, open: []}
  box2: {status: chat_only, open: []}
  box3_peildatum: {status: not_started, open: []}
  box3_actual: {status: not_started, open: []}
  deductions: {status: not_started, open: []}
  credits_screening: {status: not_started, open: []}
  partner_allocation: {status: chat_only, open: []}
  confirm: {status: not_started, open: []}
sources_loaded:
  - bd_annual_filing_obligation_2025
  - bd_annual_deadline_2025
  - bd_ondernemer_criteria_2025
  - bd_ib_aangifte_voor_ondernemers
```

## Appendix B — Field map

not yet mapped
