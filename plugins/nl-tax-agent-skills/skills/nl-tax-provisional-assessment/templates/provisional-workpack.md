# Voorlopige Aanslag Workpack — 2026

> **STATUS: {DRAFT — N open section(s) | COMPLETE DRAFT FOR REVIEW} — not for filing.** Replace `N` with the number of applicable sections not yet `complete` or `chat_only`; use "COMPLETE DRAFT FOR REVIEW" only when Appendix A `readiness` is `review_ready`. This workpack is never submission advice; you (the taxpayer) or an authorized human make every request, change, or stop manually in Mijn Belastingdienst.

> **Provenance convention.** Every numeric line in this workpack records its source in a `Src` column or inline `Src:` note.
> Source codes:
> - `F:<evidence_id>` -- value from a document listed under Documents and sources, such as a beschikking
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat, also listed under User-stated values index
> - `A:<assumption_id>` -- user-accepted assumption, also listed under Assumptions
> - `B:<baseline_ref>` -- value carried over from the existing voorlopige aanslag baseline
> - `?` -- required but still missing, also listed under Missing information
> - `C:<formula>` -- computed from other sourced rows
>
> All amounts are estimates unless explicitly tagged `B:` as baseline/from-baseline. A row marked `?` is never silently treated as zero.

## How to use this file

- This is your own working file for the 2026 voorlopige aanslag; you decide where it is kept and when it is deleted.
- To continue later, attach this file to a new conversation or keep it in your working folder as `workspace/nl-tax-provisional-2026-workpack.md`.
- Filing is always manual: you (the taxpayer) or an authorized human request, change, or stop the voorlopige aanslag in Mijn Belastingdienst.

## Contents

- Subflow: [request/change/review/stopzetten]
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

## Subflow: [request/change/review/stopzetten]

## Scope

| Field            | Value                                |
|------------------|--------------------------------------|
| Tax year         | 2026                                 |
| Workflow         | Voorlopige aanslag ([subflow])       |
| Fiscal partner   | [yes/no/unresolved]                  |
| Created          | [YYYY-MM-DD]                         |
| Last updated     | [YYYY-MM-DD]                         |

## Unsupported-case checks

- [ ] Dutch resident for all of 2026, with no migration planned: [yes/no] -- **moving abroad** needs a **residency review** and is **not a categorical stopzetten reason**
- [ ] Individual taxpayer -- non-business individual or recognised IB business form: [yes/no]
- [ ] Living taxpayer: [yes/no]
- [ ] No non-resident, treaty-heavy, or foreign-pension treaty issue: [yes/no]
- [ ] No complex Box 2 manual-review trigger blocking standard preparation: [yes/no/not applicable]

If residency, individual-taxpayer status, living status, or the
non-resident/treaty check is "no", this workpack should not be prepared; the
case is outside supported scope. A recognised IB business form is in scope:
for 2026 the workpack carries only its sourced, user-reviewed expected-profit
forecast (`onderneming.geschatte_winst`), never annual accounts or
entrepreneur deductions.

A complex business form or event (samenwerkingsverband profit share,
medegerechtigde loss caps, DGA/BV winst, agrarisch, zeevarende, cessation
profit, or another terminal business computation) is **not** a whole-case
exclusion and does not stop this workpack. It blocks one figure. Prepare the
rest of the workpack, name the blocked figure, and route only the business
forecast to manual review as described in the `Winst uit onderneming forecast`
section:

- [ ] Complex business form or event present: [no / yes -- blocked figure named in the Winst uit onderneming forecast section / not applicable]

## Taxpayer profile summary

[Facts established at intake or in this conversation, one row per fact with its
provenance. The `Key` column is stable so the field map's `source.profile_path`
can point to a row. No name, BSN, or IBAN is needed; do not record them.]

| Key | Value | Src |
|-----|-------|-----|
| `residency.full_year_nl_resident` | [yes / no -- moving or living abroad: terminal residency boundary, stop] | [F/U/?] |
| `taxpayer.type` | [non-business individual / individual with a recognised IB business form] | [F/U/?] |
| `person.date_of_birth` | [date] | [F/U/?] |
| `person.aow_by_tax_year.2026.status` | [below_all_year / reaches_during_year / aow_all_year] | [C:aow_rule(person.date_of_birth) / F/U/?] |
| `person.aow_by_tax_year.2026.transition_month` | [1..12 / n/a] | [C/F/U/?] |
| `partner.has_fiscal_partner` | [yes / no / unresolved] | [F/U/?] |
| `partner.partner_date_of_birth` | [date / n/a] | [F/U/?] |
| `partner.aow_by_tax_year.2026.status` | [below_all_year / reaches_during_year / aow_all_year / n/a] | [C/F/U/?] |
| `partner.aow_by_tax_year.2026.transition_month` | [1..12 / n/a] | [C/F/U/?] |
| `household.children_at_home_count` | [count and ages in 2026, for credit review / none] | [U/?] |
| `box2.has_aanmerkelijk_belang` | [yes/no] | [F/U/?] |
| `routing.complex_box2_screening` | [standard / manual_review / not applicable] | [U/?] |
| `business.has_onderneming` | [yes/no] | [F/U/?] |
| `business.legal_form` | [eenmanszaak / vof / maatschap / cv / bv / other / n/a] | [F/U/?] |
| `routing.complex_business_screening` | [standard / manual_review / not applicable] | [U/?] |
| `provisional.current_va_direction` | [none / monthly payment / monthly refund / unknown] | [F/U/?] |

## Documents and sources

[One row per document or chat value used. Assign the next unused `ev_NNN` and
never renumber. Name each document as you named it and use a canonical type
from the shared evidence-types reference. A chat value is named
`chat YYYY-MM-DD`, has type `user_chat`, and carries its short quote under
"Values taken". Take only the values needed plus the short quote required for
provenance: no file hashes, no copied content, and no full BSN, IBAN, policy,
contract, or aanslag number. Every `F:` code in this workpack points to a row
here.]

| ID | Document (as you named it) | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------------------------|------|----------|-------|----------|--------------|--------|
| ev_001 | [e.g. "VA 2026 letter" / chat YYYY-MM-DD] | [voorlopige_aanslag_beschikking / jaaropgaaf / woz_beschikking / hypotheek_jaaroverzicht / jaaroverzicht_bank / user_chat / other] | [2025/2026] | [taxpayer/partner/joint] | [page/section, or chat] | [values taken] | [extracted / needs review] |

## Sources used

[List exactly the reviewed `source_id`s consulted for provisional 2026, one per
line; this list equals Appendix A `sources_loaded`. Do not copy annual 2025
IDs; an ID used by both workflows appears here only if it was consulted
independently for provisional 2026.]

- [source_id_1]
- [source_id_2]
- [source_id_n]

## Existing baseline, if any

An **unsolicited** VA based on earlier data **may be issued**, but is **not guaranteed**. Record an EVA only when it actually exists in a shared document or is confirmed by the taxpayer.

[For change/review/stopzetten: summary of current voorlopige aanslag]

| Field | Value | Src |
|-------|-------|-----|
| Beschikking date | [date] | [F/U/?] |
| Monthly amount | [EUR X,XXX payment / EUR X,XXX refund] | [F/U/?] |
| Source type | [beschikking / user input / EVA / VVA] | [F/U/?] |

[For request: "No existing baseline — new request"]

## Current-year estimates

### Estimated employment income 2026

| Item                        | Amount (estimate) | Src |
|-----------------------------|-------------------|-----|
| Gross annual salary         | EUR               | [F/U/A/?] |
| Holiday allowance           | EUR               | [F/U/A/?] |
| Bonuses/other               | EUR               | [F/U/A/?] |
| **Total employment income** | EUR               | C:sum |

### Estimated pension/benefit income 2026

| Item                               | Amount (estimate) | Src |
|------------------------------------|-------------------|-----|
| AOW                                | EUR               | [F/U/A/?] |
| Pension                            | EUR               | [F/U/A/?] |
| WW/WIA/other benefits             | EUR               | [F/U/A/?] |
| **Total pension/benefit income**   | EUR               | C:sum |

### AOW age review

| Item | Value | Src / handling |
|------|-------|----------------|
| AOW status in 2026 | [below_all_year / reaches_during_year / aow_all_year] | [Taxpayer profile summary / C:aow_note / ?] |
| AOW transition month | [1..12 / N/A] | [Taxpayer profile summary / C:aow_note / ?] |
| Rate/credit handling | [whole-year non-AOW table / manual portal transition / whole-year AOW table] | [C:review] |

For `reaches_during_year`, do not use either whole-year table or interpolate a
credit. Record the month and use the live `Verzoek of wijziging voorlopige
aanslag 2026` result as a manual-review item.

### Estimated other income 2026

| Item                       | Amount (estimate) | Src |
|----------------------------|-------------------|-----|
| Other income sources       | EUR               | [F/U/A/?] |
| **Total other income**     | EUR               | C:sum |

### Expected profit from enterprise 2026

[If no enterprise: "Not applicable -- no expected profit from enterprise reported."]

| Item | Amount label | Src | Review |
|------|--------------|-----|--------|
| Expected full-year profit in `Winst uit onderneming` (`onderneming.geschatte_winst`) | EUR [amount] (estimate/from-baseline) | [F/U/B/?] | manual review required |

This is the taxpayer's sourced, user-reviewed forecast only. Do not substitute
a generic other-income field. Do not prepare annual accounts, entrepreneur
deductions, a bijdrage Zvw amount, cessation profit, or final tax.

The amount is the winst expected as ondernemer in 2026, taken **before** the
ondernemersaftrek and **before** the MKB-winstvrijstelling, excluding the btw
payable and the btw reclaimable, with a minus sign for an expected loss. State
that definition to the taxpayer before recording the amount. See the `Winst uit
onderneming forecast` section below for the rollover check and the separate
voorlopige aanslag Zorgverzekeringswet.

## Delta summary

[For `request`, `review`, or `stopzetten`, emit: `N/A — change subflow only.` For `change`, load `templates/sections/delta-summary.md` and fill that section here.]

## Review questions

[For `request`, `change`, or `stopzetten`, emit: `N/A — review subflow only.` For `review`, load `templates/sections/review-questions.md` and fill that section here.]

## Stopzetten outcome

[For `request`, `change`, or `review`, emit: `N/A — stopzetten subflow only.` For `stopzetten`, load `templates/sections/stopzetten-outcome.md` and fill that section here.]

## Income estimate

### Box 1 estimated income

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Total employment income               | EUR               | C:above |
| Total pension/benefit income          | EUR               | C:above |
| Total other income                    | EUR               | C:above |
| Expected profit from enterprise (`onderneming.geschatte_winst`) | EUR [estimate/from-baseline/N/A] | [F/U/B/?] |
| **Total Box 1 income before own-home balance** | EUR             | C:sum |

## Winst uit onderneming forecast

[If `business.has_onderneming` is `no`, emit: `Not applicable — no business income (Src: profile.business.has_onderneming).` If applicable, load `templates/sections/winst-forecast.md` and fill that section here.]

## Own-home estimate

### Estimated mortgage interest deduction 2026

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Mortgage interest (hypotheekrente)    | EUR               | [F/U/A/B/?] |
| Qualifying financing costs            | EUR               | [F/U/A/B/?] |
| Periodic erfpacht/opstal/beklemming   | EUR               | [F/U/A/B/?] |
| **Total deductible own-home costs**   | EUR               | C:sum |

### Estimated eigenwoningforfait 2026

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| WOZ-waarde (peildatum 1 January 2025) | EUR               | [F/U/A/B/?] |
| Eigenwoningforfait percentage         |                   | C:from_2026_table |
| Eigenwoningforfait amount            | EUR               | C:woz*pct |
| Hillen deduction, if applicable       | EUR               | [C:reviewed_formula/?] |
| **Box 1 own-home balance** (`box1_own_home_balance`) | EUR | C:eigenwoningforfait-total_deductible_own_home_costs-hillen_deduction |
| **Estimated Box 1 income after own-home balance** | EUR | C:income_before_own_home+box1_own_home_balance |

The WOZ date above is the own-home WOZ peildatum. Do not replace it with the
Box 3 asset/debt peildatum of 1 January 2026. Preserve every component even if
the live portal groups or labels them differently.

## Box 2 provisional estimate

[If `box2.has_aanmerkelijk_belang` is `no`, emit: `Not applicable — no substantial interest in 2026 (Src: profile.box2.has_aanmerkelijk_belang).` If applicable, load `templates/sections/box2-provisional.md` and fill that section here.]

## Box 3 provisional estimate

> Werkelijk rendement is not part of provisional 2026.

[The agent classifies rows from reviewed facts and the provisional Box 3
reference. Do not infer categories from names or keywords. Only accepted rows
with a supported category, finite non-negative value, and provenance enter the
totals below.]

### Accepted rows

| ID | Description | Category | Status | Value | Provenance |
|----|-------------|----------|--------|-------|------------|
| [row id] | [description] | [banktegoeden / overige_bezittingen / schulden] | accepted | EUR [estimate] | [F/U/A/B] |

### Rejected/manual-review rows

| ID | Description | Category | Status | Value | Provenance | Reason |
|----|-------------|----------|--------|-------|------------|--------|
| [row id] | [description] | [category/unknown] | [manual_review/rejected] | EUR [estimate] | [F/U/A/B/?] | [why excluded] |

Check trail: `check_performed_by: "checked_by_agent"`. Preserve this
trail and both tables even when there are no rejected rows.

### Assets on 1 January 2026

#### Categorie I — Banktegoeden

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Savings accounts                      | EUR               | [F/U/A/B/?] |
| Current accounts                      | EUR               | [F/U/A/B/?] |
| Deposits / term deposits              | EUR               | [F/U/A/B/?] |
| **Total banktegoeden**                | EUR               | C:sum |

#### Categorie II — Overige bezittingen

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Investments / securities              | EUR               | [F/U/A/B/?] |
| Real estate (not own home)            | EUR               | [F/U/A/B/?] |
| Crypto-assets                         | EUR               | [F/U/A/B/?] |
| Receivables (vorderingen)             | EUR               | [F/U/A/B/?] |
| Other assets                          | EUR               | [F/U/A/B/?] |
| **Total overige bezittingen**         | EUR               | C:sum |

### Categorie III — Schulden

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Candidate debts screened against the official Box 3 inclusion/exclusion list | EUR | [F/U/A/B/?] |
| **Total accepted qualifying Box 3 schulden** | EUR          | C:accepted_rows_sum |

A debt is not accepted merely because it is not an own-home mortgage. Record
its type and purpose; debts belonging in Box 1/2 and published exclusions stay
out, and unresolved debts remain in the manual-review table above. Every
candidate debt passes the official inclusion/exclusion screen before it enters
a total.

### Heffingsvrij vermogen

| Item                                  | Amount            | Src |
|---------------------------------------|-------------------|-----|
| Heffingsvrij vermogen (single)        | EUR [from `../nl-tax-shared-resources/knowledge/years/2026/provisional/box3-provisional.md`] | C:from_2026_table |
| Heffingsvrij vermogen (partners)      | EUR [from `box3-provisional.md`] | C:from_2026_table |
| Applied heffingsvrij vermogen         | EUR               | C:depends_on_partner_status |

### Drempel schulden

| Item                                  | Amount            | Src |
|---------------------------------------|-------------------|-----|
| Drempel schulden (single)             | EUR [from `box3-provisional.md`] | C:from_2026_table |
| Drempel schulden (partners)           | EUR [from `box3-provisional.md`] | C:from_2026_table |
| Aftrekbare schulden after threshold   | EUR               | C:debts-threshold |

### Provisional fictitious return calculation

| Step                                  | Value             | Src |
|---------------------------------------|-------------------|-----|
| Total Categorie I (banktegoeden)      | EUR               | C:above |
| Total Categorie II (overige bezittingen) | EUR            | C:above |
| Total Categorie III (schulden)        | EUR               | C:above |
| Aftrekbare schulden after threshold   | EUR               | C:above |
| Belastbaar rendement: I x [bank %] + II x [other-assets %] - aftrekbare schulden x [debt %] (2026 provisional percentages from `box3-provisional.md`) | EUR | C:formula |
| Rendementsgrondslag: I + II - aftrekbare schulden | EUR      | C:formula |
| Grondslag sparen en beleggen          | EUR               | C:formula |
| Aandeel in rendementsgrondslag        | [portal result / labeled workpack estimate] | C:formula; [2- or 3-decimal display convention recorded] |
| **Box 3 income**                      | EUR (estimate/from-baseline) | C:formula |
| Box 3 tax rate                        | [from `box3-provisional.md`] | C:from_2026_table |
| **Box 3 tax**                         | EUR (estimate/from-baseline) | C:formula |

The official 2026 publication says 3 decimals in the general instruction but
uses 2 decimals in its worked examples. Do not claim either display convention
is the binding portal algorithm; the live portal calculation and resulting
beschikking are authoritative.

## Deductions estimate

### Estimated alimentatie 2026

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Alimentatie (alimony)                 | EUR               | [F/U/A/B/?] |

### Estimated other deductions 2026

| Item                                  | Amount / handling | Src |
|---------------------------------------|-------------------|-----|
| Lijfrentepremie                       | [estimate; lijfrente limit manual review unless exact reviewed sources and required inputs are present] | [F/U/A/B/?] |
| Arbeidsongeschiktheidsverzekering     | [estimate] | [F/U/A/B/?] |
| Specific care costs                   | [estimate; zorgkosten threshold manual review unless exact reviewed sources and required inputs are present] | [F/U/A/B/?] |
| Gifts (giften)                        | [estimate] | [F/U/A/B/?] |
| Other deductible expenses             | [estimate/manual review] | [F/U/A/B/?] |
| **Total other deductions**            | [estimate/manual review] | C:sum |

### Fiscal-partner allocation

[If no fiscal partner in 2026: "Not applicable -- no fiscal partner."]

| Item | Scenario A | Scenario B | Estimated effect vs Scenario A | Src |
|------|------------|------------|--------------------------------|-----|
| [joint item, e.g. own-home balance / Box 3 grondslag / other deductions] | [taxpayer %] / [partner %] | [taxpayer %] / [partner %] | EUR [estimate] | [C/U/?] |

Taxpayer-selected allocation: [not selected / user-confirmed split] -- Src: [U/?]

Scenarios are traceable comparisons only; none is ranked, recommended, or
selected automatically. Both partners choose the split; until they explicitly
do, the allocation stays unresolved. The official portal calculation is binding.

## Change subflow — full re-entry reminder

[For the **change** subflow only. For request / review / stopzetten, replace this section's body with an explicit "N/A — not applicable for this subflow" line; do not omit the heading.]

> Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

The portal may offer to pre-fill figures from the most recent annual return; it
does not carry forward the current voorlopige-aanslag figures. Whether the form
opens blank or pre-filled, you (the taxpayer) verify every applicable category.

## Open questions

[Every question still awaiting your answer, including deferred ones. Q-IDs are
stable: never renumber, and reuse the same Q-ID when a deferred question is
asked again. Remove a row once its answer is recorded in its section. Appendix
A lists the same Q-IDs under each section's `open`. The field mapper adds its
own rows for mapping gaps, continuing the Q001 numbering, so every field-map
`open_question_id` resolves here.]

| Q-ID | Section | Question | Blocking | Status |
|------|---------|----------|----------|--------|
| [Q001] | [section key, e.g. `income_employment`] | [question] | [yes/no] | [open / deferred] |

[If none: "None -- no open questions."]

## Missing information

[Every row with `Src: ?` appears here, linked to its open Q-ID when one
exists. Do not include annual 2025 items. The field mapper adds its own rows
for missing mapped values, continuing the M001 numbering.]

| M-ID | Description | Workpack row | Q-ID | How to resolve |
|------|-------------|--------------|------|----------------|
| [M001] | [description] | [section/row] | [Q-ID / none] | [how you can provide it] |

Total missing items: [count]

## Assumptions

[Only assumptions you explicitly accepted. Every row with `Src: A:<id>` appears
here.]

| A-ID | Description | Accepted by taxpayer | Impact if incorrect | Resolution |
|------|-------------|----------------------|---------------------|------------|
| [A001] | [what was assumed] | [U:"<short quote>" (<YYYY-MM-DD>)] | [what changes if wrong] | [how to confirm] |

Total assumptions: [count]

[If none: "None -- no assumptions were used."]

All amounts are estimates unless explicitly tagged `B:` (baseline/from-baseline).

## User-stated values index

[Cross-index every `U:` row so you can spot-check what was recorded from chat.]

| Workpack row | Value | Quote | Stated at | Document row |
|--------------|-------|-------|-----------|--------------|
| [section/row] | [value] | "[verbatim quote]" | [YYYY-MM-DD] | [ev_NNN] |

## Field map summary

[Written by the field mapper for request/change. Until mapping runs: "not yet
mapped". For review/stopzetten: "N/A — no field map is produced for this
subflow." Once mapping has run, every manual-entry field in Appendix B appears
here with the same value, and every missing field appears as a `MISSING -
enter manually` row with its Q-ID. If a sourced fact changes after generation,
the provisional workflow adds the line `STALE — predates the change to <fact>
(<YYYY-MM-DD>); regenerate before use.` at the top of this section, of
Appendix B, and of a requested checklist; only regeneration, which re-runs the
field mapper, removes it.]

not yet mapped

## Manual-entry checklist

[Written only when you ask for a manual-entry checklist. A checklist that
carries the stale line is never used until the map is regenerated and the
checklist rebuilt.]

not requested

## Human review checklist

The taxpayer or an authorized human completes this review. Any authenticated
portal check or action is performed personally, never by the assistant.

- [ ] All income estimates are reasonable and based on current knowledge
- [ ] Expected business profit, when applicable, is included in the Box 1 rollup and change delta rather than only shown in a side section
- [ ] The business estimate was recorded as the winst before ondernemersaftrek and before MKB-winstvrijstelling, excluding btw, with a minus sign for an expected loss
- [ ] The rollover check was completed for an automatically extended or pre-filled 2026 voorlopige aanslag
- [ ] The separate voorlopige aanslag Zorgverzekeringswet was raised, with its own change route, no bijdrage amount, and no Zvw field or value inside the income-tax dataset
- [ ] Deduction estimates are based on the current situation for 2026
- [ ] AOW status uses below_all_year / reaches_during_year / aow_all_year; a transition month uses the manual portal result
- [ ] IACK, ouderenkorting, alleenstaandeouderenkorting, and jonggehandicaptenkorting reviewed manually unless exact reviewed sources are registered; alleenstaandeouderenkorting is based on a single-person AOW pension entitlement, not single-parent status
- [ ] Zorgkosten threshold manual review completed if relevant
- [ ] Lijfrente limit manual review completed if relevant
- [ ] Box 2 estimates are labeled estimate or from-baseline, if applicable
- [ ] Box 3 assets reflect the position as of 1 January 2026
- [ ] Box 3 debts passed the official inclusion/exclusion screen; unresolved debts stay outside accepted totals
- [ ] Box 3 rounding display notes the published 3-decimal/2-decimal inconsistency and defers to the portal/beschikking
- [ ] Box 3 uses the provisional fictitious method
- [ ] For change subflow: all data has been entered, not just the changed items
- [ ] All `U:` user-chat values reviewed for accuracy
- [ ] All `A:` assumptions reviewed and confirmed or corrected
- [ ] All `?` missing information resolved or consciously accepted
- [ ] Partner data is correct (if applicable)
- [ ] Allocation scenarios are traceable and the taxpayer-selected split is
  recorded with `U:` provenance, or the allocation remains unresolved (if
  fiscal partners); no scenario was ranked or automatically selected

## Not submission advice

This workpack is a preparation aid. You, the taxpayer or an authorized human,
must review the figures and perform all portal entry, signing, sending, or
changes yourself. The assistant must not access or operate Mijn
Belastingdienst.

## Appendix A — Resume record

[One fenced `yaml` block. `save_consent` defaults to `not_given` and becomes
`given` in the written file (saved in the working folder or delivered as a
download); it is a record of your decision in the conversation, never an
authorization to write. Shown in the conversation, the workpack omits both
appendices.]

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.6.0"
workflow: provisional_2026_request   # provisional_2026_request | provisional_2026_change | provisional_2026_review | provisional_2026_stopzetten
tax_year: 2026
created_at: ""                       # ISO 8601
updated_at: ""
save_consent: not_given              # not_given in the template; given in the written file
readiness: draft                     # draft | review_ready (derived from the section rollup)
generation_confirmed: false          # true after the final-review confirmation
queued_workflow: null
sections:                            # keep only the keys that apply to the subflow
  baseline: {status: not_started, open: []}                 # change / review / stopzetten
  income_employment: {status: not_started, open: []}        # request / change / review
  income_pension_benefit: {status: not_started, open: []}   # request / change / review
  income_other: {status: not_started, open: []}            # request / change / review
  winst_forecast: {status: not_started, open: []}          # request / change / review
  deductions: {status: not_started, open: []}              # request / change / review; includes own home
  box2: {status: not_started, open: []}                    # request / change / review
  box3_peildatum: {status: not_started, open: []}          # request / change / review
  partner_allocation: {status: not_started, open: []}      # request / change / review
  stopzetten_direction: {status: not_started, open: []}    # stopzetten
  confirm: {status: not_started, open: []}                 # all
sources_loaded: []                   # equals Sources used; provisional 2026 only
```

Status values: `not_started | in_progress | complete | chat_only | deferred`.
`open` lists the open question IDs from Open questions. Facts never live in
this record; they live in the sections above with provenance.

## Appendix B — Field map

not yet mapped
