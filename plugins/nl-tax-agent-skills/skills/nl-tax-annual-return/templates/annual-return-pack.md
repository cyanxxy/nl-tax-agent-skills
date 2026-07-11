# Annual Income-Tax Return Workpack -- 2025

> **STATUS: {DRAFT — N deferred section(s) | COMPLETE DRAFT FOR REVIEW} — not for filing.** Replace `N` with the number of sections still deferred or carrying `?` rows; use "COMPLETE DRAFT FOR REVIEW" only when no section is deferred. This workpack is never submission advice; filing always happens manually via Mijn Belastingdienst.

> **Provenance convention.** Every numeric line in this workpack records its source in a `Src` column or inline `Src:` note.
> Source codes:
> - `F:<evidence_id>` -- value from a file in the evidence index
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat
> - `A:<assumption_id>` -- confirmed assumption, also listed under Assumptions
> - `?` -- required but still missing, also listed under Missing information
> - `C:<formula>` -- computed from other sourced rows
>
> A row marked `?` is never silently treated as zero. It blocks finalization until resolved or explicitly accepted as missing.

## Contents

- Scope
- Unsupported-case checks
- Sources used
- Taxpayer profile summary
- Evidence summary
- Filing status and late-filing exposure
- Income notes
- Winst uit onderneming notes
- Own-home notes
- Box 2 notes
- Box 3 notes
- Deductions notes
- Credits screening
- Fiscal partner notes
- Field map summary
- Missing information
- Assumptions
- User-stated values index
- Human review checklist
- Not submission advice

## Scope

Tax year: 2025
Workflow: Annual income-tax return (aangifte inkomstenbelasting)
Taxpayer: [from profile]
Fiscal partner: [yes/no, from profile]
Created: [timestamp]

## Unsupported-case checks

- [ ] Full-year Dutch resident: [yes/no]
- [ ] Individual taxpayer -- supported IB-ondernemer (eenmanszaak / ZZP) or non-business individual, not a complex business form: [yes/no]
- [ ] Living taxpayer: [yes/no]
- [ ] No M-biljet required: [yes/no]
- [ ] No complex business manual-review trigger (partnership, DGA/BV winst, agrarisch, zeevarende, staking, resultaat uit overige werkzaamheden) blocking standard preparation: [yes/no/not applicable]
- [ ] No complex Box 2 manual-review trigger blocking standard preparation: [yes/no/not applicable]

If any check is "no", this workpack should not have been generated. Stop and consult the intake skill.

## Sources used

[Emit exactly the IDs from `workspace/shared/session-progress.yaml` -> `sources_loaded`, one per line. Do not pad with sources that were not consulted, and do not omit sources that were consulted.]

- [source_id]
- [source_id]

## Taxpayer profile summary

[Summary from workspace/taxpayer/profile.yaml. Include source provenance for each value:]

- Name: [taxpayer name] -- Src: [F/U/A/?]
- Date of birth: [date] -- Src: [F/U/A/?]
- AOW age in 2025: [yes/no] -- Src: [C:dob_vs_aow_age | U]
- Residency: full-year Dutch resident 2025 -- Src: [F/U/A/?]
- Primary income type: [employment / pension / benefit / combination] -- Src: [F/U/A/?]
- Fiscal partner: [yes/no] -- Src: [F/U/A/?]
- Partner name: [if applicable] -- Src: [F/U/A/?]
- Partner date of birth: [date or n/a] -- Src: [F/U/A/?]
- Partner AOW age in 2025: [yes/no/n/a] -- Src: [C/U]
- Children at home on 31 Dec 2025: [count] -- Src: [U/A/?]
- Children DOBs (for IACK age test on 1 Jan 2025): [list or n/a] -- Src: [U/A/?]
- Single-parent status: [yes/no] -- Src: [U/A/?]
- Address: [municipality, for WOZ reference] -- Src: [F/U/A/?]
- Special circumstances: [any flags from intake]

## Evidence summary

[Summary from workspace/taxpayer/evidence-index.yaml. Include file-based and user-chat items:]

- Total evidence items indexed: [count] (files: [count], user-chat values: [count])
- Files by category:
  - Income (jaaropgaven, pension statements): [count]
  - Own home (WOZ-beschikking, mortgage statement): [count]
  - Box 3 (bank statements, portfolio statements): [count]
  - Deductions (medical receipts, donation receipts): [count]
  - Other: [count]
- Items flagged for review: [count]
- Items with low classification confidence: [count]

## Filing status and late-filing exposure

[From workspace/annual/2025/notes/filing-status.yaml. Emit exactly one of the three subsections below.]

### On time

Filing status: on time. No late-filing exposure.

### Uitstel granted

- Granted uitsteldatum: [YYYY-MM-DD] -- Src: [U/F]
- Belastingrente still accrues from 1 July 2026 if tax is owed on the eventual aanslag.
- Belastingrente rate from 1 January 2026: [rate from `late-filing.md`] -- Src: bd_belastingrente_overview

### Late (deadline passed, no uitstel)

- Deadline route: [invitation letter / no invitation + tax due voluntary-filing guardrail / not established] -- Src: [F/U/C]
- Applicable deadline: [date from invitation letter / 14 July 2026 / not established] -- Src: [F/U/C]
- Deadline status: [passed / not established] -- Src: C:deadline_route
- Filing status: [outstanding / not established] -- Src: [U/C]

Render this late-exposure subsection only when an applicable deadline is established and has passed without granted uitstel. With **no invitation**, use 14 July 2026 only when tax due was established. If the deadline is **not established**, do not invent one and do not classify the return as late.
- Verzuimboete — **potential exposure**, not a promised penalty:
  - Herinnering received: [yes / no / unknown] -- Src: [F/U/?]
  - Aanmaning received: [yes / no / unknown] -- Src: [F/U/?]
  - 10 werkdagen after aanmaning expired while still unfiled: [yes / no / unknown] -- Src: [F/U/C/?]
  - Potential first-time amount after the full escalation: EUR [amount from `late-filing.md`] -- Src: bd_verzuimboete
  - Potential repeated amount after the full escalation: up to EUR [maximum from `late-filing.md`] -- Src: bd_verzuimboete
  - Missing the filing deadline alone does not impose the boete; exposure is conditional on the herinnering, aanmaning, and 10 werkdagen sequence.
- Belastingrente:
  - Starts running 1 July 2026 for any tax owed
  - Rate from 1 January 2026: [rate from `late-filing.md`] -- Src: bd_belastingrente_overview
- Recommended next steps:
  - File the prepared return through Mijn Belastingdienst as soon as possible.
  - Track any herinnering and aanmaning, file immediately, and do not assume that a verzuimboete will be imposed.
  - Pay the aanslag by its due date (betaaltermijn) to avoid invorderingsrente. Belastingrente is already fixed on the aanslag and is not reduced by paying faster.
- The Belastingdienst determines whether the escalation conditions are met and sets any actual boete and rente. This workpack does not compute or promise final figures.

## Income notes

### Employment income (loon uit dienstbetrekking)

| Employer | Gross salary | Loonheffing withheld | Src (gross) | Src (loonheffing) |
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

### Company car and stock options review

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

### Other box 1 income

| Description | Amount | Src |
|-------------|--------|-----|
| [e.g., alimentatie received] | EUR [amount] | [F/U/A/?] |

[If no other income, state "Not applicable." Winst uit onderneming (eenmanszaak / ZZP) is NOT recorded here -- it has its own "Winst uit onderneming notes" section below. Resultaat uit overige werkzaamheden stays a manual-review item.]

### Box 1 income total

| Item | Amount | Src |
|------|--------|-----|
| Total gross employment income | EUR [amount] | C:sum(employment.gross) |
| Total gross pension income | EUR [amount] | C:sum(pension.gross) |
| Total gross benefit income | EUR [amount] | C:sum(benefit.gross) |
| Winst uit onderneming | manual-review blocker — not included in this supported total | C:business-section schema review |
| Total other box 1 income | EUR [amount] | C:sum(other) |
| **Total box 1 income (before deductions)** | **EUR [amount]** | C:sum(rows above) |
| Total loonheffing withheld | EUR [amount] | C:sum(loonheffing) |

## Winst uit onderneming notes

[If no onderneming, emit exactly these two lines and skip the rest of this section:

> Not applicable -- no winst uit onderneming reported.
> business.has_onderneming: no
]

This section is preparation-only. Require a finalized 2025 profit-and-loss
statement and finalized 2025 balance. Organize evidence and questions but do not
derive final taxable business profit or claim a complete business return. The
annual field map remains `draft` with blocker `business-section schema review`.

### Ondernemer status

- Ondernemer voor de inkomstenbelasting (eenmanszaak / ZZP): [yes/no/manual review] -- Src: [F/U/A/?]
- Urencriterium met (at least 1,225 hours): [yes/no] -- Src: [F/U/A/?]
- Complex-case review: [none / partnership (VOF/maatschap/CV) / medegerechtigde / DGA or BV winst / agrarisch / zeevarende / staking or cessation / resultaat uit overige werkzaamheden]

### Finalized accounts evidence

| Item | Status / evidence | Src |
|------|-------------------|-----|
| Finalized profit-and-loss statement for 2025 | [reviewed/missing/open question] | [F/U/?] |
| Finalized balance for 2025 | [reviewed/missing/open question] | [F/U/?] |

### Organized facts and questions

| Area | Supplied categories / facts | Open review questions | Src |
|------|-----------------------------|-----------------------|-----|
| Profit-and-loss | [preserve statement labels] | [questions] | [F/U/?] |
| Balance | [preserve statement labels] | [questions] | [F/U/?] |
| Hours and entrepreneur status | [facts] | [questions] | [F/U/?] |
| Investments and candidate deductions | [facts only] | [questions] | [F/U/?] |

Do not apply ondernemersaftrek, MKB-winstvrijstelling, KIA, Zvw, cessation
profit, or final tax. Route every complex form or event to terminal manual
review.

## Own-home notes

[If no own home: "Not applicable -- the taxpayer does not own a primary residence. Skip to Box 3 notes."]

One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review. For those cases list the collected dates, addresses, use, occupancy, listing/rental status, WOZ evidence, and mortgage evidence; do not complete the standard calculation below.

### WOZ-waarde

- WOZ-waarde (waardepeildatum 1 January 2024): EUR [amount] -- Src: [F/U/A/?]
- Bezwaar filed: [yes/no] -- Src: [F/U/A/?]

### Deductible own-home costs

- Mortgage interest paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Qualifying financing costs paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Periodic erfpacht payments: EUR [amount] -- Src: [F/U/A/?]
- Periodic opstal payments: EUR [amount] -- Src: [F/U/A/?]
- Periodic beklemming payments: EUR [amount] -- Src: [F/U/A/?]
- `total_deductible_own_home_costs`: EUR [sum of mortgage interest, qualifying financing costs, and periodic erfpacht/opstal/beklemming] -- Src: C:cost-sum
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Mortgage type: [annuitair / lineair / aflossingsvrij (pre-2013)] -- Src: [F/U/A/?]
- Outstanding balance 31 December 2025: EUR [amount] -- Src: [F/U/A/?]
- Deduction qualification: [confirmed / requires review]

### Eigenwoningforfait

- WOZ-waarde bracket: EUR [lower] to EUR [upper]
- Applicable percentage: [percentage]%
- Eigenwoningforfait: EUR [WOZ-waarde] x [percentage]% = EUR [amount] -- Src: C:woz*pct

### Tariefsaanpassing

Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and is never added to taxable Box 1 income.

[If taxpayer income is in the top bracket above [threshold from `box1-rates.md`]:]

- Portion of deductible own-home costs falling in schijf 3: EUR [amount] -- Src: C:...
- Tariefsaanpassing: EUR [amount] x ([top bracket rate from `box1-rates.md`] - [deduction-rate cap from `deductions.md`]) = EUR [amount] -- Src: C:...
- Effective deduction rate for this portion: [deduction-rate cap from `deductions.md`]

[If income is below schijf 3: "Not applicable -- income does not exceed the schijf 3 threshold."]

### Hillenregeling

[If eigenwoningforfait exceeds `total_deductible_own_home_costs`:]

- Excess eigenwoningforfait: EUR [eigenwoningforfait] - EUR [`total_deductible_own_home_costs`] = EUR [amount] -- Src: C:...
- Hillenregeling correction: EUR [amount] x [Hillen percentage from `own-home.md`] = EUR [amount] -- Src: C:...
- `hillen_deduction`: EUR [amount] -- Src: C:...

[If total deductible own-home costs equal or exceed eigenwoningforfait: "Not applicable -- total deductible own-home costs equal or exceed the eigenwoningforfait."]

### Net own-home result

| Item | Amount | Src |
|------|--------|-----|
| Eigenwoningforfait | EUR [amount] | C:above |
| Minus: `total_deductible_own_home_costs` | EUR [amount] | C:cost-sum |
| Minus: `hillen_deduction` (if applicable) | EUR [amount] | C:above |
| **`box1_own_home_balance`** | **EUR [amount]** | C:sum |

`box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`

[A negative balance reduces box 1 taxable income. Verify optional helper output against the cited evidence; if any cost qualification or complex-home fact is unresolved, preserve it as manual review.]

### Separate tax-benefit adjustment review

| Item | Amount | Src |
|------|--------|-----|
| Tariefsaanpassing (if applicable) | EUR [amount] | C:above |

[This review adjustment affects the tax benefit only and is not included in `box1_own_home_balance`.]

## Box 2 notes

[If no aanmerkelijk belang, emit exactly these two lines and skip the rest of this section:

> Not applicable -- no substantial interest (aanmerkelijk belang) reported.
> box2.has_aanmerkelijk_belang: no
]

### Substantial-interest status

- Has aanmerkelijk belang: [yes/no/manual review]
- Basis: [generally 5% threshold, assessed with fiscal partner where applicable]
- Evidence/source: [F/U/A/?]
- Complex-case review: [none / valuation dispute / emigration / death / restructuring / treaty or nonresident issue / informal capital / non-arm's-length transfer / DGA corporate-tax issue]

### Regular benefits

| Item | Amount | Src |
|------|--------|-----|
| Gross regular benefits, including dividends (`box2.reguliere_voordelen_bruto`) | EUR [amount] | [F/U/A/?] |
| Costs of regular benefits (`box2.kosten_reguliere_voordelen`) | EUR [amount] | [F/U/A/?] |
| Fictitious regular benefit from BV lending (`box2.fictief_regulier_voordeel_bv_lening`) | EUR [amount] | [F/U/A/? / manual review] |
| Dividend withholding tax to credit (`box2.ingehouden_dividendbelasting`) | EUR [amount] | [F/U/A/?] |

### Disposal benefits

| Item | Amount | Src |
|------|--------|-----|
| Net transfer price (`box2.vervreemdingsprijs`) | EUR [amount] | [F/U/A/?] |
| Acquisition price (`box2.verkrijgingsprijs`) | EUR [amount] | [F/U/A/?] |
| Disposal costs used to derive net transfer price (`box2.vervreemdingskosten`) | EUR [amount] | [F/U/A/?] |
| Disposal benefit (`box2.vervreemdingsvoordeel`) | EUR [amount or "manual review required"] | [C:net-transfer-acquisition / F/U/A/?] |

Standard preparation formula: official net transfer price minus acquisition price. Do not subtract disposal costs from `box2.vervreemdingsprijs`; that field is the official net transfer price. Use `box2.vervreemdingskosten` only to derive net transfer price from gross proceeds, and otherwise keep it as provenance/reconciliation so costs are not deducted twice. Use manual review instead of a calculated amount when valuation, informal capital, non-arm's-length, restructuring, treaty, nonresident, emigration, death, or corporate-tax-heavy DGA facts are present.

### Loss setoff and partner allocation

- Substantial-interest loss to set off (`box2.te_verrekenen_verlies_ab`): EUR [amount] -- Src: [F/U/A/?]
- Fiscal-partner Box 2 allocation (`partner.verdeling_box2_inkomen`): [taxpayer %] / [partner %] -- Src: [F/U/A/?]
- Allocation total equals 100%: [yes/no/manual review]

Note: Box 2 allocation and any reviewed calculation remain preparation notes for manual Mijn Belastingdienst entry; they are not filing or tax advice.

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

Check trail: `check_performed_by: "[checked_by_agent | checked_by_script]"`.
The manual path and optional script apply the same row checks. Preserve this
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

### Schulden (non-mortgage debts)

| Debt | Type | Balance 1 Jan 2025 | Src |
|------|------|--------------------|-----|
| [description] | [consumer loan / student debt / other] | EUR [amount] | [F/U/A/?] |

**Total schulden (category III):** EUR [amount] -- Src: C:sum

### Heffingsvrij vermogen

- Single taxpayer: EUR [from `_shared/knowledge/years/2025/box3/fictitious.md`]
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

[Actual-return subsection status: `complete` when all required evidence is
available; otherwise `deferred/manual review`. If deferred, retain both method
explanations and list the evidence needed above. Do not imply that both
calculations were completed.]

### Comparison: fictitious vs actual

| Method | Box 3 income | Box 3 tax (at [box 3 rate from `fictitious.md`]) | Src | Data status |
|--------|-------------|-------------------|-----|-------------|
| Fictitious return (forfaitair rendement) | EUR [amount] | EUR [amount] | C:fictitious_rows | Complete |
| Actual return (werkelijk rendement) | EUR [amount] | EUR [amount] | C:actual_return_rows | [Complete / Partial / Missing] |

More favorable method: [fictitious / actual / cannot determine -- data incomplete]

Note: The final election between fictitious and actual return is made in the official Mijn Belastingdienst filing environment. This comparison is informational only and does not constitute a binding election.

### Partner allocation for box 3

[If no fiscal partner: "Not applicable -- no fiscal partner."]

[If fiscal partner:]

| Allocation | Taxpayer share | Partner share | Combined box 3 tax | Src |
|------------|---------------|--------------|-------------------|-----|
| Default (50/50) | EUR [amount] | EUR [amount] | EUR [amount] | C:allocation |
| Optimized ([X]% / [Y]%) | EUR [amount] | EUR [amount] | EUR [amount] | C:allocation |

Recommended allocation: [percentage split] -- results in EUR [amount] lower combined box 3 tax.

Note: The allocation percentage applies to the entire box 3 base (assets minus debts). Partners cannot allocate asset-by-asset. Both partners must use the same ratio in their respective returns.

## Deductions notes

### Alimentatie

[If not applicable: "Not applicable -- no partneralimentatie payments."]

- Total partneralimentatie paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Basis: [court order / divorce agreement / notarial deed] -- Src: [F/U/A/?]

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
- Zorgkosten **threshold: manual review** [required unless the complete reviewed
  2025 threshold and multiplier table is registered and all inputs are present]
- Deductible zorgkosten result: [manual review required / EUR amount with source-backed calculation] -- Src: C:threshold_calc

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
- Lijfrente limit manual review: [required unless exact reviewed 2025 jaarruimte/reserveringsruimte rules and all required inputs are present]
- Jaarruimte available: [manual review required / EUR amount with source-backed calculation] -- Src: [F/U/A/?/C]
- Reserveringsruimte available: [manual review required / EUR amount with source-backed calculation] -- Src: [F/U/A/?/C]
- Deductible lijfrentepremie result: [manual review required / EUR amount with source-backed calculation] -- Src: C:min(premie, available room)

### Other deductions

[If not applicable: "Not applicable -- no other deductions claimed."]

| Deduction | Amount | Src |
|-----------|--------|-----|
| [e.g., restant persoonsgebonden aftrek prior years] | EUR [amount] | [F/U/A/?] |

- AOV: [policy type / insurer statement / manual review]. A qualifying private
  AOV premium belongs to the **private income-provision category**, **not ordinary business costs**. Do not subtract it from business profit; ambiguous
  policy types and exact deductibility remain manual review.

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

[For each of the four credits below, emit one line: either `Triggered: <reason>` (and flag for manual review in Mijn Belastingdienst) or `Not applicable: <reason>`. Read household composition from workspace/taxpayer/profile.yaml. Do not calculate amounts.]

- **IACK (inkomensafhankelijke combinatiekorting)** -- [Triggered: child born [DOB], younger than 12 on 1 January 2025; verify arbeidsinkomen threshold in Mijn Belastingdienst] | [Not applicable: no child younger than 12 on 1 January 2025] -- Src: [profile.household.children]
- **Ouderenkorting** -- [Triggered: AOW age reached in 2025; verify amount in Mijn Belastingdienst] | [Not applicable: not AOW age in 2025] -- Src: [profile.person.aow_age_in_tax_year]
- **Alleenstaande-ouderenkorting** -- [Triggered: entitled to an AOW benefit for
  a single person; verify in Mijn Belastingdienst] | [Not applicable: no such AOW
  entitlement] -- Src: [payment-year AOW entitlement evidence / U]
- **Jonggehandicaptenkorting** -- [Triggered: Wajong / young-disabled status confirmed; verify in Mijn Belastingdienst] | [Not applicable: no Wajong / young-disabled status] -- Src: [U]

## Fiscal partner notes

[If no fiscal partner: "Not applicable -- the taxpayer does not have a fiscal partner for tax year 2025."]

### Partner status

- Fiscal partner: [yes/no] -- Src: [F/U/A/?]
- Basis: [married / registered partnership / cohabiting with qualifying conditions] -- Src: [F/U/A/?]
- Partner for full year 2025: [yes/no] -- Src: [F/U/A/?]
- Special circumstances: [e.g., partner has no income, partner is AOW-age]

### Allocation options

The following items can be freely allocated between partners:

| Item | Default allocation | Optimized allocation | Tax impact | Src |
|------|-------------------|---------------------|------------|-----|
| Eigen woning result | 50/50 | [recommendation] | EUR [savings] | C:allocation |
| Box 2 income | [taxpayer %] / [partner %] | [review scenarios] | [manual review] | [U/A/?] |
| Box 3 grondslag | 50/50 | [recommendation] | EUR [savings] | C:allocation |
| Persoonsgebonden aftrek, including eligible prior-year personal-deduction remainder for whole-year fiscal partners | [scenario split totaling 100%] | [traceable comparison; taxpayer review required] | EUR [estimated difference] | C:allocation |

Items that CANNOT be allocated:
- Arbeidskorting (personal, based on individual arbeidsinkomen)
- Ondernemersaftrek (personal to the ondernemer)
- MKB-winstvrijstelling (personal to the ondernemer)

### Recommended review points

- [ ] Verify which partner has the higher marginal tax rate
- [ ] Consider tariefsaanpassing impact on eigen woning allocation
- [ ] Consider heffingskorting phase-out impact on income allocation
- [ ] Review box 3 allocation for optimal combined result
- [ ] Review Box 2 allocation if there is an aanmerkelijk belang
- [ ] Confirm both partners will use the same box 3 allocation ratio

## Field map summary

The field map for this workpack is available at:
`workspace/annual/2025/field-map.yaml`

This field map maps each line item in this workpack to the corresponding field in the Belastingdienst online return. Use it as a guide when entering data in Mijn Belastingdienst.

Note: This field map is specific to the annual return 2025. It is separate from any provisional assessment field maps.

## Missing information

[From workspace/shared/missing-info.md, filtered for annual_2025. Every row in the workpack with `Src: ?` must appear here.]

### Critical (blocks accurate filing)

| ID | Description | Workpack row | How to resolve |
|----|-------------|--------------|----------------|
| [MI-001] | [description] | [section/row] | [resolution guidance] |

### Important (affects accuracy)

| ID | Description | Workpack row | How to resolve |
|----|-------------|--------------|----------------|
| [MI-002] | [description] | [section/row] | [resolution guidance] |

### Nice-to-have (minor impact)

| ID | Description | Workpack row | How to resolve |
|----|-------------|--------------|----------------|
| [MI-003] | [description] | [section/row] | [resolution guidance] |

Total missing items: [count]

## Assumptions

[From workspace/shared/assumptions.md, filtered for annual_2025. Every row with `Src: A:<id>` must appear here.]

| Assumption ID | Description | Confirmed by user | Impact if incorrect | Resolution |
|---------------|-------------|-------------------|---------------------|------------|
| [A001] | [what was assumed] | [yes/no] | [what changes if wrong] | [how to confirm] |

Total assumptions: [count]

## User-stated values index

[Cross-index every `U:` row so the user can spot-check what was recorded from chat.]

| Workpack row | Value | Quote | Stated at |
|--------------|-------|-------|-----------|
| [section/row] | [value] | "[verbatim quote]" | [YYYY-MM-DD] |

## Human review checklist

Before filing through Mijn Belastingdienst, review the following:

- [ ] All income sources accounted for -- compare with VIA pre-filled data
- [ ] Evidence matches reported amounts -- no unexplained discrepancies
- [ ] Box 3 peildatum values verified against bank/broker statements
- [ ] Box 3 method choice reviewed (fictitious vs actual return)
- [ ] Winst uit onderneming reviewed if applicable: finalized profit-and-loss and balance evidence organized, open questions listed, and field map kept draft with the business-section schema-review blocker
- [ ] Complex business facts (partnership, DGA/BV winst, agrarisch, zeevarende, staking, resultaat uit overige werkzaamheden) routed to manual review or professional advice
- [ ] Business administration retained for at least 7 years (AWR article 52; `law_awr_artikel_52`) if you have winst uit onderneming
- [ ] Box 2 dividends, share-sale data, withholding tax, loss setoff, and partner allocation reviewed if applicable
- [ ] Complex Box 2 facts routed to manual review or professional advice
- [ ] Partner allocation reviewed and agreed with fiscal partner
- [ ] IACK, ouderenkorting, alleenstaandeouderenkorting, and jonggehandicaptenkorting reviewed in the official portal; no calculated amounts are shown here unless exact reviewed sources are registered
- [ ] Zorgkosten threshold manual review completed if exact reviewed 2025 threshold sources are not registered
- [ ] Lijfrente limit manual review completed if exact reviewed 2025 jaarruimte/reserveringsruimte sources are not registered
- [ ] Deductions have supporting evidence retained for at least 5 years
- [ ] All `U:` user-chat values reviewed for accuracy
- [ ] All `A:` assumptions reviewed and confirmed or corrected
- [ ] All `?` missing information resolved or consciously accepted
- [ ] WOZ-waarde matches the gemeente beschikking
- [ ] Mortgage interest matches the jaaroverzicht hypotheek
- [ ] Loonheffing withheld matches jaaropgaven total
- [ ] Filing route verified: invitation letter deadline used; or, with no invitation and tax due, conditional 14 July 2026 voluntary-filing guardrail used; otherwise no deadline invented

## Not submission advice

This workpack is a preparation aid. Review all information against the official Mijn Belastingdienst portal before submitting.
