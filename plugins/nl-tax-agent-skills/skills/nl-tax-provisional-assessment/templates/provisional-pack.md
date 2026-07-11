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

[List all source_ids used in producing this workpack]

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
deductions, Zvw, cessation profit, or final tax.

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

If the current date is on or after 2026-10-01, do not generate a stopzetten checklist. State that the 2026 stopzetten cutoff has passed and route the user to review/change or annual-return settlement as applicable.

### Cash-flow direction and route

| Item | Value | Src |
|------|-------|-----|
| Current monthly direction | [refund / payment / unknown] | [F/U/?] |
| Route chosen | [stop refund / change VA / no action] | C:decision |
| Reason | [short reason] | [F/U/C] |

### Refund-stop checklist

[Include only when the taxpayer receives a monthly refund and the current-date cutoff gate is before 2026-10-01.]

- [ ] Confirm the current VA pays a monthly refund
- [ ] Confirm the current date is before 2026-10-01
- [ ] Confirm refunds should stop for the rest of 2026
- [ ] Record that final settlement happens through the 2026 annual return in 2027
- [ ] Use the official Mijn Belastingdienst stopzetten form for the taxpayer's 2026 monthly refund
- [ ] Keep the confirmation for records

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
| **Total box 1 gross income**          | EUR               | C:sum |

## Winst uit onderneming forecast

[Repeat or reference the sourced `onderneming.geschatte_winst` forecast above.
If not applicable, state that explicitly. Preserve manual review and do not
include annual deduction or final-tax calculations.]

### Estimated tax credits

| Credit area                           | Handling | Src |
|---------------------------------------|----------|-----|
| Algemene heffingskorting              | [portal estimate / source-backed estimate / manual review] | [C/F/U/A/?] |
| Arbeidskorting                        | [portal estimate / source-backed estimate / manual review] | [C/F/U/A/?] |
| IACK                                  | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Ouderenkorting                        | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Alleenstaandeouderenkorting           | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Jonggehandicaptenkorting              | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |

Do not show calculated credit amounts unless exact reviewed sources are registered and all required taxpayer facts are available.

## Own-home estimate

### Estimated mortgage interest deduction 2026

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| Mortgage interest (hypotheekrente)    | EUR               | [F/U/A/B/?] |

### Estimated eigenwoningforfait 2026

| Item                                  | Amount (estimate) | Src |
|---------------------------------------|-------------------|-----|
| WOZ-waarde                           | EUR               | [F/U/A/B/?] |
| Eigenwoningforfait percentage         |                   | C:from_2026_table |
| Eigenwoningforfait amount            | EUR               | C:woz*pct |

| **Net own-home deduction**            | EUR               | C:sum |

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
| Debts (excluding eigenwoningschuld)   | EUR               | [F/U/A/B/?] |
| **Total schulden**                    | EUR               | C:sum |

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
| Aandeel in rendementsgrondslag        |                   | C:formula |
| **Box 3 income**                      | EUR (estimate/from-baseline) | C:formula |
| Box 3 tax rate                        | [from `box3-provisional.md`] | C:from_2026_table |
| **Box 3 tax**                         | EUR (estimate/from-baseline) | C:formula |

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

- [ ] All income estimates are reasonable and based on current knowledge
- [ ] Deduction estimates are based on the current situation for 2026
- [ ] IACK, ouderenkorting, alleenstaandeouderenkorting, and jonggehandicaptenkorting reviewed manually unless exact reviewed sources are registered
- [ ] Zorgkosten threshold manual review completed if relevant
- [ ] Lijfrente limit manual review completed if relevant
- [ ] Box 2 estimates are labeled estimate or from-baseline, if applicable
- [ ] Box 3 assets reflect the position as of 1 January 2026
- [ ] Box 3 uses the provisional fictitious method
- [ ] For change subflow: all data has been entered, not just the changed items
- [ ] All `U:` user-chat values reviewed for accuracy
- [ ] All `A:` assumptions reviewed and confirmed or corrected
- [ ] All `?` missing information resolved or consciously accepted
- [ ] Partner data is correct (if applicable)
- [ ] Box 3 allocation is optimal (if fiscal partners)

## Not submission advice

This workpack is a preparation aid. Review all information against the official Mijn Belastingdienst portal before submitting or changing a voorlopige aanslag.
