# Annual Income-Tax Return Workpack -- 2025

> **STATUS: {DRAFT — N deferred section(s) | COMPLETE DRAFT FOR REVIEW} — not for filing.** Replace `N` with the number of applicable sections still deferred, incomplete, or carrying `?` rows; use "COMPLETE DRAFT FOR REVIEW" only when every applicable section is `complete` or `chat_only` and no blocking open question remains. This workpack is never submission advice; filing always happens manually via Mijn Belastingdienst.

> **Provenance convention.** Every numeric line in this workpack records its source in a `Src` column or inline `Src:` note.
> Source codes:
> - `F:<evidence_id>` -- value taken from a document row (`ev_NNN`) in Documents and sources
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat, also listed in the User-stated values index
> - `A:<assumption_id>` -- assumption the taxpayer explicitly accepted, also listed under Assumptions
> - `?` -- required but still missing, also listed under Missing information
> - `C:<formula>` -- computed from other sourced rows
>
> A row marked `?` is never silently treated as zero. It blocks finalization until resolved or explicitly accepted as missing. A `profile.<key>` reference in a `Src` cell points to that row of the Taxpayer profile summary, which carries its own provenance.

[Fill note: a tax section the conversation has not reached yet holds the single
line `Not yet reviewed.` This differs from a "Not applicable" line, which
records a sourced answer. Remove every bracketed fill note from the filled
workpack. Shown in the conversation, the workpack holds only filled sections:
no fill notes, no bracketed instructions, and no Appendix A or Appendix B
YAML.]

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
Taxpayer: [the taxpayer, or a label the taxpayer chose; no name, BSN, or IBAN needed]
Fiscal partner: [yes/no] -- Src: profile.partner.has_fiscal_partner
Created: [timestamp]

## Unsupported-case checks

- [ ] Full-year Dutch resident: [yes/no]
- [ ] Individual taxpayer -- non-business individual or recognised IB business form: [yes/no]
- [ ] Living taxpayer: [yes/no]
- [ ] No M-biljet required: [yes/no]
- [ ] No complex Box 2 manual-review trigger blocking standard preparation: [yes/no/not applicable]

If residency, individual-taxpayer status, living status, or M-biljet check is
"no", this workpack should not have been generated. A recognised complex
business form is different: keep this workpack active, prepare unaffected
sections, and leave the blocked business figure unresolved as described below.

A terminal business-computation trigger (samenwerkingsverband profit share and
KIA apportionment, medegerechtigde loss caps, DGA/BV winst, agrarisch,
zeevarende, stakingswinst, herinvesteringsreserve, oudedagsreserve wind-down,
terbeschikkingstelling) is **not** a whole-case exclusion and does not stop this
workpack. It blocks one figure. Prepare the rest of the return, name the blocked
figure, route only that figure to manual review, and keep the business field map
`draft` with the `business-section schema review` blocker:

- [ ] Terminal business-computation trigger present: [no / yes -- blocked figure named below]

## Taxpayer profile summary

[The screened facts from the start of the conversation, one row per fact with
its provenance. The `Key` column is stable so the field map's
`source.profile_path` can point to a row. No name, BSN, or IBAN is needed; do
not record them.]

| Key | Value | Src |
|-----|-------|-----|
| `residency.full_year_nl_resident` | [yes/no] | [F/U/A/?] |
| `taxpayer.type` | [individual / individual with a recognised IB business form] | [F/U/A/?] |
| `taxpayer.primary_income_type` | [employment / pension / benefit / business / combination] | [F/U/A/?] |
| `person.date_of_birth` | [date] | [F/U/A/?] |
| `person.aow_by_tax_year.2025.status` | [below_all_year / reaches_during_year / aow_all_year] | [C:aow_rule(person.date_of_birth) / F/U/?] |
| `person.aow_by_tax_year.2025.transition_month` | [1..12 / n/a] | [C/F/U/?] |
| `person.aow_by_tax_year.2025.single_person_pension_entitlement` | [yes / no / unresolved / n/a] | [F/U/?] |
| `partner.has_fiscal_partner` | [yes/no] | [F/U/A/?] |
| `partner.partner_date_of_birth` | [date / n/a] | [F/U/A/?] |
| `partner.aow_by_tax_year.2025.status` | [below_all_year / reaches_during_year / aow_all_year / n/a] | [C/F/U/?] |
| `partner.aow_by_tax_year.2025.transition_month` | [1..12 / n/a] | [C/F/U/?] |
| `household.children_at_home_count` | [count on 31 Dec 2025] | [U/A/?] |
| `household.children` | [dates of birth for the IACK age test on 1 Jan 2025 / n/a] | [U/A/?] |
| `household.single_parent_status` | [yes/no] | [U/A/?] |
| `box2.has_aanmerkelijk_belang` | [yes/no] | [F/U/A/?] |
| `routing.complex_box2_screening` | [standard / manual_review / not applicable] | [U/?] |
| `business.has_onderneming` | [yes/no] | [F/U/A/?] |
| `business.legal_form` | [eenmanszaak / vof / maatschap / cv / bv / other / n/a] | [F/U/A/?] |
| `routing.complex_business_screening` | [standard / manual_review / not applicable] | [U/?] |
| `special_circumstances` | [any manual-review flags from screening / none] | [U/?] |

## Documents and sources

[Every document or chat value used, one row each. Assign the next unused
`ev_NNN` and never renumber. Name each document as the taxpayer named it and use
a canonical type from the shared evidence-types reference. A chat value is
named `chat YYYY-MM-DD`, has type `user_chat`, and carries its short quote
under "Values taken". Record no file hashes, no full BSN, IBAN, policy,
contract, or aanslag number, and no content beyond the short quote needed for
provenance.]

| ID | Document | Type | Tax year | Owner | Location | Values taken | Status |
|----|----------|------|----------|-------|----------|--------------|--------|
| ev_001 | [name as given by the taxpayer] | [evidence type] | [2025] | [taxpayer / partner / joint] | [page / section] | [field: EUR amount; ...] | [extracted / needs review] |

[If nothing has been used yet: "None yet."]

## Sources used

[Emit exactly the reviewed `source_id`s consulted for this annual workflow, one
per line, identical to `sources_loaded` in Appendix A. Do not pad with sources
that were not consulted, omit consulted annual sources, or include provisional
source IDs.]

- [source_id]
- [source_id]

## Filing status and late-filing exposure

[From the filing-status answers given in the conversation. First emit one route
label: `invited`, `no_letter_but_mandatory`, `refund_claim_only`, or
`filing_obligation_unresolved`. These labels report reviewed facts; they do not
automatically decide a filing obligation. Then render only the applicable
timing/exposure lines below.]

- Filing-route label: [one of the four labels] -- Src: [F/U/C]
- Official result before submission: [EUR amount to pay; mandatory no-letter
  threshold EUR 58 / EUR amount back; refund-claim threshold EUR 19 /
  unresolved] -- Src: [official portal result / U/?]
- No-letter asset/scheme test: [not applicable / mandatory because both
  elements confirmed / unresolved] -- Src: [U/F/?]

### On time

Filing status: on time. No late-filing penalty exposure. This does not promise
zero belastingrente: it can still apply if the return was received on or after
1 May or the Belastingdienst deviates from the filed return.

### Uitstel granted

- Granted uitsteldatum: [YYYY-MM-DD] -- Src: [U/F]
- Belastingrente still accrues from 1 July 2026 if tax is owed on the eventual aanslag.
- Belastingrente rate from 1 January 2026: [rate from `late-filing.md`] -- Src: bd_belastingrente_overview

### Late (deadline passed, no uitstel)

- Deadline route: [invited / no_letter_but_mandatory / not established] -- Src: [F/U/C]
- Applicable deadline: [date from invitation letter / 14 July 2026 / not established] -- Src: [F/U/C]
- Deadline status: [passed / not established] -- Src: C:deadline_route
- Filing status: [outstanding / not established] -- Src: [U/C]

Render this late-exposure subsection only when an applicable deadline is
established and has passed without granted uitstel. With no invitation, use
14 July 2026 only for `no_letter_but_mandatory`. A refund-only or unresolved
route is not classified as late.
- Invited-return verzuimboete — **potential exposure**, render only for
  `invited`:
  - Herinnering received: [yes / no / unknown] -- Src: [F/U/?]
  - Aanmaning received: [yes / no / unknown] -- Src: [F/U/?]
  - 10 werkdagen after aanmaning expired while still unfiled: [yes / no / unknown] -- Src: [F/U/C/?]
  - Potential first-time amount after the full escalation: EUR [amount from `late-filing.md`] -- Src: bd_verzuimboete
  - Potential repeated amount after the full escalation: up to EUR [maximum from `late-filing.md`] -- Src: bd_verzuimboete
  - Missing the filing deadline alone does not impose the boete; exposure is conditional on the herinnering, aanmaning, and 10 werkdagen sequence.
- No-letter failure-to-request exposure — **potential exposure**, render only
  for `no_letter_but_mandatory`:
  - Aangifte requested: [yes / no / unknown] -- Src: [F/U/?]
  - Request date: [date / unknown] -- Src: [F/U/?]
  - Official timing facts: 6 months after the tax liability arose; no penalty
    when requested within the following 2 weeks -- Src: bd_verzuimboete
  - Potential amount: EUR 3,354 -- Src: bd_verzuimboete
  - Do not apply the invited-return herinnering/aanmaning sequence here; the
    Belastingdienst determines whether this separate regime applies.
- Belastingrente:
  - Can apply when the return is received on or after 1 May, or when the
    Belastingdienst deviates from the filed return, even if filed before 1 May
  - Normally starts 1 July 2026 when tax is owed and an interest ground applies
  - Rate from 1 January 2026: [rate from `late-filing.md`] -- Src: bd_belastingrente_overview
- Recommended next steps:
  - **Taxpayer:** File the prepared return through Mijn Belastingdienst as soon as possible.
  - **Taxpayer:** Track any herinnering and aanmaning, file immediately, and do not assume that a verzuimboete will be imposed.
  - **Taxpayer:** Pay the aanslag by its due date (betaaltermijn) to avoid invorderingsrente. Belastingrente is already fixed on the aanslag and is not reduced by paying faster.
- The Belastingdienst determines whether the escalation conditions are met and sets any actual boete and rente. This workpack does not compute or promise final figures.

## Income notes

### Employment income (loon uit dienstbetrekking)

| Employer | Loon / fiscaal loon (copied exactly) | Loonheffing withheld | Src (fiscaal loon) | Src (loonheffing) |
|----------|--------------|----------------------|-------------|-------------------|
| [name]   | EUR [amount] | EUR [amount]         | [F/U/A/?]   | [F/U/A/?]         |

[Add rows for each employer. If no employment income, state "Not applicable -- no employment income reported."]

### Pension income

[Use the **payment-year pension statement** for gross taxable pension and
withholding. A UPO is **accrual or projection context only** and is not
payment-year evidence.]

| Provider | Type | Gross pension | Loonheffing withheld | Src (gross) | Src (loonheffing) |
|----------|------|---------------|----------------------|-------------|-------------------|
| [name]   | [employer pension / AOW] | EUR [amount] | EUR [amount] | [F/U/A/?] | [F/U/A/?] |

[Add rows for each pension provider. If no pension income, state "Not applicable."]

### Benefit income (uitkeringen)

[AKW is **not taxable box 1 income**; if relevant, record it as household
context outside the taxable total. For ZW (Ziektewet) and WAZO, the
arbeidskorting outcome is **conditional** and depends on the employment
relationship (dienstbetrekking). Ask whether the taxpayer was still employed
and mark unresolved cases for manual review.]

| Provider | Benefit type | Gross amount | Loonheffing withheld | Src (gross) | Src (loonheffing) |
|----------|--------------|--------------|----------------------|-------------|-------------------|
| [UWV/SVB] | [WW/WIA/WAO/ZW/Anw] | EUR [amount] | EUR [amount] | [F/U/A/?] | [F/U/A/?] |

[Add rows for each benefit. If no benefit income, state "Not applicable."]

Non-taxable household context — AKW (kinderbijslag): [received/not received/not
relevant] -- Src: [F/U/A/?]. Do not include this line in taxable benefit or box
1 totals.

### Company car and equity-compensation review

- Company car (auto van de zaak / bijtelling): [yes/no]
- Evidence of **500 private kilometres or fewer**: [confirmed/not confirmed]
- Date of first admission and vehicle regime: [confirmed facts/missing]
- Rate handling: [only show after the first-admission, regime, emissions/fuel,
  catalogue-value, and private-use facts are confirmed; otherwise withhold the
  rate and mark manual review]
- Stock options: [yes/no]
- Tradability/default tax point: [date/evidence/manual review]. **Tradability**
  is the **default tax point**; by default, taxation follows when acquired
  shares become tradable. Immediate-tradability cases and any election to use
  exercise require the employer statement and manual review.
- Other equity compensation (RSU/restricted or employee shares/other):
  [instrument / grant-vesting-delivery-sale dates / employer statement / payroll
  treatment / manual review]. Do not apply a blanket vesting-date rule; unresolved
  or cross-border awards stay outside standard totals.

### Other box 1 income

| Description | Amount | Src |
|-------------|--------|-----|
| [e.g., alimentatie received] | EUR [amount] | [F/U/A/?] |

[If no other income, state "Not applicable." Winst uit onderneming (eenmanszaak / ZZP) is NOT recorded here -- it has its own "Winst uit onderneming notes" section below. Resultaat uit overige werkzaamheden IS prepared here, under `row-en-dba-2025.md`: record the opbrengsten and the costs that note allows, note that ondernemersaftrek, MKB-winstvrijstelling and investeringsaftrek never apply to it, and note that the bijdrage Zvw does. Route anything that note leaves open to manual review.]

### Box 1 income total

| Item | Amount | Src |
|------|--------|-----|
| Total gross employment income | EUR [amount] | C:sum(employment.gross) |
| Total gross pension income | EUR [amount] | C:sum(pension.gross) |
| Total gross benefit income | EUR [amount] | C:sum(benefit.gross) |
| Belastbare winst uit onderneming (line E of the chain below) | EUR [amount] | C:winst_chain_line_E |
| Resultaat uit overige werkzaamheden | EUR [amount] | C:row_result |
| Total other box 1 income | EUR [amount] | C:sum(other) |
| **Total box 1 income (before deductions)** | **EUR [amount]** | C:sum(rows above) |
| Total loonheffing withheld | EUR [amount] | C:sum(loonheffing) |

## Winst uit onderneming notes

[If `business.has_onderneming` is `no`, emit: `Not applicable — no business income (Src: profile.business.has_onderneming).` If applicable, load `templates/sections/winst.md` and fill that section here.]

## Own-home notes

[If the taxpayer had no eigen woning in 2025, emit: `Not applicable — no own home in 2025 (Src: <U/F>).` If applicable, load `templates/sections/own-home.md` and fill that section here.]

## Box 2 notes

[If `box2.has_aanmerkelijk_belang` is `no`, emit: `Not applicable — no substantial interest (aanmerkelijk belang) in 2025 (Src: profile.box2.has_aanmerkelijk_belang).` If applicable, load `templates/sections/box2.md` and fill that section here.]

## Box 3 notes

[The agent classifies rows from reviewed facts and the Box 3 reference. Do not
infer categories from names or keywords. Only accepted rows with a supported
category, finite non-negative value, and provenance enter the totals below.]

### Accepted rows

| ID | Description | Category | Status | Value | Provenance |
|----|-------------|----------|--------|-------|------------|
| [row id] | [description] | [banktegoeden / overige_bezittingen / schulden] | accepted | EUR [amount] | [F/U/A] |

### Rejected/manual-review rows

| ID | Description | Category | Status | Value | Provenance | Reason |
|----|-------------|----------|--------|-------|------------|--------|
| [row id] | [description] | [category/unknown] | [manual_review/rejected] | EUR [amount] | [F/U/A/?] | [why excluded] |

Check trail: `check_performed_by: "checked_by_agent"`. Preserve this
trail and both tables even when there are no rejected rows.

### Assets on peildatum (1 January 2025)

#### Banktegoeden

| Account | Bank | Balance 1 Jan 2025 | Src |
|---------|------|--------------------|-----|
| [description] | [bank name] | EUR [amount] | [F/U/A/?] |

**Total banktegoeden (category I):** EUR [amount] -- Src: C:sum

#### Overige bezittingen (investments, crypto, other)

| Asset | Type | Value 1 Jan 2025 | Src |
|-------|------|------------------|-----|
| [description] | [investments / crypto / real estate / receivables / other] | EUR [amount] | [F/U/A/?] |

**Total overige bezittingen (category II):** EUR [amount] -- Src: C:sum

### Schulden (screened qualifying Box 3 debts)

| Debt | Type | Official inclusion/exclusion check | Balance 1 Jan 2025 | Src | Status |
|------|------|------------------------------------|--------------------|-----|--------|
| [description] | [consumer / study / tax / business / other] | [qualifies / excluded / unresolved] | EUR [amount] | [F/U/A/?] | [accepted / rejected / manual review] |

**Total qualifying schulden (category III; accepted rows only):** EUR [amount] -- Src: C:sum

Do not use "all non-mortgage debts" as the classification rule. Keep excluded
and unresolved rows visible but outside the trusted total; apply the debt
threshold only to the qualifying total.

### Heffingsvrij vermogen

- Single taxpayer: EUR [from `../nl-tax-shared-resources/knowledge/years/2025/box3/fictitious.md`]
- Fiscal partners (combined): EUR [from `fictitious.md`]
- Applicable heffingsvrij vermogen: EUR [amount] -- Src: C:depends_on_partner_status

### Drempel schulden

- Single taxpayer: EUR [from `fictitious.md`]
- Fiscal partners (combined): EUR [from `fictitious.md`]
- Aftrekbare schulden after threshold: EUR [amount] -- Src: C:debts-threshold

### Fictitious return calculation notes

| Step | Description | Amount | Src |
|------|-------------|--------|-----|
| 1 | Category I total (banktegoeden) | EUR [amount] | C:row above |
| 2 | Category II total (overige bezittingen) | EUR [amount] | C:row above |
| 3 | Category III total (schulden) | EUR [amount] | C:row above |
| 4 | Aftrekbare schulden after threshold | EUR [amount] | C:debts-threshold |
| 5 | Belastbaar rendement: I x [bank %] + II x [other-assets %] - aftrekbare schulden x [debt %] (2025 percentages from `fictitious.md`) | EUR [amount] | C:formula |
| 6 | Rendementsgrondslag: I + II - aftrekbare schulden | EUR [amount] | C:formula |
| 7 | Grondslag sparen en beleggen: rendementsgrondslag - heffingsvrij vermogen | EUR [amount] | C:formula |
| 8 | Aandeel in rendementsgrondslag: grondslag / rendementsgrondslag | [percentage]% | C:formula |
| 9 | Box 3 income: belastbaar rendement x aandeel | EUR [amount] | C:formula |
| 10 | Box 3 tax: box 3 income x [box 3 rate from `fictitious.md`] | EUR [amount] | C:formula |

### Actual return (werkelijk rendement) data collection

[Collect the following data for the actual return comparison. If data is not available, mark Src `?` and list the gap under Missing information.]

| Income type | Amount 2025 | Src | Status |
|-------------|-------------|-----|--------|
| Interest received (bank accounts) | EUR [amount] | [F/U/A/?] | [collected / missing] |
| Dividends received (before withholding tax) | EUR [amount] | [F/U/A/?] | [collected / missing] |
| Rental income and other box 3 income | EUR [amount] | [F/U/A/?] | [collected / missing] |
| Value changes for disposed box 3 assets | EUR [amount] | [F/U/A/?] | [collected / missing] |
| Value changes for retained or acquired box 3 assets | EUR [amount] | [F/U/A/?] | [collected / missing] |
| Interest paid on box 3 debts | EUR [amount] | [F/U/A/?] | [collected / missing] |
| Qualifying WOZ-value investment correction | EUR [amount] | [F/U/A/?] | [not applicable / collected / missing] |
| **Total actual return** | **EUR [amount]** | C:sum | |

Do not deduct custody fees, transaction costs, management fees, maintenance costs, or adviser fees from actual return.

[Actual-return (`box3_actual`) section status: `complete` when all required inputs are
available with document evidence; `chat_only` when the complete input set was
supplied in chat; also `complete` with `not supplied by choice` when the taxpayer
explicitly declines this additional data collection. A declined comparison is not a
gap. Use `deferred/manual review` only for required facts still missing after
the taxpayer requested the comparison. Cross-index all `U:` inputs. If deferred,
retain both method explanations and list the unresolved inputs. Do not imply
that both calculations were completed.]

### Comparison: fictitious vs actual

| Method | Box 3 income | Box 3 tax (at [box 3 rate from `fictitious.md`]) | Src | Data status |
|--------|-------------|-------------------|-----|-------------|
| Fictitious return (forfaitair rendement) | EUR [amount] | EUR [amount] | C:fictitious_rows | Complete |
| Actual return (werkelijk rendement) | [EUR amount / Not supplied by choice] | [EUR amount / Not calculated] | [C:actual_return_rows / U] | [Complete / Partial / Not supplied by choice] |

More favorable portal calculation: [fictitious / actual / not compared because actual data was not supplied / cannot determine -- data incomplete]

Note: If actual-return data is supplied, Mijn Belastingdienst performs both
calculations and uses the more favorable amount. The workpack comparison is
informational; it does not make a tax-method election or override the portal.

### Partner allocation for box 3

[If no fiscal partner: "Not applicable -- no fiscal partner."]

[If fiscal partner:]

| Scenario | Taxpayer % | Partner % | Estimated taxpayer tax | Estimated partner tax | Estimated combined tax | Difference vs Scenario A | Sources / assumptions |
|----------|-------------|-----------|------------------------|-----------------------|------------------------|--------------------------|-----------------------|
| Scenario A | 50% | 50% | EUR [amount] | EUR [amount] | EUR [amount] | EUR 0 | [C/U/A/?] |
| Scenario B | [X]% | [Y]% | EUR [amount] | EUR [amount] | EUR [amount] | EUR [signed amount] | [C/U/A/?] |

Taxpayer-selected allocation: [not selected / user-confirmed split] -- Src: [U:?]

Do not rank, recommend, or automatically select a scenario. The taxpayers
choose after reviewing the traceable estimates and the official filing result.

Note: The allocation percentage applies to the entire box 3 base (assets minus debts). Partners cannot allocate asset-by-asset. Both partners must use the same ratio in their respective returns.

## Deductions notes

### Alimentatie

[If not applicable: "Not applicable -- no partneralimentatie payments."]

- Total partneralimentatie paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Basis: [court order / divorce or cohabitation agreement / notarial deed /
  urgent moral obligation enforceable in court / unresolved] -- Src: [F/U/A/?]
- Enforceability review: [confirmed from evidence / manual review required]

Note: Kinderalimentatie (child maintenance) is NOT deductible.

### Zorgkosten (specific medical expenses)

[If not applicable: "Not applicable -- no qualifying medical expenses claimed."]

Inventory potentially qualifying evidence only. Reimbursed costs, premiums,
and the statutory excess are excluded. **Wheelchair: not deductible**; scooters
and home modifications are also excluded for 2025. Do not treat the inventory
as a finished deduction calculation.

| Expense type | Gross amount | Reimbursed by insurance | Net qualifying amount | Src |
|-------------|-------------|------------------------|----------------------|-----|
| [type] | EUR [amount] | EUR [amount] | EUR [amount] | [F/U/A/?] |

- Total qualifying expenses: EUR [amount] -- Src: C:sum
- Drempelinkomen (combined): EUR [amount] -- Src: C:from_income
- Increase-eligible subtotal: EUR [amount]; percentage [40% / 113% / none] and
  increase EUR [amount] -- Src: C:classified_multiplier
- Non-increased subtotal (genees- en heelkundige hulp and reiskosten
  ziekenbezoek): EUR [amount] -- Src: C:classified_sum
- Mobility forfait: [not applicable / EUR 925 minus EUR [available or received
  reimbursements] = EUR [amount]], supported by [evidence] -- Src: [F/U/C]
- 2025 drempel: EUR [amount] using [single / full-year fiscal-partner] table -- Src: C:threshold_calc
- **Deductible zorgkosten result:** [EUR amount / review required because: missing input] -- Src: C:threshold_calc

### Giften (charitable donations)

[If not applicable: "Not applicable -- no charitable donations claimed."]

#### Periodieke giften

| Recipient (ANBI) | Annual amount | Agreement type | Src |
|-------------------|--------------|----------------|-----|
| [name] | EUR [amount] | [notarial deed / written agreement] | [F/U/A/?] |

Total periodieke giften before the annual maximum/transition review: EUR [amount] -- Src: C:sum

- Periodic-gift maximum for 2025: **EUR 1.5 million**, subject to the reviewed
  **transition** rule.
- Agreement date and transition outcome: [date / reviewed / manual review]

#### Gewone giften (incidental)

| Recipient (ANBI) | Amount | Cultural ANBI | Src |
|-------------------|--------|--------------|-----|
| [name] | EUR [amount] | [yes/no] | [F/U/A/?] |

- Total gewone giften: EUR [amount] -- Src: C:sum
- Cultural ANBI multiplier applied: EUR [amount] ([multiplier and maximum from `deductions.md`]) -- Src: C:formula
- Drempel ([threshold formula and minimum from `deductions.md`]): EUR [amount] -- Src: C:formula
- Cap ([cap formula from `deductions.md`]): EUR [amount] -- Src: C:formula
- **Deductible gewone giften:** EUR [amount] -- Src: C:formula

### Lijfrentepremie

[If not applicable: "Not applicable -- no lijfrentepremie claimed."]

- Premiums paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Provider: [name] -- Src: [F/U/A/?]
- Official Hulpmiddel Lijfrentepremie result retained: [yes / missing] -- Src: [F/U/?]
- Jaarruimte 2025 (based on 2024 inputs): [EUR amount / missing inputs] -- Src: [F/U/C]
- Reserveringsruimte 2025 (2015-2024 history; maximum EUR 42,108): [EUR amount / missing inputs] -- Src: [F/U/C]
- Deductible lijfrentepremie result: [EUR amount / review required because: missing input] -- Src: C:min(premie, available room)

### Other deductions

[If not applicable: "Not applicable -- no other deductions claimed."]

| Deduction | Amount | Src |
|-----------|--------|-----|
| [e.g., restant persoonsgebonden aftrek prior years] | EUR [amount] | [F/U/A/?] |

- AOV: [policy type / insurer statement / manual review]. A qualifying private
  AOV premium belongs to the **private income-provision category**, **not ordinary business costs**. Do not subtract it from business profit; ambiguous
  policy types and exact deductibility remain manual review.
- Studiekosten: [not deductible: ordinary post-2021 expense / qualifying
  prestatiebeurs exception]. If qualifying, record DUO final non-conversion
  notice, pre-1 July 2015 study periods, level, capped grant amount, separate EUR
  250 threshold per partner, and any 100%-total partner allocation -- Src: [F/U/C]

### Deductions total

| Deduction category | Amount | Src |
|-------------------|--------|-----|
| Alimentatie | EUR [amount] | C:above |
| Zorgkosten (above drempel) | [manual review required / EUR amount] | C:above |
| Giften (periodiek + gewoon) | EUR [amount] | C:above |
| Lijfrentepremie | [manual review required / EUR amount] | C:above |
| Other | EUR [amount] | C:above |
| **Total persoonsgebonden aftrek** | **EUR [amount]** | C:sum |

Allocation order: box 1 first, then box 3, then box 2.

## Credits screening

[For each item below, emit `Candidate`, `Not applicable`, or `Unresolved`, list
the facts supporting that status, and flag candidates/unresolved conditions for
review in Mijn Belastingdienst. The Taxpayer profile summary starts the screen;
it does not decide the result. Do not calculate amounts.]

- **IACK (inkomensafhankelijke combinatiekorting)** -- [status; child DOB and
  whether younger than 12 on 1 January 2025;
  6-month household status or co-parent 78-day/6-month repeating-rhythm facts;
  child-death exception if relevant; arbeidsinkomen > EUR 6,145; partner
  duration; both arbeidsinkomens; older partner if equal] -- Src: [profile/U/F/?]
- **Ouderenkorting** -- [Candidate: AOW age reached by 31 December 2025;
  verify amount in Mijn Belastingdienst] | [Not applicable: AOW age not reached
  by 31 December 2025] -- Src: [profile.person.aow_by_tax_year.2025.status +
  transition month when applicable]
- **Alleenstaande-ouderenkorting** -- [Triggered: entitled to an AOW benefit for
  a single person; verify in Mijn Belastingdienst] | [Not applicable: no such AOW
  entitlement] -- Src: [payment-year AOW entitlement evidence / U]
- **Jonggehandicaptenkorting** -- [Triggered: Wajong entitlement/work support confirmed and no ouderenkorting; verify in Mijn Belastingdienst] | [Not applicable: no Wajong entitlement/work support] | [Not applicable: ouderenkorting applies] -- Src: [U + credits screen]
- **Possible payout of unused algemene heffingskorting** -- [status; unused own
  credit; born before 1963; same fiscal partner > 6 months or partner-death
  exception; partner has sufficient Dutch tax/premium liability after own
  credits; verify portal result and do not assume EUR 3,068 maximum] -- Src:
  [profile/U/F/?]

## Fiscal partner notes

[If `partner.has_fiscal_partner` is `no`, emit: `Not applicable — no fiscal partner in 2025 (Src: profile.partner.has_fiscal_partner).` If applicable, load `templates/sections/partner.md` and fill that section here.]

## Open questions

[Every question still awaiting the taxpayer's answer, including deferred ones.
Q-IDs are stable: never renumber, and reuse the same Q-ID when a deferred
question is asked again. Remove a row once its answer is recorded in the tax
section. Appendix A lists the same Q-IDs under each section's `open`. Order the
rows by impact: filing possible at all, then tax amount, then accuracy. The
field mapper adds its own rows for mapping gaps, continuing the Q001 numbering,
so every field-map `open_question_id` resolves here.]

| Q-ID | Section | Question | Blocking | Status |
|------|---------|----------|----------|--------|
| [Q001] | [section key, e.g. `box3_actual`] | [question] | [yes/no] | [open / deferred] |

[If none: "None -- no open questions."]

## Missing information

[Every row marked `Src: ?` must appear here. Each item says what is needed and
where the taxpayer can obtain it, and links the open Q-ID when one exists. The
field mapper adds its own rows for missing mapped values, continuing the M001
numbering.]

### Critical (blocks accurate filing)

| M-ID | Description | Workpack row | Q-ID | How to resolve |
|------|-------------|--------------|------|----------------|
| [M001] | [description] | [section/row] | [Q-ID / none] | [resolution guidance] |

### Important (affects accuracy)

| M-ID | Description | Workpack row | Q-ID | How to resolve |
|------|-------------|--------------|------|----------------|
| [M002] | [description] | [section/row] | [Q-ID / none] | [resolution guidance] |

### Nice-to-have (minor impact)

| M-ID | Description | Workpack row | Q-ID | How to resolve |
|------|-------------|--------------|------|----------------|
| [M003] | [description] | [section/row] | [Q-ID / none] | [resolution guidance] |

Total missing items: [count]

## Assumptions

[Only assumptions the taxpayer explicitly accepted. Every row with
`Src: A:<id>` must appear here.]

| A-ID | Description | Accepted by taxpayer | Impact if incorrect | Resolution |
|------|-------------|----------------------|---------------------|------------|
| [A001] | [what was assumed] | [U:"<short quote>" (<YYYY-MM-DD>)] | [what changes if wrong] | [how to confirm] |

Total assumptions: [count]

[If none: "None -- no assumptions were used."]

## User-stated values index

[Cross-index every `U:` row so the user can spot-check what was recorded from chat.]

| Workpack row | Value | Quote | Stated at | Document row |
|--------------|-------|-------|-----------|--------------|
| [section/row] | [value] | "[verbatim quote]" | [YYYY-MM-DD] | [ev_NNN] |

## Field map summary

[Written only by the field mapper, from the canonical map in Appendix B. Until
mapping runs, this section holds the single line `not yet mapped`; the mapper
replaces it with its summary table. The field map maps each line item in this
workpack to the corresponding field in the Belastingdienst online return.
The taxpayer uses it as a guide while personally entering data in Mijn
Belastingdienst. It is specific to the annual return 2025 and separate from any
provisional field map. Once mapping has run, every manual-entry field in
Appendix B appears here with the same value, and every missing field appears
as a `MISSING - enter manually` row with its Q-ID. If a sourced fact changes
after generation, the annual workflow adds the line `STALE — predates the
change to <fact> (<YYYY-MM-DD>); regenerate before use.` at the top of this
section; only regeneration, which re-runs the field mapper, removes it.]

not yet mapped

## Manual-entry checklist

[Written only by the submit companion, and only when the taxpayer asks for it.
Until then this section holds the single line `not requested`. If a sourced
fact changes after generation, the annual workflow adds the same stale line at
the top of a requested checklist; its values are then never used until the
map is regenerated and the checklist rebuilt.]

not requested

## Human review checklist

The taxpayer or an authorized human completes this review personally. Before
filing through Mijn Belastingdienst, the taxpayer reviews the following; the
assistant must not open or operate the portal, enter values, sign, send, or
submit.

- [ ] I accounted for all income sources and compared them with VIA pre-filled data
- [ ] Evidence matches reported amounts -- no unexplained discrepancies
- [ ] Box 3 peildatum values verified against bank/broker statements
- [ ] I reviewed the Box 3 data-supply choice; when actual-return data was
  supplied, I checked the portal comparison and favorable amount (no method
  election was attributed to the taxpayer)
- [ ] Winst uit onderneming reviewed if applicable: every line of the chain from saldo fiscale winstberekening to belastbare winst uit onderneming checked against my own jaarstukken, and the vermogensvergelijking reconciled
- [ ] I understand that the aangifte computes the ondernemersaftrek, the kleinschaligheidsinvesteringsaftrek, the MKB-winstvrijstelling and the belastbare winst itself, and that I check those on screen against this workpack rather than typing them
- [ ] I expect a **second, separate aanslag** for the inkomensafhankelijke bijdrage Zvw alongside the aanslag inkomstenbelasting
- [ ] Terminal business computations (samenwerkingsverband profit share, medegerechtigde loss caps, DGA/BV winst, agrarisch, zeevarende, stakingswinst, herinvesteringsreserve, oudedagsreserve wind-down, terbeschikkingstelling) routed to manual review or professional advice
- [ ] Business administration retained for at least 7 years (AWR article 52; `law_awr_artikel_52`) if you have winst uit onderneming
- [ ] Box 2 dividends, share-sale data, withholding tax, loss setoff, and partner allocation reviewed if applicable
- [ ] Complex Box 2 facts routed to manual review or professional advice
- [ ] Partner filing mode confirmed; if separate, shared allocations agree
  across both returns and total no more than 100%
- [ ] I reviewed IACK, ouderenkorting, alleenstaandeouderenkorting,
  jonggehandicaptenkorting, and possible payout of unused algemene
  heffingskorting in the official portal; unresolved conditions remain visible
- [ ] Zorgkosten threshold manual review completed if exact reviewed 2025 threshold sources are not registered
- [ ] Lijfrente limit manual review completed if exact reviewed 2025 jaarruimte/reserveringsruimte sources are not registered
- [ ] Deductions have supporting evidence retained for at least 5 years
- [ ] I used the Field map summary only as a guide while personally entering each value in Mijn Belastingdienst
- [ ] All `U:` user-chat values reviewed for accuracy
- [ ] All `A:` assumptions reviewed and confirmed or corrected
- [ ] All `?` missing information resolved or consciously accepted
- [ ] Every blocking open question answered; any question left open keeps this workpack a draft
- [ ] Every Documents and sources row marked `needs review` checked against the original document
- [ ] WOZ-waarde matches the gemeente beschikking
- [ ] Mortgage interest matches the jaaroverzicht hypotheek
- [ ] Loonheffing withheld matches jaaropgaven total
- [ ] Filing-route label verified: `invited`, `no_letter_but_mandatory`,
  `refund_claim_only`, or `filing_obligation_unresolved`; 14 July 2026 used only
  for the mandatory no-letter route and no deadline invented for unresolved
  facts

## Not submission advice

This workpack is a preparation aid. You, the taxpayer or an authorized human,
must review the figures and perform all portal entry, signing, and submission
yourself. The assistant must not access or operate Mijn Belastingdienst.

## Appendix A — Resume record

[One fenced `yaml` block. Facts never live here; they live in the sections
above with provenance. Section keys and statuses mirror the conversation:
`not_started | in_progress | complete | chat_only | deferred`, with `open`
listing that section's open Q-IDs. `readiness` follows the STATUS banner.
`save_consent` defaults to `not_given` and becomes `given` in the written file
(saved in the working folder or delivered as a download); it is a record of the
taxpayer's decision in the conversation, never an authorization to write. `generation_confirmed` becomes `true`
after the final-review confirmation and returns to `false` when a sourced fact
changes afterwards; the Field map summary, Appendix B, and any checklist then
carry the stale line until regeneration. `queued_workflow` holds the queued 2026 subflow value when
the taxpayer asked for both workflows, otherwise `null`. `sources_loaded`
equals the Sources used list.]

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.6.0"
workflow: annual_2025
tax_year: 2025
created_at: ""
updated_at: ""
save_consent: not_given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  filing_status: {status: not_started, open: []}
  box1: {status: not_started, open: []}
  winst: {status: not_started, open: []}
  eigen_woning: {status: not_started, open: []}
  box2: {status: not_started, open: []}
  box3_peildatum: {status: not_started, open: []}
  box3_actual: {status: not_started, open: []}
  deductions: {status: not_started, open: []}
  credits_screening: {status: not_started, open: []}
  partner_allocation: {status: not_started, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: []
```

## Appendix B — Field map

[Written only by the field mapper: one fenced `yaml` block holding the canonical
annual field map (`workflow: annual_return`, schema v1.1 from the field-mapper
template). Until mapping runs, this section holds the single literal line
below. After a changed fact, the annual workflow adds the stale line above the
`yaml` block; the mapper removes it only by regenerating the map from the
recorded facts.]

not yet mapped
