# Rule note: How to request a voorlopige aanslag 2026

source_ids: bd_provisional_landing_2026, bd_provisional_request_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

A voorlopige aanslag (provisional assessment) for 2026 can be requested through a 4-step online process at Mijn Belastingdienst. The portal shows an estimated payment or refund and, after processing, the beschikking controls the actual amount and timing. All amounts entered are ESTIMATES for the year 2026.

## When a request may be useful to discuss

A taxpayer may want to review a request when:

- You expect to owe tax (e.g., income from multiple sources, no or insufficient payroll tax withheld)
- You want an advance refund for expected deductions (e.g., new mortgage interest deduction, alimony payments)
- You have self-employment income and want to spread payments across the year
- Your situation has changed significantly compared to the prior year

## 4-step online process

### Step 1 -- Prepare

Prepare the estimated income, deduction, own-home, and box 3 information for 2026.

### Step 2 -- Log in

Log in to Mijn Belastingdienst.

### Step 3 -- Fill in the request

Enter all expected income for the year 2026, including:

- Employment income (loon uit dienstbetrekking)
- Pension income (pensioen, AOW)
- Benefits (uitkeringen, WW, WIA, bijstand)
- Self-employment income (winst uit onderneming)
- Other income sources

Enter expected deductions, assets, and candidate debts:

- Own-home components: WOZ value with peildatum 1 January 2025,
  eigenwoningforfait, mortgage interest, qualifying financing costs, periodic
  erfpacht/opstal/beklemming, and any Hillen review
- Alimony payments (alimentatie)
- Insurance premiums (lijfrentepremie, arbeidsongeschiktheidsverzekering)
- Other deductible expenses (specific care costs, gifts, and other officially deductible items)
- Box 3: assets and qualifying debts as of 1 January 2026 (peildatum). Screen
  each debt against the official inclusion/exclusion list; unresolved debts do
  not enter accepted totals -- see box3-provisional.md

### Step 4 -- Sign and send

- Review the calculated monthly payment or refund amount
- Verify that all entered amounts are reasonable estimates
- Sign and send the request

## Processing and result

- Processing time: usually within 4 weeks after submission; sometimes longer, but within 8 weeks
- The Belastingdienst issues a beschikking (decision) with the monthly payment or refund amount
- The beschikking states whether and when payments or refunds start; do not
  turn the portal preview into a payment promise
- If the taxpayer has a 2026 filing obligation or otherwise files, the annual
  assessment reconciles the provisional amounts. A provisional assessment
  does not by itself make annual filing mandatory for everyone.

## Developer instruction

When building a workpack for requesting a voorlopige aanslag 2026:

1. Cover each applicable portal step progressively while adapting the next
   question to facts already provided; this is not a fixed interview order
2. Collect estimated income per category
3. Collect expected deductions with explanations of what qualifies
4. For box 3, follow the rules in box3-provisional.md -- use only the fictitious return method
5. Present a summary before the user submits
6. Remind the user that all amounts are estimates; the live portal and
   beschikking control the future payment/refund, and annual reconciliation is
   conditional on a return being filed

## Common failure

Do not treat the voorlopige aanslag as a final tax calculation. It is a
forward-looking estimate. Do not present the preview as a definitive amount or
payment schedule; the beschikking controls. Do not say that every taxpayer
must file solely because a provisional assessment exists.
