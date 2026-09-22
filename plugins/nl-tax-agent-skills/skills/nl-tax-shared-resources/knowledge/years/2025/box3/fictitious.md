# Rule note: Box 3 fictitious return (forfaitair rendement) calculation 2025

source_ids: bd_box3_2025_calc, bd_fisin_box3_assets_debts_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-16"
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
- Includes contant geld only for the amount above the 2025 cash exemption (EUR 661 without fiscal partner / EUR 1,322 with fiscal partner), and includes the non-exempt part of green savings.
- Also includes official bank-asset edge cases such as premiedepots, a taxpayer's share in a VvE reserve fund, and money on notary or bailiff third-party accounts.
- Fictitious return percentage for 2025: **1.37%**

### Categorie II -- Overige bezittingen (other assets)

- Includes: investments, listed and unlisted securities, crypto-assets, real estate (not being own home), receivables (vorderingen), rights to periodic payments, other assets
- Receivables/loans require exception checks. Official guidance excludes certain receivables, including receivables between fiscal partners or between parents and minor children, and usually non-callable inheritance receivables.
- Includes only the non-exempt part of green investments. The 2025 green-investment exemption shown in the official box 3 example is EUR 26,312 per person / EUR 52,624 for fiscal partners.
- Fictitious return percentage for 2025: **5.88%**

### Categorie III -- Schulden (debts)

- Include only debts that the official 2025 Box 3 guidance says belong in Box
  3, after an explicit qualification screen. Examples include consumer loans,
  negative bank balances, study-finance debts, financing for Box 3 assets,
  repayable benefits, and inheritance tax.
- Do **not** use the shortcut "all debts except the own-home mortgage." Excluded
  items include qualifying own-home debt and qualifying former-home residual
  debt in Box 1, non-callable surviving-spouse inheritance debt, short current
  liabilities, deductible maintenance obligations, most Dutch tax debts,
  business debts, debts connected with Box 2/terbeschikkingstelling/other work,
  and debts owed to a fiscal partner or minor child. The official list contains
  further conditions and exceptions.
- Keep any debt whose category or callability is unresolved out of trusted
  totals and ask a focused question or mark it for manual portal review. Apply
  the debt threshold only after qualifying debts have been identified.
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
   - Use the percentage as displayed in the official examples: truncate toward zero to 2 decimals
5. **Bereken het voordeel uit sparen en beleggen**
   - Box 3 income = belastbaar rendement * aandeel in de rendementsgrondslag
6. **Bereken hoeveel belasting moet worden betaald**
   - Box 3 tax = box 3 income * 36%

## Box 3 tax rate

The box 3 tax rate for 2025 is **36%**, applied to the calculated fictitious return.

## Partner allocation

When taxpayers qualify as fiscal partners:

- The joint grondslag sparen en beleggen can be freely allocated between partners
- Any split from 0% to 100% is permitted, as long as the allocation of the joint grondslag totals 100%
- Partners should review allocation scenarios for the lowest combined result after all tax and credit effects
- The allocation is chosen at the time of filing and applies to the joint box 3 base; do not split asset-by-asset in the field map
- Both partners must use the same allocation ratio in their respective returns

## Developer instruction

When building the workpack for box 3:

1. Collect the value of all assets and debts per category on peildatum 1 January 2025
2. Separately identify green investments/savings and cash amounts because exemptions can change what is included in banktegoeden or overige bezittingen
3. Calculate aftrekbare schulden after the debt threshold
4. Calculate belastbaar rendement by category
5. Calculate rendementsgrondslag, grondslag sparen en beleggen, aandeel in de rendementsgrondslag, box 3 income, and tax
6. If fiscal partners are present, compute allocation scenarios for the joint grondslag sparen en beleggen
7. Always present the full breakdown using the official step names above

## Common failure

Do not subtract the full debt amount. First subtract the debt threshold and use only aftrekbare schulden in the return and rendementsgrondslag calculations.

Do not apply the heffingsvrij vermogen before calculating the belastbaar rendement. The heffingsvrij vermogen is only deducted to determine the grondslag sparen en beleggen.

Do not allocate individual assets or debts between fiscal partners for the fictitious calculation. Allocate the joint grondslag sparen en beleggen.
