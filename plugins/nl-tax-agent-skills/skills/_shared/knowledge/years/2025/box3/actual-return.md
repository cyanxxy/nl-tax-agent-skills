# Rule note: Box 3 actual return (werkelijk rendement) for 2025

source_ids: bd_box3_2025_actual_return, bd_fisin_box3_actual_return_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-05-15"
review_status: reviewed

## Rule

Since the Hoge Raad ruling (kerstarrest, 24 December 2021), taxpayers may opt for taxation based on their actual return (werkelijk rendement) if it is lower than the fictitious return (forfaitair rendement). For tax year 2025, the taxpayer may provide actual return data as part of the annual return.

**This option is ONLY available in the annual return (aangifte inkomstenbelasting). It is NEVER available in the voorlopige aanslag.**

## What counts as actual return

The following income and value changes constitute actual return for box 3 purposes:

- Actual interest received on bank accounts and deposits
- Dividends received (before dividend withholding tax)
- Rental income and other income from box 3 assets
- Value changes of box 3 assets during 2025, including investments, listed or unlisted securities, crypto-assets, second homes, other box 3 real estate, and assets acquired or disposed of during the year
- Interest paid on box 3 debts, as a permitted negative component
- Other actual income from box 3 assets (e.g., royalties from intellectual property held as investment)

Actual return is calculated over the total box 3 assets and debts to which the actual-return method applies. Do not deduct the heffingsvrij vermogen from the actual-return amount.

## What does NOT count as actual return

The following are excluded from the actual return calculation:

- Hypothetical or imputed returns
- Changes in value of the own home (eigenwoningforfait belongs in box 1)
- Exempt pension rights and box 1 annuity rights. Do not categorically exclude every periodic-payment or annuity-like right: non-exempt periodic-payment rights, net annuities, or net pensions may belong in box 3 and require manual review.
- Inheritance or gifts received during the year (these are not return on existing assets)
- Changes in value of assets exempt from box 3

## Costs under actual return

Costs may not be deducted when reporting actual return, except for the specific items listed below.

Do not deduct:

- Custody and administration fees (bewaarloon)
- Transaction costs for buying and selling investments
- Management fees (beheerkosten)
- Property management costs for rented real estate
- Maintenance costs for a second home or other box 3 real estate
- General financial advice costs
- Costs related to the own home
- Tax advisory costs

Permitted exceptions:

- Interest paid on box 3 debts may be included as a negative component of actual return
- A qualifying WOZ-value investment correction may reduce the year-end WOZ value, only under the official conditions

## Data required for actual return calculation

The workpack must collect the following data to enable the actual return comparison:

1. **Bank accounts:** actual interest received during 2025 (from annual statements or jaaropgaven)
2. **Dividends:** dividend amounts received per security, including dividend withholding tax
3. **Rental income:** received bare rent (kale huur) per rented box 3 property; separate any service-cost components and add the relevant value change
4. **Disposed assets:** value at the start of 2025 or acquisition value, sale proceeds, and sale date for each disposed box 3 asset
5. **Retained or acquired assets:** value at the start of 2025 or acquisition value and value at 31 December 2025 for investments, securities, crypto-assets, second homes, other box 3 real estate, and other box 3 assets where value changes count
6. **Box 3 debt interest:** interest paid on debts that belong in box 3
7. **WOZ-value investment correction:** qualifying corrections under the official conditions

## Comparison method

The workpack should enable comparison between the two methods:

1. Calculate the fictitious return (forfaitair rendement) per the standard box 3 method
2. Calculate the total actual return from all collected data, without applying heffingsvrij vermogen
3. Present both figures side by side
4. Note which method is more favorable for the taxpayer

**The official return filing environment performs the final binding comparison.** The workpack provides the calculation as informational notes only and does not make a binding election.

## Fiscal partner allocation

For fiscal partners, the actual return follows the same distribution chosen for the joint grondslag sparen en beleggen in the annual return. If partners allocate 50% of the joint grondslag to each partner, split the actual return 50/50 for the comparison. If they allocate 100% to one partner and 0% to the other, use that same distribution for actual return.

## Developer instruction

When building the workpack for box 3 with actual return data:

1. Always collect data for BOTH the fictitious and actual return methods
2. Present the fictitious return calculation in full (per the fictitious.md rules)
3. Present the actual return calculation broken down by income type
4. Include a comparison summary showing which method is lower
5. Add a note that the final election happens in the official filing environment
6. Never present the actual return option in a voorlopige aanslag workpack
7. If the taxpayer has no actual return data available, note that the fictitious method will apply by default
8. For fiscal partners, apply the same allocation percentage to actual return as to the joint grondslag sparen en beleggen

## Common failure

Do not deduct custody fees, transaction costs, management fees, maintenance costs, or adviser fees from actual return.

If total actual return is negative, present the actual return method as EUR 0 box 3 income for the comparison. Negative actual return is not carried to another year.
