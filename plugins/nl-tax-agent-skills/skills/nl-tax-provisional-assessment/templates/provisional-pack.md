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

| Credit                               | Amount (estimate) |
|---------------------------------------|-------------------|
| Algemene heffingskorting              | EUR               |
| Arbeidskorting                        | EUR               |
| Other applicable credits              | EUR               |
| **Total estimated tax credits**       | EUR               |

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

## Box 3 provisional estimate

> CRITICAL: For the 2026 voorlopige aanslag, use the box 3 categories and values required for the provisional fictitious calculation. Werkelijk rendement is not part of the provisional calculation; it may become relevant later in the annual 2026 return.

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
| Heffingsvrij vermogen (single)        | EUR 57,000        |
| Heffingsvrij vermogen (partners)      | EUR 114,000       |
| Applied heffingsvrij vermogen         | EUR               |

### Provisional fictitious return calculation

| Step                                  | Value             |
|---------------------------------------|-------------------|
| Total Categorie I (banktegoeden)      | EUR               |
| Total Categorie II (overige bezittingen) | EUR            |
| Total Categorie III (schulden)        | EUR               |
| Rendementsgrondslag before HVV        | EUR               |
| Minus heffingsvrij vermogen           | EUR               |
| **Rendementsgrondslag**               | EUR               |
| Weighted fictitious return percentage |                   |
| **Forfaitair rendement**              | EUR               |
| Box 3 tax rate                        | 36%               |
| **Box 3 tax**                         | EUR               |

Note: The weighted fictitious return percentage is calculated based on the composition of assets and debts across the three categories. The heffingsvrij vermogen is deducted from the rendementsgrondslag AFTER the weighted percentage is calculated.

## Deductions estimate

### Estimated alimentatie 2026

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Alimentatie (alimony)                 | EUR               |

### Estimated other deductions 2026

| Item                                  | Amount (estimate) |
|---------------------------------------|-------------------|
| Lijfrentepremie                       | EUR               |
| Arbeidsongeschiktheidsverzekering     | EUR               |
| Specific care costs                   | EUR               |
| Gifts (giften)                        | EUR               |
| Other deductible expenses             | EUR               |
| **Total other deductions**            | EUR               |

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
- [ ] Box 3 assets reflect the position as of 1 January 2026
- [ ] Box 3 uses fictitious method only (no werkelijk rendement)
- [ ] For change subflow: all data has been entered, not just the changed items
- [ ] All assumptions have been reviewed and are acceptable
- [ ] All missing information items have been addressed or acknowledged
- [ ] Partner data is correct (if applicable)
- [ ] Box 3 allocation is optimal (if fiscal partners)

## Not submission advice

This workpack is a preparation aid. It does not constitute tax advice, does not submit a request, and does not interact with the Belastingdienst. You must review all information and submit through the official Mijn Belastingdienst portal using your DigiD. Do not share DigiD credentials with this tool.
