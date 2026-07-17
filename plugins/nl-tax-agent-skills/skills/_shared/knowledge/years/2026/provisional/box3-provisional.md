# Rule note: Box 3 for the voorlopige aanslag 2026 -- fictitious return only

source_ids: bd_box3_2026_provisional, bd_fisin_box3_assets_debts_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

For the 2026 voorlopige aanslag, box 3 is calculated using ONLY the fictitious return method (forfaitair rendement).

Use only this explanatory note: "Werkelijk rendement is not part of provisional 2026."

## Actual-return boundary

Reject any field, input prompt, calculation, or method-choice wording that tries
to use werkelijk rendement in this provisional workflow.

## Reference date (peildatum)

The peildatum for the 2026 provisional assessment is **1 January 2026**. Value
assets and candidate debts at this date, then apply the debt
inclusion/exclusion screen before any debt enters the Box 3 total.

## Heffingsvrij vermogen (tax-free allowance) 2026

- Single taxpayer: EUR 59,357
- Fiscal partners (combined): EUR 118,714

The heffingsvrij vermogen is deducted from the rendementsgrondslag to determine the grondslag sparen en beleggen.

## Drempel schulden

- Single taxpayer: EUR 3,800
- Fiscal partners (combined): EUR 7,600

Only the amount of accepted qualifying Box 3 debts above this threshold is
treated as aftrekbare schulden.

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

- Include only debts that pass the official Box 3 debt screen. Examples may
  include consumer debt, a negative bank balance, financing for investments or
  a second home, and a mortgage debt that is not deductible in Box 1.
- Exclude debts that belong in Box 1 or Box 2 and other published exclusions,
  including most Dutch tax debts. Inheritance-tax debt is a published example
  that can belong in Box 3, so a generic `tax debt` label is not enough.
- Do not infer qualification merely because a debt is not an own-home
  mortgage. Record the debt type and purpose, check it against the official
  list, and keep an unresolved row out of accepted totals as `manual_review`.
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
   - Aftrekbare schulden = total accepted qualifying Box 3 debts minus the debt threshold
2. **Bereken de rendementsgrondslag**
   - Rendementsgrondslag = banktegoeden + overige bezittingen - aftrekbare schulden
3. **Bereken de grondslag sparen en beleggen**
   - Grondslag sparen en beleggen = rendementsgrondslag - heffingsvrij vermogen
   - If the result is negative or zero, use EUR 0 and no box 3 tax is due
4. **Bereken het aandeel in de rendementsgrondslag**
   - Aandeel = taxpayer's share of the grondslag sparen en beleggen divided by the rendementsgrondslag
   - The published 2026 page is internally inconsistent: the general step says
     to round to 3 decimals, while its worked examples say and display 2
     decimals. Do not present either convention as the portal's guaranteed
     binding rule. A workpack may show a clearly labeled review estimate and
     record which display convention it used, but the live Mijn Belastingdienst
     calculation and the resulting beschikking are authoritative.
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

1. Collect the value of all assets and candidate debts per category on
   peildatum 1 January 2026; accept a debt into Box 3 totals only after the
   official inclusion/exclusion screen, and keep unresolved debts under manual
   review
2. Use ONLY the fictitious return method
3. If the user asks about actual return (werkelijk rendement), respond with the canonical redirect: "Werkelijk rendement is not part of the 2026 voorlopige aanslag. It may become relevant when filing the annual 2026 return in 2027." (The shorter in-workpack note — "Werkelijk rendement is not part of provisional 2026." — stays as the explanatory line written into the workpack; see line 14 above.)
4. Separately identify green investments/savings and cash amounts because exemptions can change what is included in banktegoeden or overige bezittingen
5. Calculate aftrekbare schulden after the debt threshold using accepted
   qualifying Box 3 debts only
6. Calculate belastbaar rendement, rendementsgrondslag, grondslag sparen en beleggen, aandeel in de rendementsgrondslag, box 3 income, and tax
7. If fiscal partners are present, compute allocation scenarios for the joint grondslag sparen en beleggen
8. Present the full breakdown using the official step names above
9. Mark the output as a provisional-assessment estimate; where the internal
   rounding inconsistency could change the display, state that the live portal
   and resulting beschikking control

## Common failure

Do not treat every non-own-home debt as a Box 3 debt. Apply the official
inclusion/exclusion screen first; unresolved debts stay out of accepted totals
and require manual review. Then subtract the debt threshold and use only
aftrekbare schulden in the return and rendementsgrondslag calculations.

Do not apply the heffingsvrij vermogen before calculating the belastbaar rendement. The heffingsvrij vermogen is only deducted to determine the grondslag sparen en beleggen.

Reject werkelijk-rendement inputs, fields, calculations, and method choices in the provisional flow.

Do not canonize 3-decimal or 2-decimal display rounding from the internally
inconsistent publication. Use estimates for review and defer to the live portal
and beschikking.

Do not allocate individual assets or debts between fiscal partners for the fictitious calculation. Allocate the joint grondslag sparen en beleggen.
