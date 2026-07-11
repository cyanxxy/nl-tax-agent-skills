# Rule note: How to change an existing voorlopige aanslag 2026

source_id: bd_provisional_change_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Rule

An existing voorlopige aanslag for 2026 is changed through the same "Voorlopige aanslag aanvragen of wijzigen" entry in Mijn Belastingdienst (request and change share one combined flow). Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

## CRITICAL RULE -- Every field must be complete

A change requires all applicable categories, not only the changed item. The portal MAY offer to pre-fill figures from the taxpayer's most recent aangifte (the data from two years prior) when they opt in -- it does not carry forward the figures from the current voorlopige aanslag. Whether the form opens blank or pre-filled, the workpack must prepare, and the taxpayer must verify, the COMPLETE dataset:

- All income sources (employment, pension, benefits, self-employment)
- All deductions (mortgage interest, alimentatie, premiums, etc.)
- All box 3 assets and debts

Official guidance states that all data must be present in the form, including data that does not change ("Houd er rekening mee dat u alle gegevens moet invullen. Ook de gegevens die niet wijzigen"), so the workpack must always cover the full dataset.

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

1. Log in to Mijn Belastingdienst
2. Open "Voorlopige aanslag aanvragen of wijzigen" for 2026 (request and change share one combined flow)
3. Choose to change (wijzigen) the existing 2026 voorlopige aanslag; optionally accept the offer to pre-fill prior-year figures
4. Prepare and verify the complete dataset: all applicable income, deductions, and box 3 categories, not only the changed item
5. Review the new summary and adjusted monthly amount
6. Sign and send (ondertekenen en verzenden)

## Developer instruction

When building a workpack for changing a voorlopige aanslag 2026:

1. Tell the user upfront: prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item
2. If previous workpack data is available, pre-populate the workpack as a starting point but have the user confirm every field (note that the portal itself may also offer to pre-fill prior-year figures)
3. Clearly show what changed between the old and new estimates
4. Present the delta: old monthly amount vs. new monthly amount
5. Remind the user that a new beschikking will be sent and payments will be adjusted
6. For box 3 data, follow box3-provisional.md rules

## Common failure

Do not prepare only the changed fields. The Belastingdienst guidance requires all data to be filled in again, including unchanged data. Always ensure the workpack contains the full dataset.
