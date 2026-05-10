# Rule note: Box 3 actual return (werkelijk rendement) for 2025

source_ids: bd_box3_2025_actual_return, bd_fisin_box3_actual_return_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-04-30"
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

## What does NOT count as actual return

The following are excluded from the actual return calculation:

- Hypothetical or imputed returns
- Changes in value of the own home (eigenwoningforfait belongs in box 1)
- Pension rights and annuity rights (these are box 1)
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
3. **Rental income:** gross rental income per property
4. **Disposed assets:** value at the start of 2025 or acquisition value, sale proceeds, and sale date for each disposed box 3 asset
5. **Retained or acquired assets:** value at the start of 2025 or acquisition value and value at 31 December 2025 for investments, securities, crypto-assets, second homes, other box 3 real estate, and other box 3 assets where value changes count
6. **Box 3 debt interest:** interest paid on debts that belong in box 3
7. **WOZ-value investment correction:** qualifying corrections under the official conditions

## Comparison method

The workpack should enable comparison between the two methods:

1. Calculate the fictitious return (forfaitair rendement) per the standard box 3 method
2. Calculate the total actual return from all collected data
3. Present both figures side by side
4. Note which method is more favorable for the taxpayer

**The official return filing environment performs the final binding comparison.** The workpack provides the calculation as informational notes only and does not make a binding election.

## Developer instruction

When building the workpack for box 3 with actual return data:

1. Always collect data for BOTH the fictitious and actual return methods
2. Present the fictitious return calculation in full (per the fictitious.md rules)
3. Present the actual return calculation broken down by income type
4. Include a comparison summary showing which method is lower
5. Add a note that the final election happens in the official filing environment
6. Never present the actual return option in a voorlopige aanslag workpack
7. If the taxpayer has no actual return data available, note that the fictitious method will apply by default

## Common failure

Do not deduct custody fees, transaction costs, management fees, maintenance costs, or adviser fees from actual return.

If total actual return is negative, present the actual return method as EUR 0 box 3 income for the comparison. Negative actual return is not carried to another year.
