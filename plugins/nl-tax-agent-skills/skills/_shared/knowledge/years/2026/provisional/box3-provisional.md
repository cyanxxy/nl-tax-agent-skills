# Rule note: Box 3 for the voorlopige aanslag 2026 -- fictitious return only

source_id: bd_box3_2026_provisional
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

For the 2026 voorlopige aanslag, box 3 is calculated using ONLY the fictitious return method (forfaitair rendement). Werkelijk rendement (actual return) is not part of the provisional calculation.

> For the 2026 voorlopige aanslag, use the box 3 categories and values required for the provisional fictitious calculation. Werkelijk rendement is not part of the provisional calculation; it may become relevant later in the annual 2026 return.

## HARD RULE -- No werkelijk rendement in provisional 2026

Do NOT collect or enter werkelijk rendement for the 2026 voorlopige aanslag.

- Werkelijk rendement is not part of the provisional calculation
- It may become relevant later in the annual 2026 return (filed in 2027)
- If the user asks about actual return for the provisional 2026 assessment: explain that it is not applicable here and will only potentially apply at annual return time

This distinction is critical and must be enforced in all provisional assessment flows.

## Reference date (peildatum)

The peildatum for the 2026 provisional assessment is **1 January 2026**. All assets and debts are valued as of this date.

## Heffingsvrij vermogen (tax-free allowance) 2026

- Single taxpayer: EUR 57,000
- Fiscal partners (combined): EUR 114,000
- _Pending verification from 2026 source snapshot -- amount may differ from 2025_

The heffingsvrij vermogen is deducted from the rendementsgrondslag before the fictitious return is applied.

## Asset categories and fictitious return percentages

Three categories determine the weighted average fictitious return for the provisional assessment:

### Categorie I -- Banktegoeden (savings and bank deposits)

- Includes: savings accounts, current accounts, deposits, term deposits
- Fictitious return percentage for 2026 provisional: **~0.36%**
- _Pending verification from 2026 source snapshot_

### Categorie II -- Overige bezittingen (other assets)

- Includes: investments, listed and unlisted securities, crypto-assets, real estate (not being own home), receivables (vorderingen), rights to periodic payments, other assets
- Fictitious return percentage for 2026 provisional: **~6.04%**
- _Pending verification from 2026 source snapshot_

### Categorie III -- Schulden (debts)

- Includes: all debts EXCEPT mortgage debt on the own home (eigenwoningschuld, which belongs in box 1)
- Fictitious return percentage for 2026 provisional: **~2.47%**
- _Pending verification from 2026 source snapshot_

## Box 3 tax rate 2026

- Box 3 tax rate: **36%**
- _Pending verification from 2026 source snapshot_
- Applied to the calculated fictitious return (forfaitair rendement)

## Calculation method for provisional assessment

1. **Determine totals per category** on peildatum 1 January 2026
2. **Calculate weighted fictitious return percentage:**
   - (Categorie I total * 0.36% + Categorie II total * 6.04% - Categorie III total * 2.47%) / (Categorie I total + Categorie II total - Categorie III total)
3. **Determine rendementsgrondslag:**
   - Rendementsgrondslag = total assets (Categorie I + Categorie II) minus schulden (Categorie III) minus heffingsvrij vermogen
   - If the result is negative or zero, the rendementsgrondslag is EUR 0 and no box 3 tax is due
4. **Calculate forfaitair rendement:**
   - Forfaitair rendement = rendementsgrondslag * weighted fictitious return percentage
5. **Calculate box 3 tax:**
   - Box 3 tax = forfaitair rendement * 36%

## Partner allocation

When taxpayers qualify as fiscal partners:

- Box 3 assets and debts can be freely allocated between partners
- Any split from 0% to 100% is permitted, as long as the combined totals equal 100%
- Partners should choose the allocation that results in the lowest combined box 3 tax
- The allocation applies to the entire box 3 base, not per individual asset
- Both partners must use the same allocation ratio

## Developer instruction

When building the workpack for box 3 in the voorlopige aanslag 2026:

1. Collect the value of all assets and debts per category on peildatum 1 January 2026
2. Use ONLY the fictitious return method -- do not offer or collect werkelijk rendement
3. If the user asks about actual return (werkelijk rendement), respond with:
   - "Werkelijk rendement is not part of the 2026 provisional assessment. It may become relevant when filing the annual 2026 return in 2027."
4. Calculate the weighted fictitious return percentage based on the actual composition
5. Apply the heffingsvrij vermogen deduction to the rendementsgrondslag
6. If fiscal partners are present, compute the optimal allocation split
7. Present the full breakdown: totals per category, weighted percentage, rendementsgrondslag, forfaitair rendement, and tax amount
8. Mark all amounts as provisional and pending verification

## Common failure

Do not apply the heffingsvrij vermogen before calculating the weighted return percentage. The weighting is based on the full asset and debt composition; the heffingsvrij vermogen is only deducted from the rendementsgrondslag in step 3.

Do not collect werkelijk rendement data in the provisional flow. This is the most critical enforcement rule for this file.
