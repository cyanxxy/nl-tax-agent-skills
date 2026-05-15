# Rule note: Box 3 for the voorlopige aanslag 2026 -- fictitious return only

source_id: bd_box3_2026_provisional
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-05-15"
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

- Single taxpayer: EUR 59,357
- Fiscal partners (combined): EUR 118,714

The heffingsvrij vermogen is deducted from the rendementsgrondslag to determine the grondslag sparen en beleggen.

## Drempel schulden

- Single taxpayer: EUR 3,800
- Fiscal partners (combined): EUR 7,600

Only the amount of box 3 debts above this threshold is treated as aftrekbare schulden.

## Asset categories and fictitious return percentages

Three categories determine the belastbaar rendement for the provisional assessment:

### Categorie I -- Banktegoeden (savings and bank deposits)

- Includes: savings accounts, current accounts, deposits, term deposits
- Includes contant geld only for the amount above the cash exemption, and includes the non-exempt part of green savings.
- Fictitious return percentage for 2026 provisional: **1.28%**

### Categorie II -- Overige bezittingen (other assets)

- Includes: investments, listed and unlisted securities, crypto-assets, real estate (not being own home), receivables (vorderingen), rights to periodic payments, other assets
- Includes only the non-exempt part of green investments. The 2026 green-investment exemption shown in the official box 3 example is EUR 26,715 per person / EUR 53,430 for fiscal partners.
- Fictitious return percentage for 2026 provisional: **6.00%**

### Categorie III -- Schulden (debts)

- Includes: all debts EXCEPT mortgage debt on the own home (eigenwoningschuld, which belongs in box 1)
- Fictitious return percentage for 2026 provisional: **2.70%**

## Box 3 tax rate 2026

- Box 3 tax rate: **36%**
- Applied to the calculated fictitious return (forfaitair rendement)

The percentages for banktegoeden and schulden are provisional for the 2026 provisional assessment and are expected to be finalized for the definitive 2026 annual assessment. The percentage for overige bezittingen is fixed for this provisional calculation.

## Calculation method for provisional assessment

1. **Bereken het belastbaar rendement**
   - Banktegoeden * 1.28%
   - Overige bezittingen * 6.00%
   - Aftrekbare schulden * 2.70%, subtracted from the asset returns
   - Aftrekbare schulden = total box 3 debts minus the debt threshold
2. **Bereken de rendementsgrondslag**
   - Rendementsgrondslag = banktegoeden + overige bezittingen - aftrekbare schulden
3. **Bereken de grondslag sparen en beleggen**
   - Grondslag sparen en beleggen = rendementsgrondslag - heffingsvrij vermogen
   - If the result is negative or zero, use EUR 0 and no box 3 tax is due
4. **Bereken het aandeel in de rendementsgrondslag**
   - Aandeel = taxpayer's share of the grondslag sparen en beleggen divided by the rendementsgrondslag
   - Use the percentage as displayed in the official examples: truncate toward zero to 2 decimals
5. **Bereken het voordeel uit sparen en beleggen**
   - Box 3 income = belastbaar rendement * aandeel in de rendementsgrondslag
6. **Bereken hoeveel belasting moet worden betaald**
   - Box 3 tax = box 3 income * 36%

## Partner allocation

When taxpayers qualify as fiscal partners:

- The joint grondslag sparen en beleggen can be freely allocated between partners
- Any split from 0% to 100% is permitted, as long as the allocation of the joint grondslag totals 100%
- Partners should review allocation scenarios for the lowest combined result after all tax and credit effects
- The allocation applies to the joint box 3 base, not per individual asset or debt
- Both partners must use the same allocation ratio

## Developer instruction

When building the workpack for box 3 in the voorlopige aanslag 2026:

1. Collect the value of all assets and debts per category on peildatum 1 January 2026
2. Use ONLY the fictitious return method -- do not offer or collect werkelijk rendement
3. If the user asks about actual return (werkelijk rendement), respond with:
   - "Werkelijk rendement is not part of the 2026 provisional assessment. It may become relevant when filing the annual 2026 return in 2027."
4. Separately identify green investments/savings and cash amounts because exemptions can change what is included in banktegoeden or overige bezittingen
5. Calculate aftrekbare schulden after the debt threshold
6. Calculate belastbaar rendement, rendementsgrondslag, grondslag sparen en beleggen, aandeel in de rendementsgrondslag, box 3 income, and tax
7. If fiscal partners are present, compute allocation scenarios for the joint grondslag sparen en beleggen
8. Present the full breakdown using the official step names above
9. Mark the output as a provisional-assessment estimate

## Common failure

Do not subtract the full debt amount. First subtract the debt threshold and use only aftrekbare schulden in the return and rendementsgrondslag calculations.

Do not apply the heffingsvrij vermogen before calculating the belastbaar rendement. The heffingsvrij vermogen is only deducted to determine the grondslag sparen en beleggen.

Do not collect werkelijk rendement data in the provisional flow. This is the most critical enforcement rule for this file.

Do not allocate individual assets or debts between fiscal partners for the fictitious calculation. Allocate the joint grondslag sparen en beleggen.
