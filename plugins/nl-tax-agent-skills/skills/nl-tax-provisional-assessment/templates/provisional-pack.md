# Voorlopige Aanslag Workpack — 2026

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

[For change/review/stopzetten: summary of current voorlopige aanslag]
[Include: monthly payment or refund amount, date issued, source (beschikking / user input)]

[For request: "No existing baseline — new request"]

## Current-year estimates

### Estimated employment income 2026

| Item                        | Amount (estimate) |
|-----------------------------|-------------------|
| Gross annual salary         | EUR               |
| Holiday allowance           | EUR               |
| Bonuses/other               | EUR               |
| **Total employment income** | EUR               |

### Estimated pension/benefit income 2026

| Item                               | Amount (estimate) |
|------------------------------------|-------------------|
| AOW                                | EUR               |
| Pension                            | EUR               |
| WW/WIA/other benefits             | EUR               |
| **Total pension/benefit income**   | EUR               |

### Estimated other income 2026

| Item                       | Amount (estimate) |
|----------------------------|-------------------|
| Other income sources       | EUR               |
| **Total other income**     | EUR               |

## Delta summary

[For change: see workspace/provisional/2026/delta-summary.md for full baseline vs current estimates comparison]

[For request: "N/A — new request"]

[For review: see workspace/provisional/2026/review-questions.md for items requiring verification]

[For stopzetten: "N/A — stopzetten does not require a delta calculation"]

## Income estimate

### Box 1 estimated income

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Total employment income               | EUR               |
| Total pension/benefit income          | EUR               |
| Total other income                    | EUR               |
| **Total box 1 gross income**          | EUR               |

### Estimated tax credits

| Credit area                           | Handling |
|---------------------------------------|----------|
| Algemene heffingskorting              | [portal estimate / source-backed estimate / manual review] |
| Arbeidskorting                        | [portal estimate / source-backed estimate / manual review] |
| IACK                                  | [manual review unless exact reviewed sources and required facts are present] |
| Ouderenkorting                        | [manual review unless exact reviewed sources and required facts are present] |
| Alleenstaandeouderenkorting           | [manual review unless exact reviewed sources and required facts are present] |
| Jonggehandicaptenkorting              | [manual review unless exact reviewed sources and required facts are present] |

Do not show calculated credit amounts unless exact reviewed sources are registered and all required taxpayer facts are available.

## Own-home estimate

### Estimated mortgage interest deduction 2026

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Mortgage interest (hypotheekrente)    | EUR               |

### Estimated eigenwoningforfait 2026

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| WOZ-waarde                           | EUR               |
| Eigenwoningforfait percentage         |                   |
| Eigenwoningforfait amount            | EUR               |

| **Net own-home deduction**            | EUR               |

## Box 2 provisional estimate

[If no aanmerkelijk belang: "Not applicable -- no substantial interest (aanmerkelijk belang) reported."]

| Item | Amount label | Source |
|------|--------------|--------|
| Estimated regular benefits, including dividends (`box2.geschatte_reguliere_voordelen`) | EUR [amount] (estimate/from-baseline) | [source or assumption] |
| Estimated disposal benefits (`box2.geschatte_vervreemdingsvoordelen`) | EUR [amount] (estimate/from-baseline) | [source or assumption] |
| Estimated costs (`box2.geschatte_kosten`) | EUR [amount] (estimate/from-baseline) | [source or assumption] |
| Estimated dividend withholding tax (`box2.geschatte_ingehouden_dividendbelasting`) | EUR [amount] (estimate/from-baseline) | [source or assumption] |
| Estimated fictitious regular benefit from BV lending (`box2.geschat_fictief_regulier_voordeel_bv_lening`) | EUR [amount] (estimate/from-baseline/manual review) | [source or assumption] |
| Fiscal-partner Box 2 allocation (`partner.verdeling_box2_inkomen`) | [taxpayer %] / [partner %] (estimate/from-baseline) | [user choice / baseline] |

Manual review / unsupported triggers: valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA issues.

## Box 3 provisional estimate

> Werkelijk rendement is not part of provisional 2026.

### Assets on 1 January 2026

#### Categorie I — Banktegoeden

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Savings accounts                      | EUR               |
| Current accounts                      | EUR               |
| Deposits / term deposits              | EUR               |
| **Total banktegoeden**                | EUR               |

#### Categorie II — Overige bezittingen

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Investments / securities              | EUR               |
| Real estate (not own home)            | EUR               |
| Crypto-assets                         | EUR               |
| Receivables (vorderingen)             | EUR               |
| Other assets                          | EUR               |
| **Total overige bezittingen**         | EUR               |

### Categorie III — Schulden

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Debts (excluding eigenwoningschuld)   | EUR               |
| **Total schulden**                    | EUR               |

### Heffingsvrij vermogen

| Item                                  | Amount            |
|---------------------------------------|-------------------|
| Heffingsvrij vermogen (single)        | EUR 59,357        |
| Heffingsvrij vermogen (partners)      | EUR 118,714       |
| Applied heffingsvrij vermogen         | EUR               |

### Drempel schulden

| Item                                  | Amount            |
|---------------------------------------|-------------------|
| Drempel schulden (single)             | EUR 3,800         |
| Drempel schulden (partners)           | EUR 7,600         |
| Aftrekbare schulden after threshold   | EUR               |

### Provisional fictitious return calculation

| Step                                  | Value             |
|---------------------------------------|-------------------|
| Total Categorie I (banktegoeden)      | EUR               |
| Total Categorie II (overige bezittingen) | EUR            |
| Total Categorie III (schulden)        | EUR               |
| Aftrekbare schulden after threshold   | EUR               |
| Belastbaar rendement: I x 1.28% + II x 6.00% - aftrekbare schulden x 2.70% | EUR |
| Rendementsgrondslag: I + II - aftrekbare schulden | EUR      |
| Grondslag sparen en beleggen          | EUR               |
| Aandeel in rendementsgrondslag        |                   |
| **Box 3 income**                      | EUR (estimate/from-baseline) |
| Box 3 tax rate                        | 36%               |
| **Box 3 tax**                         | EUR (estimate/from-baseline) |

## Deductions estimate

### Estimated alimentatie 2026

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Alimentatie (alimony)                 | EUR               |

### Estimated other deductions 2026

| Item                                  | Handling |
|---------------------------------------|----------|
| Lijfrentepremie                       | [estimate; lijfrente limit manual review unless exact reviewed sources and required inputs are present] |
| Arbeidsongeschiktheidsverzekering     | [estimate] |
| Specific care costs                   | [estimate; zorgkosten threshold manual review unless exact reviewed sources and required inputs are present] |
| Gifts (giften)                        | [estimate] |
| Other deductible expenses             | [estimate/manual review] |
| **Total other deductions**            | [estimate/manual review] |

## Field map summary

[Reference to workspace/provisional/2026/field-map.yaml]
[This file maps each collected data point to the corresponding field in the Mijn Belastingdienst portal]

## Missing information

[List all data points that are still needed to complete this workpack]
[Filter for provisional_2026 relevance only — do not include annual return items]

- [ ] [Missing item 1]
- [ ] [Missing item 2]

## Assumptions

[List all assumptions made in producing this workpack]
[All amounts are estimates unless explicitly sourced from an existing assessment]

- [Assumption 1]
- [Assumption 2]

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
- [ ] All assumptions have been reviewed and are acceptable
- [ ] All missing information items have been addressed or acknowledged
- [ ] Partner data is correct (if applicable)
- [ ] Box 3 allocation is optimal (if fiscal partners)

## Not submission advice

This workpack is a preparation aid. It does not constitute tax advice, does not submit a request, and does not interact with the Belastingdienst. You must review all information and submit through the official Mijn Belastingdienst portal using your DigiD. Do not share DigiD credentials with this tool.
