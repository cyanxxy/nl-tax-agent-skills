# Box 3 — Annual 2025: Classification and Calculation Rules

source_ids: bd_box3_2025_calc, bd_box3_2025_actual_return, bd_fisin_box3_actual_return_2025, bd_fisin_box3_assets_debts_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-10"
review_status: reviewed

## Asset Classification

The agent applies these official categories to reviewed facts. It does not ask
Python to classify descriptions. Before totals, each already-classified row has
`category`, `status`, `value`, and `provenance`. Only accepted rows in one of the
three categories below, with a finite non-negative value and non-empty
provenance, enter arithmetic. Preserve all other rows with rejection reasons.

A generic description is not enough to decide whether a loan is an asset or a
debt. Keep it unresolved until the direction and relevant facts are confirmed:

```yaml
- description: "Loan to friend"
  category: "unknown"
  status: "manual_review"
  value: 10000
  provenance: "U:<dated user statement>"
```

### Banktegoeden (Bank Assets)
- Savings accounts (spaarrekeningen)
- Current accounts (betaalrekeningen)
- Term deposits (deposito's)
- Foreign bank accounts (buitenlandse bankrekeningen)
- Cash only above the 2025 cash exemption: EUR 661 without fiscal partner / EUR 1,322 with fiscal partner
- Non-exempt green savings
- Premiedepots
- Share in a VvE reserve fund
- Money on notary or bailiff third-party accounts

### Overige Bezittingen (Other Assets)
- Shares (aandelen)
- Bonds (obligaties)
- Mutual funds (beleggingsfondsen)
- ETFs (exchange-traded funds)
- Cryptocurrency (crypto)
- Real estate — not own home (vastgoed, niet eigen woning)
- Loans given (verstrekte leningen), after checking official exceptions
- Other receivables (overige vorderingen), after checking official exceptions such as receivables between fiscal partners or between parents and minor children, and usually non-callable inheritance receivables
- Non-exempt green investments

### Schulden (Debts)
- Screen every debt against the official 2025 included and excluded lists before
  adding it to category III. Personal/consumer loans, negative bank balances,
  qualifying study-finance debts, Box 3 asset financing, repayable benefits,
  and inheritance tax are examples that may belong here.
- Exclusions are broader than the own-home mortgage: they also include business
  debts, most Dutch tax debts, short current liabilities, certain maintenance
  and inheritance obligations, debts tied to Box 2/other work, and debts owed
  to a fiscal partner or minor child.
- An unresolved debt stays `unknown`/`manual_review` and outside trusted totals;
  never turn "non-mortgage debt" into an automatic Box 3 classification.

## Key Parameters

| Parameter | Value |
|---|---|
| Peildatum | 1 January 2025 |
| Heffingsvrij vermogen | EUR 57,684 per person |
| Drempel schulden | EUR 3,800 per person |
| Banktegoeden percentage | 1.37% |
| Overige bezittingen percentage | 5.88% |
| Schulden percentage | 2.70% |
| Box 3 tax rate | 36% |

## Important Notes

- The fictitious method uses the 1 January 2025 position. For actual return,
  ordinary bank accounts require actual 2025 interest rather than a 31
  December balance; collect a year-end value only for an asset whose value
  change counts under `box3-actual-2025.md`.
- Apply the drempel (EUR 3,800 per person) only after the qualifying Box 3 debt
  total has been established.
- Partners can freely allocate the joint grondslag sparen en beleggen between them (any split from 0%/100% to 100%/0%); do not split individual assets or debts in the field map
- The portal asks whether the taxpayer wants to supply actual-return data. If
  supplied, it calculates both the fictitious and actual-return outcomes and
  uses the more favorable amount; the taxpayer is not asked to elect the
  higher-tax method.
- Werkelijk rendement is calculated without heffingsvrij vermogen and follows the same partner allocation percentage as the joint grondslag sparen en beleggen
- Fictitious-return workpacks must show the official steps: belastbaar rendement, rendementsgrondslag, grondslag sparen en beleggen, aandeel in rendementsgrondslag, box 3 income, and tax
- Manual and optional-script paths use the same row checks and totals. Record
  `checked_by_agent` for a manual check or `checked_by_script` for the optional
  script; never infer categories from keywords.

## Required two-method workpack treatment

Every annual 2025 workpack explains both the fictitious (forfaitair) calculation and
the actual return (werkelijk rendement) route, and offers to collect the
actual-return inputs needed for comparison. Indexed files and exact chat answers
are both valid provenance. When every required input is present, mark the
subsection `complete` if indexed evidence is used or `chat_only` if the complete
set is chat-supplied, then show the comparison. If the taxpayer declines this
additional data collection, mark it `complete` with `not supplied by choice`;
that is not a gap. Only facts still missing after the taxpayer requested the comparison may be
`deferred/manual review`; do not silently omit the explanation or claim that
both methods were completed.
