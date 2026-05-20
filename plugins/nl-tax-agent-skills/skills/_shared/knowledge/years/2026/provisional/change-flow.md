# Rule note: How to change an existing voorlopige aanslag 2026

source_id: bd_provisional_change_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

An existing voorlopige aanslag for 2026 can be changed through the same Mijn Belastingdienst portal. When changing, the taxpayer must enter ALL data again -- not just the changed items. The new provisional assessment replaces the old one entirely.

## CRITICAL RULE -- Full re-entry required

When changing a voorlopige aanslag, the portal does not carry forward previous entries. The taxpayer must re-enter:

- All income sources (employment, pension, benefits, self-employment)
- All deductions (mortgage interest, alimentatie, premiums, etc.)
- All box 3 assets and debts

The new voorlopige aanslag replaces the previous one. Official guidance says all data must be filled in again, including data that does not change, so the workpack must prepare the complete dataset.

## Common reasons to change

- Salary increase or decrease
- New mortgage, mortgage change, or mortgage payoff
- Partner situation change (marriage, registered partnership, separation, divorce)
- Changed deductions (started or stopped alimony, new insurance premiums)
- Started or stopped self-employment
- Significant change in box 3 assets or debts
- Retirement or loss of employment

## Effect of a change

- A new beschikking (decision) is issued after the change is processed
- Monthly payments or refunds are recalculated for the remaining months of the year
- The Belastingdienst recalculates the assessment from the newly submitted complete dataset
- If the change results in a higher tax liability, monthly payments increase
- If the change results in a lower tax liability, monthly payments decrease or a refund may start
- Overpayments or underpayments from earlier months are spread across the remaining months

## How to change

1. Log in to Mijn Belastingdienst with DigiD
2. Navigate to the existing voorlopige aanslag 2026
3. Select "Wijzigen" (change)
4. Enter ALL income, deductions, and box 3 data from scratch
5. Review the new summary and adjusted monthly amount
6. Submit the change

## Developer instruction

When building a workpack for changing a voorlopige aanslag 2026:

1. Warn the user upfront that ALL data must be re-entered, not just the changed fields
2. If previous workpack data is available, pre-populate it as a starting point but allow the user to update every field
3. Clearly show what changed between the old and new estimates
4. Present the delta: old monthly amount vs. new monthly amount
5. Remind the user that a new beschikking will be sent and payments will be adjusted
6. For box 3 data, follow box3-provisional.md rules

## Common failure

Do not prepare only the changed fields. The Belastingdienst guidance requires all data to be filled in again, including unchanged data. Always ensure the workpack contains the full dataset.
