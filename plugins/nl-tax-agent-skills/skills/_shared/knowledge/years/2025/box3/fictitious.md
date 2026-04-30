# Rule note: Box 3 fictitious return (forfaitair rendement) calculation 2025

source_id: bd_box3_2025_calc
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

Box 3 income from savings and investments (inkomen uit sparen en beleggen) is calculated using a fictitious return (forfaitair rendement) based on the composition of the taxpayer's assets and debts on the reference date.

## Reference date (peildatum)

The peildatum for tax year 2025 is **1 January 2025**. All assets and debts are valued as of this date. Changes during the year do not affect the box 3 calculation under the fictitious method.

## Heffingsvrij vermogen (tax-free allowance)

- Single taxpayer: EUR 57,000
- Fiscal partners (combined): EUR 114,000

The heffingsvrij vermogen is deducted from the rendementsgrondslag before the fictitious return is applied.

## Asset categories and fictitious return percentages

Three categories determine the weighted average fictitious return:

### Categorie I -- Banktegoeden (savings and bank deposits)

- Includes: savings accounts, current accounts, deposits, term deposits
- Fictitious return percentage for 2025: **0.36%**
- _Verify against source snapshot -- this percentage may be refined when the definitive percentage is published_

### Categorie II -- Overige bezittingen (other assets)

- Includes: investments, listed and unlisted securities, crypto-assets, real estate (not being own home), receivables (vorderingen), rights to periodic payments, other assets
- Fictitious return percentage for 2025: **6.04%**
- _Verify against source snapshot -- this percentage may be refined when the definitive percentage is published_

### Categorie III -- Schulden (debts)

- Includes: all debts EXCEPT mortgage debt on the own home (eigenwoningschuld, which belongs in box 1)
- Fictitious return percentage for 2025: **2.47%**
- _Verify against source snapshot -- this percentage may be refined when the definitive percentage is published_

## Calculation method

The fictitious return is a weighted average based on the composition of assets and debts:

1. **Determine totals per category** on peildatum 1 January 2025
2. **Calculate weighted fictitious return percentage:**
   - (Categorie I total * 0.36% + Categorie II total * 6.04% - Categorie III total * 2.47%) / (Categorie I total + Categorie II total - Categorie III total)
3. **Determine rendementsgrondslag:**
   - Rendementsgrondslag = total assets (Categorie I + Categorie II) minus schulden (Categorie III) minus heffingsvrij vermogen
   - If the result is negative, the rendementsgrondslag is EUR 0
4. **Calculate forfaitair rendement:**
   - Forfaitair rendement = rendementsgrondslag * weighted fictitious return percentage
5. **Calculate box 3 tax:**
   - Box 3 tax = forfaitair rendement * 36%

## Box 3 tax rate

The box 3 tax rate for 2025 is **36%**, applied to the calculated fictitious return.

## Partner allocation

When taxpayers qualify as fiscal partners:

- Box 3 assets and debts can be freely allocated between partners
- Any split from 0% to 100% is permitted, as long as the combined totals equal 100%
- Partners should choose the allocation that results in the lowest combined box 3 tax
- The allocation is chosen at the time of filing and applies to ALL box 3 assets and debts uniformly (you cannot split asset-by-asset; the chosen percentage applies to the entire box 3 base)
- Both partners must use the same allocation ratio in their respective returns

## Developer instruction

When building the workpack for box 3:

1. Collect the value of all assets and debts per category on peildatum 1 January 2025
2. Calculate the weighted fictitious return percentage based on the actual composition
3. Apply the heffingsvrij vermogen deduction
4. If fiscal partners are present, compute the optimal allocation split
5. Always present the full breakdown: totals per category, weighted percentage, rendementsgrondslag, forfaitair rendement, and tax amount

## Common failure

Do not apply the heffingsvrij vermogen before calculating the weighted return percentage. The weighting is based on the full asset and debt composition; the heffingsvrij vermogen is only deducted from the rendementsgrondslag in step 3.
