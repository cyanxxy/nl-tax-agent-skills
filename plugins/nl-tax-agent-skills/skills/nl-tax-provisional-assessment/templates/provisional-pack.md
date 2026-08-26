# Voorlopige Aanslag Workpack — 2026

> **Provenance convention.** Every numeric line in this workpack records its source in a `Src` column or inline `Src:` note.
> Source codes:
> - `F:<evidence_id>` -- value from a file in the evidence index, such as a beschikking
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat
> - `A:<assumption_id>` -- confirmed assumption, also listed under Assumptions
> - `B:<baseline_ref>` -- value carried over from the existing voorlopige aanslag baseline
> - `?` -- required but still missing, also listed under Missing information
> - `C:<formula>` -- computed from other sourced rows
>
> All amounts are estimates unless explicitly tagged `B:` as baseline/from-baseline. A row marked `?` is never silently treated as zero.

## Contents

- Subflow: [request/change/review/stopzetten]
- Scope
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
- Change subflow — full re-entry reminder (change subflow only)
- Field map summary
- User-stated values index
- Missing information
- Assumptions
- Human review checklist
- Not submission advice

## Subflow: [request/change/review/stopzetten]

## Scope

| Field            | Value                                |
|------------------|--------------------------------------|
| Tax year         | 2026                                 |
| Workflow         | Voorlopige aanslag ([subflow])       |
| Taxpayer         | [from profile]                       |
| Fiscal partner   | [yes/no]                             |
| Created          | [timestamp]                          |

## Sources used

[List exactly the source IDs from
`workspace/shared/session-progress.yaml` ->
`sources_loaded_by_workflow.provisional_2026`; do not copy the annual ledger.
An ID used by both appears here only if consulted independently for provisional
2026]

- [source_id_1]
- [source_id_2]
- [source_id_n]

## Existing baseline, if any

An **unsolicited** VA based on earlier data **may be issued**, but is **not guaranteed**. Record an EVA only when it actually exists in the evidence or is confirmed by the taxpayer.

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
| AOW status in 2026 | [below_all_year / reaches_during_year / aow_all_year] | [profile/calculated/?] |
| AOW transition month | [1..12 / N/A] | [profile/calculated/?] |
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

[For change: see workspace/provisional/2026/delta-summary.md for full baseline vs current estimates comparison]

[For request: "N/A — new request"]

[For review: see workspace/provisional/2026/review-questions.md for items requiring verification]

[For stopzetten: "N/A — stopzetten does not require a delta calculation"]

## Review questions

[For review: see workspace/provisional/2026/review-questions.md. Summarize the total counts by status and recommended action here.]

[For request/change/stopzetten: "N/A — not applicable for this subflow"]

## Stopzetten outcome

[For stopzetten only. For request/change/review, replace this section's body with "N/A — not applicable for this subflow"; do not omit the heading.]

If the taxpayer is **moving abroad**, record: "Residency review required; moving abroad is **not a categorical stopzetten reason**." Route to the unsupported residency/migration path and do not emit a refund-stop checklist solely because of the move.

### Current-date cutoff gate

| Item | Value | Src |
|------|-------|-----|
| Current date used for cutoff | [YYYY-MM-DD] | [system/user] |
| Stopzetten cutoff | 2026-10-01 | C:bd_provisional_stopzetten_2026 |
| Cutoff result | [before cutoff / cutoff passed] | C:date_compare |

If the current date is on or after 2026-10-01, do not generate a stopzetten checklist. State that the 2026 stopzetten cutoff has passed and route the user to review/change or to a separate filing-status review and, when a return will be filed, annual settlement.

### Cash-flow direction and route

| Item | Value | Src |
|------|-------|-----|
| Current monthly direction | [refund / payment / unknown] | [F/U/?] |
| Route chosen | [stop refund / change VA / no action] | C:decision |
| Reason | [short reason] | [F/U/C] |
| Refund component | [deductions / IACK / algemene heffingskorting / unknown] | [F/U/?] |
| Effective date | [2026-01-01 / selected first day of month / unknown] | [F/U/C/?] |
| Amount already received in 2026 | EUR [amount / unknown] | [F/U/?] |
| Separate repayment notice | [expected for paid deductions/IACK / not applicable / unresolved] | C:review |
| 2026 annual filing status | [required / not required / unresolved / plans to file] | [F/U/?] |

### Refund-stop checklist

[Include only when the taxpayer receives a monthly refund and the current-date cutoff gate is before 2026-10-01.]

> **HUMAN-ONLY PORTAL STEPS.** The taxpayer or an authorized human performs any
> authenticated portal action below personally. The assistant must not open or
> operate the portal, click controls, confirm, send, or submit.

- [ ] I confirmed the current VA pays a monthly refund
- [ ] I confirmed the current date is before 2026-10-01
- [ ] I identified whether the selected refund concerns deductions, IACK, or the algemene heffingskorting
- [ ] For deductions/IACK: I confirmed the effect is retroactive to 1 January 2026 and prior payments may be reclaimed in a separate notice
- [ ] For algemene heffingskorting: I confirmed the selected first day of a month and prospective payment effect from that selected/next payment month
- [ ] I checked the 2026 annual filing obligation separately; stopzetten itself does not make filing universally required
- [ ] I used the official Mijn Belastingdienst stopzetten form personally for my 2026 monthly refund
- [ ] I kept the confirmation for my records

### Payment-case redirect

[Include only when the taxpayer pays monthly and the amount is wrong.]

Stopping payments does not reduce the tax obligation. Route to the change subflow and carry the payment baseline forward there; do not include the refund-stop checklist.

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

[Repeat or reference the sourced `onderneming.geschatte_winst` forecast above.
If not applicable, state that explicitly. Preserve manual review and do not
include annual deduction or final-tax calculations.]

Definition confirmed with the taxpayer before the amount was recorded: the winst
expected as ondernemer in 2026, **before** the ondernemersaftrek and **before**
the MKB-winstvrijstelling, excluding the btw payable and the btw reclaimable,
with a minus sign for an expected loss. It is the only business figure the 2026
form asks for; the Belastingdienst applies the ondernemersaftrek and the
MKB-winstvrijstelling itself. Every 2026 business figure is read from
`_shared/knowledge/years/2026/provisional/winst-provisional-2026.md`.

### Rollover check

| Item | Value | Src |
|------|-------|-----|
| 2026 voorlopige aanslag extended automatically or opened pre-filled | [yes / no / unknown] | [F/U/?] |
| Year whose figures the current 2026 voorlopige aanslag rests on | [year / unknown] | [F/U/?] |
| Profit estimate the current 2026 voorlopige aanslag uses | EUR [amount / unknown] (from-baseline) | [F/U/B/?] |
| Still the taxpayer's own best estimate for 2026 | [yes / no / unknown] | [F/U/?] |
| Reasoning still uses an earlier year's zelfstandigenaftrek | [yes / no / unknown] | [F/U/?] |
| Finding | [carried-over zelfstandigenaftrek above the 2026 amount in `winst-provisional-2026.md` / no rollover issue found / unresolved] | C:review |

A carried-over zelfstandigenaftrek above the 2026 amount overstates the
deduction, so too little is paid through the year and the difference is owed
when the final 2026 assessment is made up. Leave an unanswered row as `?` and
list it under Missing information; never assume and never enter a zero. A change
made to the voorlopige aanslag 2025 after the cut-off date stated in
`winst-provisional-2026.md` is not carried into 2026 automatically.

### Zvw companion -- separate voorlopige aanslag Zorgverzekeringswet

[Required whenever there is winst uit onderneming or income from work performed
outside employment. Otherwise state "N/A -- no winst uit onderneming or income
from work outside employment reported."]

| Item | Value | Src |
|------|-------|-----|
| Voorlopige aanslag Zorgverzekeringswet 2026 received | [yes / no / unknown] | [F/U/?] |
| Income estimate that voorlopige aanslag Zvw uses | EUR [amount / unknown] (from-baseline) | [F/U/B/?] |
| Still matches the taxpayer's own 2026 expectation | [yes / no / unknown] | [F/U/?] |
| Handling | separate aanslag, separate change route -- manual review | C:review |

You (the taxpayer) receive two aanslagen: one for the inkomstenbelasting/premie
volksverzekeringen and a separate one for the bijdrage Zorgverzekeringswet. At
this stage there can be two voorlopige aanslagen, with separate change routes.
Whether a change to the income-tax voorlopige aanslag is coupled to the Zvw
assessment is not established in the reviewed sources. You therefore check the
Zvw assessment separately, and this workpack records what you find.

- [ ] You (the taxpayer) also check your voorlopige aanslag Zorgverzekeringswet
  2026 in Mijn Belastingdienst and change it through its own route if its
  estimate is no longer right.

The Zvw base is the belastbare winst -- a different figure from
`onderneming.geschatte_winst`, which is taken before the ondernemersaftrek and
the MKB-winstvrijstelling. The bijdrage is not deductible and is never
subtracted from the profit estimate. This section reports the Zvw alongside the
income-tax dataset and never inside it: no bijdrage amount, no Zvw row in the
income-tax form, and no Zvw instalment, deadline, payment, or refund timing.
Percentages and the maximumbijdrage-inkomen are read from
`_shared/knowledge/years/2026/provisional/zvw-provisional-2026.md`; the
Belastingdienst calculates the bijdrage.

The income-tax field map contains no Zvw field or value: no Zvw `field_id`,
label, note, amount, baseline, estimate, or manual-entry row.

### Estimated tax credits

| Credit area                           | Handling | Src |
|---------------------------------------|----------|-----|
| Algemene heffingskorting              | [portal estimate / source-backed estimate / manual review] | [C/F/U/A/?] |
| Arbeidskorting                        | [portal estimate / source-backed estimate / manual review] | [C/F/U/A/?] |
| IACK                                  | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Ouderenkorting                        | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Alleenstaandeouderenkorting           | [manual review of entitlement to an AOW pension for a single person; never infer from single-parent status or children] | [F/U/A/?] |
| Jonggehandicaptenkorting              | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |

Do not show calculated credit amounts unless exact reviewed sources are registered and all required taxpayer facts are available.

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

[If no aanmerkelijk belang: "Not applicable -- no substantial interest (aanmerkelijk belang) reported."]

| Item | Amount label | Src |
|------|--------------|-----|
| Estimated regular benefits, including dividends (`box2.geschatte_reguliere_voordelen`) | EUR [amount] (estimate/from-baseline) | [F/U/A/B/?] |
| Estimated disposal benefits (`box2.geschatte_vervreemdingsvoordelen`) | EUR [amount] (estimate/from-baseline) | [F/U/A/B/?] |
| Estimated costs (`box2.geschatte_kosten`) | EUR [amount] (estimate/from-baseline) | [F/U/A/B/?] |
| Estimated dividend withholding tax (`box2.geschatte_ingehouden_dividendbelasting`) | EUR [amount] (estimate/from-baseline) | [F/U/A/B/?] |
| Estimated fictitious regular benefit from BV lending (`box2.geschat_fictief_regulier_voordeel_bv_lening`) | EUR [amount] (estimate/from-baseline/manual review) | [F/U/A/B/?] |
| Fiscal-partner Box 2 allocation (`partner.verdeling_box2_inkomen`) | [taxpayer %] / [partner %] (estimate/from-baseline) | [U/B/?] |

Manual review / unsupported triggers: valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA issues.

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

Check trail: `check_performed_by: "[checked_by_agent | checked_by_script]"`.
The manual path and optional script apply the same row checks. Preserve this
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
out, and unresolved debts remain in the manual-review table above.

### Heffingsvrij vermogen

| Item                                  | Amount            | Src |
|---------------------------------------|-------------------|-----|
| Heffingsvrij vermogen (single)        | EUR [from `_shared/knowledge/years/2026/provisional/box3-provisional.md`] | C:from_2026_table |
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

## Change subflow — full re-entry reminder

[For the **change** subflow only. For request / review / stopzetten, replace this section's body with an explicit "N/A — not applicable for this subflow" line; do not omit the heading.]

> Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

## Field map summary

[Reference to workspace/provisional/2026/field-map.yaml]
[This file maps each collected data point to the corresponding field in the Mijn Belastingdienst portal]
[For review: reference workspace/provisional/2026/review-questions.md instead. For stopzetten: "N/A — no field map is produced for stopzetten."]

## Missing information

[From workspace/shared/missing-info.md, filtered for provisional_2026. Every row with `Src: ?` must appear here. Do not include annual return items.]

| ID | Description | Workpack row | How to resolve |
|----|-------------|--------------|----------------|
| [MI-001] | [description] | [section/row] | [how the user can provide it] |

## Assumptions

[From workspace/shared/assumptions.md, filtered for provisional_2026. Every row with `Src: A:<id>` must appear here.]

| Assumption ID | Description | Confirmed by user | Impact if incorrect |
|---------------|-------------|-------------------|---------------------|
| [A001] | [what was assumed] | [yes/no] | [what changes if wrong] |

All amounts are estimates unless explicitly tagged `B:` (baseline/from-baseline).

## User-stated values index

[Cross-index every `U:` row so the user can spot-check what was recorded from chat.]

| Workpack row | Value | Quote | Stated at |
|--------------|-------|-------|-----------|
| [section/row] | [value] | "[verbatim quote]" | [YYYY-MM-DD] |

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
- [ ] Box 3 comparison scenarios are traceable and the taxpayer-selected split
  is recorded with `U:` provenance, or the allocation remains unresolved (if
  fiscal partners); no scenario was ranked or automatically selected

## Not submission advice

This workpack is a preparation aid. You, the taxpayer or an authorized human,
must review the figures and perform all portal entry, signing, sending, or
changes yourself. The assistant must not access or operate Mijn
Belastingdienst.
