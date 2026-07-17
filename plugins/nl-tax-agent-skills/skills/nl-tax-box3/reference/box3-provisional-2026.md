# Box 3 — Provisional 2026: Fictitious-Only Rules

source_ids: bd_box3_2026_provisional, bd_fisin_box3_assets_debts_2026, bd_provisional_rates_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Method

For provisional 2026 (voorlopige aanslag 2026): **ONLY the fictitious return method** is used.

## Key Parameters

| Parameter | Value |
|---|---|
| Peildatum | 1 January 2026 |
| Heffingsvrij vermogen | EUR 59,357 per person (EUR 118,714 for fiscal partners) |
| Drempel schulden | EUR 3,800 per person (EUR 7,600 for fiscal partners) |
| Green-investment exemption | EUR 26,715 per person (EUR 53,430 for fiscal partners) |

## Categories and Fictitious Percentages (2026 Provisional)

| Category | Fictitious Return % |
|---|---|
| Banktegoeden | 1.28% |
| Overige bezittingen | 6.00% |
| Schulden | 2.70% |

Over the calculated box 3 income, the provisional 2026 box 3 tax rate is 36%.

## Input Requirements

- User provides **estimated** positions as of 1 January 2026
- All amounts are estimates — the provisional assessment is based on projected values
- Actual year-end positions will only be known after 31 December 2026
- Green investments/savings and cash need separate review because exemptions can change the amount included in banktegoeden or overige bezittingen
- Candidate debts enter `schulden` only after the official Box 3
  inclusion/exclusion screen. A non-own-home label alone is insufficient;
  unresolved debt type or purpose stays `manual_review` outside accepted totals.
- Fiscal partners allocate the joint grondslag sparen en beleggen, not individual assets or debts
- Workpacks must show the official steps: belastbaar rendement, rendementsgrondslag, grondslag sparen en beleggen, aandeel in rendementsgrondslag, box 3 income, and tax

The agent classifies reviewed facts before arithmetic. Each row needs
`category`, `status`, `value`, and `provenance`. Only `accepted` rows in
`banktegoeden`, `overige_bezittingen`, or `schulden`, with finite non-negative
values and non-empty provenance, enter trusted totals. Preserve every other row
in rejected/manual-review rows with a reason. Manual and optional-script paths
apply identical checks and record `checked_by_agent` or `checked_by_script`.
Python never classifies a description by keyword.

The official 2026 page is internally inconsistent about the displayed aandeel:
its general step says 3 decimals while worked examples say and show 2 decimals. A
workpack review estimate records the convention it used and never represents
either display rule as the binding portal calculation. The live portal and
resulting beschikking are authoritative.

Until the direction and relevant facts of a generic loan are confirmed, use:

```yaml
- description: "Loan to friend"
  category: "unknown"
  status: "manual_review"
  value: 10000
  provenance: "U:<dated user statement>"
```

## Actual-Return Boundary

Use only this explanatory note: "Werkelijk rendement is not part of provisional 2026."

Reject any field, input prompt, calculation, or method-choice wording that tries
to use werkelijk rendement in this provisional workflow.

## Handling User Questions About Actual Return

Two distinct strings exist — do not conflate them:

- **In-workpack NOTE** (the explanatory line written into the box 3 section of the
  workpack): `Werkelijk rendement is not part of provisional 2026.` — keep this
  wording verbatim (see "Actual-Return Boundary" above).
- **Conversational REDIRECT** (what you say when the user asks a question): use the
  canonical redirect below.

If the user asks: "What about my actual return for 2026?"

Respond with the canonical redirect:

> Werkelijk rendement is not part of the 2026 voorlopige aanslag. It may become relevant when filing the annual 2026 return in 2027.
