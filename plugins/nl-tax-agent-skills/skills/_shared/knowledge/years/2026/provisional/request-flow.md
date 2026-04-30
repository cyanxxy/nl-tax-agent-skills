# Rule note: How to request a voorlopige aanslag 2026

source_ids: bd_provisional_landing_2026, bd_provisional_request_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

A voorlopige aanslag (provisional assessment) for 2026 can be requested through a 4-step online process at Mijn Belastingdienst. The result is a monthly payment or refund based on the taxpayer's estimated tax position for the coming year. All amounts entered are ESTIMATES for the year 2026.

## When to request

A voorlopige aanslag should be requested when:

- You expect to owe tax (e.g., income from multiple sources, no or insufficient payroll tax withheld)
- You want an advance refund for expected deductions (e.g., new mortgage interest deduction, alimony payments)
- You have self-employment income and want to spread payments across the year
- Your situation has changed significantly compared to the prior year

## 4-step online process

### Step 1 -- Log in with DigiD

Log in to Mijn Belastingdienst using DigiD. The skill does not collect, store, or process DigiD credentials. See security/digid.md for the hard prohibition on credential handling.

### Step 2 -- Enter estimated income for 2026

Enter all expected income for the year 2026, including:

- Employment income (loon uit dienstbetrekking)
- Pension income (pensioen, AOW)
- Benefits (uitkeringen, WW, WIA, bijstand)
- Self-employment income (winst uit onderneming)
- Other income sources

### Step 3 -- Enter deductions and box 3 data

Enter expected deductions and assets/debts:

- Mortgage interest (hypotheekrente) and eigenwoningforfait
- Alimony payments (alimentatie)
- Insurance premiums (lijfrentepremie, arbeidsongeschiktheidsverzekering)
- Other deductible expenses (specific care costs, study costs where applicable, gifts)
- Box 3: assets and debts as of 1 January 2026 (peildatum) -- see box3-provisional.md for details

### Step 4 -- Review summary, check amounts, and submit

- Review the calculated monthly payment or refund amount
- Verify that all entered amounts are reasonable estimates
- Submit the request

## Processing and result

- Processing time: typically within 8 weeks after submission
- The Belastingdienst issues a beschikking (decision) with the monthly payment or refund amount
- Monthly payments or refunds begin after the beschikking is issued
- The voorlopige aanslag is settled when the annual return for 2026 is filed (in 2027)

## Developer instruction

When building a workpack for requesting a voorlopige aanslag 2026:

1. Guide the user through each step in sequence
2. Collect estimated income per category
3. Collect expected deductions with explanations of what qualifies
4. For box 3, follow the rules in box3-provisional.md -- use only the fictitious return method
5. Present a summary before the user submits
6. Remind the user that all amounts are estimates and will be reconciled at annual return time
7. Do not collect or process DigiD credentials at any point

## Common failure

Do not treat the voorlopige aanslag as a final tax calculation. It is a forward-looking estimate. Do not present the outcome as definitive tax owed or refundable -- always clarify that the final settlement occurs when the annual return for 2026 is filed.
