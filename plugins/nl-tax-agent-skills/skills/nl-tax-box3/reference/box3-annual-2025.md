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
- Personal loans (persoonlijke leningen)
- Credit card debt (creditcardschuld)
- Study debts under the Wet studiefinanciering
- Other debts (overige schulden)
- **NOT**: mortgage on own home (hypotheek eigen woning) — this belongs in box 1

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

- For the annual return: need BOTH 1 January AND 31 December positions for actual-return checks, but the fictitious method uses the 1 January 2025 position
- Debts below the drempel (EUR 3,800 per person) are not deductible from the grondslag
- Partners can freely allocate the joint grondslag sparen en beleggen between them (any split from 0%/100% to 100%/0%); do not split individual assets or debts in the field map
- The annual return allows choosing between the fictitious return method and the actual return method (werkelijk rendement)
- Werkelijk rendement is calculated without heffingsvrij vermogen and follows the same partner allocation percentage as the joint grondslag sparen en beleggen
- Fictitious-return workpacks must show the official steps: belastbaar rendement, rendementsgrondslag, grondslag sparen en beleggen, aandeel in rendementsgrondslag, box 3 income, and tax
- Manual and optional-script paths use the same row checks and totals. Record
  `checked_by_agent` for a manual check or `checked_by_script` for the optional
  script; never infer categories from keywords.

## Required two-method workpack treatment

Every annual 2025 workpack explains both the fictitious (forfaitair) method and
the actual return (werkelijk rendement) method, and offers to collect the
actual-return evidence needed for comparison. If the taxpayer provides the
complete evidence, mark the actual-return subsection `complete` and show the
comparison. If the taxpayer declines or the facts remain missing, keep the
fictitious explanation and record the actual-return subsection as
`deferred/manual review`; do not silently omit it or claim that both methods
were completed.
