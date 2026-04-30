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
- Rental income from real estate (net of directly attributable costs)
- Realized capital gains and losses on sale of investments, securities, and crypto-assets
- Unrealized value changes (mark-to-market) for listed securities between 1 January and 31 December 2025
- Other actual income from box 3 assets (e.g., royalties from intellectual property held as investment)

## What does NOT count as actual return

The following are excluded from the actual return calculation:

- Hypothetical or imputed returns
- Changes in value of the own home (eigenwoningforfait belongs in box 1)
- Pension rights and annuity rights (these are box 1)
- Inheritance or gifts received during the year (these are not return on existing assets)
- Changes in value of assets exempt from box 3

## Deductible costs under actual return

Costs that are directly attributable to box 3 assets may be deducted:

- Custody and administration fees (bewaarloon)
- Transaction costs for buying and selling investments
- Property management costs for rented real estate
- Other costs with a direct causal link to generating box 3 income

Costs that are NOT deductible:

- General financial advice costs
- Costs related to the own home
- Tax advisory costs

## Data required for actual return calculation

The workpack must collect the following data to enable the actual return comparison:

1. **Bank accounts:** actual interest received during 2025 (from annual statements or jaaropgaven)
2. **Dividends:** dividend amounts received per security, including dividend withholding tax
3. **Rental income:** gross rental income and directly attributable costs per property
4. **Realized gains/losses:** purchase price and sale price for each disposed asset
5. **Unrealized value changes:** value of listed securities on 1 January 2025 and 31 December 2025 (from broker/bank statements)
6. **Deductible costs:** custody fees, transaction costs, and other directly attributable costs with supporting documentation

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

Do not assume that a negative actual return automatically means the taxpayer pays zero box 3 tax. The comparison is between the two methods: if actual return is negative and fictitious return is positive, the taxpayer benefits from claiming actual return (resulting in EUR 0 or a negative amount). However, the official filing environment determines the final outcome -- the workpack should present both calculations without making the election.
