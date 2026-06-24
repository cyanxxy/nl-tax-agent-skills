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
| Other income           | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Own-home deduction     | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Box 3 assets (Cat I)   | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Box 3 assets (Cat II)  | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Box 3 debts (Cat III)  | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Alimentatie            | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Other deductions       | EUR           | [F/U/B/?]      | EUR              | [F/U/A/?]     | EUR           |       |
| Partner changes        | [description] | [F/U/B/?]      | [description]    | [F/U/A/?]     | [description] |       |

### Label key

- All "Baseline" values are labeled as **from-baseline**
- All "Current Estimate" values are labeled as **estimate**
- Delta = Current Estimate minus Baseline for workpack review only
- Any row where either side is `?` is also listed in the workpack's Missing information section.

## Impact

[Summary of expected directional impact on monthly payment or refund based on the workpack comparison]

- If net tax position increases: "Based on these changes, your estimated tax liability for 2026 is higher than the current voorlopige aanslag. This may result in higher monthly payments."
- If net tax position decreases: "Based on these changes, your estimated tax liability for 2026 is lower than the current voorlopige aanslag. This may result in lower monthly payments or a higher monthly refund."
- If net tax position is unchanged: "Based on these changes, your estimated tax position for 2026 is similar to the current voorlopige aanslag. No significant change in monthly payments is expected."

Note: The Belastingdienst performs its own recalculation based on the full submitted dataset. The actual adjusted monthly amount may differ from this estimate.

## Reminder

When changing your voorlopige aanslag, enter ALL data again; omitted data defaults to zero because the new VA replaces the old one entirely.
