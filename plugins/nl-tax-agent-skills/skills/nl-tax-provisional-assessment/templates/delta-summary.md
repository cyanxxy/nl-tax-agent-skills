# Comparison Summary — Voorlopige Aanslag 2026 Change

> **Provenance convention.** Each row records the source of both the baseline and current estimate.
> Source codes:
> - `F:<evidence_id>` -- value from a file, such as the existing beschikking
> - `U:"<short quote>" (<YYYY-MM-DD>)` -- value stated by the user in chat
> - `A:<assumption_id>` -- confirmed assumption
> - `B:<baseline_ref>` -- value carried over from the existing voorlopige aanslag
> - `?` -- required but still missing
> - `C:<formula>` -- computed from other sourced rows

## Baseline

| Field                | Value                                          | Src |
|----------------------|------------------------------------------------|-----|
| Source               | [existing voorlopige aanslag / prior-year data] | [F/U/?] |
| Date                 | [date of baseline beschikking or data]          | [F/U/?] |
| Monthly amount       | [EUR X,XXX payment / EUR X,XXX refund]          | [F/U/?] |
| Source type          | [beschikking / user input / EVA / VVA]          | [F/U/?] |

## Changes

| Category               | Baseline      | Src (baseline) | Current Estimate | Src (current) | Delta         | Notes |
|------------------------|---------------|----------------|------------------|---------------|---------------|-------|
| Employment income      | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Pension/benefit income | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Expected business profit (`onderneming.geschatte_winst`) | EUR | [F/U/B/?] | EUR | [F/U/A/?] | EUR | [N/A if no enterprise] |
| Other income           | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Eigenwoningforfait (WOZ peildatum 1 January 2025) | EUR | [F/U/B/?] | EUR | [F/U/A/?] | EUR | |
| Total deductible own-home costs | EUR | [F/U/B/?] | EUR | [F/U/A/?] | EUR | mortgage interest + financing costs + periodic rights |
| Hillen deduction       | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           | [if applicable] |
| Box 1 own-home balance (`box1_own_home_balance`) | EUR | [F/U/B/?] | EUR | [F/U/A/?] | EUR | EWF - deductible costs - Hillen |
| Box 3 assets (Cat I)   | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Box 3 assets (Cat II)  | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Box 3 qualifying debts (Cat III) | EUR | [F/U/B/?] | EUR | [F/U/A/?] | EUR | accepted rows only; unresolved candidates excluded |
| Alimentatie            | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Other deductions       | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Partner changes        | [description] | [F/U/B/?]      | [description]    | [F/U/A/?]     | [description] |       |

### Label key

- All "Baseline" values are labeled as **from-baseline**
- All "Current Estimate" values are labeled as **estimate**
- Delta = Current Estimate minus Baseline for workpack review only
- Any row where either side is `?` is also listed in the workpack's Missing information section.

## Impact

[Reviewed possible future payment/refund direction, or `uncertain`; never a cash-flow prediction]

- If the reviewed estimate points upward: "The prepared 2026 estimate is higher than the current baseline. The portal may therefore show a higher future payment or lower future refund."
- If the reviewed estimate points downward: "The prepared 2026 estimate is lower than the current baseline. The portal may therefore show a lower future payment or higher future refund."
- If the reviewed estimate is similar: "The prepared 2026 estimate is similar to the current baseline, but the portal can still produce a different monthly amount."

Note: These are review directions, not predicted cash flows. The Belastingdienst performs its own recalculation based on the full submitted dataset. Only the live portal result and replacement beschikking determine the actual future payment/refund amount and timing.

## Reminder

Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.
