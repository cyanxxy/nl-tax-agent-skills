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

- Single taxpayer: EUR 57,684
- Fiscal partners (combined): EUR 115,368

The heffingsvrij vermogen is deducted from the rendementsgrondslag to determine the grondslag sparen en beleggen.

## Drempel schulden

- Single taxpayer: EUR 3,800
- Fiscal partners (combined): EUR 7,600

Only the amount of box 3 debts above this threshold is treated as aftrekbare schulden.

## Asset categories and fictitious return percentages

Three categories determine the belastbaar rendement:

### Categorie I -- Banktegoeden (savings and bank deposits)

- Includes: savings accounts, current accounts, deposits, term deposits
- Fictitious return percentage for 2025: **1.37%**

### Categorie II -- Overige bezittingen (other assets)

- Includes: investments, listed and unlisted securities, crypto-assets, real estate (not being own home), receivables (vorderingen), rights to periodic payments, other assets
- Fictitious return percentage for 2025: **5.88%**

### Categorie III -- Schulden (debts)

- Includes: all debts EXCEPT mortgage debt on the own home (eigenwoningschuld, which belongs in box 1)
- Fictitious return percentage for 2025: **2.70%**

## Calculation method

Use the Belastingdienst step model. Do not present this as a free-form weighted-average shortcut.

1. **Bereken het belastbaar rendement**
   - Banktegoeden * 1.37%
   - Overige bezittingen * 5.88%
   - Aftrekbare schulden * 2.70%, subtracted from the asset returns
   - Aftrekbare schulden = total box 3 debts minus the debt threshold
2. **Bereken de rendementsgrondslag**
   - Rendementsgrondslag = banktegoeden + overige bezittingen - aftrekbare schulden
3. **Bereken de grondslag sparen en beleggen**
   - Grondslag sparen en beleggen = rendementsgrondslag - heffingsvrij vermogen
   - If the result is negative, use EUR 0
4. **Bereken het aandeel in de rendementsgrondslag**
   - Aandeel = taxpayer's share of the grondslag sparen en beleggen divided by the rendementsgrondslag
   - Round the percentage to 2 decimals; do not truncate
5. **Bereken het voordeel uit sparen en beleggen**
   - Box 3 income = belastbaar rendement * aandeel in de rendementsgrondslag
6. **Bereken hoeveel belasting moet worden betaald**
   - Box 3 tax = box 3 income * 36%

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
2. Calculate aftrekbare schulden after the debt threshold
3. Calculate belastbaar rendement by category
4. Calculate rendementsgrondslag, grondslag sparen en beleggen, aandeel in de rendementsgrondslag, box 3 income, and tax
5. If fiscal partners are present, compute allocation scenarios for the grondslag sparen en beleggen
6. Always present the full breakdown using the official step names above

## Common failure

Do not subtract the full debt amount. First subtract the debt threshold and use only aftrekbare schulden in the return and rendementsgrondslag calculations.

Do not apply the heffingsvrij vermogen before calculating the belastbaar rendement. The heffingsvrij vermogen is only deducted to determine the grondslag sparen en beleggen.
